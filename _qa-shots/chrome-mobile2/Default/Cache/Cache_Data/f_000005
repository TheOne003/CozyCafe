/**
 * Cozy Café — site interactions
 * Shared nav, reveals, food cards, ingredients, heroes, form
 */

(() => {
  "use strict";

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* Subtle pointer tilt for editorial hero media (desktop only) */
  function bindPointerTilt(hero, mediaSelector, maxX = 8, maxY = 5) {
    if (reducedMotion || !finePointer || !hero) return;
    const media = hero.querySelector(mediaSelector);
    if (!media) return;

    let ticking = false;
    let tx = 0;
    let ty = 0;

    const apply = () => {
      media.style.transform = `translate3d(${tx}px, ${ty}px, 0)`;
      ticking = false;
    };

    hero.addEventListener("pointermove", (e) => {
      const rect = hero.getBoundingClientRect();
      tx = ((e.clientX - rect.left) / rect.width - 0.5) * maxX;
      ty = ((e.clientY - rect.top) / rect.height - 0.5) * maxY;
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(apply);
      }
    });

    hero.addEventListener("pointerleave", () => {
      tx = 0;
      ty = 0;
      requestAnimationFrame(apply);
    });
  }

  /* ---------- Navigation ---------- */
  function initNav() {
    const header = document.querySelector("[data-header]");
    const toggle = document.querySelector("[data-nav-toggle]");
    const menu = document.querySelector("[data-nav-menu]");

    if (!header) return;

    requestAnimationFrame(() => header.classList.add("is-ready"));

    const onScroll = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    if (!toggle || !menu) return;

    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      menu.classList.toggle("is-open", open);
      document.body.classList.toggle("menu-open", open);
      const label = toggle.querySelector(".visually-hidden");
      if (label) label.textContent = open ? "Close menu" : "Open menu";
    };

    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });

    // Close when tapping empty overlay area (not links/buttons)
    menu.addEventListener("click", (e) => {
      if (e.target === menu) setOpen(false);
    });

    document.addEventListener("click", (e) => {
      if (toggle.getAttribute("aria-expanded") !== "true") return;
      if (menu.contains(e.target) || toggle.contains(e.target)) return;
      setOpen(false);
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") setOpen(false);
    });
  }

  /* ---------- Scroll reveals ---------- */
  function initReveals() {
    const items = [
      ...document.querySelectorAll(".reveal:not(.is-visible)"),
      ...document.querySelectorAll(".reveal-line:not(.is-visible)"),
    ].filter((el) => !el.closest(".about-hero__title") && !el.closest(".menu-hero__title") && !el.closest(".contact-hero__title"));

    if (!items.length) return;

    if (reducedMotion || !("IntersectionObserver" in window)) {
      items.forEach((el) => el.classList.add("is-visible"));
      document.querySelectorAll(".about-hero__title .reveal-line").forEach((el) => {
        el.classList.add("is-visible");
      });
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -5% 0px" }
    );

    items.forEach((el) => observer.observe(el));
  }

  /* ---------- Hero: entrance, scroll parallax, pointer tilt ---------- */
  function initHero() {
    const hero = document.querySelector("[data-hero]");
    if (!hero) return;

    requestAnimationFrame(() => {
      requestAnimationFrame(() => hero.classList.add("is-ready"));
    });

    if (reducedMotion) return;

    const media = hero.querySelector("[data-parallax='media']");
    const title = hero.querySelector("[data-parallax='title']");
    const copy = hero.querySelector("[data-parallax='copy']");
    const place = hero.querySelector("[data-parallax='place']");
    const logo = hero.querySelector("[data-parallax='logo']");
    const bloom = hero.querySelector("[data-parallax='bloom']");
    const img = hero.querySelector("[data-parallax-img] img");
    const tiltTarget = hero.querySelector("[data-pointer-tilt]");

    let scrollY = 0;
    let tiltX = 0;
    let tiltY = 0;
    let ticking = false;

    const apply = () => {
      const rect = hero.getBoundingClientRect();
      const h = Math.max(rect.height, 1);
      scrollY = Math.min(Math.max(-rect.top / h, 0), 1);

      if (media) {
        media.style.transform = `translate3d(${tiltX}px, ${scrollY * 36 + tiltY}px, 0)`;
      }
      if (img && !tiltTarget) {
        img.style.transform = `scale(${1 + scrollY * 0.045})`;
      }
      if (img && tiltTarget) {
        img.style.transform = `scale(${1 + scrollY * 0.04}) translate3d(${tiltX * 0.3}px, ${tiltY * 0.3}px, 0)`;
      }
      if (bloom) {
        bloom.style.transform = `translate3d(${tiltX * -0.3}px, ${scrollY * 22 + tiltY * -0.25}px, 0)`;
      }
      if (title) {
        title.style.transform = `translate3d(0, ${scrollY * -20}px, 0)`;
        title.style.opacity = String(Math.max(0, 1 - scrollY * 0.75));
      }
      if (copy) {
        copy.style.transform = `translate3d(0, ${scrollY * -12}px, 0)`;
        copy.style.opacity = String(Math.max(0, 1 - scrollY * 0.95));
      }
      if (place) {
        place.style.transform = `translate3d(0, ${scrollY * 14}px, 0)`;
      }
      if (logo) {
        logo.style.transform = `translate3d(0, ${scrollY * 24}px, 0)`;
      }

      ticking = false;
    };

    const requestTick = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(apply);
      }
    };

    window.addEventListener("scroll", requestTick, { passive: true });

    // Subtle pointer follow — desktop only, max ~10px
    if (finePointer && tiltTarget) {
      hero.addEventListener("pointermove", (e) => {
        const rect = hero.getBoundingClientRect();
        const nx = (e.clientX - rect.left) / rect.width - 0.5;
        const ny = (e.clientY - rect.top) / rect.height - 0.5;
        tiltX = nx * 8;
        tiltY = ny * 6;
        requestTick();
      });

      hero.addEventListener("pointerleave", () => {
        tiltX = 0;
        tiltY = 0;
        requestTick();
      });
    }
  }

  /* ---------- Food cards ---------- */
  function initFoodCards() {
    const cards = document.querySelectorAll("[data-food-card]:not([data-bound])");
    if (!cards.length) return;

    const coarse = window.matchMedia("(hover: none), (pointer: coarse)").matches;

    const setActive = (card, active) => {
      card.classList.toggle("is-active", active);
      card.setAttribute("aria-expanded", String(active));
      const cta = card.querySelector(".food-card__cta");
      if (cta && cta.tagName === "A") cta.tabIndex = active ? 0 : -1;
    };

    const clearOthers = (except) => {
      document.querySelectorAll("[data-food-card]").forEach((c) => {
        if (c !== except) setActive(c, false);
      });
    };

    cards.forEach((card) => {
      card.setAttribute("data-bound", "true");

      card.addEventListener("click", (e) => {
        if (!coarse && !e.target.closest("a")) return;

        if (e.target.closest("a") && card.classList.contains("is-active")) return;

        e.preventDefault();
        const wasActive = card.classList.contains("is-active");
        clearOthers(card);
        setActive(card, !wasActive);
      });

      card.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          const wasActive = card.classList.contains("is-active");
          clearOthers(card);
          setActive(card, !wasActive);
        }
      });

      card.addEventListener("focusin", () => {
        if (!card.classList.contains("is-active")) {
          card.setAttribute("aria-expanded", "true");
        }
      });

      card.addEventListener("focusout", (e) => {
        if (card.contains(e.relatedTarget)) return;
        if (!card.classList.contains("is-active")) {
          card.setAttribute("aria-expanded", "false");
        }
      });
    });

    if (!document.documentElement.dataset.foodOutsideBound) {
      document.documentElement.dataset.foodOutsideBound = "true";
      document.addEventListener("click", (e) => {
        if (!e.target.closest("[data-food-card]")) {
          document.querySelectorAll("[data-food-card]").forEach((c) => setActive(c, false));
        }
      });
    }
  }

  /* ---------- Ingredient storytelling + connecting lines ---------- */
  function initIngredientStory() {
    const section = document.querySelector("[data-story]");
    const stage = document.querySelector("[data-ingredient-stage]");
    if (!section || !stage) return;

    const pills = stage.querySelectorAll("[data-ingredient]");
    const lines = stage.querySelectorAll("[data-line]");

    const clearFocus = () => {
      stage.classList.remove("has-focus");
      pills.forEach((p) => p.classList.remove("is-active"));
      lines.forEach((l) => l.classList.remove("is-on"));
    };

    const focusIngredient = (name) => {
      stage.classList.add("has-focus");
      pills.forEach((p) => {
        p.classList.toggle("is-active", p.getAttribute("data-ingredient") === name);
      });
      lines.forEach((l) => {
        l.classList.toggle("is-on", l.getAttribute("data-line") === name);
      });
    };

    if (reducedMotion || !("IntersectionObserver" in window)) {
      stage.classList.add("is-inview");
    } else {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              stage.classList.add("is-inview");
              observer.unobserve(section);
            }
          });
        },
        { threshold: 0.32 }
      );
      observer.observe(section);
    }

    pills.forEach((pill) => {
      const name = pill.getAttribute("data-ingredient");

      pill.addEventListener("click", () => {
        if (pill.classList.contains("is-active")) {
          clearFocus();
        } else {
          focusIngredient(name);
        }
      });

      if (finePointer) {
        pill.addEventListener("mouseenter", () => focusIngredient(name));
        pill.addEventListener("mouseleave", () => clearFocus());
      }
    });
  }

  /* ---------- Coffee ---------- */
  function initCoffee() {
    const coffee = document.querySelector("[data-coffee]");
    if (!coffee) return;

    if (reducedMotion || !("IntersectionObserver" in window)) {
      coffee.classList.add("is-inview");
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            coffee.classList.add("is-inview");
            observer.unobserve(coffee);
          }
        });
      },
      { threshold: 0.28 }
    );

    observer.observe(coffee);
  }

  /* ---------- Atmosphere list (tap on coarse pointers) ---------- */
  function initAtmosphere() {
    const items = document.querySelectorAll(".atm-item");
    if (!items.length) return;

    const coarse = window.matchMedia("(hover: none), (pointer: coarse)").matches;
    // Notes already visible via CSS on hover:none; keep tap toggle for hybrid devices
    items.forEach((item) => {
      item.addEventListener("click", () => {
        if (!coarse && window.matchMedia("(hover: hover)").matches) return;
        const open = item.classList.contains("is-open");
        items.forEach((i) => i.classList.remove("is-open"));
        if (!open) item.classList.add("is-open");
      });

      item.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          item.classList.toggle("is-open");
        }
      });
    });
  }

  /* ---------- Cursor hint label (does not replace system cursor) ---------- */
  function initCursorHint() {
    const hint = document.querySelector("[data-cursor-hint]");
    if (!hint || reducedMotion || !finePointer) return;
    if (hint.dataset.bound === "true") return;
    hint.dataset.bound = "true";

    let visible = false;
    let x = 0;
    let y = 0;
    let ticking = false;

    const move = () => {
      hint.style.transform = `translate3d(${x}px, ${y}px, 0) translate(-50%, -160%) scale(${visible ? 1 : 0.92})`;
      ticking = false;
    };

    document.addEventListener(
      "pointermove",
      (e) => {
        x = e.clientX;
        y = e.clientY;
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(move);
        }
      },
      { passive: true }
    );

    document.addEventListener("pointerover", (e) => {
      const el = e.target.closest("[data-cursor]");
      if (!el) return;
      hint.textContent = el.getAttribute("data-cursor") || "";
      hint.classList.add("is-visible");
      visible = true;
    });

    document.addEventListener("pointerout", (e) => {
      const el = e.target.closest("[data-cursor]");
      if (!el) return;
      const related = e.relatedTarget && e.relatedTarget.closest
        ? e.relatedTarget.closest("[data-cursor]")
        : null;
      if (related === el) return;
      hint.classList.remove("is-visible");
      visible = false;
    });
  }

  /* ---------- About hero ---------- */
  function initAboutHero() {
    const hero = document.querySelector("[data-about-hero]");
    if (!hero) return;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => hero.classList.add("is-ready"));
    });
    bindPointerTilt(hero, "[data-about-media]");
  }

  /* ---------- Belief list ---------- */
  function initBeliefs() {
    const beliefs = document.querySelectorAll("[data-belief]");
    if (!beliefs.length) return;

    const coarse = window.matchMedia("(hover: none), (pointer: coarse)").matches;

    const setOpen = (item, open) => {
      item.classList.toggle("is-open", open);
      item.setAttribute("aria-expanded", String(open));
    };

    beliefs.forEach((item) => {
      // On coarse pointers, tap toggles; on fine, hover CSS handles reveal
      item.addEventListener("click", () => {
        if (!coarse && window.matchMedia("(hover: hover)").matches) return;
        const wasOpen = item.classList.contains("is-open");
        beliefs.forEach((b) => setOpen(b, false));
        setOpen(item, !wasOpen);
      });

      item.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          const wasOpen = item.classList.contains("is-open");
          beliefs.forEach((b) => setOpen(b, false));
          setOpen(item, !wasOpen);
        }
      });
    });
  }

  /* ---------- Menu page: render grids from data ---------- */
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function buildMenuCard(item) {
    const sizeClass =
      item.size === "featured"
        ? "food-card--featured"
        : item.size === "medium"
          ? "food-card--medium"
          : "food-card--small";

    const ingredients = (item.ingredients || [])
      .map((ing) => escapeHtml(ing))
      .join(" · ");

    return `
<article
  class="food-card ${sizeClass} reveal"
  data-food-card
  data-cursor="EXPLORE"
  tabindex="0"
  role="button"
  aria-expanded="false"
  aria-label="${escapeHtml(item.name)}, ${escapeHtml(item.price)}. Activate to reveal ingredients."
>
  <div class="food-card__media">
    <img
      src="${escapeHtml(item.image)}"
      alt="${escapeHtml(item.alt)}"
      width="700"
      height="700"
      loading="lazy"
    />
  </div>
  <div class="food-card__scrim" aria-hidden="true"></div>
  <div class="food-card__body">
    <span class="food-card__price">${escapeHtml(item.price)}</span>
    <h3 class="food-card__name">${escapeHtml(item.name)}</h3>
    <p class="food-card__tagline">${escapeHtml(item.description)}</p>
    <div class="food-card__reveal">
      <p class="food-card__ing-label">Ingredients</p>
      <p class="food-card__ing-line">${ingredients}</p>
      <span class="food-card__cta">
        View Item <span class="btn__arrow" aria-hidden="true">→</span>
      </span>
    </div>
  </div>
</article>`;
  }

  function initMenuGrids() {
    const data = window.COZY_MENU;
    if (!data) return;

    const breakfastGrid = document.querySelector('[data-menu-grid="breakfast"]');
    const lunchGrid = document.querySelector('[data-menu-grid="lunch"]');

    if (breakfastGrid && data.breakfast) {
      breakfastGrid.innerHTML = data.breakfast.map(buildMenuCard).join("");
    }
    if (lunchGrid && data.lunch) {
      lunchGrid.innerHTML = data.lunch.map(buildMenuCard).join("");
    }

    // Re-bind reveals + food cards for injected markup
    initReveals();
    initFoodCards();
  }

  /* ---------- Menu sticky category nav ---------- */
  function initMenuCats() {
    const links = document.querySelectorAll("[data-cat-link]");
    const sections = document.querySelectorAll("[data-menu-section]");
    if (!links.length || !sections.length) return;

    const setActive = (id) => {
      links.forEach((link) => {
        link.classList.toggle("is-active", link.getAttribute("data-cat-link") === id);
      });
    };

    links.forEach((link) => {
      link.addEventListener("click", (e) => {
        const id = link.getAttribute("data-cat-link");
        const target = document.getElementById(id);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
        setActive(id);
      });
    });

    if (!("IntersectionObserver" in window)) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActive(entry.target.getAttribute("data-menu-section"));
          }
        });
      },
      {
        rootMargin: "-35% 0px -45% 0px",
        threshold: 0.01,
      }
    );

    sections.forEach((section) => observer.observe(section));
  }

  /* ---------- Menu hero ---------- */
  function initMenuHero() {
    const hero = document.querySelector("[data-menu-hero]");
    if (!hero) return;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => hero.classList.add("is-ready"));
    });
    bindPointerTilt(hero, "[data-menu-media]");
  }

  /* ---------- Contact hero ---------- */
  function initContactHero() {
    const hero = document.querySelector("[data-contact-hero]");
    if (!hero) return;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => hero.classList.add("is-ready"));
    });
    bindPointerTilt(hero, "[data-contact-media]");
  }

  /* ---------- Contact form validation (front-end only) ---------- */
  function initContactForm() {
    const form = document.querySelector("[data-contact-form]");
    const success = document.querySelector("[data-contact-success]");
    const resetBtn = document.querySelector("[data-contact-reset]");
    const status = document.getElementById("form-status");
    if (!form) return;

    const fields = {
      name: form.querySelector("#contact-name"),
      email: form.querySelector("#contact-email"),
      subject: form.querySelector("#contact-subject"),
      message: form.querySelector("#contact-message"),
    };

    if (!fields.name || !fields.email || !fields.subject || !fields.message) return;

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const clearError = (key) => {
      const input = fields[key];
      const wrap = input.closest(".form-field");
      const err = form.querySelector(`[data-error-for="${key}"]`);
      if (wrap) wrap.classList.remove("is-invalid");
      input.removeAttribute("aria-invalid");
      if (err) {
        err.hidden = true;
        err.textContent = "";
      }
    };

    const setError = (key, message) => {
      const input = fields[key];
      const wrap = input.closest(".form-field");
      const err = form.querySelector(`[data-error-for="${key}"]`);
      if (wrap) wrap.classList.add("is-invalid");
      input.setAttribute("aria-invalid", "true");
      if (err) {
        err.hidden = false;
        err.textContent = message;
      }
    };

    const validate = () => {
      let valid = true;
      let firstInvalid = null;

      Object.keys(fields).forEach(clearError);

      if (!fields.name.value.trim()) {
        setError("name", "Please enter your name.");
        valid = false;
        firstInvalid = firstInvalid || fields.name;
      }

      const emailVal = fields.email.value.trim();
      if (!emailVal) {
        setError("email", "Please enter your email.");
        valid = false;
        firstInvalid = firstInvalid || fields.email;
      } else if (!emailPattern.test(emailVal)) {
        setError("email", "Please enter a valid email address.");
        valid = false;
        firstInvalid = firstInvalid || fields.email;
      }

      if (!fields.subject.value.trim()) {
        setError("subject", "Please add a subject.");
        valid = false;
        firstInvalid = firstInvalid || fields.subject;
      }

      if (!fields.message.value.trim()) {
        setError("message", "Please write a message.");
        valid = false;
        firstInvalid = firstInvalid || fields.message;
      }

      return { valid, firstInvalid };
    };

    const showForm = () => {
      form.classList.remove("is-hidden");
      form.removeAttribute("aria-hidden");
      if (success) {
        success.classList.remove("is-visible");
        success.hidden = true;
      }
      if (status) status.textContent = "";
      fields.name.focus();
    };

    const showSuccess = () => {
      form.classList.add("is-hidden");
      form.setAttribute("aria-hidden", "true");
      if (success) {
        success.hidden = false;
        requestAnimationFrame(() => success.classList.add("is-visible"));
        const focusTarget = resetBtn || success;
        focusTarget.focus?.();
      }
      if (status) {
        status.textContent = "Thank you. Your message is on its way. We'll see you at Cozy Café soon.";
      }
    };

    Object.keys(fields).forEach((key) => {
      fields[key].addEventListener("input", () => clearError(key));
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const { valid, firstInvalid } = validate();

      if (!valid) {
        if (status) status.textContent = "Please fix the errors in the form.";
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      showSuccess();
    });

    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        form.reset();
        Object.keys(fields).forEach(clearError);
        showForm();
      });
    }
  }

  /* ---------- Boot ---------- */
  function init() {
    initNav();
    initReveals();
    initHero();
    initFoodCards();
    initIngredientStory();
    initCoffee();
    initAtmosphere();
    initCursorHint();
    initAboutHero();
    initBeliefs();
    initMenuGrids();
    initMenuCats();
    initMenuHero();
    initContactHero();
    initContactForm();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
