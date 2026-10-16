/* Progressive enhancement: all project content is available without JavaScript. */
(() => {
  'use strict';
  const controls = document.querySelector('.project-filters');
  const cards = [...document.querySelectorAll('.project-card[data-category]')];
  if (!controls || cards.length === 0) return;
  const buttons = [...controls.querySelectorAll('button[data-filter]')];
  if (buttons.length === 0) return;

  const status = document.createElement('p');
  status.className = 'filter-status';
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  controls.insertAdjacentElement('afterend', status);

  const show = (active) => {
    const filter = active.dataset.filter;
    buttons.forEach((button) => {
      button.setAttribute('aria-pressed', String(button === active));
    });
    let count = 0;
    cards.forEach((card) => {
      card.hidden = filter !== 'all' && card.dataset.category !== filter;
      if (!card.hidden) count += 1;
    });
    status.textContent = `Showing ${count} project${count === 1 ? '' : 's'}.`;
  };

  buttons.forEach((button) => button.addEventListener('click', () => show(button)));
  show(buttons.find((button) => button.dataset.filter === 'all') || buttons[0]);
  controls.hidden = false;
})();
