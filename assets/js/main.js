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

const certificateAreas = document.querySelector('.cert-areas');

const certificateTracks = [
  {
    id: 'ai',
    title: 'AI & Generative AI',
    meta: 'LLM development, machine learning, RAG, agents, and AI foundations',
  },
  {
    id: 'devops',
    title: 'DevOps & CI/CD',
    meta: 'Delivery pipelines, infrastructure as code, automation, and operational practices',
  },
  {
    id: 'kubernetes',
    title: 'Kubernetes & Containers',
    meta: 'Kubernetes application delivery, containerisation, and Linux administration',
  },
  {
    id: 'security',
    title: 'Security',
    meta: 'Cloud, network, application, and cryptographic security',
  },
  {
    id: 'cloud',
    title: 'Cloud Infrastructure',
    meta: 'Cloud platforms, networking, deployment, migration, and observability',
  },
  {
    id: 'data',
    title: 'Data Engineering',
    meta: 'Data acquisition, processing, querying, and Google Cloud data engineering',
  },
];

const certificateTrackFor = (title) => {
  if (
    /^(Claude |AI Fluency|Introduction to Model Context Protocol|Building with the Claude API|AI Capabilities|Generative AI Driver|AI Skills Fest|AWS Generative AI Developer|AWS Certified Machine Learning)/.test(title)
    || title.includes('Google Machine Learning and AI')
  ) {
    return 'ai';
  }

  if (title.includes('Kubernetes') || title.startsWith('Red Hat') || title.includes('Containers and Virtualization')) {
    return 'kubernetes';
  }

  if (/DevOps|CI\/CD|Infrastructure as Code|Automation and Orchestration/.test(title)) {
    return 'devops';
  }

  if (/CCSP|Certified in Cybersecurity|SCOR/.test(title)) {
    return 'security';
  }

  if (title.startsWith('GCP Data Engineer') || title.startsWith('CompTIA Data+')) {
    return 'data';
  }

  return 'cloud';
};

if (certificateAreas) {
  const certificateCards = [...certificateAreas.querySelectorAll('.cert-card')];
  const cardsByTrack = new Map(certificateTracks.map((track) => [track.id, []]));

  certificateCards.forEach((card) => {
    const title = card.querySelector('.cert-title')?.textContent?.trim() || '';
    cardsByTrack.get(certificateTrackFor(title))?.push(card);
  });

  const groupedCertificates = document.createDocumentFragment();

  certificateTracks.forEach(({ id, title, meta }) => {
    const cards = cardsByTrack.get(id) || [];
    if (!cards.length) return;

    const group = document.createElement('details');
    group.className = 'cert-area-group';

    const summary = document.createElement('summary');
    const groupTitle = document.createElement('span');
    groupTitle.className = 'cert-title';
    groupTitle.textContent = title;
    const groupMeta = document.createElement('span');
    groupMeta.className = 'cert-meta';
    groupMeta.textContent = meta;
    summary.append(groupTitle, groupMeta);

    const overview = document.createElement('div');
    overview.className = 'cert-overview';
    overview.append(...cards);

    group.append(summary, overview);
    groupedCertificates.append(group);
  });

  certificateAreas.replaceChildren(groupedCertificates);
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
