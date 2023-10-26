
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
    'join','level','review','content','builder','detail','liaise','evaluating','make','~','’','e.g', 'e.g.','i.e.','i.e'
}

# words to be excluded from the final output - if any stand-alone word isn't interesting, include it here. If there are words that will
# never be interesting (like stop words), put them in STOP instead. Some of these words may appear coupled with other words in PHRASES, since they
# could be interesting in a phrase context.
IGNORE = {
    '*', 'ability', 'abreast', 'acceptance', 'access', 'accessibility', 'accordance', 'account', 'accountability', 'accuracy', 'acquisition', 
    'action', 'activity', 'addition', 'address', 'adherence', 'adheres', 'administration', 'adoption', 'advance', 'advancement', 'advice', 
    'advocate', 'agility', 'aim', 'algorithm', 'align', 'alignment', 'allowance', 'alternate', 'alternative', 'amount', 'analysis', 'analytics', 
    'analyze', 'analyzes', 'answer', 'app', 'applicant', 'application', 'applies', 'apply', 'applying', 'approach', 'appropriate', 'approval', 
    'apps', 'architecture', 'area', 'aspect', 'assessment', 'asset', 'assignment', 'assist', 'assistance', 'associate', 'assurance', 'attention', 
    'attitude', 'authentication', 'authorization', 'automation', 'availability', 
    'background', 'backlog', 'balance', 'base', 'basis', 'behavior', 'benefit', 'bi', 'blog', 'bonus', 'bottleneck', 'browser', 'bug', 'build', 
    'building', 'business', 
    'camera', 'candidate', 'capability', 'capacity', 'capital', 'card', 'care', 'career', 'case', 'cause', 'center', 'ceremony', 'certification', 
    'challenge', 'champion', 'change', 'citizen', 'citizenship', 'city', 'clean', 'clearance', 'client', 'climate', 'coach', 'code', 'codebase', 
    'coding', 'collaborate', 'collaborates', 'collaboration', 'collaborative', 'colleague', 'collection', 'collective', 'college', 'comment', 
    'commitment', 'communicate', 'communication', 'communicator', 'community', 'company', 'compass', 'compatibility', 'compiling', 'completion', 
    'complex', 'complexity', 'compliance', 'component', 'compose', 'comprehensive', 'computer', 'computing', 'concept', 'conduct', 'conducting', 
    'confer', 'conference', 'configuration', 'configures', 'confluence', 'connect', 'connectivity', 'consequence', 'consideration', 'consistency', 
    'constraint', 'construction', 'constructive', 'consumer', 'container', 'contract', 'contractor', 'contribute', 'contribution', 'contributor', 
    'control', 'controller', 'conversation', 'conversion', 'coordinate', 'coordination', 'core', 'corporation', 'cost', 'counterpart', 'country', 
    'courage', 'coverage', 'craft', 'create', 'creates', 'creation', 'creativity', 'creator', 'cross-browser', 'culture', 'custom', 'customer', 
    'customizes', 'cutting', 'cutting-edge', 'cycle', 
    'dashboard', 'data', 'date', 'day', 'db', 'deadline', 'debug', 'debugging', 'decision', 'defect', 'define', 'definition', 'degree', 'deliver', 
    'deliverable', 'delivers', 'delivery', 'demand', 'demo', 'demonstrate', 'demonstration', 'dental', 'department', 'dependency', 'deploy', 
    'deployment', 'design', 'designer', 'designing', 'desire', 'detail', 'detection', 'develop', 'developer', 'developing', 'development', 
    'develops', 'device', 'diagram', 'direction', 'director', 'disability', 'discipline', 'discus', 'discussion', 'display', 'diverse', 'document', 
    'documentation', 'documenting', 'domain', 'drive', 'driver', 'duration', 'duty', 'database',
    'earn', 'ecosystem', 'edge', 'editor', 'education', 'effectiveness', 'efficiency', 'efficient', 'effort', 'element', 
    'eligibility', 'email', 'emphasis', 'employee', 'employer', 'employment', 'end', 'end-to-end', 'end-users', 'engage', 'engagement', 'engine', 
    'engineer', 'engineering', 'enhance', 'enhancement', 'ensures', 'enterprise', 'entirety', 'environment', 'equation', 'equipment', 'equivalent', 
    'error', 'estimate', 'estimation', 'etc', 'ethic', 'evaluate', 'evaluation', 'event', 'everyone', 'excellence', 'excellent', 'exchange', 
    'execute', 'execution', 'executive', 'expense', 'experience', 'experiment', 'expert', 'expertise', 'exposure', 
    'facilitate', 'facilitating', 'facility', 'facing', 'factor', 'failure', 'familiarity', 'family', 'feasibility', 'feature', 'feedback', 
    'field', 'firm', 'fix', 'flexibility', 'flow', 'focus', 'form', 'fortune', 'foster', 'foundation', 'framework', 'function', 'functional', 
    'functionality', 'functioning', 'fundamental', 'future', 
    'gateway', 'gather', 'gathering', 'generation', 'globe', 'goal', 'government', 'grooming', 'ground', 'group', 'growth', 'guidance', 'guide', 
    'guideline', 
    'hand', 'handling', 'hands-on', 'hardware', 'health', 'healthcare', 'help', 'hibernate', 'high-performance', 'high-quality', 'hire', 'holiday', 
    'home', 'hour', 'hourly', 'hr', 'hp',
    'idea', 'ideation', 'identifies', 'identify', 'identifying', 'identity', 'image', 'impact', 'implement', 'implementation', 'improve', 
    'improvement', 'in-depth', 'in-house', 'incident', 'increase', 'independence', 'individual', 'industry', 'influence', 'information', 
    'infrastructure', 'initiative', 'innovation', 'input', 'inquiry', 'insight', 'installation', 'institution', 'instruction', 'insurance', 
    'integrate', 'integration', 'integrity', 'intent', 'interact', 'interaction', 'interest', 'interface', 'internet', 'interview', 'investigate', 
    'investigation', 'issue', 'job', 'journey', 'jr', 'key', 'knowledge', 'landscape', 'language', 'layout', 'lead', 'leader', 'leadership', 'learn', 
    'learning', 'leverage', 'liaison', 'library', 'lieu', 'life', 'life-cycle', 'lifecycle', 'limitation', 'line', 'location', 'log', 'logic', 'lunch', 
    'maintain', 'maintainability', 'maintaining', 'maintains', 'maintenance', 'making', 'manage', 'management', 'manager', 'manipulation', 'manner', 
    'market', 'marketing', 'match', 'material', 'matter', 'measure', 'mechanism', 'medium', 'meet', 'meeting', 'member', 'mentor', 'merit', 'message', 
    'method', 'methodology', 'metric', 'middleware', 'migration', 'million', 'mind', 'mindset', 'minimum', 'mission', 'mobile', 'mockups', 'model', 
    'modification', 'modify', 'module', 'money', 'monitor', 'monitoring', 'month', 'moral', 'need', 'network', 
    'object', 'objective', 'offer', 'office', 'ok', 'on-going', 'onboarding', 'online', 'opening', 'operate', 'operating', 'operation', 'opportunity', 
    'optimization', 'optimize', 'option', 'orchestration', 'order', 'organization', 'orientation', 'others', 'outcome', 'output', 'oversee', 
    'overtime', 'owner', 'ownership', 
    'package', 'page', 'pair', 'part', 'participant', 'participate', 'participates', 'partner', 'partnership', 'party', 'passion', 'passionate', 
    'pattern', 'pay', 'payment', 'peer', 'people', 'perform', 'performance', 'performing', 'performs', 'permit', 'personnel', 'phase', 'pipeline', 
    'place', 'plan', 'planning', 'platform', 'play', 'player', 'please', 'plus', 'point', 'policy', 'portfolio', 'position', 'power', 'practice', 
    'prepare', 'prepares', 'presentation', 'pricing', 'principle', 'prioritization', 'priority', 'problem', 'problem-solving', 'procedure', 
    'process', 'processing', 'produce', 'product', 'production', 'productivity', 'profession', 'professional', 'proficiency', 'proficient', 
    'program', 'programming', 'progress', 'progression', 'project', 'prospect', 'protocol', 'prototype', 'provide', 'providing', 'publication', 
    'pull', 'purpose', 
    'qualification', 'quality', 'question', 
    'raise', 'range', 'rate', 'reach', 'recognition', 'recommend', 'recommendation', 'record', 'reference', 'referral', 'refinement', 'regression', 
    'regulation', 'reimbursement', 'relationship', 'release', 'relevant', 'reliability', 'relocation', 'remuneration', 'report', 'reporting', 
    'repository', 'request', 'requirement', 'research', 'resolution', 'resolve', 'resource', 'respond', 'response', 'responsibility', 'responsive', 
    'responsiveness', 'rest', 'restriction', 'result', 'resume', 'retirement', 'review', 'reward', 'right', 'risk', 'robust', 'role', 'rule', 'run', 
    's', 'safety', 'salary', 'sale', 'scalability', 'scale', 'scenario', 'schedule', 'science', 'scope', 'screen', 'script', 'scripting', 'seamless', 
    'search', 'second', 'secure', 'security', 'seek', 'self-learner', 'self-starter', 'sense', 'sensor', 'series', 'serve', 'server', 'service', 
    'session', 'set', 'setup', 'share', 'side', 'simplicity', 'simulation', 'site', 'situation', 'size', 'skill', 'software', 'solution', 'solver', 
    'someone', 'something', 'source', 'speaking', 'specification', 'speed', 'spending', 'spring', 'stability', 'stack', 'staff', 'stage', 'stakeholder', 
    'standard', 'start', 'state', 'status', 'stay', 'stock', 'storage', 'store', 'story', 'storybook', 'strategy', 'structure', 'style', 'subject', 
    'success', 'suite', 'supervision', 'support', 'system', 
    'table', 'target', 'task', 'team', 'teammate', 'teamwork', 'tech', 'technique', 'technology', 'template', 'term', 'test', 'testing', 'thing', 
    'thorough', 'thrive', 'time', 'timeline', 'today', 'tomorrow', 'tool', 'tooling', 'towards', 'track', 'tracking', 'trade-off', 'tradeoff', 
    'traffic', 'training', 'transform', 'transformation', 'translating', 'transparency', 'travel', 'trend', 'triage', 'trouble', 'troubleshoot', 
    'troubleshooting', 'ui', 'understand', 'understanding', 'update', 'upgrade', 'usability', 'usage', 'use', 'user', 'utility', 
    'vacation', 'validation', 'value', 'variety', 'vendor', 'verification', 'verify', 'version', 'view', 'visa', 'vision', 'volume', 
    'way', 'website', 'week', 'while', 'willingness', 'window', 'windows', 'wisdom', 'work', 'work-life', 'worker', 'workflow', 'working', 'world', 
    'world-class', 'write', 'writing', 
    'year', 'yesterday', 'yr'}


# tech words we want to make sure aren't ignored or stripped by NLTK logic by accident
# our logic ideally allows any noun-like terms (that aren't stop words/ignored) to go through
# but sometimes weird things happen, so just to be safe I am listing popular terms or ones that may potentially be erroneously ignored.
SAVE_WORDS = {
    'react','react.js','assembly','git','cloud','angular','angular.js','c#','c++','mobile','android','ios','oop','object-oriented',
    'node','node.js','restful','go','golang','.net','linux','unix','macos','windows','web3','github','nosql','mysql','sql','aws','gcp',
    'bash','kernel','material-ui','mui','vuetify','a*','js'
}

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
    'system administrator',
    'full stack',
    'team lead',
    'senior engineer',
    'senior developer',
    'junior engineer',
    'junior developer',
    'web developer',
    'application developer',
    'application engineer',
    'mobile developer',
    'google cloud',
    'amazon web service',
    'rest api',
    'restful api',
    'system engineer',
    'natural language processing',
    'visual studio',
    'vs code',
    'ci cd',
    'react js',
    'angular js',
    'vue js'

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
python = 'Python'
java = 'Java'
ml = 'Machine Learning'
ai = 'Artificial Intelligence'
csharp = 'C#'
cplus = 'C++'
visualstudio = 'Visual Studio'
bachelor = "Bachelor's Degree"
master = "Master's Degree"

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
    # vue
    'vuejs': vue,
    'vue': vue,
    'vue.js': vue,
    # angular
    'angular': angular,
    'angularjs': angular,
    'angular.js': angular,
    #node
    'node': node,
    'nodejs': node,
    'node.js': node,
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
    # misc
    'batchelor': bachelor,
    'bachelor': bachelor,
    'bachelor degree': bachelor,
    'bachelors degree': bachelor,
    'baccalaureate': bachelor,
    'master': master,
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
    'aws': aws,
    'amazon web service': aws,
    'ml': ml,
    'machine learning': ml,
    'ai': ai,
    'artificial intelligence': ai,
    'vs': visualstudio,
    'vs code': visualstudio,
    'visual studio': visualstudio
}