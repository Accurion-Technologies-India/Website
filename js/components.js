/* ============================================================
   Accurion Technologies — Shared Components
   Injects navbar, mobile nav overlay, footer, and WhatsApp
   button into every page via DOMContentLoaded.

   Usage: <script src="/js/components.js"></script>
   Body attribute: data-page="home|about|products|services|blogs|contact|shop"
   ============================================================ */

(function () {
  'use strict';

  /* ── Root path detection ────────────────────────────────── */
  // The <base href="/Website/"> tag in each HTML page handles path
  // resolution, so we use empty root.  All relative URLs like
  // "index.html" will automatically resolve to "/Website/index.html".
  // When switching to a custom domain, remove the <base> tags and
  // revert root to the old depth-based calculation if needed.
  var root = '';

  /* ── Navbar ─────────────────────────────────────────────── */
  function buildNavbar() {
    var page = document.body.getAttribute('data-page') || '';

    function a(p) { return page === p ? ' active' : ''; }

    var nav = document.createElement('nav');
    nav.className = 'navbar';
    nav.id = 'navbar';
    nav.setAttribute('role', 'navigation');
    nav.setAttribute('aria-label', 'Main navigation');
    nav.innerHTML = `
<div class="container">
  <div class="navbar-inner">

    <a href="${root}index.html" class="navbar-logo" aria-label="Accurion Technologies Home">
      <img src="${root}assets/logo/PNG FILE-20260622T084410Z-3-001/PNG FILE/WITHOUT TAGLINE New Logo-01.png" alt="Accurion Technologies" />
    </a>

    <ul class="navbar-nav" role="list">
      <li class="nav-item"><a href="${root}index.html" class="nav-link${a('home')}">Home</a></li>
      <li class="nav-item"><a href="${root}about.html" class="nav-link${a('about')}">About Us</a></li>
      <li class="nav-item">
        <a href="${root}products/index.html" class="nav-link${a('products')}" aria-haspopup="true">
          Our Products <span class="nav-arrow">▾</span>
        </a>
        <div class="mega-menu" role="menu">
          <div class="mega-menu-group">
            <h4>Civil Testing</h4>
            <a href="${root}products/concrete-testing.html">Concrete Testing</a>
            <a href="${root}products/cement-testing.html">Cement Testing</a>
            <a href="${root}products/soil-testing.html">Soil Testing</a>
            <a href="${root}products/bitumen-testing.html">Bitumen Testing</a>
            <a href="${root}products/aggregate-testing.html">Aggregate Testing</a>
            <a href="${root}products/ndt-equipment.html">NDT Equipment</a>
          </div>
          <div class="mega-menu-group">
            <h4>Water &amp; Chemicals</h4>
            <a href="${root}products/water-testing.html">Water Testing</a>
            <a href="${root}products/lab-chemicals.html">Lab Chemicals</a>
            <a href="${root}products/lab-glassware.html">Lab Glassware</a>
            <a href="${root}products/lab-moulds.html">Moulds &amp; Apparatus</a>
          </div>
          <div class="mega-menu-group">
            <h4>Instruments</h4>
            <a href="${root}products/lab-balances.html">Lab Balances</a>
            <a href="${root}products/compression-machines.html">Compression Machines</a>
            <a href="${root}products/sieves-shakers.html">Sieves &amp; Shakers</a>
            <a href="${root}products/general-lab.html">General Lab Equipment</a>
          </div>
        </div>
      </li>
      <li class="nav-item"><a href="${root}services.html" class="nav-link${a('services')}">Services</a></li>
      <li class="nav-item"><a href="${root}shop-coming-soon.html" class="nav-link${a('shop')}">Shop Online</a></li>
      <li class="nav-item"><a href="${root}blogs.html" class="nav-link${a('blogs')}">Blogs</a></li>
      <li class="nav-item"><a href="${root}contact.html" class="nav-link nav-cta${a('contact')}">Contact Us</a></li>
    </ul>

    <div class="navbar-actions">
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>

  </div>
</div>`;

    document.body.insertBefore(nav, document.body.firstChild);
  }

  /* ── Mobile Nav ─────────────────────────────────────────── */
  function buildMobileNav() {
    var mobileHTML = `
<nav class="mobile-nav" id="mobileNav" aria-label="Mobile navigation">
  <ul class="mobile-nav-list">
    <li class="mobile-nav-item"><a href="${root}index.html" class="mobile-nav-link">Home</a></li>
    <li class="mobile-nav-item"><a href="${root}about.html" class="mobile-nav-link">About Us</a></li>
    <li class="mobile-nav-item">
      <a href="javascript:void(0)" class="mobile-nav-link" id="mobileProductsToggle">
        Our Products <span class="mobile-arrow" style="transition:transform 0.3s;display:inline-block;">▾</span>
      </a>
      <div class="mobile-nav-accordion" id="mobileProductsAccordion">
        <p class="mobile-nav-accordion-heading">Civil Testing</p>
        <a href="${root}products/concrete-testing.html">Concrete Testing</a>
        <a href="${root}products/cement-testing.html">Cement Testing</a>
        <a href="${root}products/soil-testing.html">Soil Testing</a>
        <a href="${root}products/bitumen-testing.html">Bitumen Testing</a>
        <a href="${root}products/aggregate-testing.html">Aggregate Testing</a>
        <a href="${root}products/ndt-equipment.html">NDT Equipment</a>
        <p class="mobile-nav-accordion-heading">Water &amp; Chemicals</p>
        <a href="${root}products/water-testing.html">Water Testing</a>
        <a href="${root}products/lab-chemicals.html">Lab Chemicals</a>
        <a href="${root}products/lab-glassware.html">Lab Glassware</a>
        <a href="${root}products/lab-moulds.html">Moulds &amp; Apparatus</a>
        <p class="mobile-nav-accordion-heading">Instruments</p>
        <a href="${root}products/lab-balances.html">Lab Balances</a>
        <a href="${root}products/compression-machines.html">Compression Machines</a>
        <a href="${root}products/sieves-shakers.html">Sieves &amp; Shakers</a>
        <a href="${root}products/general-lab.html">General Lab Equipment</a>
      </div>
    </li>
    <li class="mobile-nav-item"><a href="${root}services.html" class="mobile-nav-link">Services</a></li>
    <li class="mobile-nav-item"><a href="${root}shop-coming-soon.html" class="mobile-nav-link">Shop Online</a></li>
    <li class="mobile-nav-item"><a href="${root}blogs.html" class="mobile-nav-link">Blogs</a></li>
    <li class="mobile-nav-item"><a href="${root}contact.html" class="mobile-nav-link" style="color:var(--color-primary);font-weight:700;">Contact Us</a></li>
  </ul>
</nav>
<div class="mobile-nav-overlay" id="mobileOverlay"></div>`;

    var wrapper = document.createElement('div');
    wrapper.innerHTML = mobileHTML.trim();
    // Insert each child node after the navbar
    var navbar = document.getElementById('navbar');
    while (wrapper.firstChild) {
      navbar.parentNode.insertBefore(wrapper.firstChild, navbar.nextSibling);
    }
  }

  /* ── Footer ─────────────────────────────────────────────── */
  function buildFooter() {
    var footer = document.createElement('footer');
    footer.className = 'footer';
    footer.setAttribute('role', 'contentinfo');
    footer.innerHTML = `
<div class="container">
  <div class="footer-grid">

    <div class="footer-brand">
      <img src="${root}assets/logo/PNG FILE-20260622T084410Z-3-001/PNG FILE/WITHOUT TAGLINE New Logo-01.png" alt="Accurion Technologies" />
      <p class="footer-tagline">Where Accuracy Meets Innovation</p>
      <p class="footer-blurb">Trusted manufacturer, supplier &amp; service provider of complete Civil Quality Laboratory Equipment and NABL-accredited calibration solutions. Serving clients across India from Delhi.</p>
      <div class="footer-social">
        <a href="https://facebook.com/accuriontechnologies" class="footer-social-link" target="_blank" rel="noopener" aria-label="Facebook">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
        </a>
        <a href="https://instagram.com/accuriontechnologies" class="footer-social-link" target="_blank" rel="noopener" aria-label="Instagram">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
        </a>
        <a href="https://linkedin.com/company/accuriontechnologies" class="footer-social-link" target="_blank" rel="noopener" aria-label="LinkedIn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
        </a>
        <a href="https://youtube.com/@accuriontechnologies" class="footer-social-link" target="_blank" rel="noopener" aria-label="YouTube">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46a2.78 2.78 0 0 0-1.95 1.96A29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58A2.78 2.78 0 0 0 3.41 19.6C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.95A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58z"/><polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="white"/></svg>
        </a>
      </div>
    </div>

    <div class="footer-col">
      <h4>Quick Links</h4>
      <ul class="footer-links">
        <li><a href="${root}index.html">Home</a></li>
        <li><a href="${root}about.html">About Us</a></li>
        <li><a href="${root}products/index.html">Our Products</a></li>
        <li><a href="${root}services.html">Services</a></li>
        <li><a href="${root}shop-coming-soon.html">Shop Online</a></li>
        <li><a href="${root}blogs.html">Blogs</a></li>
        <li><a href="${root}contact.html">Contact Us</a></li>
      </ul>
    </div>

    <div class="footer-col">
      <h4>Product Categories</h4>
      <ul class="footer-links">
        <li><a href="${root}products/concrete-testing.html">Concrete Testing</a></li>
        <li><a href="${root}products/soil-testing.html">Soil Testing</a></li>
        <li><a href="${root}products/bitumen-testing.html">Bitumen Testing</a></li>
        <li><a href="${root}products/lab-balances.html">Lab Balances</a></li>
        <li><a href="${root}products/water-testing.html">Water Testing</a></li>
        <li><a href="${root}products/compression-machines.html">Compression Machines</a></li>
        <li><a href="${root}products/index.html" style="color:var(--color-primary);">View All →</a></li>
      </ul>
    </div>

    <div class="footer-col">
      <h4>Contact Us</h4>
      <div class="footer-contact-item">
        <span class="footer-contact-icon">📍</span>
        <span>E-43, 3rd Floor, St. No. 1, Parshuram Gali, West Jyoti Nagar, Delhi – 110094</span>
      </div>
      <div class="footer-contact-item">
        <span class="footer-contact-icon">📞</span>
        <span>
          <a href="tel:+918383851980">+91 83838 51980</a><br>
          <a href="tel:+918920938292">+91 89209 38292</a>
        </span>
      </div>
      <div class="footer-contact-item">
        <span class="footer-contact-icon">💬</span>
        <a href="https://wa.me/918383851980" target="_blank" rel="noopener">WhatsApp: +91 83838 51980</a>
      </div>
      <div class="footer-contact-item">
        <span class="footer-contact-icon">✉️</span>
        <span>
          <a href="mailto:accuriontechnologies@gmail.com">accuriontechnologies@gmail.com</a><br>
          <a href="mailto:sales.accuriontechnologies@gmail.com">sales.accuriontechnologies@gmail.com</a>
        </span>
      </div>
    </div>

  </div>
  <div class="footer-bottom">
    <p>© 2025 Accurion Technologies. All Rights Reserved. | Designed with precision.</p>
    <p><a href="${root}sitemap.xml" style="color:rgba(255,255,255,0.3);font-size:0.75rem;">Sitemap</a></p>
  </div>
</div>`;

    document.body.appendChild(footer);
  }

  /* ── WhatsApp Float ─────────────────────────────────────── */
  function buildWhatsApp() {
    var wa = document.createElement('a');
    wa.href = 'https://wa.me/918383851980?text=Hello%2C%20I%27m%20interested%20in%20your%20products%2Fservices.%20Please%20get%20in%20touch.';
    wa.className = 'whatsapp-float';
    wa.setAttribute('target', '_blank');
    wa.setAttribute('rel', 'noopener');
    wa.setAttribute('aria-label', 'Chat with us on WhatsApp');
    wa.innerHTML = `
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
</svg>
<span class="whatsapp-tooltip">Chat on WhatsApp</span>`;
    document.body.appendChild(wa);
  }

  /* ── Init ───────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    buildNavbar();
    buildMobileNav();
    buildFooter();
    buildWhatsApp();
  });

})();
