// Local portfolio motion demos, displayed through motion-lab.html.
if (document.body.classList.contains('portfolio-home') && !document.body.classList.contains('credentials-page') && new URLSearchParams(window.location.search).get('motion-lab') === '1') {
  document.body.classList.add('motion-lab');

  const demos = [
    ['hero', 'Hero type reveal', 'An editorial first impression'],
    ['nav', 'Navigation entrance', 'A quiet sequential arrival'],
    ['sections', 'Section signatures', 'Rules draw beneath fixed headings'],
    ['rows', 'Row arrival', 'Projects and roles rise in sequence'],
    ['rowHover', 'Row spotlight', 'A soft wash follows focus'],
    ['details', 'Detail unfold', 'Expanded content settles into place'],
    ['skills', 'Skill constellation', 'Tags arrive in a measured cascade'],
    ['contact', 'Contact invitation', 'Arrows travel toward their links'],
  ];

  const panel = document.createElement('aside');
  panel.className = 'motion-lab-panel';
  panel.setAttribute('aria-label', 'Local animation demos');
  panel.innerHTML = `
    <details open>
      <summary><span>Motion lab</span><span class="motion-lab-count"></span></summary>
      <div class="motion-lab-panel-body">
        <p>Local preview only. Toggle each idea, then replay the visible page.</p>
        <div class="motion-lab-options"></div>
        <div class="motion-lab-actions">
          <button type="button" data-action="all">All on</button>
          <button type="button" data-action="none">All off</button>
          <button type="button" data-action="replay">Replay visible</button>
        </div>
        <p class="motion-lab-reduced" hidden>Reduced motion is enabled, so these effects stay still.</p>
      </div>
    </details>
  `;
  document.body.append(panel);

  const options = panel.querySelector('.motion-lab-options');
  demos.forEach(([key, name, description]) => {
    const label = document.createElement('label');
    label.className = 'motion-lab-option';
    label.innerHTML = `<input type="checkbox" checked><span><strong>${name}</strong><small>${description}</small></span>`;
    label.querySelector('input').dataset.demo = key;
    options.append(label);
  });

  const inputs = [...options.querySelectorAll('input')];
  const targets = [
    ...document.querySelectorAll('.hero, main > .section:not(.hero), .editorial-row, .skill-group'),
  ];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.querySelectorAll('.site-nav a').forEach((link, index) => {
    link.style.setProperty('--motion-order', index);
  });
  document.querySelectorAll('.editorial-list').forEach((list) => {
    list.querySelectorAll(':scope > .editorial-row').forEach((row, index) => {
      row.style.setProperty('--motion-order', index);
    });
  });
  document.querySelectorAll('.skill-group').forEach((group, index) => {
    group.style.setProperty('--motion-order', index);
    group.querySelectorAll('.project-chips li').forEach((chip, chipIndex) => {
      chip.style.setProperty('--motion-order', chipIndex);
    });
  });

  const updateReducedMotion = () => {
    panel.querySelector('.motion-lab-reduced').hidden = !reducedMotion.matches;
  };
  reducedMotion.addEventListener('change', updateReducedMotion);
  updateReducedMotion();

  const replayVisible = () => {
    const visible = targets.filter((element) => {
      const bounds = element.getBoundingClientRect();
      return bounds.bottom > 0 && bounds.top < window.innerHeight;
    });
    visible.forEach((element) => element.classList.remove('motion-seen'));
    document.body.classList.remove('motion-started');
    void document.body.offsetWidth;
    requestAnimationFrame(() => {
      document.body.classList.add('motion-started');
      visible.forEach((element) => element.classList.add('motion-seen'));
    });
  };

  const applyOptions = () => {
    inputs.forEach((input) => {
      document.body.classList.toggle(`motion-${input.dataset.demo}`, input.checked);
    });
    panel.querySelector('.motion-lab-count').textContent = `${inputs.filter((input) => input.checked).length}/${inputs.length}`;
    replayVisible();
  };

  options.addEventListener('change', applyOptions);
  panel.querySelector('[data-action="all"]').addEventListener('click', () => {
    inputs.forEach((input) => { input.checked = true; });
    applyOptions();
  });
  panel.querySelector('[data-action="none"]').addEventListener('click', () => {
    inputs.forEach((input) => { input.checked = false; });
    applyOptions();
  });
  panel.querySelector('[data-action="replay"]').addEventListener('click', replayVisible);

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('motion-seen');
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' });
    targets.forEach((element) => observer.observe(element));
  } else {
    targets.forEach((element) => element.classList.add('motion-seen'));
  }

  if (window.matchMedia('(max-width: 600px)').matches) panel.querySelector('details').open = false;
  applyOptions();
}
