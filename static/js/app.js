/* Navigation and existing-action confirmations. No external JS dependency. */
(() => {
  const toggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  function setMenu(open) {
    sidebar.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    overlay.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    if (open) sidebar.querySelector('a').focus();
  }
  toggle.addEventListener('click', () => setMenu(!sidebar.classList.contains('is-open')));
  overlay.addEventListener('click', () => { setMenu(false); toggle.focus(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && sidebar.classList.contains('is-open')) {
      setMenu(false); toggle.focus();
    }
    if (event.key === 'Tab' && sidebar.classList.contains('is-open')) {
      const links = Array.from(sidebar.querySelectorAll('a, button'));
      const first = links[0], last = links[links.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); first.focus();
      }
    }
  });
  window.matchMedia('(min-width: 761px)').addEventListener('change', event => {
    if (event.matches) setMenu(false);
  });
  document.querySelectorAll('[data-confirm]').forEach(link => {
    link.addEventListener('click', event => {
      if (!window.confirm(link.dataset.confirm)) event.preventDefault();
    });
  });
})();
