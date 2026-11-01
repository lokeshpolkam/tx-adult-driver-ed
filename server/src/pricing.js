const db = require('./db');

let cachedPricing = null;
let cacheTime = 0;
const CACHE_TTL_MS = 5000; // 5-second in-memory cache to keep lookups ultra-fast

async function getPricing() {
  const now = Date.now();
  if (cachedPricing && (now - cacheTime < CACHE_TTL_MS)) {
    return cachedPricing;
  }

  try {
    const res = await db.query(
      `SELECT course_price_cents, rush_certificate_price_cents, updated_at
       FROM pricing_config WHERE id = 'default'`
    );
    if (res.rows.length > 0) {
      const row = res.rows[0];
      const coursePriceCents = parseInt(row.course_price_cents, 10) || 3800;
      const rushPriceCents = parseInt(row.rush_certificate_price_cents, 10) || 999;
      cachedPricing = {
        coursePriceCents,
        rushPriceCents,
        coursePriceFormatted: `$${(coursePriceCents / 100).toFixed(2)}`,
        rushPriceFormatted: `$${(rushPriceCents / 100).toFixed(2)}`,
        totalExpressCents: coursePriceCents + rushPriceCents,
        totalExpressFormatted: `$${((coursePriceCents + rushPriceCents) / 100).toFixed(2)}`,
        updatedAt: row.updated_at,
      };
      cacheTime = now;
      return cachedPricing;
    }
  } catch (err) {
    console.warn('[PRICING HELPER DB NOTICE]', err.message);
  }

  // Safe statutory defaults
  return {
    coursePriceCents: 3800,
    rushPriceCents: 999,
    coursePriceFormatted: '$38.00',
    rushPriceFormatted: '$9.99',
    totalExpressCents: 4799,
    totalExpressFormatted: '$47.99',
    updatedAt: new Date().toISOString(),
  };
}

function invalidatePricingCache() {
  cachedPricing = null;
  cacheTime = 0;
}

module.exports = {
  getPricing,
  invalidatePricingCache,
};
