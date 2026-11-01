const { Pool } = require('pg');

const pool = new Pool({
  connectionString: 'postgresql://postgres:3sN2TqCzSosnuptWexZ3si4M0TiK0f8M@34.70.206.169:5432/tx_ade_production?sslmode=disable'
});

async function queryUsers() {
  try {
    const res = await pool.query('SELECT id, email, full_name, enrollment_status, created_at FROM users ORDER BY created_at DESC LIMIT 50;');
    console.log(JSON.stringify(res.rows, null, 2));
  } catch (err) {
    console.error('Error querying users:', err.message);
  } finally {
    await pool.end();
  }
}

queryUsers();
