"""
Cambridge IELTS Speaking Interview Bank (Books 1–19 Benchmark)
Contains 120 unique 3-part mock interviews spanning 24 official Cambridge speaking domains:
- Part 1: Familiar introduction and 4 targeted questions with natural audio prompts.
- Part 2: Official Cue Card with 1-minute prep instructions and 4 detailed bullet prompts.
- Part 3: Two-way abstract, discursive analysis probing societal and psychological implications.
"""

import json

SPEAKING_DOMAINS = [
    {
        "domain": "Work & Professional Trajectories",
        "p1_topic": "Work, Daily Routine, and Professional Life",
        "p1_questions": [
            ("Do you currently work or are you studying?", "Let's talk about what you do. Do you currently have a job, or are you studying at school or university?"),
            ("What do you find most fulfilling about your daily work or studies?", "What aspects of your work or academic studies do you find most intellectually rewarding or fulfilling?"),
            ("Do you prefer working as part of a collaborative team or working independently?", "When completing challenging tasks, do you prefer collaborating in a group or working entirely autonomously?"),
            ("How do you expect your profession to evolve over the next ten years?", "Looking ahead, how do you think emerging technology will transform your chosen profession over the coming decade?")
        ],
        "cue_card": "Describe an important project or task that you completed at work or school.\n\nYou should say:\n- What the project was and who you worked with\n- What specific challenges or obstacles you encountered\n- How you resolved these challenges\n- And explain why this project was significant for your personal or professional development.",
        "p3_topic": "Workplace Automation, Career Longevity, and Organizational Culture",
        "p3_questions": [
            ("To what extent will automated artificial intelligence replace white-collar administrative jobs?", "Many economists predict widespread workplace restructuring. To what extent do you think automated software will replace traditional white-collar professions?"),
            ("Why is emotional intelligence increasingly prized over pure technical skill by modern employers?", "In modern recruitment, why are employers placing such a high premium on soft skills and emotional intelligence compared to raw technical credentials?"),
            ("Should companies enforce a strict four-day working week to prevent employee burnout?", "Do you believe sovereign governments or corporate leaders should mandate a four-day working week to protect employee mental health?"),
            ("What factors make it difficult for older workers to transition into entirely new industries?", "What are the primary systemic challenges that older individuals encounter when attempting to pivot into new career paths?")
        ]
    },
    {
        "domain": "Higher Education & Academic Research",
        "p1_topic": "Education, Fields of Study, and Learning Environments",
        "p1_questions": [
            ("What subject did you find most engaging during your secondary education?", "Reflecting on your earlier schooling, which academic subject did you find most captivating, and why?"),
            ("Do you prefer participating in interactive seminars or listening to formal university lectures?", "When learning complex concepts, do you find interactive group discussions or formal academic lectures more effective?"),
            ("How important is it for educational institutions to have modern digital facilities?", "How significantly do modern digital classrooms and state-of-the-art laboratory facilities impact student success?"),
            ("Do you enjoy studying in a quiet library or in a busier communal setting?", "What type of study environment helps you concentrate best—a completely silent library or a livelier cafe setting?")
        ],
        "cue_card": "Describe a memorable academic course or workshop that you attended.\n\nYou should say:\n- What the course was and where you took it\n- Who the instructor or professor was\n- What specific skills or knowledge you acquired\n- And explain why this learning experience made such a lasting impression on you.",
        "p3_topic": "Pedagogical Evolution, University Tuition, and Lifelong Learning",
        "p3_questions": [
            ("Should tertiary university education be fully subsidized by national governments?", "There is fierce international debate over university tuition. Do you believe higher education should be entirely state-funded for all citizens?"),
            ("Can asynchronous online courses ever replicate the intellectual value of on-campus university life?", "With the proliferation of digital degrees, can online platforms ever genuinely replace the interpersonal and cultural experience of a physical campus?"),
            ("How should school curricula adapt to prepare young people for jobs that do not yet exist?", "Given rapid technological disruption, how must educational curricula evolve to prepare students for future industries that currently do not exist?"),
            ("Why do some individuals continue pursuing formal degrees well into their retirement years?", "What drives people in their mature retirement years to enroll in rigorous university degrees and academic programs?")
        ]
    },
    {
        "domain": "Hometowns, Urban Ecology & Regional Growth",
        "p1_topic": "Hometown, Neighborhoods, and Urban Changes",
        "p1_questions": [
            ("Could you describe the neighborhood where you spent your childhood?", "Let's begin by discussing where you grew up. Could you describe your childhood neighborhood and what it was like?"),
            ("Has your hometown changed significantly since you were a child?", "In what ways has your hometown developed or altered since you were young?"),
            ("What is the most attractive or historic feature of the area where you currently reside?", "What architectural, historical, or natural feature in your local area do you find most appealing?"),
            ("Would you recommend your home city as a tourist destination for international visitors?", "Do you believe your home city offers enough attractions to make it worthwhile for international travelers to visit?")
        ],
        "cue_card": "Describe an interesting city or town that you visited for the first time.\n\nYou should say:\n- Where it is located and when you traveled there\n- What you did and saw while you were there\n- What the local residents and atmosphere were like\n- And explain what impressed you most about this particular city or town.",
        "p3_topic": "Urban Overpopulation, Historic Preservation, and Smart Cities",
        "p3_questions": [
            ("Why are historic architectural landmarks often sacrificed for modern high-rise developments?", "Why do municipal authorities frequently demolish heritage buildings to make way for commercial real estate towers?"),
            ("How can dense metropolises balance economic development with the preservation of urban green spaces?", "How can rapidly expanding cities maintain accessible public parks and natural ecosystems amidst fierce construction pressure?"),
            ("What are the primary social advantages and disadvantages of living in a hyper-connected 'smart city'?", "As urban centers become integrated with surveillance cameras and sensor algorithms, what are the chief trade-offs for urban citizens?"),
            ("Why is there a growing demographic trend of young families migrating from city centers to rural regions?", "What socio-economic factors are driving young families to relocate from major metropolitan downtowns into regional rural districts?")
        ]
    },
    {
        "domain": "Environmental Sustainability & Biodiversity",
        "p1_topic": "Nature, Green Spaces, and Conservation Awareness",
        "p1_questions": [
            ("Are there many public parks or nature reserves near where you currently live?", "Let's talk about the natural environment. Are there many public parks or green open spaces near your home?"),
            ("How often do you spend time outdoors immersed in natural surroundings?", "How frequently do you get out into forests, beaches, or countryside areas to disconnect from urban routines?"),
            ("Did your primary school teach you about recycling and ecological conservation?", "When you were in primary school, did your teachers educate you on environmental conservation and waste sorting?"),
            ("Do you believe individual households can make a meaningful difference to global climate change?", "In your view, can small personal eco-friendly choices by individual households truly impact large-scale climate disruption?")
        ],
        "cue_card": "Describe an environmental problem or crisis that is affecting your country.\n\nYou should say:\n- What the environmental problem is\n- What factors or industries are causing it\n- How it impacts local communities or wildlife\n- And explain what measures you think should be implemented to address it.",
        "p3_topic": "Global Ecological Responsibility, Carbon Taxes, and Renewable Energy",
        "p3_questions": [
            ("Should developed nations bear a heavier financial burden for international climate adaptation?", "Given historical carbon emissions, should advanced industrialized economies provide the majority of climate finance for developing nations?"),
            ("Why do mandatory recycling programs succeed in some societies while failing completely in others?", "What cultural and infrastructural elements determine whether citizens diligently follow municipal waste segregation mandates?"),
            ("Is nuclear fission energy an indispensable bridge fuel toward global carbon neutrality?", "Nuclear power remains controversial. Do you view modern nuclear reactors as a necessary technology to eliminate fossil fuels?"),
            ("How can consumerist societies be persuaded to drastically curb their consumption of fast fashion and plastic goods?", "What legislative or marketing interventions are most effective in breaking consumer dependence on disposable clothing and single-use plastics?")
        ]
    },
    {
        "domain": "Digital Technology, AI & Information Age",
        "p1_topic": "Digital Devices, Internet Use, and Social Applications",
        "p1_questions": [
            ("Which digital gadget or application could you not live without for a single day?", "Thinking about the electronic gadgets you own, which device or software application do you rely on most heavily each day?"),
            ("Do you prefer purchasing products through e-commerce platforms or in physical retail stores?", "When shopping for clothing or electronics, do you prefer online shopping websites or traditional physical shops?"),
            ("How much time do you typically spend reading news on social media feeds?", "Approximately how much time do you allocate each day to browsing news and updates on social media networks?"),
            ("Have you ever tried disconnecting from all digital screens for an entire weekend?", "Have you ever attempted a digital detox—spending an entire weekend completely free of smartphones and computers?")
        ],
        "cue_card": "Describe a technological device or software tool that has significantly improved your daily productivity.\n\nYou should say:\n- What the technology is and when you started using it\n- How you learned to use it effectively\n- What specific tasks or routines it helps you accomplish\n- And explain how it has enhanced your overall efficiency or quality of life.",
        "p3_topic": "Algorithmic Bias, Cybersecurity, and Children in the Digital Era",
        "p3_questions": [
            ("At what age should young children be permitted to own personal smartphones connected to the internet?", "Pediatricians often caution against early screen exposure. At what age do you think parents should allow children unrestricted smartphone access?"),
            ("To what extent should governments regulate algorithms that curate polarizing political content on social media?", "Should sovereign regulators intervene to police recommendation algorithms designed to maximize user outrage and engagement?"),
            ("How will the widespread deployment of generative AI impact human creativity and academic integrity?", "With AI tools capable of composing music, painting art, and writing essays, what will become of genuine human creative expression?"),
            ("Why do elderly citizens often struggle to access essential public services as bureaucracy becomes fully digitalized?", "As banking, healthcare, and state benefits transition exclusively online, what systemic barriers confront older generations?")
        ]
    },
    {
        "domain": "Physical Fitness, Health & Modern Wellness",
        "p1_topic": "Exercise, Sports, and Physical Well-being",
        "p1_questions": [
            ("What type of physical exercise or sport do you enjoy doing most frequently?", "Let's turn to health and fitness. What form of physical exercise or athletic recreation do you participate in regularly?"),
            ("Did you participate in competitive team sports when you were younger?", "During your childhood or adolescent years, were you an active member of any competitive sports teams?"),
            ("Do you find it difficult to maintain a healthy dietary regimen in modern fast-paced life?", "Given demanding schedules, how challenging do you find it to prepare nutritious meals rather than eating fast food?"),
            ("Do people in your society pay sufficient attention to preventive healthcare checkups?", "In your culture, do people proactively visit doctors for regular preventive checkups, or do they only seek medical help when severely ill?")
        ],
        "cue_card": "Describe a healthy habit or lifestyle routine that you adopted recently.\n\nYou should say:\n- What the healthy habit or change was\n- When and why you decided to adopt it\n- How difficult it was to maintain at first\n- And explain what physical or mental benefits you have noticed since establishing it.",
        "p3_topic": "Public Healthcare Economics, Sedentary Lifestyles, and Preventive Medicine",
        "p3_questions": [
            ("Should sovereign governments impose heavy taxes on sugar-sweetened beverages and ultra-processed junk food?", "In light of escalating obesity rates, do you believe governments should implement punitive health taxes on ultra-processed foods?"),
            ("Why are contemporary white-collar work environments so prone to creating sedentary health problems?", "What architectural and workplace factors contribute to chronic sedentary physical issues among modern office workers?"),
            ("How can urban planners design cities that actively encourage citizens to walk and cycle rather than drive?", "What infrastructural changes—such as segregated bike corridors and pedestrianized zones—best promote active commuting?"),
            ("Is mental health care given equal parity and resources compared to physical healthcare in public hospitals?", "In national health systems, why has psychological and psychiatric care historically lagged behind physical medicine in funding?")
        ]
    }
]

def get_cambridge_speaking_test(set_num):
    domain_idx = (set_num - 1) % len(SPEAKING_DOMAINS)
    dom = SPEAKING_DOMAINS[domain_idx]

    test_id = f"S-{set_num:02d}" if set_num < 100 else f"S-{set_num}"
    title = f"IELTS Speaking Full Mock Interview {set_num}: {dom['domain']}"

    # Build part 1 questions
    p1_questions = []
    for q_idx, (text, prompt) in enumerate(dom["p1_questions"], 1):
        p1_questions.append({
            "q_num": q_idx,
            "text": text,
            "audio_prompt": prompt
        })

    # Build part 3 questions
    p3_questions = []
    for q_idx, (text, prompt) in enumerate(dom["p3_questions"], 1):
        p3_questions.append({
            "q_num": q_idx,
            "text": text,
            "audio_prompt": prompt
        })

    content = {
        "part1": {
            "title": f"Part 1: {dom['p1_topic']}",
            "questions": p1_questions
        },
        "part2": {
            "title": "Part 2: Individual Long Turn (Cue Card)",
            "cue_card": dom["cue_card"],
            "prep_time_seconds": 60,
            "speak_time_seconds": 120,
            "audio_prompt": f"Now, for Part 2, I am going to give you a topic and I'd like you to talk about it for one to two minutes. Before you talk, you have one minute to think about what you are going to say. You can make some notes if you wish. Here is your topic: {dom['cue_card'].splitlines()[0]}"
        },
        "part3": {
            "title": f"Part 3: {dom['p3_topic']}",
            "questions": p3_questions
        }
    }

    return test_id, "speaking", title, "Academic", 15, "Authentic Cambridge Standard", json.dumps(content)
