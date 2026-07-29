const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
const year = document.querySelector('#year');

const replaySectionUnderline = (section) => {
  section.classList.remove('nav-target');
  // Force a completed keyframe to reset before replaying it on a later nav click.
  void section.offsetWidth;
  requestAnimationFrame(() => section.classList.add('nav-target'));
};

const replaySectionUnderlineWhenVisible = (section, frame = 0) => {
  const heading = section.querySelector('h2');
  const bounds = (heading || section).getBoundingClientRect();
  const triggerLine = Math.min(window.innerHeight * 0.45, 320);
  const isVisible = bounds.top < triggerLine && bounds.bottom > 0;

  if (isVisible) {
    section.classList.add('in-view');
    replaySectionUnderline(section);
    return;
  }

  if (frame < 180) {
    requestAnimationFrame(() => replaySectionUnderlineWhenVisible(section, frame + 1));
  }
};

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
      const destination = link.getAttribute('href');
      const target = destination?.startsWith('#') ? document.querySelector(destination) : null;

      if (target) {
        target.classList.add('nav-reveal');
        replaySectionUnderlineWhenVisible(target);
      }

      nav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    nav.classList.remove('is-open');
    navToggle.setAttribute('aria-expanded', 'false');
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

if ('IntersectionObserver' in window) {
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
} else {
  revealTargets.forEach((element) => element.classList.add('in-view'));
}
