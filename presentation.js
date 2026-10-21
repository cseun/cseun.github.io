const imageDialog = document.createElement('dialog');
imageDialog.className = 'slide-image-dialog';
imageDialog.setAttribute('aria-label', '발표자료 이미지 확대');
imageDialog.innerHTML = `<div class="slide-image-toolbar"><span class="slide-image-title"></span><div><button type="button" data-image-prev aria-label="이전 페이지">‹</button><span data-image-count aria-live="polite"></span><button type="button" data-image-next aria-label="다음 페이지">›</button><button type="button" data-zoom-out aria-label="축소">−</button><button type="button" data-zoom-reset>화면에 맞춤</button><button type="button" data-zoom-in aria-label="확대">+</button><button type="button" data-image-close aria-label="전체 화면 닫기">닫기 ×</button></div></div><div class="slide-image-stage"><img alt=""><video controls playsinline hidden></video></div>`;
document.body.append(imageDialog);
const enlargedImage = imageDialog.querySelector('img');
const imageStage = imageDialog.querySelector('.slide-image-stage');
const enlargedVideo = imageDialog.querySelector('video');
let activeSlides = [];
let activeIndex = 0;
let imageZoom = 1;
let imageOrigin;
let oldOverflow;
function sizeImage() {
  if (!enlargedImage.naturalWidth) return;
  const fit = Math.min((imageStage.clientWidth - 32) / enlargedImage.naturalWidth, (imageStage.clientHeight - 32) / enlargedImage.naturalHeight, 1);
  enlargedImage.style.width = `${enlargedImage.naturalWidth * fit * imageZoom}px`;
  enlargedImage.style.height = 'auto';
}
function displayPage(index) {
  activeIndex = Math.max(0, Math.min(index, activeSlides.length - 1));
  const figure = activeSlides[activeIndex];
  const source = figure.querySelector('img, video');
  imageZoom = 1;
  enlargedVideo.pause();
  const isVideo = source.tagName === 'VIDEO';
  enlargedImage.hidden = isVideo;
  enlargedVideo.hidden = !isVideo;
  if (isVideo) {
    enlargedVideo.src = source.currentSrc || source.querySelector('source')?.src || source.src;
    enlargedVideo.poster = source.poster;
    source.pause();
  } else {
    enlargedImage.alt = source.alt;
    enlargedImage.src = source.currentSrc || source.src;
  }
  imageDialog.querySelector('.slide-image-title').textContent = figure.querySelector('figcaption')?.textContent || source.alt;
  imageDialog.querySelector('[data-image-count]').textContent = `${activeIndex + 1} / ${activeSlides.length}`;
  imageDialog.querySelector('[data-image-prev]').disabled = activeIndex === 0;
  imageDialog.querySelector('[data-image-next]').disabled = activeIndex === activeSlides.length - 1;
  imageDialog.querySelectorAll('[data-zoom-in], [data-zoom-out], [data-zoom-reset]').forEach(button => { button.disabled = isVideo; });
  sizeImage();
  imageStage.scrollTo(0, 0);
}
function openImage(source) {
  imageOrigin = source;
  activeSlides = [...source.closest('[data-presentation-carousel]').querySelectorAll('.presentation-slide')];
  activeIndex = activeSlides.indexOf(source.closest('.presentation-slide'));
  oldOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  imageDialog.showModal();
  displayPage(activeIndex);
  if (imageDialog.requestFullscreen) imageDialog.requestFullscreen().catch(() => {});
  imageDialog.querySelector('[data-image-close]').focus();
}
enlargedImage.addEventListener('load', sizeImage);
imageDialog.querySelector('[data-zoom-in]').addEventListener('click', () => { imageZoom = Math.min(4, imageZoom + .5); sizeImage(); });
imageDialog.querySelector('[data-zoom-out]').addEventListener('click', () => { imageZoom = Math.max(1, imageZoom - .5); sizeImage(); });
imageDialog.querySelector('[data-zoom-reset]').addEventListener('click', () => { imageZoom = 1; sizeImage(); imageStage.scrollTo(0, 0); });
imageDialog.querySelector('[data-image-close]').addEventListener('click', () => imageDialog.close());
imageDialog.addEventListener('click', event => { if (event.target === imageDialog) imageDialog.close(); });
imageDialog.addEventListener('close', () => { enlargedVideo.pause(); if (document.fullscreenElement === imageDialog) document.exitFullscreen().catch(() => {}); document.body.style.overflow = oldOverflow; imageOrigin?.focus({ preventScroll: true }); });
imageDialog.querySelector('[data-image-prev]').addEventListener('click', () => displayPage(activeIndex - 1));
imageDialog.querySelector('[data-image-next]').addEventListener('click', () => displayPage(activeIndex + 1));
imageDialog.addEventListener('keydown', event => {
  if (event.target === enlargedVideo) return;
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); displayPage(activeIndex + (event.key === 'ArrowRight' ? 1 : -1)); }
});
window.addEventListener('resize', () => { if (imageDialog.open) sizeImage(); });

document.querySelectorAll('[data-presentation-carousel]').forEach((carousel) => {
  carousel.querySelectorAll('.presentation-slide img').forEach(source => {
    source.tabIndex = 0;
    source.setAttribute('role', 'button');
    source.setAttribute('aria-label', `${source.alt} — 확대해서 보기`);
    let startX = 0;
    let startY = 0;
    source.addEventListener('pointerdown', event => { startX = event.clientX; startY = event.clientY; });
    source.addEventListener('click', event => { if (Math.hypot(event.clientX - startX, event.clientY - startY) < 12) openImage(source); });
    source.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); event.stopPropagation(); openImage(source); }
    });
  });
  const hint = carousel.querySelector('.presentation-hint');
  if (hint) hint.textContent = '좌우로 넘기거나 이미지를 눌러 확대해서 볼 수 있습니다.';
  const viewport = carousel.querySelector('.presentation-viewport');
  const slides = carousel.querySelectorAll('.presentation-slide');
  const previous = carousel.querySelector('[data-presentation-prev]');
  const next = carousel.querySelector('[data-presentation-next]');
  const count = carousel.querySelector('[data-presentation-count]');
  const fullscreen = document.createElement('button');
  fullscreen.type = 'button';
  fullscreen.textContent = '전체 화면 ⛶';
  fullscreen.setAttribute('aria-label', '현재 자료 전체 화면으로 보기');
  fullscreen.addEventListener('click', () => { openImage(slides[index].querySelector('img, video')); imageOrigin = fullscreen; });
  carousel.querySelector('.presentation-controls').append(fullscreen);
  let index = 0;

  function updateControls() {
    count.textContent = `${index + 1} / ${slides.length}`;
    previous.disabled = index === 0;
    next.disabled = index === slides.length - 1;
  }

  function showSlide(target) {
    index = Math.max(0, Math.min(target, slides.length - 1));
    viewport.scrollTo({ left: slides[index].offsetLeft - slides[0].offsetLeft, behavior: 'smooth' });
    updateControls();
  }

  previous.addEventListener('click', () => showSlide(index - 1));
  next.addEventListener('click', () => showSlide(index + 1));
  viewport.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showSlide(index + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  viewport.addEventListener('scroll', () => {
    index = Math.max(0, Math.min(Math.round(viewport.scrollLeft / viewport.clientWidth), slides.length - 1));
    updateControls();
  }, { passive: true });
  window.addEventListener('resize', () => {
    viewport.scrollLeft = slides[index].offsetLeft - slides[0].offsetLeft;
  });

  updateControls();
});
