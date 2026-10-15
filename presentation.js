document.querySelectorAll('[data-presentation-carousel]').forEach((carousel) => {
  const viewport = carousel.querySelector('.presentation-viewport');
  const slides = carousel.querySelectorAll('.presentation-slide');
  const previous = carousel.querySelector('[data-presentation-prev]');
  const next = carousel.querySelector('[data-presentation-next]');
  const count = carousel.querySelector('[data-presentation-count]');
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
