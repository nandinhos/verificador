/* mcp.ai sob auditoria — interações (sem dependências) */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(pointer: fine)").matches;

  /* ---------- barra de progresso ---------- */
  var bar = document.getElementById("progress");
  function onScroll() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var p = max > 0 ? (h.scrollTop / max) * 100 : 0;
    if (bar) bar.style.width = p.toFixed(2) + "%";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- revelação por scroll ---------- */
  var items = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }
  /* fallback: revela o que já está na viewport no carregamento e garante que nada fique invisível */
  function revealVisible() {
    items.forEach(function (el) {
      if (el.classList.contains("in")) return;
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.96) el.classList.add("in");
    });
  }
  window.addEventListener("load", revealVisible);
  setTimeout(revealVisible, 900);
  setTimeout(revealVisible, 2600);

  /* ---------- contadores ---------- */
  var nf = new Intl.NumberFormat("pt-BR");
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10) || 0;
    var prefix = el.getAttribute("data-prefix") || "";
    if (reduce) { el.textContent = prefix + nf.format(target); return; }
    el.textContent = prefix + "0";
    var t0 = performance.now(), dur = 1400;
    function step(now) {
      var k = Math.min(1, (now - t0) / dur);
      var eased = 1 - Math.pow(1 - k, 3);
      el.textContent = prefix + nf.format(Math.round(target * eased));
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    setTimeout(function () { el.textContent = prefix + nf.format(target); }, dur + 250);
  }
  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  } else {
    counters.forEach(countUp);
  }
  /* garantia: se a animação for interrompida (aba oculta, rAF pausado), fixa o valor final */
  setTimeout(function () {
    counters.forEach(function (el) {
      var target = parseInt(el.getAttribute("data-count"), 10) || 0;
      el.textContent = (el.getAttribute("data-prefix") || "") + nf.format(target);
    });
  }, 3000);

  /* ---------- luz que segue o cursor nos painéis ---------- */
  document.querySelectorAll(".glass").forEach(function (el) {
    el.addEventListener("pointermove", function (ev) {
      var r = el.getBoundingClientRect();
      el.style.setProperty("--mx", (ev.clientX - r.left) + "px");
      el.style.setProperty("--my", (ev.clientY - r.top) + "px");
    });
  });

  /* ---------- inclinação suave ---------- */
  if (fine && !reduce) {
    document.querySelectorAll("[data-tilt]").forEach(function (el) {
      var raf = 0;
      el.addEventListener("pointermove", function (ev) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          var r = el.getBoundingClientRect();
          var dx = (ev.clientX - r.left) / r.width - 0.5;
          var dy = (ev.clientY - r.top) / r.height - 0.5;
          el.style.transform = "perspective(1200px) rotateX(" + (-dy * 3).toFixed(2) + "deg) rotateY(" + (dx * 3).toFixed(2) + "deg)";
          raf = 0;
        });
      });
      el.addEventListener("pointerleave", function () {
        el.style.transform = "";
      });
    });
  }

  /* ---------- mira ---------- */
  if (fine && !reduce) {
    var mira = document.createElement("div");
    mira.className = "mira";
    mira.setAttribute("aria-hidden", "true");
    mira.innerHTML =
      '<span class="mira__ring"></span><span class="mira__dot"></span>' +
      '<span class="mira__bar t"></span><span class="mira__bar b"></span>' +
      '<span class="mira__bar l"></span><span class="mira__bar r"></span>' +
      '<span class="mira__label"></span>';
    document.body.appendChild(mira);
    var label = mira.querySelector(".mira__label");

    var tx = window.innerWidth / 2, ty = window.innerHeight / 2;
    var cx = tx, cy = ty, visible = false, running = false;

    function tick() {
      cx += (tx - cx) * 0.18;
      cy += (ty - cy) * 0.18;
      mira.style.transform = "translate3d(" + cx.toFixed(1) + "px," + cy.toFixed(1) + "px,0)";
      if (Math.abs(tx - cx) + Math.abs(ty - cy) > 0.3) {
        requestAnimationFrame(tick);
      } else {
        running = false;
      }
    }

    window.addEventListener("pointermove", function (e) {
      tx = e.clientX; ty = e.clientY;
      if (!visible) { visible = true; mira.classList.add("on"); }
      if (!running) { running = true; requestAnimationFrame(tick); }
    }, { passive: true });
    document.addEventListener("pointerleave", function () {
      visible = false; mira.classList.remove("on");
    });

    var interactive = "a, button, [data-tilt], .card, .checklist li, .fact";
    document.addEventListener("pointerover", function (e) {
      var t = e.target.closest(interactive);
      if (t) {
        mira.classList.add("is-target");
        label.textContent = t.getAttribute("data-mira") || (t.tagName === "A" ? "abrir" : "ler");
      } else {
        mira.classList.remove("is-target");
      }
    });

    tick();
  }

  /* ---------- navegação ativa ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav a"));
  var sections = links.map(function (a) { return document.querySelector(a.getAttribute("href")); }).filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    var nio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) {
          a.setAttribute("aria-current", a.getAttribute("href") === "#" + e.target.id ? "true" : "false");
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(function (s) { nio.observe(s); });
  }
})();
