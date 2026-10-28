# IELTS Master: Full-Stack Practice & Improvement Tracker (Gemini AI Powered)

A full-stack IELTS preparation platform tailored to systematically improve your scores across all 4 segments: **LISTENING**, **READING**, **WRITING**, and **SPEAKING**.

Instead of unstructured chat, this application provides an authentic examination environment, automated official IELTS 9-band rubric assessments, granular weakness diagnostics, progress trendlines, and Gemini AI-driven coaching.

---

## 🌟 Key Features Across All 4 Segments

### 1. 🎧 Listening Simulation
- **Authentic 4-Part Structure**: Section 1 (Everyday social dialogue), Section 2 (Public monologue/orientation), Section 3 (Academic consultation/tutorial), and Section 4 (Academic lecture).
- **Interactive Audio Simulator**: Built-in voice player using Web Speech Synthesis, variable playback speed (`0.85x`, `1.0x`, `1.2x`), audio wave visualizer, and collapsible transcript toggle.
- **Auto-Grading & Analysis**: Instant grading against official Cambridge band conversion tables (out of 40 raw score to Band 0–9).
- **Distractor Analysis**: Detailed explanations explaining *why* an answer is correct and where the speaker distractors were.

### 2. 📖 Academic Reading (Split-Screen Interface)
- **Authentic Reading Passages**: High-difficulty descriptive and scientific texts (Passage 1 & Passage 2).
- **Split-Screen UX**: Passage on the left with interactive **Text Highlighter** and font size scaling (`A-` / `A+`); questions on the right.
- **Standard Question Formats**: True/False/Not Given, Matching Headings, Summary Completion, and Multiple Choice.
- **60-Minute Exam Countdown Timer**: Accustoms you to real test pacing pressure.

### 3. ✍️ Writing Task 1 & Task 2 Evaluator (Gemini AI Examiner)
- **Task 1 (Academic)**: Data reports with tables/charts and 150-word minimum threshold.
- **Task 2 (Discursive Essay)**: Complex social/technological essays with 250-word minimum threshold.
- **Real-Time Word Counter**: Color-coded feedback ensuring you never fall short of minimum word count penalties.
- **Examiner Evaluation Report (Gemini AI)**:
  - Estimated Band Score (0.0 to 9.0 in 0.5 increments).
  - Breakdown across the 4 official IELTS criteria:
    1. *Task Achievement / Task Response*
    2. *Coherence and Cohesion*
    3. *Lexical Resource*
    4. *Grammatical Range and Accuracy*
  - **Line-by-Line Corrections**: Pinpoints exact sentences, native Band 8+ rewrites, and grammatical rationales.
  - **Band 8+ Lexical Upgrades**: Replaces repetitive or elementary vocabulary with academic collocations and provides a 1-click button to save them to your notebook.
  - **Band 9 Model Answers**: Complete model essays for comparison.

### 4. 🗣️ Speaking Mock Interview (Live Examiner Simulation)
- **Full 3-Part Test**:
  - *Part 1*: Warm-up questions on occupation, routines, and leisure.
  - *Part 2*: Cue Card with 1-minute prep timer and 2-minute speaking countdown.
  - *Part 3*: In-depth abstract two-way discussion questions.
- **Live Voice Examiner**: Uses browser voice synthesis to ask questions aloud just like a Cambridge/IDP examiner.
- **Voice Transcription**: Speak directly into your microphone (Web Speech API) or type your responses.
- **Examiner Evaluation Report (Gemini AI)**:
  - 4 Criteria: *Fluency & Coherence*, *Lexical Resource*, *Grammatical Range & Accuracy*, *Pronunciation*.
  - **Filler Word Detection**: Analyzes hesitations (e.g. *“um”*, *“like”*, *“you know”*).
  - **PREP Framework Expansion Advice**: Teaches how to formulate structured 4-sentence answers (*Point, Reason, Example, Point*).
  - **Native Conversational Expressions**: Suggestions to elevate everyday idioms to natural Band 8+ register.

---

## 📊 Diagnostic Engine: "What Things You Need to Improve"

The dashboard does not just give a number; it diagnoses your specific bottlenecks:
- **Official IELTS Overall Band Score**: Automatically averages your 4 modules using the official IELTS rounding formula (rounding up from .25 to .5, and .75 to the next whole band).
- **Segment Diagnostic Radar**:
  - *Listening*: Identifies whether Multiple Choice distractors or Form Completion spellings are pulling your score down.
  - *Reading*: Differentiates between *False* (contradiction) and *Not Given* (absence of evidence) mistakes.
  - *Writing*: Highlights your lowest scoring criterion (e.g., Lexical Resource vs Grammar Range).
  - *Speaking*: Analyzes fluency pauses and provides targeted speaking drills.
- **Personalized 3-Step Action Roadmap**: Automatically generates high-priority drills based on historical performance.
- **Interactive Visualizations**: Radar chart comparing your current balance vs your target band, plus score trendlines over time.
- **Study Activity Streak & Exam Countdown**: Tracks consecutive study days and time spent.

---

## 🚀 Quick Start Guide

### 1. Launch the Application
Run the startup script in terminal:
```bash
cd /Users/sadhukhandebjit/.gemini/antigravity/scratch/ielts-gemini-prep
./start.sh 8080
```
Open your browser and navigate to:
```
http://localhost:8080
```

### 2. Configure Your Gemini AI Key (Optional but Recommended)
1. Go to the **Settings** tab in the sidebar.
2. Enter your **Google Gemini API Key** and select **Gemini 3.8 Flash** (or **Gemini 3.8 Pro**).
3. Click **Test Key** to verify connectivity, then click **Save Settings**.
*(Note: If no API key is provided, the platform automatically switches to its built-in Intelligent Heuristic Examiner, ensuring full offline functionality!)*

### 3. Recommended Active Workspace
To open this project directly in your IDE workspace, set the workspace directory to:
```
/Users/sadhukhandebjit/.gemini/antigravity/scratch/ielts-gemini-prep
```

---

## 📁 Project Architecture

```
ielts-gemini-prep/
├── backend/
│   ├── server.py          # Python HTTP server & REST API (zero external dependencies)
│   ├── database.py        # SQLite storage (settings, tests, attempts, vocabulary, study logs)
│   ├── analytics.py       # Diagnostic engine, official IELTS rounding, weakness detector
│   ├── gemini_service.py  # Google Gemini REST client & intelligent fallback evaluator
│   └── seed_data.py       # Authentic IELTS practice tests, questions, and model answers
├── frontend/
│   ├── index.html         # Responsive SPA layout with Tailwind CSS & Chart.js
│   ├── app.js             # Client state, Web Speech audio & recognition, interactive timers
│   └── styles.css         # Custom animations, audio visualizer, split-screen layout
├── data/
│   └── ielts_prep.db      # SQLite local database file
├── start.sh               # Quick launch script
└── README.md              # Documentation
```
