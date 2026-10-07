const Redis = require('ioredis');

let client = null;
const memoryStore = new Map();

function getRedis() {
  if (client) return client;

  const redisHost = process.env.REDIS_HOST;
  const redisPort = parseInt(process.env.REDIS_PORT || '6379', 10);

  if (redisHost) {
    try {
      client = new Redis({
        host: redisHost,
        port: redisPort,
        connectTimeout: 5000,
        retryStrategy(times) {
          if (times > 3) {
            console.warn('[REDIS] Connection failed, falling back to in-memory store.');
            return null;
          }
          return Math.min(times * 100, 2000);
        },
      });

      client.on('error', (err) => {
        console.warn('[REDIS] Redis client error:', err.message);
      });

      client.on('connect', () => {
        console.log(`[REDIS] Connected to Redis at ${redisHost}:${redisPort}`);
      });

      return client;
    } catch (e) {
      console.warn('[REDIS] Could not initialize Redis client, using fallback:', e.message);
    }
  }

  // Fallback in-memory implementation for local dev
  return {
    async get(key) {
      const item = memoryStore.get(key);
      if (!item) return null;
      if (item.expires && Date.now() > item.expires) {
        memoryStore.delete(key);
        return null;
      }
      return item.value;
    },
    async set(key, value, mode, ttl) {
      let expires = null;
      if (mode === 'EX' && ttl) {
        expires = Date.now() + ttl * 1000;
      }
      memoryStore.set(key, { value, expires });
      return 'OK';
    },
    async del(key) {
      return memoryStore.delete(key) ? 1 : 0;
    },
    async incr(key) {
      const current = parseInt(await this.get(key) || '0', 10);
      const next = current + 1;
      await this.set(key, String(next));
      return next;
    },
  };
}

module.exports = { getRedis };
