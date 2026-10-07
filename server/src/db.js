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

    config.max = 20;
    config.idleTimeoutMillis = 30000;
    config.connectionTimeoutMillis = 10000;

    pool = new Pool(config);

    pool.on('error', (err) => {
      console.error('[DB] Unexpected error on idle PostgreSQL client:', err);
    });
  }
  return pool;
}

module.exports = {
  query: (text, params) => getPool().query(text, params),
  getPool,
};
