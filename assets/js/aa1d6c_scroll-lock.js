/*
    ++++++++++ ATTENTION!!! ++++++++++
    Before including this file
    make sure if your had included JQUERY too

    Mobile scroll-lock and everything that breaks because of it.

    Templates using the mobile scroll-lock pattern (see exclusive-*.css) keep
    html/body permanently locked (overflow:hidden) on mobile and move the
    real scroll to .kat-page__side-to-side (or .kat-page__solo-pane, on
    templates with no primary/secondary-pane split) instead — this fixes the
    mobile browser's address/bottom bar collapsing/expanding on scroll (and,
    with html included in the lock, the Android-specific variant of that bug
    where Chrome uses <html> rather than <body> as the document scroller).

    Locking the page's own scroll like that has side effects: anything that
    assumed "the page scrolls" (AOS's reveal-on-scroll engine, Chrome's
    native pull-to-refresh gesture) breaks, because none of them were ever
    watching the real scroller. This file is only the lock detection
    plus the fixes for what it breaks — template.js still owns the rest of
    the page (startTheJourney, music, particles, etc.) and just calls
    isMobileScrollLocked() from here when it needs to know the lock state.
*/

// Only exclusive- and biasa- templates (template/exclusive-*.php,
// template/biasa-*.php, styled by src/template/exclusive-*.css /
// src/template/biasa-*.css) get this treatment — never custom- ones, even
// though some custom- templates reuse an exclusive/biasa design's body
// class for styling (e.g. custom-farah-imran.php ships its own separate
// custom-farah-imran.css but still uses body class "chitra", the same class
// exclusive-chitra.php uses — so body class alone can't tell them apart).
// The one signal that can't collide: each page's own stylesheet <link>,
// which always matches its own PHP file's name.
//
// Checked via the tag's data-asset-key (set by AssetManifest::css() in
// class/webpack.class.php), not its href — the production build content-
// hashes CSS filenames (src/template/exclusive-chinese.css becomes
// something like e312506c.css), so the href carries no trace of the
// original file name once built. data-asset-key preserves it.
function isExclusiveTemplate() {
    var links = document.querySelectorAll('link[rel="stylesheet"][data-asset-key]');
    for (var i = 0; i < links.length; i++) {
        var key = links[i].getAttribute('data-asset-key') || '';
        if (/(^|\/)(exclusive|biasa)-[^\/]+$/.test(key)) return true;
    }
    return false;
}

// The real mobile scroller under the lock — .kat-page__side-to-side on
// templates with the two-pane (primary-pane/secondary-pane) desktop layout,
// .kat-page__solo-pane on templates that never had that split (exclusive-01
// through 08: single-column, no side panel, so there's nothing to name
// "side to side" — everything just scrolls inside one plain wrapper).
var SCROLL_CONTAINER_SELECTOR = '.kat-page__side-to-side, .kat-page__solo-pane';

// Detected via computed style rather than a class/flag, since it's the CSS
// media query — not JS — that decides whether the lock is actually active
// for the current template and viewport width. Gated on isExclusiveTemplate()
// as a hard boundary — see its comment — so this can never fire on a
// custom- page even if one later copies an exclusive template's CSS.
function isMobileScrollLocked() {
    if (!isExclusiveTemplate()) return false;
    var container = document.querySelector(SCROLL_CONTAINER_SELECTOR);
    return !!container && getComputedStyle(container).overflowY === 'auto';
}

// ============================================================
// AOS REVEAL — custom scroll-reveal for [data-aos] elements.
// AOS's own engine (template.js's initAOS) tracks each element's position
// against window scroll — but under the lock, window never scrolls, so AOS
// never reveals anything. Only runs when the lock is active; AOS's own
// engine already works fine everywhere else.
//
// IntersectionObserver instead of a scroll/rAF loop: no per-frame
// getBoundingClientRect() reads (which force a synchronous layout for every
// still-pending element on every scroll frame — expensive on templates with
// hundreds of [data-aos] elements), no scroll or resize listeners at all —
// the browser computes intersection off the main thread and only calls back
// when something actually changes. Reuses AOS's own 'aos-animate' class
// (and thus AOS's CSS animations/timing), just decides when to add it
// independently.
//
// root is deliberately left as the default (null = viewport), not the
// scroll container itself. Viewport-relative intersection is already
// correct regardless of which ancestor actually scrolls (same reason the
// old getBoundingClientRect() version worked without knowing the scroller),
// and a custom root is a known weak spot in the in-app WebViews these pages
// are usually opened from (WhatsApp/Instagram/Facebook) — some poll custom
// roots far less often than the viewport, or don't support them correctly
// at all, which reads as "sometimes doesn't animate" or "animates late".
//
// A MutationObserver still watches for new [data-aos] elements — content
// rendered later via AJAX (RSVP) brings its own — but only to hand each new
// element to the IntersectionObserver once (a Set lookup, not a layout
// read); the observer itself does the actual visibility tracking.
// ============================================================
(function () {
    // Positive, not negative — this must only ever GROW the observable area,
    // never shrink it. A negative bottom margin (shrinking the viewport's
    // bottom edge inward before computing intersection) seems like the
    // obvious way to match AOS's "trigger a bit early" feel, but it creates
    // a dead zone: once the container is scrolled to its absolute max, a
    // short trailing element (shorter than the offset — a footer line, a
    // small badge) can be fully on-screen and still never cross that
    // shrunk boundary, since there's no more scroll room left to push it
    // there. It gets permanently stuck unrevealed. A positive margin only
    // extends how early an element can start intersecting; it can never
    // make something unreachable.
    var REVEAL_OFFSET = 120;

    // AOS's own transition-duration/delay/easing CSS only activates once
    // <body> carries data-aos-duration/data-aos-delay/data-aos-easing
    // (e.g. body[data-aos-duration="400"] [data-aos]{transition-duration:.4s}
    // in aos.css) — and the real AOS.init() is the only thing that sets
    // those, via template.js's initAOS(), itself wrapped in a 1000ms
    // setTimeout inside the ready handler. This fallback reveals elements
    // as soon as they intersect, which for anything visible right when the
    // invitation opens (or already in the initial viewport) happens well
    // before that 1000ms mark — so .aos-animate gets added while the body
    // still has no duration/delay/easing attributes, the CSS transition
    // falls back to the browser default (0s), and the element just snaps
    // to its end state instead of animating (most visible on fade-up, since
    // it also carries a 100px translate that would otherwise slide into
    // place). Setting the same attributes here, immediately, removes the
    // dependency on initAOS()'s timing.
    function ensureAOSBodyDefaults() {
        var body = document.body;
        if (body.hasAttribute('data-aos-duration')) return; // AOS.init() already ran
        var opts = (typeof AOSOptions !== 'undefined' && AOSOptions) || {};
        body.setAttribute('data-aos-easing', opts.easing || 'ease');
        body.setAttribute('data-aos-duration', opts.duration || 400);
        body.setAttribute('data-aos-delay', opts.delay || 0);
    }

    function boot() {
        if (!isMobileScrollLocked()) return;

        ensureAOSBodyDefaults();

        var seen = new WeakSet();

        var globalOnce = (typeof AOSOptions !== 'undefined' && AOSOptions.once === true);

        // ------------------------------------------------------------
        // Clipping fallback. IntersectionObserver's intersection rect is
        // clipped by every ancestor with overflow != visible along the way
        // to root — not just root itself — even a static, non-scrolling
        // overflow:hidden section (usually there to mask a decorative shape
        // bleeding off its edge, not meant to clip real content). A
        // fade-up/fade-down element sits, before it's revealed, at its
        // translateY() offset — if that pushes it outside such a section's
        // clip box, its computed intersection is permanently zero and IO
        // never calls back with isIntersecting:true, so .aos-animate never
        // gets added and it's stuck in its pre-animation state forever.
        //
        // getBoundingClientRect() isn't subject to that ancestor clipping,
        // so it's used here as a backstop — but only polled on a throttled
        // interval, and only while elements remain that IO hasn't managed
        // to reveal yet, never on every scroll frame for every element
        // (that per-frame version is what this replaced, and it's what
        // made scrolling janky on low-end phones).
        // ------------------------------------------------------------
        var pending = new Set(); // observed, not yet revealed — candidates for the rect fallback
        var fallbackTimer = null;
        var FALLBACK_INTERVAL = 250;

        function isOnceFor(el) {
            return el.hasAttribute('data-aos-once') ? (el.getAttribute('data-aos-once') === 'true') : globalOnce;
        }

        function reveal(el) {
            el.classList.add('aos-animate');
            pending.delete(el);
            if (isOnceFor(el)) {
                io.unobserve(el);
            }
        }

        function checkPendingViaRect() {
            if (pending.size === 0) {
                clearInterval(fallbackTimer);
                fallbackTimer = null;
                return;
            }
            var threshold = window.innerHeight + REVEAL_OFFSET;
            pending.forEach(function (el) {
                var rect = el.getBoundingClientRect();
                if (rect.top <= threshold && rect.bottom >= -REVEAL_OFFSET) {
                    reveal(el);
                }
            });
        }

        function startFallbackIfNeeded() {
            if (fallbackTimer || pending.size === 0) return;
            fallbackTimer = setInterval(checkPendingViaRect, FALLBACK_INTERVAL);
        }

        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                var el = entry.target;

                if (entry.isIntersecting) {
                    reveal(el);
                } else if (!isOnceFor(el)) {
                    el.classList.remove('aos-animate');
                }
            });
        }, {
            rootMargin: '0px 0px ' + REVEAL_OFFSET + 'px 0px',
        });

        function observeNew() {
            document.querySelectorAll('[data-aos]:not(.aos-animate)').forEach(function (el) {
                if (seen.has(el)) return;
                seen.add(el);
                pending.add(el);
                io.observe(el);
            });
            startFallbackIfNeeded();
        }

        observeNew();

        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // ELEMENT_NODE
                            if (node.hasAttribute('data-aos') && !node.classList.contains('aos-animate')) {
                                if (!seen.has(node)) {
                                    seen.add(node);
                                    pending.add(node);
                                    io.observe(node);
                                }
                            }
                            var aosElements = node.querySelectorAll('[data-aos]:not(.aos-animate)');
                            aosElements.forEach(function (el) {
                                if (!seen.has(el)) {
                                    seen.add(el);
                                    pending.add(el);
                                    io.observe(el);
                                }
                            });
                        }
                    });
                }
            });
            startFallbackIfNeeded();
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }

    document.addEventListener('DOMContentLoaded', boot);
})();

// ---------- Pull To Refresh (custom, for scroll-locked templates) ------------------------
// Chrome's native swipe-down-to-refresh gesture works by detecting overscroll
// on the document's root scroller — but the mobile scroll-lock sets
// html/body to overflow:hidden precisely so that root never scrolls (that's
// what fixes the Android address-bar collapse bug), so Chrome sees nothing
// to overscroll and drops the gesture entirely. This reimplements it by hand
// on the real scroll container under the lock (see SCROLL_CONTAINER_SELECTOR).
function initPullToRefresh() {
    if (!isMobileScrollLocked()) return; // native gesture still works fine here

    var container = document.querySelector(SCROLL_CONTAINER_SELECTOR);
    var THRESHOLD = 70; // px of pull needed to trigger a refresh
    var MAX_PULL = 100; // px cap on visual travel

    var startY = 0;
    var pull = 0;
    var tracking = false;
    var refreshing = false;

    container.addEventListener('touchstart', function (e) {
        if (refreshing || container.scrollTop > 0) {
            tracking = false;
            return;
        }
        startY = e.touches[0].clientY;
        tracking = true;
    }, { passive: true });

    container.addEventListener('touchmove', function (e) {
        if (!tracking || refreshing) return;

        var diff = e.touches[0].clientY - startY;
        if (diff <= 0 || container.scrollTop > 0) {
            tracking = false;
            pull = 0;
            return;
        }

        pull = Math.min(diff * 0.5, MAX_PULL);
    }, { passive: true });

    container.addEventListener('touchend', function () {
        if (!tracking || refreshing) return;
        tracking = false;

        if (pull >= THRESHOLD) {
            refreshing = true;
            location.reload();
        }
        pull = 0;
    }, { passive: true });
}

$(document).ready(function () {
    initPullToRefresh();
});
