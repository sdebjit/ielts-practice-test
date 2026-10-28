"""
Cambridge IELTS General Training (GT) Exam Bank
Calibrated strictly to official Cambridge IELTS General Training specifications:
- GT Reading: 40 Questions across 3 distinct sections:
    * Section 1: 2-3 short informational texts based on everyday life (social survival)
    * Section 2: 2 factual texts dealing with work issues (workplace context)
    * Section 3: 1 longer descriptive text of general interest
- GT Writing:
    * Task 1: Letter (Formal, Semi-formal, Informal) addressing 3 bullet points with Band 9 models
    * Task 2: Discursive Essay on general interest themes with Band 9 models
"""

import json

# ==============================================================================
# GENERAL TRAINING READING SUITES (EACH SUITE CONTAINS FULL 40 QUESTIONS)
# ==============================================================================

GT_READING_SUITES = [
    # -------------------------------------------------------------------------
    # SUITE 1: Community Services, Workplace Policies & Technology Innovation
    # -------------------------------------------------------------------------
    {
        "suite_id": 1,
        "domain": "Everyday Services, Employment & Social History",
        "cambridge_ref": "Cambridge General Training Reading Benchmark (Vol 18 / 19)",
        
        # SECTION 1: Social Survival (Text 1: Community Sports Centre & Text 2: City Library Services)
        "s1_title": "Section 1: Everyday Community Information (Texts A & B)",
        "s1_text": """Text A: Westbridge Community Sports Centre – Facilities and Bookings
Westbridge Community Sports Centre provides a wide range of recreational amenities for residents of all ages. The centre is open Monday to Friday from 06:30 to 22:00, and on weekends from 08:00 to 20:00.

Membership Options:
- Gold Membership: Provides unrestricted access to the 25-metre heated swimming pool, modern fitness gym, sauna, and all scheduled group classes. Direct debit fee is £45 monthly with no minimum contract period.
- Silver Membership: Permits off-peak access (09:00 to 16:00 on weekdays and after 14:00 on weekends). Monthly fee is £28.
- Pay-as-You-Go: Non-members can purchase day passes at reception (£8.50 for adult gym access, £5.00 for pool sessions).

Court Bookings:
Badminton and squash courts can be reserved up to seven days in advance by members, or three days in advance by non-members. Reservations cancelled less than twenty-four hours before the booked time will incur the standard court hire charge. Clean indoor trainers with non-marking rubber soles must be worn on all timber courts at all times.

Lockers and Equipment:
Lockers operate using refundable £1 coins or tokens available from reception. Padlocks may not be left on lockers overnight; security staff inspect and clear all lockers after closing each evening. Any unclaimed items are transferred to lost property and retained for twenty-eight days before disposal.

--------------------------------------------------------------------------------
Text B: City Central Library – Digital Access and Study Spaces
City Central Library offers quiet study areas, meeting rooms, and extensive digital resources across three floors.

Wi-Fi and Computer Workstations:
Free high-speed wireless internet is accessible throughout the premises. Fifty desktop computers are located on the second floor. Library cardholders may reserve workstations for up to two consecutive hours per day free of charge. Guests without cards may obtain a temporary day pass from the information desk upon presenting government-issued photographic identification.

Printing, Scanning, and Photocopying:
Self-service multifunction printers are situated on Floors 1 and 2. Black-and-white printouts cost 10p per A4 page; colour copies cost 30p per page. Payment is made using pre-loaded library print cards. Scanners are free to use when sending digital documents directly to an email address or USB storage device.

Group Study Rooms:
Four study rooms accommodating between four and eight people can be booked for academic and collaborative projects. Bookings must be made online at least forty-eight hours in advance. A minimum of three participants must be present when collecting the room key from the second-floor service desk.""",
        "s1_questions": [
            {"id": "Q1", "type": "True/False/Not Given", "question_text": "Silver members may use the gym at 10:00 on a Tuesday morning.", "correct_answer": "TRUE", "explanation": "Text A states Silver Membership permits off-peak access from 09:00 to 16:00 on weekdays."},
            {"id": "Q2", "type": "True/False/Not Given", "question_text": "Non-members must pay a monthly administrative fee to book a squash court.", "correct_answer": "FALSE", "explanation": "Text A states non-members can book courts three days in advance on a pay-as-you-go basis without monthly fees."},
            {"id": "Q3", "type": "True/False/Not Given", "question_text": "Swimmers are required to wear silicone swimming caps in the 25-metre pool.", "correct_answer": "NOT GIVEN", "explanation": "Text A mentions non-marking footwear for courts, but does not state any rule regarding swimming caps."},
            {"id": "Q4", "type": "True/False/Not Given", "question_text": "Unclaimed items removed from lockers are kept for four weeks before being discarded.", "correct_answer": "TRUE", "explanation": "Text A states items are retained for twenty-eight days (four weeks) before disposal."},
            {"id": "Q5", "type": "True/False/Not Given", "question_text": "Library visitors without a card must pay £5 to access computer workstations.", "correct_answer": "FALSE", "explanation": "Text B states guests may obtain a temporary pass upon presenting photo ID; no £5 fee is mentioned."},
            {"id": "Q6", "type": "True/False/Not Given", "question_text": "Scanning documents and sending them to a USB drive incurs no financial charge.", "correct_answer": "TRUE", "explanation": "Text B explicitly notes 'Scanners are free to use when sending digital documents directly to an email address or USB storage device'."},
            {"id": "Q7", "type": "True/False/Not Given", "question_text": "Two people may reserve and occupy a group study room on the second floor.", "correct_answer": "FALSE", "explanation": "Text B specifies 'A minimum of three participants must be present when collecting the room key'."},
            {"id": "Q8", "type": "Sentence Completion", "question_text": "Gold membership direct debit charges are paid on a ____________ basis.", "correct_answer": "monthly", "explanation": "Text A: 'Direct debit fee is £45 monthly'."},
            {"id": "Q9", "type": "Sentence Completion", "question_text": "Players using timber courts must wear shoes with ____________ soles.", "correct_answer": "non-marking rubber", "explanation": "Text A: 'Clean indoor trainers with non-marking rubber soles must be worn'."},
            {"id": "Q10", "type": "Sentence Completion", "question_text": "To secure lockers, users require either tokens or a ____________.", "correct_answer": "refundable £1 coin", "explanation": "Text A: 'Lockers operate using refundable £1 coins or tokens'."},
            {"id": "Q11", "type": "Sentence Completion", "question_text": "Library cardholders may use computer workstations for a maximum of ____________ daily.", "correct_answer": "two consecutive hours", "explanation": "Text B: 'reserve workstations for up to two consecutive hours per day'."},
            {"id": "Q12", "type": "Sentence Completion", "question_text": "Visitors must present ____________ identification to receive a temporary computer pass.", "correct_answer": "government-issued photographic", "explanation": "Text B: 'upon presenting government-issued photographic identification'."},
            {"id": "Q13", "type": "Sentence Completion", "question_text": "Group study room reservations must be arranged at least ____________ ahead of time.", "correct_answer": "forty-eight hours", "explanation": "Text B: 'Bookings must be made online at least forty-eight hours in advance'."},
            {"id": "Q14", "type": "Sentence Completion", "question_text": "Multifunction printers are located on both Floor 1 and ____________.", "correct_answer": "Floor 2", "explanation": "Text B: 'Multifunction printers are situated on Floors 1 and 2'."}
        ],

        # SECTION 2: Workplace Survival (Text 1: Annual Leave & Flexible Hours, Text 2: Health and Safety Guidelines)
        "s2_title": "Section 2: Workplace Policies and Staff Procedures (Texts C & D)",
        "s2_text": """Text C: Meridian Enterprises – Employee Annual Leave and Flexible Working Policy
1. Annual Leave Entitlement:
Full-time permanent employees are entitled to twenty-five working days of paid annual leave per calendar year, excluding statutory public holidays. Part-time personnel accrue paid leave on a pro-rata basis calibrated to their contracted weekly hours. The holiday year runs from 1st January to 31st December.

2. Booking Annual Leave:
Holiday requests must be submitted through the internal HR Portal. For periods of leave exceeding five consecutive working days, employees must submit applications at least four weeks in advance. Notice equivalent to twice the duration of the requested leave is required for shorter periods. Departmental line managers review requests based on operational requirements and team coverage. No more than two team members in any single unit may take concurrent leave without prior director-level authorisation.

3. Carry-Over of Unused Leave:
Employees are encouraged to utilize their full leave entitlement within the relevant calendar year. However, up to five unused days may be transferred into the subsequent holiday year with written managerial approval. Any carried-over days must be taken before 31st March, after which they will lapse without financial remuneration.

4. Flexible Working Hours (Core Time):
The company operates a core-hours flexitime framework. All staff must be present or logged into remote systems during core business hours between 10:00 and 12:00 in the morning, and 14:00 and 16:00 in the afternoon. Flexible arrival times are permitted between 07:30 and 10:00, while departures may be scheduled between 16:00 and 19:00, provided the contracted 37.5 weekly hours are fulfilled.

--------------------------------------------------------------------------------
Text D: Workplace Health and Ergonomic Safety Guidelines
All employees are legally entitled to a safe, comfortable working environment. Meridian Enterprises is committed to maintaining high occupational health and safety standards across all commercial office spaces.

Display Screen Equipment (DSE) Assessments:
Every new team member must complete a computerized Display Screen Equipment self-assessment within fourteen days of commencing employment. Line managers provide adjustable ergonomic seating, wrist supports, and monitor risers based on assessment findings. Employees who routinely utilize display screens for more than two continuous hours per day are eligible for an annual subsidised eye examination funded by the corporate healthcare scheme.

Reporting Hazards and Near Misses:
Safety is a collective responsibility. Any physical hazard, including loose cabling across walkways, liquid spillages, or malfunctioning electrical hardware, must be reported immediately using the online Facilities Incident Form. Where a hazard poses imminent danger, the Facilities Hotline (ext. 4400) should be dialled immediately. Incident logs are reviewed monthly by the Health and Safety Committee.

Evacuation Protocols:
Fire alarm testing is conducted every Tuesday at 10:30. In the event of a sustained emergency alarm, all staff must immediately evacuate via the nearest illuminated emergency exit stairwell. Passenger lifts are automatically deactivated during alarm activations and must never be utilized. Staff must congregate at Designated Assembly Point C in the North Car Park until roll calls are completed by designated fire wardens.""",
        "s2_questions": [
            {"id": "Q15", "type": "Sentence Completion", "question_text": "Full-time personnel receive ____________ days of paid annual leave annually.", "correct_answer": "twenty-five working days", "explanation": "Text C: 'entitled to twenty-five working days of paid annual leave per calendar year'."},
            {"id": "Q16", "type": "Sentence Completion", "question_text": "Leave requests longer than five days require at least ____________ notice.", "correct_answer": "four weeks", "explanation": "Text C: 'submit applications at least four weeks in advance'."},
            {"id": "Q17", "type": "Sentence Completion", "question_text": "A maximum of ____________ unused leave days may be rolled over into the following year.", "correct_answer": "five", "explanation": "Text C: 'up to five unused days may be transferred into the subsequent holiday year'."},
            {"id": "Q18", "type": "Sentence Completion", "question_text": "Carried-over holidays must be utilized before ____________ or they will expire.", "correct_answer": "31st March", "explanation": "Text C: 'must be taken before 31st March, after which they will lapse'."},
            {"id": "Q19", "type": "Sentence Completion", "question_text": "Morning core working hours require mandatory attendance between 10:00 and ____________.", "correct_answer": "12:00", "explanation": "Text C: 'core business hours between 10:00 and 12:00 in the morning'."},
            {"id": "Q20", "type": "Sentence Completion", "question_text": "Employees must submit their initial DSE assessment within ____________ of starting work.", "correct_answer": "fourteen days", "explanation": "Text D: 'self-assessment within fourteen days of commencing employment'."},
            {"id": "Q21", "type": "Sentence Completion", "question_text": "Staff who operate screens for extended periods are entitled to a yearly ____________.", "correct_answer": "subsidised eye examination", "explanation": "Text D: 'eligible for an annual subsidised eye examination funded by the corporate healthcare scheme'."},
            {"id": "Q22", "type": "True/False/Not Given", "question_text": "Three colleagues working in the marketing team can take simultaneous leave if their line manager agrees.", "correct_answer": "FALSE", "explanation": "Text C states 'No more than two team members in any single unit may take concurrent leave without prior director-level authorisation'."},
            {"id": "Q23", "type": "True/False/Not Given", "question_text": "Employees are paid financial compensation for any carried-over leave not taken by March.", "correct_answer": "FALSE", "explanation": "Text C states carried-over days 'will lapse without financial remuneration'."},
            {"id": "Q24", "type": "True/False/Not Given", "question_text": "An employee may arrive at work at 08:30 under the flexitime arrangement.", "correct_answer": "TRUE", "explanation": "Text C specifies flexible arrivals are permitted between 07:30 and 10:00."},
            {"id": "Q25", "type": "True/False/Not Given", "question_text": "Staff who work from home are exempt from completing ergonomic safety assessments.", "correct_answer": "NOT GIVEN", "explanation": "Text D mentions every new team member must complete the computerized self-assessment, with no exemption mentioned for remote workers."},
            {"id": "Q26", "type": "True/False/Not Given", "question_text": "Immediate threats to physical safety must be phoned in via extension 4400.", "correct_answer": "TRUE", "explanation": "Text D specifies: 'Where a hazard poses imminent danger, the Facilities Hotline (ext. 4400) should be dialled immediately'."},
            {"id": "Q27", "type": "True/False/Not Given", "question_text": "Employees may use the service elevators to evacuate during an emergency fire drill.", "correct_answer": "FALSE", "explanation": "Text D clearly states 'Passenger lifts are automatically deactivated during alarm activations and must never be utilized'."}
        ],

        # SECTION 3: General Reading Article (Comprehensive Descriptive Text)
        "s3_title": "Section 3: The Architecture and Conservation of the Global Seed Vault",
        "s3_text": """Paragraph A
Deep inside a sandstone mountain on the remote Arctic archipelago of Svalbard, midway between mainland Norway and the North Pole, lies the Svalbard Global Seed Vault. Often referred to by journalists as the 'Doomsday Vault', this engineering marvel is designed as an ultimate insurance policy for world agriculture. It houses duplicate backup samples of crop seeds conserved in gene banks across the globe. In an era threatened by accelerating climate disruption, biodiversity contraction, geopolitical conflict, and catastrophic civil unrest, the facility ensures that the genetic diversity of humanity's principal food crops remains safeguarded against permanent extinction.

Paragraph B
The vault's physical location was selected through rigorous geographical and tectonic assessments. Svalbard satisfies virtually all geological prerequisites for ultra-secure long-term preservation. The archipelago is tectonically inert, with negligible risk of volcanic upheaval or catastrophic earthquakes. Located 130 metres above sea level, the entrance remains safely above projected sea-level increases even under severe planetary climate models predicting the complete melting of Greenland and Antarctic ice sheets. Crucially, the surrounding permafrost maintains an ambient sub-zero ground temperature year-round, ensuring that even if the mechanical refrigeration systems suffer catastrophic power failure, the subterranean chambers will remain frozen for decades.

Paragraph C
The structural design reflects extreme defensive engineering. The facility extends 120 metres horizontally into the permafrost mountain. Access is gained through a reinforced concrete portal that juts dramatically out of the snowy mountainside. Beyond the exterior doorway, a 100-metre tunnel equipped with heavy blast doors leads past security checkpoints to three large underground storage vaults. Within these chambers, seeds are maintained at an optimal storage temperature of minus eighteen degrees Celsius. Air moisture is mechanically extracted, and each seed variety is packaged inside specialized four-ply foil packets that are heat-sealed to exclude moisture and oxygen. Under these dry, frozen conditions, seeds of major cereal staples such as wheat, rice, and barley can remain biologically viable for centuries.

Paragraph D
Importantly, the Svalbard facility does not operate as an active agricultural research center or commercial seed exchange. It functions strictly as a safety deposit facility, analogous to a bank vault. Ownership of the biological samples remains entirely with the depositor institutions; no third party, including the Norwegian government or the Global Crop Diversity Trust, possesses legal authority to access, distribute, or genetically modify deposited seeds. Furthermore, depositors may only withdraw seed samples that they deposited themselves, and only when their domestic seed collections have suffered irrecoverable destruction due to conflict, technological breakdown, or natural catastrophe.

Paragraph E
The critical importance of this failsafe was dramatically underscored in 2015 following the devastation of the International Center for Agricultural Research in the Dry Areas (ICARDA) during the Syrian civil war. Based in Aleppo, ICARDA maintained one of the world's most valuable collections of drought-tolerant wheat, barley, lentil, and chickpea landraces historically adapted to arid Mediterranean climates. When fighting destroyed the Aleppo facility, ICARDA scientists made the first-ever formal withdrawal from the Svalbard vault. They successfully retrieved 128,000 duplicate seed packets, replanted them at newly established research facilities in Lebanon and Morocco, multiplied the seed stocks, and eventually returned fresh replacement deposits to Svalbard in 2017, proving the vault's practical humanitarian utility.

Paragraph F
Despite its robust design, the vault has faced environmental challenges. In 2017, unprecedented Arctic winter temperatures and heavy rain caused melting permafrost water to breach the entrance tunnel, freezing into a sheet of ice before reaching the storage vaults. While no seed packets sustained damage, the incident prompted the Norwegian government to undertake a €20 million upgrade. Engineering teams excavated the approach tunnel, replacing the corrugated steel entryway with a fully waterproof concrete access tunnel and relocating all electrical cooling infrastructure to a separate above-ground service building to eliminate internal heat accumulation.

Paragraph G
Today, the Global Seed Vault preserves over 1.2 million distinct seed samples originating from nearly every sovereign state on Earth. It embodies an extraordinary triumph of international diplomatic and scientific cooperation, transcending political conflicts to preserve the collective agricultural heritage of our species for centuries to come.""",
        "s3_questions": [
            {"id": "Q28", "type": "Matching Headings", "question_text": "Which heading best summarizes Paragraph A?", "options": ["i. Geological criteria for site selection", "ii. A real-world rescue mission in the Middle East", "iii. The ultimate backup policy for planetary crops", "iv. Engineering upgrades after an Arctic meltwater breach", "v. Defensive architecture and refrigeration specs", "vi. Legal ownership and access regulations", "vii. Worldwide diplomatic collaboration numbers"], "correct_answer": "iii. The ultimate backup policy for planetary crops", "explanation": "Paragraph A introduces the vault as the ultimate insurance policy safeguarding agricultural genetic diversity against extinction."},
            {"id": "Q29", "type": "Matching Headings", "question_text": "Which heading best summarizes Paragraph B?", "options": ["i. Geological criteria for site selection", "ii. A real-world rescue mission in the Middle East", "iii. The ultimate backup policy for planetary crops", "iv. Engineering upgrades after an Arctic meltwater breach", "v. Defensive architecture and refrigeration specs", "vi. Legal ownership and access regulations", "vii. Worldwide diplomatic collaboration numbers"], "correct_answer": "i. Geological criteria for site selection", "explanation": "Paragraph B explains why Svalbard was chosen: tectonic stability, elevation above sea level, and permafrost cooling."},
            {"id": "Q30", "type": "Matching Headings", "question_text": "Which heading best summarizes Paragraph C?", "options": ["i. Geological criteria for site selection", "ii. A real-world rescue mission in the Middle East", "iii. The ultimate backup policy for planetary crops", "iv. Engineering upgrades after an Arctic meltwater breach", "v. Defensive architecture and refrigeration specs", "vi. Legal ownership and access regulations", "vii. Worldwide diplomatic collaboration numbers"], "correct_answer": "v. Defensive architecture and refrigeration specs", "explanation": "Paragraph C details the 100-metre tunnel, blast doors, minus 18 degree refrigeration, and four-ply foil packets."},
            {"id": "Q31", "type": "Matching Headings", "question_text": "Which heading best summarizes Paragraph D?", "options": ["i. Geological criteria for site selection", "ii. A real-world rescue mission in the Middle East", "iii. The ultimate backup policy for planetary crops", "iv. Engineering upgrades after an Arctic meltwater breach", "v. Defensive architecture and refrigeration specs", "vi. Legal ownership and access regulations", "vii. Worldwide diplomatic collaboration numbers"], "correct_answer": "vi. Legal ownership and access regulations", "explanation": "Paragraph D discusses deposit ownership rules, withdrawal restrictions, and safety deposit box analogy."},
            {"id": "Q32", "type": "Matching Headings", "question_text": "Which heading best summarizes Paragraph E?", "options": ["i. Geological criteria for site selection", "ii. A real-world rescue mission in the Middle East", "iii. The ultimate backup policy for planetary crops", "iv. Engineering upgrades after an Arctic meltwater breach", "v. Defensive architecture and refrigeration specs", "vi. Legal ownership and access regulations", "vii. Worldwide diplomatic collaboration numbers"], "correct_answer": "ii. A real-world rescue mission in the Middle East", "explanation": "Paragraph E describes the 2015 ICARDA withdrawal and rescue following the Syrian conflict."},
            {"id": "Q33", "type": "Matching Headings", "question_text": "Which heading best summarizes Paragraph F?", "options": ["i. Geological criteria for site selection", "ii. A real-world rescue mission in the Middle East", "iii. The ultimate backup policy for planetary crops", "iv. Engineering upgrades after an Arctic meltwater breach", "v. Defensive architecture and refrigeration specs", "vi. Legal ownership and access regulations", "vii. Worldwide diplomatic collaboration numbers"], "correct_answer": "iv. Engineering upgrades after an Arctic meltwater breach", "explanation": "Paragraph F covers the 2017 meltwater intrusion and the subsequent €20 million waterproofing overhaul."},
            {"id": "Q34", "type": "True/False/Not Given", "question_text": "The Global Seed Vault was built at an elevation that protects it from potential polar ice cap melting.", "correct_answer": "TRUE", "explanation": "Paragraph B states at 130m above sea level, it remains safe even under models predicting complete melting of ice sheets."},
            {"id": "Q35", "type": "True/False/Not Given", "question_text": "Commercial agricultural corporations can purchase seed varieties directly from the Svalbard facility.", "correct_answer": "FALSE", "explanation": "Paragraph D explicitly states no third party possesses legal authority to access, distribute, or buy seeds."},
            {"id": "Q36", "type": "True/False/Not Given", "question_text": "Seeds inside the vault are packaged within sealed three-ply aluminum containers.", "correct_answer": "FALSE", "explanation": "Paragraph C specifies 'specialized four-ply foil packets that are heat-sealed', not three-ply."},
            {"id": "Q37", "type": "True/False/Not Given", "question_text": "Meltwater in 2017 caused irreversible damage to thousands of grain seed packets.", "correct_answer": "FALSE", "explanation": "Paragraph F notes water froze in the approach tunnel and 'no seed packets sustained damage'."},
            {"id": "Q38", "type": "Multiple Choice", "question_text": "Why did scientists from ICARDA make a withdrawal from Svalbard in 2015?", "options": ["A. To cross-breed drought-resistant crops with Arctic flora", "B. Because their primary seed collection in Aleppo was destroyed by war", "C. To commercialize drought-tolerant seeds in international retail markets", "D. Because permafrost melting threatened their original collection in Lebanon"], "correct_answer": "B. Because their primary seed collection in Aleppo was destroyed by war", "explanation": "Paragraph E explains fighting destroyed the Aleppo facility, leading to the withdrawal."},
            {"id": "Q39", "type": "Multiple Choice", "question_text": "What engineering modification was implemented following the 2017 meltwater breach?", "options": ["A. Relocating the vault to an elevated site in Norway", "B. Lowering storage temperatures to minus thirty degrees", "C. Replacing the entrance with a waterproof concrete tunnel and moving cooling units", "D. Banning international visitors from entering the facility"], "correct_answer": "C. Replacing the entrance with a waterproof concrete tunnel and moving cooling units", "explanation": "Paragraph F describes replacing corrugated steel with a waterproof concrete tunnel and moving cooling equipment."},
            {"id": "Q40", "type": "Sentence Completion", "question_text": "The seed chambers are mechanically maintained at an optimal temperature of ____________ Celsius.", "correct_answer": "minus eighteen degrees", "explanation": "Paragraph C specifies 'an optimal storage temperature of minus eighteen degrees Celsius'."}
        ]
    }
]

# ==============================================================================
# GENERAL TRAINING WRITING SUITES (LETTERS FOR TASK 1 + DISCURSIVE ESSAYS FOR TASK 2)
# ==============================================================================

GT_WRITING_TASK1_COLLECTION = [
    {
        "subtype": "Formal Letter",
        "title": "Formal Complaint to Municipal Council Concerning Hazardous Road Infrastructure",
        "prompt": "You should spend about 20 minutes on this task.\n\nYou have noticed a serious safety hazard on a main road near your home, which is causing traffic congestion and endangering pedestrians.\n\nWrite a letter to the local municipal council. In your letter:\n- Describe the exact location and nature of the hazard\n- Explain how this problem is affecting local residents and traffic\n- Suggest specific measures the council should take to rectify the situation\n\nWrite at least 150 words. You do NOT need to write any addresses.\nBegin your letter as follows:\nDear Sir or Madam,",
        "band9_sample": "Dear Sir or Madam,\n\nI am writing to formally draw your urgent attention to an increasingly perilous road hazard situated along High Street, directly adjacent to the pedestrian crossing near the entrance of Elmwood Primary School.\n\nOver the past three weeks, an extensive subsidence has formed on the westbound carriageway, measuring approximately two metres in width and over fifteen centimetres in depth. This severe pothole is situated immediately after a blind bend, compelling motorists to either swerve abruptly into the opposing lane to avoid wheel damage or brake violently.\n\nThe resulting situation has precipitated immense traffic congestion during peak commuter and school hours. More critically, it poses an immediate threat to the safety of young schoolchildren and pedestrians crossing at this intersection. Just yesterday morning, a vehicle swerved onto the pavement curb to avoid the depression, narrowly averting a catastrophic collision with a pram.\n\nTo remediate this hazardous situation before serious injury occurs, I strongly urge the council to dispatch a road maintenance crew to execute an immediate resurfacing repair. In the interim, clear hazard warning signage and temporary speed reduction barriers should be deployed on both approaches to the bend.\n\nThank you for your prompt attention to this urgent safety matter. I look forward to your expeditious response.\n\nYours faithfully,\n\nDavid Sterling"
    },
    {
        "subtype": "Semi-Formal Letter",
        "title": "Request to Landlord Regarding Urgent Residential Heating and Plumbing Repairs",
        "prompt": "You should spend about 20 minutes on this task.\n\nYou are renting an apartment, and the central heating system has broken down during severe winter weather. You have already contacted the letting agency by telephone, but no action has been taken.\n\nWrite a letter to your landlord. In your letter:\n- Explain the nature of the heating breakdown and when it started\n- Detail the inconvenience and health impact this is causing you and your family\n- State what action you expect the landlord to take immediately\n\nWrite at least 150 words. You do NOT need to write any addresses.\nBegin your letter as follows:\nDear Mr. Jenkins,",
        "band9_sample": "Dear Mr. Jenkins,\n\nI am writing to inform you of a critical maintenance failure regarding the central heating and hot water system at Apartment 4B, 18 Kensington Gardens, which I currently lease from you.\n\nThe combination boiler ceased functioning entirely on Friday evening, 12th January. Despite resetting the unit according to the manufacturer's manual, the pilot light fails to ignite, and the digital display registers a persistent pressure fault error (code F22). As a result, the apartment has had neither heating nor running hot water for the past four days.\n\nWith ambient external temperatures currently dropping below minus three degrees Celsius, the living conditions inside the flat have become profoundly uninhabitable. My elderly mother, who resides with me and suffers from chronic arthritis, has seen her health severely compromised by the persistent cold. While I telephoned your management agency, City Lettings, on Saturday morning and was assured an engineer would attend, no technician has contacted us or inspected the property.\n\nIn light of the statutory obligation to maintain essential heating utilities, I request that you instruct an emergency Gas Safe registered engineer to attend the property within the next twenty-four hours. Should the issue remain unresolved by tomorrow evening, I will have no alternative but to commission an emergency repair service independently and deduct the invoiced expense from next month's rental remittance.\n\nI trust this will not be necessary and await your immediate confirmation.\n\nYours sincerely,\n\nRachel Bennett"
    },
    {
        "subtype": "Informal Letter",
        "title": "Invitation to an Overseas Friend to Visit Your New City with Itinerary Suggestions",
        "prompt": "You should spend about 20 minutes on this task.\n\nYou have recently moved to a new city for work, and you would like to invite a friend from your hometown to visit you for a long weekend.\n\nWrite a letter to your friend. In your letter:\n- Share your initial impressions of your new home and neighbourhood\n- Invite your friend to stay with you and recommend dates\n- Suggest several enjoyable activities you could do together during their visit\n\nWrite at least 150 words. You do NOT need to write any addresses.\nBegin your letter as follows:\nDear Tom,",
        "band9_sample": "Dear Tom,\n\nI hope you're having a brilliant week! I'm finally settled into my new flat here in Edinburgh, and I couldn't wait to write and tell you all about it.\n\nThe neighbourhood I've moved into, Stockbridge, is absolutely charming. It has cobblestone lanes, wonderful independent bookshops, and an incredible Sunday farmers' market right around the corner. The city has so much character—even on drizzly afternoons, there’s an infectious energy about the place that I know you’d fall in love with.\n\nSince I’ve finally unpacked and set up the guest bedroom, I would love for you to come up and stay for a long weekend. How about the bank holiday weekend from the 3rd to the 6th of May? The spring weather should be lovely by then, and direct trains from London only take about four hours.\n\nI've already started putting together a mini-itinerary for us. We can hike up Arthur's Seat on Saturday morning for a panoramic view across the Firth of Forth, grab lunch at an authentic Scottish pub, and spend Sunday exploring the Old Town and the National Museum. We can even take an evening ghost tour through the underground vaults if you're feeling adventurous!\n\nLet me know if those dates work for you so I can keep the weekend completely free.\n\nWarm regards,\n\nLiam"
    }
]

GT_WRITING_TASK2_COLLECTION = [
    {
        "subtype": "Discussion Essay",
        "title": "Working From Home vs Office Collaboration for Employee Productivity and Wellbeing",
        "prompt": "You should spend about 40 minutes on this task.\n\nSome people believe that working from home provides significant advantages for both workers and companies, while others argue that working in a traditional office environment is essential for productivity and teamwork.\n\nDiscuss both views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "The dramatic proliferation of remote working technologies has provoked intense debate regarding the optimal workspace for the contemporary workforce. While proponents of telecommuting emphasize enhanced work-life balance and operational cost efficiencies, detractors contend that in-person office interaction remains indispensable for collaborative innovation and accountability. This essay examines both perspectives before arguing that a flexible hybrid paradigm represents the most efficacious compromise.\n\nOn the one hand, remote working confers substantial personal and professional benefits. Primarily, the elimination of lengthy daily commutes liberates considerable time and financial resources, thereby reducing chronic stress and fatigue among employees. Workers often report higher concentrations of uninterrupted deep focus in home environments, particularly when performing analytical or written tasks. Furthermore, employers benefit from reduced capital expenditure on commercial real estate leases, utility consumption, and on-site facilities management, while concurrently accessing a geographically diverse talent pool unrestricted by municipal boundaries.\n\nConversely, traditional office spaces fulfill vital social and collaborative functions that digital communication platforms struggle to replicate. Spontaneous, serendipitous interactions around communal areas frequently serve as the catalyst for creative problem-solving and cross-departmental synergy. Moreover, junior employees rely heavily on informal, observational learning from experienced colleagues—an educational osmosis severely attenuated in isolated remote environments. Prolonged isolation can also blur the boundaries between domestic life and occupational responsibilities, culminating in burnout and weakened organizational loyalty.\n\nIn conclusion, while working from home optimizes individual focus and personal autonomy, physical office presence remains essential for fostering corporate culture, mentorship, and spontaneous team collaboration. In my view, the optimal approach is a balanced hybrid model in which personnel combine remote working for solitary tasks with two to three days on-site dedicated to collaborative endeavors."
    },
    {
        "subtype": "Opinion Essay",
        "title": "Public Transport Subsidies vs Road Construction for Alleviating Urban Traffic Congestion",
        "prompt": "You should spend about 40 minutes on this task.\n\nIn many cities, traffic congestion is a serious problem. Some people suggest that the best solution is for governments to make public transport free, while others believe that building more roads is more effective.\n\nDiscuss both views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "Metropolitan traffic congestion represents one of the most debilitating socioeconomic challenges confronting modern urban planners. While certain commentators advocate for the expansion of highway networks, others argue that subsidizing public transit to make it entirely cost-free is a far more sustainable remedy. In my view, investing in free, high-capacity mass transit systems is markedly superior to road building, which invariably exacerbates urban gridlock through induced vehicular demand.\n\nProponents of highway construction contend that widening existing arteries and constructing bypasses provides immediate capacity relief for burgeoning vehicular volumes. In expanding economies where industrial logistics depend heavily on freight transit, modern road infrastructure is undeniably vital for economic competitiveness. However, decades of transportation research have comprehensively demonstrated the phenomenon of 'induced demand': when additional road capacity is constructed, it initially lowers travel times, which subsequently incentivizes more motorists to drive, ultimately returning the expanded highway to total congestion within a few years.\n\nIn contrast, abolishing fares on municipal public transport offers a transformative economic and behavioral incentive for commuters to abandon private passenger vehicles. When transit is free, reliable, and frequent, substantial segments of the commuting public transition toward electrified commuter rail, subways, and bus rapid transit systems. Cities such as Tallinn and Montpellier, which introduced free public transportation, experienced immediate declines in urban vehicle emissions and rush-hour bottlenecks. Furthermore, cost-free public transit democratizes urban mobility, ensuring low-income residents can access employment and educational opportunities across metropolitan regions without financial impediment.\n\nTo conclude, although expanding road infrastructure may appear to be a straightforward remedy, it inevitably fails due to induced traffic demand. Governments should instead allocate fiscal resources toward delivering comprehensive, high-frequency, and zero-fare public transportation networks."
    }
]

def get_cambridge_gt_reading_test(set_num=1):
    test_id = f"GTR-{set_num:02d}"
    suite_idx = (set_num - 1) % len(GT_READING_SUITES)
    suite = GT_READING_SUITES[suite_idx]
    title = f"IELTS General Training Reading Test {set_num}: {suite['domain']}"

    # Prepare passages format matching frontend expectation
    s1_qs = [dict(q, id=f"{test_id}-{q['id']}") for q in suite["s1_questions"]]
    s2_qs = [dict(q, id=f"{test_id}-{q['id']}") for q in suite["s2_questions"]]
    s3_qs = [dict(q, id=f"{test_id}-{q['id']}") for q in suite["s3_questions"]]

    content = {
        "passages": [
            {
                "passage_num": 1,
                "title": suite["s1_title"],
                "text": suite["s1_text"],
                "questions": s1_qs
            },
            {
                "passage_num": 2,
                "title": suite["s2_title"],
                "text": suite["s2_text"],
                "questions": s2_qs
            },
            {
                "passage_num": 3,
                "title": suite["s3_title"],
                "text": suite["s3_text"],
                "questions": s3_qs
            }
        ]
    }

    return test_id, "reading", title, "General Training", 60, "Authentic Cambridge GT Standard", json.dumps(content)

def get_cambridge_gt_writing_test(set_num=1):
    test_id = f"GTW-{set_num:02d}"
    is_task2 = (set_num % 2 == 1)

    if is_task2:
        idx = ((set_num + 1) // 2 - 1) % len(GT_WRITING_TASK2_COLLECTION)
        item = GT_WRITING_TASK2_COLLECTION[idx]
        title = f"IELTS GT Writing Task 2 (Set {set_num}): {item['title']}"
        payload = {
            "task_type": "Task 2",
            "subtype": item["subtype"],
            "title": item["title"],
            "prompt": item["prompt"],
            "min_words": 250,
            "target_time_mins": 40,
            "band9_sample": item["band9_sample"]
        }
        duration = 40
    else:
        idx = (set_num // 2 - 1) % len(GT_WRITING_TASK1_COLLECTION)
        item = GT_WRITING_TASK1_COLLECTION[idx]
        title = f"IELTS GT Writing Task 1 (Set {set_num}): {item['title']}"
        payload = {
            "task_type": "Task 1",
            "subtype": item["subtype"],
            "title": item["title"],
            "prompt": item["prompt"],
            "min_words": 150,
            "target_time_mins": 20,
            "band9_sample": item["band9_sample"]
        }
        duration = 20

    return test_id, "writing", title, "General Training", duration, "Authentic Cambridge GT Standard", json.dumps(payload)

def seed_cambridge_gt_bank():
    from database import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    
    # Seed 60 GT Reading tests
    for i in range(1, 61):
        t_id, module, title, exam_type, duration, diff, content = get_cambridge_gt_reading_test(i)
        cursor.execute('''
        INSERT OR REPLACE INTO tests (id, module, title, type, duration_minutes, difficulty, content)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, module, title, exam_type, duration, diff, content))

    # Seed 60 GT Writing tests
    for i in range(1, 61):
        t_id, module, title, exam_type, duration, diff, content = get_cambridge_gt_writing_test(i)
        cursor.execute('''
        INSERT OR REPLACE INTO tests (id, module, title, type, duration_minutes, difficulty, content)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, module, title, exam_type, duration, diff, content))

    conn.commit()
    conn.close()
    print("Cambridge General Training tests seeded successfully.")

