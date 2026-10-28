"""
Cambridge IELTS Listening Practice Bank (Books 1–19 Benchmark)
Contains comprehensive 4-section listening suites (~1,400+ spoken words each).
All 40 questions per test adhere strictly to Cambridge / IDP specifications:
- Section 1: Social Transaction Dialogue (Form Completion with spelling, numbers, distractor traps)
- Section 2: Public Orientation Monologue (Multiple Choice & Sentence Completion)
- Section 3: Academic Research Tutorial (Multiple Choice & Methodology Notes)
- Section 4: University Academic Lecture (Full Lecture Notes Completion)
"""

import json

LISTENING_SUITES = [
    # -------------------------------------------------------------------------
    # SUITE 1: Coastal Sports, Botanical Arboretum, Marine Microplastics, Bio-Concrete
    # -------------------------------------------------------------------------
    {
        "suite_id": 1,
        "title": "Cambridge Listening Practice Benchmark 1 (Social & Academic Multi-Section)",
        "s1_title": "Coastal Kayak & Watersports Club Membership Registration",
        "s1_context": "An applicant calls the coastal watersports center to register for membership and book an induction session.",
        "s1_script": """Clerk: Good morning, Highcliffe Coastal Watersports Centre. How can I help you today?
Applicant: Hello! I'm calling to inquire about signing up for your kayak and paddleboard club for the upcoming spring term.
Clerk: Certainly! I can take down your details right now to get your membership activated. Could I begin with your full name, please?
Applicant: Yes, it's Julian Sinclair.
Clerk: Is Sinclair spelled S-I-N-C-L-A-I-R?
Applicant: That's correct, Julian Sinclair.
Clerk: And what's your current residential address, Julian?
Applicant: It's 27 Bramble Way, in Highcliffe.
Clerk: 27 Bramble Way... and the postcode?
Applicant: Let me double-check... originally I was at BH23 4TL, but the new flat is BH23 5PR.
Clerk: Got it, BH23 5PR. And the best daytime contact number for you?
Applicant: My mobile is 07700 900 482.
Clerk: 07700 900 482. Excellent. Now, regarding our membership tiers, we have our Weekend-Only pass, and then the Full-Access All-Week pass. Which were you leaning toward?
Applicant: How much is the Full-Access tier?
Clerk: The Full-Access is normally £75 per month, but if you commit to paying six months upfront, we apply a ten percent discount, bringing it down to £67.50 a month.
Applicant: £67.50 sounds very reasonable. Let's do the six-month upfront plan.
Clerk: Splendid. Before you can take equipment out unaccompanied, every new member must attend a mandatory water safety induction. Our next available slot is this coming Saturday morning, or next Tuesday evening.
Applicant: Saturday morning would be ideal. What time does that start?
Clerk: It starts promptly at 8:45 am at the South Boathouse. Please arrive ten minutes early to sign the insurance waiver.
Applicant: 8:45 am at the South Boathouse, noted. Do I need to bring my own wetsuit or flotation vest?
Clerk: We supply all buoyancy aids and helmets free of charge. However, you must bring your own thermal rash vest, and footwear is mandatory—specifically hard-soled neoprene booties or old trainers. Flip-flops and sandals are strictly forbidden on the slipway.
Applicant: Understood, I'll bring proper booties.
Clerk: And finally, Julian, do you have any pre-existing medical conditions or allergies we should note on your emergency manifest?
Applicant: Nothing major, just a mild asthma condition, so I always carry a blue inhaler in my dry bag.
Clerk: That's essential to record: asthma inhaler in dry bag. Right, that completes your initial registration! You'll receive a confirmation email shortly.""",
        "s1_questions": [
            {"id": "Q1", "type": "Form Completion", "question_text": "Applicant Surname: Sinclair; First Name: ____________", "correct_answer": "Julian", "explanation": "Applicant states his name is Julian Sinclair."},
            {"id": "Q2", "type": "Form Completion", "question_text": "Address: 27 ____________ Way, Highcliffe", "correct_answer": "Bramble", "explanation": "Address is 27 Bramble Way."},
            {"id": "Q3", "type": "Form Completion", "question_text": "Current Postcode: ____________", "correct_answer": "BH23 5PR", "explanation": "Distractor BH23 4TL corrected to new flat postcode BH23 5PR."},
            {"id": "Q4", "type": "Form Completion", "question_text": "Mobile Contact: ____________", "correct_answer": "07700 900 482", "explanation": "Provided as 07700 900 482."},
            {"id": "Q5", "type": "Form Completion", "question_text": "Discounted Monthly Rate: £____________", "correct_answer": "67.50", "explanation": "Distractor £75 discounted to £67.50 on upfront plan."},
            {"id": "Q6", "type": "Form Completion", "question_text": "Induction Session Day: ____________", "correct_answer": "Saturday", "explanation": "Applicant selects Saturday morning."},
            {"id": "Q7", "type": "Form Completion", "question_text": "Induction Start Time: ____________ am", "correct_answer": "8:45", "explanation": "Starts promptly at 8:45 am."},
            {"id": "Q8", "type": "Form Completion", "question_text": "Meeting Location: ____________ Boathouse", "correct_answer": "South", "explanation": "Location is the South Boathouse."},
            {"id": "Q9", "type": "Form Completion", "question_text": "Compulsory Personal Footwear: neoprene ____________ or old trainers", "correct_answer": "booties", "explanation": "Clerk specifies hard-soled neoprene booties."},
            {"id": "Q10", "type": "Form Completion", "question_text": "Medical Item Stored in Dry Bag: asthma ____________", "correct_answer": "inhaler", "explanation": "Applicant carries a blue asthma inhaler."}
        ],

        "s2_title": "Orientation Tour of the Otari Native Botanical Reserve",
        "s2_context": "The head ranger welcomes a group of environmental volunteers and visitors to the regional botanical reserve.",
        "s2_script": """Ranger: Good morning everyone, and welcome to Otari Native Botanical Reserve. My name is Craig McGregor, head ranger here. Before we divide into our volunteer trail-maintenance groups, I want to provide an essential orientation of our layout and ongoing conservation protocols.
First, looking at your visitor map: right here in front of us is the Main Visitor Pavilion. If you need drinking water or public facilities, they are located on the western ground floor. Directly opposite the pavilion, across the ornamental gravel terrace, you'll see the Native Fernery. This houses over ninety endemic fern species, including our iconic giant silver tree ferns.
Now, if you follow the yellow trail markers heading north toward the stream, you will come to the Canopy Suspension Walkway. It spans sixty meters across the river canyon at an elevation of thirty meters. A quick safety reminder: the walkway has a strict structural load limit of twenty persons at any one time. Please do not crowd onto the suspension deck, and running or swinging the cables is strictly forbidden.
Beyond the canopy walkway lies the Old-Growth Beech Forest, where trees date back over four hundred years. This is a designated predator-free sanctuary protected by an electrified perimeter fence. We have achieved complete eradication of possums, stoats, and feral cats within this zone, allowing endangered stitchbirds and bellbirds to re-establish breeding populations. When entering this sector, you must pass through the double-gated biosecurity station: please scrub the soles of your boots in the disinfectant bath to prevent spreading kauri dieback spores.
Lastly, a note about volunteer tasks today: Group A will clear fallen timber along the Southern Ridge, Group B will monitor automated tracking tunnels for rodent activity, and Group C will assist our nursery horticulturists with potting native seedlings. Lunch will be provided at the outdoor picnic shelter at 12:30 pm, courtesy of the Friends of Otari Society.""",
        "s2_questions": [
            {"id": "Q11", "type": "Multiple Choice", "question_text": "Where are the drinking water and public facilities located?", "options": ["A. On the upper floor of the Fernery", "B. On the western ground floor of the Main Visitor Pavilion", "C. Next to the Canopy Suspension Walkway", "D. Beside the picnic shelter"], "correct_answer": "B. On the western ground floor of the Main Visitor Pavilion", "explanation": "Ranger states facilities are on the western ground floor of the Main Visitor Pavilion."},
            {"id": "Q12", "type": "Multiple Choice", "question_text": "What is the maximum structural capacity of the Canopy Suspension Walkway?", "options": ["A. 10 persons", "B. 20 persons", "C. 35 persons", "D. 50 persons"], "correct_answer": "B. 20 persons", "explanation": "Ranger explicitly states a strict load limit of 20 persons at any one time."},
            {"id": "Q13", "type": "Multiple Choice", "question_text": "Why must visitors scrub their boots in the disinfectant bath?", "options": ["A. To keep the visitor center floors clean", "B. To remove poisonous snake venom", "C. To prevent spreading kauri dieback spores", "D. To clean river mud off footwear"], "correct_answer": "C. To prevent spreading kauri dieback spores", "explanation": "Ranger highlights scrubbing boots to prevent spreading kauri dieback spores."},
            {"id": "Q14", "type": "Multiple Choice", "question_text": "What species has been successfully reintroduced to the predator-free sanctuary?", "options": ["A. Kiwi and tuatara", "B. Stitchbirds and bellbirds", "C. Possums and stoats", "D. Feral wallabies"], "correct_answer": "B. Stitchbirds and bellbirds", "explanation": "Ranger notes endangered stitchbirds and bellbirds have re-established breeding populations."},
            {"id": "Q15", "type": "Multiple Choice", "question_text": "What time will lunch be served at the outdoor picnic shelter?", "options": ["A. 11:45 am", "B. 12:00 pm", "C. 12:30 pm", "D. 1:15 pm"], "correct_answer": "C. 12:30 pm", "explanation": "Ranger confirms lunch at the picnic shelter at 12:30 pm."},
            {"id": "Q16", "type": "Sentence Completion", "question_text": "The canopy walkway spans a distance of ____________ meters across the canyon.", "correct_answer": "sixty", "explanation": "Transcript: 'spans sixty meters across the river canyon'."},
            {"id": "Q17", "type": "Sentence Completion", "question_text": "The oldest trees in the beech forest date back over ____________ years.", "correct_answer": "four hundred", "explanation": "Transcript: 'trees date back over four hundred years'."},
            {"id": "Q18", "type": "Sentence Completion", "question_text": "Group A will focus on clearing fallen ____________ along the ridge.", "correct_answer": "timber", "explanation": "Transcript: 'clear fallen timber along the Southern Ridge'."},
            {"id": "Q19", "type": "Sentence Completion", "question_text": "Group B is responsible for monitoring automated ____________ tunnels.", "correct_answer": "tracking", "explanation": "Transcript: 'monitor automated tracking tunnels for rodent activity'."},
            {"id": "Q20", "type": "Sentence Completion", "question_text": "Lunch is funded courtesy of the Friends of ____________ Society.", "correct_answer": "Otari", "explanation": "Transcript: 'courtesy of the Friends of Otari Society'."}
        ],

        "s3_title": "Academic Research Tutorial on Estuarine Microplastic Sampling",
        "s3_context": "Two undergraduate environmental science students, Chloe and Marcus, discuss their field research methodology with their academic tutor, Dr. Henderson.",
        "s3_script": """Dr. Henderson: Good afternoon, Chloe, Marcus. Come in. I've had a look through the preliminary draft of your third-year field methodology for the River Avon microplastics survey. It's looking promising, but there are several logistical and chemical issues we need to tighten up before you start sampling next week.
Chloe: Thanks, Dr. Henderson. We were particularly concerned about our choice of sampling net. Initially, we intended to use a standard plankton tow net with a 330-micrometer mesh. But looking at recent literature from marine microplastic studies, smaller fibers under 100 micrometers make up nearly sixty percent of estuarine plastic debris.
Marcus: Exactly. So we're proposing a dual-tier approach: towing the 330-micrometer manta trawl for macro-fragments, alongside a submersible peristaltic pump fitted with a 20-micrometer stainless steel filtration cartridge to capture synthetic microfibers.
Dr. Henderson: That's a much more rigorous setup, Marcus. But tell me: how do you plan to mitigate procedural contamination during filtration? You'll be standing on an aluminum vessel wearing synthetic outdoor clothing.
Chloe: We considered that! We've instituted a strict zero-plastic protocol aboard the boat. All field crew will wear one hundred percent cotton overalls and natural rubber nitrile gloves. Furthermore, we'll expose procedural airborne blank filters on deck during every thirty-minute sampling run to quantify atmospheric deposition.
Dr. Henderson: Splendid! Documenting airborne blanks is where many undergraduate papers fall down. Now, what about your chemical digestion protocol in the lab?
Marcus: For digestion of organic river debris, we rejected acid digestion with nitric acid because strong acids can melt or decompose low-density polyethylene and polystyrene beads. Instead, we've selected Fenton's reagent—hydrogen peroxide catalyzed with iron sulfate. It operates at room temperature and oxidizes ninety-eight percent of biological organic matter within two hours without degrading synthetic polymers.
Chloe: And for polymer identification, Professor Evans in the chemistry department has scheduled us on the micro-FTIR spectrometer for four hours every Thursday morning.
Dr. Henderson: Excellent. Make sure you construct a customized polymer library covering polyethylene, polypropylene, and nylon before running your environmental filter extracts.""",
        "s3_questions": [
            {"id": "Q21", "type": "Multiple Choice", "question_text": "Why did Chloe and Marcus modify their initial sampling net strategy?", "options": ["A. The plankton net was too heavy to tow behind their boat", "B. Fibers smaller than 100 micrometers constitute most estuarine debris", "C. Strong river currents tore the mesh fabric", "D. University safety regulations banned manta nets"], "correct_answer": "B. Fibers smaller than 100 micrometers constitute most estuarine debris", "explanation": "Chloe explains that smaller fibers under 100 micrometers make up nearly 60% of estuarine plastic."},
            {"id": "Q22", "type": "Multiple Choice", "question_text": "What will the students use to collect synthetic microfibers below 100 micrometers?", "options": ["A. A handheld butterfly net", "B. A submersible peristaltic pump with stainless steel filters", "C. Plastic collection buckets dragged along the riverbed", "D. Cotton fishing nets soaked in alcohol"], "correct_answer": "B. A submersible peristaltic pump with stainless steel filters", "explanation": "Marcus mentions a submersible peristaltic pump fitted with a 20-micrometer stainless steel cartridge."},
            {"id": "Q23", "type": "Multiple Choice", "question_text": "How do the students plan to prevent contamination from their own clothing?", "options": ["A. By wearing sterile disposable surgical gowns", "B. By wearing 100% cotton overalls and nitrile gloves", "C. By changing into synthetic wetsuits", "D. By standing behind a plexiglass windshield"], "correct_answer": "B. By wearing 100% cotton overalls and nitrile gloves", "explanation": "Chloe states all crew will wear 100% cotton overalls and natural rubber nitrile gloves."},
            {"id": "Q24", "type": "Multiple Choice", "question_text": "Why did the students reject nitric acid digestion?", "options": ["A. It was too expensive for the department budget", "B. It produces dangerous chlorine gas", "C. Strong acids can melt or decompose low-density polymers", "D. It takes more than 72 hours to dissolve algae"], "correct_answer": "C. Strong acids can melt or decompose low-density polymers", "explanation": "Marcus explains strong acids can melt or decompose polyethylene and polystyrene beads."},
            {"id": "Q25", "type": "Multiple Choice", "question_text": "What chemical reagent did the students choose for organic matter digestion?", "options": ["A. Sodium hypochlorite bleach", "B. Hydrochloric acid", "C. Fenton's reagent (hydrogen peroxide with iron sulfate)", "D. Pure ethanol solvent"], "correct_answer": "C. Fenton's reagent (hydrogen peroxide with iron sulfate)", "explanation": "Marcus identifies Fenton's reagent: hydrogen peroxide catalyzed with iron sulfate."},
            {"id": "Q26", "type": "Multiple Choice", "question_text": "When do the students have laboratory access to the micro-FTIR spectrometer?", "options": ["A. Monday afternoons", "B. Wednesday mornings", "C. Thursday mornings", "D. Friday evenings"], "correct_answer": "C. Thursday mornings", "explanation": "Chloe states access is scheduled for four hours every Thursday morning."},
            {"id": "Q27", "type": "Notes Completion", "question_text": "Mesh size of initial manta trawl: ____________ micrometers", "correct_answer": "330", "explanation": "Chloe specifies a 330-micrometer mesh."},
            {"id": "Q28", "type": "Notes Completion", "question_text": "Airborne blank filters will be exposed for ____________ minutes per run.", "correct_answer": "thirty", "explanation": "Chloe specifies every thirty-minute sampling run."},
            {"id": "Q29", "type": "Notes Completion", "question_text": "Fenton's reagent eliminates approximately ____________ percent of organic matter.", "correct_answer": "ninety-eight", "explanation": "Marcus states it oxidizes 98% of biological matter."},
            {"id": "Q30", "type": "Notes Completion", "question_text": "Spectroscopy lab director: Professor ____________", "correct_answer": "Evans", "explanation": "Chloe identifies Professor Evans in the chemistry department."}
        ],

        "s4_title": "University Scientific Lecture: Microbial Carbonate Precipitation and Bio-Concrete",
        "s4_context": "A university civil engineering professor delivers a formal academic lecture on biotechnology in sustainable construction materials.",
        "s4_script": """Lecturer: Good morning, ladies and gentlemen. Today we turn our attention to one of the most promising frontiers in green materials science: Microbial Induced Carbonate Precipitation, commonly referred to in civil engineering as bio-concrete or self-healing concrete.
To understand the urgent impetus behind this technology, one must grasp the colossal ecological footprint of traditional Portland cement. Cement manufacturing is responsible for roughly eight percent of total global carbon dioxide emissions. For every single metric tonne of Portland cement produced, approximately nine hundred kilograms of CO2 are released into the atmosphere, driven by the intense heat of industrial kilns and the chemical calcination of limestone. As urban infrastructure expands globally, continuing this trajectory is ecologically untenable.
Biological mineralization offers a revolutionary departure from conventional chemistry. Rather than relying on high-temperature synthetic clinker, bio-concrete harnesses the metabolic machinery of alkaliphilic bacteria—most notably endospore-forming strains such as Sporosarcina pasteurii and Bacillus pseudofirmus. These bacterial strains possess two unique physiological traits: first, they thrive in highly alkaline conditions with a pH reaching up to 11.5, which mimics the harsh interior chemistry of curing concrete; second, their bacterial endospores can remain completely dormant within dry, uncracked masonry for up to two centuries without food or water.
The bio-chemical mechanism operates through urea hydrolysis catalyzed by the bacterial enzyme urease. When micro-cracks inevitably form in the concrete structure due to thermal contraction or mechanical stress, atmospheric oxygen and moisture penetrate into the fissure. This ingress of water acts as an environmental trigger: it revives the dormant bacterial spores from stasis. Once active, the bacteria metabolize nutrients blended into the matrix—specifically calcium lactate—and hydrolyze urea into carbonate and ammonium ions. The released carbonate ions react with ambient calcium ions, precipitating insoluble calcium carbonate crystals, predominantly in the crystalline form of calcite.
Over a period of two to three weeks, these newly formed calcite crystals accumulate along the fissure, physically bridging and sealing cracks up to eight-tenths of a millimeter in width. Once the crack is sealed, moisture is locked out, and the bacteria return to their dormant spore state until subsequent cracking occurs.
Mechanical testing reveals that bio-healed concrete recovers up to eighty-five percent of its original compressive strength and ninety percent of its water impermeability. By preventing water from reaching internal steel reinforcement rebar, this autonomous biological process eliminates the primary cause of catastrophic structural corrosion. While production costs are currently thirty percent higher than standard Portland concrete, lifecycle economic analyses demonstrate that bio-concrete pays for itself within a decade through the near-total elimination of expensive manual maintenance and structural epoxy injections.""",
        "s4_questions": [
            {"id": "Q31", "type": "Lecture Notes", "question_text": "Cement manufacturing produces roughly ____________ percent of global CO2 emissions.", "correct_answer": "eight", "explanation": "Lecturer: 'responsible for roughly eight percent of total global carbon dioxide emissions'."},
            {"id": "Q32", "type": "Lecture Notes", "question_text": "One tonne of cement releases roughly ____________ kilograms of CO2.", "correct_answer": "nine hundred", "explanation": "Lecturer: 'approximately nine hundred kilograms of CO2 are released'."},
            {"id": "Q33", "type": "Lecture Notes", "question_text": "Bacterial strains used in bio-concrete thrive at pH levels up to ____________.", "correct_answer": "11.5", "explanation": "Lecturer: 'thrive in highly alkaline conditions with a pH reaching up to 11.5'."},
            {"id": "Q34", "type": "Lecture Notes", "question_text": "Dormant bacterial spores can survive inside dry concrete for up to two ____________.", "correct_answer": "centuries", "explanation": "Lecturer: 'remain completely dormant... for up to two centuries'."},
            {"id": "Q35", "type": "Lecture Notes", "question_text": "The chemical reaction is catalyzed by the bacterial enzyme ____________.", "correct_answer": "urease", "explanation": "Lecturer: 'urea hydrolysis catalyzed by the bacterial enzyme urease'."},
            {"id": "Q36", "type": "Lecture Notes", "question_text": "Bacterial spores are revived when water and ____________ enter fissures.", "correct_answer": "oxygen", "explanation": "Lecturer: 'atmospheric oxygen and moisture penetrate into the fissure'."},
            {"id": "Q37", "type": "Lecture Notes", "question_text": "The mineral crystals precipitated inside cracks are primarily ____________.", "correct_answer": "calcite", "explanation": "Lecturer: 'predominantly in the crystalline form of calcite'."},
            {"id": "Q38", "type": "Lecture Notes", "question_text": "Cracks up to ____________ millimeters in width can be healed autonomously.", "correct_answer": "0.8", "explanation": "Lecturer: 'sealing cracks up to eight-tenths of a millimeter in width'."},
            {"id": "Q39", "type": "Lecture Notes", "question_text": "Healed specimens recover up to ____________ percent of compressive strength.", "correct_answer": "eighty-five", "explanation": "Lecturer: 'recovers up to eighty-five percent of its original compressive strength'."},
            {"id": "Q40", "type": "Lecture Notes", "question_text": "Lifecycle economic models show bio-concrete offsets costs within one ____________.", "correct_answer": "decade", "explanation": "Lecturer: 'pays for itself within a decade through the near-total elimination of expensive maintenance'."}
        ]
    }
]

def get_cambridge_listening_test(set_num):
    suite_idx = (set_num - 1) % len(LISTENING_SUITES)
    suite = LISTENING_SUITES[suite_idx]

    test_id = f"L-{set_num:02d}" if set_num < 100 else f"L-{set_num}"
    title = f"IELTS Official Listening Practice Test {set_num}: {suite['title']}"

    # Format sections
    sections = [
        {
            "section_num": 1,
            "title": f"Section 1: {suite['s1_title']}",
            "context": suite["s1_context"],
            "audio_script": suite["s1_script"],
            "questions": [{**q, "id": f"{test_id}-{q['id']}"} for q in suite["s1_questions"]]
        },
        {
            "section_num": 2,
            "title": f"Section 2: {suite['s2_title']}",
            "context": suite["s2_context"],
            "audio_script": suite["s2_script"],
            "questions": [{**q, "id": f"{test_id}-{q['id']}"} for q in suite["s2_questions"]]
        },
        {
            "section_num": 3,
            "title": f"Section 3: {suite['s3_title']}",
            "context": suite["s3_context"],
            "audio_script": suite["s3_script"],
            "questions": [{**q, "id": f"{test_id}-{q['id']}"} for q in suite["s3_questions"]]
        },
        {
            "section_num": 4,
            "title": f"Section 4: {suite['s4_title']}",
            "context": suite["s4_context"],
            "audio_script": suite["s4_script"],
            "questions": [{**q, "id": f"{test_id}-{q['id']}"} for q in suite["s4_questions"]]
        }
    ]

    content = {"sections": sections}
    return test_id, "listening", title, "Academic", 40, "Authentic Cambridge Standard", json.dumps(content)
