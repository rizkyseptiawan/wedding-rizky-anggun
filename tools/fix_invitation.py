import re
import os
import json

with open("tools/page_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Clean the invalid Cloudflare injection and the fake early </body> at line 160
html = re.sub(r'<body[^>]*>.*?</body>', '<body class="eloise original preset-original" data-template="eloise">', html, count=1, flags=re.DOTALL)
html = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', '', html, flags=re.DOTALL)
html = re.sub(r'<noscript>.*?googletagmanager\.com.*?</noscript>', '', html, flags=re.DOTALL)

# 2. Map CSS
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

# 3. Map JS
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

# 5. Map eloise assets
eloise_files = os.listdir("assets/img/eloise")
for ef in eloise_files:
    html = re.sub(r'https?://[^"\']*/media/template/exclusive/eloise/original/' + re.escape(ef), f'assets/img/eloise/{ef}', html)
    html = html.replace(f'https:\\/\\/annajeremiah.katsudoto.id\\/media\\/template\\/exclusive\\/eloise\\/original\\/{ef}', f'assets/img/eloise/{ef}')
    html = html.replace(f'https://katsudoto.id/media/template/exclusive/eloise/original/{ef}', f'assets/img/eloise/{ef}')
    html = html.replace(f'https:\\/\\/katsudoto.id\\/media\\/template\\/exclusive\\/eloise\\/original\\/{ef}', f'assets/img/eloise/{ef}')

# 6. Map photos
if os.path.exists("tools/photo_map.json"):
    with open("tools/photo_map.json", "r", encoding="utf-8") as f:
        photo_map = json.load(f)
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
html = re.sub(r'https?://[^"\']*frame-cover\.png', 'assets/img/eloise/frame-cover.png', html)
html = re.sub(r'https?://[^"\']*frame-couple\.png', 'assets/img/eloise/frame-couple.png', html)
html = re.sub(r'https?://[^"\']*frame-sd\.png', 'assets/img/eloise/frame-sd.png', html)

# 9. Direct inline onclick="window.openWeddingInvitation()" on all open triggers
html = html.replace('<p class="open-btn"', '<p class="open-btn" onclick="window.openWeddingInvitation()"')
html = html.replace('<div class="open-btn-wrap"', '<div class="open-btn-wrap" onclick="window.openWeddingInvitation()"')
html = html.replace('<div class="open-trigger" id="openInvTrigger">', '<div class="open-trigger" id="openInvTrigger" onclick="window.openWeddingInvitation()">')
html = html.replace('<div class="orn-tc-click">', '<div class="orn-tc-click" onclick="window.openWeddingInvitation()">')
html = html.replace('<div class="orn-tc-5">', '<div class="orn-tc-5" onclick="window.openWeddingInvitation()">')

# 10. CSS polish and preloader optimization
extra_css = """
<style>
/* Background polish */
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
    max-width: 100% !important;
    height: auto !important;
}
/* Rotating vinyl disc */
#music-box.playing, .music-box.playing {
    animation: spinDisc 4s linear infinite !important;
}
@keyframes spinDisc {
    100% { transform: rotate(360deg); }
}
/* Ensure mobile open button is prominently clickable and animated */
.open-btn-wrap, .open-btn, .open-trigger, .orn-tc-5, .tc-ph-trigger, .orn-tc-click {
    cursor: pointer !important;
    pointer-events: auto !important;
}
.open-btn-wrap {
    z-index: 9999999 !important;
    position: absolute !important;
}
.open-btn {
    user-select: none !important;
    -webkit-user-select: none !important;
    display: inline-block !important;
    padding: 8px 20px !important;
    border-radius: 25px !important;
    background: rgba(53, 58, 32, 0.65) !important;
    color: #F5F0E8 !important;
    border: 1px solid rgba(245, 240, 232, 0.6) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    animation: pulseBtn 2s infinite ease-in-out !important;
    transition: transform 0.2s, background 0.2s !important;
}
@keyframes pulseBtn {
    0%, 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(0,0,0,0.35); }
    50% { transform: scale(1.05); box-shadow: 0 6px 20px rgba(53,58,32,0.5); }
}
.open-btn:active {
    transform: scale(0.95) !important;
    background: rgba(53, 58, 32, 0.85) !important;
}
/* Smooth slide-up transition for top-cover */
.top-cover.hide {
    transform: translateY(-120%) !important;
    opacity: 0 !important;
    pointer-events: none !important;
    transition: transform 1.2s cubic-bezier(0.23, 0.56, 0.38, 0.78), opacity 1s !important;
}
</style>
<script>
window.playMusicOnce = function() {};
window.AOSOptions = { duration: 1000, once: false };
</script>
"""

html = html.replace('</head>', extra_css + '\n</head>')

# 11. Client-side static enhancement script
enhancement_script = """
<script>
(function() {
    console.log("[Wedding] Initializing static wedding invitation enhancements...");

    // 1. Audio object
    var audio = new Audio('assets/audio/wedding-song.mp3');
    audio.loop = true;
    window.weddingAudio = audio;
    var isPlaying = false;

    window.toggleWeddingAudio = function() {
        if (isPlaying) {
            audio.pause();
            isPlaying = false;
            document.querySelectorAll('#music-box, .music-box').forEach(function(b) {
                b.classList.remove('playing', 'auto');
            });
        } else {
            audio.play().then(function() {
                isPlaying = true;
                document.querySelectorAll('#music-box, .music-box').forEach(function(b) {
                    b.classList.add('playing');
                });
            }).catch(function(e) {
                console.log('Audio autoplay blocked:', e);
            });
        }
    };

    // 2. MASTER OPEN INVITATION FUNCTION
    var opened = false;
    window.openWeddingInvitation = function() {
        if (opened) return;
        opened = true;
        console.log("[Wedding] Opening wedding invitation!");

        // A. Hide top-cover on mobile
        var topCovers = document.querySelectorAll('.top-cover');
        topCovers.forEach(function(tc) {
            tc.classList.add('hide');
            tc.style.transform = 'translateY(-120%)';
            tc.style.opacity = '0';
            tc.style.pointerEvents = 'none';
            setTimeout(function() {
                tc.style.display = 'none';
            }, 1200);
        });

        // B. Hide cover-opening on desktop
        var openingCover = document.getElementById('cover-opening');
        if (openingCover) {
            openingCover.style.transition = 'opacity 0.8s ease';
            openingCover.style.opacity = '0';
            setTimeout(function() {
                openingCover.style.display = 'none';
            }, 800);
        }

        // C. Unlock scrolling on HTML & BODY & Containers
        document.body.classList.remove('scroll-locked');
        document.documentElement.classList.remove('scroll-locked');
        document.body.style.cssText += '; overflow: visible !important; overflow-y: auto !important; height: auto !important; position: static !important;';
        document.documentElement.style.cssText += '; overflow: visible !important; overflow-y: auto !important; height: auto !important;';
        
        var sideToSide = document.querySelector('.kat-page__side-to-side');
        if (sideToSide) {
            sideToSide.style.cssText += '; overflow-y: auto !important; height: auto !important;';
        }
        var secondaryPane = document.querySelector('.secondary-pane');
        if (secondaryPane) {
            secondaryPane.style.cssText += '; overflow-y: auto !important; height: auto !important;';
        }

        if (window.scrollLock && typeof window.scrollLock.disable === 'function') {
            try { window.scrollLock.disable(); } catch(e) {}
        }

        // D. Play audio
        audio.play().then(function() {
            isPlaying = true;
            document.querySelectorAll('#music-box, .music-box').forEach(function(b) {
                b.classList.add('playing');
            });
        }).catch(function(err) {
            console.log('Audio autoplay gesture waiting:', err);
        });

        // E. Smoothly scroll into main content
        setTimeout(function() {
            var target = document.querySelector('.cover, .quote-wrap');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        }, 100);

        // F. Trigger AOS animations
        setTimeout(function() {
            if (window.AOS) {
                if (typeof window.AOS.refreshHard === 'function') {
                    window.AOS.refreshHard();
                } else if (typeof window.AOS.refresh === 'function') {
                    window.AOS.refresh();
                }
            }
        }, 400);
    };

    // Alias for Katsudoto's internal call
    window.startTheJourney = function() {
        window.openWeddingInvitation();
    };

    // Attach click and touch listeners via native JS and jQuery
    var triggers = '.open-btn, .open-btn-wrap, #openInvTrigger, .open-trigger, .orn-tc-5, .tc-ph-trigger, .orn-tc-click, [data-action="open-invitation"]';
    
    function attachTriggers() {
        document.querySelectorAll(triggers).forEach(function(el) {
            el.addEventListener('click', function(e) {
                e.preventDefault();
                window.openWeddingInvitation();
            });
            el.addEventListener('touchend', function(e) {
                e.preventDefault();
                window.openWeddingInvitation();
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', attachTriggers);
    } else {
        attachTriggers();
    }

    if (window.jQuery) {
        $(document).on('click touchend', triggers, function(e) {
            e.preventDefault();
            window.openWeddingInvitation();
        });
    }

    // Toggle music
    document.addEventListener('click', function(e) {
        if (e.target.closest('#music-box, .music-box')) {
            e.preventDefault();
            window.toggleWeddingAudio();
        }
    });

    // 3. Dynamic guest name (?to=... or ?u=...)
    function applyGuestName() {
        var urlParams = new URLSearchParams(window.location.search);
        var guestName = urlParams.get('to') || urlParams.get('u') || urlParams.get('guest');
        if (guestName) {
            guestName = decodeURIComponent(guestName.replace(/\\+/g, ' ')).trim();
            document.querySelectorAll('.bottom-text, p.bottom-text').forEach(function(el) {
                el.innerHTML = 'Hai&nbsp;' + guestName;
            });
            document.querySelectorAll('input[name="guest_name"], input[name="name"]').forEach(function(el) {
                el.value = guestName;
            });
            function replaceText(node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    if (node.nodeValue.includes('Katsudoto')) {
                        node.nodeValue = node.nodeValue.replace(/Katsudoto/g, guestName);
                    }
                } else if (node.nodeType === Node.ELEMENT_NODE && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                    for (var i = 0; i < node.childNodes.length; i++) {
                        replaceText(node.childNodes[i]);
                    }
                }
            }
            replaceText(document.body);
        }
    }

    // 4. Copy to clipboard
    window.copyTextToClipboard = function(text, label) {
        if (!text) return;
        var done = function() { showToast((label || 'Nomor rekening') + ' berhasil disalin!'); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(done).catch(function() {
                fallbackCopy(text, done);
            });
        } else {
            fallbackCopy(text, done);
        }
    };

    function fallbackCopy(text, cb) {
        var temp = document.createElement('input');
        temp.value = text;
        document.body.appendChild(temp);
        temp.select();
        document.execCommand('copy');
        document.body.removeChild(temp);
        if (cb) cb();
    }

    function showToast(msg) {
        var toast = document.getElementById('wedding-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'wedding-toast';
            toast.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#353A20;color:#fff;padding:12px 24px;border-radius:30px;font-family:sans-serif;font-size:14px;z-index:9999999;box-shadow:0 4px 15px rgba(0,0,0,0.3);transition:opacity 0.3s;opacity:0;pointer-events:none;';
            document.body.appendChild(toast);
        }
        toast.textContent = msg;
        toast.style.opacity = '1';
        setTimeout(function() {
            toast.style.opacity = '0';
        }, 3000);
    }

    document.addEventListener('click', function(e) {
        var copyBtn = e.target.closest('.btn-copy, .btn-salin, [data-copy], .copy-btn, .action-copy');
        if (copyBtn) {
            e.preventDefault();
            var text = copyBtn.getAttribute('data-copy') || copyBtn.getAttribute('data-credential') || copyBtn.textContent.trim();
            window.copyTextToClipboard(text, 'Nomor rekening / Alamat');
        }
    });

    // 5. Offline wishes via localStorage
    var WISHES_STORAGE_KEY = 'wedding_anna_jeremiah_wishes';
    var defaultWishes = [
        { name: 'Sarah & Kevin', attendance: 'Hadir', message: 'Happy wedding Anna & Jeremiah! Wishing you both a lifetime of love and joy!', time: '2 jam yang lalu' },
        { name: 'Bambang Sutrisno', attendance: 'Hadir', message: 'Selamat menempuh hidup baru untuk kedua mempelai. Kiranya selalu diberkati Tuhan.', time: '5 jam yang lalu' },
        { name: 'Jessica Tan', attendance: 'Hadir', message: 'Congratulations Anna & Jeremiah! So happy for both of you!', time: '1 hari yang lalu' }
    ];

    function getStoredWishes() {
        try {
            var raw = localStorage.getItem(WISHES_STORAGE_KEY);
            return raw ? JSON.parse(raw) : defaultWishes;
        } catch(e) {
            return defaultWishes;
        }
    }

    function renderWishes() {
        var wishes = getStoredWishes();
        var container = document.querySelector('.wedding-wish-list, #wishList, .wish-container');
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

    document.addEventListener('submit', function(e) {
        var form = e.target.closest('#rsvpForm, form.rsvp-form, .rsvp-body form');
        if (form) {
            e.preventDefault();
            var nameInput = form.querySelector('input[name="name"], input[name="guest_name"]');
            var name = nameInput ? nameInput.value : 'Tamu Undangan';
            var msgInput = form.querySelector('textarea[name="message"], textarea[name="wish"]');
            var message = msgInput ? msgInput.value : '';

            if (!message.trim()) {
                showToast('Silakan tuliskan ucapan & doa terlebih dahulu.');
                return;
            }

            var attInput = form.querySelector('select[name="attendance"], input[name="attendance"]:checked');
            var attendance = attInput ? (attInput.value || 'Hadir') : 'Hadir';

            var newWish = {
                name: name,
                attendance: attendance,
                message: message,
                time: 'Baru saja'
            };

            var cur = getStoredWishes();
            cur.unshift(newWish);
            try {
                localStorage.setItem(WISHES_STORAGE_KEY, JSON.stringify(cur));
            } catch(err) {}

            renderWishes();
            form.reset();
            showToast('Terima kasih atas konfirmasi kehadiran & ucapannya!');
        }
    });

    // Run on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            applyGuestName();
            renderWishes();
        });
    } else {
        applyGuestName();
        renderWishes();
    }
})();
</script>
"""

# Replace ONLY the last </body> tag
last_body_idx = html.rfind('</body>')
if last_body_idx != -1:
    html = html[:last_body_idx] + enhancement_script + '\n' + html[last_body_idx:]
else:
    html += enhancement_script

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated perfected index.html!")
