import json, urllib.request, asyncio, base64
import websockets

async def main():
    tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json"))
    page = next(t for t in tabs if t.get("type") == "page")
    async with websockets.connect(page["webSocketDebuggerUrl"], max_size=20_000_000) as ws:
        n = [0]
        async def call(method, params=None):
            n[0] += 1
            await ws.send(json.dumps({"id": n[0], "method": method, "params": params or {}}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get("id") == n[0]:
                    return resp

        await call("Page.enable")
        await call("Emulation.setDeviceMetricsOverride", {
            "width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True
        })
        await call("Page.navigate", {"url": "http://127.0.0.1:8080/"})
        await asyncio.sleep(2.5)
        await call("Runtime.evaluate", {
            "expression": "document.querySelectorAll('[data-header],[data-hero]').forEach(el => el.classList.add('is-ready'));"
        })
        await asyncio.sleep(0.5)

        # closed menu
        res = await call("Page.captureScreenshot", {"format": "png", "fromSurface": True})
        open(r"d:\CozyCafe\_qa-shots\mobile-home.png", "wb").write(base64.b64decode(res["result"]["data"]))
        print("saved mobile-home")

        # open hamburger
        await call("Runtime.evaluate", {
            "expression": """(() => {
              const t = document.querySelector('[data-nav-toggle]');
              const m = document.querySelector('[data-nav-menu]');
              t.setAttribute('aria-expanded','true');
              m.classList.add('is-open');
              document.body.classList.add('menu-open');
              return !!m.classList.contains('is-open');
            })()"""
        })
        await asyncio.sleep(0.6)
        res = await call("Page.captureScreenshot", {"format": "png", "fromSurface": True})
        open(r"d:\CozyCafe\_qa-shots\mobile-menu-open.png", "wb").write(base64.b64decode(res["result"]["data"]))
        print("saved mobile-menu-open")

        # menu page too
        await call("Page.navigate", {"url": "http://127.0.0.1:8080/menu.html"})
        await asyncio.sleep(2.2)
        await call("Runtime.evaluate", {
            "expression": "document.querySelectorAll('[data-header],[data-menu-hero]').forEach(el => el.classList.add('is-ready')); document.querySelector('[data-nav-toggle]').setAttribute('aria-expanded','true'); document.querySelector('[data-nav-menu]').classList.add('is-open'); document.body.classList.add('menu-open');"
        })
        await asyncio.sleep(0.5)
        res = await call("Page.captureScreenshot", {"format": "png", "fromSurface": True})
        open(r"d:\CozyCafe\_qa-shots\mobile-menu-page-open.png", "wb").write(base64.b64decode(res["result"]["data"]))
        print("saved mobile-menu-page-open")

asyncio.run(main())
