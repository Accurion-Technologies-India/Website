/* ============================================================
   Accurion Technologies — Main JS
   Handles: Dark mode, Navbar scroll, Mobile menu, Hero carousel,
            Scroll-reveal, Active nav link, Smooth anchor scroll
   ============================================================ */

(function () {
  'use strict';

  /* ── Theme must init BEFORE DOMContentLoaded to avoid FOUC ── */
  const THEME_KEY = 'accurion-theme';
  const html = document.documentElement;

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    const toggle = document.getElementById('themeToggle');
    if (toggle) {
      toggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      toggle.innerHTML = theme === 'dark'
        ? '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
        : '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
  }

  // Clean .html and /index.html from URL bar immediately if present
  (function cleanUrlEarly() {
    try {
      var path = window.location.pathname;
      if (path && (path.endsWith('.html') || path.endsWith('/index') || path.endsWith('/index.html'))) {
        var clean = path
          .replace(/\/index\.html$/, '/')
          .replace(/\/index$/, '/')
          .replace(/\.html$/, '');
        if (!clean) clean = '/';
        var newUrl = clean + window.location.search + window.location.hash;
        window.history.replaceState(null, '', newUrl);
      }
    } catch (e) {}
  })();

  // Apply stored or system theme immediately (before DOM ready, to prevent flash)
  (function initThemeEarly() {
    const stored = localStorage.getItem(THEME_KEY);
    html.setAttribute('data-theme', stored || getSystemTheme());
  })();

  // Listen for system preference changes (only if user has no stored preference)
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    if (!localStorage.getItem(THEME_KEY)) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  /* ── Everything else waits for DOM + components.js to inject HTML ── */
  document.addEventListener('DOMContentLoaded', function () {

    /* ── 1. Dark / Light Mode toggle ─────────────────────── */
    // Re-apply now that #themeToggle exists in the DOM (injected by components.js)
    applyTheme(localStorage.getItem(THEME_KEY) || getSystemTheme());

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function () {
        const current = html.getAttribute('data-theme') || getSystemTheme();
        const next = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem(THEME_KEY, next);
        applyTheme(next);
      });
    }

    /* ── 2. Navbar Scroll Effect ──────────────────────────── */
    const navbar = document.getElementById('navbar');

    function handleNavbarScroll() {
      if (!navbar) return;
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    }

    window.addEventListener('scroll', handleNavbarScroll, { passive: true });
    handleNavbarScroll();

    /* ── 3. Mobile Menu ───────────────────────────────────── */
    const hamburger    = document.getElementById('hamburger');
    const mobileNav    = document.getElementById('mobileNav');
    const mobileOverlay = document.getElementById('mobileOverlay');

    function openMobileNav() {
      if (!mobileNav) return;
      mobileNav.classList.add('open');
      mobileOverlay.classList.add('open');
      hamburger.classList.add('open');
      hamburger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }

    function closeMobileNav() {
      if (!mobileNav) return;
      mobileNav.classList.remove('open');
      mobileOverlay.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }

    if (hamburger) {
      hamburger.addEventListener('click', function () {
        mobileNav.classList.contains('open') ? closeMobileNav() : openMobileNav();
      });
    }

    if (mobileOverlay) {
      mobileOverlay.addEventListener('click', closeMobileNav);
    }

    // Accordion: Our Products in mobile menu
    const mobileProductsToggle    = document.getElementById('mobileProductsToggle');
    const mobileProductsAccordion = document.getElementById('mobileProductsAccordion');

    if (mobileProductsToggle && mobileProductsAccordion) {
      mobileProductsToggle.addEventListener('click', function (e) {
        e.preventDefault();
        const isOpen = mobileProductsAccordion.classList.contains('open');
        mobileProductsAccordion.classList.toggle('open', !isOpen);
        const arrow = mobileProductsToggle.querySelector('.mobile-arrow');
        if (arrow) arrow.style.transform = isOpen ? '' : 'rotate(180deg)';
      });
    }

    // Close mobile nav when a link is clicked
    document.querySelectorAll('.mobile-nav-link:not(#mobileProductsToggle), .mobile-nav-accordion a')
      .forEach(function (link) {
        link.addEventListener('click', closeMobileNav);
      });

    /* ── 4. Hero Carousel ─────────────────────────────────── */
    const heroCarousel = document.getElementById('heroCarousel');

    if (heroCarousel) {
      const slides = heroCarousel.querySelectorAll('.hero-slide');
      const dots   = heroCarousel.querySelectorAll('.hero-dot');
      let current  = 0;
      let autoPlayTimer = null;
      const INTERVAL = 5000;

      function goToSlide(index) {
        slides[current].classList.remove('active');
        if (dots[current]) dots[current].classList.remove('active');
        current = (index + slides.length) % slides.length;
        slides[current].classList.add('active');
        if (dots[current]) dots[current].classList.add('active');
      }

      function startAutoPlay() {
        stopAutoPlay();
        autoPlayTimer = setInterval(function () { goToSlide(current + 1); }, INTERVAL);
      }

      function stopAutoPlay() {
        if (autoPlayTimer) { clearInterval(autoPlayTimer); autoPlayTimer = null; }
      }

      // Dot clicks
      dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () { goToSlide(i); stopAutoPlay(); startAutoPlay(); });
      });

      // Arrow buttons
      const prevBtn = document.getElementById('heroPrev');
      const nextBtn = document.getElementById('heroNext');
      if (prevBtn) prevBtn.addEventListener('click', function () { goToSlide(current - 1); stopAutoPlay(); startAutoPlay(); });
      if (nextBtn) nextBtn.addEventListener('click', function () { goToSlide(current + 1); stopAutoPlay(); startAutoPlay(); });

      // Touch / swipe
      let touchStartX = 0;
      heroCarousel.addEventListener('touchstart', function (e) { touchStartX = e.touches[0].clientX; }, { passive: true });
      heroCarousel.addEventListener('touchend', function (e) {
        const diff = touchStartX - e.changedTouches[0].clientX;
        if (Math.abs(diff) > 50) { goToSlide(diff > 0 ? current + 1 : current - 1); stopAutoPlay(); startAutoPlay(); }
      }, { passive: true });

      // Pause on hover / tab visibility
      heroCarousel.addEventListener('mouseenter', stopAutoPlay);
      heroCarousel.addEventListener('mouseleave', startAutoPlay);
      document.addEventListener('visibilitychange', function () {
        document.hidden ? stopAutoPlay() : startAutoPlay();
      });

      // Init
      if (slides.length > 0) {
        slides[0].classList.add('active');
        if (dots[0]) dots[0].classList.add('active');
        startAutoPlay();
      }
    }

    /* ── 5. Scroll Reveal ─────────────────────────────────── */
    const revealElements = document.querySelectorAll('.reveal');

    if (revealElements.length > 0 && 'IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -48px 0px' });

      revealElements.forEach(function (el) { revealObserver.observe(el); });
    } else {
      revealElements.forEach(function (el) { el.classList.add('visible'); });
    }

    /* ── 6. Active Nav Link ───────────────────────────────── */
    const rawPath = window.location.pathname;
    const currentPath = rawPath.replace(/\/index\.html$/, '/').replace(/\.html$/, '') || '/';
    document.querySelectorAll('.nav-link').forEach(function (link) {
      const href = link.getAttribute('href');
      if (!href) return;
      const cleanHref = href.replace(/^(\.\/|\/|\.\.\/)+/, '').replace(/\/index\.html$/, '').replace(/\.html$/, '').replace(/\/$/, '');
      const isHome = (href === '/' || href === './' || href === '' || href.endsWith('index.html')) &&
                     (currentPath === '/' || currentPath === '');
      const isMatch = !isHome && href !== '#' && cleanHref &&
                      (currentPath === '/' + cleanHref || currentPath.endsWith('/' + cleanHref) || currentPath.includes(cleanHref));
      if (isHome || isMatch) link.classList.add('active');
    });

    /* ── 7. Smooth Anchor Scrolling ───────────────────────── */
    const navbarEl = document.getElementById('navbar');
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          const navH = navbarEl ? navbarEl.offsetHeight : 72;
          window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - navH - 16, behavior: 'smooth' });
        }
      });
    });

  }); // end DOMContentLoaded

})();
