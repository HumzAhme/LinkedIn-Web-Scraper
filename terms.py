
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
    '*','+', 'ability', 'abstraction', 'acceptance', 'access', 'accessibility', 'accountability', 'accuracy', 'act', 'activity', 'addition', 
    'address', 'adherence', 'adheres', 'administration', 'administrator', 'adoption', 'advancement', 'advantage', 'advice', 'advocate', 'agency', 
    'algorithm', 'align', 'alignment', 'ambiguity', 'analysis', 'analyst', 'analytics', 'analyze', 'analyzes', 'anticipate', 'app', 'applicant', 
    'application', 'approach', 'appropriate', 'apps', 'architect', 'architecture', 'area', 'artifact', 'aspect', 'ass', 'assessment', 'asset', 'assignment', 
    'assist', 'assistance', 'associate', 'assurance', 'attention', 'attitude', 'audience', 'authentication', 'author', 'authorization', 
    'autonomy', 'availability', 'average', 'awareness', 'background', 'backlog', 'balance', 'bar', 'base', 'basis', 'batch', 'behavior', 'benefit', 
    'bonus', 'bottleneck', 'brand', 'browser', 'bs', 'budget', 'bug', 'build', 'building', 'business', 'call', 'candidate', 'capability', 'capacity', 
    'capture', 'care', 'career', 'case', 'cause', 'center', 'ceremony', 'certification', 'challenge', 'champion', 'chance', 'change', 'charge', 
    'chart', 'citizen', 'citizenship', 'clarity', 'class', 'clean', 'clearance', 'client', 'co-founders', 'coach', 'code', 'codebase', 'codebases', 
    'coding', 'collaborate', 'collaborates', 'collaboration', 'colleague', 'collection', 'college', 'color', 'combination', 'command', 'comment', 
    'commitment', 'communicate', 'communicates', 'communication', 'communicator', 'community', 'company', 'compatibility', 'compensation',
    'competency', 'completeness', 'completion', 'complex', 'complexity', 'compliance', 'component', 'computer', 'computing', 'concept', 'concise', 
    'conduct', 'confidence', 'configuration', 'configure', 'confluence', 'connect', 'connection', 'consideration', 'consistency', 'constraint', 
    'consumer', 'contact', 'context', 'contract', 'contractor', 'contribute', 'contributes', 'contribution', 'contributor', 'control', 'conversion', 
    'coordinate', 'coordination', 'core', 'correct', 'correctness', 'cost', 'country', 'course', 'coverage', 'craft', 'create', 'creates', 
    'creation', 'creativity', 'creator', 'criterion', 'cross', 'culture', 'curiosity', 'curve', 'custom', 'customer', 'cutting-edge', 'cycle', 
    'dashboard', 'data', 'database', 'date', 'day', 'deadline', 'debt', 'debug', 'debugging', 'debugs', 'decision', 'defect', 'define', 
    'definition', 'degree', 'deliver', 'deliverable', 'delivers', 'delivery', 'demo', 'demonstrate', 'dental', 'department', 'dependency',
    'deploy', 'deploying', 'deployment', 'description', 'design', 'designer', 'designing', 'desire', 'desktop', 'determines', 'dev', 'develop', 
    'developer', 'developing', 'development', 'develops', 'device', 'diagram', 'direction', 'disability', 'disaster', 'discipline', 'discovery', 
    'discus', 'discussion', 'disease', 'display', 'diverse', 'diversity', 'document', 'documentation', 'documenting', 'domain', 'drive', 'driven', 
    'driver', 'duplication', 'duration', 'duty', 'ease', 'ecosystem', 'edge', 'education', 'effectiveness', 'efficiency', 'efficient', 'effort', 
    'element', 'embrace', 'empathy', 'emphasis', 'employee', 'employer', 'employment', 'end', 'end-to-end', 'end-user', 'end-users', 'endpoint', 
    'energy', 'engage', 'engagement', 'engine', 'engineer', 'engineering', 'enhance', 'enhancement', 'ensures', 'ensure', 'enterprise', 'entity', 
    'environment', 'equipment', 'equity', 'equivalent', 'error', 'estimate', 'estimation', 'etc', 'evaluate', 'evaluation', 'event', 'everyone', 
    'everything', 'evolution', 'example', 'excellence', 'exchange', 'execute', 'executes', 'execution', 'executive', 'exp', 'expectation', 
    'experience', 'experiment', 'expert', 'expertise', 'exposure', 'express', 'extensibility', 'extension', 'eye', 'facility', 'facing', 'factor', 
    'failure', 'familiarity', 'family', 'fast', 'feasibility', 'feature', 'feedback', 'feel', 'field', 'file', 'finance', 'finding', 'firm', 'fix', 
    'fixing', 'flexibility', 'flow', 'flowchart', 'fluent', 'focus', 'forefront', 'form', 'format', 'foundation', 'founder', 'framework', 'fun', 
    'function', 'functionality', 'fundamental', 'future', 'gap', 'gateway', 'gather', 'gathering', 'generate', 'generation', 'globe', 'goal', 
    'government', 'graduate', 'grasp', 'ground', 'group', 'grow', 'growth', 'guidance', 'guide', 'guideline', 'hand', 'hardware', 'hat', 'head', 
    'health', 'healthcare', 'help', 'hibernate', 'high-performance', 'high-quality', 'hire', 'hiring', 'holiday', 'home', 'hour', 'hundred', 'idea', 
    'identification', 'identifies', 'identify', 'identity', 'image', 'impact', 'implement', 'implementation', 'implementing', 'improvement', 
    'in-house', 'inception', 'incident', 'inclusion', 'individual', 'industry', 'influence', 'information', 'infrastructure', 'ingestion', 
    'initiative', 'injection', 'innovation', 'input', 'insight', 'installation', 'instruction', 'insurance', 'integrate', 'integration', 'integrity', 
    'intelligence', 'interact', 'interaction', 'interest', 'interface', 'interoperability', 'interview', 'investigate', 'investigation', 
    'investment', 'issue', 'item', 'iterate', 'iteration', 'job', 'judgment', 'junior', 'k', 'kind', 'knowledge', 'language', 'latency', 'launch', 
    'layer', 'layout', 'lead', 'leader', 'leadership', 'learn', 'learning', 'leave', 'legacy', 'leverage', 'library', 'life', 'lifecycle', 'line', 
    'load', 'location', 'log', 'logging', 'logic', 'look', 'loop', 'love', 'machine', 'maintain', 'maintainability', 'maintains', 'maintenance', 
    'manage', 'management', 'manager', 'manipulation', 'manner', 'manual', 'manufacturing', 'market', 'marketing', 'marketplace', 'master', 'match', 
    'material', 'matter', 'measure', 'mechanism', 'medium', 'meet', 'meeting', 'member', 'memory', 'mentor', 'mentoring', 'mentorship', 'message', 
    'method', 'methodology', 'metric', 'micro', 'migration', 'milestone', 'million', 'mind', 'mindset', 'minimum', 'mission', 'mockups', 'model', 
    'modeling', 'modification', 'modifies', 'modify', 'module', 'monitor', 'monitoring', 'month', 'multiple', 'multitude', 'name', 'need', 'network', 
    'networking', 'note', 'number', 'object', 'objective', 'observability', 'offer', 'offering', 'office', 'one', 'online', 'operating', 'operation', 
    'opportunity', 'optimization', 'optimize', 'option', 'orchestration', 'order', 'organization', 'others', 'outcome', 'output', 'oversee', 'owner', 
    'ownership', 'package', 'page', 'pair', 'part', 'participate', 'participates', 'partner', 'party', 'passion', 'passionate', 'path', 'patient', 
    'pattern', 'pay', 'payment', 'peer', 'people', 'perform', 'performance', 'performant', 'performs', 'person', 'personnel', 'phase', 'phone', 
    'physic', 'piece', 'pipeline', 'place', 'plan', 'planning', 'platform', 'player', 'plus', 'point', 'policy', 'polygraph', 'population', 
    'portfolio', 'position', 'power', 'practice', 'prepare', 'prepares', 'presentation', 'prevent', 'pride', 'principle', 'priority', 'privacy', 
    'problem', 'problem-solving', 'procedure', 'process', 'processing', 'produce', 'product', 'production', 'productivity', 'professional', 
    'proficiency', 'proficient', 'program', 'programmer', 'programming', 'progress', 'project', 'promote', 'propose', 'protection', 'protocol', 
    'prototype', 'prototyping', 'provide', 'provider', 'pto', 'purpose', 'qa', 'qualification', 'quality', 'query', 'question', 'range', 'rate', 
    'recognition', 'recommendation', 'record', 'reduction', 'refactor', 'refactoring', 'regression', 'regulation', 'reimbursement', 'relationship', 
    'release', 'reliability', 'remediation', 'report', 'reporting', 'repository', 'request', 'requirement', 'research', 'resiliency', 'resolution', 
    'resolve', 'reference', 'resource', 'respect', 'response', 'responsibility', 'responsive', 'responsiveness', 'result', 'retirement', 'retrieval', 
    'retrospective', 'reuse', 'revenue', 'risk', 'roadmap', 'roadmaps', 'robustness','robust', 'role', 'roll-out', 'root', 'safety', 'salary', 'sale', 
    'satisfaction', 'saving', 'scalability', 'scale', 'scaling', 'scenario', 'schedule', 'science', 'scientist', 'scope', 'score', 'scratch', 
    'screen', 'script', 'scripting', 'seamless', 'search', 'secure', 'security', 'selection', 'self-learner', 'self-starter', 'sense', 'sensor', 
    'series', 'serve', 'server', 'service', 'session', 'set', 'setting', 'setup', 'share', 'sharing', 'ship', 'shortage', 'simple', 'simulation', 
    'site', 'situation', 'skill', 'software', 'solution', 'solve', 'solver', 'solving', 'someone', 'something', 'source', 'space', 'spec', 
    'specialist', 'specification', 'speed', 'stability', 'stack', 'staff', 'stage', 'stakeholder', 'standard', 'start', 'startup', 'state', 
    'statement', 'status', 'stay', 'step', 'storage', 'story', 'strategy', 'structure', 'student', 'study', 'style', 'success', 'suggestion', 
    'suite', 'supervision', 'support', 'system', 'table', 'talent', 'task', 'team', 'teammate', 'teamwork', 'tech', 'technique', 'technology', 
    'template', 'term', 'test', 'testing', 'thing', 'thinking', 'thousand', 'threat', 'ticket', 'tier', 'time', 'timeline', 'today', 'tool', 
    'tooling', 'top', 'towards', 'track', 'tracking', 'trade-off', 'tradeoff', 'train', 'training', 'transfer', 'transformation', 'transition', 
    'translate', 'travel', 'trend', 'triage', 'troubleshoot', 'troubleshooting', 'troubleshoots', 'trust', 'tuition', 'tuning', 'type', 'understand', 
    'understanding', 'unit', 'university', 'update', 'upgrade', 'us', 'usability', 'usage', 'use', 'user', 'utility', 'vacation', 'validate', 
    'validation', 'value', 'variety', 'vehicle', 'velocity', 'vendor', 'verification', 'version', 'video', 'view', 'vision', 'voice', 'volume', 
    'vulnerability', 'way', 'web', 'website', 'week', 'willingness', 'window', 'wireframes', 'word', 'work', 'workarounds', 'workflow', 'workplace', 
    'world', 'world-class', 'write', 'writing', 'year', 'yrs', 'zone','proven','shape','transparency','sprint','must','fairness','paid','ethics','ethic','pace',
    'apply','recommend','accordance','groundbreaking','fortune','ui','self-actualization','ceo','complies','electrical','third','w','gender','race'
}

# tech words we specifically wanna look out for
# not really that important in theory, but helps nonetheless to ensure these terms are not ignored or stripped out
# especially useful if a term might be interpreted as not a noun (like 'react', which might be seen as a verb)
os = {'linux','unix','debian','ubuntu','ios','windows','mac','android','mobile','macos'}
prog_lang = {'javascript','java','typescript','go','golang','c','c#','c++','bash','.net','js','swift','matlab','r','lisp','scheme','cobol','prolog','objective-c','python','rust','ruby'}
frameworks = {'react','react.js','reactjs','node.js','nodejs','angular','angular.js','angularjs','vue','vue.js','vuejs','material-ui','mui','vuetify','svelte','redux'}
db = {'sql','mysql','postgres','nosql','serverless'}
misc = {'a*','git','sass','docker','kubernetes','automation','security','remote','hybrid'}
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
    'ci/cd',
    'ci cd',
    'continuous deployment',
    'react js',
    'angular js',
    'vue js',
    'node js',
    'express js',
    'neural network',
    'spring boot',
    'mongo db',
    'large language model',
    'visual basic',
    'assembly language',
    'tailwind css',
    'internet of things',
    'react native',
    # slash terms
    'pl/sql',

]

# preferred names for conflated terms
class terms:
    'preferred forms of common tech terms'
    javascript = 'Javascript'
    typescript = 'Typescript'
    node = 'Node.js'
    react = 'React.js'
    vue = 'Vue.js'
    angular = 'Angular.js'
    express = 'Express.js'
    golang = 'Go'
    oop = 'OOP'
    frontend = 'front-end'
    backend = 'back-end'
    fullstack = 'full-stack'
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
    mongodb = 'MongoDB'
    microservices = 'Microservices'
    css = 'CSS'
    html = 'HTML'
    llm = 'Large Language Model'
    container = 'Containerization'
    cicd = 'CI/CD'
    iot = 'IoT'
    compsci = 'Computer Science'
    git = 'Git'
    github = 'GitHub'

# terms to conflate into a singular preferred form
# since there are many ways a given concept may be written, we conform
# them all using this dictionary
CONFLATE = {
    # javascript/typescript
    'js': terms.javascript,
    'javascript': terms.javascript,
    'ts': terms.typescript,
    'typescript': terms.typescript,
    # react
    'react': terms.react,
    'reactjs': terms.react,
    'react.js': terms.react,
    'react js': terms.react,
    # vue
    'vuejs': terms.vue,
    'vue': terms.vue,
    'vue.js': terms.vue,
    'vue js': terms.vue,
    # angular
    'angular': terms.angular,
    'angularjs': terms.angular,
    'angular.js': terms.angular,
    'angular js': terms.angular,
    #node
    'node': terms.node,
    'nodejs': terms.node,
    'node.js': terms.node,
    'node js': terms.node,
    # other js
    'expressjs': terms.express,
    'express js': terms.express,
    'express.js': terms.express,
    'express': terms.express,
    # golang
    'golang': terms.golang,
    'go.lang': terms.golang,
    'go': terms.golang,
    # ruby-on-rails
    'ruby-on-rails': terms.rails,
    'ruby on rails': terms.rails,
    'rails': terms.rails,
    'rail': terms.rails,
    # ruby
    'ruby': terms.ruby,
    # .NET
    '.net': terms.dotnet,
    '.NET': terms.dotnet,
    # Sass
    'sass': terms.sass,
    'scss': terms.sass,
    # python
    'python': terms.python,
    'py': terms.python,
    # java
    'java': terms.java,
    # c#
    'c#': terms.csharp,
    'c-sharp': terms.csharp,
    # c++
    'c++': terms.cplus,
    # c
    'c': terms.c,
    # perl:
    'perl': terms.perl,
    # sql
    'sql': terms.sql,
    'mysql': terms.sql,
    'postgre': terms.sql,
    'postgresql': terms.sql,
    'nosql': terms.nosql,
    # cloud
    'aws': terms.aws,
    'amazon web service': terms.aws,
    'gcp': terms.gcp,
    'google cloud': terms.gcp,
    'google cloud platform': terms.gcp,
    'azure': terms.azure,
    'oracle cloud': terms.oracloud,
    # misc
    'computer science': terms.compsci,
    'compsci': terms.compsci,
    'comp sci': terms.compsci,
    'cs': terms.compsci,
    'batchelor': terms.bachelor,
    'bachelor': terms.bachelor,
    'bs': terms.bachelor,
    'bachelor degree': terms.bachelor,
    'bachelors degree': terms.bachelor,
    'baccalaureate': terms.bachelor,
    'masters': terms.master,
    'ms': terms.master,
    'master degree': terms.master,
    'masters degree': terms.master,
    'restful api': terms.restAPI,
    'rest api': terms.restAPI,
    'restful': terms.restAPI,
    'rest': terms.restAPI,
    'oop': terms.oop,
    'object-oriented': terms.oop,
    'object-oriented-programming': terms.oop,
    'object oriented': terms.oop,
    'object oriented programming': terms.oop,
    'frontend': terms.frontend,
    'front-end': terms.frontend,
    'front end': terms.frontend,
    'backend': terms.backend,
    'back-end': terms.backend,
    'back end': terms.backend,
    'full stack': terms.fullstack,
    'full-stack': terms.fullstack,
    'fullstack': terms.fullstack,
    'api': terms.api,
    'apis': terms.api,
    'nlp': terms.nlp,
    'natural language processing': terms.nlp,
    'ux': terms.ux,
    'ui/ux': terms.ux,
    'ml': terms.ml,
    'machine learning': terms.ml,
    'large language model': terms.llm,
    'llm': terms.llm,
    'ai': terms.ai,
    'artificial intelligence': terms.ai,
    'vs': terms.visualstudio,
    'vs code': terms.visualstudio,
    'visual studio': terms.visualstudio,
    'ios': terms.ios,
    'mongodb': terms.mongodb,
    'mongo db': terms.mongodb,
    'microservice': terms.microservices,
    'microservices': terms.microservices,
    'micro-services': terms.microservices,
    'micro-service': terms.microservices,
    'css': terms.css,
    'css3': terms.css,
    'html': terms.html,
    'html5': terms.html,
    'container': terms.container,
    'containerization': terms.container,
    'containerisation': terms.container,
    'ci cd': terms.cicd,
    'ci/cd': terms.cicd,
    'ci': terms.cicd,
    'cd': terms.cicd,
    'continuous deployment': terms.cicd,
    'internet of things': terms.iot,
    'iot': terms.iot,
    'git': terms.git
}

def format_term(word: str):
    'Format a term to its preferred form'
    word = word.lower()

    if word in CONFLATE:
        return CONFLATE[word]
    
    # detect JS libraries and format them as Name.js
    if len(word) > 4 and word[-2:] == "js":
        return format_js(word)

    # make abbreviations all caps
    if len(word) <= 3:
        return word.upper()
    # make regular words capitalized
    return word.capitalize()

def format_js(word: str):
    # remove periods if they exist
    word = word.replace(".", "")
    name = word[:-2].capitalize()
    return "{}.js".format(name)