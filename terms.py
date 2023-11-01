
# words to strip that you will never want to analyze
# especially for words that will never be "interesting" to our data, regardless of context.
# ex: if 'factor' is never part of a string you care to see, regardless of what words it's paired with, add it here.
#
# however, a counter example...
# perhaps "admin" by itself isn't useful, but "linux admin" together is.
# in that case, you wouldn't put "admin" in STOP, but rather in IGNORE (and put "linux admin" in PHRASES)
#
# it's best to fill this up with as much junk words as possible, because it cuts words out in the beginning and will prevent
# extra unnecessary looping
STOP = {
    'join','level','review','content','builder','detail','liaise','evaluating','make','~','’','e.g', 'e.g.','i.e.','i.e','take','action','+'
}

# words to be excluded from the final output - if any stand-alone word isn't interesting, include it here. If there are words that will
# never be interesting (like stop words), put them in STOP instead. Some of these words may appear coupled with other words in PHRASES, since they
# could be interesting in a phrase context.
IGNORE = {
    'area', 'organization', 'pipeline', 'ecosystem', 'expectation', 'browser', 'perform', 'collective', 'drive', 'contributes', 'report', 
    'feature', 'fortune', 'collaborative', 'author', 'demo', 'team', 'input', 'culture', 'define', 'view', 'oversee', 'healthcare', 'coordination', 
    'discus', 'update', 'ensures', 'error', 'clean', 'salary', 'provide', 'communicator', 'ok', 'issue', 'k', 'sexuality', 'professional', 
    'solution', 'line', 'phone', 'assurance', 'behavior', 'storybook', 'accordance', 'creates', 'program', 'enhancement', 'country', 'coding', 
    'conference', 'reuse', 'order', 'effectiveness', 'investigate', 'request', 'technique', 'student', 'purpose', 'computer', 'influence', 
    'validation', 'compatibility', 'match', 'maintainability', 'demonstration', 'power', 'increase', 'abreast', 'second', 'tooling', 'dental', 
    'adherence', 'regression', '*', 'side', 'delivery', 'verification', 'visa', 'event', 'meeting', 'object', 'intent', 'scale', 'produce', 
    'referral', 'release', 'party', 'measure', 'image', 'training', 'performing', 'insurance', 'requirement', 'develop', 'communicate', 'gender', 
    'three', 'role', 'in-house', 'material', 'use', 'compliance', 'delivers', 'stage', 'goal', 'enterprise', 'ease', 'anticipate', 'experience', 
    'engage', 'insight', 'edge', 'foster', 'incident', 'windows', 'mockups', 'scope', 'range', 'mission', 'desktop', 'manager', 'holiday', 
    'tutoring', 'prototype', 'foundation', 'work-life', 'proven', 'opportunity', 'employer', 'teammate', 'duty', 'worker', 'metric', 'company', 
    'self-learner', 'ideation', 'landscape', 'qualification', 'facility', 'post-release', 'interview', 'existing', 'complexity', 'world', 
    'element', 'payment', 'module', 'quality', 'documenting', 'eligibility', 'bottleneck', 'recommend', 'constructive', 'engagement', 'strategy', 
    'proficiency', 'operating', 'person', 'conversation', 'contributor', 'consistency', 'bar', 'database', 'minute', 'solver', 'validate', 
    'identity', 'world-class', 'lieu', 'contribute', 'status', 'development', 'methodology', 'overtime', 'ability', 'change', 'performance', 
    'course', 'collaborates', 'online', 'industry', 'prepare', 'independence', 'sci', 'responsive', 'future', 'method', 'reach', 'query', 
    'discipline', 'year', 'allowance', 'help', 'translate', 'machine', 'month', 'troubleshoot', 'generation', 'spring', 'bi', 'handling', 
    'maintaining', 'contribution', 'call', 'participant', 'suite', 'someone', 'layer', 'card', 'build', 'serve', 'scalability', 'traffic', 
    'innovation', 'executive', 'architect', 'flow', 'execute', 'master', 'troubleshooting', 'towards', 'improvement', 'facilitating', 'operation', 
    'conduct', 'aim', 'record', 'run', 'template', 'parental', 'pay', 'individual', 'equation', 'factor', 'camera', 'form', 'week', 'cause', 
    'applies', 'write', 'acquisition', 'building', 'downtime', 'volume', 'mentor', 'advancement', 'repair', 'interface', 'leverage', 'assist', 
    'consideration', 'acceptance', 'retirement', 'community', 'risk', 'jr', 'model', 'log', 'guidance', 'functioning', 'software', 'integrity', 
    'confer', 'supervision', 'table', 'tradeoff', 'roadmap', 'analytics', 'deploy', 'computing', 'fixing', 'mentorship', 'coverage', 'passionate', 
    'robust', 'monitor', 'architecture', 'operate', 'storage', 'ticket', 'advocate', 'end-to-end', 'something', 'scientist', 'relevant', 'adheres', 
    'page', 'expert', 'manipulation', 'office', 'balance', 'engineer', 'evaluate', 'disability', 'version', 'equipment', 'medium', 'government', 
    'ship', 'file', 'decision', 'flexibility', 'response', 'feasibility', 'agility', 'designing', 'availability', 'tool', 'system', 'alternative', 
    'peer', 'transparency', 'thorough', 'domain', 'resource', 'hour', 'appropriate', 'ceremony', 'opening', 'platform', 'duration', 'testing', 
    'mentoring', 'matter', 'definition', 'progression', 'compose', 'editor', 'planning', 'rule', 'emphasis', 'phase', 'excellence', 'right', 
    'position', 'create', 'product', 'setting', 'idea', 'health', 'conversion', 'audience', 'specification', 'collection', 'option', 'others', 
    'root', 'making', 'on-going', 'religion', 'maintain', 'container', 'timeline', 'identify', 'prepares', 'expertise', 'equity', 'train', 
    'application', 'seek', 'moral', 'play', 'vision', 'brand', 'evaluation', 'craft', 'member', 'asset', 'teamwork', 'sense', 'leader', 
    'onboarding', 'account', 'alignment', 'sex', 'detail', 'cycle', 'engine', 'hands-on', 'intern', 'staff', 'custom', 'skill', 'store', 
    'scripting', 'connectivity', 'resolution', 'transform', 'sale', 'deliver', 'orientation', 'study', 'two', 'responsibility', 'associate', 
    'productivity', 'raise', 'service', 'vacation', 'transformation', 'hand', 'publication', 'etc', 'institution', 'configure', 'construction', 
    'develops', 'hiring', 'functional', 'process', 'message', 'integrate', 'detection', 'stakeholder', 'capacity', 'champion', 'family', 'job', 
    'estimation', 'identifies', 'liaison', 'refactor', 'dashboard', 'prioritization', 'million', 'exposure', 'site', 'approval', 'interact', 
    'fulfillment', 'prospect', 'owner', 'way', 'working', 'yr', 'comment', 'consequence', 'verify', 'focus', 'approach', 'controller', 'addition', 
    'authentication', 'speaking', 'target', 'thing', 'vendor', 'globe', 'tech', 'look', 'authorization', 'climate', 'tracking', 'triage', 'plan', 
    'code', 'fix', 'identifying', 'spending', 'situation', 'impact', 'hp', 'interest', 'backlog', 'cutting', 'standard', 'limitation', 'exchange', 
    'alternate', 'center', 'base', 'component', 'today', 'success', 'initiative', 'production', 'task', 'display', 'background', 'gather', 
    'compiling', 'share', 'modification', 'junior', 'story', 'hire', 'life', 'simulation', 'website', 'offering', 'candidate', 'stack', 'partner', 
    'installation', 'science', 'style', 'usability', 'field', 'trouble', 'yesterday', 'hardware', 'source', 'creator', 'optimization', 'output', 
    'advice', 'completion', 'logic', 'ui', 'answer', 'interaction', 'collaborate', 'concept', 'cross-browser', 'connection', 'performs', 
    'reference', 'analysis', 'internet', 'review', 'education', 'document', 'learning', 'department', 'understanding', 'finding', 'estimate', 
    'thrive', 'race', 'case', 'stock', 'practice', 'clearance', 'in-depth', 'confluence', 'marketing', 'blog', 'network', 'relocation', 'attitude', 
    'reporting', 'reliability', 'grooming', 'mobile', 'creativity', 'minimum', 'high-performance', 'infrastructure', 'resume', 'respond', 
    'university', 'commitment', 'adoption', 'gathering', 'environment', 'sensor', 'package', 'milestone', 'pair', 'diagram', 'result', 'lunch', 
    'support', 'certification', 'unit', 'knowledge', 'constraint', 'experiment', 'configuration', 'writing', 'leave', 'personnel', 'driver', 
    'passion', 'learn', 'end', 'defect', 'participate', 'bug', 'modify', 'location', 'objective', 'providing', 'proficient', 'day', 'career', 
    'type', 'ownership', 'simplicity', 'accuracy', 'grow', 'pull', 'city', 'information', 'reimbursement', 'customizes', 'size', 'research', 
    'engineering', 'presentation', 'statement', 'cost', 'function', 'aspect', 'hibernate', 'hourly', 'permit', 'contractor', 'internship', 'lead', 
    'algorithm', 'customer', 'desire', 'employee', 'framework', 'key', 'counterpart', 'guide', 'space', 'debugging', 'user', 'structure', 'one', 
    'security', 'relationship', 'procedure', 'feedback', 'accountability', 'level', 'implement', 'db', 'workflow', 'coach', 'participates', 
    'optimize', 'question', 'assignment', 'investigation', 'safety', 'advance', 'progress', 'library', 'facilitate', 'email', 'responsiveness', 
    'cross', 'benefit', 'upgrade', 's', 'rest', 'respect', 'app', 'migration', 'language', 'stay', 'accessibility', 'series', 'debug', 'script', 
    'cutting-edge', 'expense', 'collaboration', 'trade-off', 'gateway', 'journey', 'trend', 'discussion', 'demonstrate', 'orchestration', 
    'enhance', 'provider', 'technology', 'secure', 'protocol', 'functionality', 'failure', 'check', 'college', 'variety', 'design', 'middleware', 
    'translating', 'familiarity', 'courage', 'fundamental', 'director', 'programming', 'activity', 'dependency', 'mindset', 'apps', 'group', 
    'effort', 'life-cycle', 'work', 'problem', 'instruction', 'deployment', 'coordinate', 'monitoring', 'refinement', 'integration', 
    'problem-solving', 'date', 'facing', 'portfolio', 'efficiency', 'core', 'lifecycle', 'legacy', 'leadership', 'processing', 'accounting', 
    'part', 'start', 'align', 'priority', 'citizen', 'capability', 'basis', 'stability', 'maintenance', 'while', 'self-starter', 'improve', 
    'apply', 'class', 'scenario', 'please', 'bonus', 'criterion', 'conducting', 'colleague', 'entirety', 'trading', 'value', 'deliverable', 
    'guideline', 'challenge', 'bs', 'people', 'pattern', 'offer', 'degree', 'compass', 'boot', 'developing', 'attention', 'reward', 'configures', 
    'place', 'assessment', 'codebase', 'management', 'address', 'maintains', 'direction', 'subject', 'window', 'business', 'project', 'care', 
    'need', 'manage', 'time', 'regulation', 'manner', 'citizenship', 'color', 'capital', 'schedule', 'remuneration', 'tomorrow', 'access', 'note', 
    'seamless', 'participation', 'inquiry', 'assistance', 'execution', 'understand', 'willingness', 'utility', 'demand', 'analyst', 'principle', 
    'complex', 'control', 'end-users', 'resolve', 'rate', 'amount', 'everyone', 'diversity', 'session', 'automation', 'repository', 'ethic', 
    'earn', 'ground', 'mind', 'aid', 'connect', 'manual', 'rollout', 'efficient', 'administration', 'plus', 'recommendation', 'growth', 'contract',
    'outcome', 'market', 'set', 'employment', 'communication', 'analyzes', 'point', 'deadline', 'applicant', 'speed', 'consumer', 'applying', 
    'search', 'term', 'wisdom', 'policy', 'profession', 'usage', 'client', 'player', 'corporation', 'screen', 'meet', 'firm', 'home', 
    'partnership', 'state', 'track', 'setup', 'merit', 'device', 'analyze', 'diverse', 'high-quality', 'excellent', 'restriction', 'comprehensive', 
    'equivalent', 'money', 'data', 'test', 'hr', 'designer', 'developer', 'server', 'mechanism', 'travel', 'recognition', 'documentation', 
    'pricing', 'implementation', 'layout', 'creation'}

# tech words we specifically wanna look out for
# not really that important in theory, but helps nonetheless to ensure these terms are not ignored or stripped out
# especially useful if a term might be interpreted as not a noun (like 'react', which might be seen as a verb)
os = {'linux','unix','debian','ubuntu','ios','windows','mac','android','mobile','macos'}
prog_lang = {'javascript','java','typescript','go','golang','c','c#','c++','bash','.net','js',}
frameworks = {'react','react.js','reactjs','node.js','nodejs','angular','angular.js','angularjs','vue','vue.js','vuejs','material-ui','mui','vuetify'}
db = {'sql','mysql','postgres','nosql','serverless'}
misc = {'a*','kernel','git'}
SAVE_WORDS = set().union(os,prog_lang,frameworks,db,misc)

# phrases or terms that includes spaces - since sentences are split by spaces, we try to intercept these terms first
SAVE_PHRASES = [
    'back end',
    'front end',
    'object oriented',
    'ruby on rails',
    'site reliability',
    'machine learning',
    'data mining',
    'artificial intelligence',
    'data analysis',
    'unit test',
    'computer science',
    'bachelor degree',
    "bachelors degree",
    'master degree',
    "masters degree",
    'full stack',
    'google cloud',
    'oracle cloud',
    'amazon web service',
    'rest api',
    'restful api',
    'natural language processing',
    'visual studio',
    'vs code',
    'ci cd',
    'react js',
    'angular js',
    'vue js',
    'node js',
    '3d modeling',
]

# preferred names for conflated terms
javascript = 'Javascript'
typescript = 'Typescript'
node = 'Node.js'
react = 'React.js'
vue = 'Vue.js'
angular = 'Angular.js'
golang = 'Go'
oop = 'OOP'
frontend = 'front-end'
backend = 'back-end'
rails = 'Ruby-on-Rails'
ruby = 'Ruby'
dotnet = '.NET'
api = 'API'
restAPI = 'RESTful API'
nlp = 'Natural Language Processing'
sass = 'Sass'
ux = 'UX'
aws = 'AWS'
gcp = 'Google Cloud'
azure = 'Azure'
oracloud = 'Oracle Cloud'
python = 'Python'
java = 'Java'
ml = 'Machine Learning'
ai = 'Artificial Intelligence'
csharp = 'C#'
cplus = 'C++'
c = 'C'
perl = 'Perl'
visualstudio = 'Visual Studio'
bachelor = "Bachelor's Degree"
master = "Master's Degree"
sql = 'SQL'
nosql = 'NoSQL'
ios = 'iOS'

# terms to conflate into a singular preferred form
# since there are many ways a given concept may be written, we conform
# them all using this dictionary
CONFLATE = {
    # javascript/typescript
    'js': javascript,
    'javascript': javascript,
    'ts': typescript,
    'typescript': typescript,
    # react
    'react': react,
    'reactjs': react,
    'react.js': react,
    'react js': react,
    # vue
    'vuejs': vue,
    'vue': vue,
    'vue.js': vue,
    'vue js': vue,
    # angular
    'angular': angular,
    'angularjs': angular,
    'angular.js': angular,
    'angular js': angular,
    #node
    'node': node,
    'nodejs': node,
    'node.js': node,
    'node js': node,
    # golang
    'golang': golang,
    'go.lang': golang,
    'go': golang,
    # ruby-on-rails
    'ruby-on-rails': rails,
    'ruby on rails': rails,
    'rails': rails,
    # ruby
    'ruby': ruby,
    # .NET
    '.net': dotnet,
    '.NET': dotnet,
    # Sass
    'sass': sass,
    'scss': sass,
    # python
    'python': python,
    'py': python,
    # java
    'java': java,
    # c#
    'c#': csharp,
    'c-sharp': csharp,
    # c++
    'c++': cplus,
    # c
    'c': c,
    # perl:
    'perl': perl,
    # sql
    'sql': sql,
    'mysql': sql,
    'postgre': sql,
    'postgresql': sql,
    'nosql': nosql,
    # cloud
    'aws': aws,
    'amazon web service': aws,
    'gcp': gcp,
    'google cloud': gcp,
    'google cloud platform': gcp,
    'azure': azure,
    'oracle cloud': oracloud,
    # misc
    'batchelor': bachelor,
    'bachelor': bachelor,
    'bachelor degree': bachelor,
    'bachelors degree': bachelor,
    'baccalaureate': bachelor,
    'masters': master,
    'master degree': master,
    'masters degree': master,
    'restful api': restAPI,
    'rest api': restAPI,
    'restful': restAPI,
    'oop': oop,
    'object-oriented': oop,
    'object-oriented-programming': oop,
    'object oriented': oop,
    'object oriented programming': oop,
    'frontend': frontend,
    'front-end': frontend,
    'front end': frontend,
    'backend': backend,
    'back-end': backend,
    'back end': backend,
    'api': api,
    'apis': api,
    'nlp': nlp,
    'natural language processing': nlp,
    'ux': ux,
    'ml': ml,
    'machine learning': ml,
    'ai': ai,
    'artificial intelligence': ai,
    'vs': visualstudio,
    'vs code': visualstudio,
    'visual studio': visualstudio,
    'ios': ios
}