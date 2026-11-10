import re
import os
import json

with open("tools/page_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

# Load photo map if exists
photo_map = {}
if os.path.exists("tools/photo_map.json"):
    with open("tools/photo_map.json", "r", encoding="utf-8") as f:
        photo_map = json.load(f)

# 1. Clean Cloudflare tracking & GTM
html = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', '', html, flags=re.DOTALL)
html = re.sub(r'<noscript>.*?googletagmanager\.com.*?</noscript>', '', html, flags=re.DOTALL)
html = re.sub(r'\(function\(\)\{function c\(\)\{.*?challenge-platform.*?\}\)\(\);', '', html, flags=re.DOTALL)

# 2. Map CSS files
css_files = [f for f in os.listdir("assets/css") if f.endswith(".css")]
for cf in css_files:
    orig_name = cf.split("_", 1)[-1]
    html = re.sub(r'https?://[^"\']*/' + re.escape(orig_name), f'assets/css/{cf}', html)
    html = re.sub(r'/public/dist/' + re.escape(orig_name), f'assets/css/{cf}', html)
    html = re.sub(r'/plugin/[^"\']*/' + re.escape(orig_name), f'assets/css/{cf}', html)

for cf in css_files:
    if "all.min.css" in cf:
        html = re.sub(r'https?://[^"\']*font-awesome[^"\']*all\.min\.css', f'assets/css/{cf}', html)
    if "swiper-bundle.min.css" in cf:
        html = re.sub(r'https?://[^"\']*swiper[^"\']*swiper-bundle\.min\.css', f'assets/css/{cf}', html)

# 3. Map JS files
js_files = [f for f in os.listdir("assets/js") if f.endswith(".js")]
for jf in js_files:
    orig_name = jf.split("_", 1)[-1].split("?")[0]
    html = re.sub(r'https?://[^"\']*/' + re.escape(orig_name) + r'(\?[^"\']*)?', f'assets/js/{jf}', html)
    html = re.sub(r'/public/dist/' + re.escape(orig_name) + r'(\?[^"\']*)?', f'assets/js/{jf}', html)
    html = re.sub(r'/src/js/' + re.escape(orig_name) + r'(\?[^"\']*)?', f'assets/js/{jf}', html)
    html = re.sub(r'/src/template/' + re.escape(orig_name) + r'(\?[^"\']*)?', f'assets/js/{jf}', html)
    html = re.sub(r'/src/' + re.escape(orig_name) + r'(\?[^"\']*)?', f'assets/js/{jf}', html)
    html = re.sub(r'/plugin/[^"\']*/' + re.escape(orig_name) + r'(\?[^"\']*)?', f'assets/js/{jf}', html)

# 4. Map cf-fonts
font_files = os.listdir("assets/fonts")
for ff in font_files:
    if ff.startswith("cf-fonts_"):
        orig_rel = "/" + ff.replace("_", "/")
        html = html.replace(orig_rel, f"assets/fonts/{ff}")

# 5. Map eloise template ornaments and frames
eloise_files = os.listdir("assets/img/eloise")
for ef in eloise_files:
    html = re.sub(r'https?://[^"\']*/media/template/exclusive/eloise/original/' + re.escape(ef), f'assets/img/eloise/{ef}', html)
    html = html.replace(f'https:\\/\\/annajeremiah.katsudoto.id\\/media\\/template\\/exclusive\\/eloise\\/original\\/{ef}', f'assets/img/eloise/{ef}')
    html = html.replace(f'https://katsudoto.id/media/template/exclusive/eloise/original/{ef}', f'assets/img/eloise/{ef}')
    html = html.replace(f'https:\\/\\/katsudoto.id\\/media\\/template\\/exclusive\\/eloise\\/original\\/{ef}', f'assets/img/eloise/{ef}')

# 6. Map photos
for orig_url, local_path in photo_map.items():
    html = html.replace(orig_url, local_path)
    html = html.replace(orig_url.replace("/", "\\/"), local_path)

# 7. Map audio
html = re.sub(r'https?://[^"\']*\.mp3[^"\']*', 'assets/audio/wedding-song.mp3', html)
html = re.sub(r'https?:\\\/\\\/[^"\']*\.mp3[^"\']*', 'assets/audio/wedding-song.mp3', html)

# 8. Map custom logo & icons
html = re.sub(r'https?://[^"\']*thumb-md-969211-400-400[^"\']*', 'assets/img/photos/photo_26.jpg', html)
html = re.sub(r'https?:\\\/\\\/[^"\']*thumb-md-969211-400-400[^"\']*', 'assets/img/photos/photo_26.jpg', html)
html = re.sub(r'https?://[^"\']*cloud-upload\.png', 'assets/img/img_e871216e.png', html)
html = re.sub(r'https?://[^"\']*ic-dress-man-garden\.png', 'assets/img/img_d2939cb1.png', html)
html = re.sub(r'https?://[^"\']*ic-dress-woman-garden-party\.png', 'assets/img/img_0474352a.png', html)

# Additional CSS polish for static background, mobile responsiveness, and clickability
extra_css = """
<style>
/* Static Clone Polish */
.bg-pp:before {
    background-image: url("assets/img/eloise/bg-pp.png") !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-size: cover !important;
    opacity: 0.9 !important;
}
.bg-pp {
    opacity: 1 !important;
}
img[alt="Cover Frame"] {
    display: none !important;
}
/* Ensure music box spins when playing */
#music-box.playing, .music-box.playing {
    animation: spinDisc 4s linear infinite !important;
}
@keyframes spinDisc {
    100% { transform: rotate(360deg); }
}
/* Ensure mobile open button is clearly clickable and above ornaments */
.open-btn-wrap, .open-btn, .open-trigger, .orn-tc-5, .tc-ph-trigger, .orn-tc-click {
    cursor: pointer !important;
    pointer-events: auto !important;
}
.open-btn-wrap {
    z-index: 9999 !important;
}
.open-btn {
    user-select: none;
    -webkit-user-select: none;
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(53, 58, 32, 0.15);
    backdrop-filter: blur(4px);
    transition: transform 0.2s, background 0.2s;
}
.open-btn:active {
    transform: scale(0.95);
    background: rgba(53, 58, 32, 0.3);
}
/* Wishes container styling */
.static-wishes-board {
    margin-top: 24px;
    max-height: 400px;
    overflow-y: auto;
    padding: 10px;
}
</style>
"""

html = html.replace('</head>', extra_css + '\n</head>')

# Client-side static enhancement script
enhancement_script = """
<script>
(function() {
    // 1. DYNAMIC GUEST NAME REPLACEMENT (?to=Nama+Tamu or ?u=Nama+Tamu or ?guest=...)
    function applyGuestName() {
        const urlParams = new URLSearchParams(window.location.search);
        let guestName = urlParams.get('to') || urlParams.get('u') || urlParams.get('guest');
        if (guestName) {
            guestName = decodeURIComponent(guestName.replace(/\\+/g, ' ')).trim();
            // Update greetings
            document.querySelectorAll('.bottom-text, p.bottom-text').forEach(function(el) {
                el.innerHTML = 'Hai&nbsp;' + guestName;
            });
            // Update any inputs
            document.querySelectorAll('input[name="guest_name"], input[name="name"]').forEach(function(el) {
                el.value = guestName;
            });
            // Replace text nodes containing Katsudoto
            function replaceText(node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    if (node.nodeValue.includes('Katsudoto')) {
                        node.nodeValue = node.nodeValue.replace(/Katsudoto/g, guestName);
                    }
                } else if (node.nodeType === Node.ELEMENT_NODE && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                    for (let child of node.childNodes) {
                        replaceText(child);
                    }
                }
            }
            replaceText(document.body);
        }
    }

    // 2. AUDIO PLAYER & COVER OPENING
    window.weddingAudio = new Audio('assets/audio/wedding-song.mp3');
    window.weddingAudio.loop = true;
    let isPlaying = false;

    window.toggleWeddingAudio = function() {
        if (isPlaying) {
            window.weddingAudio.pause();
            isPlaying = false;
            document.querySelectorAll('#music-box, .music-box').forEach(b => b.classList.remove('playing', 'auto'));
        } else {
            window.weddingAudio.play().then(() => {
                isPlaying = true;
                document.querySelectorAll('#music-box, .music-box').forEach(b => b.classList.add('playing'));
            }).catch(e => console.log('Audio autoplay prevented:', e));
        }
    };

    window.startTheJourney = function() {
        // A. Slide up mobile top-cover
        $(".top-cover").addClass("hide");
        setTimeout(function() {
            $(".top-cover").fadeOut(600, function() {
                $(this).remove();
            });
        }, 1200);

        // B. Fade out desktop opening cover
        $('#cover-opening').fadeOut(700, function() {
            $(this).remove();
        });

        // C. Unlock page scroll on body, html, and container elements
        $('body').removeClass('scroll-locked').css({
            'overflow': 'visible',
            'overflow-y': 'auto',
            'height': 'auto',
            'position': 'static'
        });
        $('html').css({
            'overflow': 'visible',
            'overflow-y': 'auto',
            'height': 'auto'
        });
        $('.kat-page__side-to-side, .secondary-pane').css({
            'overflow-y': 'auto',
            'height': 'auto'
        });

        if (typeof scrollLock !== 'undefined' && scrollLock.disable) {
            scrollLock.disable();
        }

        // D. Play audio
        window.weddingAudio.play().then(function() {
            isPlaying = true;
            $('#music-box, .music-box').addClass('playing');
        }).catch(function(err) {
            console.log('Audio playback waiting for gesture:', err);
        });

        // E. Refresh AOS animations
        setTimeout(function() {
            if (typeof AOS !== 'undefined') {
                if (typeof AOS.refreshHard === 'function') {
                    AOS.refreshHard();
                } else {
                    AOS.refresh();
                }
            }
        }, 300);
    };

    // Open invitation trigger handlers (supporting both desktop wax seal and mobile 'Click to open invitation')
    $(document).on('click touchend', '.open-btn, .open-btn-wrap, #openInvTrigger, .open-trigger, .orn-tc-5, .tc-ph-trigger, .orn-tc-click, [data-action="open-invitation"]', function(e) {
        e.preventDefault();
        e.stopPropagation();
        window.startTheJourney();
    });

    // Toggle music
    $(document).on('click', '#music-box, .music-box', function(e) {
        e.preventDefault();
        window.toggleWeddingAudio();
    });

    // 3. COPY TO CLIPBOARD HELPER WITH TOAST
    window.copyTextToClipboard = function(text, label) {
        if (!text) return;
        navigator.clipboard.writeText(text).then(function() {
            showToast((label || 'Nomor rekening') + ' berhasil disalin!');
        }).catch(function() {
            const temp = document.createElement('input');
            temp.value = text;
            document.body.appendChild(temp);
            temp.select();
            document.execCommand('copy');
            document.body.removeChild(temp);
            showToast((label || 'Nomor rekening') + ' berhasil disalin!');
        });
    };

    function showToast(msg) {
        let toast = document.getElementById('wedding-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'wedding-toast';
            toast.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#353A20;color:#fff;padding:12px 24px;border-radius:30px;font-family:sans-serif;font-size:14px;z-index:99999;box-shadow:0 4px 15px rgba(0,0,0,0.25);transition:opacity 0.3s;opacity:0;pointer-events:none;';
            document.body.appendChild(toast);
        }
        toast.textContent = msg;
        toast.style.opacity = '1';
        setTimeout(function() {
            toast.style.opacity = '0';
        }, 3000);
    }

    // Bind copy triggers
    $(document).on('click', '.btn-copy, .btn-salin, [data-copy], .copy-btn', function(e) {
        e.preventDefault();
        const text = $(this).data('copy') || $(this).attr('data-credential') || $(this).siblings('.credential, .rekening-number').text().trim() || $(this).text().trim();
        window.copyTextToClipboard(text, 'Nomor rekening / Alamat');
    });

    // 4. OFFLINE / LOCAL WISHES & RSVP
    const WISHES_STORAGE_KEY = 'wedding_anna_jeremiah_wishes';
    const defaultWishes = [
        { name: 'Sarah & Kevin', attendance: 'Hadir', message: 'Happy wedding Anna & Jeremiah! Wishing you both a lifetime of love and joy!', time: '2 jam yang lalu' },
        { name: 'Bambang Sutrisno', attendance: 'Hadir', message: 'Selamat menempuh hidup baru untuk kedua mempelai. Kiranya selalu diberkati Tuhan.', time: '5 jam yang lalu' },
        { name: 'Jessica Tan', attendance: 'Hadir', message: 'Congratulations Anna & Jeremiah! So happy for both of you!', time: '1 hari yang lalu' }
    ];

    function getStoredWishes() {
        try {
            const raw = localStorage.getItem(WISHES_STORAGE_KEY);
            return raw ? JSON.parse(raw) : defaultWishes;
        } catch(e) {
            return defaultWishes;
        }
    }

    function renderWishes() {
        const wishes = getStoredWishes();
        const container = document.querySelector('.wedding-wish-list, #wishList, .wish-container');
        if (!container) return;
        container.innerHTML = wishes.map(function(w) {
            return '<div class="wish-item" style="background:rgba(255,255,255,0.9);padding:16px;margin-bottom:12px;border-radius:12px;border-left:4px solid #353A20;box-shadow:0 2px 10px rgba(0,0,0,0.06);text-align:left;">' +
                '<div style="font-weight:600;color:#353A20;display:flex;justify-content:space-between;align-items:center;">' +
                    '<span>' + w.name + '</span>' +
                    '<span style="font-size:11px;background:#e2e8d8;color:#353A20;padding:3px 10px;border-radius:12px;font-weight:500;">' + w.attendance + '</span>' +
                '</div>' +
                '<div style="font-size:13px;color:#444;margin-top:8px;line-height:1.6;">' + w.message + '</div>' +
                '<div style="font-size:10px;color:#888;margin-top:6px;text-align:right;">' + w.time + '</div>' +
            '</div>';
        }).join('');
    }

    $(document).on('submit', '#rsvpForm, form.rsvp-form, .rsvp-body form', function(e) {
        e.preventDefault();
        const form = $(this);
        const name = form.find('input[name="name"], input[name="guest_name"]').val() || 'Tamu Undangan';
        const attendance = form.find('select[name="attendance"], input[name="attendance"]:checked').val() || 'Hadir';
        const message = form.find('textarea[name="message"], textarea[name="wish"]').val() || '';

        if (!message.trim()) {
            showToast('Silakan tuliskan ucapan & doa terlebih dahulu.');
            return;
        }

        const newWish = {
            name: name,
            attendance: attendance,
            message: message,
            time: 'Baru saja'
        };

        const currentWishes = getStoredWishes();
        currentWishes.unshift(newWish);
        try {
            localStorage.setItem(WISHES_STORAGE_KEY, JSON.stringify(currentWishes));
        } catch(e) {}

        renderWishes();
        form[0].reset();
        showToast('Terima kasih atas konfirmasi kehadiran & ucapannya!');
    });

    $(document).ready(function() {
        applyGuestName();
        renderWishes();
    });
})();
</script>
"""

html = html.replace('</body>', enhancement_script + '\n</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Regenerated index.html with complete mobile open invitation support!")
