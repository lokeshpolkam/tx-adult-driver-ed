/**
 * Texas Adult Driver Education (ADE-1317)
 * Universal Dynamic Pricing Client Engine
 * 
 * Synchronizes course tuition, rush certificate delivery fees, and express totals
 * site-wide from the authoritative backend pricing configuration.
 * 
 * Eliminates all hardcoded pricing numbers ($38.00, etc.) across the platform.
 */

(function () {
  'use strict';

  // Resolve API Base URL
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const API_BASE = isLocal
    ? (window.location.port === '8080' ? '' : 'http://localhost:8080')
    : ''; // Relative path leverages Vercel vercel.json rewrite to Cloud Run

  const CACHE_KEY = 'tx_pricing_cache';
  const CACHE_TTL_MS = 60 * 1000; // 1-minute client cache to prevent repeated fetches

  let cachedPricing = null;

  function getCachedPricing() {
    try {
      const raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (Date.now() - parsed.timestamp < CACHE_TTL_MS) {
        return parsed.data;
      }
    } catch (_) {}
    return null;
  }

  function setCachedPricing(data) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        data,
        timestamp: Date.now()
      }));
    } catch (_) {}
  }

  /**
   * Apply pricing figures to all matching DOM elements
   */
  function applyPricingToDOM(p) {
    if (!p || typeof p.coursePriceCents !== 'number') return;

    const courseCents = p.coursePriceCents;
    const rushCents = p.rushPriceCents || 999;
    const totalExpressCents = courseCents + rushCents;

    const courseFormatted = p.coursePriceFormatted || `$${(courseCents / 100).toFixed(2)}`;
    const courseDollarsInt = `$${Math.round(courseCents / 100)}`;
    const courseWhole = Math.floor(courseCents / 100).toString();
    const courseDecimal = '.' + (courseCents % 100).toString().padStart(2, '0');

    const rushFormatted = p.rushPriceFormatted || `$${(rushCents / 100).toFixed(2)}`;
    const totalExpressFormatted = p.totalExpressFormatted || `$${(totalExpressCents / 100).toFixed(2)}`;

    // 1. Full formatted course price: e.g. "$38.00" or "$45.00"
    document.querySelectorAll('.dyn-price-full').forEach(el => {
      el.textContent = courseFormatted;
    });

    // 2. Integer course price: e.g. "$38" or "$45"
    document.querySelectorAll('.dyn-price-int').forEach(el => {
      el.textContent = courseDollarsInt;
    });

    // 3. Whole number split: e.g. "38" or "45"
    document.querySelectorAll('.dyn-price-whole').forEach(el => {
      el.textContent = courseWhole;
    });

    // 4. Decimal split: e.g. ".00"
    document.querySelectorAll('.dyn-price-decimal').forEach(el => {
      el.textContent = courseDecimal;
    });

    // 5. Rush delivery fee
    document.querySelectorAll('.dyn-rush-price').forEach(el => {
      el.textContent = rushFormatted;
    });

    // 6. Rush delivery badge: e.g. "+$9.99"
    document.querySelectorAll('.dyn-rush-badge').forEach(el => {
      el.textContent = `+${rushFormatted}`;
    });

    // 7. Total express combined
    document.querySelectorAll('.dyn-total-express').forEach(el => {
      el.textContent = totalExpressFormatted;
    });

    // 8. Update Schema.org JSON-LD scripts dynamically if present
    document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
      try {
        const json = JSON.parse(script.textContent);
        let modified = false;

        function updateSchema(obj) {
          if (!obj || typeof obj !== 'object') return;
          if (obj['@type'] === 'Offer' && obj.price) {
            obj.price = (courseCents / 100).toFixed(2);
            modified = true;
          }
          if (obj['@type'] === 'MonetaryAmount' && obj.value) {
            obj.value = courseWhole;
            modified = true;
          }
          for (const k of Object.keys(obj)) {
            if (typeof obj[k] === 'object') updateSchema(obj[k]);
          }
        }

        updateSchema(json);
        if (modified) {
          script.textContent = JSON.stringify(json, null, 2);
        }
      } catch (_) {}
    });

    // Dispatch global event for custom page handlers (checkout.html, player.html)
    window.dispatchEvent(new CustomEvent('txPricingLoaded', { detail: p }));
  }

  /**
   * Fetch fresh pricing from the API
   */
  async function fetchPricing(force = false) {
    if (!force) {
      const cached = getCachedPricing();
      if (cached) {
        cachedPricing = cached;
        applyPricingToDOM(cached);
        return cached;
      }
    }

    try {
      const endpoint = `${API_BASE}/api/v1/billing/pricing`;
      const res = await fetch(endpoint);
      if (res.ok) {
        const data = await res.json();
        if (data.success && typeof data.coursePriceCents === 'number') {
          cachedPricing = data;
          setCachedPricing(data);
          applyPricingToDOM(data);
          return data;
        }
      }
    } catch (err) {
      console.warn('[PRICING CLIENT] Live fetch warning:', err.message);
    }

    // Statutory default fallback
    const fallback = {
      coursePriceCents: 3800,
      rushPriceCents: 999,
      coursePriceFormatted: '$38.00',
      rushPriceFormatted: '$9.99',
      totalExpressCents: 4799,
      totalExpressFormatted: '$47.99',
    };
    cachedPricing = fallback;
    applyPricingToDOM(fallback);
    return fallback;
  }

  // Public API
  window.getCoursePricing = fetchPricing;

  // Immediate execution on DOM load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => fetchPricing());
  } else {
    fetchPricing();
  }
})();
