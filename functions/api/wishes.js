/**
 * Cloudflare Pages Functions - Wedding Wishes API (SQLite via D1)
 * 
 * Jika Anda mendeploy proyek ini ke Cloudflare Pages dan mengaktifkan Cloudflare D1:
 * 1. Buat D1 Database di Cloudflare Dashboard atau wrangler:
 *    wrangler d1 create wedding-db
 * 2. Bind D1 database dengan variable name: 'DB' di Cloudflare Pages Dashboard
 * 3. Eksekusi tabel:
 *    CREATE TABLE IF NOT EXISTS wedding_wishes (
 *        id INTEGER PRIMARY KEY AUTOINCREMENT,
 *        name TEXT NOT NULL,
 *        comment TEXT NOT NULL,
 *        created_at TEXT NOT NULL
 *    );
 */

export async function onRequestGet(context) {
    const { env, request } = context;
    const url = new URL(request.url);
    const limit = Math.min(parseInt(url.searchParams.get('limit') || '20', 10), 100);
    const offset = parseInt(url.searchParams.get('offset') || '0', 10);

    const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    };

    if (!env || !env.DB) {
        return new Response(JSON.stringify({ error: "Cloudflare D1 binding 'DB' not configured" }), {
            status: 500,
            headers
        });
    }

    try {
        const { results } = await env.DB.prepare(
            "SELECT id, name, comment, created_at FROM wedding_wishes ORDER BY datetime(created_at) DESC LIMIT ? OFFSET ?"
        ).bind(limit, offset).all();

        return new Response(JSON.stringify(results || []), {
            status: 200,
            headers
        });
    } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
            status: 500,
            headers
        });
    }
}

export async function onRequestPost(context) {
    const { env, request } = context;
    const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    };

    if (!env || !env.DB) {
        return new Response(JSON.stringify({ error: "Cloudflare D1 binding 'DB' not configured" }), {
            status: 500,
            headers
        });
    }

    try {
        const body = await request.json();
        const name = (body.name || '').trim();
        const comment = (body.comment || '').trim();

        if (!name || !comment) {
            return new Response(JSON.stringify({ error: "Nama dan ucapan wajib diisi" }), {
                status: 400,
                headers
            });
        }

        const createdAt = new Date().toISOString();
        const result = await env.DB.prepare(
            "INSERT INTO wedding_wishes (name, comment, created_at) VALUES (?, ?, ?)"
        ).bind(name, comment, createdAt).run();

        return new Response(JSON.stringify({
            success: true,
            data: {
                id: result.meta.last_row_id,
                name,
                comment,
                created_at: createdAt
            }
        }), {
            status: 201,
            headers
        });
    } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
            status: 500,
            headers
        });
    }
}

export async function onRequestOptions() {
    return new Response(null, {
        status: 204,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    });
}

