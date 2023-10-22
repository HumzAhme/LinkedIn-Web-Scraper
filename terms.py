
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
    'join','level','review','content','builder','detail','liaise','evaluating','make','~','’'
}

# words that you don't want to gather stats on, especially if they are just stand-alone and aren't paired with something specific.
# for example, maybe you want to watch for the specific term "data analysis", but "data" itself isn't interesting. 
# you can add "data", and "analysis" here (and add "data analysis" to PHRASES)
IGNORE = {
    'ability', 'advantage', 'agreement', 'agreements', 'alternatives', 'application', 'applications', 'apps', 'aptitude', 'attention', 
    'bachelor', 'building', 
    'challenge', 'challenges', 'clean', 'client', 'code', 'coding', 'collaborate', 'colleagues', 'communication', 'communities', 'company', 
    'compliance', 'components', 'conduct', 'considerations', 'constructive', 'contribute', 'cooperate', 'create', 'culture', 
    'custom', 'customers', 'cutting-edge', 
    'deliver', 'delivery', 'design', 'designers', 'developer', 'development', 'documentation', 'documents', 'drive', 
    'e.g', 'efficiency', 'efficient', 'end', 'end-to-end', 'engineer', 'engineering', 'engineers', 'enhance', 'enhancement', 'enhancements', 
    'environment', 'environments', 'evaluate', 'evaluations', 'exceptional', 'experience', 'experiences', 'expertise', 
    'familiarity', 'fault', 'features', 'feedback', 'field', 'frameworks', 'functionality', 
    'gathering', 'guide', 
    'high-quality', 
    'ideal', 'implement', 'improvement', 'improvements', 'infrastructure', 'inputs', 'insights', 'integration', 'interface', 'issues', 
    'job', 'jpy', 
    'knowledge', 
    'language', 'languages', 'leadership', 'level', 'lifecycle', 'location', 'love', 
    'maintain', 'maintainability', 'manage', 'management', 'manner', 'markup', 'master', 'members', 'middleware', 'mind', 
    'networker', 
    'offer', 'operating', 'optimal', 'optimise', 'optimize', 'organizational', 
    'packages', 'page', 'part', 'party', 'past', 'patterns', 'pay', 'performance', 'performant', 'platform', 'platforms', 'plus', 'portfolio', 
    'position', 'possess', 'practice', 'practices', 'preferences', 'product', 'production', 'products', 'proficiency', 'proficient', 'programing', 
    'programming', 'project', 'projects', 'provide', 
    'quality', 
    'range', 'readability', 'region', 'relationship', 'repositories', 'requests', 'requirement', 'reviews', 'role', 'runs', 
    'salary', 'scratch', 'secure', 'server', 'service', 'site', 'skills', 'soap', 'software', 'solutions', 'specialities', 
    'specialization', 'speed', 'stakeholders', 'standard', 'standards', 'support', 'system', 'systems', 
    'team', 'teams', 'tech', 'technologies', 'technology', 'test', 'testability', 'tickets', 'tolerant', 'tools', 'translation', 'troubleshoot', 
    'understanding', 'university', 'updates', 'usability', 'user', 'verbal', 'version', 'website', 'winning', 'work', 'year', 'years',
    'troubleshooting', 'degree', 'style', 'stack', 'problem-solving', 'debugging', 'providing', 'architectural', 'high-performance', 'framework', 
    'participate', 'seamless', 'build', 'workflow', 'diploma', 'identify', 'ticketing', 'training', 'relevant', 'prior', 'reliability', 
    'professional', 'down', 'practical', 'good', 'debug', 'fellow', 'proven', 'testing', 'pipeline', 'real-time', 'excellent', 'in-depth', 
    'hands-on', 'adeptness', 'managers', 'source', 'libraries', 'days', 'leave', 'care', 'holiday', 'week', 'saturday', 'nursing', 'sunday', 
    'holidays', 'in-house', 'interest', 'anticipation', 'people', 'hr', 'ideas', 'screening', 'online', 'cv', 'interviews', 'regress', 'proponent', 
    'isolate', 'area', 'develop', 'output', 'attitude', 'proposals', 'problems', 'solution', 'concepts', 'learn', 'requirements', 'zone', 'expert', 
    'comfort', 'abstraction', 'workflows', 'business', 'scalability','monitoring','industry','implementation','specifications','balance','diverse',
    'staff','operations','opportunity','customer','users','partners','processes',
}

# tech words we want to make sure aren't ignored or stripped by NLTK logic by accident
# our logic ideally allows any noun-like terms (that aren't stop words/ignored) to go through
# but sometimes weird things happen, so just to be safe I am listing popular terms or ones that may potentially be erroneously ignored.
SAVE_WORDS = {
    'react','react.js','assembly','git','cloud','angular','angular.js','c#','c++','mobile','android','ios','oop','object-oriented',
    'node','node.js','restful','go','golang','.net','linux','unix','macos','windows','web3','github','nosql','mysql','sql','aws','gcp',
    'bash','kernel','material-ui','mui','vuetify'
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
    "batchelors degree",
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
    'google cloud platform',
    'amazon web service',
    'rest api',
    'restful api',
    'system engineer',
    'natural language processing',
    'visual studio',
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

# terms to conflate into a singular preferred form
# since there are many ways a given concept may be written, we conform
# them all using this dictionary
CONFLATE = {
    # javascript/typescript
    'js': javascript,
    'ts': typescript,
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
    # misc
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
}