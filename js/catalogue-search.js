/**
 * Accurion Technologies — Client-Side Catalogue Search & Filter Engine
 * Powered by static products/products.json index
 * Instantaneous fuzzy/keyword search across Name, SKU, Category, and IS Standards.
 */

(function () {
  'use strict';

  let productsIndex = [];
  let isLoaded = false;
  let activeCategory = 'all';

  const searchInput = document.getElementById('catalogue-search-input');
  const clearBtn = document.getElementById('catalogue-search-clear');
  const filterPillsContainer = document.getElementById('catalogue-filter-pills');
  const resultsContainer = document.getElementById('catalogue-search-results');
  const resultsGrid = document.getElementById('catalogue-results-grid');
  const resultsCount = document.getElementById('catalogue-results-count');
  const defaultCategoriesSection = document.getElementById('default-categories-grid');

  if (!searchInput || !resultsContainer) {
    return;
  }

  // Fetch static products.json
  async function loadIndex() {
    if (isLoaded) return;
    try {
      const response = await fetch('products/products.json');
      if (response.ok) {
        productsIndex = await response.json();
        isLoaded = true;
      }
    } catch (err) {
      console.warn('Could not load products search index:', err);
    }
  }

  // Pre-load on hover or focus of search input
  searchInput.addEventListener('focus', loadIndex);
  searchInput.addEventListener('mouseenter', loadIndex);
  window.addEventListener('DOMContentLoaded', loadIndex);

  // Normalize string for fuzzy match
  function normalize(str) {
    return (str || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  }

  function matchesItem(item, query, catFilter) {
    // 1. Category Filter check
    if (catFilter !== 'all' && item.category !== catFilter) {
      return false;
    }

    if (!query) {
      return true;
    }

    const q = query.toLowerCase().trim();
    const qNorm = normalize(query);

    // Exact or normalized SKU / Code match (Highest priority)
    if (item.code && (item.code.toLowerCase().includes(q) || normalize(item.code).includes(qNorm))) {
      return true;
    }

    // Name match
    if (item.name && item.name.toLowerCase().includes(q)) {
      return true;
    }

    // Short description match
    if (item.short_description && item.short_description.toLowerCase().includes(q)) {
      return true;
    }

    // Category / subcategory match
    if (item.category && item.category.toLowerCase().includes(q)) {
      return true;
    }
    if (item.subcategory && item.subcategory.toLowerCase().includes(q)) {
      return true;
    }

    // Specifications search (e.g. "IS 13311", "2.207 J", "2000 kN", "OLED", "Bluetooth")
    if (item.specifications && Array.isArray(item.specifications)) {
      for (const spec of item.specifications) {
        const p = (spec.parameter || '').toLowerCase();
        const v = (spec.value || '').toLowerCase();
        if (p.includes(q) || v.includes(q)) {
          return true;
        }
      }
    }

    return false;
  }

  function highlightMatch(text, query) {
    if (!query || !text) return text;
    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escaped})`, 'gi');
    return text.replace(regex, '<mark style="background: rgba(196,18,23,0.15); color: #c41217; padding: 0 2px; border-radius: 2px;">$1</mark>');
  }

  function renderResults(matches, query) {
    if (!matches || matches.length === 0) {
      resultsCount.innerHTML = `No instruments found matching "<strong>${escapeHtml(query)}</strong>"`;
      resultsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 48px 20px; background: var(--color-surface); border: 1px dashed var(--color-border); border-radius: 16px;">
          <div style="font-size: 2.4rem; margin-bottom: 12px;">🔍</div>
          <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 8px;">No matching equipment found</h3>
          <p style="color: var(--color-text-secondary); max-width: 480px; margin: 0 auto 20px;">
            We manufacture and supply custom civil laboratory setups. Contact our engineering team for inquiries about unlisted models.
          </p>
          <a href="contact" class="btn btn-primary">Request Custom Instrument Quote</a>
        </div>
      `;
      return;
    }

    resultsCount.innerHTML = `Found <strong>${matches.length}</strong> instrument${matches.length === 1 ? '' : 's'}${query ? ` matching "<strong>${escapeHtml(query)}</strong>"` : ''}`;

    const cardsHtml = matches.map(item => {
      const displayName = query ? highlightMatch(escapeHtml(item.name), query) : escapeHtml(item.name);
      const displayCode = query ? highlightMatch(escapeHtml(item.code), query) : escapeHtml(item.code);
      const displayDesc = query ? highlightMatch(escapeHtml(item.short_description || ''), query) : escapeHtml(item.short_description || '');

      // Specs snippet
      let specsPreview = '';
      if (item.specifications && item.specifications.length > 0) {
        const topSpecs = item.specifications.slice(0, 3);
        specsPreview = `
          <ul style="list-style: none; padding: 0; margin: 12px 0 16px; font-size: 0.82rem; color: var(--color-text-secondary); display: flex; flex-direction: column; gap: 4px;">
            ${topSpecs.map(s => `<li><strong>${escapeHtml(s.parameter)}:</strong> ${escapeHtml(s.value)}</li>`).join('')}
          </ul>
        `;
      }

      return `
        <div class="product-card" style="display: flex; flex-direction: column; height: 100%;">
          <div class="product-card-img-wrap" style="height: 220px;">
            <img src="${item.featured_image || 'images/categories/ndt-equipment.jpg'}" alt="${escapeHtml(item.name)}" class="product-card-img" width="300" height="200" loading="lazy" />
            <div class="product-badges">
              <span class="product-badge badge-popular">${escapeHtml(item.category)}</span>
            </div>
          </div>
          <div class="product-card-body" style="display: flex; flex-direction: column; flex: 1;">
            <div class="product-model-tag" style="font-size: 0.82rem; font-weight: 700; color: var(--color-primary); margin-bottom: 6px;">
              Model ${displayCode}
            </div>
            <h3 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 8px; line-height: 1.35;">
              <a href="${item.url}" style="color: inherit; text-decoration: none;">${displayName}</a>
            </h3>
            <p style="font-size: 0.85rem; color: var(--color-text-secondary); line-height: 1.5; margin-bottom: 10px;">
              ${displayDesc}
            </p>
            ${specsPreview}
            <div style="margin-top: auto; display: flex; gap: 8px; padding-top: 14px; border-top: 1px solid var(--color-border);">
              <a href="${item.url}" class="btn btn-outline" style="flex: 1; justify-content: center; font-size: 0.85rem; padding: 8px 12px;">View Details</a>
              <a href="contact?product=${encodeURIComponent(item.name)}" class="btn btn-primary" style="flex: 1; justify-content: center; font-size: 0.85rem; padding: 8px 12px;">Enquire</a>
            </div>
          </div>
        </div>
      `;
    }).join('');

    resultsGrid.innerHTML = cardsHtml;
  }

  function executeSearch() {
    const query = searchInput.value.trim();

    if (query) {
      if (clearBtn) clearBtn.style.display = 'block';
    } else {
      if (clearBtn) clearBtn.style.display = 'none';
    }

    // If no search query and category is "all", show default categories grid
    if (!query && activeCategory === 'all') {
      resultsContainer.style.display = 'none';
      if (defaultCategoriesSection) defaultCategoriesSection.style.display = 'grid';
      return;
    }

    // Otherwise, show live search results
    if (defaultCategoriesSection) defaultCategoriesSection.style.display = 'none';
    resultsContainer.style.display = 'block';

    const matches = productsIndex.filter(item => matchesItem(item, query, activeCategory));
    renderResults(matches, query);
  }

  // Event Listeners
  searchInput.addEventListener('input', function () {
    if (!isLoaded) {
      loadIndex().then(executeSearch);
    } else {
      executeSearch();
    }
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      searchInput.value = '';
      activeCategory = 'all';
      updateActiveFilterPills();
      executeSearch();
      searchInput.focus();
    });
  }

  // Filter Pills Clicking
  if (filterPillsContainer) {
    filterPillsContainer.addEventListener('click', function (e) {
      const btn = e.target.closest('button[data-filter]');
      if (!btn) return;
      activeCategory = btn.getAttribute('data-filter');
      updateActiveFilterPills();
      if (!isLoaded) {
        loadIndex().then(executeSearch);
      } else {
        executeSearch();
      }
    });
  }

  function updateActiveFilterPills() {
    if (!filterPillsContainer) return;
    const pills = filterPillsContainer.querySelectorAll('button[data-filter]');
    pills.forEach(p => {
      if (p.getAttribute('data-filter') === activeCategory) {
        p.classList.add('active');
        p.style.backgroundColor = 'var(--color-primary)';
        p.style.color = '#ffffff';
        p.style.borderColor = 'var(--color-primary)';
      } else {
        p.classList.remove('active');
        p.style.backgroundColor = 'var(--color-surface)';
        p.style.color = 'var(--color-text)';
        p.style.borderColor = 'var(--color-border)';
      }
    });
  }

  // Quick Chips
  document.addEventListener('click', function (e) {
    const chip = e.target.closest('[data-quick-search]');
    if (!chip) return;
    const term = chip.getAttribute('data-quick-search');
    searchInput.value = term;
    activeCategory = 'all';
    updateActiveFilterPills();
    if (!isLoaded) {
      loadIndex().then(executeSearch);
    } else {
      executeSearch();
    }
    searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  function escapeHtml(str) {
    return (str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

})();
