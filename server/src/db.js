const { Pool } = require('pg');

let pool;

function getPool() {
  if (!pool) {
    const connectionString = process.env.DATABASE_URL;
    const isCloudRun = Boolean(process.env.K_SERVICE);
    
    const config = connectionString 
      ? { connectionString } 
      : {
          user: process.env.DB_USER || 'postgres',
          password: process.env.DB_PASSWORD,
          database: process.env.DB_NAME || 'tx_ade_production',
          host: process.env.DB_HOST || '34.70.206.169',
          port: parseInt(process.env.DB_PORT || '5432', 10),
        };

    // If using Cloud SQL Unix socket
    if (process.env.INSTANCE_CONNECTION_NAME && isCloudRun) {
      config.host = `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`;
    }

    config.max = 5; // Capped at 5 to safely allow Cloud Run to scale to 15+ instances without exhausting Cloud SQL connection limits
    config.idleTimeoutMillis = 30000;
    config.connectionTimeoutMillis = 10000;
    config.keepAlive = true;
    config.keepAliveInitialDelayMillis = 10000;

    pool = new Pool(config);

    pool.on('error', (err) => {
      console.warn('[DB] Handled idle PostgreSQL client error:', err.message);
    });
  }
  return pool;
}

async function query(text, params, attempts = 2) {
  for (let i = 0; i < attempts; i++) {
    try {
      return await getPool().query(text, params);
    } catch (err) {
      const isConnError = err.code === 'ECONNRESET' ||
                          err.code === 'EPIPE' ||
                          err.code === 'ETIMEDOUT' ||
                          (err.message && err.message.includes('Connection terminated'));
      if (isConnError && i < attempts - 1) {
        console.warn(`[DB] Reconnecting after ${err.code || err.message}...`);
        await new Promise(res => setTimeout(res, 250));
        continue;
      }
      throw err;
    }
  }
}

module.exports = {
  query,
  getPool,
};
