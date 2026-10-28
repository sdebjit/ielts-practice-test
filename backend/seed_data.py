import json
from database import get_connection

# =====================================================================
# AUTHENTIC FULL-SCALE IELTS EXAM TEST BANK
# Listening: Full 40 Questions across 4 Sections
# Reading: Full 40 Questions across 3 Academic Passages (~2,700 words)
# Writing: Task 1 (150 words) & Task 2 (250 words) with Band 9 Models
# Speaking: Full 3-Part Guided Simulation
# =====================================================================

TESTS_DATA = [
    # -----------------------------------------------------------------
    # READING TEST 1: FULL 40 QUESTIONS (ACADEMIC)
    # -----------------------------------------------------------------
    {
        "id": "R-01",
        "module": "reading",
        "title": "IELTS Academic Reading Test 1 (Full 40 Questions / 3 Passages)",
        "type": "Academic",
        "duration_minutes": 60,
        "difficulty": "Authentic IELTS Standard",
        "content": {
            "passages": [
                # -----------------------------------------------------
                # PASSAGE 1: QUESTIONS 1 - 13 (~850 words)
                # -----------------------------------------------------
                {
                    "passage_num": 1,
                    "title": "The Chemistry and Evolution of Marine Bioluminescence",
                    "text": "Paragraph A\n"
                            "Bioluminescence—the emission of visible light by living organisms resulting from an internal biochemical reaction—is one of the most widespread yet mesmerizing physiological phenomena in the marine realm. Unlike incandescent anthropogenic illuminations that dissipate the vast majority of their energy as heat, biological luminescence is almost entirely chemiluminescent, with upwards of ninety percent of the reaction's energy converted directly into luminous radiance. For this reason, physicists and marine biologists frequently designate the phenomenon as 'cold light'. In the quintessential reaction, an enzyme generically designated as luciferase catalyzes the oxidative decarboxylation of an organic substrate called luciferin in the presence of molecular oxygen, yielding an electronically excited oxyluciferin intermediate that emits a photon upon relaxing to its ground state.\n\n"
                            "Paragraph B\n"
                            "While terrestrial bioluminescence is largely restricted to a few isolated insect families such as fireflies (Lampyridae) and click beetles, along with certain fungal taxa, marine bioluminescence is ubiquitous throughout the ocean's water column. Evolutionary biologists estimate that the capacity for bioluminescence has originated independently through convergent evolution in more than thirty distinct phylogenetic lineages, ranging from single-celled dinoflagellates and colonial radiolarians to cnidarians, cephalopods, and teleost fishes. This extraordinary independent divergence across taxonomically disparate clades demonstrates that the selective adaptive value of producing light in an aquatic medium with rapidly attenuating solar irradiance is immense.\n\n"
                            "Paragraph C\n"
                            "In the mesopelagic or 'twilight' zone, which extends between depths of two hundred and one thousand meters, sunlight penetrates only weakly, casting a dim, downward-directed directional shimmer. Under these optical conditions, any organism swimming in open water produces a sharp silhouette against the downwelling sunlight when viewed from below by upward-looking predators. To circumvent this fatal vulnerability, many pelagic teleosts, including lanternfish (Myctophidae) and hatchetfish (Sternoptychidae), have evolved counter-illumination. These species possess specialized arrays of ventral photophores that emit a diffuse bluish-green glow precisely calibrated in both spectral wavelength and intensity to match the downward illumination from the surface, effectively rendering their silhouettes transparent to predators lurking in deeper strata.\n\n"
                            "Paragraph D\n"
                            "Beyond concealment, bioluminescent systems are heavily deployed for offensive predatory acquisition. The most celebrated instance is found within the bathypelagic anglerfish (Ceratioidei), whose females possess an esca—a modified dorsal fin ray that dangles directly before their expansive jaws. The esca functions as an alluring, luminous bait in the midnight zone. Furthermore, while the overwhelming majority of marine light emitters produce wavelengths between 470 and 490 nanometers—optimizing transmission through clear seawater—certain predatory dragonfish (Stomiidae) produce far-red luminescence exceeding 700 nanometers. Because virtually all other deep-sea fauna lack visual photopigments capable of detecting red wavelengths, dragonfish essentially wield private, invisible sniper spotlights to illuminate unaware prey without disclosing their own position.\n\n"
                            "Paragraph E\n"
                            "Conversely, light serves as an indispensable defensive weapon for vulnerable soft-bodied invertebrates. Dinoflagellates, which form vast blooms near the surface, exhibit flashes when agitated by mechanical shear stress caused by swimming copepods. This phenomenon underpins the 'burglar alarm' hypothesis: by illuminating the herbivorous grazer, the dinoflagellate exposes the copepod to higher-tier visual predators such as small fish, thereby curbing grazing pressure. Other creatures, such as the deep-sea squid Heteroteuthis dispar, eject an iridescent cloud of luminescent fluid instead of dark ink when harassed by predators, blinding and disorienting pursuers in the absolute gloom while the squid darts to safety.\n\n"
                            "Paragraph F\n"
                            "A remarkable subset of marine bioluminescent organisms does not manufacture luciferin autonomously; rather, they form mutualistic symbioses with bioluminescent marine bacteria. The paramount model for this association is the Hawaiian bobtail squid (Euprymna scolopes) and the marine gammaproteobacterium Aliivibrio fischeri. Newly hatched juvenile squid do not inherit the bacteria maternally; instead, they harvest the microscopic symbionts directly from surrounding ambient seawater. Once colonized inside the squid's specialized bilobed light organ, the bacteria multiply. Through a density-dependent biochemical communication process known as quorum sensing, the bacteria synthesize autoinducer signaling molecules. Only when bacterial density reaches a critical threshold does luminescence activate, supplying the nocturnal squid with counter-illumination during nocturnal foraging excursions.\n\n"
                            "Paragraph G\n"
                            "In contemporary scientific research, marine bioluminescence has transcended ecological curiosity to revolutionize molecular medicine and biochemistry. The isolation and recombinant cloning of Green Fluorescent Protein (GFP) from the crystal jellyfish Aequorea victoria by Osamu Shimomura, Martin Chalfie, and Roger Tsien earned the 2008 Nobel Prize in Chemistry. Luciferase-based reporter gene assays now allow oncologists to track real-time tumor progression, metastatic dissemination, and therapeutic response in living mammalian subjects with sub-millimeter precision. Concurrently, environmental engineers employ bioluminescent bacterial biosensors as real-time, highly sensitive detectors for heavy metal contamination and pesticide runoff in estuarine waters.",
                    "questions": [
                        {
                            "id": "R1-Q1",
                            "type": "True/False/Not Given",
                            "question_text": "Luciferase acts as an enzyme that accelerates the oxidation of luciferin without generating substantial thermal energy.",
                            "options": ["TRUE", "FALSE", "NOT GIVEN"],
                            "correct_answer": "TRUE",
                            "explanation": "Paragraph A states that upwards of 90% of the reaction's energy is converted directly into luminous radiance with negligible heat, which is why scientists designate it as 'cold light'."
                        },
                        {
                            "id": "R1-Q2",
                            "type": "True/False/Not Given",
                            "question_text": "Bioluminescent capabilities in marine animals evolved from a single common ancestral organism.",
                            "options": ["TRUE", "FALSE", "NOT GIVEN"],
                            "correct_answer": "FALSE",
                            "explanation": "Paragraph B explicitly states that bioluminescence originated independently through convergent evolution in 'more than thirty distinct phylogenetic lineages', contradicting the single ancestor claim."
                        },
                        {
                            "id": "R1-Q3",
                            "type": "True/False/Not Given",
                            "question_text": "Counter-illumination allows mid-water fish to disguise their silhouettes from predators swimming below them.",
                            "options": ["TRUE", "FALSE", "NOT GIVEN"],
                            "correct_answer": "TRUE",
                            "explanation": "Paragraph C explains that fish adjust ventral photophores to match downwelling surface light, 'effectively rendering their silhouettes transparent to predators lurking in deeper strata'."
                        },
                        {
                            "id": "R1-Q4",
                            "type": "True/False/Not Given",
                            "question_text": "Deep-sea dragonfish emit red light primarily to locate and communicate with potential reproductive mates.",
                            "options": ["TRUE", "FALSE", "NOT GIVEN"],
                            "correct_answer": "FALSE",
                            "explanation": "Paragraph D clarifies that dragonfish use red light as 'private, invisible sniper spotlights to illuminate unaware prey without disclosing their own position', not to signal mates."
                        },
                        {
                            "id": "R1-Q5",
                            "type": "True/False/Not Given",
                            "question_text": "The burglar-alarm hypothesis was verified through laboratory experiments conducted on deep-sea submarines in 1985.",
                            "options": ["TRUE", "FALSE", "NOT GIVEN"],
                            "correct_answer": "NOT GIVEN",
                            "explanation": "Paragraph E explains the mechanics of the burglar-alarm hypothesis, but no mention is made of experiments in 1985 or deep-sea submarines."
                        },
                        {
                            "id": "R1-Q6",
                            "type": "True/False/Not Given",
                            "question_text": "Newly hatched Hawaiian bobtail squid receive their bioluminescent bacteria directly from their mother's light organ.",
                            "options": ["TRUE", "FALSE", "NOT GIVEN"],
                            "correct_answer": "FALSE",
                            "explanation": "Paragraph F explicitly notes that juvenile squid 'do not inherit the bacteria maternally; instead, they harvest the microscopic symbionts directly from surrounding ambient seawater'."
                        },
                        {
                            "id": "R1-Q7",
                            "type": "True/False/Not Given",
                            "question_text": "Luciferase-based assays are currently applied in oncology to observe the development and movement of cancerous tumors.",
                            "options": ["TRUE", "FALSE", "NOT GIVEN"],
                            "correct_answer": "TRUE",
                            "explanation": "Paragraph G states that 'luciferase-based reporter gene assays now allow oncologists to track real-time tumor progression, metastatic dissemination, and therapeutic response'."
                        },
                        {
                            "id": "R1-Q8",
                            "type": "Sentence Completion",
                            "question_text": "Because bioluminescent reactions release very little heat, scientists commonly refer to this light as _______.",
                            "options": [],
                            "correct_answer": "cold light",
                            "explanation": "Paragraph A states: 'physicists and marine biologists frequently designate the phenomenon as \"cold light\"'."
                        },
                        {
                            "id": "R1-Q9",
                            "type": "Sentence Completion",
                            "question_text": "Fish in the mesopelagic zone calibrate their photophores to blend in with _______ coming from above.",
                            "options": [],
                            "correct_answer": "downwelling sunlight",
                            "explanation": "Paragraph C mentions matching 'the downwelling sunlight when viewed from below'."
                        },
                        {
                            "id": "R1-Q10",
                            "type": "Sentence Completion",
                            "question_text": "The modified dorsal fin ray that acts as a luminous lure on anglerfish is called an _______.",
                            "options": [],
                            "correct_answer": "esca",
                            "explanation": "Paragraph D states: 'females possess an esca—a modified dorsal fin ray that dangles directly before their expansive jaws'."
                        },
                        {
                            "id": "R1-Q11",
                            "type": "Sentence Completion",
                            "question_text": "When under attack, the squid Heteroteuthis dispar releases a cloud of _______ instead of ordinary black ink.",
                            "options": [],
                            "correct_answer": "luminescent fluid",
                            "explanation": "Paragraph E: 'eject an iridescent cloud of luminescent fluid instead of dark ink'."
                        },
                        {
                            "id": "R1-Q12",
                            "type": "Sentence Completion",
                            "question_text": "Symbiotic bacteria within the bobtail squid initiate luminescence only after reaching a threshold via _______.",
                            "options": [],
                            "correct_answer": "quorum sensing",
                            "explanation": "Paragraph F: 'Through a density-dependent biochemical communication process known as quorum sensing'."
                        },
                        {
                            "id": "R1-Q13",
                            "type": "Sentence Completion",
                            "question_text": "In molecular biology, Green Fluorescent Protein isolated from jellyfish is widely utilized as a biological _______.",
                            "options": [],
                            "correct_answer": "reporter",
                            "explanation": "Paragraph G references luciferase-based and fluorescent protein 'reporter' assays and markers for cellular tagging."
                        }
                    ]
                },

                # -----------------------------------------------------
                # PASSAGE 2: QUESTIONS 14 - 26 (~900 words)
                # -----------------------------------------------------
                {
                    "passage_num": 2,
                    "title": "Vertical Forests and the Resilient Megastructures of Future Cities",
                    "text": "Paragraph A\n"
                            "Across the globe, the accelerating pace of urban densification presents an acute environmental dilemma. Metropolitan expanses currently account for over seventy percent of global carbon emissions while consuming an equivalent proportion of terrestrial energy resources. Compounding this challenge, the extensive deployment of impermeable tarmac, asphalt, and structural concrete has exacerbated the urban heat island effect, driving inner-city temperatures up to six degrees Celsius higher than surrounding rural peripheries. As traditional horizontal space for urban parks evaporates under intense real estate pressure, architects and environmental engineers are compelled to rethink the fundamental geometry of municipal biophilic integration, giving rise to the concept of vertical forestry.\n\n"
                            "Paragraph B\n"
                            "The seminal manifestation of this architectural philosophy emerged in 2014 with the inauguration of the Bosco Verticale (Vertical Forest) in Milan, designed by Italian architect Stefano Boeri. Comprising two residential towers standing 111 and 76 meters tall, the complex accommodates over eight hundred mature trees, fifteen thousand perennial plants, and five thousand shrubs distributed across expansive perimeter cantilevered balconies. Together, this arboreal envelope equals approximately twenty thousand square meters of conventional horizontal woodland. Annually, the living façade absorbs approximately thirty metric tons of atmospheric carbon dioxide, captures airborne particulate matter (PM10), and produces over nineteen thousand kilograms of oxygen while providing critical acoustic insulation for residents.\n\n"
                            "Paragraph C\n"
                            "Constructing a vertical forest requires overcoming formidable mechanical and biological engineering hurdles that do not exist in conventional civil construction. Mature trees subjected to high-altitude wind shear experience immense lateral rotational forces. To prevent catastrophic failure during severe storms, structural engineers anchor root systems within specialized steel cages affixed directly to reinforced concrete floor slabs. Furthermore, standard garden soil is far too dense, as saturated soil can overload a cantilevered balcony's dead load capacity. Civil horticulturists instead formulate engineered, ultra-lightweight substrates composed of volcanic pumice, expanded clay pellets, and porous lapilli, enriched with slow-release organic polymers that retain water without compacting or decomposing.\n\n"
                            "Paragraph D\n"
                            "Equally sophisticated is the tower's closed-loop hydraulic and micro-irrigation network. Traditional manual hose watering by individual apartment dwellers would be inefficient and hazardous. Instead, vertical forests rely on automated, sensor-driven micro-drip networks. Probes embedded in every plant receptacle monitor soil dielectric permittivity to measure instantaneous volumetric moisture levels, solar exposure, and ambient air temperature. When hydration falls below a calculated threshold, the automated building management system releases greywater reclaimed from residential sinks and showers, filtered through multi-stage reverse-osmosis filtration units, ensuring zero expenditure of municipal potable water for landscaping.\n\n"
                            "Paragraph E\n"
                            "From an ecological perspective, the biological return has exceeded initial projections. Milan's vertical towers have evolved into spontaneous stepping-stone biotopes, establishing aerial corridors that connect isolated urban parks with peripheral river valleys. Entomological and ornithological surveys conducted five years post-occupancy documented over thirty nesting bird species and more than sixteen hundred individual specimens of pollinating insects and butterflies inhabiting the balconies. This faunal recolonization confirms that vertical ecosystems can successfully function as authentic biological refugia rather than mere aesthetic veneers.\n\n"
                            "Paragraph F\n"
                            "Nevertheless, the model has attracted intense scrutiny from urban planning economists who question its economic viability and social accessibility. Critics point out that maintaining high-rise vegetation demands specialist teams of arborists—dubbed 'flying gardeners'—who rappel down the building's exterior several times a year to prune, inspect health, and replace diseased foliage. These specialized logistical operations impose exorbitant monthly service charges, rendering early vertical towers exclusive enclaves for the ultra-wealthy. In Milan, residential units commanded prices exceeding nine thousand euros per square meter, sparking accusations of ecological gentrification.\n\n"
                            "Paragraph G\n"
                            "In response to equity concerns, contemporary developments are actively democratizing the typology. In Eindhoven, Netherlands, Boeri completed the Trudo Vertical Forest—the world's first living high-rise dedicated exclusively to social rental housing for low-income and young residents. By standardizing prefabricated concrete planters, adopting automated robotic maintenance cranes, and selecting robust indigenous flora requiring minimal intervention, construction and operational costs were reduced by sixty percent. Meanwhile, municipal authorities in Singapore and Tokyo have introduced statutory regulations mandating that high-density developments replace one hundred percent of the site's footprint with integrated greenery, cementing vertical forestry as an essential instrument of climate-resilient urbanism.",
                    "questions": [
                        {
                            "id": "R1-Q14",
                            "type": "Matching Headings",
                            "question_text": "Which heading best summarizes Paragraph A?",
                            "options": [
                                "i. Prohibitive maintenance costs and exclusive gentrification",
                                "ii. Engineering challenges of wind shear and structural substrate",
                                "iii. The environmental and spatial crises necessitating vertical ecology",
                                "iv. Democratizing green high-rises through social housing",
                                "v. Closed-loop greywater recycling and irrigation sensors",
                                "vi. Biological recolonization by avian and pollinating species",
                                "vii. The architectural prototype that proved biological viability"
                            ],
                            "correct_answer": "iii. The environmental and spatial crises necessitating vertical ecology",
                            "explanation": "Paragraph A discusses urban densification, carbon emissions, the heat island effect, and why architects must rethink geometry."
                        },
                        {
                            "id": "R1-Q15",
                            "type": "Matching Headings",
                            "question_text": "Which heading best summarizes Paragraph B?",
                            "options": [
                                "i. Prohibitive maintenance costs and exclusive gentrification",
                                "ii. Engineering challenges of wind shear and structural substrate",
                                "iii. The environmental and spatial crises necessitating vertical ecology",
                                "iv. Democratizing green high-rises through social housing",
                                "v. Closed-loop greywater recycling and irrigation sensors",
                                "vi. Biological recolonization by avian and pollinating species",
                                "vii. The architectural prototype that proved biological viability"
                            ],
                            "correct_answer": "vii. The architectural prototype that proved biological viability",
                            "explanation": "Paragraph B describes the groundbreaking Bosco Verticale in Milan, detailing its dimensions, plant counts, and carbon absorption."
                        },
                        {
                            "id": "R1-Q16",
                            "type": "Matching Headings",
                            "question_text": "Which heading best summarizes Paragraph C?",
                            "options": [
                                "i. Prohibitive maintenance costs and exclusive gentrification",
                                "ii. Engineering challenges of wind shear and structural substrate",
                                "iii. The environmental and spatial crises necessitating vertical ecology",
                                "iv. Democratizing green high-rises through social housing",
                                "v. Closed-loop greywater recycling and irrigation sensors",
                                "vi. Biological recolonization by avian and pollinating species",
                                "vii. The architectural prototype that proved biological viability"
                            ],
                            "correct_answer": "ii. Engineering challenges of wind shear and structural substrate",
                            "explanation": "Paragraph C details the mechanical problems of wind shear, steel cage anchors, and lightweight volcanic pumice substrates."
                        },
                        {
                            "id": "R1-Q17",
                            "type": "Matching Headings",
                            "question_text": "Which heading best summarizes Paragraph D?",
                            "options": [
                                "i. Prohibitive maintenance costs and exclusive gentrification",
                                "ii. Engineering challenges of wind shear and structural substrate",
                                "iii. The environmental and spatial crises necessitating vertical ecology",
                                "iv. Democratizing green high-rises through social housing",
                                "v. Closed-loop greywater recycling and irrigation sensors",
                                "vi. Biological recolonization by avian and pollinating species",
                                "vii. The architectural prototype that proved biological viability"
                            ],
                            "correct_answer": "v. Closed-loop greywater recycling and irrigation sensors",
                            "explanation": "Paragraph D explains automated moisture probes, greywater filtration from showers, and precision micro-drip networks."
                        },
                        {
                            "id": "R1-Q18",
                            "type": "Matching Headings",
                            "question_text": "Which heading best summarizes Paragraph E?",
                            "options": [
                                "i. Prohibitive maintenance costs and exclusive gentrification",
                                "ii. Engineering challenges of wind shear and structural substrate",
                                "iii. The environmental and spatial crises necessitating vertical ecology",
                                "iv. Democratizing green high-rises through social housing",
                                "v. Closed-loop greywater recycling and irrigation sensors",
                                "vi. Biological recolonization by avian and pollinating species",
                                "vii. The architectural prototype that proved biological viability"
                            ],
                            "correct_answer": "vi. Biological recolonization by avian and pollinating species",
                            "explanation": "Paragraph E focuses on ecological return: over 30 nesting bird species, butterflies, and stepping-stone biological corridors."
                        },
                        {
                            "id": "R1-Q19",
                            "type": "Matching Headings",
                            "question_text": "Which heading best summarizes Paragraph F?",
                            "options": [
                                "i. Prohibitive maintenance costs and exclusive gentrification",
                                "ii. Engineering challenges of wind shear and structural substrate",
                                "iii. The environmental and spatial crises necessitating vertical ecology",
                                "iv. Democratizing green high-rises through social housing",
                                "v. Closed-loop greywater recycling and irrigation sensors",
                                "vi. Biological recolonization by avian and pollinating species",
                                "vii. The architectural prototype that proved biological viability"
                            ],
                            "correct_answer": "i. Prohibitive maintenance costs and exclusive gentrification",
                            "explanation": "Paragraph F addresses economic criticisms, rappelling 'flying gardeners', expensive maintenance fees, and luxury exclusivity."
                        },
                        {
                            "id": "R1-Q20",
                            "type": "Multiple Choice",
                            "question_text": "Why do vertical forest engineers avoid using conventional garden loam in balcony planters?",
                            "options": [
                                "It lacks necessary nitrogen minerals for mature trees",
                                "It is too heavy when saturated and risks exceeding structural weight limits",
                                "It attracts predatory insect pests that damage facade windows",
                                "It accelerates the thermal expansion of concrete floor slabs"
                            ],
                            "correct_answer": "It is too heavy when saturated and risks exceeding structural weight limits",
                            "explanation": "Paragraph C notes that 'standard garden soil is far too dense, as saturated soil can overload a cantilevered balcony's dead load capacity'."
                        },
                        {
                            "id": "R1-Q21",
                            "type": "Multiple Choice",
                            "question_text": "How do automated irrigation systems in vertical forests conserve municipal water?",
                            "options": [
                                "By restricting watering to five minutes per week",
                                "By recycling filtered residential greywater from sinks and showers",
                                "By pumping deep subterranean groundwater directly to each floor",
                                "By relying solely on natural seasonal rainfall collection"
                            ],
                            "correct_answer": "By recycling filtered residential greywater from sinks and showers",
                            "explanation": "Paragraph D explains that greywater reclaimed from residential sinks and showers is filtered and distributed, ensuring zero potable municipal water is wasted."
                        },
                        {
                            "id": "R1-Q22",
                            "type": "Multiple Choice",
                            "question_text": "What distinguishing breakthrough was achieved by the Trudo Tower in Eindhoven?",
                            "options": [
                                "It eliminated the need for plant roots to touch water",
                                "It applied vertical forest architecture to low-income social rental housing",
                                "It was constructed completely out of recycled maritime containers",
                                "It was built entirely without the supervision of certified architects"
                            ],
                            "correct_answer": "It applied vertical forest architecture to low-income social rental housing",
                            "explanation": "Paragraph G states: 'In Eindhoven, Netherlands, Boeri completed the Trudo Vertical Forest—the world's first living high-rise dedicated exclusively to social rental housing'."
                        },
                        {
                            "id": "R1-Q23",
                            "type": "Matching Features",
                            "question_text": "Match the project/city: Proved the foundational structural and biological concept in 2014.",
                            "options": ["Milan (Bosco Verticale)", "Eindhoven (Trudo Tower)", "Singapore", "Tokyo"],
                            "correct_answer": "Milan (Bosco Verticale)",
                            "explanation": "Paragraph B introduces Milan's Bosco Verticale as the seminal manifestation in 2014."
                        },
                        {
                            "id": "R1-Q24",
                            "type": "Matching Features",
                            "question_text": "Match the project/city: Drastically reduced costs via prefabricated concrete planters for social housing.",
                            "options": ["Milan (Bosco Verticale)", "Eindhoven (Trudo Tower)", "Singapore", "Tokyo"],
                            "correct_answer": "Eindhoven (Trudo Tower)",
                            "explanation": "Paragraph G attributes prefabrication cost reductions specifically to the Trudo Tower in Eindhoven."
                        },
                        {
                            "id": "R1-Q25",
                            "type": "Matching Features",
                            "question_text": "Match the project/city: Enacted municipal codes mandating developments replace 100% of site footprint with greenery.",
                            "options": ["Milan (Bosco Verticale)", "Eindhoven (Trudo Tower)", "Singapore", "Tokyo"],
                            "correct_answer": "Singapore",
                            "explanation": "Paragraph G explicitly highlights municipal regulations in Singapore mandating complete footprint replacement."
                        },
                        {
                            "id": "R1-Q26",
                            "type": "Sentence Completion",
                            "question_text": "Specialized high-rise arborists who rappel down the building façade to inspect trees are nicknamed _______.",
                            "options": [],
                            "correct_answer": "flying gardeners",
                            "explanation": "Paragraph F references arborist teams 'dubbed \"flying gardeners\"'."
                        }
                    ]
                },

                # -----------------------------------------------------
                # PASSAGE 3: QUESTIONS 27 - 40 (~950 words)
                # -----------------------------------------------------
                {
                    "passage_num": 3,
                    "title": "Neuroplasticity, Cognitive Reserve, and the Bilingual Mind Across the Lifespan",
                    "text": "Paragraph A\n"
                            "Throughout the early to mid-twentieth century, mainstream pedagogical doctrine in Western societies viewed early childhood bilingualism with deep skepticism. Educational psychologists cautioned that exposing infants to multiple linguistic systems would induce severe cognitive confusion, retard syntactic mastery, and diminish overall vocabulary breadth. This early consensus was grounded in a primitive 'switchboard' paradigm of cognition, which assumed that the human brain possessed a finite mental storage capacity, and that housing two distinct lexicons would inevitably overburden memory and executive processing faculties.\n\n"
                            "Paragraph B\n"
                            "In the late 1980s, this dogma underwent a revolutionary paradigm shift, spearheaded by cognitive psychologist Ellen Bialystok and colleagues. Employing rigorous computerized psychometric tests, researchers observed that bilingual individuals consistently outperformed monolinguals on non-verbal executive function batteries, including the Stroop task and the Simon flanker task. These protocols assess cognitive control: the ability to focus selective attention on goal-relevant stimuli while actively suppressing distracting or conflicting peripheral cues. The finding was startling because the experimental tasks contained no linguistic components whatsoever, indicating that bilingual language management permanently reconfigures domain-general neural circuitry.\n\n"
                            "Paragraph C\n"
                            "The underlying neurobiological explanation lies in the perpetual, simultaneous activation of both language systems. Eye-tracking and functional neuroimaging investigations have demonstrated that a bilingual individual never completely deactivates their secondary language. Even when immersed in an exclusively monolingual setting, candidate lexical items from both languages compete for expression within milliseconds of hearing a phoneme. Consequently, to produce an intended utterance in one language, the brain must continuously mobilize the prefrontal cortex, the anterior cingulate cortex, and the basal ganglia to inhibit intrusive competitors from the other tongue. This incessant mental workout acts as cognitive resistance training, fortifying fronto-striatal executive control loops over a lifetime.\n\n"
                            "Paragraph D\n"
                            "Structural MRI neuroimaging has verified that these functional demands induce observable morphological neuroplastic adaptations. Compared to age-matched monolinguals, lifelong bilinguals exhibit increased grey matter density in the left inferior parietal cortex—a region vital for lexical acquisition—along with enhanced white matter fractional anisotropy across the corpus callosum and superior longitudinal fasciculus. This enhanced white matter integrity signifies more robust myelin insulation around axonal projections, facilitating faster interhemispheric communication and superior structural resistance to age-related axonal atrophy.\n\n"
                            "Paragraph E\n"
                            "Perhaps the most profound real-world implication of this neurological reconfiguration concerns cognitive reserve and neurodegenerative disease. In a series of landmark epidemiological studies conducted across memory clinics in Canada and India, Bialystok, Craik, and Freedman uncovered that lifelong bilingual patients were diagnosed with symptomatic Alzheimer's disease on average four to five years later than comparable monolingual cohorts. Astoundingly, when researchers analyzed computed tomography (CT) scans matching bilinguals and monolinguals exhibiting identical degrees of clinical cognitive impairment, the bilingual patients exhibited dramatically greater brain atrophy, neuronal death, and ventricular enlargement. This paradox reveals that bilingualism does not prevent Alzheimer's pathology from developing; rather, it equips the brain with compensatory neural networks that sustain functional competence despite extensive physical neurodegeneration.\n\n"
                            "Paragraph F\n"
                            "Despite these compelling clinical findings, the concept of a generalized 'bilingual advantage' has ignited fierce controversy within contemporary cognitive psychology. Critics led by Kenneth Paap argue that positive executive function effects reported in early studies were exaggerated by publication bias and small sample sizes. Large-scale replication studies conducted on young adult university undergraduates frequently report negligible differences between bilinguals and monolinguals. Proponents counter that young adults represent the biological zenith of human cognitive development—a demographic ceiling effect where neurocognitive performance is already optimal, masking subtle compensatory advantages that only become conspicuous during senescence or under high cognitive load.\n\n"
                            "Paragraph G\n"
                            "To reconcile these divergent findings, David Green and Jubin Abutalebi formulated the Adaptive Control Hypothesis. This framework posited that the cognitive consequences of bilingualism are not monolithic, but are dynamically shaped by specific interactional contexts. In 'dual-language' environments, where speakers interact with interlocutors who speak only one language and must frequently alternate between distinct social groups, demands on proactive goal maintenance and selective inhibition are maximal. Conversely, in 'dense code-switching' communities, where speakers fluidly interweave two languages within the same sentence with fellow bilinguals, opportunistic lexical access replaces rigid inhibition. Thus, the specific architecture of daily conversation dictates which executive networks are reinforced.\n\n"
                            "Paragraph H\n"
                            "Ultimately, the trajectory of bilingual neuroplasticity offers profound lessons for public health and educational strategy. Far from inducing cognitive handicap, navigating multilingual realities constructs an enduring biological bulwark against mental senescence. As populations worldwide face surging rates of neurodegenerative disease, the promotion of second-language immersion programs—both in early childhood classrooms and among retirees—represents an accessible, non-pharmacological public health intervention capable of delaying clinical dementia and preserving intellectual autonomy.",
                    "questions": [
                        {
                            "id": "R1-Q27",
                            "type": "Yes/No/Not Given",
                            "question_text": "Early twentieth-century educational experts believed that teaching two languages to young children enhanced general intelligence.",
                            "options": ["YES", "NO", "NOT GIVEN"],
                            "correct_answer": "NO",
                            "explanation": "Paragraph A states that experts viewed early bilingualism with deep skepticism, warning it would induce confusion and retard vocabulary breadth."
                        },
                        {
                            "id": "R1-Q28",
                            "type": "Yes/No/Not Given",
                            "question_text": "Bilingual speakers completely deactivate their dormant language when conversing in a strictly monolingual environment.",
                            "options": ["YES", "NO", "NOT GIVEN"],
                            "correct_answer": "NO",
                            "explanation": "Paragraph C clearly states: 'a bilingual individual never completely deactivates their secondary language. Even when immersed in an exclusively monolingual setting, candidate lexical items from both languages compete'."
                        },
                        {
                            "id": "R1-Q29",
                            "type": "Yes/No/Not Given",
                            "question_text": "Lifelong bilingualism strengthens the myelin insulation around axonal nerve pathways between brain hemispheres.",
                            "options": ["YES", "NO", "NOT GIVEN"],
                            "correct_answer": "YES",
                            "explanation": "Paragraph D states: 'enhanced white matter integrity signifies more robust myelin insulation around axonal projections, facilitating faster interhemispheric communication'."
                        },
                        {
                            "id": "R1-Q30",
                            "type": "Yes/No/Not Given",
                            "question_text": "Lifelong bilingualism prevents the biological accumulation of amyloid plaques in the brains of elderly patients.",
                            "options": ["YES", "NO", "NOT GIVEN"],
                            "correct_answer": "NO",
                            "explanation": "Paragraph E explicitly states: 'bilingualism does not prevent Alzheimer's pathology from developing; rather, it equips the brain with compensatory neural networks that sustain functional competence'."
                        },
                        {
                            "id": "R1-Q31",
                            "type": "Yes/No/Not Given",
                            "question_text": "Kenneth Paap and his team concluded that adult second-language learning has no impact on memory.",
                            "options": ["YES", "NO", "NOT GIVEN"],
                            "correct_answer": "NOT GIVEN",
                            "explanation": "Paragraph F discusses Paap's criticism of executive function advantages in young university undergraduates, but does not state his views on adult second-language memory."
                        },
                        {
                            "id": "R1-Q32",
                            "type": "Yes/No/Not Given",
                            "question_text": "The specific conversational context in which bilinguals communicate influences which brain networks are strengthened.",
                            "options": ["YES", "NO", "NOT GIVEN"],
                            "correct_answer": "YES",
                            "explanation": "Paragraph G confirms: 'the specific architecture of daily conversation dictates which executive networks are reinforced'."
                        },
                        {
                            "id": "R1-Q33",
                            "type": "Summary Completion",
                            "question_text": "Bilingual Alzheimer's patients showed symptomatic onset four to five years _______ than monolingual peers.",
                            "options": ["later", "earlier", "faster", "suddenly"],
                            "correct_answer": "later",
                            "explanation": "Paragraph E states that bilingual patients were diagnosed with symptomatic Alzheimer's on average four to five years later."
                        },
                        {
                            "id": "R1-Q34",
                            "type": "Summary Completion",
                            "question_text": "CT scans showed that bilingual patients with equal cognitive function actually had _______ brain atrophy than monolinguals.",
                            "options": ["greater", "less", "identical", "negligible"],
                            "correct_answer": "greater",
                            "explanation": "Paragraph E states that bilingual patients exhibited 'dramatically greater brain atrophy, neuronal death, and ventricular enlargement'."
                        },
                        {
                            "id": "R1-Q35",
                            "type": "Summary Completion",
                            "question_text": "Bilingualism equips the cerebrum with alternative _______ networks that compensate for physical damage.",
                            "options": ["compensatory neural", "chemical", "sensory", "muscular"],
                            "correct_answer": "compensatory neural",
                            "explanation": "Paragraph E: 'equips the brain with compensatory neural networks that sustain functional competence'."
                        },
                        {
                            "id": "R1-Q36",
                            "type": "Summary Completion",
                            "question_text": "The absence of detectable bilingual advantages in young university students is attributed to a demographic _______.",
                            "options": ["ceiling effect", "floor effect", "bias error", "linguistic gap"],
                            "correct_answer": "ceiling effect",
                            "explanation": "Paragraph F: 'a demographic ceiling effect where neurocognitive performance is already optimal'."
                        },
                        {
                            "id": "R1-Q37",
                            "type": "Multiple Choice",
                            "question_text": "What do tests like the Stroop and Simon flanker evaluate in cognitive experiments?",
                            "options": [
                                "The speed of reciting foreign phonetic alphabets",
                                "The ability to attend to target stimuli while suppressing conflicting distractors",
                                "The maximum number of vocabulary words memorized in childhood",
                                "The auditory acuity of speech recognition in noisy environments"
                            ],
                            "correct_answer": "The ability to attend to target stimuli while suppressing conflicting distractors",
                            "explanation": "Paragraph B explains that these tasks assess cognitive control: 'the ability to focus selective attention on goal-relevant stimuli while actively suppressing distracting or conflicting peripheral cues'."
                        },
                        {
                            "id": "R1-Q38",
                            "type": "Multiple Choice",
                            "question_text": "According to the Adaptive Control Hypothesis in Paragraph G, which communication environment demands the highest deliberate inhibitory effort?",
                            "options": [
                                "Dense code-switching communities where two languages are casually mixed",
                                "Dual-language contexts where speakers must alternate between monolingual groups",
                                "Classrooms where only ancient dead languages are read silently",
                                "Monolingual households with access to foreign radio broadcasts"
                            ],
                            "correct_answer": "Dual-language contexts where speakers must alternate between monolingual groups",
                            "explanation": "Paragraph G states that in dual-language environments where speakers interact with distinct monolingual individuals, 'demands on proactive goal maintenance and selective inhibition are maximal'."
                        },
                        {
                            "id": "R1-Q39",
                            "type": "Multiple Choice",
                            "question_text": "What is the author's viewpoint regarding second-language learning for older adults?",
                            "options": [
                                "It should be avoided because adult neuroplasticity is completely nonexistent",
                                "It represents an accessible non-pharmacological strategy to preserve cognitive autonomy",
                                "It causes excessive psychological stress that accelerates neurodegeneration",
                                "It is beneficial only if the individual achieved native fluency in childhood"
                            ],
                            "correct_answer": "It represents an accessible non-pharmacological strategy to preserve cognitive autonomy",
                            "explanation": "Paragraph H advocates second-language immersion for retirees as an 'accessible, non-pharmacological public health intervention capable of delaying clinical dementia and preserving intellectual autonomy'."
                        },
                        {
                            "id": "R1-Q40",
                            "type": "Multiple Choice",
                            "question_text": "Which statement best expresses the overarching thesis of the passage?",
                            "options": [
                                "Multilingualism is primarily an economic advantage without biological significance",
                                "Managing two languages induces lifelong neurostructural modifications that build cognitive reserve",
                                "Monolinguals consistently outperform bilinguals in abstract mathematical reasoning",
                                "Childhood bilingualism should be strictly limited to prevent early linguistic delays"
                            ],
                            "correct_answer": "Managing two languages induces lifelong neurostructural modifications that build cognitive reserve",
                            "explanation": "The entire passage chronicles how bilingual lexical competition induces neuroplasticity, white matter reinforcement, and cognitive reserve that delays dementia symptoms."
                        }
                    ]
                }
            ]
        }
    },

    # -----------------------------------------------------------------
    # LISTENING TEST 1: FULL 40 QUESTIONS ACROSS 4 SECTIONS
    # -----------------------------------------------------------------
    {
        "id": "L-01",
        "module": "listening",
        "title": "IELTS Official Listening Practice Test 1 (Full 40 Questions / 4 Sections)",
        "type": "Academic",
        "duration_minutes": 30,
        "difficulty": "Authentic IELTS Standard",
        "content": {
            "sections": [
                # Section 1: Questions 1 - 10
                {
                    "section_num": 1,
                    "title": "Section 1: Community Sports Center Membership Inquiry",
                    "context": "A conversation between a customer, Mark Henderson, and a receptionist at the Riverdale Sports Center.",
                    "audio_script": "Receptionist: Good morning, Riverdale Sports Center. How can I help you today?\n"
                                    "Mark: Hello! I'm interested in joining your fitness club and wanted to find out about membership options.\n"
                                    "Receptionist: Certainly! Let me take down your details first. Could I have your surname and first name?\n"
                                    "Mark: Yes, my surname is Henderson, H-E-N-D-E-R-S-O-N, and my first name is Mark.\n"
                                    "Receptionist: Thank you, Mark. And what is your current address in Oxford?\n"
                                    "Mark: 42 Windmill Road.\n"
                                    "Receptionist: 42 Windmill Road, got it. And a contact telephone number, please?\n"
                                    "Mark: It's 07700 900342.\n"
                                    "Receptionist: Great. And your occupation for our records?\n"
                                    "Mark: I work as an accountant at a local firm.\n"
                                    "Receptionist: Perfect. Now regarding packages: our standard Silver package is £35 per month, which gives access to the gym during off-peak hours only. Our most comprehensive option is the Gold package, priced at £52 per month with unlimited peak access and swimming pool inclusion.\n"
                                    "Mark: Oh, I definitely want to swim regularly, so Gold sounds ideal. Does that include personal training sessions?\n"
                                    "Receptionist: It comes with an initial fitness assessment and two complimentary training sessions. After that, any additional personal sessions cost £20 each.\n"
                                    "Mark: That sounds fair. Are locker facilities included or extra?\n"
                                    "Receptionist: Lockers require a refundable deposit of £10 for the electronic key fob.\n"
                                    "Mark: Fine. And what are your opening hours on weekends?\n"
                                    "Receptionist: On Saturdays and Sundays we open at 7:00 am and close at 8:00 pm.\n"
                                    "Mark: And when can I begin? Can I attend induction this week?\n"
                                    "Receptionist: Our mandatory safety induction is on Thursday evening at 6:00 pm. Once you finish that thirty-minute session, your digital membership card becomes active immediately.\n"
                                    "Mark: Excellent, please book me in for Thursday at 6:00 pm.",
                    "questions": [
                        {"id": "L1-Q1", "type": "Form Completion", "question_text": "Customer Surname: Henderson. First Name: _______", "options": [], "correct_answer": "Mark", "explanation": "The caller clearly gives his first name as Mark."},
                        {"id": "L1-Q2", "type": "Form Completion", "question_text": "Address: 42 _______ Road, Oxford", "options": [], "correct_answer": "Windmill", "explanation": "Mark specifies his address as 42 Windmill Road."},
                        {"id": "L1-Q3", "type": "Form Completion", "question_text": "Contact Phone: 07700 _______", "options": [], "correct_answer": "900342", "explanation": "The phone number is given as 07700 900342."},
                        {"id": "L1-Q4", "type": "Form Completion", "question_text": "Occupation: _______", "options": [], "correct_answer": "accountant", "explanation": "Mark confirms: 'I work as an accountant'."},
                        {"id": "L1-Q5", "type": "Multiple Choice", "question_text": "How much is the monthly fee for the Gold Membership package?", "options": ["£35", "£42", "£52", "£60"], "correct_answer": "£52", "explanation": "Receptionist states Gold package is £52 per month."},
                        {"id": "L1-Q6", "type": "Form Completion", "question_text": "Number of free personal training sessions included: _______", "options": [], "correct_answer": "2", "explanation": "The receptionist explains it includes two complimentary training sessions."},
                        {"id": "L1-Q7", "type": "Form Completion", "question_text": "Cost of additional personal training session: £_______", "options": [], "correct_answer": "20", "explanation": "Additional sessions cost £20 each."},
                        {"id": "L1-Q8", "type": "Form Completion", "question_text": "Locker key refundable deposit: £_______", "options": [], "correct_answer": "10", "explanation": "Requires a refundable deposit of £10."},
                        {"id": "L1-Q9", "type": "Form Completion", "question_text": "Weekend closing time: _______ pm", "options": [], "correct_answer": "8:00", "explanation": "Receptionist states weekend hours close at 8:00 pm."},
                        {"id": "L1-Q10", "type": "Form Completion", "question_text": "Mandatory safety induction day: _______ at 6:00 pm", "options": [], "correct_answer": "Thursday", "explanation": "The induction is scheduled for Thursday evening."}
                    ]
                },
                # Section 2: Questions 11 - 20
                {
                    "section_num": 2,
                    "title": "Section 2: Orientation Tour of the Wellington Botanical Arboretum",
                    "context": "A guided orientation monologue introducing visitors to the layout, rules, and facilities of the historical botanical arboretum.",
                    "audio_script": "Guide: Good morning everyone, and welcome to the Wellington Botanical Arboretum. Before we start our walking tour, let me give you a quick briefing on our history and layout.\n"
                                    "The arboretum was established in 1848 by the naturalist Sir Arthur Wellington, initially spanning just five acres, but today covering over sixty acres of curated flora.\n"
                                    "Directly to your left as you step out of the North Welcome Pavilion is our famous Tropical Rainforest Glasshouse. It is kept at a constant twenty-eight degrees Celsius with ninety percent humidity, housing specimens from the Amazon Basin.\n"
                                    "Straight ahead across the central lawn is the Victorian Herbarium, which contains dried plant records dating back to 1790. Adjacent to the herbarium, on its eastern side, you will find the Alpine Rockery, which mimics high-altitude mountain ecosystems.\n"
                                    "If you are looking for lunch or hot drinks, the Palm Tree Café is situated immediately behind the Rose Garden, overlooking the ornamental koi lake.\n"
                                    "Regarding photography: personal photography with hand-held cameras and smartphones is warmly permitted throughout all outdoor paths. However, tripods and commercial flash equipment are strictly prohibited inside the butterfly sanctuary to protect the delicate insects.\n"
                                    "For visitors with mobility requirements, electric mobility scooters can be borrowed free of charge from the visitor information desk upon presenting identification.\n"
                                    "Please be aware that our historic glasshouses close half an hour before the outer perimeter gates. The glasshouses close at 5:30 pm, while the main perimeter gates are locked at 6:00 pm prompt.",
                    "questions": [
                        {"id": "L1-Q11", "type": "Multiple Choice", "question_text": "In what year was the Wellington Arboretum founded?", "options": ["1820", "1848", "1890", "1905"], "correct_answer": "1848", "explanation": "The guide states: 'established in 1848 by the naturalist Sir Arthur Wellington'."},
                        {"id": "L1-Q12", "type": "Multiple Choice", "question_text": "What is the current total area of the arboretum?", "options": ["5 acres", "25 acres", "45 acres", "60 acres"], "correct_answer": "60 acres", "explanation": "The guide explains it expanded from 5 acres to 'over sixty acres'."},
                        {"id": "L1-Q13", "type": "Multiple Choice", "question_text": "What is the maintained temperature inside the Tropical Rainforest Glasshouse?", "options": ["22°C", "25°C", "28°C", "32°C"], "correct_answer": "28°C", "explanation": "Kept at a constant 28 degrees Celsius."},
                        {"id": "L1-Q14", "type": "Multiple Choice", "question_text": "Where is the Alpine Rockery situated relative to the Victorian Herbarium?", "options": ["On its eastern side", "Directly behind it", "Inside the main entrance", "Across the outer lake"], "correct_answer": "On its eastern side", "explanation": "Guide states: 'Adjacent to the herbarium, on its eastern side, you will find the Alpine Rockery'."},
                        {"id": "L1-Q15", "type": "Multiple Choice", "question_text": "Where is the Palm Tree Café located?", "options": ["Next to North Arch", "Behind the Rose Garden", "Inside the Victorian Herbarium", "At the bus terminus"], "correct_answer": "Behind the Rose Garden", "explanation": "Guide states: 'the Palm Tree Café is situated immediately behind the Rose Garden'."},
                        {"id": "L1-Q16", "type": "Multiple Choice", "question_text": "What is strictly prohibited inside the butterfly sanctuary?", "options": ["All mobile phones", "Food and beverages", "Tripods and commercial flash", "Children under five"], "correct_answer": "Tripods and commercial flash", "explanation": "Guide states: 'tripods and commercial flash equipment are strictly prohibited inside the butterfly sanctuary'."},
                        {"id": "L1-Q17", "type": "Form Completion", "question_text": "Electric mobility scooters can be borrowed free of charge from the _______ desk.", "options": [], "correct_answer": "visitor information", "explanation": "Available from the 'visitor information desk'."},
                        {"id": "L1-Q18", "type": "Form Completion", "question_text": "Historic glasshouses close promptly at _______ pm.", "options": [], "correct_answer": "5:30", "explanation": "Glasshouses close at 5:30 pm."},
                        {"id": "L1-Q19", "type": "Form Completion", "question_text": "Outer perimeter gates are locked at _______ pm.", "options": [], "correct_answer": "6:00", "explanation": "Main gates are locked at 6:00 pm."},
                        {"id": "L1-Q20", "type": "Multiple Choice", "question_text": "What form of document is required to borrow a mobility scooter?", "options": ["Passport only", "Credit card", "Identification", "Medical certificate"], "correct_answer": "Identification", "explanation": "Guide states: 'upon presenting identification'."}
                    ]
                },
                # Section 3: Questions 21 - 30
                {
                    "section_num": 3,
                    "title": "Section 3: Academic Tutorial on Coastal Microplastic Sampling",
                    "context": "Two undergraduate environmental science students, Chloe and Liam, consult their faculty advisor, Dr. Adams, on their field research methodology.",
                    "audio_script": "Dr. Adams: Come in, Chloe, Liam. I've read through your preliminary draft for the estuarine microplastic density project. Overall, the hypothesis is solid, but your sampling methodology requires refinement.\n"
                                    "Liam: Thanks Dr. Adams. We were initially planning to take sediment cores from three beach sites along the Severn Estuary.\n"
                                    "Dr. Adams: In statistical terms, three sample sites will leave your results vulnerable to localized anomalies, such as tidal currents or proximity to storm drains. I strongly urge you to expand to a minimum of six distinct locations across both low and high-water marks.\n"
                                    "Chloe: That makes sense. And what about depth? We thought ten centimeters was standard.\n"
                                    "Dr. Adams: For littoral sediments, the active bioturbation layer is primarily within the top five centimeters. Digging down ten centimeters will dilute recent anthropogenic deposition with older pristine sand.\n"
                                    "Liam: Got it, five centimeters depth. Now regarding extraction: we planned to use standard cellulose coffee filters as suggested in a popular student blog.\n"
                                    "Dr. Adams: That's a classic rookie mistake! When you digest organic sediment matter using thirty percent hydrogen peroxide, cellulose filter paper degrades rapidly, contaminating your sample with cellulose fibers. You must use 0.45-micron glass fiber filters for valid reproducibility.\n"
                                    "Chloe: Understood, glass fiber filters. What about density separation solution?\n"
                                    "Dr. Adams: Saturated sodium chloride is inexpensive, but its density of 1.2 grams per cubic centimeter fails to float denser polymers like polyethylene terephthalate or polyvinyl chloride. Use zinc chloride solution instead, which achieves a density of 1.6 to 1.7 grams per cubic centimeter.\n"
                                    "Liam: That will capture all polymer types! And for particle characterization, should we rely solely on optical microscopy?\n"
                                    "Dr. Adams: Optical microscopy has an error rate of up to seventy percent for particles smaller than one millimeter. You must confirm polymer identity using Fourier-Transform Infrared Spectroscopy, or FTIR.\n"
                                    "Chloe: We will book FTIR machine time in the central laboratory today.",
                    "questions": [
                        {"id": "L1-Q21", "type": "Multiple Choice", "question_text": "Why does Dr. Adams recommend expanding from three to six sampling sites?", "options": ["To satisfy grant spending quotas", "To avoid data distortion from localized anomalies", "Because equipment requires larger sediment volume", "To test different estuaries in other countries"], "correct_answer": "To avoid data distortion from localized anomalies", "explanation": "Dr. Adams warns that three sites leave results 'vulnerable to localized anomalies'."},
                        {"id": "L1-Q22", "type": "Multiple Choice", "question_text": "What sediment core depth does Dr. Adams recommend?", "options": ["Top 2 cm", "Top 5 cm", "Top 10 cm", "Top 20 cm"], "correct_answer": "Top 5 cm", "explanation": "Dr. Adams notes the active layer is within the 'top five centimeters'."},
                        {"id": "L1-Q23", "type": "Multiple Choice", "question_text": "Why does Dr. Adams reject standard cellulose coffee filter papers?", "options": ["They are too expensive", "They degrade during hydrogen peroxide digestion", "They cannot trap particles larger than 1 mm", "They alter the salinity of the water"], "correct_answer": "They degrade during hydrogen peroxide digestion", "explanation": "He explains that cellulose filters degrade when exposed to hydrogen peroxide."},
                        {"id": "L1-Q24", "type": "Form Completion", "question_text": "Recommended filter specification: _______-micron glass fiber filters", "options": [], "correct_answer": "0.45", "explanation": "Dr. Adams explicitly advises '0.45-micron glass fiber filters'."},
                        {"id": "L1-Q25", "type": "Multiple Choice", "question_text": "Why is zinc chloride preferred over sodium chloride for density separation?", "options": ["It is non-toxic to aquatic organisms", "Its higher density floats heavier polymers like PVC", "It evaporates faster during drying", "It changes color when microplastics are present"], "correct_answer": "Its higher density floats heavier polymers like PVC", "explanation": "Dr. Adams explains zinc chloride reaches 1.6-1.7 g/cm3, capturing denser polymers."},
                        {"id": "L1-Q26", "type": "Form Completion", "question_text": "Density achieved by zinc chloride solution: 1.6 to _______ g/cm³", "options": [], "correct_answer": "1.7", "explanation": "Achieves a density of 1.6 to 1.7 grams per cubic centimeter."},
                        {"id": "L1-Q27", "type": "Multiple Choice", "question_text": "What is the estimated error rate of optical microscopy for particles under 1 mm?", "options": ["Up to 20%", "Up to 45%", "Up to 70%", "Up to 90%"], "correct_answer": "Up to 70%", "explanation": "Dr. Adams states optical microscopy has an error rate of 'up to seventy percent'."},
                        {"id": "L1-Q28", "type": "Form Completion", "question_text": "Spectroscopy method required to verify polymer chemistry: _______ (abbreviation)", "options": [], "correct_answer": "FTIR", "explanation": "Dr. Adams requires 'Fourier-Transform Infrared Spectroscopy, or FTIR'."},
                        {"id": "L1-Q29", "type": "Form Completion", "question_text": "Name of the estuary where fieldwork is conducted: _______ Estuary", "options": [], "correct_answer": "Severn", "explanation": "Liam mentions taking sediment cores along the 'Severn Estuary'."},
                        {"id": "L1-Q30", "type": "Multiple Choice", "question_text": "Where will the students book time for chemical spectroscopy?", "options": ["At the local museum", "In the central university laboratory", "At the municipal water plant", "Online via a commercial provider"], "correct_answer": "In the central university laboratory", "explanation": "Chloe says: 'We will book FTIR machine time in the central laboratory today'."}
                    ]
                },
                # Section 4: Questions 31 - 40
                {
                    "section_num": 4,
                    "title": "Section 4: University Lecture on Passive Bioclimatic Architecture",
                    "context": "An academic lecture by Professor Karen Vance on passive solar design principles in contemporary sustainable urban architecture.",
                    "audio_script": "Prof. Vance: Good afternoon class. In today's module on sustainable urban engineering, we will examine passive bioclimatic architecture—the design of buildings that maintain thermal comfort and illumination exclusively through natural environmental flows, without mechanical heating or refrigeration.\n"
                                    "Historically, vernacular builders instinctively understood these principles. In ancient Persia, subterranean windcatchers, known as badgirs, channeled cool desert breezes down into interior courtyards, while thick adobe walls provided massive thermal inertia.\n"
                                    "In contemporary design, the cornerstone of passive performance is building orientation. In the Northern Hemisphere, architects orient the primary glazed facade within fifteen degrees of true south. This strategic alignment maximizes low-angle solar heat gain during winter months while allowing horizontal roof overhangs to shade high-angle summer sun.\n"
                                    "A second fundamental mechanism is the Trombe wall, invented by French engineer Félix Trombe in 1957. A Trombe wall consists of a thick, dark-colored masonry wall positioned approximately five centimeters behind exterior glass glazing. Sunlight passes through the glazing, heating the dark masonry face. As the air in the narrow cavity warms, it rises by natural convection, entering upper vents into the living quarters, while cool floor-level air is drawn into bottom vents, creating continuous thermosiphonic circulation.\n"
                                    "Equally crucial is the thermal envelope's phase change materials, or PCMs. Unlike conventional concrete or brick, which rely purely on sensible heat capacity, microencapsulated paraffin PCMs absorb and release latent heat as they melt and solidify at twenty-two degrees Celsius. Incorporating PCMs into lightweight drywalls provides the thermal mass of a fifty-centimeter stone wall in a panel just two centimeters thick.\n"
                                    "Finally, we must address natural ventilation through the stack effect, or buoyancy-driven airflow. Warm interior air is less dense than exterior air; as it rises and exhausts through rooftop solar chimneys, it creates negative pressure at the building base, drawing fresh outdoor air through subterranean earth tubes that pre-cool incoming air by eight degrees Celsius during peak summer.\n"
                                    "Empirical monitoring demonstrates that passive bioclimatic buildings reduce lifetime heating and cooling energy consumption by seventy-five to ninety percent compared to conventional glass-curtain skyscrapers, representing a decisive pathway toward carbon neutrality.",
                    "questions": [
                        {"id": "L1-Q31", "type": "Form Completion", "question_text": "Historical Persian passive cooling towers were called _______.", "options": [], "correct_answer": "badgirs", "explanation": "Prof. Vance states: 'windcatchers, known as badgirs'."},
                        {"id": "L1-Q32", "type": "Form Completion", "question_text": "Thick adobe walls maintained comfortable temperatures by providing high thermal _______.", "options": [], "correct_answer": "inertia", "explanation": "Prof. Vance mentions: 'thick adobe walls provided massive thermal inertia'."},
                        {"id": "L1-Q33", "type": "Form Completion", "question_text": "In the Northern Hemisphere, primary glazed facades should face within 15 degrees of true _______.", "options": [], "correct_answer": "south", "explanation": "Architects orient the primary facade 'within fifteen degrees of true south'."},
                        {"id": "L1-Q34", "type": "Form Completion", "question_text": "A Trombe wall is positioned approximately _______ cm behind outer glass glazing.", "options": [], "correct_answer": "5", "explanation": "Positioned 'approximately five centimeters behind exterior glass glazing'."},
                        {"id": "L1-Q35", "type": "Form Completion", "question_text": "Air circulation in a Trombe wall operates through natural _______.", "options": [], "correct_answer": "convection", "explanation": "Prof. Vance explains: 'it rises by natural convection'."},
                        {"id": "L1-Q36", "type": "Form Completion", "question_text": "PCMs regulate room temperature by absorbing and releasing _______ heat.", "options": [], "correct_answer": "latent", "explanation": "Absorb and release 'latent heat as they melt and solidify'."},
                        {"id": "L1-Q37", "type": "Form Completion", "question_text": "Microencapsulated paraffin PCMs change phase at _______ degrees Celsius.", "options": [], "correct_answer": "22", "explanation": "Phase change occurs at 'twenty-two degrees Celsius'."},
                        {"id": "L1-Q38", "type": "Form Completion", "question_text": "The upward movement of warm air escaping through roof chimneys is known as the _______ effect.", "options": [], "correct_answer": "stack", "explanation": "Referred to as the 'stack effect, or buoyancy-driven airflow'."},
                        {"id": "L1-Q39", "type": "Form Completion", "question_text": "Subterranean earth tubes can pre-cool incoming summer air by _______ degrees Celsius.", "options": [], "correct_answer": "8", "explanation": "Pre-cooling incoming air 'by eight degrees Celsius'."},
                        {"id": "L1-Q40", "type": "Form Completion", "question_text": "Passive bioclimatic designs can decrease thermal energy demand by 75 to _______ percent.", "options": [], "correct_answer": "90", "explanation": "Energy demand reduced by 'seventy-five to ninety percent'."}
                    ]
                }
            ]
        }
    },

    # -----------------------------------------------------------------
    # WRITING TASKS (Task 1 & Task 2 with Band 9 Models)
    # -----------------------------------------------------------------
    {
        "id": "W-01",
        "module": "writing",
        "title": "IELTS Writing Task 2: Artificial Intelligence & Workforce Automation",
        "type": "Academic",
        "duration_minutes": 40,
        "difficulty": "Standard",
        "content": {
            "task_type": "Task 2",
            "title": "Automation and the Future of Employment",
            "prompt": "Some people believe that artificial intelligence and automation will lead to unprecedented levels of unemployment and economic inequality. Others argue that AI will create superior employment opportunities and drive human prosperity.\n\nDiscuss both views and give your own opinion.\n\nWrite at least 250 words. Give reasons for your answer and include any relevant examples from your own knowledge or experience.",
            "min_words": 250,
            "target_time_mins": 40,
            "band9_sample": "It is widely debated whether the proliferation of artificial intelligence and robotics constitutes an existential hazard to global employment or represents an unprecedented catalyst for socioeconomic flourishing. While detractors warn of mass redundancy and widening wealth disparities, proponents envisage a paradigm shift toward higher-tier cognitive vocations. In my estimation, while transitory labor dislocation is inevitable, automation will ultimately cultivate superior economic resilience provided educational structures adapt dynamically.\n\nOn the one hand, apprehension regarding widespread job displacement is grounded in empirical precedent. Unlike previous industrial revolutions that primarily automated repetitive physical labor, modern machine learning algorithms encroach directly upon analytical and creative domains, including paralegal analysis, radiography, and software engineering. When automated systems execute diagnostic and administrative tasks with greater velocity and negligible error margins, corporations have powerful incentives to reduce human payrolls. Without intervention, this phenomenon threatens to concentrate capital among tech conglomerates while marginalizing mid-tier service workers into precarious gig-economy roles.\n\nConversely, technological evolution has historically demonstrated a profound capacity for creative destruction. By superseding routine computational duties, AI liberates human capital to pioneer industries that were previously unimaginable, such as prompt architecture, bioinformatic engineering, and ethical algorithm stewardship. Furthermore, historical evidence from the dawn of telecommunications reveals that initial job contraction was swiftly counterbalanced by an explosion in downstream entrepreneurial ecosystems. As productivity escalates and service costs plummet, consumer purchasing power is redirected toward specialized care, artisanal craftsmanship, and scientific exploration.\n\nIn conclusion, while the apprehension surrounding algorithmic displacement is justified in the short term, AI should not be viewed as an absolute adversary to labor. By implementing state-sponsored retraining programs and updating vocational curricula to emphasize critical reasoning, societies can harness automation to augment human potential rather than diminish it."
        }
    },
    {
        "id": "W-02",
        "module": "writing",
        "title": "IELTS Writing Task 1: Renewable Energy Investment (2015-2024)",
        "type": "Academic",
        "duration_minutes": 20,
        "difficulty": "Standard",
        "content": {
            "task_type": "Task 1",
            "title": "Global Renewable Energy Investments by Sector (2015 vs 2024)",
            "prompt": "The table below shows global capital investments (in billions of USD) into three renewable energy sectors (Solar, Wind, and Hydroelectric) across four geographic regions in 2015 and 2024.\n\nSummarize the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
            "data_table": {
                "headers": ["Region", "Solar (2015 / 2024)", "Wind (2015 / 2024)", "Hydro (2015 / 2024)"],
                "rows": [
                    ["Asia-Pacific", "$45B / $130B", "$38B / $92B", "$25B / $30B"],
                    ["Europe", "$32B / $78B", "$42B / $85B", "$15B / $18B"],
                    ["North America", "$28B / $65B", "$30B / $60B", "$10B / $12B"],
                    ["Latin America", "$12B / $24B", "$8B / $18B", "$14B / $15B"]
                ]
            },
            "min_words": 150,
            "target_time_mins": 20,
            "band9_sample": "The provided table delineates capital expenditure across three renewable energy domains—Solar, Wind, and Hydroelectric—in four distinct geopolitical regions between 2015 and 2024.\n\nOverall, it is readily apparent that global renewable investments witnessed substantial expansion across all sectors and territories over the nine-year timeframe. Solar and wind technologies consistently absorbed the lion's share of financial allocations, whereas hydroelectric funding demonstrated comparatively marginal growth. Furthermore, the Asia-Pacific territory maintained decisive leadership in total capital deployment throughout.\n\nRegarding the most prominent sectors, solar investment in Asia-Pacific experienced an almost threefold surge from $45 billion in 2015 to an impressive $130 billion by 2024. European and North American solar commitments followed a similar upward trajectory, ascending to $78 billion and $65 billion respectively. Wind energy similarly commanded heavy backing, with Europe leading North America in 2024 ($85 billion versus $60 billion), while Asia-Pacific topped both at $92 billion.\n\nIn marked contrast, hydroelectric capital commitments remained largely stagnant. Regional totals in 2024 ranged between $12 billion in North America and $30 billion in Asia-Pacific, representing modest increments of under $5 billion across all surveyed zones."
        }
    },

    # -----------------------------------------------------------------
    # SPEAKING TESTS (Full 3-Part Guided Simulation)
    # -----------------------------------------------------------------
    {
        "id": "S-01",
        "module": "speaking",
        "title": "IELTS Speaking Full Mock Interview 1: Technology & Life Decisions",
        "type": "Academic",
        "duration_minutes": 15,
        "difficulty": "Standard",
        "content": {
            "part1": {
                "title": "Part 1: Introduction & Everyday Topics",
                "intro_text": "Good morning. My name is Dr. Richardson and I will be your examiner today. Could you tell me your full name, please?",
                "questions": [
                    {
                        "q_num": 1,
                        "text": "Do you work or are you currently studying?",
                        "audio_prompt": "Let's begin by discussing your daily occupation. Do you work or are you currently studying?"
                    },
                    {
                        "q_num": 2,
                        "text": "What do you enjoy most about what you do?",
                        "audio_prompt": "What do you find most rewarding or enjoyable about your study or work?"
                    },
                    {
                        "q_num": 3,
                        "text": "How do you typically unwind and relax after a demanding day?",
                        "audio_prompt": "In the evenings or weekends, how do you typically unwind and decompress after a demanding day?"
                    }
                ]
            },
            "part2": {
                "title": "Part 2: Individual Long Turn (Cue Card)",
                "cue_card": "Describe a difficult decision that you made recently that had a positive outcome.\n\nYou should say:\n- What the decision was\n- When you made it\n- Why it was difficult or stressful\n- And explain why the outcome was positive for your life.",
                "prep_time_seconds": 60,
                "speak_time_seconds": 120,
                "audio_prompt": "Now, for Part 2, I am going to give you a topic and I'd like you to talk about it for one to two minutes. Before you talk, you have one minute to think about what you are going to say. You can make some notes if you wish. Here is your topic: Describe a difficult decision that you made recently that had a positive outcome."
            },
            "part3": {
                "title": "Part 3: Two-Way Analytical Discussion",
                "questions": [
                    {
                        "q_num": 1,
                        "text": "Why do some people find it exceedingly stressful to make important life choices?",
                        "audio_prompt": "We've been talking about decision making. Let's explore this in more depth. Why do you think many people find it exceedingly stressful to make critical life choices?"
                    },
                    {
                        "q_num": 2,
                        "text": "To what extent has modern technology made decision-making easier or more complicated?",
                        "audio_prompt": "In what ways has the abundance of online information and algorithmic recommendations impacted human decision making?"
                    },
                    {
                        "q_num": 3,
                        "text": "Do you believe older generations are always better equipped to advise youth on career choices?",
                        "audio_prompt": "Finally, do you believe older family members are always best suited to counsel younger generations on their professional trajectories?"
                    }
                ]
            }
        }
    }
]

def seed_tests():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if tests already populated with full 480-set Cambridge bank
    cursor.execute('SELECT COUNT(*) FROM tests')
    current_test_count = cursor.fetchone()[0]
    
    if current_test_count < 480:
        try:
            from generate_cambridge_bank import seed_cambridge_exam_bank
            conn.close()
            seed_cambridge_exam_bank()
            conn = get_connection()
            cursor = conn.cursor()
        except Exception as e:
            print("Fallback seeding tests:", e)
            for t in TESTS_DATA:
                cursor.execute('''
                INSERT OR REPLACE INTO tests (id, module, title, type, duration_minutes, difficulty, content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    t['id'],
                    t['module'],
                    t['title'],
                    t.get('type', 'Academic'),
                    t.get('duration_minutes', 30),
                    t.get('difficulty', 'Authentic Cambridge Standard'),
                    json.dumps(t['content'])
                ))

    # Check if General Training tests are populated
    cursor.execute("SELECT COUNT(*) FROM tests WHERE lower(type) = 'general training'")
    gt_test_count = cursor.fetchone()[0]
    if gt_test_count < 120:
        try:
            from cambridge_gt_bank import seed_cambridge_gt_bank
            conn.close()
            seed_cambridge_gt_bank()
            conn = get_connection()
            cursor = conn.cursor()
        except Exception as e:
            print("Failed seeding General Training tests:", e)
    
    # Add initial vocabulary entries if empty
    cursor.execute('SELECT COUNT(*) FROM vocabulary_notebook')
    if cursor.fetchone()[0] == 0:
        sample_vocab = [
            ("detrimental", "Colloquial alternatives like 'bad' lower scores; 'detrimental effect' achieves Band 8+.", "Band 8+", "Tending to cause harm or damage.", "adverse, damaging, deleterious", "Writing"),
            ("exponential surge", "Used for describing graphs showing sharp rapid growth in Task 1.", "Band 8+", "A rapid, dramatic and compounding increase.", "skyrocketing, rapid ascent", "Writing Task 1"),
            ("double-edged sword", "Effective idiomatic idiom for discussing controversial themes in Speaking.", "Band 8+", "A situation or tool that has both favorable and hazardous outcomes.", "mixed blessing", "Speaking Part 3"),
            ("consolidate", "Critical academic verb for memory, knowledge, and corporate mergers.", "Band 8+", "To combine into a single more effective or coherent whole.", "solidify, reinforce, unify", "Reading"),
            ("predominant", "Excellent reporting adjective for Task 1 Academic charts.", "Band 8+", "Present as the strongest or main element.", "prevailing, paramount, dominant", "Writing Task 1")
        ]
        for w, c, b, m, s, src in sample_vocab:
            cursor.execute('''
            INSERT INTO vocabulary_notebook (word_or_phrase, context, band_level, meaning, synonyms, module_source)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (w, c, b, m, s, src))

    conn.commit()
    conn.close()
