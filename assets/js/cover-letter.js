const coverLetterForm = document.querySelector('#cover-letter-form');
const letterDraft = document.querySelector('#letter-draft');
const copyLetterButton = document.querySelector('#copy-letter');
const keywordMatch = document.querySelector('#keyword-match');
const keywordMatchSummary = document.querySelector('#keyword-match-summary');
const keywordMatchList = document.querySelector('#keyword-match-list');

const supportedTerms = [
  { label: 'CI/CD', aliases: ['ci/cd', 'continuous integration', 'continuous delivery'] },
  { label: 'Jenkins', aliases: ['jenkins'] },
  { label: 'Groovy', aliases: ['groovy'] },
  { label: 'Spinnaker', aliases: ['spinnaker'] },
  { label: 'Python', aliases: ['python'] },
  { label: 'Kubernetes', aliases: ['kubernetes', 'k8s'] },
  { label: 'Docker', aliases: ['docker', 'containers', 'containerisation', 'containerization'] },
  { label: 'Helm/Helmfile', aliases: ['helm', 'helmfile'] },
  { label: 'Artifact repositories', aliases: ['artifactory', 'nexus', 'artifact repository', 'artifact management'] },
  { label: 'Unit testing', aliases: ['unit testing', 'unit tests', 'automated testing', 'automated tests'] },
  { label: 'Git', aliases: ['git', 'gerrit'] },
  { label: 'Bash', aliases: ['bash', 'shell scripting'] },
  { label: 'APIs', aliases: ['api', 'apis'] },
  { label: 'SQLite', aliases: ['sqlite'] },
  { label: 'PHP', aliases: ['php'] },
  { label: 'SCSS', aliases: ['scss', 'sass'] },
  { label: 'HTML and CSS', aliases: ['html', 'css'] },
  { label: 'JavaScript', aliases: ['javascript'] },
  { label: 'Responsive web development', aliases: ['responsive design', 'responsive web', 'responsive behaviour', 'responsive behavior'] },
  { label: 'Accessibility', aliases: ['accessibility', 'accessible'] },
  { label: 'Quality assurance', aliases: ['quality assurance', 'qa'] },
];

const asSentence = (value) => /[.!?]$/.test(value) ? value : `${value}.`;

const joinedList = (items) => {
  if (items.length < 2) return items[0] || '';
  if (items.length === 2) return `${items[0]} and ${items[1]}`;
  return `${items.slice(0, -1).join(', ')}, and ${items.at(-1)}`;
};

const containsTerm = (text, term) => {
  const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(?:^|[^a-z0-9])${escapedTerm}(?=$|[^a-z0-9])`, 'i').test(text);
};

const supportedTermsIn = (description) => {
  const normalisedDescription = description.toLocaleLowerCase();
  return supportedTerms.filter(({ aliases }) => aliases.some((term) => containsTerm(normalisedDescription, term)));
};

const lowerFirst = (value) => `${value.charAt(0).toLocaleLowerCase()}${value.slice(1)}`;

const experienceFor = (cv, focus) => {
  const ericsson = cv.experience.find(({ organisation }) => organisation === 'Ericsson');
  const ossark = cv.experience.find(({ organisation }) => organisation === 'Ossark');
  const tradingProject = cv.projects.find(({ title }) => title === 'Multi-Broker Trading Research Platform');

  if (focus === 'web' && ossark) {
    return `At ${ossark.organisation}, I ${lowerFirst(ossark.bullets[0])} I also ${lowerFirst(ossark.bullets[2])}`;
  }

  if (focus === 'software' && ericsson && tradingProject) {
    return `At ${ericsson.organisation}, I ${lowerFirst(ericsson.bullets[1])} In my ${tradingProject.title} project, I ${lowerFirst(tradingProject.bullets[1])}`;
  }

  if (ericsson) {
    return `At ${ericsson.organisation}, I ${lowerFirst(ericsson.bullets[0])} I also ${lowerFirst(ericsson.bullets[2])}`;
  }

  return cv.profile;
};

const buildLetter = (cv, values) => {
  const company = values.company.trim();
  const role = values.role.trim();
  const hiringManager = values.hiringManager.trim();
  const requirements = values.requirements.trim();
  const motivation = values.motivation.trim();
  const applicationType = values.applicationType;
  const matchedTerms = supportedTermsIn(requirements).map(({ label }) => label);
  const greeting = hiringManager ? `Dear ${hiringManager},` : 'Dear Hiring Manager,';
  const profile = cv.profile.replace(/\s+/g, ' ').trim();
  const applicationContext = applicationType === 'us-internship'
    ? 'As a University of Galway Computer Science & Information Technology student, I am seeking an opportunity to apply my practical engineering experience in an internship setting.'
    : 'As I work towards my degree at the University of Galway, I am seeking to begin my career in a graduate engineering role.';
  const tailoring = motivation
    ? `I am particularly interested in this opportunity because ${asSentence(motivation)}`
    : `I am keen to contribute my practical software engineering experience to ${company}.`;
  const requirementsSentence = matchedTerms.length
    ? `The role's emphasis on ${joinedList(matchedTerms.slice(0, 4))} aligns well with the experience I have developed through internships and personal projects.`
    : 'I would welcome the opportunity to apply this experience in a new team and continue developing as an engineer.';

  return `${greeting}\n\nI am writing to apply for the ${role} position at ${company}. ${applicationContext}\n\n${profile}\n\n${experienceFor(cv, values.focus)}\n\n${tailoring} ${requirementsSentence}\n\nThank you for considering my application. I would welcome the opportunity to discuss how my experience and interest in software engineering could contribute to ${company}.\n\nKind regards,\n${cv.name}`;
};

const showKeywordMatch = (requirements) => {
  const matchedTerms = supportedTermsIn(requirements).map(({ label }) => label);
  keywordMatch.hidden = false;
  keywordMatchList.replaceChildren();

  if (!requirements) {
    keywordMatchSummary.textContent = 'Add the job description to identify CV-supported terms for this application.';
    return;
  }

  if (!matchedTerms.length) {
    keywordMatchSummary.textContent = 'No direct CV-supported terms were identified. Review the job description and use only skills you can evidence.';
    return;
  }

  keywordMatchSummary.textContent = `${matchedTerms.length} supported term${matchedTerms.length === 1 ? '' : 's'} identified from the job details.`;
  matchedTerms.forEach((term) => {
    const item = document.createElement('li');
    item.textContent = term;
    keywordMatchList.append(item);
  });
};

const loadCv = async () => {
  const response = await fetch('content/cv.json');
  if (!response.ok) throw new Error('Unable to load CV data.');
  return response.json();
};

if (coverLetterForm && letterDraft && copyLetterButton) {
  let cv;

  loadCv().then((data) => {
    cv = data;
  }).catch(() => {
    letterDraft.placeholder = 'The CV details could not be loaded. Please refresh and try again.';
  });

  coverLetterForm.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!cv) {
      letterDraft.placeholder = 'The CV details are still loading. Please try again in a moment.';
      return;
    }

    const values = Object.fromEntries(new FormData(coverLetterForm));
    letterDraft.value = buildLetter(cv, values);
    showKeywordMatch(values.requirements.trim());
    copyLetterButton.disabled = false;
    letterDraft.focus();
  });

  copyLetterButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(letterDraft.value);
    } catch {
      letterDraft.select();
      document.execCommand('copy');
    }

    copyLetterButton.textContent = 'Copied';
    window.setTimeout(() => {
      copyLetterButton.textContent = 'Copy';
    }, 1800);
  });
}
