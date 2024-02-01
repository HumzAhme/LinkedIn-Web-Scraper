from terms import format_term
from engine import run_engine

cases = [
    [
        "Familiarity with cloud infrastructure (AWS, GCP, etc.).",
        ["AWS", "GCP", "cloud"]
    ],
    [
        "Experience with Front-End technologies (React, etc.) and GraphQL.",
        ["Frontend", "React", "GraphQL"]
    ],
    [
        "Knowledge of other programming languages (Go, Rust, Python, etc.).",
        ["Go", "Rust", "Python"]
    ],
    [
        "A minimum of 3 years of experience in Back-End application development using Ruby and Ruby on Rails (or Go/Python/Rust).",
        ["Backend", "Ruby", "Ruby on Rails", "Go", "Python", "Rust"]
    ],
    [
        "Good JavaScript knowledge as well as other web technologies",
        ["Javascript"]
    ],
    [
        "Knowledge of at least one backend programming language, such as Go or Scala.",
        ["Backend", "Go", "Scala"]
    ],
    [
        "Assist in designing a scalable cloud offering to work across everything from a few Elasticsearch clusters and Kibana instances to many thousands",
        ["cloud", "ElasticSearch", "Kibana"]
    ],
    [
        "Use your frontend expertise to help design clear and simple APIs",
        ["Frontend", "API"]
    ],
    [
        "Knowledge of and experience with database (RDBMS, NoSQL), network, Linux server, surveillance system, logging, SLA, SLO, and system operation",
        ["RDBMS", "NoSQL", "Linux", "SLA", "SLO"]
    ],
    [
        "Backend: Design, development, and operation of APIs using Go, PHP, or Java",
        ["Backend", "API", "Go", "PHP", "Java"]
    ],
    [
        "Frontend: Development related to frontend fields such as web browsers, JavaScript, TypeScript, React.js, Next.js, or Redux",
        ["Frontend", "Javascript", "Typescript", "React", "Next.js", "Redux"]
    ],
    [
        "Mobile: Development using Swift or Kotlin for iOS and Android",
        ["Mobile", "Swift", "Kotlin", "iOS", "Android"]
    ],
    [
        "Data Platform: Development using distributed processing frameworks (Dataflow/Spark/Kafka/Flink, etc.) and knowledge of data schemas represented by Avro and Protocol Buffers, along with file formats (Parquet/ORC, etc.)",
        ["Dataflow", "Spark", "Kafka", "Flink", "Avro", "Parquet", "ORC"]
    ],
    [
        "Familiar with front end JavaScript web technologies such as ReactJS, NextJS or AngularJS",
        ["Frontend", "Javascript", "React", "Next.js", "Angular"]
    ],
    [
        "Experience with MongoDB, Rest API, JavaScript/Typescript, CSS and HTML5.",
        ["MongoDB", "REST API", "Javascript", "Typescript", "CSS", "HTML"]
    ],
    [
        "Strong coding and testing skills in any Object Oriented Programming Language (Java, Javascript, Kotlin, PHP)",
        ["OOP", "Java", "Javascript", "Kotlin", "PHP"]
    ],
    [
        "Experienced with CI/CD systems and can develop basic build/test pipelines",
        ["CI/CD"]
    ],
    [
        "In this role you will need to be proficient in at least one programming language (Python, JavaScript, HTML, C++, C# and SQL) and able to solve coding problems (think LeetCode, HackerRank, etc).",
        ["Python", "Javascript", "HTML", "C++", "C#", "SQL", "LeetCode", "HackerRank"]
    ],
    [
        "5+ Years of experience building and delivering cloud based services and applications in a CI/CD environment via containerization technologies including Docker and Kubernetes",
        ["cloud", "ci/cd", "container", "docker", "kubernetes"]
    ],
    [
        "Familiarity with backing stores and databases including both SQL/NoSQL such as Postgres and Redis",
        ["SQL", "NoSQL", "Postgres", "Redis"]
    ],
    [
        "History of delivering products built on multiple frameworks such as Express or Django.",
        ["Express", "Django"]
    ],
    [
        "Eagle Eye Networks is leveraging artificial intelligence on its true cloud platform to dramatically reshape the video surveillance and security industry.",
        ["artificial intelligence", "cloud", "security"]
    ],
    [
        "Enhance our backend technology stack using modern tools: ReactJS/React Native, NodeJS, Kubernetes, GCP, MongoDB, Docker.",
        ["backend", "React", "React native", "node.js", "kubernetes", "gcp", "MongoDB", "Docker"]
    ],
    [
        "Experience setting up automation infrastructure using CI tools (ex. GitHub Actions, GitLab CI)",
        ["automation", "CI/CD", "Github", "Gitlab"]
    ],
    [
        "Build machine learning models using deep neural networks and use AI to classify queries, generate ad copies or construct ad keywords.",
        ["machine learning", "neural network", "artificial intelligence"]
    ],
    [
        "Our tech stack ranges from Java, Python, MySQL, React.js, Node.js, web services, Docker, Hadoop, Splunk, monitoring tools to Tensorflow, Keras, and statistical analysis tools.",
        ["Java", "Python", "SQL", "React", "node.js", "Docker", "Hadoop", "Splunk", "Tensorflow", "Keras"]
    ],
    [
        "MS Degree in Computer Science, information technologies or a closely related field. Experience of microservice development with REST and API development, Knowledge of YAML to build models",
        ["Masters degree", "Computer science", "microservice", "REST API", "API", "YAML"]
    ],
    [
        "Experience of data analysis and/or visualization with Python, R, MATLAB, BI tools or other similar tools",
        ["visualization", "python", "R", "Matlab", "BI"]
    ],
    [
        "As part of the engineering team, you will be responsible for building and maintaining our NextJS shopify storefront and NestJS backend.",
        ["Next.js", "shopify", "nestjs", "backend"]
    ],
    [
        "Infrastructure : AWS(App Runner, EC2, ECS, Lambda, S3, Aurora, RDS, etc.).",
        ["AWS", "App Runner", "EC2", "ECS", "Lambda", "S3", "Aurora", "RDS"]
    ],
    [
        "Others : GitHub Actions, Docker, Terraform, Serverless Framework, etc.",
        ["github", "docker", "terraform", "serverless"]
    ],
    [
        "3+ years of development experiences with Java and Spring or Springboot",
        ["Java", "Spring", "Spring Boot"]
    ],
    [
        "You will be able to create Proof Of Concept using high level languages such as Python, and rewrite those PoC in C/C++ to integrate the main product codebase.",
        ["Python", "C", "C++"]
    ],
    [
        "Proficiency in Containerization technologies (i.e Docker) and Version Control (i.e Git) for easy team collaboration.",
        ["container", "Docker", "Git"]
    ],
    [
        "3+ years of experience creating/maintaining and executing automation tests utilizing tools such as Selenium required (Python essential).",
        ["automation", "Selenium", "Python"]
    ],
    [
        "The Software Engineer will be responsible for developing and maintaining software applications, configuring existing systems and services, and integrating third-party solutions.",
        []
    ],
    [
        "Work with our UI designer and CEO to create new engaging features for our customers.",
        []
    ],
    [
        "They offer solutions for corporate contact centers and local governments that cover a wide range of support areas, from chat to telephone.",
        []
    ],
    [
        "we aim to achieve this goal through the development of core technologies that enable real-time teleportation of human presence and skills through robots and other mobility solutions.",
        []
    ],
    [
        "We are looking for an engineer who is a good communicator and is dedicated to solving people's problems.",
        []
    ],
    [
        "Being one of the largest e-commerce platforms in the world, the group has almost 100 million customers based in Japan and 1 billion globally as well, providing more than 70 services in a variety such as media, sports, telecommunication, e-commerce, payment services, financial services, etc.",
        []
    ]
]

class colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

def printColor(color: str, *args):
    print(color, *args, colors.RESET)

def judgeAccuracy(mode = 3):
    totalScore = 0
    outOf = 0
    extraTermCount = 0
    extraTerms = set()
    i = 1
    for case in cases:
        score = 0

        sentence = case[0]
        expOut = [format_term(term) for term in case[1]]

        outOf += len(expOut)

        out = run_engine(mode, sentence)

        # judge accuracy of the output
        passTest = True
        if (len(expOut) == 0) and (len(out) > 0):
            passTest = False
        for term in expOut:
            if term in out:
                score += 1
            else:
                passTest = False
        
        if not passTest:
            printColor(colors.RED, "(X) Failed case {}".format(i))
            print("Input: {}".format(sentence))
            print("Output:", out)
            print("ExpOut:", expOut)
            printColor(colors.YELLOW, "Missing:", [word for word in expOut if word not in out], "\n")
            if len(expOut) == 0:
                printColor(colors.YELLOW, "Expected no output")
        
        # see if extra terms were in the output
        if len(out) > len(expOut):
            extra = [word for word in out if word not in expOut]
            extraTermCount += len(extra)
            extraTerms = extraTerms.union(set(extra))
        
        totalScore += score
        i += 1
    
    accuracy = round(totalScore / outOf * 100)
    color = colors.GREEN if accuracy >= 80 else colors.YELLOW if accuracy >= 50 else colors.RED
    printColor(colors.CYAN, "Total tests run: {}".format(len(cases)))
    printColor(color, "Average accuracy: {}%".format(accuracy))
    printColor(colors.CYAN, "Average number of extra terms per case: {}".format(round(extraTermCount / len(cases) * 100) / 100))
    print(extraTerms)

def judgeAccuracyNltk(): judgeAccuracy(mode=1)
def judgeAccuracySpacy(): judgeAccuracy(mode=2)

def testEngine(n, spacy = False):
    n = n-1
    sentence = cases[n][0]
    expOut = cases[n][1]

    out = set()
    if spacy:
        print("(spacy engine)")
        out = run_engine(2, sentence)
    else:
        print("(nltk engine)")
        out = run_engine(1, sentence)

    score = 0

    # judge accuracy of the output
    for term in expOut:
        term = format_term(term)
        if term in out:
            score += 1
    print("Input:", sentence)
    print("Output:", out)
    print("Expected:", expOut)
    print("score: {}/{}".format(score, len(expOut)))
    if len(out) > len(expOut):
        print("extra terms:", len(out) - len(expOut))

def testSpacy(n): testEngine(n, True)

def testNltk(n): testEngine(n, False)

judgeAccuracy()
#testNltk(4)
#testSpacy(30)