/**
 * Wedding Wishes Backend & Client Handler
 * Rizky Septiawan & Anggun Pratiwi Wedding
 * 
 * Mendukung 3 Mode Otomatis:
 * 1. SUPABASE REST API (Sangat direkomendasikan untuk GitHub Pages & Cloudflare Pages)
 * 2. CLOUDFLARE PAGES D1 / SQLite API (Jika di-deploy di Cloudflare Pages dengan D1)
 * 3. LOCAL STORAGE FALLBACK (Bekerja instan saat preview lokal atau sebelum konfigurasi Supabase)
 */

window.WEDDING_BACKEND_CONFIG = {
    // ------------------------------------------------------------------------
    // PENGATURAN SUPABASE (Gratis di https://supabase.com)
    // ------------------------------------------------------------------------
    // Cukup buat project baru di Supabase, lalu salin URL dan Anon Key ke sini:
    supabaseUrl: "https://tihnmtkjkyxhhkfkatcr.supabase.co",        // Contoh: "https://xyzcompany.supabase.co"
    supabaseAnonKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRpaG5tdGtqa3l4aGhrZmthdGNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQyODUzMjQsImV4cCI6MjEwOTg2MTMyNH0.pKolhPLUHRcvByY1IveoFi-mvqFWEc9q_UCjO7fivZA",    // Contoh: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    tableName: "wedding_wishes",

    // Endpoint Cloudflare Pages Functions (opsional, jika pakai Cloudflare D1)
    cloudflareApiUrl: "/api/wishes"
};

(function () {
    const config = window.WEDDING_BACKEND_CONFIG;
    let activeBackend = 'detecting'; // 'cloudflare' | 'supabase' | 'local'
    let currentPage = 1;
    const PAGE_SIZE = 5;
    let totalLoadedCount = 0;
    let cachedTotalCount = null;

    // Data awal ucapan (seed data jika offline / lokal)
    const SEED_WISHES = [
        {
            id: 'seed-1',
            name: 'Dimas Wicaksono',
            comment: 'Selamat menempuh hidup baru untuk Rizky dan Anggun! Semoga menjadi keluarga yang sakinah, mawaddah, warahmah. Bahagia selalu sampai kakek nenek!',
            created_at: new Date(Date.now() - 1000 * 60 * 35).toISOString() // 35 menit lalu
        },
        {
            id: 'seed-2',
            name: 'Sarah Amalia',
            comment: 'Happy Wedding Anggun cantik & Mas Rizky! MasyaAllah ikut terharu lihat perjalanan cinta kalian dari masa kuliah sampai sekarang. Lancar acaranya yaa!',
            created_at: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString() // 3 jam lalu
        },
        {
            id: 'seed-3',
            name: 'Budi Santoso & Keluarga',
            comment: 'Barakallahu lakum wa baraka alaikum. Selamat buat temanku Rizky & Anggun. Semoga pernikahannya senantiasa dipenuhi berkah dan rahmat Allah SWT.',
            created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString() // 1 hari lalu
        },
        {
            id: 'seed-4',
            name: 'Maya Septiani',
            comment: 'Selamat yaa Anggun & Mas Rizky! Semoga cinta kalian selalu bertambah setiap harinya dan segera dikaruniai momongan yang sholeh/sholehah, aamiin.',
            created_at: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString() // 2 hari lalu
        }
    ];

    // Helper: Escape HTML untuk mencegah XSS
    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Helper: Format tanggal ramah pengguna
    function formatTimeAgo(isoString) {
        try {
            const date = new Date(isoString);
            const now = new Date();
            const diffMs = now - date;
            const diffSec = Math.floor(diffMs / 1000);
            const diffMin = Math.floor(diffSec / 60);
            const diffHour = Math.floor(diffMin / 60);
            const diffDay = Math.floor(diffHour / 24);

            if (diffSec < 60) return 'Baru saja';
            if (diffMin < 60) return `${diffMin} menit yang lalu`;
            if (diffHour < 24) return `${diffHour} jam yang lalu`;
            if (diffDay < 7) return `${diffDay} hari yang lalu`;

            // Tanggal absolut jika lebih dari 7 hari
            const options = { day: 'numeric', month: 'short', year: 'numeric' };
            return date.toLocaleDateString('id-ID', options);
        } catch (e) {
            return 'Baru saja';
        }
    }

    // Local Storage Helpers
    function getLocalWishes() {
        try {
            const stored = localStorage.getItem('wedding_wishes_rizky_anggun');
            if (stored) {
                return JSON.parse(stored);
            }
        } catch (e) {
            console.warn('[Wishes] LocalStorage read error:', e);
        }
        return [...SEED_WISHES];
    }

    function saveLocalWish(wish) {
        try {
            const existing = getLocalWishes();
            existing.unshift(wish);
            localStorage.setItem('wedding_wishes_rizky_anggun', JSON.stringify(existing));
            return existing;
        } catch (e) {
            console.warn('[Wishes] LocalStorage save error:', e);
            return [wish];
        }
    }

    // Tampilkan Toast Alert
    function showWishToast(message, type = 'success') {
        let toast = document.getElementById('wishToast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'wishToast';
            toast.className = 'wish-toast';
            const form = document.getElementById('weddingWishForm');
            if (form && form.parentNode) {
                form.parentNode.insertBefore(toast, form.nextSibling);
            }
        }
        toast.className = `wish-toast ${type}`;
        const icon = type === 'success' ? '<i class="fas fa-check-circle"></i>' : '<i class="fas fa-exclamation-circle"></i>';
        toast.innerHTML = `${icon} <span>${escapeHtml(message)}</span>`;
        toast.style.display = 'flex';

        setTimeout(() => {
            if (toast) toast.style.display = 'none';
        }, 5000);
    }

    // Render satu kartu ucapan
    function createWishCardHtml(wish) {
        return `
            <div class="comment-item" data-wish-id="${escapeHtml(String(wish.id))}">
                <div class="comment-head">
                    <h3 class="comment-name">
                        <i class="fas fa-user-circle"></i>
                        <span>${escapeHtml(wish.name)}</span>
                    </h3>
                    <span class="comment-date">
                        <i class="far fa-clock"></i>
                        <span>${formatTimeAgo(wish.created_at)}</span>
                    </span>
                </div>
                <div class="comment-body">
                    <p class="comment-caption">${escapeHtml(wish.comment)}</p>
                </div>
            </div>
        `;
    }

    // Deteksi Backend yang Tersedia
    async function detectBackend() {
        // 1. Cek Cloudflare Pages D1 API (jika di-deploy di Cloudflare)
        if (window.location.protocol.startsWith('http')) {
            try {
                const cfRes = await fetch(config.cloudflareApiUrl, { method: 'HEAD', cache: 'no-cache' });
                if (cfRes.ok || cfRes.status === 405 || cfRes.status === 200) {
                    console.log('[Wishes] Cloudflare D1 Backend active');
                    activeBackend = 'cloudflare';
                    return 'cloudflare';
                }
            } catch (e) {
                // Cloudflare endpoint not available, fallback to Supabase
            }
        }

        // 2. Cek apakah konfigurasi Supabase terisi
        if (config.supabaseUrl && config.supabaseAnonKey && config.supabaseUrl.startsWith('https://')) {
            console.log('[Wishes] Supabase Backend active');
            activeBackend = 'supabase';
            return 'supabase';
        }

        // 3. Fallback ke LocalStorage (Ideal untuk GitHub Pages awal / dev)
        console.log('[Wishes] LocalStorage fallback active (Siap dihubungkan ke Supabase kapan saja)');
        activeBackend = 'local';
        return 'local';
    }

    // Ambil daftar ucapan dari Backend aktif
    async function fetchWishes(page = 1, limit = PAGE_SIZE) {
        const offset = (page - 1) * limit;

        if (activeBackend === 'detecting') {
            await detectBackend();
        }

        // Mode 1: Cloudflare D1 API
        if (activeBackend === 'cloudflare') {
            try {
                const res = await fetch(`${config.cloudflareApiUrl}?limit=${limit}&offset=${offset}`, { cache: 'no-cache' });
                if (res.ok) {
                    const data = await res.json();
                    const list = Array.isArray(data) ? data : (data.results || []);
                    list.totalCount = data.total || null;
                    return list;
                }
            } catch (e) {
                console.warn('[Wishes] Cloudflare fetch error, falling back:', e);
            }
        }

        // Mode 2: Supabase REST API
        if (activeBackend === 'supabase') {
            try {
                const endpoint = `${config.supabaseUrl}/rest/v1/${config.tableName}?select=*&order=created_at.desc&limit=${limit}&offset=${offset}`;
                const res = await fetch(endpoint, {
                    headers: {
                        'apikey': config.supabaseAnonKey,
                        'Authorization': `Bearer ${config.supabaseAnonKey}`,
                        'Accept': 'application/json',
                        'Prefer': 'count=exact'
                    }
                });
                if (res.ok) {
                    const data = await res.json();
                    const list = Array.isArray(data) ? data : [];
                    
                    // Parse PostgREST content-range header e.g. "0-4/42"
                    const contentRange = res.headers.get('content-range');
                    let serverTotal = null;
                    if (contentRange && contentRange.includes('/')) {
                        const totalStr = contentRange.split('/')[1];
                        if (totalStr && totalStr !== '*') {
                            serverTotal = parseInt(totalStr, 10);
                        }
                    }
                    list.totalCount = serverTotal;
                    return list;
                } else {
                    console.warn('[Wishes] Supabase fetch non-200:', res.status);
                }
            } catch (e) {
                console.warn('[Wishes] Supabase fetch error:', e);
            }
        }

        // Mode 3: LocalStorage
        const local = getLocalWishes();
        const list = local.slice(offset, offset + limit);
        list.totalCount = local.length;
        return list;
    }

    // Kirim ucapan baru ke Backend aktif
    async function submitWish(name, comment) {
        const newWish = {
            name: name.trim(),
            comment: comment.trim(),
            created_at: new Date().toISOString()
        };

        if (activeBackend === 'detecting') {
            await detectBackend();
        }

        // Mode 1: Cloudflare D1
        if (activeBackend === 'cloudflare') {
            try {
                const res = await fetch(config.cloudflareApiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newWish)
                });
                if (res.ok) {
                    const data = await res.json();
                    return data.data || newWish;
                }
            } catch (e) {
                console.warn('[Wishes] Cloudflare post error:', e);
            }
        }

        // Mode 2: Supabase
        if (activeBackend === 'supabase') {
            try {
                const endpoint = `${config.supabaseUrl}/rest/v1/${config.tableName}`;
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'apikey': config.supabaseAnonKey,
                        'Authorization': `Bearer ${config.supabaseAnonKey}`,
                        'Content-Type': 'application/json',
                        'Prefer': 'return=representation'
                    },
                    body: JSON.stringify(newWish)
                });
                if (res.ok) {
                    const created = await res.json();
                    return Array.isArray(created) ? created[0] : newWish;
                } else {
                    console.warn('[Wishes] Supabase post failed with status:', res.status);
                }
            } catch (e) {
                console.warn('[Wishes] Supabase post error:', e);
            }
        }

        // Mode 3: Simpan di LocalStorage
        saveLocalWish(newWish);
        return newWish;
    }

    // Render daftar ucapan ke DOM
    async function loadWishes(append = false) {
        const container = document.querySelector('.comment-wrap');
        const moreWrap = document.querySelector('.more-comment-wrap');
        const moreBtn = document.getElementById('moreComment');

        if (!container) return;

        if (!append) {
            currentPage = 1;
            totalLoadedCount = 0;
            container.innerHTML = '<div style="text-align:center; padding:15px; color:#8a7b6b; font-family:var(--body-text-family);"><i class="fas fa-spinner fa-spin"></i> Memuat ucapan...</div>';
            container.classList.add('show');
        } else {
            if (moreBtn) {
                moreBtn.disabled = true;
                moreBtn.innerHTML = 'Memuat... <i class="fas fa-spinner fa-spin"></i>';
            }
        }

        const wishes = await fetchWishes(currentPage, PAGE_SIZE);

        if (!append) {
            container.innerHTML = '';
        }

        if (wishes && wishes.length > 0) {
            const html = wishes.map(createWishCardHtml).join('');
            if (append) {
                container.insertAdjacentHTML('beforeend', html);
            } else {
                container.innerHTML = html;
            }
            totalLoadedCount += wishes.length;

            if (wishes.totalCount !== undefined && wishes.totalCount !== null) {
                cachedTotalCount = wishes.totalCount;
            }

            const hasMore = (cachedTotalCount !== null)
                ? (totalLoadedCount < cachedTotalCount)
                : (wishes.length >= PAGE_SIZE);

            if (hasMore) {
                if (moreWrap) moreWrap.classList.add('show');
                if (moreBtn) {
                    moreBtn.disabled = false;
                    const remaining = (cachedTotalCount !== null && cachedTotalCount > totalLoadedCount)
                        ? ` (${cachedTotalCount - totalLoadedCount} lagi)`
                        : '';
                    moreBtn.innerHTML = `Lihat ucapan lainnya${remaining} <i class="fas fa-chevron-down" style="font-size:12px; margin-left:4px;"></i>`;
                }
            } else {
                if (moreWrap) moreWrap.classList.remove('show');
            }
        } else {
            if (!append) {
                container.innerHTML = '<div style="text-align:center; padding:24px 16px; color:#8a7b6b; font-family:var(--body-text-family); font-size:18px;"><i class="far fa-heart" style="font-size:24px; display:block; margin-bottom:8px; opacity:0.6;"></i>Belum ada ucapan. Jadilah yang pertama memberikan doa restu untuk Rizky &amp; Anggun!</div>';
            }
            if (moreWrap) moreWrap.classList.remove('show');
        }
    }

    // Inisialisasi Event Handlers
    function init() {
        const form = document.getElementById('weddingWishForm');
        const moreBtn = document.getElementById('moreComment');

        // Form Submit
        if (form) {
            form.addEventListener('submit', async function (e) {
                e.preventDefault();
                e.stopPropagation();

                const nameInput = form.querySelector('input[name="name"]');
                const commentInput = form.querySelector('textarea[name="comment"]');
                const submitBtn = form.querySelector('button[type="submit"]');

                const name = nameInput ? nameInput.value.trim() : '';
                const comment = commentInput ? commentInput.value.trim() : '';

                if (!name) {
                    if (nameInput) nameInput.focus();
                    showWishToast('Silakan masukkan nama Anda.', 'error');
                    return;
                }

                if (!comment) {
                    if (commentInput) commentInput.focus();
                    showWishToast('Silakan tuliskan ucapan atau doa restu Anda.', 'error');
                    return;
                }

                // UI Loading State
                const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                }

                try {
                    const savedWish = await submitWish(name, comment);

                    // Prepend card langsung ke atas container komentar
                    const container = document.querySelector('.comment-wrap');
                    if (container) {
                        const cardHtml = createWishCardHtml(savedWish);
                        container.insertAdjacentHTML('afterbegin', cardHtml);
                        container.classList.add('show');
                        // Scroll halus ke ucapan paling atas
                        container.scrollTo({ top: 0, behavior: 'smooth' });
                    }

                    if (cachedTotalCount !== null) {
                        cachedTotalCount++;
                    }

                    // Reset form
                    if (commentInput) commentInput.value = '';
                    showWishToast('Terima kasih! Ucapan dan doa restu Anda berhasil dikirimkan.', 'success');
                } catch (err) {
                    console.error('[Wishes] Submit error:', err);
                    showWishToast('Maaf, terjadi kendala saat mengirim ucapan. Silakan coba lagi.', 'error');
                } finally {
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalBtnHtml;
                    }
                }
            });
        }

        // More Comment Click
        if (moreBtn) {
            moreBtn.addEventListener('click', function (e) {
                e.preventDefault();
                currentPage++;
                loadWishes(true);
            });
        }

        // Load awal ucapan setelah DOM siap
        setTimeout(() => {
            loadWishes(false);
        }, 800);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

