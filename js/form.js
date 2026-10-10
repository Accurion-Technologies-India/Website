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
    const requestType = params.get('request');
    const messageField = document.getElementById('message');
    const subjectField = document.getElementById('subject');

    if (product) {
      const decoded = decodeURIComponent(product.replace(/\+/g, ' '));
      if (requestType === 'catalogue') {
        if (messageField) {
          messageField.value = 'Please send me the official product catalogue, data sheet, and technical specifications for: ' + decoded + '.\n\nThank you.';
        }
        if (subjectField) {
          subjectField.value = 'Catalogue Request: ' + decoded;
        }
      } else {
        if (messageField) {
          messageField.value = 'I am interested in: ' + decoded + '.\n\nPlease send me more details and pricing.';
        }
        if (subjectField && !subjectField.value) {
          subjectField.value = 'Enquiry: ' + decoded;
        }
      }
    }
  /* ── 1b. Save Enquiry to Local CRM Storage ────────────────── */
  function saveLocalEnquiry(formData) {
    try {
      var enquiries = JSON.parse(localStorage.getItem('accurion_enquiries') || '[]');
      var randomSuffix = Math.floor(1000 + Math.random() * 9000);
      var newEntry = {
        id: 'ENQ-' + randomSuffix,
        date: new Date().toISOString(),
        name: formData.get('name') || '',
        company: formData.get('company') || 'Direct / Individual',
        phone: formData.get('phone') || '',
        email: formData.get('email') || '',
        subject: formData.get('subject') || 'General Equipment Enquiry',
        message: formData.get('message') || '',
        status: 'New',
        notes: ''
      };
      enquiries.unshift(newEntry);
      localStorage.setItem('accurion_enquiries', JSON.stringify(enquiries));
    } catch (err) {
      console.warn('Could not store enquiry locally:', err);
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
        if (field.type === 'checkbox') {
          if (!field.checked) {
            field.style.outline = '2px solid #C41217';
            valid = false;
          } else {
            field.style.outline = '';
          }
        } else if (!field.value.trim()) {
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

      var formData = new FormData(form);
      saveLocalEnquiry(formData);

      try {
        var response = await fetch(form.action, {
          method: 'POST',
          body: formData,
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
