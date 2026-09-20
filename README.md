# Cozy Café

A premium, editorial brand website for **Cozy Café** in Cadillac, MI — coffee, food, and good vibes.

Built with HTML5, CSS3, and vanilla JavaScript. No frameworks. No backend.

## Pages

| Page | File | Status |
|------|------|--------|
| Home | `index.html` | Complete — visual benchmark |
| About | `about.html` | Complete — editorial storytelling |
| Menu | `menu.html` | Complete — interactive food experience |
| Contact | `contact.html` | Complete — visit invitation |

## Structure

```
CozyCafe/
├── index.html
├── about.html          (planned)
├── menu.html           (planned)
├── contact.html        (planned)
├── css/
│   └── style.css
├── js/
│   └── script.js
├── assets/
│   ├── images/
│   └── icons/
└── README.md
```

## Design system

**Colors**

- Dark brown `#4A2C20`
- Cream `#F8F1E5` (dominant background)
- Warm beige `#E8D8C3`
- Muted olive `#5F7355`
- Soft white `#FFFDF8`
- Dark text `#2C211C`

**Typography**

- Display: [Fraunces](https://fonts.google.com/specimen/Fraunces)
- Body: [Figtree](https://fonts.google.com/specimen/Figtree)

## Run locally

Open `index.html` in a browser, or serve the folder:

```bash
# Python
python -m http.server 8080

# Node
npx serve .
```

Then visit `http://localhost:8080`.

## Interactions

- Sticky nav with blur transition on scroll
- Animated mobile menu
- Continuous marquees
- Food cards: hover (desktop) / tap (mobile) ingredient reveals
- Ingredient storytelling stage
- Scroll reveals via IntersectionObserver
- Subtle hero parallax
- `prefers-reduced-motion` respected

## Brand details

- **Address:** 8834 E 34 Rd #131, Cadillac, MI 49601
- **Phone:** +1(56)88289017

## License

© 2026 Cozy Café. All rights reserved.
