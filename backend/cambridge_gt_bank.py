"""
Cambridge IELTS General Training (GT) Exam Bank
Calibrated strictly to official Cambridge IELTS General Training specifications:
- GT Reading: 40 Questions across 3 distinct sections (6 Full Authentic Suites):
    * Section 1: 2-3 short informational texts based on everyday life (social survival)
    * Section 2: 2 factual texts dealing with work issues (workplace context)
    * Section 3: 1 longer descriptive text of general interest
- GT Writing:
    * Task 1: 6 Authentic Letters (Formal, Semi-formal, Informal) addressing 3 bullet points with Band 9 models
    * Task 2: 6 Authentic Discursive Essays on general interest themes with Band 9 models
"""

import json

# ==============================================================================
# GENERAL TRAINING READING SUITES (6 SUITES, EACH 40 AUTHENTIC QUESTIONS)
# ==============================================================================

GT_READING_SUITES = [
    {
        "suite_id": 1,
        "domain": "Everyday Services, Employment & Social History",
        "cambridge_ref": "Cambridge General Training Reading Benchmark (Vol 18 / 19)",
        "s1_title": "Section 1: Everyday Community Information (Texts A & B)",
        "s1_text": "Text A: Westbridge Community Sports Centre \u2013 Facilities and Bookings\nWestbridge Community Sports Centre provides a wide range of recreational amenities for residents of all ages. The centre is open Monday to Friday from 06:30 to 22:00, and on weekends from 08:00 to 20:00.\n\nMembership Options:\n- Gold Membership: Provides unrestricted access to the 25-metre heated swimming pool, modern fitness gym, sauna, and all scheduled group classes. Direct debit fee is \u00a345 monthly with no minimum contract period.\n- Silver Membership: Permits off-peak access (09:00 to 16:00 on weekdays and after 14:00 on weekends). Monthly fee is \u00a328.\n- Pay-as-You-Go: Non-members can purchase day passes at reception (\u00a38.50 for adult gym access, \u00a35.00 for pool sessions).\n\nCourt Bookings:\nBadminton and squash courts can be reserved up to seven days in advance by members, or three days in advance by non-members. Reservations cancelled less than twenty-four hours before the booked time will incur the standard court hire charge. Clean indoor trainers with non-marking rubber soles must be worn on all timber courts at all times.\n\nLockers and Equipment:\nLockers operate using refundable \u00a31 coins or tokens available from reception. Padlocks may not be left on lockers overnight; security staff inspect and clear all lockers after closing each evening. Any unclaimed items are transferred to lost property and retained for twenty-eight days before disposal.\n\n--------------------------------------------------------------------------------\nText B: City Central Library \u2013 Digital Access and Study Spaces\nCity Central Library offers quiet study areas, meeting rooms, and extensive digital resources across three floors.\n\nWi-Fi and Computer Workstations:\nFree high-speed wireless internet is accessible throughout the premises. Fifty desktop computers are located on the second floor. Library cardholders may reserve workstations for up to two consecutive hours per day free of charge. Guests without cards may obtain a temporary day pass from the information desk upon presenting government-issued photographic identification.\n\nPrinting, Scanning, and Photocopying:\nSelf-service multifunction printers are situated on Floors 1 and 2. Black-and-white printouts cost 10p per A4 page; colour copies cost 30p per page. Payment is made using pre-loaded library print cards. Scanners are free to use when sending digital documents directly to an email address or USB storage device.\n\nGroup Study Rooms:\nFour study rooms accommodating between four and eight people can be booked for academic and collaborative projects. Bookings must be made online at least forty-eight hours in advance. A minimum of three participants must be present when collecting the room key from the second-floor service desk.",
        "s1_questions": [
            {
                "id": "Q1",
                "type": "True/False/Not Given",
                "question_text": "Silver members may use the gym at 10:00 on a Tuesday morning.",
                "correct_answer": "TRUE",
                "explanation": "Text A states Silver Membership permits off-peak access from 09:00 to 16:00 on weekdays."
            },
            {
                "id": "Q2",
                "type": "True/False/Not Given",
                "question_text": "Non-members must pay a monthly administrative fee to book a squash court.",
                "correct_answer": "FALSE",
                "explanation": "Text A states non-members can book courts three days in advance on a pay-as-you-go basis without monthly fees."
            },
            {
                "id": "Q3",
                "type": "True/False/Not Given",
                "question_text": "Swimmers are required to wear silicone swimming caps in the 25-metre pool.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text A mentions non-marking footwear for courts, but does not state any rule regarding swimming caps."
            },
            {
                "id": "Q4",
                "type": "True/False/Not Given",
                "question_text": "Unclaimed items removed from lockers are kept for four weeks before being discarded.",
                "correct_answer": "TRUE",
                "explanation": "Text A states items are retained for twenty-eight days (four weeks) before disposal."
            },
            {
                "id": "Q5",
                "type": "True/False/Not Given",
                "question_text": "Library visitors without a card must pay \u00a35 to access computer workstations.",
                "correct_answer": "FALSE",
                "explanation": "Text B states guests may obtain a temporary pass upon presenting photo ID; no \u00a35 fee is mentioned."
            },
            {
                "id": "Q6",
                "type": "True/False/Not Given",
                "question_text": "Scanning documents and sending them to a USB drive incurs no financial charge.",
                "correct_answer": "TRUE",
                "explanation": "Text B explicitly notes 'Scanners are free to use when sending digital documents directly to an email address or USB storage device'."
            },
            {
                "id": "Q7",
                "type": "True/False/Not Given",
                "question_text": "Two people may reserve and occupy a group study room on the second floor.",
                "correct_answer": "FALSE",
                "explanation": "Text B specifies 'A minimum of three participants must be present when collecting the room key'."
            },
            {
                "id": "Q8",
                "type": "Sentence Completion",
                "question_text": "Gold membership direct debit charges are paid on a ____________ basis.",
                "correct_answer": "monthly",
                "explanation": "Text A: 'Direct debit fee is \u00a345 monthly'."
            },
            {
                "id": "Q9",
                "type": "Sentence Completion",
                "question_text": "Players using timber courts must wear shoes with ____________ soles.",
                "correct_answer": "non-marking rubber",
                "explanation": "Text A: 'Clean indoor trainers with non-marking rubber soles must be worn'."
            },
            {
                "id": "Q10",
                "type": "Sentence Completion",
                "question_text": "To secure lockers, users require either tokens or a ____________.",
                "correct_answer": "refundable \u00a31 coin",
                "explanation": "Text A: 'Lockers operate using refundable \u00a31 coins or tokens'."
            },
            {
                "id": "Q11",
                "type": "Sentence Completion",
                "question_text": "Library cardholders may use computer workstations for a maximum of ____________ daily.",
                "correct_answer": "two consecutive hours",
                "explanation": "Text B: 'reserve workstations for up to two consecutive hours per day'."
            },
            {
                "id": "Q12",
                "type": "Sentence Completion",
                "question_text": "Visitors must present ____________ identification to receive a temporary computer pass.",
                "correct_answer": "government-issued photographic",
                "explanation": "Text B: 'upon presenting government-issued photographic identification'."
            },
            {
                "id": "Q13",
                "type": "Sentence Completion",
                "question_text": "Group study room reservations must be arranged at least ____________ ahead of time.",
                "correct_answer": "forty-eight hours",
                "explanation": "Text B: 'Bookings must be made online at least forty-eight hours in advance'."
            },
            {
                "id": "Q14",
                "type": "Sentence Completion",
                "question_text": "Multifunction printers are located on both Floor 1 and ____________.",
                "correct_answer": "Floor 2",
                "explanation": "Text B: 'Multifunction printers are situated on Floors 1 and 2'."
            }
        ],
        "s2_title": "Section 2: Workplace Policies and Staff Procedures (Texts C & D)",
        "s2_text": "Text C: Meridian Enterprises \u2013 Employee Annual Leave and Flexible Working Policy\n1. Annual Leave Entitlement:\nFull-time permanent employees are entitled to twenty-five working days of paid annual leave per calendar year, excluding statutory public holidays. Part-time personnel accrue paid leave on a pro-rata basis calibrated to their contracted weekly hours. The holiday year runs from 1st January to 31st December.\n\n2. Booking Annual Leave:\nHoliday requests must be submitted through the internal HR Portal. For periods of leave exceeding five consecutive working days, employees must submit applications at least four weeks in advance. Notice equivalent to twice the duration of the requested leave is required for shorter periods. Departmental line managers review requests based on operational requirements and team coverage. No more than two team members in any single unit may take concurrent leave without prior director-level authorisation.\n\n3. Carry-Over of Unused Leave:\nEmployees are encouraged to utilize their full leave entitlement within the relevant calendar year. However, up to five unused days may be transferred into the subsequent holiday year with written managerial approval. Any carried-over days must be taken before 31st March, after which they will lapse without financial remuneration.\n\n4. Flexible Working Hours (Core Time):\nThe company operates a core-hours flexitime framework. All staff must be present or logged into remote systems during core business hours between 10:00 and 12:00 in the morning, and 14:00 and 16:00 in the afternoon. Flexible arrival times are permitted between 07:30 and 10:00, while departures may be scheduled between 16:00 and 19:00, provided the contracted 37.5 weekly hours are fulfilled.\n\n--------------------------------------------------------------------------------\nText D: Workplace Health and Ergonomic Safety Guidelines\nAll employees are legally entitled to a safe, comfortable working environment. Meridian Enterprises is committed to maintaining high occupational health and safety standards across all commercial office spaces.\n\nDisplay Screen Equipment (DSE) Assessments:\nEvery new team member must complete a computerized Display Screen Equipment self-assessment within fourteen days of commencing employment. Line managers provide adjustable ergonomic seating, wrist supports, and monitor risers based on assessment findings. Employees who routinely utilize display screens for more than two continuous hours per day are eligible for an annual subsidised eye examination funded by the corporate healthcare scheme.\n\nReporting Hazards and Near Misses:\nSafety is a collective responsibility. Any physical hazard, including loose cabling across walkways, liquid spillages, or malfunctioning electrical hardware, must be reported immediately using the online Facilities Incident Form. Where a hazard poses imminent danger, the Facilities Hotline (ext. 4400) should be dialled immediately. Incident logs are reviewed monthly by the Health and Safety Committee.\n\nEvacuation Protocols:\nFire alarm testing is conducted every Tuesday at 10:30. In the event of a sustained emergency alarm, all staff must immediately evacuate via the nearest illuminated emergency exit stairwell. Passenger lifts are automatically deactivated during alarm activations and must never be utilized. Staff must congregate at Designated Assembly Point C in the North Car Park until roll calls are completed by designated fire wardens.",
        "s2_questions": [
            {
                "id": "Q15",
                "type": "Sentence Completion",
                "question_text": "Full-time personnel receive ____________ days of paid annual leave annually.",
                "correct_answer": "twenty-five working days",
                "explanation": "Text C: 'entitled to twenty-five working days of paid annual leave per calendar year'."
            },
            {
                "id": "Q16",
                "type": "Sentence Completion",
                "question_text": "Leave requests longer than five days require at least ____________ notice.",
                "correct_answer": "four weeks",
                "explanation": "Text C: 'submit applications at least four weeks in advance'."
            },
            {
                "id": "Q17",
                "type": "Sentence Completion",
                "question_text": "A maximum of ____________ unused leave days may be rolled over into the following year.",
                "correct_answer": "five",
                "explanation": "Text C: 'up to five unused days may be transferred into the subsequent holiday year'."
            },
            {
                "id": "Q18",
                "type": "Sentence Completion",
                "question_text": "Carried-over holidays must be utilized before ____________ or they will expire.",
                "correct_answer": "31st March",
                "explanation": "Text C: 'must be taken before 31st March, after which they will lapse'."
            },
            {
                "id": "Q19",
                "type": "Sentence Completion",
                "question_text": "Morning core working hours require mandatory attendance between 10:00 and ____________.",
                "correct_answer": "12:00",
                "explanation": "Text C: 'core business hours between 10:00 and 12:00 in the morning'."
            },
            {
                "id": "Q20",
                "type": "Sentence Completion",
                "question_text": "Employees must submit their initial DSE assessment within ____________ of starting work.",
                "correct_answer": "fourteen days",
                "explanation": "Text D: 'self-assessment within fourteen days of commencing employment'."
            },
            {
                "id": "Q21",
                "type": "Sentence Completion",
                "question_text": "Staff who operate screens for extended periods are entitled to a yearly ____________.",
                "correct_answer": "subsidised eye examination",
                "explanation": "Text D: 'eligible for an annual subsidised eye examination funded by the corporate healthcare scheme'."
            },
            {
                "id": "Q22",
                "type": "True/False/Not Given",
                "question_text": "Three colleagues working in the marketing team can take simultaneous leave if their line manager agrees.",
                "correct_answer": "FALSE",
                "explanation": "Text C states 'No more than two team members in any single unit may take concurrent leave without prior director-level authorisation'."
            },
            {
                "id": "Q23",
                "type": "True/False/Not Given",
                "question_text": "Employees are paid financial compensation for any carried-over leave not taken by March.",
                "correct_answer": "FALSE",
                "explanation": "Text C states carried-over days 'will lapse without financial remuneration'."
            },
            {
                "id": "Q24",
                "type": "True/False/Not Given",
                "question_text": "An employee may arrive at work at 08:30 under the flexitime arrangement.",
                "correct_answer": "TRUE",
                "explanation": "Text C specifies flexible arrivals are permitted between 07:30 and 10:00."
            },
            {
                "id": "Q25",
                "type": "True/False/Not Given",
                "question_text": "Staff who work from home are exempt from completing ergonomic safety assessments.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text D mentions every new team member must complete the computerized self-assessment, with no exemption mentioned for remote workers."
            },
            {
                "id": "Q26",
                "type": "True/False/Not Given",
                "question_text": "Immediate threats to physical safety must be phoned in via extension 4400.",
                "correct_answer": "TRUE",
                "explanation": "Text D specifies: 'Where a hazard poses imminent danger, the Facilities Hotline (ext. 4400) should be dialled immediately'."
            },
            {
                "id": "Q27",
                "type": "True/False/Not Given",
                "question_text": "Employees may use the service elevators to evacuate during an emergency fire drill.",
                "correct_answer": "FALSE",
                "explanation": "Text D clearly states 'Passenger lifts are automatically deactivated during alarm activations and must never be utilized'."
            }
        ],
        "s3_title": "Section 3: The Architecture and Conservation of the Global Seed Vault",
        "s3_text": "Paragraph A\nDeep inside a sandstone mountain on the remote Arctic archipelago of Svalbard, midway between mainland Norway and the North Pole, lies the Svalbard Global Seed Vault. Often referred to by journalists as the 'Doomsday Vault', this engineering marvel is designed as an ultimate insurance policy for world agriculture. It houses duplicate backup samples of crop seeds conserved in gene banks across the globe. In an era threatened by accelerating climate disruption, biodiversity contraction, geopolitical conflict, and catastrophic civil unrest, the facility ensures that the genetic diversity of humanity's principal food crops remains safeguarded against permanent extinction.\n\nParagraph B\nThe vault's physical location was selected through rigorous geographical and tectonic assessments. Svalbard satisfies virtually all geological prerequisites for ultra-secure long-term preservation. The archipelago is tectonically inert, with negligible risk of volcanic upheaval or catastrophic earthquakes. Located 130 metres above sea level, the entrance remains safely above projected sea-level increases even under severe planetary climate models predicting the complete melting of Greenland and Antarctic ice sheets. Crucially, the surrounding permafrost maintains an ambient sub-zero ground temperature year-round, ensuring that even if the mechanical refrigeration systems suffer catastrophic power failure, the subterranean chambers will remain frozen for decades.\n\nParagraph C\nThe structural design reflects extreme defensive engineering. The facility extends 120 metres horizontally into the permafrost mountain. Access is gained through a reinforced concrete portal that juts dramatically out of the snowy mountainside. Beyond the exterior doorway, a 100-metre tunnel equipped with heavy blast doors leads past security checkpoints to three large underground storage vaults. Within these chambers, seeds are maintained at an optimal storage temperature of minus eighteen degrees Celsius. Air moisture is mechanically extracted, and each seed variety is packaged inside specialized four-ply foil packets that are heat-sealed to exclude moisture and oxygen. Under these dry, frozen conditions, seeds of major cereal staples such as wheat, rice, and barley can remain biologically viable for centuries.\n\nParagraph D\nImportantly, the Svalbard facility does not operate as an active agricultural research center or commercial seed exchange. It functions strictly as a safety deposit facility, analogous to a bank vault. Ownership of the biological samples remains entirely with the depositor institutions; no third party, including the Norwegian government or the Global Crop Diversity Trust, possesses legal authority to access, distribute, or genetically modify deposited seeds. Furthermore, depositors may only withdraw seed samples that they deposited themselves, and only when their domestic seed collections have suffered irrecoverable destruction due to conflict, technological breakdown, or natural catastrophe.\n\nParagraph E\nThe critical importance of this failsafe was dramatically underscored in 2015 following the devastation of the International Center for Agricultural Research in the Dry Areas (ICARDA) during the Syrian civil war. Based in Aleppo, ICARDA maintained one of the world's most valuable collections of drought-tolerant wheat, barley, lentil, and chickpea landraces historically adapted to arid Mediterranean climates. When fighting destroyed the Aleppo facility, ICARDA scientists made the first-ever formal withdrawal from the Svalbard vault. They successfully retrieved 128,000 duplicate seed packets, replanted them at newly established research facilities in Lebanon and Morocco, multiplied the seed stocks, and eventually returned fresh replacement deposits to Svalbard in 2017, proving the vault's practical humanitarian utility.\n\nParagraph F\nDespite its robust design, the vault has faced environmental challenges. In 2017, unprecedented Arctic winter temperatures and heavy rain caused melting permafrost water to breach the entrance tunnel, freezing into a sheet of ice before reaching the storage vaults. While no seed packets sustained damage, the incident prompted the Norwegian government to undertake a \u20ac20 million upgrade. Engineering teams excavated the approach tunnel, replacing the corrugated steel entryway with a fully waterproof concrete access tunnel and relocating all electrical cooling infrastructure to a separate above-ground service building to eliminate internal heat accumulation.\n\nParagraph G\nToday, the Global Seed Vault preserves over 1.2 million distinct seed samples originating from nearly every sovereign state on Earth. It embodies an extraordinary triumph of international diplomatic and scientific cooperation, transcending political conflicts to preserve the collective agricultural heritage of our species for centuries to come.",
        "s3_questions": [
            {
                "id": "Q28",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph A?",
                "options": [
                    "i. Geological criteria for site selection",
                    "ii. A real-world rescue mission in the Middle East",
                    "iii. The ultimate backup policy for planetary crops",
                    "iv. Engineering upgrades after an Arctic meltwater breach",
                    "v. Defensive architecture and refrigeration specs",
                    "vi. Legal ownership and access regulations",
                    "vii. Worldwide diplomatic collaboration numbers"
                ],
                "correct_answer": "iii. The ultimate backup policy for planetary crops",
                "explanation": "Paragraph A introduces the vault as the ultimate insurance policy safeguarding agricultural genetic diversity against extinction."
            },
            {
                "id": "Q29",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph B?",
                "options": [
                    "i. Geological criteria for site selection",
                    "ii. A real-world rescue mission in the Middle East",
                    "iii. The ultimate backup policy for planetary crops",
                    "iv. Engineering upgrades after an Arctic meltwater breach",
                    "v. Defensive architecture and refrigeration specs",
                    "vi. Legal ownership and access regulations",
                    "vii. Worldwide diplomatic collaboration numbers"
                ],
                "correct_answer": "i. Geological criteria for site selection",
                "explanation": "Paragraph B explains why Svalbard was chosen: tectonic stability, elevation above sea level, and permafrost cooling."
            },
            {
                "id": "Q30",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph C?",
                "options": [
                    "i. Geological criteria for site selection",
                    "ii. A real-world rescue mission in the Middle East",
                    "iii. The ultimate backup policy for planetary crops",
                    "iv. Engineering upgrades after an Arctic meltwater breach",
                    "v. Defensive architecture and refrigeration specs",
                    "vi. Legal ownership and access regulations",
                    "vii. Worldwide diplomatic collaboration numbers"
                ],
                "correct_answer": "v. Defensive architecture and refrigeration specs",
                "explanation": "Paragraph C details the 100-metre tunnel, blast doors, minus 18 degree refrigeration, and four-ply foil packets."
            },
            {
                "id": "Q31",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph D?",
                "options": [
                    "i. Geological criteria for site selection",
                    "ii. A real-world rescue mission in the Middle East",
                    "iii. The ultimate backup policy for planetary crops",
                    "iv. Engineering upgrades after an Arctic meltwater breach",
                    "v. Defensive architecture and refrigeration specs",
                    "vi. Legal ownership and access regulations",
                    "vii. Worldwide diplomatic collaboration numbers"
                ],
                "correct_answer": "vi. Legal ownership and access regulations",
                "explanation": "Paragraph D discusses deposit ownership rules, withdrawal restrictions, and safety deposit box analogy."
            },
            {
                "id": "Q32",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph E?",
                "options": [
                    "i. Geological criteria for site selection",
                    "ii. A real-world rescue mission in the Middle East",
                    "iii. The ultimate backup policy for planetary crops",
                    "iv. Engineering upgrades after an Arctic meltwater breach",
                    "v. Defensive architecture and refrigeration specs",
                    "vi. Legal ownership and access regulations",
                    "vii. Worldwide diplomatic collaboration numbers"
                ],
                "correct_answer": "ii. A real-world rescue mission in the Middle East",
                "explanation": "Paragraph E describes the 2015 ICARDA withdrawal and rescue following the Syrian conflict."
            },
            {
                "id": "Q33",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph F?",
                "options": [
                    "i. Geological criteria for site selection",
                    "ii. A real-world rescue mission in the Middle East",
                    "iii. The ultimate backup policy for planetary crops",
                    "iv. Engineering upgrades after an Arctic meltwater breach",
                    "v. Defensive architecture and refrigeration specs",
                    "vi. Legal ownership and access regulations",
                    "vii. Worldwide diplomatic collaboration numbers"
                ],
                "correct_answer": "iv. Engineering upgrades after an Arctic meltwater breach",
                "explanation": "Paragraph F covers the 2017 meltwater intrusion and the subsequent \u20ac20 million waterproofing overhaul."
            },
            {
                "id": "Q34",
                "type": "True/False/Not Given",
                "question_text": "The Global Seed Vault was built at an elevation that protects it from potential polar ice cap melting.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph B states at 130m above sea level, it remains safe even under models predicting complete melting of ice sheets."
            },
            {
                "id": "Q35",
                "type": "True/False/Not Given",
                "question_text": "Commercial agricultural corporations can purchase seed varieties directly from the Svalbard facility.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph D explicitly states no third party possesses legal authority to access, distribute, or buy seeds."
            },
            {
                "id": "Q36",
                "type": "True/False/Not Given",
                "question_text": "Seeds inside the vault are packaged within sealed three-ply aluminum containers.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph C specifies 'specialized four-ply foil packets that are heat-sealed', not three-ply."
            },
            {
                "id": "Q37",
                "type": "True/False/Not Given",
                "question_text": "Meltwater in 2017 caused irreversible damage to thousands of grain seed packets.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph F notes water froze in the approach tunnel and 'no seed packets sustained damage'."
            },
            {
                "id": "Q38",
                "type": "Multiple Choice",
                "question_text": "Why did scientists from ICARDA make a withdrawal from Svalbard in 2015?",
                "options": [
                    "A. To cross-breed drought-resistant crops with Arctic flora",
                    "B. Because their primary seed collection in Aleppo was destroyed by war",
                    "C. To commercialize drought-tolerant seeds in international retail markets",
                    "D. Because permafrost melting threatened their original collection in Lebanon"
                ],
                "correct_answer": "B. Because their primary seed collection in Aleppo was destroyed by war",
                "explanation": "Paragraph E explains fighting destroyed the Aleppo facility, leading to the withdrawal."
            },
            {
                "id": "Q39",
                "type": "Multiple Choice",
                "question_text": "What engineering modification was implemented following the 2017 meltwater breach?",
                "options": [
                    "A. Relocating the vault to an elevated site in Norway",
                    "B. Lowering storage temperatures to minus thirty degrees",
                    "C. Replacing the entrance with a waterproof concrete tunnel and moving cooling units",
                    "D. Banning international visitors from entering the facility"
                ],
                "correct_answer": "C. Replacing the entrance with a waterproof concrete tunnel and moving cooling units",
                "explanation": "Paragraph F describes replacing corrugated steel with a waterproof concrete tunnel and moving cooling equipment."
            },
            {
                "id": "Q40",
                "type": "Sentence Completion",
                "question_text": "The seed chambers are mechanically maintained at an optimal temperature of ____________ Celsius.",
                "correct_answer": "minus eighteen degrees",
                "explanation": "Paragraph C specifies 'an optimal storage temperature of minus eighteen degrees Celsius'."
            }
        ]
    },
    {
        "suite_id": 2,
        "domain": "Urban Transit, Adult Education, Cybersecurity & Archaeological Science",
        "cambridge_ref": "Cambridge General Training Reading Benchmark (Vol 18 / 19)",
        "s1_title": "Section 1: Everyday Community Information (Texts A & B)",
        "s1_text": "Text A: Metro Transit Smart Card \u2013 Regulations, Auto-Top-Up & Off-Peak Fares\nMetro Transit operates an automated contactless smart card ticketing system across all metropolitan underground and suburban rail networks. Cardholders must tap their card on the card reader at the electronic gate when entering and exiting stations to ensure the correct fare is calculated.\n\nPeak and Off-Peak Fare Windows:\n- Peak Fares apply between 07:00 and 09:30, and between 16:30 and 19:00 on Monday through Friday.\n- Off-Peak Fares apply outside these hours, as well as all day on weekends and public bank holidays. Off-peak travel offers a standard 30% reduction on single journey fares.\n\nAuto-Top-Up Facility:\nRegistered users can link their transit card to a verified bank debit or credit card. Whenever the card balance drops below the minimum balance threshold of \u00a35.00, an automatic transfer of \u00a320.00 is initiated. Auto-top-up avoids queueing at ticket vending machines and guarantees that cardholders will never be trapped at exit gates due to insufficient funds.\n\nPenalty Fares and Forgotten Taps:\nFailing to tap in at your origin station will result in the maximum possible single journey tariff (\u00a39.80) being deducted at your destination. Commuters found travelling without a validated journey card during ticket inspections face an instant penalty fare notice of \u00a350.00.\n\nCard Replacement & Balance Protection:\nRegistered cards carry full loss protection. If a card is reported stolen online or via the 24-hour helpline (0800 555 121), the lost card is instantly cancelled, and the remaining funds are transferred to a replacement card issued for a nominal \u00a33.00 administrative fee. Unregistered cards do not qualify for balance recovery. Physical refund of unused balances requires surrender of the card within 30 days of purchase at any central customer service counter.\n\n--------------------------------------------------------------------------------\nText B: St. Jude Community College \u2013 Evening and Weekend Enrichment Courses\nSt. Jude Community College offers a wide selection of adult non-credit enrichment classes designed to foster creative skills, foreign language acquisition, and practical computing expertise.\n\nEnrollment Periods and Entry Requirements:\nEnrollment opens exactly four weeks prior to the start of each academic semester. The courses are open to all community residents aged eighteen and older; no prior academic qualifications or entrance examinations are required.\n\nTerm Structure and Attendance:\nEach term lasts for ten consecutive weeks. Classes meet once per week for a two-hour evening session (18:30 to 20:30) or on Saturday mornings (10:00 to 12:00). To qualify for a Certificate of Course Completion, attendees must maintain a minimum attendance rate of 80% across the ten scheduled sessions.\n\nDiscounts and Materials:\n- Early Bird Enrollment: A 15% discount on tuition is granted to learners who register and pay in full at least fourteen days prior to the first class.\n- Student & Senior Concessions: A 25% discount is available to full-time university students and senior citizens (aged 65+) upon presentation of valid photographic identification.\n- Workshop Supplies: Tuition covers basic classroom handouts and standard equipment. Specialized materials (such as oil paints, foreign language workbooks, or cooking ingredients) must be purchased independently by each learner as detailed in the course syllabus.\n\nWithdrawal and Cancellation:\nLearners may cancel their registration and receive a full tuition refund (minus a \u00a315 processing fee) provided written notice is submitted at least seven calendar days before the course commencement date. No refunds are granted after classes commence.",
        "s1_questions": [
            {
                "id": "Q1",
                "type": "True/False/Not Given",
                "question_text": "A commuter travelling on the metro at 10:15 on a Monday morning qualifies for off-peak ticket pricing.",
                "correct_answer": "TRUE",
                "explanation": "Text A states peak fares end at 09:30 on weekdays, so 10:15 is in the off-peak period."
            },
            {
                "id": "Q2",
                "type": "True/False/Not Given",
                "question_text": "Unregistered cardholders can recover their remaining cash balance if their card is lost.",
                "correct_answer": "FALSE",
                "explanation": "Text A states 'Unregistered cards do not qualify for balance recovery.'"
            },
            {
                "id": "Q3",
                "type": "True/False/Not Given",
                "question_text": "The penalty fare for riding without tapping in is reduced if paid within seven days.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text A mentions the \u00a350 penalty fare, but does not mention any prompt-payment discount."
            },
            {
                "id": "Q4",
                "type": "True/False/Not Given",
                "question_text": "Registered users pay a five-pound administrative fee to receive a replacement transit card.",
                "correct_answer": "FALSE",
                "explanation": "Text A states replacement cards are issued for a nominal \u00a33.00 administrative fee, not \u00a35.00."
            },
            {
                "id": "Q5",
                "type": "True/False/Not Given",
                "question_text": "Auto-top-up triggers automatically whenever the transit card balance falls below five pounds.",
                "correct_answer": "TRUE",
                "explanation": "Text A confirms auto-top-up initiates \u00a320 transfer whenever balance drops below \u00a35.00."
            },
            {
                "id": "Q6",
                "type": "True/False/Not Given",
                "question_text": "Physical cards must be returned to customer service to obtain a monetary refund.",
                "correct_answer": "TRUE",
                "explanation": "Text A states 'Physical refund of unused balances requires surrender of the card within 30 days'."
            },
            {
                "id": "Q7",
                "type": "True/False/Not Given",
                "question_text": "Enrichment courses at St. Jude Community College are open to high school students aged sixteen.",
                "correct_answer": "FALSE",
                "explanation": "Text B states courses are open to residents aged eighteen and older."
            },
            {
                "id": "Q8",
                "type": "Sentence Completion",
                "question_text": "Enrichment courses run for a total duration of ____________ weeks.",
                "correct_answer": "ten",
                "explanation": "Text B: 'Each term lasts for ten consecutive weeks.'"
            },
            {
                "id": "Q9",
                "type": "Sentence Completion",
                "question_text": "Learners who register at least two weeks before term start receive a ____________ discount.",
                "correct_answer": "15%",
                "explanation": "Text B: 'A 15% discount on tuition is granted to learners who register... at least fourteen days prior.'"
            },
            {
                "id": "Q10",
                "type": "Sentence Completion",
                "question_text": "Full-time university students can claim a ____________ fee reduction with valid identification.",
                "correct_answer": "25%",
                "explanation": "Text B: 'A 25% discount is available to full-time university students and senior citizens.'"
            },
            {
                "id": "Q11",
                "type": "Sentence Completion",
                "question_text": "All specialized art supplies and personal tools must be purchased by the ____________.",
                "correct_answer": "learner",
                "explanation": "Text B: 'Specialized materials... must be purchased independently by each learner.'"
            },
            {
                "id": "Q12",
                "type": "Sentence Completion",
                "question_text": "Students must achieve an attendance rate of at least ____________ percent to receive a certificate.",
                "correct_answer": "80",
                "explanation": "Text B: 'attendees must maintain a minimum attendance rate of 80% across the ten scheduled sessions.'"
            },
            {
                "id": "Q13",
                "type": "Sentence Completion",
                "question_text": "Refund requests after cancellation must be submitted at least ____________ days before classes start.",
                "correct_answer": "seven calendar",
                "explanation": "Text B: 'provided written notice is submitted at least seven calendar days before the course commencement date.'"
            },
            {
                "id": "Q14",
                "type": "Sentence Completion",
                "question_text": "Weekly class meetings last for ____________ hours per session.",
                "correct_answer": "two",
                "explanation": "Text B: 'Classes meet once per week for a two-hour evening session'."
            }
        ],
        "s2_title": "Section 2: Workplace Context \u2013 Data Security & Dispute Resolution (Texts C & D)",
        "s2_text": "Text C: Apex Solutions \u2013 Remote Work Data Security and Device Policy\nAs flexible remote working becomes a core component of operations at Apex Solutions, all personnel must adhere strictly to established data security protocols to safeguard client data and commercial intellectual property.\n\nVirtual Private Network (VPN) and Wi-Fi Security:\nStaff accessing corporate servers, internal databases, or cloud email systems from outside the corporate headquarters must connect exclusively through the corporate Virtual Private Network (VPN). Public, unsecured Wi-Fi networks (such as those in cafes, airports, or hotels) must never be utilized without an active VPN tunnel. Home Wi-Fi routers must be encrypted with WPA3 or WPA2 protocols.\n\nDevice Management and Screen Locks:\nEmployees are strictly prohibited from storing company documents on personal desktop computers, tablets, or external hard drives. Only company-issued laptops equipped with full-disk encryption and multi-factor authentication (MFA) may be used for work duties. Laptops are configured to lock their display screens automatically after three minutes of inactivity. When stepping away from a workstation in a public or home environment, employees must lock their screens immediately using the designated keyboard shortcut.\n\nHardware Protection and USB Restrictions:\nUnder no circumstances may unauthorized USB storage flash drives, external memory cards, or personal mobile phones be connected to company machines. The transfer of data to unauthorized storage mediums will trigger an automatic security alert and suspension of network credentials. Any lost, misplaced, or stolen company equipment must be reported directly to the IT Security Desk within two hours of discovery.\n\n--------------------------------------------------------------------------------\nText D: Apex Solutions \u2013 Workplace Grievance and Dispute Resolution Procedure\nApex Solutions is committed to providing a transparent, fair, and supportive workplace. When work-related disagreements or grievances arise, employees are encouraged to utilize the following progressive resolution stages.\n\nStage 1: Informal Discussion\nMost workplace grievances can be resolved promptly through open dialogue. An employee should first raise the matter informally with their immediate supervisor within ten working days of the incident. The supervisor must arrange an informal meeting within five working days of receiving the notification to discuss the situation and seek an amicable resolution. If the grievance involves the direct supervisor, the employee may instead contact an HR Advisor.\n\nStage 2: Formal Grievance Lodging\nIf the informal stage fails to resolve the issue, or if the gravity of the matter makes informal discussion inappropriate, the employee may submit a formal grievance. This must be submitted in writing using Official Grievance Form G-1 to the Human Resources Department within ten working days of receiving the informal outcome. An HR Manager and an independent department head will convene a formal grievance hearing within ten working days. The employee has the statutory right to be accompanied by a trade union representative or a workplace colleague.\n\nStage 3: Formal Appeals Process\nIf the employee considers the decision of the formal hearing unsatisfactory, they have seven working days from the date of the formal decision letter to lodge a written appeal. The appeal must clearly state the grounds for dissatisfaction. An Appeals Panel, consisting of a Senior Director and an independent HR representative who was not involved in previous hearings, will convene within fourteen calendar days. The decision of the Appeals Panel is final and concludes the internal grievance procedure.",
        "s2_questions": [
            {
                "id": "Q15",
                "type": "Sentence Completion",
                "question_text": "Remote staff accessing company servers must connect exclusively through the corporate ____________.",
                "correct_answer": "VPN",
                "explanation": "Text C: 'must connect exclusively through the corporate Virtual Private Network (VPN).'"
            },
            {
                "id": "Q16",
                "type": "Sentence Completion",
                "question_text": "Laptops are programmed to automatically activate screen lock after ____________ of inactivity.",
                "correct_answer": "three minutes",
                "explanation": "Text C: 'configured to lock their display screens automatically after three minutes of inactivity.'"
            },
            {
                "id": "Q17",
                "type": "Sentence Completion",
                "question_text": "Missing or stolen company laptops must be reported to the IT Security Desk within ____________.",
                "correct_answer": "two hours",
                "explanation": "Text C: 'must be reported directly to the IT Security Desk within two hours of discovery.'"
            },
            {
                "id": "Q18",
                "type": "Sentence Completion",
                "question_text": "Connecting an unauthorized ____________ to a work laptop triggers an instant security alert.",
                "correct_answer": "USB storage flash drive",
                "explanation": "Text C: 'Under no circumstances may unauthorized USB storage flash drives... be connected'."
            },
            {
                "id": "Q19",
                "type": "Sentence Completion",
                "question_text": "In Stage 1, employees must raise their concern informally within ____________ working days.",
                "correct_answer": "ten",
                "explanation": "Text D: 'raise the matter informally with their immediate supervisor within ten working days'."
            },
            {
                "id": "Q20",
                "type": "Sentence Completion",
                "question_text": "Formal grievances in Stage 2 must be submitted using ____________ to Human Resources.",
                "correct_answer": "Official Grievance Form G-1",
                "explanation": "Text D: 'submitted in writing using Official Grievance Form G-1'."
            },
            {
                "id": "Q21",
                "type": "Sentence Completion",
                "question_text": "Staff members have the right to be accompanied to formal hearings by a colleague or ____________.",
                "correct_answer": "trade union representative",
                "explanation": "Text D: 'accompanied by a trade union representative or a workplace colleague.'"
            },
            {
                "id": "Q22",
                "type": "True/False/Not Given",
                "question_text": "Employees are permitted to transfer company documents onto personal encrypted USB sticks.",
                "correct_answer": "FALSE",
                "explanation": "Text C strictly prohibits connecting unauthorized USB storage flash drives under any circumstances."
            },
            {
                "id": "Q23",
                "type": "True/False/Not Given",
                "question_text": "Home Wi-Fi routers must be secured using either WPA2 or WPA3 encryption protocols.",
                "correct_answer": "TRUE",
                "explanation": "Text C states 'Home Wi-Fi routers must be encrypted with WPA3 or WPA2 protocols.'"
            },
            {
                "id": "Q24",
                "type": "True/False/Not Given",
                "question_text": "The supervisor must schedule an informal meeting within five working days of being notified.",
                "correct_answer": "TRUE",
                "explanation": "Text D: 'The supervisor must arrange an informal meeting within five working days'."
            },
            {
                "id": "Q25",
                "type": "True/False/Not Given",
                "question_text": "Formal grievance hearings are recorded and transcribed by an automated artificial intelligence system.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text D details the composition and attendees of the formal hearing, but does not mention automated AI recording."
            },
            {
                "id": "Q26",
                "type": "True/False/Not Given",
                "question_text": "An employee has seven working days from the formal decision letter to lodge an appeal.",
                "correct_answer": "TRUE",
                "explanation": "Text D: 'they have seven working days from the date of the formal decision letter to lodge a written appeal.'"
            },
            {
                "id": "Q27",
                "type": "True/False/Not Given",
                "question_text": "An employee who is dissatisfied with Stage 3 can appeal to an external government tribunal immediately.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text D notes that Stage 3 concludes internal procedures, without stating tribunal procedures."
            }
        ],
        "s3_title": "Section 3: The Antikythera Mechanism: Unlocking the Ancient World's First Computer",
        "s3_text": "Paragraph A\nIn the spring of 1900, a crew of Greek sponge divers returning from North Africa sought shelter from a severe Mediterranean gale off the rugged coastline of Antikythera, a tiny island situated between Crete and the Peloponnese. Diving into the calm waters once the tempest subsided, diver Elias Stadiatis discovered the submerged remnants of a luxury Roman merchant ship that had foundered during the first century BCE. Among the precious marble statuary, bronze sculptures, and amphorae retrieved from the seabed was an unassuming, calcified lump of corroded bronze. When it split open several months later at the National Archaeological Museum in Athens, conservators were startled to observe intricate bronze gear teeth embedded deep within the petrified sediment.\n\nParagraph B\nFor decades, mainstream classical archaeologists dismissed the corroded fragment as an anomalous curiosity or perhaps an astrolabe dropped overboard by an Arab navigator centuries later. The consensus among 20th-century historians was that mechanical geared devices of such precision did not emerge until the cathedral clockmakers of medieval Europe in the fourteenth century. It was not until the 1950s that British historian of science Derek de Solla Price subjected the fragments to systematic scientific scrutiny. Price recognized that the device, now christened the Antikythera Mechanism, was in fact an extraordinarily sophisticated analog computing device designed to track astronomical phenomena with astonishing mathematical precision.\n\nParagraph C\nThe true technological brilliance of the mechanism remained shrouded until 2005, when an international consortium of British, Greek, and American researchers deployed advanced micro-focus X-ray computed tomography (CT) and reflectance transformation imaging. The high-resolution volumetric scans penetrated through layers of calcification, exposing over thirty interlocking bronze gears with triangular teeth varying between 15 and 223 in count. Furthermore, the scans revealed thousands of microscopic Greek inscription characters etched directly into the bronze casing plates, functioning as a comprehensive user manual explaining the planetary dials and operational calendar cycles.\n\nParagraph D\nThe mechanism operated via a hand-turned wooden crank on its wooden casing. When rotated forward or backward in time, the internal differential gear trains translated the motion onto multiple exterior dials. On the front face, pointers displayed the synchronized positions of the Sun and the Moon against the zodiac constellations, along with an ingenious rotating spherical ball that displayed the exact visual phase of the Moon. On the rear face, a large upper spiral dial tracked the 223-month Saros cycle, a Babylonian astronomical sequence used to forecast solar and lunar eclipses, including the specific hour, magnitude, and coloration of each eclipse event.\n\nParagraph E\nMost surprisingly, recent analyses uncovered a dedicated four-year dial linked directly to the Panhellenic Games, tracking the calendar for the ancient Olympic Games, the Pythian Games at Delphi, the Isthmian Games at Corinth, and the Nemean Games. The inclusion of this athletic calendar demonstrates that the Antikythera Mechanism was not merely an esoteric scholarly exercise or nautical navigation instrument, but an artifact deeply embedded within Hellenistic social, civic, and cultural life.\n\nParagraph F\nThe provenance and authorship of this masterwork remain subjects of vigorous scholarly debate. The linguistic style of the inscriptions points towards the Corinthian dialect, suggesting the mechanism may have originated in Syracuse, the Sicilian city where the legendary polymath Archimedes developed mechanical planetaria during the third century BCE. Other researchers advocate for the island of Rhodes, renowned in antiquity as a major centre for astronomical inquiry and the home of the astronomer Hipparchus, whose theories on the Moon's irregular elliptical velocity closely match the mechanical pin-and-slot gear arrangements engineered into the Antikythera device.\n\nParagraph G\nThe Antikythera Mechanism has profoundly reshaped the modern narrative concerning classical antiquity's technological capabilities. It proves that Hellenistic civilization possessed an empirical understanding of mechanical engineering and gear kinematics that was subsequently lost for more than a millennium following the collapse of the Roman Empire. Far from being a primitive civilization restricted to simple tools, the ancient Mediterranean world stood on the threshold of a mechanical revolution that history failed to sustain.",
        "s3_questions": [
            {
                "id": "Q28",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph A?",
                "options": [
                    "i. Initial discovery among shipwreck treasures",
                    "ii. Academic skepticism and delayed recognition",
                    "iii. Modern X-ray tomography reveals inner gears",
                    "iv. Operational dials and astronomical forecasts",
                    "v. Civic and cultural athletic calendars",
                    "vi. Competing hypotheses of ancient authorship",
                    "vii. Overturning assumptions about classical science"
                ],
                "correct_answer": "i. Initial discovery among shipwreck treasures",
                "explanation": "Paragraph A describes sponge divers seeking shelter and discovering the shipwreck and bronze artifact."
            },
            {
                "id": "Q29",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph B?",
                "options": [
                    "i. Initial discovery among shipwreck treasures",
                    "ii. Academic skepticism and delayed recognition",
                    "iii. Modern X-ray tomography reveals inner gears",
                    "iv. Operational dials and astronomical forecasts",
                    "v. Civic and cultural athletic calendars",
                    "vi. Competing hypotheses of ancient authorship",
                    "vii. Overturning assumptions about classical science"
                ],
                "correct_answer": "ii. Academic skepticism and delayed recognition",
                "explanation": "Paragraph B explains how archaeologists initially dismissed it until Derek de Solla Price investigated it."
            },
            {
                "id": "Q30",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph C?",
                "options": [
                    "i. Initial discovery among shipwreck treasures",
                    "ii. Academic skepticism and delayed recognition",
                    "iii. Modern X-ray tomography reveals inner gears",
                    "iv. Operational dials and astronomical forecasts",
                    "v. Civic and cultural athletic calendars",
                    "vi. Competing hypotheses of ancient authorship",
                    "vii. Overturning assumptions about classical science"
                ],
                "correct_answer": "iii. Modern X-ray tomography reveals inner gears",
                "explanation": "Paragraph C details the 2005 micro-focus X-ray CT scans revealing gears and inscriptions."
            },
            {
                "id": "Q31",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph D?",
                "options": [
                    "i. Initial discovery among shipwreck treasures",
                    "ii. Academic skepticism and delayed recognition",
                    "iii. Modern X-ray tomography reveals inner gears",
                    "iv. Operational dials and astronomical forecasts",
                    "v. Civic and cultural athletic calendars",
                    "vi. Competing hypotheses of ancient authorship",
                    "vii. Overturning assumptions about classical science"
                ],
                "correct_answer": "iv. Operational dials and astronomical forecasts",
                "explanation": "Paragraph D explains how the dials operated to track the Sun, Moon phases, and eclipse predictions."
            },
            {
                "id": "Q32",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph E?",
                "options": [
                    "i. Initial discovery among shipwreck treasures",
                    "ii. Academic skepticism and delayed recognition",
                    "iii. Modern X-ray tomography reveals inner gears",
                    "iv. Operational dials and astronomical forecasts",
                    "v. Civic and cultural athletic calendars",
                    "vi. Competing hypotheses of ancient authorship",
                    "vii. Overturning assumptions about classical science"
                ],
                "correct_answer": "v. Civic and cultural athletic calendars",
                "explanation": "Paragraph E focuses on the Olympic and Panhellenic games calendar dial."
            },
            {
                "id": "Q33",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph F?",
                "options": [
                    "i. Initial discovery among shipwreck treasures",
                    "ii. Academic skepticism and delayed recognition",
                    "iii. Modern X-ray tomography reveals inner gears",
                    "iv. Operational dials and astronomical forecasts",
                    "v. Civic and cultural athletic calendars",
                    "vi. Competing hypotheses of ancient authorship",
                    "vii. Overturning assumptions about classical science"
                ],
                "correct_answer": "vi. Competing hypotheses of ancient authorship",
                "explanation": "Paragraph F discusses whether Archimedes in Syracuse or Hipparchus in Rhodes created it."
            },
            {
                "id": "Q34",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph G?",
                "options": [
                    "i. Initial discovery among shipwreck treasures",
                    "ii. Academic skepticism and delayed recognition",
                    "iii. Modern X-ray tomography reveals inner gears",
                    "iv. Operational dials and astronomical forecasts",
                    "v. Civic and cultural athletic calendars",
                    "vi. Competing hypotheses of ancient authorship",
                    "vii. Overturning assumptions about classical science"
                ],
                "correct_answer": "vii. Overturning assumptions about classical science",
                "explanation": "Paragraph G summarizes how the device changed historical perspectives on ancient technology."
            },
            {
                "id": "Q35",
                "type": "Multiple Choice",
                "question_text": "Early twentieth-century archaeologists initially doubted the authenticity of the mechanism because:",
                "options": [
                    "A. The bronze was in too pristine a condition to be authentic.",
                    "B. They believed precision geared machinery was not invented until the medieval era.",
                    "C. No written records in Athens mentioned any calculating machines.",
                    "D. It was discovered alongside modern navigational instruments."
                ],
                "correct_answer": "B. They believed precision geared machinery was not invented until the medieval era.",
                "explanation": "Paragraph B states historians believed geared devices of such precision did not emerge until fourteenth-century cathedral clocks."
            },
            {
                "id": "Q36",
                "type": "Multiple Choice",
                "question_text": "The CT scans conducted in 2005 were significant primarily because they:",
                "options": [
                    "A. Reconstructed the wooden outer case without dismantling it.",
                    "B. Disproved Derek de Solla Price's initial theories on gear counts.",
                    "C. Revealed over 30 internal gears and thousands of instructional characters.",
                    "D. Proved the ship sank due to an explosion in the cargo hold."
                ],
                "correct_answer": "C. Revealed over 30 internal gears and thousands of instructional characters.",
                "explanation": "Paragraph C states scans exposed over thirty interlocking gears and thousands of microscopic Greek characters."
            },
            {
                "id": "Q37",
                "type": "Multiple Choice",
                "question_text": "The presence of the Panhellenic Games dial indicates that the machine:",
                "options": [
                    "A. Was used exclusively for sports wagering in Olympic stadiums.",
                    "B. Was intended for wider societal and cultural relevance beyond astronomy.",
                    "C. Was fabricated during the reign of Emperor Nero.",
                    "D. Was carried as a religious trophy won in ancient athletic contests."
                ],
                "correct_answer": "B. Was intended for wider societal and cultural relevance beyond astronomy.",
                "explanation": "Paragraph E states it proves the artifact was deeply embedded within Hellenistic social, civic, and cultural life."
            },
            {
                "id": "Q38",
                "type": "True/False/Not Given",
                "question_text": "The sponge divers were initially seeking refuge from a gale when they moored near Antikythera.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph A states the crew sought shelter from a severe Mediterranean gale."
            },
            {
                "id": "Q39",
                "type": "True/False/Not Given",
                "question_text": "Archaeologists have located Archimedes' signature engraved on the inner gears.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph F notes Syracuse and Archimedes are theories based on dialect, with no signature found."
            },
            {
                "id": "Q40",
                "type": "True/False/Not Given",
                "question_text": "The rear Saros dial was engineered to forecast the specific hour of solar and lunar eclipses.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph D confirms it tracked the 223-month Saros cycle forecasting hour, magnitude, and color."
            }
        ]
    },
    {
        "suite_id": 3,
        "domain": "Environmental Recycling, Parks, Professional Appraisals & Solar Desalination",
        "cambridge_ref": "Cambridge General Training Reading Benchmark (Vol 18 / 19)",
        "s1_title": "Section 1: Everyday Community Information (Texts A & B)",
        "s1_text": "Text A: Municipal Household Recycling and Waste Collection Regulations\nThe City Borough Council operates a mandatory three-stream kerbside collection scheme to minimize landfill disposal and support circular economy recycling targets.\n\nKerbside Wheeled Bins:\n- Blue-Lidded Bin (Clean Recyclables): Dry paper, cardboard boxes (flattened), clean aluminium and tin cans, and rigid plastic beverage bottles. Materials must be placed loose into the bin; recyclables tied inside black plastic bin bags will be rejected.\n- Brown-Lidded Bin (Organic Garden & Food Waste): Grass clippings, hedge trimmings, raw vegetable peelings, and coffee grounds. Meat bones, plastic bags, and pet feces are strictly prohibited and will contaminate the municipal composting facility.\n- Grey-Lidded Bin (Non-Recyclable Residuals): General non-hazardous domestic waste that cannot be repurposed or recycled.\n\nCollection Schedule and Placement Rules:\nBins must be wheeled onto the public pavement outside your property boundary line by 07:00 on your designated weekly collection morning, with bin handles turned toward the street. Collection crews will not enter private driveways or rear gardens. Lids must be fully closed; overfilled bins with raised lids will not be emptied due to mechanical loading safety regulations.\n\nHazardous Chemicals and Electronics:\nBatteries, motor oils, solvents, and electronic appliances (WEEE) must never be deposited in household bins. These items must be brought directly to the Borough Civic Amenity Centre on Mill Road, open Tuesday through Sunday from 08:30 to 17:00.\n\n--------------------------------------------------------------------------------\nText B: Highfield Country Park \u2013 Visitor Regulations and Trail Etiquette\nHighfield Country Park encompasses 450 hectares of ancient deciduous woodland, wildflower meadows, and scenic freshwater lakes. To protect wildlife habitats and ensure a pleasant visit for all patrons, guests are requested to respect park regulations.\n\nOpening Hours and Vehicle Parking:\nThe park gates open daily at 07:00 and close at dusk (posted times range from 17:00 in December to 21:30 in midsummer). Automatic vehicle barriers lock precisely thirty minutes after closing time. Overnight parking is prohibited; vehicles remaining inside the gates after lockup are subject to a \u00a375 release fee.\n\nTrail Etiquette and Cycling:\nPedestrians enjoy right-of-way across all trails. Cyclists must remain strictly on the paved Blue Perimeter Loop and must not exceed the posted 15 km/h speed limit. Cycling across unpaved woodland footpaths and equestrian bridleways is strictly forbidden to prevent soil erosion and disturbance to ground-nesting birds.\n\nDog Walking Guidelines:\nDogs are warmly welcomed in the park but must be kept on a lead no longer than two metres around the Lakeside Nature Reserve and children's playground zones. Owners are legally required to clean up immediately after their pets using the red disposal bins located at every trailhead.\n\nBarbecues and Open Fires:\nDisposable charcoal barbecues, open campfires, and portable camping gas stoves are completely banned across the entire park reserve throughout the year to eliminate wildfire hazards.",
        "s1_questions": [
            {
                "id": "Q1",
                "type": "True/False/Not Given",
                "question_text": "Recyclable items in the blue-lidded bin should be enclosed within black plastic bags.",
                "correct_answer": "FALSE",
                "explanation": "Text A states: 'recyclables tied inside black plastic bin bags will be rejected.'"
            },
            {
                "id": "Q2",
                "type": "True/False/Not Given",
                "question_text": "Household meat scraps and cooked bones can be composted in the brown-lidded bin.",
                "correct_answer": "FALSE",
                "explanation": "Text A states: 'Meat bones, plastic bags, and pet feces are strictly prohibited'."
            },
            {
                "id": "Q3",
                "type": "True/False/Not Given",
                "question_text": "Collection crews will enter private gardens to collect bins for senior citizens.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text A notes crews will not enter private driveways, but does not mention special assistance for seniors."
            },
            {
                "id": "Q4",
                "type": "True/False/Not Given",
                "question_text": "Bins with lids that do not close completely will be left unemptied by collection staff.",
                "correct_answer": "TRUE",
                "explanation": "Text A states: 'overfilled bins with raised lids will not be emptied'."
            },
            {
                "id": "Q5",
                "type": "True/False/Not Given",
                "question_text": "The Civic Amenity Centre on Mill Road accepts discarded electrical appliances.",
                "correct_answer": "TRUE",
                "explanation": "Text A specifies electronic appliances (WEEE) must be brought to Mill Road."
            },
            {
                "id": "Q6",
                "type": "True/False/Not Given",
                "question_text": "Vehicles locked inside Highfield Country Park overnight can be released without charge.",
                "correct_answer": "FALSE",
                "explanation": "Text B states vehicles remaining after lockup are subject to a \u00a375 release fee."
            },
            {
                "id": "Q7",
                "type": "True/False/Not Given",
                "question_text": "Cyclists are permitted to ride on unpaved forest trails if they yield to pedestrians.",
                "correct_answer": "FALSE",
                "explanation": "Text B states: 'Cycling across unpaved woodland footpaths... is strictly forbidden'."
            },
            {
                "id": "Q8",
                "type": "Sentence Completion",
                "question_text": "Household bins must be positioned on the pavement by ____________ on collection mornings.",
                "correct_answer": "07:00",
                "explanation": "Text A: 'must be wheeled onto the public pavement... by 07:00'."
            },
            {
                "id": "Q9",
                "type": "Sentence Completion",
                "question_text": "Bin handles must be oriented facing toward the ____________ when positioned outside.",
                "correct_answer": "street",
                "explanation": "Text A: 'with bin handles turned toward the street.'"
            },
            {
                "id": "Q10",
                "type": "Sentence Completion",
                "question_text": "The Mill Road Civic Amenity Centre is closed on ____________ each week.",
                "correct_answer": "Mondays",
                "explanation": "Text A states it is open Tuesday through Sunday, meaning closed Mondays."
            },
            {
                "id": "Q11",
                "type": "Sentence Completion",
                "question_text": "In December, Highfield Country Park vehicle gates close at ____________.",
                "correct_answer": "17:00",
                "explanation": "Text B: 'posted times range from 17:00 in December to 21:30 in midsummer'."
            },
            {
                "id": "Q12",
                "type": "Sentence Completion",
                "question_text": "Cyclists on the Blue Perimeter Loop must observe a maximum speed of ____________ km/h.",
                "correct_answer": "15",
                "explanation": "Text B: 'must not exceed the posted 15 km/h speed limit.'"
            },
            {
                "id": "Q13",
                "type": "Sentence Completion",
                "question_text": "In bird nesting and playground zones, dogs must be kept on leads under ____________ metres long.",
                "correct_answer": "two",
                "explanation": "Text B: 'must be kept on a lead no longer than two metres'."
            },
            {
                "id": "Q14",
                "type": "Sentence Completion",
                "question_text": "Disposable charcoal barbecues are banned throughout the year to mitigate ____________ hazards.",
                "correct_answer": "wildfire",
                "explanation": "Text B: 'completely banned across the entire park reserve... to eliminate wildfire hazards.'"
            }
        ],
        "s2_title": "Section 2: Workplace Context \u2013 Appraisals & Sickness Absence (Texts C & D)",
        "s2_text": "Text C: Meridian Enterprises \u2013 Annual Performance Review and Professional Development Framework\nMeridian Enterprises conducts formal Performance Development Reviews (PDR) annually during the month of October to assess employee contributions, recognize achievements, and formulate personalized career development roadmaps.\n\nThe Three Pillars of the Review:\n1. Retrospective Achievement Evaluation: The employee and line manager evaluate individual performance against key performance indicators (KPIs) and objectives established during the previous review cycle.\n2. 360-Degree Peer Feedback: Anonymous feedback gathered from at least three colleagues and internal stakeholders is reviewed to evaluate teamwork, communication effectiveness, and interpersonal collaboration.\n3. Future Goal Setting and SMART Targets: Establishing three to five SMART objectives (Specific, Measurable, Achievable, Relevant, Time-bound) for the upcoming operating year.\n\nSelf-Evaluation Submission:\nEmployees must complete and submit their electronic Self-Assessment Form via the internal HR portal at least ten working days prior to their scheduled appraisal interview. Failure to submit the self-appraisal on time will result in the postponement of the meeting and may delay eligibility for annual performance-related salary increments.\n\nPost-Review Documentation:\nFollowing the formal interview, the line manager prepares a summary review document within five working days. The employee has three working days to review the appraisal notes, add written comments, and sign off digitally. Signed reviews are stored permanently in the employee's central personnel file.\n\n--------------------------------------------------------------------------------\nText D: Meridian Enterprises \u2013 Workplace Sickness Absence and Phased Return Policy\nThis policy outlines the protocols employees and managers must follow when illness prevents an employee from performing their contractual duties.\n\nNotification Requirements:\nAn employee unable to attend work due to acute sickness or injury must notify their line manager via telephone by 08:30 on the first working day of absence. Text messages, emails, or messages left via third parties are unacceptable, except in circumstances involving emergency hospitalization. The employee must indicate the nature of the illness and the expected date of return.\n\nMedical Certification:\n- Self-Certification (Days 1 to 7): For absences of up to seven consecutive calendar days (including non-working weekend days), employees must complete a Self-Certification Absence Form upon resuming work.\n- Statement of Fitness for Work (Fit Note): For absences exceeding seven consecutive calendar days, employees must obtain a medical 'Fit Note' issued by a certified general practitioner or hospital clinician. Consecutive Fit Notes must be provided without gaps until the employee is medically cleared to resume duties.\n\nReturn-to-Work Interview:\nOn the day an employee returns to duty after any period of sickness, the manager must conduct an informal Return-to-Work Interview. This ensures the employee is fit to resume work and discusses whether workplace adjustments are warranted.\n\nPhased Return and Reasonable Adjustments:\nFollowing long-term illness (defined as continuous absence exceeding four weeks), Occupational Health may recommend a phased return over a four-to-six-week period. This may involve reduced working hours, temporary light duties, or hybrid work arrangements while retaining full baseline salary.",
        "s2_questions": [
            {
                "id": "Q15",
                "type": "Sentence Completion",
                "question_text": "Annual Performance Development Reviews are conducted during the month of ____________.",
                "correct_answer": "October",
                "explanation": "Text C: 'conducts formal Performance Development Reviews (PDR) annually during the month of October'."
            },
            {
                "id": "Q16",
                "type": "Sentence Completion",
                "question_text": "Peer feedback is gathered anonymously from a minimum of ____________ workplace colleagues.",
                "correct_answer": "three",
                "explanation": "Text C: 'Anonymous feedback gathered from at least three colleagues and internal stakeholders'."
            },
            {
                "id": "Q17",
                "type": "Sentence Completion",
                "question_text": "Employees must submit their self-assessment at least ____________ working days before the interview.",
                "correct_answer": "ten",
                "explanation": "Text C: 'submit their electronic Self-Assessment Form... at least ten working days prior'."
            },
            {
                "id": "Q18",
                "type": "Sentence Completion",
                "question_text": "Line managers must provide the written appraisal summary within ____________ working days.",
                "correct_answer": "five",
                "explanation": "Text C: 'prepares a summary review document within five working days.'"
            },
            {
                "id": "Q19",
                "type": "Sentence Completion",
                "question_text": "Sickness absence notification must be communicated by ____________ on the first morning.",
                "correct_answer": "08:30",
                "explanation": "Text D: 'must notify their line manager via telephone by 08:30 on the first working day'."
            },
            {
                "id": "Q20",
                "type": "Sentence Completion",
                "question_text": "Absences extending beyond ____________ calendar days require a certified doctor's Fit Note.",
                "correct_answer": "seven",
                "explanation": "Text D: 'For absences exceeding seven consecutive calendar days, employees must obtain a medical Fit Note'."
            },
            {
                "id": "Q21",
                "type": "Sentence Completion",
                "question_text": "Continuous sickness lasting over four weeks is formally classified as ____________ illness.",
                "correct_answer": "long-term",
                "explanation": "Text D: 'Following long-term illness (defined as continuous absence exceeding four weeks)'."
            },
            {
                "id": "Q22",
                "type": "True/False/Not Given",
                "question_text": "Employees who submit late self-evaluations risk delaying their performance bonus reviews.",
                "correct_answer": "TRUE",
                "explanation": "Text C states late submission may delay eligibility for annual performance-related salary increments."
            },
            {
                "id": "Q23",
                "type": "True/False/Not Given",
                "question_text": "Employees are permitted to notify their team via SMS text message if suffering a migraine.",
                "correct_answer": "FALSE",
                "explanation": "Text D states: 'Text messages, emails, or messages left via third parties are unacceptable'."
            },
            {
                "id": "Q24",
                "type": "True/False/Not Given",
                "question_text": "Weekend days are counted when calculating the seven-day self-certification threshold.",
                "correct_answer": "TRUE",
                "explanation": "Text D specifies 'including non-working weekend days'."
            },
            {
                "id": "Q25",
                "type": "True/False/Not Given",
                "question_text": "Managers must conduct a return-to-work interview whenever an employee returns from sick leave.",
                "correct_answer": "TRUE",
                "explanation": "Text D: 'On the day an employee returns to duty after any period of sickness, the manager must conduct an informal Return-to-Work Interview.'"
            },
            {
                "id": "Q26",
                "type": "True/False/Not Given",
                "question_text": "During a phased return to work, employees receive a 20% reduction in basic salary.",
                "correct_answer": "FALSE",
                "explanation": "Text D states phased return may involve reduced hours 'while retaining full baseline salary.'"
            },
            {
                "id": "Q27",
                "type": "True/False/Not Given",
                "question_text": "Employees may request paid compassionate leave in the event of family bereavement.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text D covers sickness absence and phased return, but makes no mention of bereavement leave."
            }
        ],
        "s3_title": "Section 3: Solar Desalination: Providing Clean Drinking Water in Arid Coastal Regions",
        "s3_text": "Paragraph A\nAcross the arid regions of the Middle East, North Africa, and coastal Australia, fresh potable water represents a more precious commodity than petroleum. Traditional thermal desalination and reverse osmosis (RO) facilities produce immense quantities of freshwater, yet they remain tethered to fossil-fuel-fired power grids and diesel generators. Conventional desalination operations consume massive amounts of electrical power and emit tens of millions of metric tons of greenhouse gases annually. As climate change intensifies desertification and groundwater aquifers suffer irreversible saline intrusion, environmental engineers are turning toward solar desalination as a sustainable lifeline for thirsty populations.\n\nParagraph B\nSolar desalination technologies broadly bifurcate into direct and indirect thermodynamic systems. Direct solar desalination employs solar stills\u2014shallow, insulated basins covered by angled transparent glass or polycarbonate panes. Solar radiation penetrates the glazing, warming the saline feed water and causing evaporation. The evaporated water vapor condenses against the cooler inner surface of the transparent cover, trickling down into collection channels as pure distilled water. While direct solar stills are mechanically straightforward, inexpensive to construct, and devoid of moving components, their production yield is inherently modest, generating between two and four litres of water per square metre of collector area per day.\n\nParagraph C\nIn contrast, indirect solar desalination decouples energy collection from the phase-change distillation process. These industrial-scale facilities utilize fields of parabolic trough collectors or photovoltaic (PV) solar arrays to power high-efficiency membrane systems. Concentrated solar power (CSP) installations harness banks of mirrored heliostats to focus thermal energy onto molten salt heat exchangers, creating superheated steam that drives multi-stage flash (MSF) or multi-effect distillation (MED) chambers. Alternatively, photovoltaic-reverse osmosis (PV-RO) systems harness sunlight to generate direct electrical currents, driving high-pressure reciprocating pumps that force saltwater through semi-permeable polyamide membranes at pressures exceeding 70 atmospheres.\n\nParagraph D\nDespite its carbon-neutral credentials, solar desalination confronts formidable technological hurdles. The primary limitation of solar energy is its diurnal intermittency: sunlight is available only during daylight hours, whereas membrane filtration systems operate with maximum economic and chemical efficiency under uninterrupted, steady-state hydraulic pressure. Rapid cycling between operational pressures causes thermal fatigue and accelerates membrane compaction. To combat this limitation, state-of-the-art facilities integrate thermal energy storage using insulated liquid molten salts or utility-scale lithium-iron-phosphate battery storage arrays, enabling 24-hour continuous operations.\n\nParagraph E\nAnother grave environmental consequence centers on brine disposal. For every litre of purified drinking water produced, approximately one litre of hyper-saline brine\u2014concentrated to twice the salinity of natural seawater and laden with chemical anti-scalants and corrosion inhibitors\u2014must be discharged. Dumping concentrated brine directly into shallow coastal bays depletes dissolved oxygen levels and devastates benthic marine ecosystems, notably seagrass beds and coral reefs. Cutting-edge facilities are pioneering zero-liquid-discharge (ZLD) technologies, using secondary crystalline evaporators to extract solid industrial salts, magnesium, and lithium from the residual brine, transforming an ecological hazard into commercial minerals.\n\nParagraph F\nThe economics of solar desalination have shifted dramatically over the past two decades. Driven by the precipitous 85% decline in photovoltaic module manufacturing costs and breakthroughs in energy recovery devices (ERDs), the levelized cost of solar-desalinated water has plunged from over $3.00 per cubic metre in the year 2000 to approximately $0.55 per cubic metre in contemporary high-capacity installations. Consequently, nations across the Arabian Gulf, which previously relied almost exclusively on gas-fired thermal plants, are currently investing billions of dollars in gigawatt-scale solar desalination complexes.\n\nParagraph G\nLooking toward the future, decentralized solar desalination holds transformative potential for remote, off-grid communities. Modular, containerized solar desalination units capable of purifying brackish groundwater can now be transported on standard flatbed trucks and deployed in isolated villages within hours. By democratizing access to safe drinking water without requiring expensive national electrical grids or pipeline networks, solar water technologies represent one of humanity's most potent tools for climate adaptation in the twenty-first century.",
        "s3_questions": [
            {
                "id": "Q28",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph A?",
                "options": [
                    "i. The ecological dilemma of conventional desalination",
                    "ii. Direct solar stills: Simplicity versus low yield",
                    "iii. Industrial indirect solar and membrane architectures",
                    "iv. Addressing energy intermittency through thermal storage",
                    "v. Environmental threats of hyper-saline brine discharge",
                    "vi. Plummeting production costs and economic viability",
                    "vii. Decentralized off-grid humanitarian solutions"
                ],
                "correct_answer": "i. The ecological dilemma of conventional desalination",
                "explanation": "Paragraph A introduces how fossil-fuel-powered desalination causes severe carbon emissions, prompting solar alternatives."
            },
            {
                "id": "Q29",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph B?",
                "options": [
                    "i. The ecological dilemma of conventional desalination",
                    "ii. Direct solar stills: Simplicity versus low yield",
                    "iii. Industrial indirect solar and membrane architectures",
                    "iv. Addressing energy intermittency through thermal storage",
                    "v. Environmental threats of hyper-saline brine discharge",
                    "vi. Plummeting production costs and economic viability",
                    "vii. Decentralized off-grid humanitarian solutions"
                ],
                "correct_answer": "ii. Direct solar stills: Simplicity versus low yield",
                "explanation": "Paragraph B outlines direct solar stills and notes their low daily yield of 2-4 litres."
            },
            {
                "id": "Q30",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph C?",
                "options": [
                    "i. The ecological dilemma of conventional desalination",
                    "ii. Direct solar stills: Simplicity versus low yield",
                    "iii. Industrial indirect solar and membrane architectures",
                    "iv. Addressing energy intermittency through thermal storage",
                    "v. Environmental threats of hyper-saline brine discharge",
                    "vi. Plummeting production costs and economic viability",
                    "vii. Decentralized off-grid humanitarian solutions"
                ],
                "correct_answer": "iii. Industrial indirect solar and membrane architectures",
                "explanation": "Paragraph C describes CSP, molten salts, and PV-RO membrane configurations."
            },
            {
                "id": "Q31",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph D?",
                "options": [
                    "i. The ecological dilemma of conventional desalination",
                    "ii. Direct solar stills: Simplicity versus low yield",
                    "iii. Industrial indirect solar and membrane architectures",
                    "iv. Addressing energy intermittency through thermal storage",
                    "v. Environmental threats of hyper-saline brine discharge",
                    "vi. Plummeting production costs and economic viability",
                    "vii. Decentralized off-grid humanitarian solutions"
                ],
                "correct_answer": "iv. Addressing energy intermittency through thermal storage",
                "explanation": "Paragraph D discusses solar intermittency and battery/molten salt storage solutions."
            },
            {
                "id": "Q32",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph E?",
                "options": [
                    "i. The ecological dilemma of conventional desalination",
                    "ii. Direct solar stills: Simplicity versus low yield",
                    "iii. Industrial indirect solar and membrane architectures",
                    "iv. Addressing energy intermittency through thermal storage",
                    "v. Environmental threats of hyper-saline brine discharge",
                    "vi. Plummeting production costs and economic viability",
                    "vii. Decentralized off-grid humanitarian solutions"
                ],
                "correct_answer": "v. Environmental threats of hyper-saline brine discharge",
                "explanation": "Paragraph E focuses on hyper-saline brine hazards and zero-liquid-discharge innovations."
            },
            {
                "id": "Q33",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph F?",
                "options": [
                    "i. The ecological dilemma of conventional desalination",
                    "ii. Direct solar stills: Simplicity versus low yield",
                    "iii. Industrial indirect solar and membrane architectures",
                    "iv. Addressing energy intermittency through thermal storage",
                    "v. Environmental threats of hyper-saline brine discharge",
                    "vi. Plummeting production costs and economic viability",
                    "vii. Decentralized off-grid humanitarian solutions"
                ],
                "correct_answer": "vi. Plummeting production costs and economic viability",
                "explanation": "Paragraph F covers the decline in PV costs and drop from $3.00 to $0.55 per cubic metre."
            },
            {
                "id": "Q34",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph G?",
                "options": [
                    "i. The ecological dilemma of conventional desalination",
                    "ii. Direct solar stills: Simplicity versus low yield",
                    "iii. Industrial indirect solar and membrane architectures",
                    "iv. Addressing energy intermittency through thermal storage",
                    "v. Environmental threats of hyper-saline brine discharge",
                    "vi. Plummeting production costs and economic viability",
                    "vii. Decentralized off-grid humanitarian solutions"
                ],
                "correct_answer": "vii. Decentralized off-grid humanitarian solutions",
                "explanation": "Paragraph G discusses containerized, off-grid mobile units for remote villages."
            },
            {
                "id": "Q35",
                "type": "Multiple Choice",
                "question_text": "Direct solar stills are characterized by their:",
                "options": [
                    "A. High operational maintenance costs due to complex turbines.",
                    "B. Simple design combined with relatively low daily freshwater yields.",
                    "C. Heavy reliance on grid-connected electrical compression pumps.",
                    "D. Inability to remove salt from ocean water."
                ],
                "correct_answer": "B. Simple design combined with relatively low daily freshwater yields.",
                "explanation": "Paragraph B notes direct solar stills are mechanically straightforward but yield only 2-4 litres per sq metre."
            },
            {
                "id": "Q36",
                "type": "Multiple Choice",
                "question_text": "Why is operating RO membrane plants intermittently undesirable?",
                "options": [
                    "A. The solar panels overheat when pumps shut down.",
                    "B. Constant pressure fluctuations cause material fatigue and damage membranes.",
                    "C. Stored water turns brackish within three hours of pump cessation.",
                    "D. Chemical anti-scalants solidify into crystals at atmospheric pressure."
                ],
                "correct_answer": "B. Constant pressure fluctuations cause material fatigue and damage membranes.",
                "explanation": "Paragraph D states rapid cycling between operational pressures causes thermal fatigue and accelerates membrane compaction."
            },
            {
                "id": "Q37",
                "type": "Multiple Choice",
                "question_text": "Zero-Liquid-Discharge (ZLD) systems benefit the environment by:",
                "options": [
                    "A. Neutralizing brine before releasing it directly into coral reefs.",
                    "B. Eliminating brine dumping by evaporating liquid to harvest solid minerals.",
                    "C. Pumping hypersaline water into deep underground tectonic vaults.",
                    "D. Converting salt crystals into organic fertilizers."
                ],
                "correct_answer": "B. Eliminating brine dumping by evaporating liquid to harvest solid minerals.",
                "explanation": "Paragraph E explains ZLD uses secondary evaporators to extract solid industrial salts, avoiding ocean dumping."
            },
            {
                "id": "Q38",
                "type": "True/False/Not Given",
                "question_text": "PV module costs have dropped by approximately 85% over the past two decades.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph F cites the 'precipitous 85% decline in photovoltaic module manufacturing costs.'"
            },
            {
                "id": "Q39",
                "type": "True/False/Not Given",
                "question_text": "The cost of desalinated water in modern solar installations is currently $0.55 per cubic metre.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph F confirms it has plunged to approximately $0.55 per cubic metre."
            },
            {
                "id": "Q40",
                "type": "True/False/Not Given",
                "question_text": "Containerized solar desalination units require specialized crane ships for deployment.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph G states they can be transported on standard flatbed trucks and deployed within hours."
            }
        ]
    },
    {
        "suite_id": 4,
        "domain": "Hospitality Services, Mountain Safety, Corporate Travel & Evolutionary Psychology",
        "cambridge_ref": "Cambridge General Training Reading Benchmark (Vol 18 / 19)",
        "s1_title": "Section 1: Everyday Community Information (Texts A & B)",
        "s1_text": "Text A: Highland View Hotel \u2013 Guest Information and Dining Timetable\nWelcome to Highland View Hotel. Please review our house policies and dining hours to ensure a relaxing and comfortable stay.\n\nCheck-In and Check-Out Protocols:\n- Standard check-in commences at 15:00. Guests arriving earlier are invited to leave their luggage with the concierge free of charge.\n- Express check-out is at 11:00 on the day of departure. Late departures up to 13:30 may be requested at reception subject to room availability, incurring a supplemental fee of \u00a325.00.\n\nDining Room Schedules:\n- Complimentary Continental & Cooked Breakfast: Served in the Oak Room from 07:00 to 09:30 on weekdays, and from 07:30 to 10:30 on Saturdays, Sundays, and public bank holidays.\n- Afternoon Cream Tea: Served daily in the Drawing Room between 14:30 and 16:30. Reservations must be booked at least two hours in advance.\n- Dinner Service: The Glenview Bistro opens for evening reservations from 18:00 to 21:30. Smart casual attire is requested; athletic sportswear and swimwear are strictly disallowed.\n\nLeisure Amenities & Spa:\nThe indoor thermal pool, hydropool, and Scandinavian sauna are available to all hotel residents between 06:30 and 21:00 daily. Children under sixteen must be accompanied by a supervising adult at all times. Pool towels are provided at the spa reception; room towels must not be removed from guest suites.\n\n--------------------------------------------------------------------------------\nText B: Highland Mountain Adventure Club \u2013 Guided Ridge Walks and Equipment Rules\nThe Highland Mountain Adventure Club organizes weekly guided hillwalking expeditions for trekkers of varying experience levels across the Cairngorm mountain range.\n\nExcursion Classifications and Physical Fitness:\n- Grade 1 (Introductory): Lowland valley walks, 8 to 12 kilometres, gentle gradients. Suitable for beginners with reasonable general fitness.\n- Grade 2 (Intermediate): High moorland routes, 14 to 18 kilometres, rocky ascents of up to 600 metres. Participants must be accustomed to 5-6 hours of continuous walking.\n- Grade 3 (Advanced Ridge Scrambling): Exposed ridgelines, steep scree slopes, and scrambling sections requiring handholds. Not suitable for anyone suffering from vertigo or cardiovascular ailments.\n\nMandatory Equipment and Gear Checks:\nEvery trekker must submit to a gear inspection by the Lead Guide thirty minutes prior to departure at the club base. Guides reserve the right to exclude any participant whose gear is judged substandard.\n1. Waterproof outerwear: High-performance hooded jacket and waterproof trousers made from breathable membrane fabrics (Gore-Tex or equivalent). Plastic ponchos are forbidden.\n2. Footwear: Sturdy ankle-high trekking boots with deep tread Vibram rubber soles. Running sneakers, canvas shoes, or sandals will result in immediate disqualification without refund.\n3. Rucksack Contents: Minimum two litres of drinking water, high-energy emergency rations, spare warm thermal fleece layer, whistle, survival foil bivy bag, and a working LED headtorch with spare batteries.\n\nWeather Cancellations and Route Alterations:\nMountain weather changes rapidly. If gale-force winds exceeding 60 km/h or electrical thunderstorms are forecast, expeditions will be rerouted to lower woodland trails or postponed. Notice of cancellations will be issued via SMS text alert by 06:00 on the morning of the climb.",
        "s1_questions": [
            {
                "id": "Q1",
                "type": "True/False/Not Given",
                "question_text": "Hotel guests arriving before 15:00 must pay a fee to store their bags with the concierge.",
                "correct_answer": "FALSE",
                "explanation": "Text A states guests arriving earlier can leave luggage with the concierge free of charge."
            },
            {
                "id": "Q2",
                "type": "True/False/Not Given",
                "question_text": "On Sunday mornings, breakfast is served until 10:30 in the Oak Room.",
                "correct_answer": "TRUE",
                "explanation": "Text A states breakfast is served from 07:30 to 10:30 on Saturdays, Sundays, and bank holidays."
            },
            {
                "id": "Q3",
                "type": "True/False/Not Given",
                "question_text": "Afternoon cream tea can be ordered without prior booking upon showing room keys.",
                "correct_answer": "FALSE",
                "explanation": "Text A states: 'Reservations must be booked at least two hours in advance.'"
            },
            {
                "id": "Q4",
                "type": "True/False/Not Given",
                "question_text": "Children under sixteen are permitted in the sauna unaccompanied if they can swim.",
                "correct_answer": "FALSE",
                "explanation": "Text A states children under sixteen must be accompanied by a supervising adult at all times."
            },
            {
                "id": "Q5",
                "type": "True/False/Not Given",
                "question_text": "Grade 3 mountain scrambles are suitable for individuals who experience mild dizziness at heights.",
                "correct_answer": "FALSE",
                "explanation": "Text B states Grade 3 is 'Not suitable for anyone suffering from vertigo'."
            },
            {
                "id": "Q6",
                "type": "True/False/Not Given",
                "question_text": "Participants who arrive wearing trail running sneakers will be refused entry to mountain walks.",
                "correct_answer": "TRUE",
                "explanation": "Text B states running sneakers will result in immediate disqualification without refund."
            },
            {
                "id": "Q7",
                "type": "True/False/Not Given",
                "question_text": "Trekkers who are disqualified during the morning gear check receive an 80% ticket refund.",
                "correct_answer": "FALSE",
                "explanation": "Text B clearly states: 'immediate disqualification without refund.'"
            },
            {
                "id": "Q8",
                "type": "Sentence Completion",
                "question_text": "A late hotel check-out up to 13:30 incurs a supplemental payment of \u00a3____________.",
                "correct_answer": "25.00",
                "explanation": "Text A: 'incurring a supplemental fee of \u00a325.00.'"
            },
            {
                "id": "Q9",
                "type": "Sentence Completion",
                "question_text": "Guests dining at the Glenview Bistro must dress in ____________ attire.",
                "correct_answer": "smart casual",
                "explanation": "Text A: 'Smart casual attire is requested'."
            },
            {
                "id": "Q10",
                "type": "Sentence Completion",
                "question_text": "Hotel residents must obtain pool towels directly from the ____________ reception.",
                "correct_answer": "spa",
                "explanation": "Text A: 'Pool towels are provided at the spa reception'."
            },
            {
                "id": "Q11",
                "type": "Sentence Completion",
                "question_text": "Grade 2 trekking participants should be prepared for up to ____________ hours of continuous hiking.",
                "correct_answer": "5-6",
                "explanation": "Text B: 'Participants must be accustomed to 5-6 hours of continuous walking.'"
            },
            {
                "id": "Q12",
                "type": "Sentence Completion",
                "question_text": "Mandatory gear inspections take place ____________ minutes prior to excursion departures.",
                "correct_answer": "thirty",
                "explanation": "Text B: 'thirty minutes prior to departure at the club base.'"
            },
            {
                "id": "Q13",
                "type": "Sentence Completion",
                "question_text": "Trekkers must carry at least ____________ litres of potable drinking water.",
                "correct_answer": "two",
                "explanation": "Text B: 'Minimum two litres of drinking water'."
            },
            {
                "id": "Q14",
                "type": "Sentence Completion",
                "question_text": "Morning cancellation text notifications are broadcast by ____________ on expedition days.",
                "correct_answer": "06:00",
                "explanation": "Text B: 'Notice of cancellations will be issued via SMS text alert by 06:00'."
            }
        ],
        "s2_title": "Section 2: Workplace Context \u2013 Business Travel & Warehouse Safety (Texts C & D)",
        "s2_text": "Text C: Vantage Logistics \u2013 Corporate Travel and Expense Reimbursement Policy\nVantage Logistics reimburses personnel for legitimate, necessary, and documented business expenses incurred while conducting company business away from their primary office base.\n\nAir Travel and Rail Bookings:\nAll business travel must be reserved through the corporate travel booking portal (TravelPort). For flights under six hours in duration, employees must book standard economy class. Premium economy or business class bookings are authorized only for transcontinental journeys exceeding six continuous flying hours, subject to prior written approval from an Executive Vice President. Rail travel must be booked in standard class; first-class train tickets are non-reimbursable under all circumstances.\n\nHotel Lodging and Per Diem Meal Allowances:\nCorporate lodging is capped at \u00a3140.00 per night for regional cities and \u00a3195.00 per night for central London and international capitals.\n- Breakfast: Reimbursable up to \u00a315.00 when not included in hotel room rates.\n- Lunch: Reimbursable up to \u00a320.00 during business journeys exceeding six hours away from base.\n- Dinner: Reimbursable up to \u00a335.00 for overnight trips.\nAlcoholic beverages of any kind are strictly non-reimbursable.\n\nExpense Submission Deadlines:\nAll expense claims must be submitted electronically via the Concur expense system within twenty-one calendar days of the completion of the business trip. Itemized receipts displaying the merchant's VAT number and detailed purchase breakdown must be scanned and attached. Credit card transaction slips lacking itemization will be rejected.\n\n--------------------------------------------------------------------------------\nText D: Vantage Logistics \u2013 Warehouse Manual Handling and Heavy Lifting Regulations\nWarehouse operations involve repetitive physical handling of parcels, pallets, and shipping containers. To prevent musculoskeletal disorders (MSDs) and spinal injuries, all personnel must adhere to safe lifting guidelines.\n\nWeight Thresholds and Lifting Guidelines:\n- Maximum Solo Lift: The maximum allowable weight for an unassisted, two-handed solo lift under ideal conditions is twenty-five kilograms (25 kg) for male operatives and sixteen kilograms (16 kg) for female operatives.\n- Heavy Cargo (25 kg to 50 kg): Items weighing between 25 kg and 50 kg must be handled either using a synchronized two-person team lift or utilizing manual mechanical aids such as hydraulic hand pallet trucks or sack barrows.\n- Cargo Exceeding 50 kg: Any parcel or freight item exceeding 50 kg must be moved exclusively using powered industrial equipment (such as counterbalance forklifts or electric reach trucks) operated by certified, licensed personnel.\n\nErgonomic Lifting Technique:\n1. Assess the Load: Check package labeling for weight indicators, fragile markings, and center-of-gravity symbols.\n2. Stable Footing: Position feet shoulder-width apart, with one foot slightly forward to maintain balance.\n3. Bend the Knees: Never bend over from the waist. Squat by bending knees and hips while maintaining the natural inward curve of the spine.\n4. Secure Grip: Grasp the load firmly using whole hands, not just fingertips.\n5. Smooth Lift: Lift smoothly using powerful leg muscles; avoid sudden jerking motions or twisting the torso while bearing weight.\n\nIncident Reporting:\nAny twinge, back spasm, or sprain incurred during material handling must be reported to the on-duty Health and Safety Officer before the end of the work shift and entered into the statutory Accident Logbook.",
        "s2_questions": [
            {
                "id": "Q15",
                "type": "Sentence Completion",
                "question_text": "Flights exceeding six hours may qualify for business class with approval from an ____________.",
                "correct_answer": "Executive Vice President",
                "explanation": "Text C: 'subject to prior written approval from an Executive Vice President.'"
            },
            {
                "id": "Q16",
                "type": "Sentence Completion",
                "question_text": "First-class rail travel tickets are strictly ____________ under corporate policy.",
                "correct_answer": "non-reimbursable",
                "explanation": "Text C: 'first-class train tickets are non-reimbursable under all circumstances.'"
            },
            {
                "id": "Q17",
                "type": "Sentence Completion",
                "question_text": "The maximum nightly lodging reimbursement limit in central London is \u00a3____________.",
                "correct_answer": "195.00",
                "explanation": "Text C: 'and \u00a3195.00 per night for central London and international capitals.'"
            },
            {
                "id": "Q18",
                "type": "Sentence Completion",
                "question_text": "Dinner expenses on overnight trips are capped at \u00a3____________.",
                "correct_answer": "35.00",
                "explanation": "Text C: 'Dinner: Reimbursable up to \u00a335.00 for overnight trips.'"
            },
            {
                "id": "Q19",
                "type": "Sentence Completion",
                "question_text": "Travel expense claims must be filed within ____________ calendar days of return.",
                "correct_answer": "twenty-one",
                "explanation": "Text C: 'within twenty-one calendar days of the completion of the business trip.'"
            },
            {
                "id": "Q20",
                "type": "Sentence Completion",
                "question_text": "For male workers, the maximum allowable unassisted solo lift is ____________ kilograms.",
                "correct_answer": "twenty-five",
                "explanation": "Text D: 'twenty-five kilograms (25 kg) for male operatives'."
            },
            {
                "id": "Q21",
                "type": "Sentence Completion",
                "question_text": "Parcels weighing over fifty kilograms must be moved exclusively using ____________ equipment.",
                "correct_answer": "powered industrial",
                "explanation": "Text D: 'moved exclusively using powered industrial equipment'."
            },
            {
                "id": "Q22",
                "type": "True/False/Not Given",
                "question_text": "Employees can claim the cost of a glass of wine consumed with dinner while travelling.",
                "correct_answer": "FALSE",
                "explanation": "Text C states: 'Alcoholic beverages of any kind are strictly non-reimbursable.'"
            },
            {
                "id": "Q23",
                "type": "True/False/Not Given",
                "question_text": "Credit card slips without itemized line items are accepted for meal claims under ten pounds.",
                "correct_answer": "FALSE",
                "explanation": "Text C: 'Credit card transaction slips lacking itemization will be rejected.'"
            },
            {
                "id": "Q24",
                "type": "True/False/Not Given",
                "question_text": "A two-person team lift may be utilized for freight weighing forty kilograms.",
                "correct_answer": "TRUE",
                "explanation": "Text D specifies items between 25 kg and 50 kg must be handled using a two-person team lift or mechanical aids."
            },
            {
                "id": "Q25",
                "type": "True/False/Not Given",
                "question_text": "Operatives are instructed to bend at the waist when picking up boxes from floor level.",
                "correct_answer": "FALSE",
                "explanation": "Text D states: 'Never bend over from the waist. Squat by bending knees and hips'."
            },
            {
                "id": "Q26",
                "type": "True/False/Not Given",
                "question_text": "Operatives who operate forklifts must hold a recognized industrial equipment license.",
                "correct_answer": "TRUE",
                "explanation": "Text D states forklifts must be operated by 'certified, licensed personnel.'"
            },
            {
                "id": "Q27",
                "type": "True/False/Not Given",
                "question_text": "Workplace back sprains can be logged on the day after the injury occurred.",
                "correct_answer": "FALSE",
                "explanation": "Text D specifies: 'must be reported... before the end of the work shift'."
            }
        ],
        "s3_title": "Section 3: The Evolutionary Origins and Social Dynamics of Human Laughter",
        "s3_text": "Paragraph A\nLaughter is one of the most ubiquitous yet enigmatic human vocalizations. From birth, infants exhibit social smiles at six weeks and spontaneous laughter around four months\u2014long before they acquire verbal speech or grammatical competence. Blind and deaf children laugh normally without ever having seen a smile or heard a chuckle, indicating that the neurological apparatus for laughter is hardwired into human biology. Despite its superficial association with comedy, humor, and witty anecdotes, behavioral researchers have discovered that laughter fundamentally functions not as an intellectual appreciation of jokes, but as a primal vocal signaling system forged by natural selection to orchestrate social relationships.\n\nParagraph B\nPioneering research conducted by neurobiologist and psychologist Robert Provine involved analyzing over 1,200 instances of spontaneous laughter in everyday public settings, such as university campuses, shopping malls, and restaurants. Provine uncovered an astonishing fact: less than twenty percent of natural human laughter occurs in response to overt jokes or deliberate humor. Instead, the overwhelming majority of laughter follows mundane conversational statements such as 'Are you sure?', 'It was nice meeting you', or 'I have to go now'. In real-world interactions, laughter serves as an emotional punctuation mark, smoothing conversational transitions, defusing social tensions, and signaling mutual agreement, friendliness, and group solidarity.\n\nParagraph C\nEvolutionary biologists trace the phylogenetic lineage of human laughter back millions of years to our ancestral anthropoid primates. When chimpanzees, gorillas, and orangutans engage in rough-and-tumble play or tickling, they emit a rhythmic, panting vocalization characterized by rapid inhalations and exhalations. This pant-laugh serves as a crucial social play marker, communicating benign intentions to playmates: 'I am wrestling with you, but this is mock aggression, not a genuine physical attack.' Over evolutionary time, as ancestral hominins developed bipedalism and enhanced thoracic breathing control, this primitive breathy pant transformed into the distinct, resonant voiced syllables\u2014the characteristic 'ha-ha-ha'\u2014of modern human laughter.\n\nParagraph D\nFrom a physiological perspective, the act of laughing triggers profound biochemical and neurochemical shifts within the human body. Vigorous laughter stimulates the autonomic nervous system, initially elevating heart rate, blood pressure, and oxygen consumption. This transient arousal is followed by a prolonged refractory period of systemic parasympathetic relaxation, wherein arterial walls dilate and skeletal muscle tone softens. More importantly, laughter triggers the hypothalamus and pituitary gland to release endogenous opioid peptides, known as beta-endorphins, into the bloodstream and cerebrospinal fluid. These natural biochemical painkillers bind to mu-opioid receptors in the brain, inducing a sense of psychological euphoria and significantly raising individual pain tolerance thresholds.\n\nParagraph E\nBritish evolutionary anthropologist Robin Dunbar posits that the endorphin-releasing mechanism of shared laughter was pivotal to early human survival. In non-human primates, social cohesion and alliance formation depend on physical one-on-one grooming. However, grooming is an inherently time-consuming, dyadic activity that limits primate social group sizes to approximately fifty individuals. As early human bands expanded into tribal communities numbering 150 individuals, one-on-one grooming became mathematically untenable. Dunbar argues that chorused, synchronized laughter evolved as a form of 'grooming at a distance', enabling multiple group members to trigger mutual neurochemical bonding simultaneously around communal campfires.\n\nParagraph F\nThe human auditory and neural systems have evolved exquisite sensitivity to distinguish between authentic and simulated laughter. Neuroimaging experiments conducted using functional Magnetic Resonance Imaging (fMRI) reveal that authentic, spontaneous laughter\u2014originating from ancient subcortical brain structures like the amygdala and basal ganglia\u2014activates the anterior cingulate cortex and auditory processing centers. Conversely, polite, volitional, or 'fake' laughter\u2014controlled by the higher-order prefrontal motor cortex\u2014prompts listeners to activate brain areas associated with mentalizing and theory of mind, as they automatically decipher the underlying social motives or hidden intentions of the speaker.\n\nParagraph G\nIn contemporary society, the therapeutic and social utility of laughter is increasingly recognized within medical and corporate contexts. Clinical trials have demonstrated that mirthful laughter reduces circulating levels of cortisol and epinephrine, bolstering immune function by increasing natural killer cell activity and immunoglobulin A levels. In workplace environments, team-wide laughter fosters psychological safety, diminishes hierarchical barriers between leadership and staff, and sparks creative problem-solving. Far from being a frivolous biological quirk, laughter remains humanity's oldest and most powerful acoustic bridge between individual minds.",
        "s3_questions": [
            {
                "id": "Q28",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph A?",
                "options": [
                    "i. Innate biology versus the intellectual joke theory",
                    "ii. The mundane reality of conversational laughter",
                    "iii. Primate origins: From play pants to voiced laughs",
                    "iv. Physiological and neurochemical analgesic effects",
                    "v. Social bonding at a distance and tribe expansion",
                    "vi. Neural discernment between spontaneous and fake laughs",
                    "vii. Clinical therapy and modern workplace benefits"
                ],
                "correct_answer": "i. Innate biology versus the intellectual joke theory",
                "explanation": "Paragraph A discusses how laughter is hardwired from infancy and is a biological signaling system."
            },
            {
                "id": "Q29",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph B?",
                "options": [
                    "i. Innate biology versus the intellectual joke theory",
                    "ii. The mundane reality of conversational laughter",
                    "iii. Primate origins: From play pants to voiced laughs",
                    "iv. Physiological and neurochemical analgesic effects",
                    "v. Social bonding at a distance and tribe expansion",
                    "vi. Neural discernment between spontaneous and fake laughs",
                    "vii. Clinical therapy and modern workplace benefits"
                ],
                "correct_answer": "ii. The mundane reality of conversational laughter",
                "explanation": "Paragraph B outlines Provine's research showing <20% of laughter follows actual jokes, following ordinary statements instead."
            },
            {
                "id": "Q30",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph C?",
                "options": [
                    "i. Innate biology versus the intellectual joke theory",
                    "ii. The mundane reality of conversational laughter",
                    "iii. Primate origins: From play pants to voiced laughs",
                    "iv. Physiological and neurochemical analgesic effects",
                    "v. Social bonding at a distance and tribe expansion",
                    "vi. Neural discernment between spontaneous and fake laughs",
                    "vii. Clinical therapy and modern workplace benefits"
                ],
                "correct_answer": "iii. Primate origins: From play pants to voiced laughs",
                "explanation": "Paragraph C traces primate panting play signals to modern resonant syllables."
            },
            {
                "id": "Q31",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph D?",
                "options": [
                    "i. Innate biology versus the intellectual joke theory",
                    "ii. The mundane reality of conversational laughter",
                    "iii. Primate origins: From play pants to voiced laughs",
                    "iv. Physiological and neurochemical analgesic effects",
                    "v. Social bonding at a distance and tribe expansion",
                    "vi. Neural discernment between spontaneous and fake laughs",
                    "vii. Clinical therapy and modern workplace benefits"
                ],
                "correct_answer": "iv. Physiological and neurochemical analgesic effects",
                "explanation": "Paragraph D discusses beta-endorphins, pain tolerance, and cardiovascular responses."
            },
            {
                "id": "Q32",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph E?",
                "options": [
                    "i. Innate biology versus the intellectual joke theory",
                    "ii. The mundane reality of conversational laughter",
                    "iii. Primate origins: From play pants to voiced laughs",
                    "iv. Physiological and neurochemical analgesic effects",
                    "v. Social bonding at a distance and tribe expansion",
                    "vi. Neural discernment between spontaneous and fake laughs",
                    "vii. Clinical therapy and modern workplace benefits"
                ],
                "correct_answer": "v. Social bonding at a distance and tribe expansion",
                "explanation": "Paragraph E focuses on Robin Dunbar's theory of laughter replacing 1-on-1 grooming for larger tribes."
            },
            {
                "id": "Q33",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph F?",
                "options": [
                    "i. Innate biology versus the intellectual joke theory",
                    "ii. The mundane reality of conversational laughter",
                    "iii. Primate origins: From play pants to voiced laughs",
                    "iv. Physiological and neurochemical analgesic effects",
                    "v. Social bonding at a distance and tribe expansion",
                    "vi. Neural discernment between spontaneous and fake laughs",
                    "vii. Clinical therapy and modern workplace benefits"
                ],
                "correct_answer": "vi. Neural discernment between spontaneous and fake laughs",
                "explanation": "Paragraph F explores brain scans differentiating genuine versus polite, volitional laughter."
            },
            {
                "id": "Q34",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph G?",
                "options": [
                    "i. Innate biology versus the intellectual joke theory",
                    "ii. The mundane reality of conversational laughter",
                    "iii. Primate origins: From play pants to voiced laughs",
                    "iv. Physiological and neurochemical analgesic effects",
                    "v. Social bonding at a distance and tribe expansion",
                    "vi. Neural discernment between spontaneous and fake laughs",
                    "vii. Clinical therapy and modern workplace benefits"
                ],
                "correct_answer": "vii. Clinical therapy and modern workplace benefits",
                "explanation": "Paragraph G covers clinical immune benefits and corporate team-building dynamics."
            },
            {
                "id": "Q35",
                "type": "Multiple Choice",
                "question_text": "Robert Provine's observational studies revealed that:",
                "options": [
                    "A. Laughter is predominantly caused by rehearsed comedic storytelling.",
                    "B. Over 80% of laughter follows ordinary, non-humorous conversational phrases.",
                    "C. Men laugh significantly more frequently than women in social settings.",
                    "D. Laughter inhibits verbal language acquisition in young children."
                ],
                "correct_answer": "B. Over 80% of laughter follows ordinary, non-humorous conversational phrases.",
                "explanation": "Paragraph B states less than 20% occurs from jokes, so over 80% follows mundane phrases."
            },
            {
                "id": "Q36",
                "type": "Multiple Choice",
                "question_text": "How did pant-laughter benefit ancestral non-human primates during play?",
                "options": [
                    "A. It frightened away nearby territorial predators.",
                    "B. It warned juveniles that play had become too dangerous.",
                    "C. It signaled that mock aggressive fighting was safe and non-threatening.",
                    "D. It established strict dominant hierarchies without bloodshed."
                ],
                "correct_answer": "C. It signaled that mock aggressive fighting was safe and non-threatening.",
                "explanation": "Paragraph C explains it communicated benign intentions: mock aggression rather than a real attack."
            },
            {
                "id": "Q37",
                "type": "Multiple Choice",
                "question_text": "According to Robin Dunbar, laughter replaced physical grooming because:",
                "options": [
                    "A. Physical touch transmitted contagious viral pathogens among early humans.",
                    "B. Grooming multiple individuals simultaneously allowed larger groups to bond.",
                    "C. Human skin lost protective fur, rendering manual grooming obsolete.",
                    "D. Early tribes lacked the physical dexterity required for fine grooming."
                ],
                "correct_answer": "B. Grooming multiple individuals simultaneously allowed larger groups to bond.",
                "explanation": "Paragraph E states laughter functioned as grooming at a distance, allowing simultaneous bonding in larger groups."
            },
            {
                "id": "Q38",
                "type": "True/False/Not Given",
                "question_text": "Children who are born blind and deaf do not develop the capability to laugh.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph A states blind and deaf children laugh normally without ever seeing a smile or hearing a chuckle."
            },
            {
                "id": "Q39",
                "type": "True/False/Not Given",
                "question_text": "Beta-endorphins released during laughter bind to mu-opioid receptors and elevate pain tolerance.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph D confirms beta-endorphins bind to mu-opioid receptors and raise pain tolerance thresholds."
            },
            {
                "id": "Q40",
                "type": "True/False/Not Given",
                "question_text": "Listeners process volitional, fake laughter using the exact same subcortical brain pathways as real laughter.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph F explains fake laughter engages prefrontal motor regions and theory-of-mind networks instead."
            }
        ]
    },
    {
        "suite_id": 5,
        "domain": "Community Gardening, Micro-Mobility, Occupational Health & Railway Engineering",
        "cambridge_ref": "Cambridge General Training Reading Benchmark (Vol 18 / 19)",
        "s1_title": "Section 1: Everyday Community Information (Texts A & B)",
        "s1_text": "Text A: Green Meadows Community Allotments \u2013 Rules and Tenancy Guidelines\nGreen Meadows Allotment Association manages ninety-five organic cultivation plots leased annually to local residents for fruit, vegetable, and floral gardening.\n\nTenancy Terms and Plot Maintenance:\n- Annual Tenancy: The allotment season runs from 1st April to 31st March. Plot fees are \u00a370.00 annually for a standard full plot (250 sq metres) and \u00a340.00 for a half plot.\n- Cultivation Quota: Tenants must actively cultivate at least 75% of their plot area. Plots left fallow, unweeded, or covered in noxious weeds for more than sixty consecutive days will be subject to a Tenancy Termination Notice.\n- Chemical Restrictions: In accordance with our certified organic covenant, chemical pesticides, synthetic herbicides, and artificial inorganic fertilizers are strictly prohibited. Gardeners may utilize approved natural remedies (such as neem oil, companion planting, and biological nematode controls).\n\nWater Usage and Infrastructure:\nMains water troughs are operational from 15th April to 31st October. Hosepipes, sprinklers, and automated irrigation drips connected directly to mains supply taps are banned; water must be collected using hand-held watering cans. All sheds erected on plots must not exceed 2.0m x 1.8m in footprint and must be painted in natural dark green wood preservative.\n\n--------------------------------------------------------------------------------\nText B: CityCycle Public Bicycle Sharing Scheme \u2013 User Guidelines\nCityCycle offers a convenient, sustainable micro-mobility bike-share scheme operating across forty automated docking stations in the central business district.\n\nUnlocking Bikes and Operational Rules:\n- Smartphone App or Keycard: Users unlock bicycles by scanning the QR code on the rear mudguard via the CityCycle app or tapping a registered RFID smart card on the docking pillar.\n- Helmet Law and Safety: Riders must wear an approved, fastened cycle helmet at all times when riding on public highways. Headlights and rear LED lights activate automatically upon motion. Riding on pedestrian sidewalks is illegal and subject to municipal police fines.\n\nFare Tariffs and Journey Windows:\n- Unlock Fee: \u00a31.00 per ride.\n- Commuter Tier: The first thirty minutes of any trip are included free of charge under standard monthly subscriptions (\u00a312.00/month).\n- Pay-as-You-Go: For non-subscribers, trips are billed at \u00a30.10 per minute after the initial unlocking.\n- Maximum Usage Cap: To keep bicycles circulating among the public, single rentals may not exceed six continuous hours. Bicycles not returned to a recognized docking station within twenty-four hours will be treated as stolen, and the user's registered bank card will be debited a \u00a3350.00 replacement charge.\n\nDocking and Out-of-Zone Penalties:\nWhen returning a bicycle, push the front wheel firmly into an empty dock terminal until a green LED illuminates and a confirmation chime sounds. If all docks at your destination station are full, users can tap 'Full Station' on the terminal touchscreen to receive fifteen minutes of free overtime to reach the nearest available docking station. Abandoning a bicycle outside an authorized geofenced dock incurs an instant \u00a325.00 recovery surcharge.",
        "s1_questions": [
            {
                "id": "Q1",
                "type": "True/False/Not Given",
                "question_text": "An allotment tenant can use chemical weed killers if weeds threaten their vegetables.",
                "correct_answer": "FALSE",
                "explanation": "Text A states synthetic herbicides and chemical pesticides are strictly prohibited."
            },
            {
                "id": "Q2",
                "type": "True/False/Not Given",
                "question_text": "Tenants must cultivate at least 75 percent of their allotted land area.",
                "correct_answer": "TRUE",
                "explanation": "Text A states: 'Tenants must actively cultivate at least 75% of their plot area.'"
            },
            {
                "id": "Q3",
                "type": "True/False/Not Given",
                "question_text": "Gardeners are permitted to connect hosepipes directly to the mains water troughs.",
                "correct_answer": "FALSE",
                "explanation": "Text A states hosepipes and sprinklers are banned; water must be collected using watering cans."
            },
            {
                "id": "Q4",
                "type": "True/False/Not Given",
                "question_text": "CityCycle riders can ride on pedestrian sidewalks if they travel under 10 km/h.",
                "correct_answer": "FALSE",
                "explanation": "Text B states: 'Riding on pedestrian sidewalks is illegal and subject to municipal police fines.'"
            },
            {
                "id": "Q5",
                "type": "True/False/Not Given",
                "question_text": "CityCycle bicycle lights turn on automatically as soon as the bicycle starts moving.",
                "correct_answer": "TRUE",
                "explanation": "Text B confirms: 'Headlights and rear LED lights activate automatically upon motion.'"
            },
            {
                "id": "Q6",
                "type": "True/False/Not Given",
                "question_text": "Monthly subscribers must pay a per-minute fee for the first thirty minutes of every ride.",
                "correct_answer": "FALSE",
                "explanation": "Text B states the first thirty minutes are included free of charge under monthly subscriptions."
            },
            {
                "id": "Q7",
                "type": "True/False/Not Given",
                "question_text": "Users can receive additional free time if all docks at their target station are occupied.",
                "correct_answer": "TRUE",
                "explanation": "Text B confirms tapping 'Full Station' grants fifteen minutes of free overtime."
            },
            {
                "id": "Q8",
                "type": "Sentence Completion",
                "question_text": "The annual fee for leasing a half-sized allotment plot is \u00a3____________.",
                "correct_answer": "40.00",
                "explanation": "Text A: 'and \u00a340.00 for a half plot.'"
            },
            {
                "id": "Q9",
                "type": "Sentence Completion",
                "question_text": "Mains water troughs are decommissioned for the winter on ____________.",
                "correct_answer": "31st October",
                "explanation": "Text A: 'operational from 15th April to 31st October.'"
            },
            {
                "id": "Q10",
                "type": "Sentence Completion",
                "question_text": "Garden sheds on allotment plots must be coated with ____________ wood preservative.",
                "correct_answer": "natural dark green",
                "explanation": "Text A: 'painted in natural dark green wood preservative.'"
            },
            {
                "id": "Q11",
                "type": "Sentence Completion",
                "question_text": "CityCycle bicycles feature a scanable QR code located on the ____________.",
                "correct_answer": "rear mudguard",
                "explanation": "Text B: 'scanning the QR code on the rear mudguard via the CityCycle app'."
            },
            {
                "id": "Q12",
                "type": "Sentence Completion",
                "question_text": "The unlock fee charged for initiating a single bicycle trip is \u00a3____________.",
                "correct_answer": "1.00",
                "explanation": "Text B: 'Unlock Fee: \u00a31.00 per ride.'"
            },
            {
                "id": "Q13",
                "type": "Sentence Completion",
                "question_text": "Failing to return a bicycle within twenty-four hours incurs a replacement fee of \u00a3____________.",
                "correct_answer": "350.00",
                "explanation": "Text B: 'debited a \u00a3350.00 replacement charge.'"
            },
            {
                "id": "Q14",
                "type": "Sentence Completion",
                "question_text": "Leaving a rental bicycle outside a recognized dock results in a \u00a3____________ surcharge.",
                "correct_answer": "25.00",
                "explanation": "Text B: 'incurs an instant \u00a325.00 recovery surcharge.'"
            }
        ],
        "s2_title": "Section 2: Workplace Context \u2013 Noise Standards & Fire Safety (Texts C & D)",
        "s2_text": "Text C: Apex Manufacturing \u2013 Occupational Noise Exposure and Audiometric Surveillance\nIn industrial manufacturing and stamping environments, excessive acoustic noise represents a major cause of irreversible sensorineural hearing loss. Apex Manufacturing enforces stringent hearing conservation protocols across all production facilities.\n\nNoise Exposure Action Values:\n- Lower Exposure Action Value (80 dBA): Where average daily noise exposure reaches 80 dBA, the company must provide certified hearing protection (earmuffs or foam earplugs) and make audiometric testing available upon employee request.\n- Upper Exposure Action Value (85 dBA): In designated hearing protection zones where noise reaches or exceeds 85 dBA, wearing hearing protection is legally mandatory for all staff, contractors, and visitors. Blue 'Ear Protection Required' warning signs mark all perimeter access doors.\n- Exposure Limit Value (87 dBA): Under no circumstances may an employee's actual sound exposure (taking into account the attenuation provided by protective ear defenders) exceed 87 dBA.\n\nHealth Surveillance Program:\nAll workers operating in mandatory hearing protection zones must participate in annual audiometric screening conducted by the Occupational Health Department. Pure-tone audiograms are performed at baseline (pre-employment), followed by testing at twelve-month intervals. If an audiogram detects a confirmed hearing threshold shift exceeding 15 dB at test frequencies, the employee will be referred to an ENT specialist, and workplace engineering noise controls will be audited.\n\n--------------------------------------------------------------------------------\nText D: Apex Manufacturing \u2013 Emergency Evacuation Protocols and Nominated Fire Wardens\nThis protocol details the emergency procedures to be executed in the event of fire, structural hazard, or hazardous chemical vapor release.\n\nAlarm Activation and Evacuation Orders:\nUpon discovering an active fire or hazardous leak, personnel must instantly operate the nearest manual red call point and shout 'Fire!'. Do not attempt to extinguish a fire that is larger than a standard wastepaper bin or that blocks your evacuation route. Upon hearing the continuous electronic siren, all staff must immediately evacuate via the nearest green emergency exit fire door. Lifts must never be used.\n\nAssembly Areas and Roll Call:\nStaff must proceed calmly to their designated Fire Assembly Point:\n- Assembly Point A (North Visitor Car Park): Administrative, Engineering, and Procurement personnel.\n- Assembly Point B (South Haulage Yard): Production Floor, Maintenance, and Warehouse operatives.\nPersonnel must remain assembled by department until their nominated Fire Warden confirms a 100% headcount.\n\nFire Warden Duties:\nDesignated Fire Wardens wear high-visibility orange reflective vests. During an alarm activation, Fire Wardens must conduct a rapid sweep of their assigned building sector, checking washrooms, breakrooms, and solitary storage areas to ensure complete evacuation. Wardens report floor clearance directly to the Chief Incident Commander at the central security gatehouse. No employee may re-enter any company building until the Incident Commander gives the formal 'All Clear' announcement.",
        "s2_questions": [
            {
                "id": "Q15",
                "type": "Sentence Completion",
                "question_text": "Wearing hearing protection becomes legally mandatory at the upper action value of ____________ dBA.",
                "correct_answer": "85",
                "explanation": "Text C: 'where noise reaches or exceeds 85 dBA, wearing hearing protection is legally mandatory'."
            },
            {
                "id": "Q16",
                "type": "Sentence Completion",
                "question_text": "Blue warning signs on perimeter doors indicate that ____________ is required inside.",
                "correct_answer": "ear protection",
                "explanation": "Text C: 'Blue Ear Protection Required warning signs mark all perimeter access doors.'"
            },
            {
                "id": "Q17",
                "type": "Sentence Completion",
                "question_text": "Hearing tests are conducted annually by the ____________ Department.",
                "correct_answer": "Occupational Health",
                "explanation": "Text C: 'audiometric screening conducted by the Occupational Health Department.'"
            },
            {
                "id": "Q18",
                "type": "Sentence Completion",
                "question_text": "A confirmed hearing threshold shift exceeding ____________ dB triggers specialist medical referral.",
                "correct_answer": "15",
                "explanation": "Text C: 'detects a confirmed hearing threshold shift exceeding 15 dB'."
            },
            {
                "id": "Q19",
                "type": "Sentence Completion",
                "question_text": "Upon discovering a fire, employees must activate the nearest manual ____________.",
                "correct_answer": "red call point",
                "explanation": "Text D: 'operate the nearest manual red call point'."
            },
            {
                "id": "Q20",
                "type": "Sentence Completion",
                "question_text": "Warehouse and production floor employees must gather at Assembly Point ____________.",
                "correct_answer": "B",
                "explanation": "Text D: 'Assembly Point B (South Haulage Yard): Production Floor, Maintenance, and Warehouse operatives.'"
            },
            {
                "id": "Q21",
                "type": "Sentence Completion",
                "question_text": "Nominated Fire Wardens wear high-visibility ____________ reflective vests during evacuations.",
                "correct_answer": "orange",
                "explanation": "Text D: 'Designated Fire Wardens wear high-visibility orange reflective vests.'"
            },
            {
                "id": "Q22",
                "type": "True/False/Not Given",
                "question_text": "The company is legally required to offer audiometric testing when noise averages 80 dBA.",
                "correct_answer": "TRUE",
                "explanation": "Text C states at 80 dBA the company must make audiometric testing available upon request."
            },
            {
                "id": "Q23",
                "type": "True/False/Not Given",
                "question_text": "Employees are permitted to use passenger elevators during emergency fire evacuations.",
                "correct_answer": "FALSE",
                "explanation": "Text D explicitly commands: 'Lifts must never be used.'"
            },
            {
                "id": "Q24",
                "type": "True/False/Not Given",
                "question_text": "Workers should attempt to fight a fire even if it is spreading toward their exit route.",
                "correct_answer": "FALSE",
                "explanation": "Text D states: 'Do not attempt to extinguish a fire that is larger than a standard wastepaper bin or that blocks your evacuation route.'"
            },
            {
                "id": "Q25",
                "type": "True/False/Not Given",
                "question_text": "Fire Wardens are responsible for checking staff washrooms during building sweeps.",
                "correct_answer": "TRUE",
                "explanation": "Text D confirms wardens conduct a rapid sweep 'checking washrooms, breakrooms, and solitary storage areas'."
            },
            {
                "id": "Q26",
                "type": "True/False/Not Given",
                "question_text": "Employees can return to the factory once their line manager confirms the roll call.",
                "correct_answer": "FALSE",
                "explanation": "Text D specifies only the Chief Incident Commander gives the formal 'All Clear' announcement."
            },
            {
                "id": "Q27",
                "type": "True/False/Not Given",
                "question_text": "All Fire Wardens receive certified first-aid training including defibrillator operation.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text D details fire sweep duties and orange vests, but does not mention defibrillator training."
            }
        ],
        "s3_title": "Section 3: Engineering the Impossible: The Construction of the Trans-Siberian Railway",
        "s3_text": "Paragraph A\nSpanning eight time zones, traversing two continents, and stretching over 9,289 kilometres (5,772 miles) from Moscow to the Pacific port of Vladivostok, the Trans-Siberian Railway represents the longest continuous railway line ever constructed. When Tsar Alexander III issued the imperial rescript authorizing construction in March 1891, contemporary European engineers considered the project an impossible fantasy. The proposed route traversed thousands of kilometres of impenetrable virgin taiga forest, treacherous peat bogs, mountain ranges of solid granite, and vast expanses of continuous permafrost\u2014subterranean soil perpetually frozen since the Pleistocene epoch.\n\nParagraph B\nConstruction commenced simultaneously from both the western terminal in Chelyabinsk and the eastern terminal in Vladivostok, with work progressing inward toward the remote interior of central Siberia. The colossal endeavor was overseen by Sergei Witte, the visionary Russian Minister of Finance, who recognized that an iron artery was vital to unite the fragmented empire, defend its eastern borders against expansionist imperial powers, and exploit the untapped mineral, timber, and agricultural wealth of Siberia. To fund the gargantuan capital expenditure, Witte secured massive sovereign loans from French financial markets and prioritized speed and economy over structural durability during the initial laying of track.\n\nParagraph C\nThe human labor force mobilized for the railway was immense and diverse. Over 90,000 workers were engaged during peak construction periods, consisting of Russian railway engineers, peasant agrarian laborers, soldiers from the Imperial Russian Army, foreign contract workers, and tens of thousands of penal convict laborers. Working conditions were brutal in the extreme. In summer, laborers contended with sweltering humidity and tormenting swarms of mosquitoes and biting flies emerging from the Siberian marshes. In winter, temperatures routinely plummeted to minus forty-five degrees Celsius, causing iron tools to turn brittle and shatter upon impact with frozen bedrock. Dynamiting frozen ground required lighting wood fires along the track bed for hours to thaw the surface soil before drill bits could penetrate.\n\nParagraph D\nThe most formidable geographical impediment along the entire route was Lake Baikal\u2014the deepest, oldest, and most voluminous freshwater lake on Earth. Surrounded by precipitous jagged mountain cliffs that plummeted directly into the water, Baikal formed a colossal physical barrier 636 kilometres in length. During the early operational years, the railway line terminated at both shores. Passengers and freight cars were ferried across the lake's open waters on two massive British-built icebreaking steamships: the SS Baikal and the SS Angara. During the dead of winter, when lake ice froze to a thickness of two metres, engineers laid temporary railway tracks directly across the frozen surface of the lake, hauling individual carriages across forty kilometres of ice using horses and lightweight steam locomotives.\n\nParagraph E\nTo eliminate the hazardous, weather-dependent lake crossing, the Imperial government embarked on the construction of the Circum-Baikal Railway between 1901 and 1904. Carved into the sheer cliffs skirting the southern shore of the lake, this 260-kilometre section was the most complex and expensive civil engineering undertaking in railway history. Dubbed the 'Golden Buckle of the Trans-Siberian Belt', the line required the excavation of thirty-eight tunnels blasted through solid granite, hundreds of stone retaining walls, and dozens of bridges spanning mountain gorges. Laborers worked clinging to sheer rock faces suspended on ropes, blasting cliffs that sheared off and plunged directly into the icy waters below.\n\nParagraph F\nThe completion of the Trans-Siberian Railway fundamentally transformed Russian society and global geopolitical dynamics. Travel time between Moscow and the Pacific, which previously required months of agonizing travel by horse-drawn carriage and river barge, was compressed to just sixteen days. Millions of peasant settlers from European Russia migrated eastward, establishing flourishing agrarian farming communities and booming commercial trading cities across Siberia, including Novosibirsk, Irkutsk, and Omsk. Economically, the railway opened Siberian timber reserves, gold deposits, and agricultural wheat to global markets, creating an enduring continental trade corridor bridging Europe and East Asia.\n\nParagraph G\nOver a century after its completion, the Trans-Siberian Railway remains one of the world's primary transport lifelines. Electrified entirely in 2002, the modern double-track railway transports millions of passengers each year alongside massive container freight trains carrying industrial manufactured goods from China and East Asia to European markets. The line stands as a permanent testament to human resilience and engineering audacity, having conquered the world's most inhospitable wilderness to connect two oceans across the vast Russian continent.",
        "s3_questions": [
            {
                "id": "Q28",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph A?",
                "options": [
                    "i. A monumental vision through hostile terrain",
                    "ii. Geopolitical motivations and French financing",
                    "iii. Severe climate hardships and diverse workforce",
                    "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                    "v. The Golden Buckle: Tunnels through granite cliffs",
                    "vi. Economic migration and societal transformation",
                    "vii. A modern electrified continental trade artery"
                ],
                "correct_answer": "i. A monumental vision through hostile terrain",
                "explanation": "Paragraph A introduces the 9,289 km line and the extreme challenges of taiga, bogs, and permafrost."
            },
            {
                "id": "Q29",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph B?",
                "options": [
                    "i. A monumental vision through hostile terrain",
                    "ii. Geopolitical motivations and French financing",
                    "iii. Severe climate hardships and diverse workforce",
                    "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                    "v. The Golden Buckle: Tunnels through granite cliffs",
                    "vi. Economic migration and societal transformation",
                    "vii. A modern electrified continental trade artery"
                ],
                "correct_answer": "ii. Geopolitical motivations and French financing",
                "explanation": "Paragraph B explains Sergei Witte's leadership, geopolitical motives, and French financing."
            },
            {
                "id": "Q30",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph C?",
                "options": [
                    "i. A monumental vision through hostile terrain",
                    "ii. Geopolitical motivations and French financing",
                    "iii. Severe climate hardships and diverse workforce",
                    "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                    "v. The Golden Buckle: Tunnels through granite cliffs",
                    "vi. Economic migration and societal transformation",
                    "vii. A modern electrified continental trade artery"
                ],
                "correct_answer": "iii. Severe climate hardships and diverse workforce",
                "explanation": "Paragraph C details the 90,000 workers, sub-zero winter temperatures, and thawing frozen ground."
            },
            {
                "id": "Q31",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph D?",
                "options": [
                    "i. A monumental vision through hostile terrain",
                    "ii. Geopolitical motivations and French financing",
                    "iii. Severe climate hardships and diverse workforce",
                    "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                    "v. The Golden Buckle: Tunnels through granite cliffs",
                    "vi. Economic migration and societal transformation",
                    "vii. A modern electrified continental trade artery"
                ],
                "correct_answer": "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                "explanation": "Paragraph D discusses crossing Lake Baikal via icebreakers and tracks laid across frozen winter ice."
            },
            {
                "id": "Q32",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph E?",
                "options": [
                    "i. A monumental vision through hostile terrain",
                    "ii. Geopolitical motivations and French financing",
                    "iii. Severe climate hardships and diverse workforce",
                    "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                    "v. The Golden Buckle: Tunnels through granite cliffs",
                    "vi. Economic migration and societal transformation",
                    "vii. A modern electrified continental trade artery"
                ],
                "correct_answer": "v. The Golden Buckle: Tunnels through granite cliffs",
                "explanation": "Paragraph E covers the Circum-Baikal railway and its 38 tunnels blasted through rock cliffs."
            },
            {
                "id": "Q33",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph F?",
                "options": [
                    "i. A monumental vision through hostile terrain",
                    "ii. Geopolitical motivations and French financing",
                    "iii. Severe climate hardships and diverse workforce",
                    "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                    "v. The Golden Buckle: Tunnels through granite cliffs",
                    "vi. Economic migration and societal transformation",
                    "vii. A modern electrified continental trade artery"
                ],
                "correct_answer": "vi. Economic migration and societal transformation",
                "explanation": "Paragraph F covers the 16-day transit time, peasant migrations, and Siberian economic growth."
            },
            {
                "id": "Q34",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph G?",
                "options": [
                    "i. A monumental vision through hostile terrain",
                    "ii. Geopolitical motivations and French financing",
                    "iii. Severe climate hardships and diverse workforce",
                    "iv. Crossing Lake Baikal: Icebreakers and frozen tracks",
                    "v. The Golden Buckle: Tunnels through granite cliffs",
                    "vi. Economic migration and societal transformation",
                    "vii. A modern electrified continental trade artery"
                ],
                "correct_answer": "vii. A modern electrified continental trade artery",
                "explanation": "Paragraph G describes the modern electrified line as a global freight corridor."
            },
            {
                "id": "Q35",
                "type": "Multiple Choice",
                "question_text": "Sergei Witte prioritized building the Trans-Siberian Railway primarily to:",
                "options": [
                    "A. Allow the Tsar to visit his summer estates in Vladivostok.",
                    "B. Unify the Russian empire and protect its borders against eastern powers.",
                    "C. Prove Russian dominance over British railway technology.",
                    "D. Transport timber exclusively to Scandinavian markets."
                ],
                "correct_answer": "B. Unify the Russian empire and protect its borders against eastern powers.",
                "explanation": "Paragraph B states Witte recognized it was vital to unite the fragmented empire and defend borders."
            },
            {
                "id": "Q36",
                "type": "Multiple Choice",
                "question_text": "Before the Circum-Baikal line was completed, trains crossed Lake Baikal in winter by:",
                "options": [
                    "A. Waiting until spring when the ice melted completely.",
                    "B. Running carriages along temporary tracks laid directly on the surface ice.",
                    "C. Travelling through an underwater submerged floating tube.",
                    "D. Detouring 2,000 kilometres south through Mongolia."
                ],
                "correct_answer": "B. Running carriages along temporary tracks laid directly on the surface ice.",
                "explanation": "Paragraph D states engineers laid temporary tracks directly across the two-metre-thick frozen ice."
            },
            {
                "id": "Q37",
                "type": "Multiple Choice",
                "question_text": "The Circum-Baikal Railway earned the nickname 'Golden Buckle' because:",
                "options": [
                    "A. It was financed with physical gold bars extracted from Siberian mines.",
                    "B. It was the most expensive and intricate link closing the railway belt.",
                    "C. Its tracks were plated in brass to resist corrosion from lake water.",
                    "D. It was constructed exclusively by royal master craftsmen."
                ],
                "correct_answer": "B. It was the most expensive and intricate link closing the railway belt.",
                "explanation": "Paragraph E explains it was the most complex and expensive civil engineering undertaking in railway history, linking the ends."
            },
            {
                "id": "Q38",
                "type": "True/False/Not Given",
                "question_text": "Dynamite drill bits could easily penetrate frozen Siberian permafrost without preheating.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph C states wood fires had to be lit for hours to thaw the surface soil before drill bits could penetrate."
            },
            {
                "id": "Q39",
                "type": "True/False/Not Given",
                "question_text": "The entire Trans-Siberian Railway line was fully electrified by 2002.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph G confirms: 'Electrified entirely in 2002, the modern double-track railway...'"
            },
            {
                "id": "Q40",
                "type": "True/False/Not Given",
                "question_text": "The icebreaker SS Baikal was constructed in a shipyard located in Saint Petersburg.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph D states the steamships were 'British-built icebreaking steamships'."
            }
        ]
    },
    {
        "suite_id": 6,
        "domain": "Aquatic Sports, Creative Arts, Workplace Equality & Deep-Sea Oceanography",
        "cambridge_ref": "Cambridge General Training Reading Benchmark (Vol 18 / 19)",
        "s1_title": "Section 1: Everyday Community Information (Texts A & B)",
        "s1_text": "Text A: Riverside Aquatic Centre \u2013 Public Swimming, Lessons & Pool Etiquette\nRiverside Aquatic Centre features an Olympic-standard 50-metre competition pool, a heated 25-metre training pool, and an interactive shallow splash zone for toddlers.\n\nPublic Lane Swimming and Bookings:\n- Lane Designations: The main pool is configured into dedicated fast, medium, and slow swimming lanes during public sessions. Swimmers must observe the clockwise rotation indicated by direction signs at each lane head.\n- Timed Booking Slots: Public sessions operate in 60-minute increments from 06:00 to 21:00 on weekdays, and 07:30 to 19:30 on weekends. Online reservations open forty-eight hours in advance via the Riverside mobile app. Walk-ins are accommodated only if lane capacity allows.\n- Admission Charges: Adult single swim is \u00a36.50; Junior (ages 4-15) and Senior (65+) swim is \u00a34.00; Children under four swim free.\n\nSupervision and Hygiene Standards:\nChildren under eight years of age must be accompanied in the water by a responsible person aged sixteen or older at a strict ratio of no more than two children per adult. All swimmers must take a cleansing pre-swim shower before entering the pool. Outdoor footwear is forbidden in the poolside zone; blue disposable shoe covers are available at the changing room turnstiles.\n\n--------------------------------------------------------------------------------\nText B: The Artisan Guild \u2013 Weekend Ceramic & Pottery Workshops for Beginners\nThe Artisan Guild hosts introductory pottery and ceramic glazing workshops for hobbyists wishing to learn wheel throwing and hand-building techniques.\n\nWorkshop Schedule and Structure:\nWorkshops run on alternate Saturdays from 09:30 to 16:30, with a one-hour lunch break at 12:30. The six-hour intensive course introduces participants to clay wedging, centring on the motorized wheel, pulling cylinder walls, and basic hand-sculpting methods. The class size is strictly capped at ten participants per session to guarantee personalized guidance from the resident master ceramicist.\n\nMaterials, Tools, and Safety:\n- Included Supplies: Tuition covers twelve kilograms of stoneware clay, tool kits (wire cutters, ribs, and wooden modeling tools), and transparent studio underglazes.\n- Protective Clothing: Clay throwing is inherently messy. Participants must bring an old apron or wear clothes they do not mind staining. Long hair must be tied securely back, and finger jewelry must be removed to avoid snagging on rotating potter's wheels.\n\nFiring, Glazing, and Collection of Finished Pieces:\nCeramic pieces created during the workshop require slow air-drying for two weeks before undergoing their preliminary bisque firing in the studio kiln at 1,000\u00b0C. Following bisque firing, studio staff apply the participant's chosen glaze and conduct a second high-temperature glaze firing at 1,240\u00b0C. Completed ceramic wares are ready for collection four weeks after the workshop date. Uncollected wares are donated to community charity shops after sixty days.",
        "s1_questions": [
            {
                "id": "Q1",
                "type": "True/False/Not Given",
                "question_text": "Swimmers in lane swimming sessions may swim in either direction within their lane.",
                "correct_answer": "FALSE",
                "explanation": "Text A states: 'Swimmers must observe the clockwise rotation indicated by direction signs.'"
            },
            {
                "id": "Q2",
                "type": "True/False/Not Given",
                "question_text": "Children under four years old do not pay an admission charge at Riverside Aquatic Centre.",
                "correct_answer": "TRUE",
                "explanation": "Text A states: 'Children under four swim free.'"
            },
            {
                "id": "Q3",
                "type": "True/False/Not Given",
                "question_text": "One adult may supervise three six-year-old children in the pool at the same time.",
                "correct_answer": "FALSE",
                "explanation": "Text A states: 'at a strict ratio of no more than two children per adult.'"
            },
            {
                "id": "Q4",
                "type": "True/False/Not Given",
                "question_text": "Swimmers must wear outdoor shoes when walking around the edge of the competition pool.",
                "correct_answer": "FALSE",
                "explanation": "Text A states: 'Outdoor footwear is forbidden in the poolside zone'."
            },
            {
                "id": "Q5",
                "type": "True/False/Not Given",
                "question_text": "Artisan Guild pottery workshops are held every Saturday throughout the year.",
                "correct_answer": "FALSE",
                "explanation": "Text B states: 'Workshops run on alternate Saturdays'."
            },
            {
                "id": "Q6",
                "type": "True/False/Not Given",
                "question_text": "Each beginner pottery workshop is limited to a maximum of ten attendees.",
                "correct_answer": "TRUE",
                "explanation": "Text B states: 'class size is strictly capped at ten participants per session.'"
            },
            {
                "id": "Q7",
                "type": "True/False/Not Given",
                "question_text": "Finished pottery pieces can be picked up immediately at the end of the Saturday session.",
                "correct_answer": "FALSE",
                "explanation": "Text B states wares require two weeks air drying and firings, ready for collection after four weeks."
            },
            {
                "id": "Q8",
                "type": "Sentence Completion",
                "question_text": "Public lane swimming sessions run in increments of ____________ minutes.",
                "correct_answer": "60",
                "explanation": "Text A: 'Public sessions operate in 60-minute increments'."
            },
            {
                "id": "Q9",
                "type": "Sentence Completion",
                "question_text": "Online swimming slot reservations open ____________ hours in advance.",
                "correct_answer": "forty-eight",
                "explanation": "Text A: 'Online reservations open forty-eight hours in advance'."
            },
            {
                "id": "Q10",
                "type": "Sentence Completion",
                "question_text": "Swimmers must take a ____________ shower before entering the swimming pools.",
                "correct_answer": "cleansing pre-swim",
                "explanation": "Text A: 'must take a cleansing pre-swim shower before entering the pool.'"
            },
            {
                "id": "Q11",
                "type": "Sentence Completion",
                "question_text": "The midday lunch intermission during the pottery workshop begins at ____________.",
                "correct_answer": "12:30",
                "explanation": "Text B: 'with a one-hour lunch break at 12:30.'"
            },
            {
                "id": "Q12",
                "type": "Sentence Completion",
                "question_text": "Tuition covers ____________ kilograms of stoneware clay per participant.",
                "correct_answer": "twelve",
                "explanation": "Text B: 'covers twelve kilograms of stoneware clay'."
            },
            {
                "id": "Q13",
                "type": "Sentence Completion",
                "question_text": "Preliminary bisque firing in the kiln takes place at a temperature of ____________ \u00b0C.",
                "correct_answer": "1,000",
                "explanation": "Text B: 'bisque firing in the studio kiln at 1,000\u00b0C.'"
            },
            {
                "id": "Q14",
                "type": "Sentence Completion",
                "question_text": "Completed ceramic items left uncollected after ____________ days are donated to charity.",
                "correct_answer": "sixty",
                "explanation": "Text B: 'donated to community charity shops after sixty days.'"
            }
        ],
        "s2_title": "Section 2: Workplace Context \u2013 Equal Opportunity & Parental Rights (Texts C & D)",
        "s2_text": "Text C: Sterling Corporation \u2013 Dignity at Work and Anti-Harassment Policy\nSterling Corporation is dedicated to fostering a professional work culture based on mutual dignity, respect, and equal opportunity, completely free from bullying, intimidation, and unlawful discrimination.\n\nScope and Protected Characteristics:\nThis policy applies to all permanent staff, contract personnel, and job applicants. Discrimination or harassment on the grounds of age, disability, gender reassignment, marriage, pregnancy, race, religion, sex, or sexual orientation will not be tolerated. The policy governs behavior in physical offices, at client locations, and at work-sponsored social gatherings.\n\nReporting Channels:\n1. Informal Channel: If comfortable doing so, the employee should inform the offending individual directly that their conduct is offensive and must cease immediately.\n2. Formal Channel: Where informal discussion is inappropriate, ineffective, or where serious misconduct is alleged, the employee should submit a formal complaint in writing to the Head of Employee Relations.\n3. Whistleblowing Helpline: An independent 24/7 confidential helpline (0800 999 442) is available for employees wishing to disclose harassment anonymously.\n\nInvestigation Standards and Disciplinary Consequences:\nAll formal allegations are investigated by an independent investigation officer within fifteen working days. Both parties have the right to provide witness statements and documentary evidence. Any employee found guilty of unlawful harassment or retaliatory victimization will be subject to disciplinary sanctions, up to and including gross misconduct dismissal without notice.\n\n--------------------------------------------------------------------------------\nText D: Sterling Corporation \u2013 Parental Leave, Maternity Provisions & Flexible Working\nSterling Corporation provides comprehensive parental and family support packages that surpass statutory minimum benchmarks.\n\nMaternity and Adoption Leave:\nAll pregnant employees and primary adoptive parents are entitled to fifty-two weeks of Statutory Maternity Leave, regardless of their length of company service.\n- Enhanced Maternity Pay: Employees with at least twenty-six weeks of continuous service at the qualifying week receive full basic salary for the first sixteen weeks, followed by fifty percent basic pay for the subsequent ten weeks, and standard statutory pay thereafter.\n- Keeping in Touch (KIT) Days: Employees may undertake up to ten paid KIT days during their maternity leave without bringing their leave period to an end.\n\nPaternity and Partner Leave:\nFathers and secondary partners are entitled to two consecutive weeks of paid Paternity Leave taken within fifty-six days of the child's birth, remunerated at full basic contractual pay.\n\nStatutory Flexible Working Requests:\nAll personnel have the legal right to submit a formal Flexible Working Request from their first day of employment. Requests may seek changes to working hours, condensed four-day working weeks, or remote home-working arrangements. Employees may submit up to two formal requests within any twelve-month period. Management must consult with the employee and issue a written final decision within two months of receiving the application.",
        "s2_questions": [
            {
                "id": "Q15",
                "type": "Sentence Completion",
                "question_text": "The anti-harassment policy extends to company offices, client premises, and ____________.",
                "correct_answer": "work-sponsored social gatherings",
                "explanation": "Text C: 'in physical offices, at client locations, and at work-sponsored social gatherings.'"
            },
            {
                "id": "Q16",
                "type": "Sentence Completion",
                "question_text": "Anonymous disclosures of workplace harassment can be phoned in via the ____________.",
                "correct_answer": "Whistleblowing Helpline",
                "explanation": "Text C: 'Whistleblowing Helpline: An independent 24/7 confidential helpline'."
            },
            {
                "id": "Q17",
                "type": "Sentence Completion",
                "question_text": "Formal harassment complaints must be investigated within ____________ working days.",
                "correct_answer": "fifteen",
                "explanation": "Text C: 'investigated by an independent investigation officer within fifteen working days.'"
            },
            {
                "id": "Q18",
                "type": "Sentence Completion",
                "question_text": "Severe harassment may result in dismissal without notice for ____________.",
                "correct_answer": "gross misconduct",
                "explanation": "Text C: 'up to and including gross misconduct dismissal without notice.'"
            },
            {
                "id": "Q19",
                "type": "Sentence Completion",
                "question_text": "Employees qualify for enhanced maternity pay after completing ____________ weeks of service.",
                "correct_answer": "twenty-six",
                "explanation": "Text D: 'with at least twenty-six weeks of continuous service'."
            },
            {
                "id": "Q20",
                "type": "Sentence Completion",
                "question_text": "Mothers on maternity leave are permitted up to ten paid ____________ days.",
                "correct_answer": "KIT",
                "explanation": "Text D: 'up to ten paid KIT days during their maternity leave'."
            },
            {
                "id": "Q21",
                "type": "Sentence Completion",
                "question_text": "Management must deliver a written decision on flexible work requests within ____________.",
                "correct_answer": "two months",
                "explanation": "Text D: 'issue a written final decision within two months of receiving the application.'"
            },
            {
                "id": "Q22",
                "type": "True/False/Not Given",
                "question_text": "Harassment occurring at an off-site corporate Christmas party is covered by company policy.",
                "correct_answer": "TRUE",
                "explanation": "Text C explicitly governs behavior at work-sponsored social gatherings."
            },
            {
                "id": "Q23",
                "type": "True/False/Not Given",
                "question_text": "All pregnant employees are entitled to fifty-two weeks of leave regardless of length of service.",
                "correct_answer": "TRUE",
                "explanation": "Text D states: 'entitled to fifty-two weeks... regardless of their length of company service.'"
            },
            {
                "id": "Q24",
                "type": "True/False/Not Given",
                "question_text": "Secondary partners receive 80% of basic pay during their two weeks of paternity leave.",
                "correct_answer": "FALSE",
                "explanation": "Text D states paternity leave is 'remunerated at full basic contractual pay' (100%)."
            },
            {
                "id": "Q25",
                "type": "True/False/Not Given",
                "question_text": "An employee must have worked for at least six months before submitting a flexible working request.",
                "correct_answer": "FALSE",
                "explanation": "Text D states employees have the right 'from their first day of employment.'"
            },
            {
                "id": "Q26",
                "type": "True/False/Not Given",
                "question_text": "An employee may submit three formal flexible working applications in a single year.",
                "correct_answer": "FALSE",
                "explanation": "Text D states employees may submit 'up to two formal requests within any twelve-month period.'"
            },
            {
                "id": "Q27",
                "type": "True/False/Not Given",
                "question_text": "Flexible working arrangements can be revoked by managers after a trial period of three months.",
                "correct_answer": "NOT GIVEN",
                "explanation": "Text D outlines application limits and two-month decision times, but does not discuss revocation rules."
            }
        ],
        "s3_title": "Section 3: Oasis in the Abyss: The Discovery and Ecology of Hydrothermal Vents",
        "s3_text": "Paragraph A\nUntil the late 1970s, fundamental biological dogma held that all life on Earth was ultimately powered by solar irradiance. Photosynthesis\u2014the photochemical process whereby plants and phytoplankton convert sunlight, carbon dioxide, and water into organic glucose\u2014was considered the mandatory energetic foundation for every terrestrial and marine food web. Science assumed that the deep abyssal ocean floor, plunged into eternal darkness, frigid near-freezing temperatures, and crushing hydrostatic pressures exceeding 250 atmospheres, was a biological desert populated only by scarce scavengers feeding on organic detritus falling from the sunlit surface waters above.\n\nParagraph B\nThis ecological paradigm was shattered in 1977 during an oceanographic geological expedition to the Galapagos Rift, an underwater volcanic spreading center located 2,500 metres beneath the Pacific Ocean. Geologists aboard the deep-submergence research submarine Alvin were mapping geothermal hot springs along the tectonic boundary when they encountered an astonishing sight. Surrounding volcanic fissures gushing mineral-black fluids at temperatures exceeding 350 degrees Celsius was a dense, thriving biological metropolis. Clustered around the vent chimneys were two-metre-long red-plumed tube worms, giant white clams the size of dinner plates, ghostly albino crabs, and undulating eel-like fish\u2014densities of biomass rivaling tropical coral reefs and equatorial rainforests.\n\nParagraph C\nThe mystery of how complex organisms could thrive in a pitch-black abyss without sunlight was solved when microbiologists analyzed water samples from the plumes. They identified dense populations of specialized chemoautotrophic bacteria. Rather than harnessing photon energy from the Sun, these extremophile bacteria perform chemosynthesis: they oxidize toxic hydrogen sulfide gas dissolved in the superheated geothermal fluid, using the liberated chemical energy to convert inorganic carbon into nutrient biomass. These sulfur-oxidizing bacteria represent the true primary producers of the hydrothermal vent biome, supporting an entire food pyramid that operates completely independently of solar photosynthesis.\n\nParagraph D\nAmong the most bizarre organisms discovered at hydrothermal vents is Riftia pachyptila, the giant hydrothermal tube worm. Encased within tough white tubes made of chitin and protein, these creatures possess neither mouth, gut, nor digestive tract. Instead, their visceral cavity is filled with a specialized vascular organ called a trophosome, which houses billions of symbiotic sulfur-oxidizing bacteria. The worm's brilliant crimson plume\u2014colored by highly specialized hemoglobin molecules capable of binding hydrogen sulfide and oxygen simultaneously without suffering chemical poisoning\u2014absorbs dissolved chemicals from the hydrothermal plume and transports them to the bacteria, which in turn nourish the host worm with organic carbohydrates.\n\nParagraph E\nHydrothermal vents themselves, often called 'black smokers', are dynamic geological structures formed along mid-ocean ridge spreading zones where tectonic plates diverge. Seawater seeps deep into fractures in the oceanic crust, where it is heated by magma chambers to temperatures exceeding 400\u00b0C. Under intense pressure, the superheated water leaches heavy metals\u2014including iron, copper, zinc, and gold\u2014from the surrounding basalt bedrock. When this buoyant, mineral-saturated fluid erupts into the freezing 2\u00b0C ocean water, the dissolved metals instantly precipitate out of solution as fine dark sulfide minerals, building towering mineral chimneys that can reach heights of thirty metres before collapsing under their own mass.\n\nParagraph F\nThe ephemeral lifespan of hydrothermal vents presents extreme evolutionary challenges for resident fauna. Because volcanic vents are fueled by shifting sub-crustal magma movements, individual hydrothermal chimneys typically remain active for only a few decades before volcanism ceases, abruptly starving the local chemosynthetic ecosystem. Vent organisms have evolved remarkable larval dispersal strategies to locate new active vents hundreds of kilometres away across the barren seafloor. Some larvae drift along deep ocean currents, detecting microscopic thermal plumes and acoustic vibrations from active chimneys, while others utilize whale carcass 'stepping stones' on the abyssal plain to sustain their populations during cross-ocean voyages.\n\nParagraph G\nThe discovery of hydrothermal vent ecosystems has fundamentally revolutionized astrobiology and the search for extraterrestrial life. Planetary scientists now recognize that analogous chemosynthetic biospheres could exist within the subterranean oceans of icy moons in our solar system, notably Jupiter's moon Europa and Saturn's moon Enceladus. Both moons possess liquid water oceans hidden beneath miles of planetary surface ice, sustained by tidal heating and geothermal seafloor venting. If life arose independently around volcanic fissures in the lightless oceans of ancient Earth, it may very well have sparked into existence under identical conditions in the dark oceans of the outer solar system.",
        "s3_questions": [
            {
                "id": "Q28",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph A?",
                "options": [
                    "i. The historic assumption of photosynthesis supremacy",
                    "ii. An unexpected deep-sea biological metropolis",
                    "iii. Chemosynthesis: Primary production without sunlight",
                    "iv. Symbiotic adaptations of the giant tube worm",
                    "v. Geological genesis of towering black smokers",
                    "vi. Ephemeral vent lifespans and larval migration",
                    "vii. Astrobiological implications for icy solar moons"
                ],
                "correct_answer": "i. The historic assumption of photosynthesis supremacy",
                "explanation": "Paragraph A explains that scientists previously believed all life relied on solar photosynthesis, assuming the deep ocean was a biological desert."
            },
            {
                "id": "Q29",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph B?",
                "options": [
                    "i. The historic assumption of photosynthesis supremacy",
                    "ii. An unexpected deep-sea biological metropolis",
                    "iii. Chemosynthesis: Primary production without sunlight",
                    "iv. Symbiotic adaptations of the giant tube worm",
                    "v. Geological genesis of towering black smokers",
                    "vi. Ephemeral vent lifespans and larval migration",
                    "vii. Astrobiological implications for icy solar moons"
                ],
                "correct_answer": "ii. An unexpected deep-sea biological metropolis",
                "explanation": "Paragraph B describes the 1977 Alvin submersible discovery of dense animal life around hot springs at the Galapagos Rift."
            },
            {
                "id": "Q30",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph C?",
                "options": [
                    "i. The historic assumption of photosynthesis supremacy",
                    "ii. An unexpected deep-sea biological metropolis",
                    "iii. Chemosynthesis: Primary production without sunlight",
                    "iv. Symbiotic adaptations of the giant tube worm",
                    "v. Geological genesis of towering black smokers",
                    "vi. Ephemeral vent lifespans and larval migration",
                    "vii. Astrobiological implications for icy solar moons"
                ],
                "correct_answer": "iii. Chemosynthesis: Primary production without sunlight",
                "explanation": "Paragraph C details the discovery of chemoautotrophic bacteria oxidizing hydrogen sulfide gas."
            },
            {
                "id": "Q31",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph D?",
                "options": [
                    "i. The historic assumption of photosynthesis supremacy",
                    "ii. An unexpected deep-sea biological metropolis",
                    "iii. Chemosynthesis: Primary production without sunlight",
                    "iv. Symbiotic adaptations of the giant tube worm",
                    "v. Geological genesis of towering black smokers",
                    "vi. Ephemeral vent lifespans and larval migration",
                    "vii. Astrobiological implications for icy solar moons"
                ],
                "correct_answer": "iv. Symbiotic adaptations of the giant tube worm",
                "explanation": "Paragraph D discusses Riftia pachyptila, its trophosome, and sulfur-binding hemoglobin."
            },
            {
                "id": "Q32",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph E?",
                "options": [
                    "i. The historic assumption of photosynthesis supremacy",
                    "ii. An unexpected deep-sea biological metropolis",
                    "iii. Chemosynthesis: Primary production without sunlight",
                    "iv. Symbiotic adaptations of the giant tube worm",
                    "v. Geological genesis of towering black smokers",
                    "vi. Ephemeral vent lifespans and larval migration",
                    "vii. Astrobiological implications for icy solar moons"
                ],
                "correct_answer": "v. Geological genesis of towering black smokers",
                "explanation": "Paragraph E outlines how black smoker chimneys form from superheated seawater precipitating metal sulfides."
            },
            {
                "id": "Q33",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph F?",
                "options": [
                    "i. The historic assumption of photosynthesis supremacy",
                    "ii. An unexpected deep-sea biological metropolis",
                    "iii. Chemosynthesis: Primary production without sunlight",
                    "iv. Symbiotic adaptations of the giant tube worm",
                    "v. Geological genesis of towering black smokers",
                    "vi. Ephemeral vent lifespans and larval migration",
                    "vii. Astrobiological implications for icy solar moons"
                ],
                "correct_answer": "vi. Ephemeral vent lifespans and larval migration",
                "explanation": "Paragraph F covers vent lifespans and the dispersal mechanisms of drifting larvae."
            },
            {
                "id": "Q34",
                "type": "Matching Headings",
                "question_text": "Which heading best summarizes Paragraph G?",
                "options": [
                    "i. The historic assumption of photosynthesis supremacy",
                    "ii. An unexpected deep-sea biological metropolis",
                    "iii. Chemosynthesis: Primary production without sunlight",
                    "iv. Symbiotic adaptations of the giant tube worm",
                    "v. Geological genesis of towering black smokers",
                    "vi. Ephemeral vent lifespans and larval migration",
                    "vii. Astrobiological implications for icy solar moons"
                ],
                "correct_answer": "vii. Astrobiological implications for icy solar moons",
                "explanation": "Paragraph G discusses the search for life in the oceans of Europa and Enceladus."
            },
            {
                "id": "Q35",
                "type": "Multiple Choice",
                "question_text": "Chemosynthetic bacteria at hydrothermal vents obtain their energy from:",
                "options": [
                    "A. Filtering microscopic algae falling from the ocean surface.",
                    "B. Oxidizing toxic hydrogen sulfide dissolved in geothermal fluid.",
                    "C. Absorbing low-frequency infrared light radiated by magma.",
                    "D. Breaking down heavy metal ores such as copper and gold."
                ],
                "correct_answer": "B. Oxidizing toxic hydrogen sulfide dissolved in geothermal fluid.",
                "explanation": "Paragraph C explains that bacteria oxidize toxic hydrogen sulfide gas to convert inorganic carbon into biomass."
            },
            {
                "id": "Q36",
                "type": "Multiple Choice",
                "question_text": "How do adult giant tube worms digest their food?",
                "options": [
                    "A. They ingest sediment using muscular microscopic tentacles.",
                    "B. They catch swimming albino crabs in their crimson plumes.",
                    "C. They rely completely on symbiotic bacteria living inside their trophosome.",
                    "D. They absorb sunlight stored in deep hydrothermal minerals."
                ],
                "correct_answer": "C. They rely completely on symbiotic bacteria living inside their trophosome.",
                "explanation": "Paragraph D states worms have no mouth or gut; symbiotic bacteria inside their trophosome nourish them with carbohydrates."
            },
            {
                "id": "Q37",
                "type": "Multiple Choice",
                "question_text": "Why do black smoker chimneys eventually collapse?",
                "options": [
                    "A. Giant clams bore into the mineral walls and destabilize them.",
                    "B. They grow up to thirty metres tall and collapse under their own physical mass.",
                    "C. Underwater earthquakes demolish all chimneys every five years.",
                    "D. Submarines accidentally collide with them during surveys."
                ],
                "correct_answer": "B. They grow up to thirty metres tall and collapse under their own physical mass.",
                "explanation": "Paragraph E states chimneys can reach thirty metres before collapsing under their own mass."
            },
            {
                "id": "Q38",
                "type": "True/False/Not Given",
                "question_text": "Prior to 1977, biologists believed the abyssal seafloor was devoid of dense, complex communities.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph A confirms it was assumed to be a biological desert populated only by scarce scavengers."
            },
            {
                "id": "Q39",
                "type": "True/False/Not Given",
                "question_text": "The research submersible Alvin was operated by an autonomous robotic computer.",
                "correct_answer": "FALSE",
                "explanation": "Paragraph B describes 'Geologists aboard the deep-submergence research submarine Alvin', showing it was manned."
            },
            {
                "id": "Q40",
                "type": "True/False/Not Given",
                "question_text": "Both Europa and Enceladus possess subterranean liquid water oceans warmed by geothermal activity.",
                "correct_answer": "TRUE",
                "explanation": "Paragraph G confirms both moons have oceans hidden under surface ice with geothermal seafloor venting."
            }
        ]
    }
]

# ==============================================================================
# GENERAL TRAINING WRITING TASK 1 (LETTERS) - 6 COMPLETE TASKS
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
        "band9_sample": "Dear Tom,\n\nI hope you're having a brilliant week! I'm finally settled into my new flat here in Edinburgh, and I couldn't wait to write and tell you all about it.\n\nThe neighbourhood I've moved into, Stockbridge, is absolutely charming. It has cobblestone lanes, wonderful independent bookshops, and an incredible Sunday farmers' market right around the corner. The city has so much character\u2014even on drizzly afternoons, there\u2019s an infectious energy about the place that I know you\u2019d fall in love with.\n\nSince I\u2019ve finally unpacked and set up the guest bedroom, I would love for you to come up and stay for a long weekend. How about the bank holiday weekend from the 3rd to the 6th of May? The spring weather should be lovely by then, and direct trains from London only take about four hours.\n\nI've already started putting together a mini-itinerary for us. We can hike up Arthur's Seat on Saturday morning for a panoramic view across the Firth of Forth, grab lunch at an authentic Scottish pub, and spend Sunday exploring the Old Town and the National Museum. We can even take an evening ghost tour through the underground vaults if you're feeling adventurous!\n\nLet me know if those dates work for you so I can keep the weekend completely free.\n\nWarm regards,\n\nLiam"
    },
    {
        "subtype": "Formal Letter",
        "title": "Formal Resignation Notice and Project Handover Plan",
        "prompt": "You should spend about 20 minutes on this task.\n\nYou have recently accepted a new employment opportunity and need to resign from your current position.\n\nWrite a formal letter to your department director. In your letter:\n- State clearly that you are resigning and specify your final working day\n- Express appreciation for the opportunities and professional experience gained\n- Outline a handover plan for your ongoing projects and offer assistance in training your replacement\n\nWrite at least 150 words.\nYou do NOT need to write any addresses.\nBegin your letter as follows: Dear Mr. Harrison,",
        "band9_sample": "Dear Mr. Harrison,\n\nPlease accept this letter as formal notification that I am resigning from my position as Senior Project Coordinator at Apex Solutions. In accordance with my employment contract, my notice period is four weeks, which means my final working day will be Friday, 28th November.\n\nI would like to take this opportunity to express my sincere gratitude for the support and professional development opportunities provided to me during my three years with the organization. It has been a genuine privilege to collaborate with such a talented multidisciplinary team, and I am especially grateful for the guidance you extended during the successful delivery of the European Logistics Upgrade.\n\nTo ensure a seamless transition of my operational responsibilities before my departure, I have prepared a comprehensive handover folder documenting the current status, key milestones, and stakeholder contacts for all ongoing client accounts. Over the next fortnight, I intend to finalize the quarterly performance audit and delegate daily operational oversight of the Nordic supply contract to Sarah Jenkins. Furthermore, I am fully prepared to assist in screening candidates or training my designated successor during my remaining time with the firm.\n\nI wish you, the department, and Apex Solutions continued success in all future endeavors.\n\nYours sincerely,\nJulian Vance"
    },
    {
        "subtype": "Semi-formal Letter",
        "title": "Request for Temporary Medical Freeze of Health Club Membership",
        "prompt": "You should spend about 20 minutes on this task.\n\nYou are a member of a local fitness club, but due to a recent sports injury, you are unable to exercise for several months.\n\nWrite a letter to the fitness club manager. In your letter:\n- Explain the circumstances of your medical injury\n- Request a three-month temporary suspension of your membership\n- Inquire about the administrative requirements and confirm the adjustment to your monthly direct debit\n\nWrite at least 150 words.\nYou do NOT need to write any addresses.\nBegin your letter as follows: Dear Club Manager,",
        "band9_sample": "Dear Club Manager,\n\nI am writing to formally request a temporary suspension of my annual gym membership (Membership No. HM-48291) at the Westbridge Health and Fitness Club due to an unforeseen medical setback.\n\nLast weekend, while participating in a regional amateur tennis tournament, I sustained a severe fracture to my left ankle that required surgical immobilization. My orthopedic consultant has advised strict non-weight-bearing rest followed by intensive physical rehabilitation, precluding me from using any gym equipment, weights, or pool facilities for at least twelve weeks.\n\nUnder clause 4.2 of the membership agreement, members who suffer certified medical injuries are permitted to freeze their account without penalty. I would therefore like to request that my membership be placed on hold for a period of three months, commencing on 1st November and resuming on 1st February.\n\nI have enclosed a signed medical certificate from Dr. Clara Evans at St. Jude Hospital verifying the diagnosis and recovery prognosis. Could you please confirm in writing that this documentation satisfies your requirements, and verify that the monthly direct debit of \u00a345.00 scheduled for November and December will be paused accordingly?\n\nThank you for your prompt attention and understanding.\n\nYours sincerely,\nMarcus Holloway"
    },
    {
        "subtype": "Informal Letter",
        "title": "Hospitality Gratitude and Retrieving Forgotten Sunglasses",
        "prompt": "You should spend about 20 minutes on this task.\n\nYou recently spent a long weekend staying at a friend's house in another town. After returning home, you realized that you left an item behind.\n\nWrite a letter to your friend. In your letter:\n- Thank them for their hospitality and mention what you enjoyed most about the visit\n- Explain what item you left behind and describe where it might be\n- Ask if they can post the item to you and offer to reimburse the postage costs\n\nWrite at least 150 words.\nYou do NOT need to write any addresses.\nBegin your letter as follows: Dear Liam,",
        "band9_sample": "Dear Liam,\n\nI arrived back in Bristol safely on Sunday evening, and I wanted to drop you a quick line to thank you and Sophie for such a fantastic long weekend. It was so great to catch up properly after such a long time! I had a wonderful time exploring the coastal walking trails around Port Isaac, and that home-cooked seafood risotto you made on Saturday night was honestly restaurant-worthy.\n\nUnfortunately, as I was unpacking my luggage yesterday morning, I realized that I had managed to leave my prescription sunglasses behind. They are in a matte black hard case, and I am fairly certain I left them on the small wooden bedside table in your guest bedroom, or possibly on the kitchen counter next to the coffee grinder.\n\nIf you happen to find them, would you mind posting them to my home address when you next head to the post office? There is absolutely no rush at all, so please only do it whenever it is convenient for you. Please let me know how much the tracked parcel postage costs so I can transfer the money straight into your bank account.\n\nThanks a million again for being such fabulous hosts, and I hope you can make it down to Bristol for a return visit very soon!\n\nWarm regards,\nAlex"
    }
]

# ==============================================================================
# GENERAL TRAINING WRITING TASK 2 (ESSAYS) - 6 COMPLETE DISCURSIVE ESSAYS
# ==============================================================================

GT_WRITING_TASK2_COLLECTION = [
    {
        "subtype": "Discussion Essay",
        "title": "Working From Home vs Office Collaboration for Employee Productivity and Wellbeing",
        "prompt": "You should spend about 40 minutes on this task.\n\nSome people believe that working from home provides significant advantages for both workers and companies, while others argue that working in a traditional office environment is essential for productivity and teamwork.\n\nDiscuss both views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "The dramatic proliferation of remote working technologies has provoked intense debate regarding the optimal workspace for the contemporary workforce. While proponents of telecommuting emphasize enhanced work-life balance and operational cost efficiencies, detractors contend that in-person office interaction remains indispensable for collaborative innovation and accountability. This essay examines both perspectives before arguing that a flexible hybrid paradigm represents the most efficacious compromise.\n\nOn the one hand, remote working confers substantial personal and professional benefits. Primarily, the elimination of lengthy daily commutes liberates considerable time and financial resources, thereby reducing chronic stress and fatigue among employees. Workers often report higher concentrations of uninterrupted deep focus in home environments, particularly when performing analytical or written tasks. Furthermore, employers benefit from reduced capital expenditure on commercial real estate leases, utility consumption, and on-site facilities management, while concurrently accessing a geographically diverse talent pool unrestricted by municipal boundaries.\n\nConversely, traditional office spaces fulfill vital social and collaborative functions that digital communication platforms struggle to replicate. Spontaneous, serendipitous interactions around communal areas frequently serve as the catalyst for creative problem-solving and cross-departmental synergy. Moreover, junior employees rely heavily on informal, observational learning from experienced colleagues\u2014an educational osmosis severely attenuated in isolated remote environments. Prolonged isolation can also blur the boundaries between domestic life and occupational responsibilities, culminating in burnout and weakened organizational loyalty.\n\nIn conclusion, while working from home optimizes individual focus and personal autonomy, physical office presence remains essential for fostering corporate culture, mentorship, and spontaneous team collaboration. In my view, the optimal approach is a balanced hybrid model in which personnel combine remote working for solitary tasks with two to three days on-site dedicated to collaborative endeavors."
    },
    {
        "subtype": "Opinion Essay",
        "title": "Public Transport Subsidies vs Road Construction for Alleviating Urban Traffic Congestion",
        "prompt": "You should spend about 40 minutes on this task.\n\nIn many cities, traffic congestion is a serious problem. Some people suggest that the best solution is for governments to make public transport free, while others believe that building more roads is more effective.\n\nDiscuss both views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "Metropolitan traffic congestion represents one of the most debilitating socioeconomic challenges confronting modern urban planners. While certain commentators advocate for the expansion of highway networks, others argue that subsidizing public transit to make it entirely cost-free is a far more sustainable remedy. In my view, investing in free, high-capacity mass transit systems is markedly superior to road building, which invariably exacerbates urban gridlock through induced vehicular demand.\n\nProponents of highway construction contend that widening existing arteries and constructing bypasses provides immediate capacity relief for burgeoning vehicular volumes. In expanding economies where industrial logistics depend heavily on freight transit, modern road infrastructure is undeniably vital for economic competitiveness. However, decades of transportation research have comprehensively demonstrated the phenomenon of 'induced demand': when additional road capacity is constructed, it initially lowers travel times, which subsequently incentivizes more motorists to drive, ultimately returning the expanded highway to total congestion within a few years.\n\nIn contrast, abolishing fares on municipal public transport offers a transformative economic and behavioral incentive for commuters to abandon private passenger vehicles. When transit is free, reliable, and frequent, substantial segments of the commuting public transition toward electrified commuter rail, subways, and bus rapid transit systems. Cities such as Tallinn and Montpellier, which introduced free public transportation, experienced immediate declines in urban vehicle emissions and rush-hour bottlenecks. Furthermore, cost-free public transit democratizes urban mobility, ensuring low-income residents can access employment and educational opportunities across metropolitan regions without financial impediment.\n\nTo conclude, although expanding road infrastructure may appear to be a straightforward remedy, it inevitably fails due to induced traffic demand. Governments should instead allocate fiscal resources toward delivering comprehensive, high-frequency, and zero-fare public transportation networks."
    },
    {
        "subtype": "Discussion and Opinion",
        "title": "The Four-Day Work Week: Productivity vs Economic Disruption",
        "prompt": "You should spend about 40 minutes on this task.\n\nIn many countries, there is a growing debate about reducing the standard working week from five days to four days without any reduction in salary.\n\nSome believe this increases employee wellbeing and productivity, while others argue it would disrupt business operations and harm the economy.\n\nDiscuss both views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "The proposition of transitioning to a four-day working week with no corresponding loss in remuneration has emerged as a cornerstone of modern labor reform discussions. While sceptics contend that compressing working schedules risks damaging commercial productivity and competitiveness, proponents argue that shorter working hours optimize employee wellbeing and output quality. In my opinion, adopting a four-day working model delivers substantial net societal and economic advantages, provided that implementation is tailored flexibly across distinct industrial sectors.\n\nOn the one hand, critics of a compressed working week maintain that many economic sectors fundamentally rely on continuous physical presence and five-day operational coverage. In client-facing industries such as retail banking, healthcare provision, logistics, and emergency manufacturing, closing operations for an extra weekday could lead to severe backlogs, diminished client satisfaction, and inflated overtime labor costs. Furthermore, smaller commercial enterprises with tight operating margins might struggle to recruit additional personnel to bridge coverage gaps, potentially rendering them uncompetitive against international rivals operating in standard forty-hour jurisdictions.\n\nConversely, modern industrial psychology suggests that elongated working hours do not correlate linearly with productivity. Extensive trials conducted across the United Kingdom, Iceland, and Japan have conclusively demonstrated that employees on a four-day schedule experience significantly lower rates of occupational burnout, chronic stress, and sickness absence. With three full days of rest, workers return to duty revitalized, displaying sharper cognitive focus and reduced workplace errors. Moreover, the imperative to compress weekly outputs into thirty-two hours frequently impels organizations to streamline inefficient internal processes, eliminate redundant meetings, and automate administrative tasks, thereby producing equal or superior economic output in less time.\n\nTo conclude, while certain operational sectors require phased adjustments or staggered scheduling, the overarching benefits of a four-day working week in terms of employee mental health, talent retention, and concentrated productivity far outweigh the logistical challenges. Governments and progressive businesses should proactively explore compressed work schedules as the sustainable future of labor."
    },
    {
        "subtype": "Opinion Essay",
        "title": "Mass International Tourism: Economic Lifeline vs Environmental and Cultural Strain",
        "prompt": "You should spend about 40 minutes on this task.\n\nInternational tourism has grown significantly in recent decades, bringing economic benefits to host countries. However, many people believe that the environmental and cultural disadvantages of mass tourism outweigh its benefits.\n\nTo what extent do you agree or disagree?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "The dramatic expansion of global travel over recent decades has converted international tourism into a multibillion-dollar economic juggernaut. While host destinations undeniably gain substantial foreign exchange revenue and infrastructural development, critics assert that the environmental degradation and cultural commodification wrought by uncurbed visitor influxes constitute an unbearable burden. I largely agree with this viewpoint, as the irreparable ecological damage and societal displacement inflicted by mass tourism frequently eclipse its short-term financial windfalls.\n\nThe foremost casualty of uncontrolled tourism is the natural environment. Fragile marine ecosystems, pristine coastal wetlands, and Alpine habitats have suffered catastrophic degradation under the weight of excessive tourist traffic. In renowned destinations such as Maya Bay in Thailand or the Venetian lagoons, anchor damage from cruise vessels, untreated sewage discharges from beachfront resorts, and widespread plastic contamination have decimated local coral reefs and collapsed aquatic biodiversity. Furthermore, global commercial aviation and cruise transport generate immense carbon emissions, accelerating the global climate crisis while exhausting finite local freshwater aquifers in arid island economies.\n\nEqually pernicious is the cultural and socio-economic distortion inflicted upon resident communities. In historically celebrated cities like Barcelona, Amsterdam, and Dubrovnik, the uncontrolled proliferation of short-term holiday rentals has caused residential rental prices to skyrocket, pricing local families out of historic city centers and creating hollow tourist theme parks. Moreover, authentic indigenous traditions and sacred customs are often watered down and commodified into superficial spectacle to satisfy foreign expectations, eroding cultural integrity and breeding intense resentment among native populations.\n\nAdmittedly, for developing island nations with scarce natural resources, international hospitality represents an indispensable generator of employment and foreign capital. However, when tourism is permitted to expand without stringent carrying capacity limits, ecological degradation ultimately destroys the very natural beauty that attracted travelers in the first place.\n\nIn conclusion, although tourism yields demonstrable financial dividends, its environmental toll and cultural disruption represent profound liabilities. Governments must transition away from relentless volume growth toward high-value, strictly regulated ecotourism models that preserve local heritage and ecosystems."
    },
    {
        "subtype": "Advantages and Disadvantages",
        "title": "Digital Transition of Public Services: Efficiency vs Exclusion of the Elderly",
        "prompt": "You should spend about 40 minutes on this task.\n\nIn many countries today, an increasing number of essential public services, such as banking, healthcare appointment booking, and tax filing, are moving exclusively online.\n\nDo the advantages of this digital transition outweigh the disadvantages?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "In an era of rapid technological acceleration, public administrations and financial institutions worldwide are systematically digitizing essential civic services, migrating everything from medical appointment bookings to tax compliance onto internet portals. While this digital transition delivers unprecedented administrative efficiency and convenience for the digitally literate majority, it also introduces grave risks of disenfranchising older and less technologically adept citizens. In my assessment, the advantages of digitization outweigh the drawbacks, provided that governments preserve accessible analog safety nets for vulnerable demographics.\n\nThe principal merit of transitioning public services online lies in the immense gain in operational efficiency, transparency, and consumer convenience. Digital portals empower citizens to access public utilities, submit passport renewals, and manage financial transactions twenty-four hours a day, entirely freeing them from the inconvenience of traveling to municipal offices and standing in bureaucratic queues. For municipal authorities, automating repetitive clerical processes radically slashes administrative overheads, eliminates paper consumption, and minimizes human data entry errors. The fiscal savings generated can subsequently be redirected toward frontline public healthcare and social welfare infrastructure.\n\nConversely, the most concerning hazard of wholesale digitization is the systemic marginalization of senior citizens and low-income individuals who experience digital exclusion. Many elderly individuals lack high-speed broadband connections, modern smartphones, or the intuitive digital literacy required to navigate multifaceted online verification systems. When physical municipal counters and high-street bank branches close down permanently, these vulnerable citizens are frequently cut off from essential medical appointments, pension claims, and financial management, exposing them to acute anxiety and fraudulent cyber scams.\n\nNevertheless, digital exclusion is not an intractable consequence of technological progress; rather, it represents a policy failure that can be mitigated. Forward-thinking administrations have successfully instituted free community digital training courses at local public libraries, simplified user interface standards, and maintained dedicated telephone assistance helplines alongside roaming mobile administrative vans.\n\nIn conclusion, the migration of essential public amenities to digital architectures offers overwhelmingly positive dividends for societal efficiency and economic resource management. However, to ensure that progress remains equitable, authorities must never abandon the human and analog support channels upon which senior citizens continue to depend."
    },
    {
        "subtype": "Discussion and Opinion",
        "title": "Taxation on Unhealthy Foods vs Personal Freedom of Dietary Choice",
        "prompt": "You should spend about 40 minutes on this task.\n\nObesity and lifestyle-related health problems are rising globally. Some people argue that governments should impose high taxes on sugary and high-fat foods to encourage healthier eating habits, while others believe that individuals should have complete freedom over their dietary choices.\n\nDiscuss both views and give your own opinion.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\nWrite at least 250 words.",
        "band9_sample": "The dramatic surge in global obesity rates and lifestyle-related morbidities, including type-2 diabetes and cardiovascular disease, has ignited a fierce ideological debate over state intervention in personal nutrition. While libertarian advocates argue that food consumption is an intensely personal prerogative that must remain free from state interference, public health authorities contend that taxing unhealthy foods is an imperative economic and epidemiological necessity. In my view, targeted excise taxation on ultra-processed and sugary foodstuffs is entirely justified, given the immense collective burden that dietary illnesses place on publicly funded healthcare systems.\n\nOpponents of fiscal nutritional taxes frequently ground their objections on principles of personal liberty and economic fairness. They contend that adult citizens in a democratic society possess the fundamental right to decide what they consume without punitive financial coercion from the state. Furthermore, critics point out that regressive food taxes disproportionately penalize low-income families, who often rely on calorie-dense, inexpensive processed foods because fresh, organic produce is economically out of reach or unavailable in urban food deserts. Imposing additional taxes without making nutritious alternatives affordable could therefore exacerbate socioeconomic hardship without genuinely reforming long-term eating habits.\n\nOn the other hand, the argument for state intervention rests on the inescapable reality of positive and negative economic externalities. When millions of citizens suffer from preventable dietary diseases, the staggering clinical costs of emergency hospitalizations, chronic insulin therapies, and lost economic productivity are borne collectively by taxpayers through national health services. Just as punitive excise taxes on tobacco and alcohol have historically proven extraordinarily effective in suppressing consumption and saving millions of lives, levying taxes on sugar-sweetened beverages has produced immediate, demonstrable reductions in caloric intake in countries such as Mexico and the United Kingdom. Moreover, revenue generated from sugar taxes can be legally ring-fenced to subsidize fresh agricultural produce and fund physical education in public schools.\n\nIn conclusion, although individual consumer autonomy is an important social principle, it cannot supersede the government's duty to protect public health and maintain the viability of healthcare infrastructure. Selective taxation on ultra-processed foods represents a balanced, highly effective policy tool to steer populations toward sustainable, wholesome nutrition."
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

if __name__ == '__main__':
    seed_cambridge_gt_bank()
