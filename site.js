// Au fil du tracé — script partagé (vanilla JS, sans dépendance).
// Reprend fidèlement les animations validées le 30/07 (révélation au scroll,
// tracés SVG synchronisés au défilement) et l'accordéon FAQ, portés depuis le
// composant d'origine (Claude Design) vers du DOM pur pour le site statique.
(function () {
  'use strict';

  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var animOn = document.body.dataset.anim === 'on';

  // ── Révélation au scroll (« L'encre qui se pose ») ──────────────────────
  function revealEl(el, immediate) {
    el.dataset.rvDone = '1';
    if (immediate) el.style.transition = 'none';
    el.style.opacity = '1';
    el.style.transform = 'none';
    clearTimeout(el.__rvT);
    el.__rvT = setTimeout(function () {
      el.style.transition = 'none';
      el.style.opacity = '1';
      el.style.transform = 'none';
    }, 1600);
  }

  var io;
  function observeReveals() {
    var els = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]:not([data-rv])'));
    if (!els.length) return;
    els.forEach(function (el) { el.dataset.rv = '1'; });
    if (!animOn || prefersReduced || typeof IntersectionObserver === 'undefined') return;
    if (!io) {
      io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { revealEl(en.target); io.unobserve(en.target); }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    }
    var isMobile = window.matchMedia('(max-width: 700px)').matches;
    var amp = isMobile ? 16 : 28;
    var seen = new Map();
    els.forEach(function (el) {
      var authored = el.style.transitionDelay;
      var delay = authored;
      if (!authored) {
        var key = el.parentElement;
        var i = seen.get(key) || 0;
        seen.set(key, i + 1);
        delay = Math.min(i, 3) * 0.18 + 's';
      }
      el.style.opacity = '0';
      el.style.transform = 'translateY(' + amp + 'px)';
      el.style.transition = 'opacity .9s cubic-bezier(.4,0,.2,1), transform .9s cubic-bezier(.4,0,.2,1)';
      el.style.transitionDelay = delay;
      io.observe(el);
    });
    setTimeout(function () {
      els.forEach(function (el) {
        if (el.dataset.rvDone) return;
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight * 1.15) revealEl(el, true);
      });
    }, 3000);
    setTimeout(function () {
      els.forEach(function (el) { if (!el.dataset.rvDone) revealEl(el, true); });
    }, 30000);
  }

  // ── Tracés SVG (« Le tracé qui s'écrit ») ───────────────────────────────
  var tracePending = [];
  var traceRaf = 0, sawScroll = false, traceFallbackT;

  function canScroll() {
    var se = document.scrollingElement || document.documentElement;
    return se.scrollHeight > window.innerHeight + 4;
  }

  function playTrace(el) {
    var late = el.hasAttribute('data-trace-late');
    if (el.hasAttribute('data-trait')) {
      el.style.animation = 'traitX .8s cubic-bezier(.16,.84,.3,1) both';
    } else if (el.getAttribute('fill') === 'currentColor') {
      var i = Number(el.dataset.trIdx || 0);
      el.style.animation = 'inkIn .5s ease ' + (0.95 + i * 0.12).toFixed(2) + 's both';
    } else {
      el.style.animation = 'traceUnit 1.8s cubic-bezier(.22,.7,.25,1) ' + (late ? '1.1s' : '.15s') + ' both';
    }
  }

  function checkTraces() {
    if (!tracePending.length) return;
    var vh = window.innerHeight || 800;
    var ready = [];
    tracePending = tracePending.filter(function (it) {
      if (!it.host.isConnected) return false;
      if (it.host.getBoundingClientRect().top < vh * 0.88) { ready.push(it); return false; }
      return true;
    });
    var order = [];
    ready.forEach(function (it) {
      var i = order.indexOf(it.host);
      if (i < 0) { order.push(it.host); i = order.length - 1; }
      setTimeout(function () { playTrace(it.el); }, Math.min(1300, i * 110));
    });
  }

  function onTraceScroll(e) {
    if (e && e.type === 'scroll') sawScroll = true;
    if (traceRaf) return;
    traceRaf = requestAnimationFrame(function () { traceRaf = 0; checkTraces(); });
  }

  function observeTraces() {
    var els = Array.prototype.slice.call(document.querySelectorAll('[data-trait]:not([data-tr]),[data-trace]:not([data-tr])'));
    if (!els.length) return;
    var perParent = new Map();
    els.forEach(function (el) {
      el.dataset.tr = '1';
      var k = el.parentElement;
      var i = perParent.get(k) || 0;
      perParent.set(k, i + 1);
      el.dataset.trIdx = String(i);
    });
    if (!animOn || prefersReduced) return;
    els.forEach(function (el) {
      var svg = el.ownerSVGElement;
      tracePending.push({ el: el, host: svg ? (svg.parentElement || svg) : el });
    });
    window.addEventListener('scroll', onTraceScroll, { passive: true });
    window.addEventListener('resize', onTraceScroll, { passive: true });
    checkTraces();
    clearTimeout(traceFallbackT);
    traceFallbackT = setTimeout(function () {
      if (!tracePending.length) return;
      var embedded = window.self !== window.top;
      if (canScroll() && !(embedded && !sawScroll)) return;
      var seen = [];
      tracePending.splice(0).forEach(function (it) {
        var i = seen.indexOf(it.host);
        if (i < 0) { seen.push(it.host); i = seen.length - 1; }
        setTimeout(function () { playTrace(it.el); }, Math.min(2600, i * 110));
      });
    }, 1400);
  }

  function scheduleReveals() {
    [40, 250, 800, 1800].forEach(function (t) {
      setTimeout(function () { observeReveals(); observeTraces(); }, t);
    });
  }

  // ── Accordéon FAQ ────────────────────────────────────────────────────────
  function initFaq() {
    var items = document.querySelectorAll('[data-faq-item]');
    items.forEach(function (item) {
      var btn = item.querySelector('[data-faq-toggle]');
      var panel = item.querySelector('[data-faq-panel]');
      var chev = item.querySelector('[data-faq-chevron]');
      if (!btn || !panel) return;
      btn.addEventListener('click', function () {
        var isOpen = item.getAttribute('data-open') === 'true';
        // Un seul panneau ouvert à la fois, comme dans la version d'origine.
        document.querySelectorAll('[data-faq-item][data-open="true"]').forEach(function (other) {
          if (other !== item) {
            other.setAttribute('data-open', 'false');
            other.querySelector('[data-faq-panel]').hidden = true;
            other.style.borderColor = '#f0e7da';
            var oc = other.querySelector('[data-faq-chevron]');
            if (oc) oc.style.transform = 'rotate(0deg)';
          }
        });
        item.setAttribute('data-open', isOpen ? 'false' : 'true');
        panel.hidden = isOpen;
        item.style.borderColor = isOpen ? '#f0e7da' : '#DDBEA9';
        if (chev) chev.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(45deg)';
      });
    });
  }

  // ── Formulaire de contact ────────────────────────────────────────────────
  // Le formulaire poste vers un Worker Cloudflare (voir 04_SCRIPTS/brevo-worker/)
  // qui relaie l'e-mail via l'API Brevo. La clé API Brevo reste côté serveur
  // (secret du Worker) — jamais exposée dans ce fichier ni dans le navigateur.
  var CONTACT_ENDPOINT = 'https://aufildutrace-contact.CHANGEME.workers.dev';

  function initForm() {
    var form = document.querySelector('[data-contact-form]');
    if (!form) return;
    var sentBlock = document.querySelector('[data-form-sent]');
    var errorBlock = form.querySelector('[data-form-error]');
    var submitBtn = form.querySelector('button[type="submit"]');
    var submitLabel = submitBtn ? submitBtn.textContent : '';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var prenom = form.querySelector('[name="prenom"]');
      var email = form.querySelector('[name="email"]');
      var telephone = form.querySelector('[name="telephone"]');
      var message = form.querySelector('[name="message"]');
      var honeypot = form.querySelector('[name="site_web"]');
      var errors = {};
      if (!prenom.value.trim()) errors.prenom = 'Merci d’indiquer votre prénom.';
      if (!email.value.trim()) errors.email = 'Merci d’indiquer votre e-mail.';
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) errors.email = 'Cet e-mail ne semble pas valide (ex. prenom@exemple.fr).';
      if (!message.value.trim()) errors.message = 'Merci de préciser votre question.';

      [prenom, email, message].forEach(function (field) {
        var name = field.getAttribute('name');
        var errEl = document.getElementById('err-' + name);
        if (errors[name]) {
          field.style.borderColor = '#B3261E';
          if (errEl) errEl.textContent = errors[name];
        } else {
          field.style.borderColor = 'var(--kaki)';
          if (errEl) errEl.textContent = '';
        }
      });
      if (Object.keys(errors).length) return;

      if (errorBlock) errorBlock.hidden = true;

      // Piège anti-spam : si ce champ caché est rempli, c'est un robot —
      // on affiche quand même le message de succès pour ne pas l'alerter,
      // mais on n'envoie rien à Brevo.
      if (honeypot && honeypot.value.trim()) {
        form.hidden = true;
        if (sentBlock) sentBlock.hidden = false;
        return;
      }

      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Envoi en cours…'; }

      fetch(CONTACT_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prenom: prenom.value.trim(),
          email: email.value.trim(),
          telephone: telephone ? telephone.value.trim() : '',
          message: message.value.trim()
        })
      })
        .then(function (res) {
          if (!res.ok) throw new Error('Réponse serveur ' + res.status);
          form.hidden = true;
          if (sentBlock) sentBlock.hidden = false;
        })
        .catch(function () {
          if (errorBlock) errorBlock.hidden = false;
        })
        .finally(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitLabel; }
        });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    scheduleReveals();
    initFaq();
    initForm();
  });
})();
