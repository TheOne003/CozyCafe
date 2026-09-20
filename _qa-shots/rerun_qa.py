import json, urllib.request, asyncio, base64, re, time
import websockets

PAGES = [
    ("home", "http://127.0.0.1:8080/"),
    ("about", "http://127.0.0.1:8080/about.html"),
    ("menu", "http://127.0.0.1:8080/menu.html"),
    ("contact", "http://127.0.0.1:8080/contact.html"),
]
WIDTHS = [
    (1440, 1100, False),
    (1024, 1100, False),
    (390, 1600, True),
    (360, 1600, True),
]

EXPECTED_PRICES = {
    "Butter Croissant": "$200",
    "Chocolate Croissant": "$500",
    "Cinnamon Roll": "$300",
    "Banana Bread Slice": "$1,000",
    "Blueberry Muffin": "$1,200",
    "Cheese Danish": "$1,400",
    "Toast & Jam": "$900",
    "Pancake Stack": "$800",
    "Club Sandwich": "$500",
    "Chicken Sandwich": "$200",
    "Veggie Sandwich": "$100",
    "Beef Burger": "$500",
    "Chicken Burger": "$800",
    "French Fries": "$500",
    "Meat Pie": "$800",
    "Sausage Roll": "$700",
    "Spring Rolls": "$200",
}

async def get_ws():
    tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json"))
    page = next(t for t in tabs if t.get("type") == "page")
    return page["webSocketDebuggerUrl"]

async def call(ws, method, params=None, n_holder=None):
    n_holder[0] += 1
    n = n_holder[0]
    await ws.send(json.dumps({"id": n, "method": method, "params": params or {}}))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get("id") == n:
            return resp

async def main():
    ws_url = await get_ws()
    report = {"shots": [], "checks": {}}
    async with websockets.connect(ws_url, max_size=20_000_000) as ws:
        n_holder = [0]
        await call(ws, "Page.enable", n_holder=n_holder)
        await call(ws, "Runtime.enable", n_holder=n_holder)
        await call(ws, "Console.enable", n_holder=n_holder)
        console_errors = []

        for name, url in PAGES:
            for w, h, mobile in WIDTHS:
                await call(ws, "Emulation.setDeviceMetricsOverride", {
                    "width": w, "height": h, "deviceScaleFactor": 1, "mobile": mobile
                }, n_holder=n_holder)
                await call(ws, "Page.navigate", {"url": url}, n_holder=n_holder)
                await asyncio.sleep(2.2)
                ready = (
                    "document.querySelectorAll('[data-header],[data-hero],[data-menu-hero],[data-about-hero],[data-contact-hero]')"
                    ".forEach(el => el.classList.add('is-ready'));"
                    "document.querySelectorAll('.reveal,.reveal-line').forEach(el => el.classList.add('is-visible'));"
                )
                await call(ws, "Runtime.evaluate", {"expression": ready}, n_holder=n_holder)
                await asyncio.sleep(0.4)

                metrics = await call(ws, "Runtime.evaluate", {
                    "expression": """(() => {
                      const t = document.querySelector('[data-nav-toggle]');
                      const cs = t ? getComputedStyle(t) : null;
                      const br = t ? t.getBoundingClientRect() : null;
                      const titles = [...document.querySelectorAll('h1')].map(h => h.innerText.replace(/\\s+/g,' ').trim());
                      const overflow = document.documentElement.scrollWidth > document.documentElement.clientWidth + 1;
                      return {
                        vw: innerWidth,
                        toggleDisplay: cs ? cs.display : null,
                        toggleVisible: !!(t && cs && cs.display !== 'none' && br.width > 0),
                        titles,
                        overflowX: overflow,
                        phone: (document.body.innerText.match(/\\\\+1\\\\(56\\\\)88289017/)||[])[0] || null,
                        address: document.body.innerText.includes('8834 E 34 Rd #131')
                      };
                    })()""",
                    "returnByValue": True
                }, n_holder=n_holder)
                val = metrics["result"]["result"]["value"]

                # title clip heuristic: look for suspiciously short hero fragments
                title_ok = True
                joined = " | ".join(val.get("titles") or [])
                bad_bits = ["Con hun", "Lear", "Good day", " start", "Co get", "coz."]
                for b in bad_bits:
                    if b in joined:
                        title_ok = False

                shot_path = rf"d:\CozyCafe\_qa-shots\{name}-{w}.png"
                res = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True}, n_holder=n_holder)
                open(shot_path, "wb").write(base64.b64decode(res["result"]["data"]))

                entry = {
                    "page": name, "width": w, "mobile": mobile,
                    "toggleVisible": val.get("toggleVisible"),
                    "toggleDisplay": val.get("toggleDisplay"),
                    "overflowX": val.get("overflowX"),
                    "titleOk": title_ok,
                    "titles": val.get("titles"),
                    "file": shot_path,
                }
                report["shots"].append(entry)
                print(f"OK {name} {w} toggle={val.get('toggleVisible')} overflow={val.get('overflowX')} titles={joined[:80]}")

            # page-specific deeper checks once at 1440
            if name == "menu":
                await call(ws, "Emulation.setDeviceMetricsOverride", {
                    "width": 1440, "height": 2000, "deviceScaleFactor": 1, "mobile": False
                }, n_holder=n_holder)
                await call(ws, "Page.navigate", {"url": url}, n_holder=n_holder)
                await asyncio.sleep(2.5)
                price_res = await call(ws, "Runtime.evaluate", {
                    "expression": """(() => {
                      const cards = [...document.querySelectorAll('[data-food-card]')];
                      return cards.map(c => ({
                        name: c.querySelector('.food-card__name')?.textContent?.trim(),
                        price: c.querySelector('.food-card__price')?.textContent?.trim()
                      }));
                    })()""",
                    "returnByValue": True
                }, n_holder=n_holder)
                cards = price_res["result"]["result"]["value"]
                fails = []
                for nme, price in EXPECTED_PRICES.items():
                    match = next((c for c in cards if c["name"] == nme), None)
                    if not match:
                        fails.append(f"missing {nme}")
                    elif match["price"] != price:
                        fails.append(f"{nme}: got {match['price']} want {price}")
                report["checks"]["prices"] = {"count": len(cards), "fails": fails, "ok": len(fails)==0 and len(cards)==17}
                print("PRICES", report["checks"]["prices"])

            if name == "contact":
                await call(ws, "Emulation.setDeviceMetricsOverride", {
                    "width": 390, "height": 2200, "deviceScaleFactor": 1, "mobile": True
                }, n_holder=n_holder)
                await call(ws, "Page.navigate", {"url": url}, n_holder=n_holder)
                await asyncio.sleep(2.2)
                biz = await call(ws, "Runtime.evaluate", {
                    "expression": """(() => {
                      const text = document.body.innerText;
                      return {
                        phone: text.includes('+1(56)88289017'),
                        address: text.includes('8834 E 34 Rd #131') && text.includes('Cadillac, MI 49601'),
                        form: !!document.querySelector('form, [data-contact-form], .contact-form'),
                        labels: [...document.querySelectorAll('label')].map(l => l.textContent.trim())
                      };
                    })()""",
                    "returnByValue": True
                }, n_holder=n_holder)
                report["checks"]["contact"] = biz["result"]["result"]["value"]
                print("CONTACT", report["checks"]["contact"])

        # asset / page status
        for path in ["/", "/about.html", "/menu.html", "/contact.html"]:
            code = urllib.request.urlopen(f"http://127.0.0.1:8080{path}").status
            print(f"HTTP {path} {code}")

        open(r"d:\CozyCafe\_qa-shots\report.json", "w", encoding="utf-8").write(json.dumps(report, indent=2))
        # summary
        overflows = [s for s in report["shots"] if s["overflowX"]]
        title_fails = [s for s in report["shots"] if not s["titleOk"]]
        mobile_no_toggle = [s for s in report["shots"] if s["mobile"] and not s["toggleVisible"]]
        desktop_toggle = [s for s in report["shots"] if not s["mobile"] and s["toggleVisible"]]
        print("---SUMMARY---")
        print("shots", len(report["shots"]))
        print("overflows", len(overflows))
        print("title_fails", len(title_fails))
        print("mobile_missing_toggle", len(mobile_no_toggle))
        print("desktop_showing_toggle", len(desktop_toggle))
        print("prices_ok", report["checks"].get("prices",{}).get("ok"))
        print("contact", report["checks"].get("contact"))

asyncio.run(main())
