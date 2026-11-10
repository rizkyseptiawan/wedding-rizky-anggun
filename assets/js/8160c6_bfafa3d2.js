function adjustContainerHeight(){document.querySelectorAll(".sticky-bg-container").forEach(e=>{const t=e.querySelector(".scroll-content");if(t){const n=1.02*t.offsetHeight;e.style.height=`${n}px`}})}function initHeightObserver(){document.querySelectorAll(".sticky-bg-container.observe").forEach(e=>{const t=e.querySelector(".scroll-content");if(!t)return;new MutationObserver(adjustContainerHeight).observe(t,{childList:!0,subtree:!0,characterData:!0,attributes:!0})})}"scrollRestoration"in history&&(history.scrollRestoration="manual"),window.addEventListener("beforeunload",function(){window.scrollTo(0,0)});var syncPairs=[],heightSyncQueued=!1,scrollTriggerRefreshTimer=null;function containerHeightIsStale(){for(var e=0;e<syncPairs.length;e++){var t=1.02*syncPairs[e].content.offsetHeight,n=parseFloat(syncPairs[e].container.style.height)||0;if(Math.abs(t-n)>1)return!0}return!1}function queueScrollTriggerRefresh(){"undefined"!=typeof ScrollTrigger&&(clearTimeout(scrollTriggerRefreshTimer),scrollTriggerRefreshTimer=setTimeout(function(){ScrollTrigger.refresh()},200))}function queueContainerHeightSync(){heightSyncQueued||(heightSyncQueued=!0,requestAnimationFrame(function(){heightSyncQueued=!1,containerHeightIsStale()&&(adjustContainerHeight(),queueScrollTriggerRefresh())}))}function initContentResizeSync(){document.querySelectorAll(".sticky-bg-container").forEach(function(e){var t=e.querySelector(".scroll-content");t&&(syncPairs.push({container:e,content:t}),"undefined"!=typeof ResizeObserver?new ResizeObserver(queueContainerHeightSync).observe(t):t.querySelectorAll("img").forEach(function(e){e.complete||(e.addEventListener("load",queueContainerHeightSync),e.addEventListener("error",queueContainerHeightSync))}))}),document.fonts&&document.fonts.ready&&document.fonts.ready.then(queueContainerHeightSync)}$(".wedding-gift__next").on("click",()=>{$(".wedding-gift-details").css("opacity",0),$(".wedding-gift-picture").css("opacity",1)}),$(".wedding-gift__prev").on("click",()=>{$(".wedding-gift-details").css("opacity",1),$(".wedding-gift-picture").css("opacity",0)}),$(".bank-btn-top").on("click",function(){const e=$(".bank-btn-top").index(this),t=$(".bank-item").eq(e),n=$(this).find(".ph-fill"),r=$(this);t.slideToggle(500),n.toggleClass("rotate"),r.toggleClass("active")}),$(".bank-item").each(function(e){const t=$(".bank-btn-top").eq(e).find(".ph-fill"),n=$(".bank-btn-top").eq(e),r=$(this).is(":visible");t.toggleClass("rotate",r),n.toggleClass("active",r)});var kadoSwiper=null,init_gifts_slick=function(){var e=$(".hadiah-wrap"),t=document.querySelector(".hi-swiper"),n=document.querySelector(".hib-swiper");if(e.length&&t&&n){var r=new Swiper(n,{effect:"fade",direction:"horizontal",fadeEffect:{crossFade:!0},allowTouchMove:!1});kadoSwiper=new Swiper(t,{effect:"cards",direction:"horizontal",cardsEffect:{slideShadows:!1},rewind:!0,autoplay:{delay:3e3,disableOnInteraction:!1},controller:{control:r}}),$(".kado-chv.left").on("click",function(){kadoSwiper.slidePrev()}),$(".kado-chv.right").on("click",function(){kadoSwiper.slideNext()})}},toggleGift=function(){$(".gift-form-sender-wrapper").slideToggle()};function updatePreviewKadoCSS(){const e=document.querySelector(".secondary-pane");if(!e)return;const t=e.offsetWidth,n=Math.min(t/390,1),r=document.querySelector(".hadiah-wrap");if(!r)return;const o=r.offsetWidth||198,i=(o*n).toFixed(2),a=(o*n).toFixed(2),c=((o*n).toFixed(2),(o*n).toFixed(2),document.getElementById("dynamic-preview-style"));c&&c.remove();const s=document.createElement("style");s.id="dynamic-preview-style",s.innerHTML=`\n        .wedding-gifts-body .hadiah-wrap .hadiah-card-wrap{\n            width: ${i}px !important;\n            height: ${a}px !important;\n        }\n    `,document.head.appendChild(s)}function initLoveStoryAnimation(){
    var e=document.querySelector("section.love-story");
    if(!e)return;
    var t=e.querySelectorAll(".story-item-wrapper");
    if(t.length<2)return;

    var n=[],r=[];
    t.forEach(function(item){
        var sub=item.querySelector(".story-sub-title"),
            cap=item.querySelector(".story-caption"),
            prev=item.querySelector(".story__slider-preview");
        n.push({
            subtitle:sub?sub.textContent.trim():"",
            caption:cap?cap.innerHTML:""
        });
        prev&&r.push(prev);
    });

    var o=t[0],
        i=o.querySelector(".story-sub-title"),
        a=o.querySelector(".story-caption"),
        c=r[0],
        s=c.offsetTop,
        l=c.offsetLeft,
        u=c.offsetWidth;

    for(var d=1;d<r.length;d++){
        o.appendChild(r[d]);
        r[d].style.position="absolute";
        r[d].style.top=s+"px";
        r[d].style.left=l+"px";
        r[d].style.width=u+"px";
        r[d].style.margin="0";
        r[d].style.willChange="transform";
    }

    for(var f=1;f<t.length;f++){
        t[f].style.display="none";
    }

    e.classList.add("ls-animated");
    r.forEach(function(el,idx){
        el.style.zIndex=idx+1;
    });

    var g=getRotationDeg(r[0])||15;
    r.slice(1).forEach(function(el){
        el.style.transition="none";
        el.style.transform="translate(-50%, 80vh) rotate(-30deg)";
    });

    var h=e.offsetHeight,
        p=document.createElement("div");
    p.className="ls-runway";
    e.parentNode.insertBefore(p,e);
    p.appendChild(e);
    e.classList.add("ls-sticky");

    var y=r.length-1;
    var m=0;

    function isMobile(){
        return window.matchMedia("(max-width: 960px)").matches;
    }

    function updatePreviewPositions(){
        if(!c)return;
        s=c.offsetTop;
        l=c.offsetLeft;
        u=c.offsetWidth;
        for(var d=1;d<r.length;d++){
            r[d].style.top=s+"px";
            r[d].style.left=l+"px";
            r[d].style.width=u+"px";
        }
    }

    function b(){
        h=e.offsetHeight;
        if(isMobile()){
            p.style.height="auto";
        }else{
            p.style.height=h+400*y+"px";
        }
        updatePreviewPositions();
    }

    function T(idx){
        if(idx<1||idx>=r.length)return;
        var el=r[idx],
            rot=idx%2!==0?-6:g;
        el.style.transition="transform 600ms cubic-bezier(0.25, 0.46, 0.45, 0.94), opacity 600ms ease";
        el.style.transform="translate3d(0, 0, 0) rotate("+rot+"deg)";
        el.style.opacity="1";
    }

    function x(idx){
        if(idx<1||idx>=r.length)return;
        var el=r[idx];
        el.style.transition="transform 600ms cubic-bezier(0.25, 0.46, 0.45, 0.94), opacity 600ms ease";
        el.style.transform="translate(-50%, 80vh) rotate(-30deg)";
        el.style.opacity="0";
    }

    function setStoryIndex(idx){
        idx=Math.max(0,Math.min(y,idx));
        if(idx===m)return;
        if(idx>m){
            for(var tIdx=m+1;tIdx<=idx;tIdx++)T(tIdx);
        }else{
            for(var tIdx=m;tIdx>idx;tIdx--)x(tIdx);
        }
        m=idx;
        if(i&&n[idx])i.textContent=n[idx].subtitle;
        if(a&&n[idx])a.innerHTML=n[idx].caption;
        updateMobileIndicators(idx);
    }

    var v=0,w=0,S=null;
    function E(){
        var rect=p.getBoundingClientRect(),
            delta=rect.height-h,
            pct=delta>0?-rect.top/delta:0;
        return Math.max(0,Math.min(1,pct));
    }

    function C(){
        if(isMobile())return;
        v=E();
        w+=0.12*(v-w);
        if(Math.abs(v-w)<0.0008)w=v;
        var targetIdx=Math.max(0,Math.min(y,Math.round(w*y)));
        if(targetIdx!==m){
            setStoryIndex(targetIdx);
        }
        S=w!==v?requestAnimationFrame(C):null;
    }

    function k(){
        if(isMobile())return;
        if(null===S)S=requestAnimationFrame(C);
    }

    b();
    new IntersectionObserver(function(entries){
        if(entries[0].isIntersecting&&!isMobile())k();
    },{rootMargin:"200px 0px 200px 0px"}).observe(p);

    window.addEventListener("scroll",k,{passive:true});
    var q=document.querySelector(".kat-page__side-to-side");
    if(q)q.addEventListener("scroll",k,{passive:true});

    window.addEventListener("resize",function(){
        b();
        if(isMobile()){
            p.style.height="auto";
            setStoryIndex(m);
        }else{
            k();
        }
    });

    var mobileControlsWrap=document.createElement("div");
    mobileControlsWrap.className="ls-mobile-controls-wrap";

    var navContainer=document.createElement("div");
    navContainer.className="ls-mobile-nav";
    navContainer.setAttribute("aria-label","Navigasi cerita cinta");

    var prevBtn=document.createElement("button");
    prevBtn.type="button";
    prevBtn.className="ls-nav-btn ls-prev disabled";
    prevBtn.disabled=true;
    prevBtn.innerHTML="&#8249;";
    prevBtn.setAttribute("aria-label","Cerita sebelumnya");

    var nextBtn=document.createElement("button");
    nextBtn.type="button";
    nextBtn.className="ls-nav-btn ls-next";
    nextBtn.innerHTML="&#8250;";
    nextBtn.setAttribute("aria-label","Cerita selanjutnya");

    var dotsWrap=document.createElement("div");
    dotsWrap.className="ls-mobile-dots";

    var dots=[];
    n.forEach(function(item,idx){
        var dot=document.createElement("button");
        dot.type="button";
        dot.className="ls-dot"+(idx===0?" active":"");
        var yearMatch=item.subtitle.match(/\b(20\d\d)\b/);
        var label=yearMatch?yearMatch[1]:(idx+1);
        dot.innerHTML="<span>"+label+"</span>";
        dot.setAttribute("aria-label","Menuju tahun "+label);
        dot.addEventListener("click",function(ev){
            ev.preventDefault();
            ev.stopPropagation();
            setStoryIndex(idx);
        });
        dotsWrap.appendChild(dot);
        dots.push(dot);
    });

    prevBtn.addEventListener("click",function(ev){
        ev.preventDefault();
        ev.stopPropagation();
        if(m>0)setStoryIndex(m-1);
    });

    nextBtn.addEventListener("click",function(ev){
        ev.preventDefault();
        ev.stopPropagation();
        if(m<y)setStoryIndex(m+1);
    });

    navContainer.appendChild(prevBtn);
    navContainer.appendChild(dotsWrap);
    navContainer.appendChild(nextBtn);

    var hintText=document.createElement("div");
    hintText.className="ls-swipe-hint";
    hintText.innerHTML="<span>&#8592; Geser untuk cerita lainnya &#8594;</span>";

    mobileControlsWrap.appendChild(navContainer);
    mobileControlsWrap.appendChild(hintText);
    o.appendChild(mobileControlsWrap);

    function updateMobileIndicators(idx){
        dots.forEach(function(d,i){
            d.classList.toggle("active",i===idx);
        });
        prevBtn.disabled=idx===0;
        nextBtn.disabled=idx===y;
        prevBtn.classList.toggle("disabled",idx===0);
        nextBtn.classList.toggle("disabled",idx===y);
    }
    updateMobileIndicators(0);

    var touchStartX=0,touchStartY=0,touchEndX=0,touchEndY=0,isTouching=false;
    e.addEventListener("touchstart",function(ev){
        if(!isMobile())return;
        var t=ev.touches[0];
        touchStartX=t.clientX;
        touchStartY=t.clientY;
        touchEndX=touchStartX;
        touchEndY=touchStartY;
        isTouching=true;
    },{passive:true});

    e.addEventListener("touchmove",function(ev){
        if(!isTouching||!isMobile())return;
        var t=ev.touches[0];
        touchEndX=t.clientX;
        touchEndY=t.clientY;
    },{passive:true});

    e.addEventListener("touchend",function(ev){
        if(!isTouching||!isMobile())return;
        isTouching=false;
        var dx=touchEndX-touchStartX;
        var dy=touchEndY-touchStartY;
        if(Math.abs(dx)>=35&&Math.abs(dx)>Math.abs(dy)){
            if(dx<0){
                if(m<y)setStoryIndex(m+1);
            }else{
                if(m>0)setStoryIndex(m-1);
            }
        }
    },{passive:true});

    var mouseStartX=0,isMouseDown=false;
    e.addEventListener("mousedown",function(ev){
        if(!isMobile())return;
        mouseStartX=ev.clientX;
        isMouseDown=true;
    });
    e.addEventListener("mouseup",function(ev){
        if(!isMouseDown||!isMobile())return;
        isMouseDown=false;
        var dx=ev.clientX-mouseStartX;
        if(Math.abs(dx)>=40){
            if(dx<0&&m<y)setStoryIndex(m+1);
            else if(dx>0&&m>0)setStoryIndex(m-1);
        }
    });
}
function getRotationDeg(e){
    var t=window.getComputedStyle(e).transform;
    if(!t||"none"===t)return 0;
    var n=t.match(/^matrix\(([^)]+)\)$/);
    if(!n)return 0;
    var r=n[1].split(",").map(parseFloat);
    return Math.round(Math.atan2(r[1],r[0])*(180/Math.PI));
}
function initGalleryParallax(){var e=document.querySelector(".photo-box");if(e)if(window.matchMedia("(hover: none) and (pointer: coarse)").matches){var t=Array.from(e.querySelectorAll("a img"));if(!t.length)return;var n=new IntersectionObserver(function(e){e.forEach(function(e){var n=e.target,r=n===t[0]?"0":"-8%";e.isIntersecting&&e.intersectionRatio>=.2?(n.style.transition="transform 1000ms cubic-bezier(0.25, 0.46, 0.45, 0.94)",n.style.transform="translate3d(0, "+r+", 0)"):e.isIntersecting||(n.style.transition="none",n.style.transform="translate3d(0, 8%, 0)")})},{threshold:[0,.2]});t.forEach(function(e){e.style.transform="translate3d(0, 8%, 0)",e.style.willChange="transform",n.observe(e)})}else{var r=[{from:15,to:-15}],o=Array.from(e.querySelectorAll("a")).map(function(e,t){var n,o,i=e.querySelector("img");if(!i)return null;if(0===t)n=8,o=0;else{var a=r[t%r.length];n=a.from,o=a.to}return i.style.willChange="transform",{el:e,img:i,from:n,to:o,currentY:n,targetY:n,inView:!1}}).filter(Boolean);if(0!==o.length){var i=window.innerHeight,a=null,c=!1,s=new IntersectionObserver(function(e){e.forEach(function(e){var t=o.find(function(t){return t.el===e.target});t&&(t.inView=e.isIntersecting)}),(c=o.some(function(e){return e.inView}))&&d()},{rootMargin:"200px 0px 200px 0px"});o.forEach(function(e){s.observe(e.el)}),window.addEventListener("scroll",function(){c&&d()},{passive:!0});var l=document.querySelector(".kat-page__side-to-side");l&&l.addEventListener("scroll",function(){c&&d()},{passive:!0}),window.addEventListener("resize",function(){i=window.innerHeight,c&&d()}),d()}}function u(){var e=!1;o.forEach(function(e){if(e.inView){var t=function(e){var t=e.getBoundingClientRect(),n=i+t.height,r=(i-t.top)/n;return Math.max(0,Math.min(1,r))}(e.el);e.targetY=e.from+(e.to-e.from)*t}}),o.forEach(function(t){var n=t.targetY-t.currentY;Math.abs(n)>.05?(t.currentY+=.12*n,e=!0,t.img.style.transform="translate3d(0, "+t.currentY+"%, 0)"):t.currentY!==t.targetY&&(t.currentY=t.targetY,t.img.style.transform="translate3d(0, "+t.currentY+"%, 0)")}),a=e?requestAnimationFrame(u):null}function d(){null===a&&(a=requestAnimationFrame(u))}}function initTopCoverInteractionForPane(e){var t=e.querySelector(".tc-frame .orn-tc-photo:not(.tc-ph-trigger)"),n=e.querySelector(".tc-ph-trigger"),r=e.querySelector(".orn-tc-click"),o=e.querySelector(".orn-tc-2"),i=e.querySelector(".tc-frame");if(t&&n&&r&&o&&i){var a=!1;gsap.to([t,n],{y:"-=12",duration:1,ease:"sine.inOut",repeat:-1,yoyo:!0}),n.addEventListener("click",function(){if(gsap.killTweensOf([t,n]),a=!a,i.classList.toggle("active",a),a){var e=.2*o.offsetHeight;gsap.to([t,n],{rotation:0,x:0,y:-2,width:"92.81%",left:"50%",xPercent:-50,duration:.65,ease:"power2.out",overwrite:!0}),gsap.to(r,{autoAlpha:0,duration:.3}),gsap.to(o,{y:e,duration:.65,ease:"power2.out"})}else gsap.to([t,n],{rotation:-9.33,x:"9%",y:"-30%",width:"44.44%",left:"0%",xPercent:0,duration:.65,ease:"power2.out",overwrite:!0}),gsap.to(r,{autoAlpha:1,duration:.3,delay:.35}),gsap.to(o,{y:0,duration:.65,ease:"power2.out"})})}}function initTopCoverInteraction(){var e=document.querySelector(".secondary-pane");e&&initTopCoverInteractionForPane(e);var t=document.querySelector(".primary-pane");t&&initTopCoverInteractionForPane(t)}function initOpenInvAnimation(){var e=document.querySelector(".secondary-pane"),t=document.getElementById("openInvTrigger"),n=e&&e.querySelector(".tc-frame .orn-tc-photo:not(.tc-ph-trigger)"),r=e&&e.querySelector(".orn-tc-1"),o=e&&e.querySelector(".orn-tc-2"),i=e&&e.querySelector(".tc-frame-content"),a=e&&e.querySelector(".tc-frame");t&&a&&t.addEventListener("click",function(){var e,t,c,s;e=a.getBoundingClientRect(),t=e.left+e.width/2,c=e.bottom-.15*e.height,s=gsap.timeline({onComplete:function(){"function"==typeof startTheJourney&&startTheJourney()}}),[n,r,o,i].forEach(function(e){if(e){var n=e.getBoundingClientRect(),r=n.left+n.width/2,o=n.top+n.height/2;s.to(e,{x:"+="+(t-r),y:"+="+(c-o),scale:0,autoAlpha:0,duration:.75,ease:"power2.in"},0)}})})}function getRundownScroller(){return window.matchMedia("(max-width: 960px)").matches?".kat-page__side-to-side":window}window.addEventListener("resize",updatePreviewKadoCSS);var rundownTriggers=[];function initRundownAnimation(e){rundownTriggers.forEach(function(e){e.kill()}),rundownTriggers=[];var t=document.querySelectorAll("section.rundown-container .rundown-agenda-list");t.length&&"undefined"!=typeof gsap&&"undefined"!=typeof ScrollTrigger&&(gsap.registerPlugin(ScrollTrigger),t.forEach(function(t){var n=t.querySelector(".orn-rd-center");if(n){var r=n.querySelector("svg"),o=t.querySelectorAll(".rundown-agenda");if(o.length){var i=Array.from(o).map(function(e){return e.offsetTop+e.offsetHeight/2-n.offsetHeight/2});if(gsap.set(n,{y:i[0]}),r){var a=gsap.fromTo(r,{rotation:0},{rotation:720,ease:"none",scrollTrigger:{scroller:e,trigger:t,start:"top 85%",end:"bottom center",scrub:1.2}});a.scrollTrigger&&rundownTriggers.push(a.scrollTrigger)}o.forEach(function(t,n){rundownTriggers.push(ScrollTrigger.create({scroller:e,trigger:t,start:"top center",end:"bottom center",onEnter:function(){c(i[n])},onEnterBack:function(){c(i[n])}}))})}}function c(e){gsap.timeline().to(n,{scale:0,duration:.2,ease:"power2.in"}).set(n,{y:e}).to(n,{scale:1,duration:.45,ease:"back.out(1.7)"})}}))}window.addEventListener("load",function(){window.matchMedia("(max-width: 960px)").addEventListener("change",function(){initRundownAnimation(getRundownScroller()),ScrollTrigger.refresh()})}),$(document).ready(function(){if(adjustContainerHeight(),initHeightObserver(),initContentResizeSync(),initTopCoverInteraction(),initOpenInvAnimation(),window.addEventListener("load",function(){adjustContainerHeight(),initLoveStoryAnimation(),initGalleryParallax(),initRundownAnimation(getRundownScroller()),"undefined"!=typeof ScrollTrigger&&ScrollTrigger.refresh()}),$(".kado-wrapper"))var e=setInterval(function(){var t=$(".hadiah-wrap");t.length&&t.children().length>0&&(clearInterval(e),updatePreviewKadoCSS(),init_gifts_slick())},500)}),$(window).on("resize",()=>{adjustContainerHeight(),initHeightObserver()});