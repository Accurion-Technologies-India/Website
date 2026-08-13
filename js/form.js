/* ============================================================
   Accurion Technologies — Form JS
   Handles: Contact form Formspree submission + URL param pre-fill
   ============================================================ */

(function () {
  'use strict';

  /* ── 1. Pre-fill from URL param ─────────────────────────── */
  function prefillFromURL() {
    const params = new URLSearchParams(window.location.search);
    const product = params.get('product');
    const messageField = document.getElementById('message');
    const subjectField = document.getElementById('subject');

    if (product && messageField) {
      const decoded = decodeURIComponent(product.replace(/\+/g, ' '));
      messageField.value = 'I am interested in: ' + decoded + '.\n\nPlease send me more details and pricing.';
      if (subjectField && !subjectField.value) {
        subjectField.value = 'Enquiry: ' + decoded;
      }
    }
  }

  /* ── 2. Contact Form Submission ─────────────────────────── */
  function initContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    // Guard: prevent double-binding if called more than once
    if (form.dataset.bound === 'true') return;
    form.dataset.bound = 'true';

    const submitBtn = form.querySelector('[type="submit"]');
    const successMsg = document.getElementById('formSuccess');
    const errorMsg = document.getElementById('formError');

    form.addEventListener('submit', async function (e) {
      e.preventDefault();

      // Hide any previous messages first
      if (successMsg) successMsg.style.display = 'none';
      if (errorMsg)   errorMsg.style.display = 'none';

      // Validate required fields
      const required = form.querySelectorAll('[required]');
      let valid = true;
      required.forEach(function (field) {
        field.style.borderColor = '';
        if (!field.value.trim()) {
          field.style.borderColor = '#C41217';
          valid = false;
        }
      });
      if (!valid) return;

      // Disable submit button while sending
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending\u2026';
      }

      var succeeded = false;

      try {
        var response = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'Accept': 'application/json' }
        });

        if (response.ok) {
          succeeded = true;
          form.reset();
          if (successMsg) {
            successMsg.style.display = 'block';
            successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        } else {
          // Log Formspree's error detail to console for debugging
          try {
            var json = await response.json();
            var reason = (json && json.error) ? json.error
                       : (json && json.errors) ? json.errors.map(function(er){ return er.message; }).join(', ')
                       : 'HTTP ' + response.status;
            console.error('Formspree rejected submission:', reason);
          } catch (_) {
            console.error('Formspree error, status:', response.status);
          }
        }
      } catch (networkErr) {
        console.error('Form network error:', networkErr.message);
      }

      // Show error once only if submission did not succeed
      if (!succeeded && errorMsg) {
        errorMsg.style.display = 'block';
      }

      // Re-enable submit button
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
      }
    });
  }

  /* ── Init ───────────────────────────────────────────────── */
  // Scripts load at end of <body> so DOM is usually already ready.
  // Handle both cases to avoid missed or duplicate DOMContentLoaded events.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      prefillFromURL();
      initContactForm();
    });
  } else {
    prefillFromURL();
    initContactForm();
  }

})();
