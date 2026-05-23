const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
const year = document.querySelector('#year');

if (year) {
  year.textContent = String(new Date().getFullYear());
}

if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('is-open');
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

const revealTargets = [
  ...document.querySelectorAll('.section'),
  ...document.querySelectorAll('.card'),
  ...document.querySelectorAll('.cert-area-group'),
];

revealTargets.forEach((element, index) => {
  element.classList.add('reveal');
  element.style.setProperty('--reveal-delay', `${Math.min(index * 35, 220)}ms`);
});

const revealObserver = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('in-view');
      observer.unobserve(entry.target);
    });
  },
  {
    threshold: 0.15,
    rootMargin: '0px 0px -40px 0px',
  },
);

revealTargets.forEach((element) => revealObserver.observe(element));
