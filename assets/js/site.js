/* ==========================================================================
   Soliu Quadri — portfolio behaviour
   Vanilla JS, no dependencies. Every feature degrades gracefully.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  };

  /* ------------------------------------------------------------------
     1. Colour theme — remembered, and follows the OS by default
     ------------------------------------------------------------------ */
  var THEME_KEY = "sq-theme";

  function readStoredTheme() {
    try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
  }
  function storeTheme(value) {
    try { localStorage.setItem(THEME_KEY, value); } catch (e) { /* ignore */ }
  }

  function applyTheme(theme) {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.removeAttribute("data-theme");
    }
    $$(".theme-toggle").forEach(function (btn) {
      var isDark = theme === "dark";
      btn.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
      btn.setAttribute("title", isDark ? "Switch to light mode" : "Switch to dark mode");
      var icon = btn.querySelector("[aria-hidden]") || btn;
      icon.textContent = isDark ? "☀" : "☾";
    });
  }

  var stored = readStoredTheme();
  var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(stored || (prefersDark ? "dark" : "light"));

  $$(".theme-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      storeTheme(next);
      applyTheme(next);
    });
  });

  /* ------------------------------------------------------------------
     2. Mobile drawer
     ------------------------------------------------------------------ */
  var burger = $(".burger");
  var drawer = $("#drawer");

  function setDrawer(open) {
    if (!burger || !drawer) return;
    drawer.classList.toggle("open", open);
    burger.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", String(open));
    drawer.setAttribute("aria-hidden", String(!open));
    if (open) {
      drawer.removeAttribute("inert");
    } else {
      drawer.setAttribute("inert", "");
    }
    var label = burger.querySelector(".sr-only");
    if (label) label.textContent = open ? "Close menu" : "Open menu";
  }

  if (burger && drawer) {
    burger.addEventListener("click", function () {
      setDrawer(!drawer.classList.contains("open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("open")) {
        setDrawer(false);
        burger.focus();
      }
    });
    // Close the drawer after following a link
    $$("a", drawer).forEach(function (a) {
      a.addEventListener("click", function () { setDrawer(false); });
    });
  }

  /* ------------------------------------------------------------------
     3. Reveal on scroll
     ------------------------------------------------------------------ */
  var revealables = $$(".reveal");
  if (revealables.length) {
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
      revealables.forEach(function (el) { io.observe(el); });
    } else {
      revealables.forEach(function (el) { el.classList.add("in"); });
    }
  }

  /* ------------------------------------------------------------------
     4. Testimonial register (tabs)
     ------------------------------------------------------------------ */
  $$("[data-register]").forEach(function (register) {
    var items = $$(".register-item", register);
    var quotes = $$("[data-quote]", register.parentNode);

    function select(index) {
      items.forEach(function (item, i) {
        var active = i === index;
        item.classList.toggle("active", active);
        item.setAttribute("aria-selected", String(active));
        item.setAttribute("tabindex", active ? "0" : "-1");
      });
      quotes.forEach(function (quote, i) {
        var active = i === index;
        quote.classList.toggle("active", active);
        if (active) {
          quote.removeAttribute("hidden");
        } else {
          quote.setAttribute("hidden", "");
        }
      });
    }

    items.forEach(function (item, i) {
      item.addEventListener("click", function () { select(i); });
    });

    // Arrow-key navigation between testimonials
    register.addEventListener("keydown", function (e) {
      var current = items.indexOf(document.activeElement);
      if (current === -1) return;
      var next = null;
      if (e.key === "ArrowDown" || e.key === "ArrowRight") next = (current + 1) % items.length;
      if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = (current - 1 + items.length) % items.length;
      if (next !== null) {
        e.preventDefault();
        select(next);
        items[next].focus();
      }
    });

    if (items.length) select(0);
  });

  /* ------------------------------------------------------------------
     5. Record expander (small screens)
     ------------------------------------------------------------------ */
  $$(".record-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var record = btn.closest(".record");
      if (!record) return;
      var open = record.classList.toggle("record-open");
      btn.setAttribute("aria-expanded", String(open));
      btn.textContent = open ? "Show fewer" : "Show 5 more";
    });
  });

  /* ------------------------------------------------------------------
     6. Contact form — no backend, so hand off to the user's mail client
     ------------------------------------------------------------------ */
  var form = $("#contact-form");
  if (form) {
    var status = $("#form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var name = (data.get("name") || "").toString().trim();
      var email = (data.get("email") || "").toString().trim();
      var message = (data.get("message") || "").toString().trim();
      var to = form.getAttribute("data-mailto") || "";

      if (!name || !email || !message) {
        if (status) status.textContent = "Please fill in every field.";
        return;
      }

      var subject = "Portfolio enquiry from " + name;
      var body = message + "\n\n— " + name + "\n" + email;
      window.location.href =
        "mailto:" + to +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);

      if (status) status.textContent = "Opening your email client…";
    });
  }

  /* ------------------------------------------------------------------
     7. Mark the current page in the navigation
     ------------------------------------------------------------------ */
  function markCurrent() {
    var path = window.location.pathname;
    var leaf = path.substring(path.lastIndexOf("/") + 1) || "index.html";
    $$(".nav-item, .drawer-link").forEach(function (a) {
      var href = a.getAttribute("href");
      if (!href) return;
      var target = href.substring(href.lastIndexOf("/") + 1) || "index.html";
      if (target === leaf) a.setAttribute("aria-current", "page");
    });
  }
  markCurrent();

  /* ------------------------------------------------------------------
     8. Footer year
     ------------------------------------------------------------------ */
  $$("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
