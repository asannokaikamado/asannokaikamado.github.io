// スマホメニュー
const toggle = document.getElementById("menuToggle");
const gnav = document.getElementById("gnav");
toggle.addEventListener("click", () => {
  const open = gnav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", open);
});
gnav.addEventListener("click", e => {
  if (e.target.tagName === "A") { gnav.classList.remove("open"); toggle.setAttribute("aria-expanded", false); }
});

// 献立表：「今月の献立.jpg」（拡張子が小文字）で置かれた場合も表示できるようにする
document.querySelectorAll("img[data-kondate]").forEach(img => {
  const retry = () => {
    if (img.dataset.retried) return;
    img.dataset.retried = "1";
    const alt = img.getAttribute("src").replace(/\.JPG$/, ".jpg");
    img.src = alt;
    document.querySelectorAll("a[data-kondate]").forEach(a => a.setAttribute("href", alt));
  };
  img.addEventListener("error", retry);
  if (img.complete && img.naturalWidth === 0) retry();
});

// カード型スライダー（写真の一覧は tools/update_gallery.py が index.html に書き出す）
(() => {
  const track = document.getElementById("slTrack");
  const bar = document.getElementById("slBar");
  const idxEl = document.getElementById("slIdx");
  const prev = document.querySelector(".sl-btn.prev");
  const next = document.querySelector(".sl-btn.next");
  const cards = [...track.querySelectorAll(".sl-card")];
  if (cards.length < 2) return;

  document.getElementById("slTotal").textContent = cards.length;

  const step = () => cards[1].offsetLeft - cards[0].offsetLeft;
  const maxScroll = () => track.scrollWidth - track.clientWidth;
  const currentIndex = () => Math.round(track.scrollLeft / step());
  const goTo = i => track.scrollTo({ left: Math.max(0, Math.min(i, cards.length - 1)) * step(), behavior: "smooth" });

  const update = () => {
    const atEnd = track.scrollLeft >= maxScroll() - 4;
    const i = atEnd ? cards.length - 1 : currentIndex();
    idxEl.textContent = i + 1;
    bar.style.width = ((i + 1) / cards.length * 100) + "%";
    prev.disabled = track.scrollLeft <= 4;
    next.disabled = atEnd;
  };
  let ticking = false;
  track.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { update(); ticking = false; });
  }, { passive: true });

  prev.addEventListener("click", () => { goTo(currentIndex() - 1); restart(); });
  next.addEventListener("click", () => { goTo(currentIndex() + 1); restart(); });
  track.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") { e.preventDefault(); goTo(currentIndex() + 1); restart(); }
    if (e.key === "ArrowLeft") { e.preventDefault(); goTo(currentIndex() - 1); restart(); }
  });

  // 自動再生：最後まで行ったら先頭へ戻る（ホバー・操作中は止める）
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let timer = null, paused = false;
  const restart = () => {
    clearInterval(timer);
    if (reduce) return;
    timer = setInterval(() => {
      if (paused || document.hidden) return;
      if (track.scrollLeft >= maxScroll() - 4) track.scrollTo({ left: 0, behavior: "smooth" });
      else goTo(currentIndex() + 1);
    }, 3500);
  };
  const slider = track.closest(".slider-wrap");
  slider.addEventListener("mouseenter", () => paused = true);
  slider.addEventListener("mouseleave", () => paused = false);
  slider.addEventListener("focusin", () => paused = true);
  slider.addEventListener("focusout", () => paused = false);
  track.addEventListener("touchstart", () => { paused = true; }, { passive: true });
  track.addEventListener("touchend", () => { paused = false; restart(); }, { passive: true });

  update();
  restart();
})();
