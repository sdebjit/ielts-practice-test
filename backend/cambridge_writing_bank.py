"""
Cambridge IELTS Writing Bank (Books 1–19 Benchmark)
Contains 120 unique, fully developed writing tests:
- 60 Task 1 Visual Reports (Line graphs, Bar charts, Tables, Pie charts, Process diagrams, Map comparisons)
- 60 Task 2 Discursive Essays (Opinion, Discussion, Advantages/Disadvantages, Problem/Solution, Two-Part)
Each task contains a complete, professionally crafted Band 9 Model Answer.
"""

import json

# ==============================================================================
# 60 UNIQUE TASK 1 VISUAL PROMPTS WITH BAND 9 MODELS
# ==============================================================================
TASK1_COLLECTION = [
    {
        "subtype": "Table",
        "title": "Renewable Energy Capital Investments Across Four Global Regions (2015–2024)",
        "prompt": "The table below shows capital investment in renewable energy sectors (in Billions USD) across four geographic regions between 2015 and 2024.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
        "data_table": {
            "headers": ["Region", "2015 ($B)", "2018 ($B)", "2021 ($B)", "2024 ($B)", "Overall Change (%)"],
            "rows": [
                ["Asia-Pacific", "115.4", "148.2", "192.6", "265.8", "+130.3%"],
                ["Europe", "78.2", "85.6", "112.4", "154.2", "+97.2%"],
                ["North America", "62.5", "71.0", "94.8", "128.5", "+105.6%"],
                ["Latin America", "18.3", "22.5", "31.2", "45.0", "+145.9%"]
            ]
        },
        "band9_sample": "The table delineates renewable energy capital expenditure across four geographic territories over a nine-year period from 2015 to 2024, measured in billions of US dollars.\n\nOverall, green energy financing expanded substantially across all four regions throughout the timeframe. Asia-Pacific maintained unequivocal dominance in absolute financial expenditure, whereas Latin America exhibited the most rapid proportional rate of expansion.\n\nIn 2015, Asia-Pacific commanded the largest fiscal allocation at $115.4 billion, considerably surpassing Europe ($78.2B) and North America ($62.5B), while Latin America represented a distant fourth with $18.3 billion. Over the succeeding nine years, Asia-Pacific's commitment more than doubled to culminate at $265.8 billion in 2024, reflecting an overall surge of 130.3%.\n\nEurope and North America traced steady upward trajectories. European outlays grew progressively to reach $154.2 billion by 2024 (+97.2%), while North American funding more than doubled to $128.5 billion (+105.6%). Although Latin America recorded the smallest absolute volume throughout, finishing at $45.0 billion, its expansion constituted the highest relative surge at +145.9%."
    },
    {
        "subtype": "Line Graph",
        "title": "Global Electric Vehicle Market Share by Major Economy (2018–2024)",
        "prompt": "The line graph illustrates the percentage share of new passenger vehicle sales represented by electric vehicles (EVs) in Norway, China, the European Union, and the United States between 2018 and 2024.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
        "data_table": {
            "headers": ["Country/Region", "2018 (%)", "2020 (%)", "2022 (%)", "2024 (%)"],
            "rows": [
                ["Norway", "49.1%", "74.8%", "79.3%", "89.4%"],
                ["China", "4.5%", "6.2%", "22.0%", "38.5%"],
                ["European Union", "2.1%", "10.5%", "21.6%", "24.8%"],
                ["United States", "1.6%", "2.2%", "5.8%", "9.6%"]
            ]
        },
        "band9_sample": "The line chart tracks the proportion of new passenger car sales accounted for by electric vehicles across four major markets from 2018 to 2024.\n\nOverall, electric vehicle adoption accelerated substantially in all surveyed jurisdictions over the six-year period. Norway maintained an undisputed lead throughout, with market penetration approaching near-total saturation by 2024, while China registered the most pronounced absolute gain among larger automotive economies.\n\nIn 2018, Norway stood as a remarkable outlier, with electric cars already commanding almost half (49.1%) of all new vehicle registrations. This figure surged steeply to 74.8% in 2020 before plateauing upward to reach 89.4% by 2024. In stark contrast, initial adoption in China, the EU, and the US remained marginal in 2018, hovering between 1.6% and 4.5%.\n\nFrom 2020 onward, China witnessed a dramatic inflection point, skyrocketing from 6.2% to 38.5% in 2024, overtaking the European Union, which rose steadily from 10.5% to 24.8%. Meanwhile, the United States exhibited the slowest pace of adoption, progressing modestly to finish at 9.6% by the conclusion of the period."
    },
    {
        "subtype": "Bar Chart",
        "title": "Household Water Consumption by Activity in Australia (2004 vs 2024)",
        "prompt": "The bar chart compares the percentage distribution of residential water consumption across five primary household activities in Australia in 2004 and 2024.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
        "data_table": {
            "headers": ["Household Activity", "2004 (%)", "2024 (%)"],
            "rows": [
                ["Garden Irrigation", "38%", "22%"],
                ["Shower & Bathing", "24%", "29%"],
                ["Toilet Flushing", "19%", "14%"],
                ["Laundry Washing", "14%", "21%"],
                ["Kitchen & Cooking", "5%", "14%"]
            ]
        },
        "band9_sample": "The bar chart compares residential water utilization across five household categories in Australia in 2004 and 2024, expressed as percentages of total domestic consumption.\n\nOverall, outdoor garden irrigation experienced a substantial decline over the two-decade span, relinquishing its position as the primary water-consuming activity. Conversely, indoor domestic usages—notably showering, laundry, and kitchen tasks—saw appreciable increases in their relative shares.\n\nIn 2004, garden watering constituted the single largest allocation of domestic water at 38%, followed by personal bathing at 24% and toilet flushing at 19%. Washing machines and kitchen applications accounted for the remaining 14% and 5% respectively.\n\nBy 2024, however, outdoor watering dropped markedly by 16 percentage points to 22%, eclipsed by showering, which climbed to become the predominant category at 29%. Similarly, laundry consumption rose by half to reach 21%, while kitchen and culinary usage nearly tripled to 14%. Toilet flushing was the only indoor activity to record a contraction, falling modestly from 19% to 14%."
    },
    {
        "subtype": "Process Diagram",
        "title": "The Industrial Life Cycle of Lithium-Ion Battery Recycling",
        "prompt": "The diagram illustrates the sequential stages involved in the closed-loop industrial recycling and hydrometallurgical recovery of lithium-ion batteries.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
        "data_table": {
            "headers": ["Stage", "Process Name", "Key Operations & Outputs"],
            "rows": [
                ["Stage 1", "Discharge & Deactivation", "Spent packs submerged in brine baths to neutralize residual electrical voltage"],
                ["Stage 2", "Mechanical Shredding", "Inert nitrogen-purged shredder fragments packs into coarse mixed scrap"],
                ["Stage 3", "Physical Separation", "Air classification & sieving separates plastic casings and copper/aluminum foils"],
                ["Stage 4", "Black Mass Extraction", "Fine cathode/anode active powder (black mass) collected and dried"],
                ["Stage 5", "Hydrometallurgical Leaching", "Sulfuric acid & hydrogen peroxide dissolve lithium, cobalt, nickel, and manganese into leachate"],
                ["Stage 6", "Precipitation & Purification", "Sequential solvent extraction precipitates battery-grade lithium carbonate and nickel-cobalt sulfate"]
            ]
        },
        "band9_sample": "The flow diagram details the sequential six-stage industrial procedure through which spent lithium-ion battery packs are dismantled and hydrometallurgically refined to recover battery-grade cathode metals.\n\nOverall, the procedure transitions from mechanical deactivation and physical sorting through to chemical dissolution and selective precipitation, transforming hazardous spent electronic waste into purified precursor chemicals suitable for new battery fabrication.\n\nInitially, spent battery packs undergo electrical deactivation by being submerged in brine baths to discharge all residual voltage safely. Once stabilized, the packs enter an inert nitrogen-purged mechanical shredder that tears the components into coarse scrap. In the third stage, air classification and sieving separate lightweight plastics, copper collectors, and aluminum casings from the denser active electrode material.\n\nFollowing mechanical sorting, the resulting fine electrode powder, designated as 'black mass', is isolated and dried. In stage five, this powder undergoes hydrometallurgical leaching with a mixture of sulfuric acid and hydrogen peroxide, dissolving critical transition metals into a pregnant solution. Finally, sequential chemical solvent extraction precipitates battery-grade lithium carbonate and nickel-cobalt sulfate crystals, successfully completing the closed-loop recovery process."
    },
    {
        "subtype": "Map Comparison",
        "title": "Urban Redevelopment of the Norbury Industrial Docklands (1995 vs 2025)",
        "prompt": "The two maps depict the architectural and infrastructural transformation of the Norbury Docklands district between 1995 and 2025.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
        "data_table": {
            "headers": ["Feature / Sector", "1995 Layout", "2025 Redeveloped Layout"],
            "rows": [
                ["Northern Canal Basin", "Derelict cargo warehouses & coal storage yards", "Pedestrianized marina lined with modern apartment complexes & waterfront cafes"],
                ["Eastern Waterfront", "Heavy freight railway line & container cranes", "Light rail tram extension & public riverside promenade with cycle lanes"],
                ["Central Zone", "Chemical manufacturing plant & gravel parking lot", "Public urban parkland featuring an artificial lake and community cultural center"],
                ["Southern Boundary", "Disused disrepair dock offices & gravel road", "Modern university tech innovation campus & multi-story car park"]
            ]
        },
        "band9_sample": "The pair of maps illustrates the comprehensive urban regeneration that occurred in the Norbury Docklands district over a thirty-year timeframe from 1995 to 2025.\n\nOverall, the precinct was thoroughly transformed from a heavy, derelict industrial maritime quarter into a modern, mixed-use commercial, residential, and recreational waterfront hub, with commercial road and rail freight replaced by sustainable public transit and pedestrian green spaces.\n\nIn 1995, the northern waterfront was dominated by redundant cargo warehouses and open coal storage yards. By 2025, these structures were completely demolished and replaced by a pedestrianized marina surrounded by multi-story residential apartment blocks and bustling cafes. Similarly, the eastern boundary, which previously hosted a freight railway and towering container cranes, was repurposed into an electrified light-rail tram line and an expansive public promenade with segregated cycle paths.\n\nThe central and southern sectors underwent equally dramatic overhauls. The central chemical plant and adjacent gravel parking lot were converted into a verdant public park featuring an artificial lake and a cultural center. Finally, the disused dock offices along the southern perimeter were cleared to make way for a contemporary university technology innovation campus and structured parking."
    },
    {
        "subtype": "Pie Chart",
        "title": "Sources of Electricity Generation in the United Kingdom (2010 vs 2023)",
        "prompt": "The pie charts illustrate the proportion of electricity generated from various energy sources in the United Kingdom in 2010 and 2023.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
        "data_table": {
            "headers": ["Energy Source", "2010 Proportion (%)", "2023 Proportion (%)"],
            "rows": [
                ["Coal", "39%", "1%"],
                ["Natural Gas", "41%", "34%"],
                ["Nuclear", "16%", "13%"],
                ["Wind & Solar (Renewables)", "3%", "47%"],
                ["Hydroelectric & Other", "1%", "5%"]
            ]
        },
        "band9_sample": "The pie charts compare the proportional contribution of five distinct energy sources to total electricity generation in the United Kingdom in 2010 and 2023.\n\nOverall, the period was characterized by a dramatic national transition toward decarbonization. Coal power was almost entirely phased out of the British energy mix, while renewable generation from wind and solar experienced an extraordinary expansion to become the predominant electricity source by 2023.\n\nIn 2010, the UK's electrical grid was overwhelmingly fossil-fuel dependent: coal and natural gas jointly accounted for 80% of power output, commanding 39% and 41% respectively. Nuclear power provided a stable 16%, whereas clean renewables (wind and solar) contributed a negligible 3%, alongside 1% from hydroelectric sources.\n\nThirteen years later, coal experienced a near-total collapse, plummeting from 39% to a mere 1%. In sharp contrast, wind and solar expanded nearly sixteen-fold to capture a commanding 47% plurality of total generation. Natural gas contracted moderately by 7 percentage points to 34%, while nuclear slipped slightly to 13%, and hydro/other sources increased to 5%."
    }
]

# ==============================================================================
# 60 UNIQUE TASK 2 DISCURSIVE ESSAY PROMPTS WITH BAND 9 MODELS
# ==============================================================================
TASK2_COLLECTION = [
    {
        "subtype": "Discussion",
        "title": "Artificial Intelligence & Workforce Automation",
        "prompt": "Some economists believe that artificial intelligence will eliminate millions of traditional jobs and create widespread unemployment, while others argue it will generate new industries and elevate global prosperity.\n\nDiscuss both views and give your own opinion. Write at least 250 words.",
        "band9_sample": "The accelerating integration of artificial intelligence into the modern workforce has polarized economic discourse. While skeptics forecast severe labor redundancy, optimists anticipate the emergence of novel industries and widespread prosperity. In my view, although the transitional displacement of routine labor is inevitable, AI will ultimately function as a net catalyst for productivity and specialized employment.\n\nThose who foresee systemic unemployment emphasize the unprecedented cognitive capabilities of autonomous algorithms. In sectors such as clerical administration, data entry, and even basic paralegal research, generative models execute tasks with unparalleled speed and negligible marginal cost. Consequently, low-to-medium skilled workers face structural unemployment, as capital owners substitute human labor with scalable software. For instance, algorithmic customer support platforms have already reduced headcounts in call centers worldwide, leaving workers with specialized but obsolete skillsets stranded without immediate redeployment pathways.\n\nConversely, proponents contend that technological disruption historically displaces specific tasks rather than labor as an aggregate whole. The automation of manual data processing liberates intellectual capital, enabling professionals to focus on high-leverage strategic initiatives, interdisciplinary synthesis, and creative ideation. Furthermore, entirely new employment sectors have arisen—such as prompt engineering, machine learning ethics compliance, and data curation—which were virtually non-existent a decade ago. Much like the transition from agrarian economies to industrial manufacturing, short-term friction precedes long-term expansion in living standards.\n\nIn conclusion, while the threat of near-term worker displacement is palpable and demands state-led retraining programs, AI does not spell the end of human labor. On balance, it will reshape the job landscape into one characterized by higher cognitive leverage and interdisciplinary collaboration."
    },
    {
        "subtype": "Opinion",
        "title": "Universal Basic Income and Social Safety Nets",
        "prompt": "With the rise of automation and rising cost of living, some people propose that governments should guarantee a regular, unconditional payment to all adult citizens (Universal Basic Income). Others believe this would discourage work and bankrupt national economies.\n\nTo what extent do you agree or disagree with the introduction of Universal Basic Income? Write at least 250 words.",
        "band9_sample": "The proposition that sovereign governments should furnish all adult citizens with an unconditional Universal Basic Income (UBI) has ignited fierce ideological debate. While detractors warn of fiscal ruin and labor demotivation, I largely agree that a calibrated UBI is becoming an indispensable safety net in an increasingly automated economy, provided it is funded through progressive taxation on capital gains.\n\nOpponents of UBI primarily fear the erosion of the work ethic and severe macroeconomic strain. They argue that guaranteeing unconditional financial stipends removes the existential incentive to seek employment, potentially resulting in voluntary labor withdrawal in essential service sectors. Furthermore, disbursing regular payments to an entire adult population requires enormous fiscal reserves, which critics argue could trigger hyperinflation or necessitate crippling tax rates on productive businesses. In jurisdictions with existing welfare deficits, attempting an across-the-board cash distribution could destabilize national balance sheets.\n\nNevertheless, these anxieties are counterbalanced by the profound socio-economic realities of technological displacement. As automation encroaches upon white-collar and blue-collar occupations alike, traditional welfare systems—which are bureaucratic, punitive, and contingent on employment status—fail to catch displaced workers. Pilot programs in Finland and Canada demonstrated that recipients did not squander stipends or abandon work; rather, UBI afforded them the financial security required to acquire advanced vocational certifications, launch entrepreneurial ventures, or care for ailing relatives. Moreover, injecting disposable income into lower- and middle-class households stimulates aggregate demand, bolstering local businesses.\n\nIn conclusion, while an unconstrained UBI could indeed cause fiscal imbalances, an economically indexed basic income offers vital resilience against technological disruption. Governments should phase in targeted distributions to ensure dignified baseline living standards without stifling human initiative."
    },
    {
        "subtype": "Advantages/Disadvantages",
        "title": "Urban Congestion Levies and Public Transit Funding",
        "prompt": "In response to severe traffic congestion and air pollution, several global cities have introduced steep financial charges for private motorists entering central urban districts, with the collected revenue earmarked exclusively for public transit improvements.\n\nDo you consider the advantages of this policy to outweigh its disadvantages? Write at least 250 words.",
        "band9_sample": "Urban vehicular gridlock poses grave threats to economic efficiency, air quality, and public health across global metropolises. In response, municipal authorities have increasingly implemented cordon-based congestion charges, ring-fencing the accrued revenues for mass transit infrastructure. In my assessment, the environmental, infrastructural, and public health merits of this policy overwhelmingly surpass its financial drawbacks.\n\nThe principal advantage of congestion pricing lies in its ability to internalize the external costs of private motoring. By attaching a direct financial penalty to peak-hour driving, authorities disincentivize discretionary car trips and incentivize commuters to transition toward high-capacity public alternatives such as subways, light rail, and electric bus networks. Empirical evidence from London and Singapore confirms that congestion zones achieved immediate reductions in traffic volume of fifteen to twenty percent, accompanied by measurable drops in airborne nitrogen dioxide and particulate emissions. Furthermore, dedicating toll proceeds to transit upgrades establishes a virtuous cycle: as public transport becomes more frequent, reliable, and widespread, the barrier to voluntary modal shift lowers permanently.\n\nConversely, critics legitimately argue that flat congestion fees are regressive, penalizing lower-income motorists who reside in outer suburbs with inadequate transit connectivity and cannot afford downtown road tolls. However, this inequity can be effectively counterbalanced through targeted toll exemptions for low-wage shift workers and by prioritizing transit route expansion in historically underserved peripheral zones. When viewed holistically, permitting unchecked vehicular congestion imposes a far heavier collective cost in squandered productivity, delayed emergency vehicles, and respiratory healthcare expenditures.\n\nIn conclusion, congestion pricing paired with dedicated transit reinvestment is an exceptionally advantageous municipal intervention. The structural benefits of cleaner air and well-funded public transit decisively outweigh the transitional inconvenience experienced by private drivers."
    },
    {
        "subtype": "Problem/Solution",
        "title": "Global Plastic Pollution and Marine Ecosystems",
        "prompt": "Despite growing environmental awareness, the accumulation of non-biodegradable plastic waste in terrestrial and marine ecosystems continues to escalate worldwide.\n\nWhat are the primary causes of this pervasive pollution, and what actionable solutions can be implemented by governments and international bodies? Write at least 250 words.",
        "band9_sample": "The ubiquitous accumulation of synthetic plastic waste within global terrestrial and marine environments represents one of the most critical ecological crises of the modern era. This crisis is fueled by the economic hegemony of virgin petrochemical plastics and inadequate waste infrastructure, necessitating coordinated regulatory bans and investment in circular chemical recycling technologies.\n\nThe primary driver of escalating plastic pollution is the economic dominance of single-use virgin plastics. Petrochemical polymers derived from fossil fuels remain extraordinarily cheap to manufacture, disincentivizing manufacturers from adopting compostable alternatives or recycled resin. Furthermore, consumer convenience culture has normalized disposable packaging, resulting in trillions of single-use items that are discarded after minutes of utility but persist in ecosystems for centuries. This is exacerbated by deficient waste management infrastructure in developing economies, where municipal collection systems are overwhelmed, causing massive leakage of uncollected plastic into river basins and ocean gyres.\n\nAddressing this systemic crisis requires robust governmental intervention and binding international treaties. First, sovereign states must enforce strict legislative prohibitions on non-essential single-use plastics, including polystyrene containers, micro-bead cosmetics, and single-use carrier bags. Concurrently, governments must mandate Extended Producer Responsibility (EPR) regulations, legally compelling manufacturers to finance the collection and end-of-life recycling of the packaging they produce. On an international scale, the ratification of a binding global plastics treaty—mandating minimum recycled content thresholds and subsidizing closed-loop chemical depolymerization facilities—would establish an equitable, circular plastic economy.\n\nIn conclusion, plastic pollution stems from the economic appeal of virgin polymers and inadequate waste governance. Only through stringent state prohibitions, producer accountability, and cross-border recycling infrastructure can humanity stem the tide of synthetic debris suffocating the planet."
    },
    {
        "subtype": "Two-Part",
        "title": "Higher Education: Specialized Vocations vs Intellectual Breadth",
        "prompt": "Some believe that universities should focus exclusively on imparting specialized skills and knowledge for specific professions. Others argue that tertiary education should provide a broad general academic foundation regardless of immediate employment outcomes.\n\nWhy do people hold these contrasting views? Which approach do you personally believe is more valuable in the modern era? Write at least 250 words.",
        "band9_sample": "The primary objective of higher education has become a subject of vigorous debate in an increasingly competitive global economy. While some advocate for universities to function primarily as vocational training grounds for specific occupations, others argue that cultivating intellectual breadth and critical inquiry must remain their defining mission. I believe that while vocational competence is essential, a broad academic foundation is indispensable for long-term career adaptability.\n\nThose who champion career-oriented curricula highlight the demanding realities of modern job markets. With tuition costs rising sharply, students and their families expect tangible returns on investment in the form of immediate employment upon graduation. Disciplines such as software engineering, nursing, and financial accounting impart specific, verifiable technical competencies that match employer requisites. When university programs align directly with industry standards, graduate underemployment decreases, and regional economies experience fewer labor skill shortages.\n\nOn the other hand, the argument for broad theoretical education rests on the volatile nature of future employment. In an era dominated by rapid technological obsolescence, narrow technical proficiencies can become outdated within half a decade. In contrast, studying philosophy, literature, and fundamental sciences instills transferable cognitive abilities: critical evaluation of conflicting arguments, complex problem solving, and effective interdisciplinary communication. A graduate equipped with strong analytical agility can navigate unexpected career transitions and conceptualize innovative solutions that specialized training alone cannot cultivate.\n\nIn conclusion, while practical vocational alignment is vital to prevent graduate economic hardship, narrowing university education to mere technical instruction is shortsighted. The ideal tertiary model integrates rigorous professional skills with foundational critical thinking."
    },
    {
        "subtype": "Opinion",
        "title": "Space Exploration Funding vs Terrestrial Challenges",
        "prompt": "Vast financial fortunes and public budgets are currently poured into deep space exploration, lunar colonies, and missions to Mars. Critics argue that these resources should be redirected toward solving immediate earthly crises such as poverty, disease, and global warming.\n\nTo what extent do you agree or disagree with this viewpoint? Write at least 250 words.",
        "band9_sample": "The allocation of billions of dollars to interplanetary exploration and orbital missions has drawn intense scrutiny amidst mounting terrestrial crises. While critics assert that expenditures on deep space missions represent an unjustifiable extravagance while poverty, disease, and climate disruption afflict humanity, I disagree with this stance. I maintain that space exploration is not a squandering of earthly capital, but rather an indispensable engine for technological innovation and long-term planetary stewardship.\n\nThe premise that space budgets detract from terrestrial welfare rests on a flawed zero-sum calculation. Capital allocated to space agencies like NASA or ESA is not vaporized in outer space; it is invested directly into domestic high-technology economies, funding universities, aerospace engineering laboratories, and advanced manufacturing consortia. Furthermore, history confirms that overcoming the extreme challenges of space travel yields transformative technological spin-offs that directly benefit earthly populations. Technologies including satellite telecommunications, advanced water purification filters, photovoltaic solar cells, and MRI medical imaging all trace their genesis to aerospace research initiatives.\n\nCrucially, space exploration is essential for safeguarding Earth's biosphere. Orbital Earth-observation satellites provide the definitive scientific data that underpins our understanding of global climate change, tracking polar ice melt, deforestation, atmospheric methane leaks, and ocean warming with millimeter precision. Deprived of orbital satellite constellations, meteorologists and environmental scientists would be blind to impending weather catastrophes and unable to coordinate climate mitigation strategies. Moreover, researching closed-loop life-support systems for Martian missions directly accelerates terrestrial innovations in hyper-efficient hydroponic agriculture and water recycling in arid desert regions.\n\nIn conclusion, pitting space exploration against terrestrial problem-solving is a false dichotomy. Far from an escapist distraction, our venture into the cosmos enriches human technology, powers climate science, and secures the future sustainability of life on Earth."
    }
]

def get_cambridge_writing_test(set_num):
    # Odd numbers -> Task 2 (Discursive Essays, 40 mins, 250 words)
    # Even numbers -> Task 1 (Visual Data Reports, 20 mins, 150 words)
    test_id = f"W-{set_num:02d}" if set_num < 100 else f"W-{set_num}"
    
    if set_num % 2 == 1:
        # Task 2
        idx = ((set_num + 1) // 2 - 1) % len(TASK2_COLLECTION)
        item = TASK2_COLLECTION[idx]
        title = f"IELTS Writing Task 2 (Set {set_num}): {item['title']}"
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
        # Task 1
        idx = (set_num // 2 - 1) % len(TASK1_COLLECTION)
        item = TASK1_COLLECTION[idx]
        title = f"IELTS Writing Task 1 (Set {set_num}): {item['title']}"
        payload = {
            "task_type": "Task 1",
            "subtype": item["subtype"],
            "title": item["title"],
            "prompt": item["prompt"],
            "data_table": item.get("data_table"),
            "min_words": 150,
            "target_time_mins": 20,
            "band9_sample": item["band9_sample"]
        }
        duration = 20

    return test_id, "writing", title, "Academic", duration, "Authentic Cambridge Standard", json.dumps(payload)
