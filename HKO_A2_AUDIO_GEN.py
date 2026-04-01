#!/usr/bin/env python3
"""
HKO ESL Generator 2030 — Piper TTS Audio Generator
Generates all audio for A2 HR English L01-L12

Usage:
  python3 HKO_A2_AUDIO_GEN.py [lesson_id]   # e.g. python3 HKO_A2_AUDIO_GEN.py L01
  python3 HKO_A2_AUDIO_GEN.py all           # generate all lessons

Requirements:
  pip install piper-tts pathvalidate
  # Download models:
  # Female: en_US-lessac-medium.onnx  (María, narration)
  # Male:   en_US-ryan-medium.onnx    (Carlos, interviewer)
"""

import subprocess, os, sys, json, base64

# ── CONFIGURATION ────────────────────────────────────────────
MODELS_DIR = "./tts_models"
MODEL_F = f"{MODELS_DIR}/en_US-lessac-medium.onnx"   # female
MODEL_M = f"{MODELS_DIR}/en_US-ryan-medium.onnx"      # male

OUT_BASE = "./audio"
os.makedirs(OUT_BASE, exist_ok=True)

# ── LESSON DATA ──────────────────────────────────────────────
LESSONS = {

"L01": {
    "title": "I Started in HR Five Years Ago",
    "character_f": "María López",
    "character_m": "Carlos",
    "story": """Hello. My name is María López. I work in Human Resources.
I am an HR Coordinator at MineSafe Company in Santiago.
But I did not always work in this role. Let me tell you my story.
I graduated from university in 2018. I studied Psychology.
After I graduated, I applied for several HR positions.
I received five interview invitations. I attended all of them.
MineSafe offered me a job as an HR Assistant. I started in July 2018.
I worked in that role for two years.
In 2020, I joined the recruitment team.
My manager asked me if I wanted to change roles. I said yes, immediately.
I worked as a recruiter for three years.
Last year, I moved to the HR Coordinator role.
I now supervise three recruiters. I also manage our applicant tracking system.
I love my job!""",
    "words": {
        "started":   "I started as an HR Assistant.",
        "graduated": "She graduated from university in 2018.",
        "applied":   "He applied for three positions.",
        "received":  "We received fifty applications.",
        "changed":   "I changed to a recruiter role.",
        "joined":    "She joined the HR team in March.",
        "worked":    "I worked there for two years.",
        "moved":     "I moved to coordinator last year.",
        "asked":     "She asked for an application form.",
        "finished":  "We finished the interview process.",
    },
    "dialogue": [
        ("c", "Hi! Are you new to the HR team?"),
        ("m", "No, I started here five years ago. I graduated in 2018 and applied right away!"),
        ("c", "How did you get the job?"),
        ("m", "I received an invitation. I worked as an assistant first, then joined the recruitment team."),
        ("c", "Did you always want to work in HR?"),
        ("m", "Yes! I changed roles several times, then moved to coordinator last year."),
    ],
},

"L02": {
    "title": "We Received 200 Applications",
    "character_f": "Ana Torres",
    "character_m": "Diego",
    "story": """Hello. My name is Ana Torres. I work in Talent Acquisition at MineSafe.
Last month was very busy. We received over two hundred applications for one position.
I read every CV carefully. I chose the best candidates.
I wrote emails to thirty people. I invited them for interviews.
I spoke to each candidate for thirty minutes.
I took notes during the interviews.
I gave my recommendations to the manager.
We made an offer to the best candidate. She accepted immediately.
It was a great result. I felt very satisfied.""",
    "words": {
        "received":  "We received two hundred applications.",
        "chose":     "I chose the best candidates.",
        "wrote":     "I wrote emails to the candidates.",
        "spoke":     "I spoke to each candidate.",
        "took":      "I took notes during the interviews.",
        "gave":      "I gave my recommendations to the manager.",
        "made":      "We made an offer to the candidate.",
        "felt":      "I felt very satisfied with the result.",
        "read":      "I read every CV carefully.",
        "accepted":  "She accepted the offer immediately.",
    },
    "dialogue": [
        ("c", "How many applications did you receive?"),
        ("m", "We received over two hundred! I read every single one."),
        ("c", "How did you choose the candidates?"),
        ("m", "I chose based on experience and skills. Then I wrote invitation emails."),
        ("c", "Did many people accept the interview?"),
        ("m", "Yes, I spoke to thirty people. We made an offer and she accepted."),
    ],
},

"L03": {
    "title": "She Has Worked Here for Three Years",
    "character_f": "Valentina",
    "character_m": "Marco",
    "story": """Good morning. My name is Valentina Cruz. I am the HR Manager at MineSafe.
I have worked here for three years. I have learned a lot in that time.
I have hired over fifty people since I joined.
I have also developed our onboarding programme.
My team has grown from two people to six people.
We have improved our recruitment process significantly.
I have attended many conferences about HR technology.
I have not always found the work easy. But I have never wanted to leave.
I love building teams. I have always believed in the people I hire.""",
    "words": {
        "worked":    "She has worked here for three years.",
        "learned":   "I have learned a lot in this role.",
        "hired":     "I have hired over fifty people.",
        "developed": "We have developed a new programme.",
        "grown":     "The team has grown significantly.",
        "improved":  "We have improved the process.",
        "attended":  "I have attended many conferences.",
        "believed":  "I have always believed in my team.",
        "joined":    "I have worked here since I joined.",
        "found":     "I have not always found the work easy.",
    },
    "dialogue": [
        ("c", "How long have you worked in HR?"),
        ("m", "I have worked in HR for six years. Three of them here at MineSafe."),
        ("c", "What have you achieved in that time?"),
        ("m", "I have hired fifty people and developed our onboarding programme."),
        ("c", "Has the team grown?"),
        ("m", "Yes! We have grown from two to six people. I am very proud of that."),
    ],
},

"L04": {
    "title": "The Interview Will Be on Monday",
    "character_f": "Lucía",
    "character_m": "Felipe",
    "story": """Hello. My name is Lucía Gómez. I applied for a new position last week.
The recruiter called me yesterday. She said the interview will be on Monday.
I am going to prepare very carefully this weekend.
I will research the company before the interview.
I am going to practice common interview questions.
I will wear professional clothes. I will arrive fifteen minutes early.
I am going to bring copies of my CV and portfolio.
I will speak clearly and confidently.
After the interview, I will send a thank-you email.
I hope I will get the job. I am very excited!""",
    "words": {
        "will be":    "The interview will be on Monday.",
        "going to":   "I am going to prepare this weekend.",
        "will research": "I will research the company.",
        "will practice": "I will practice interview questions.",
        "will wear":  "I will wear professional clothes.",
        "will arrive": "I will arrive fifteen minutes early.",
        "will bring":  "I will bring copies of my CV.",
        "will speak":  "I will speak clearly and confidently.",
        "will send":   "I will send a thank-you email.",
        "will get":    "I hope I will get the job.",
    },
    "dialogue": [
        ("c", "When is your interview?"),
        ("m", "The interview will be on Monday at ten o'clock."),
        ("c", "Are you going to prepare?"),
        ("m", "Yes! I am going to research the company and practice my answers."),
        ("c", "What will you wear?"),
        ("m", "I will wear a suit. I always dress professionally for interviews."),
    ],
},

"L05": {
    "title": "If You Apply Now, We Will Review It",
    "character_f": "Sofía",
    "character_m": "Andrés",
    "story": """Hello. My name is Sofía Ramírez. I work in the HR department at MineSafe.
I often speak to candidates about the application process.
I always tell them: if you apply before the deadline, we will review your application.
If your CV is strong, we will invite you for an interview.
If you attend the interview, you will meet our team.
If you get the job, you will start a great career.
But if you miss the deadline, we cannot consider your application.
If you need help with your CV, we can offer advice.
If you have questions, please send me an email.
I am always happy to help candidates succeed.""",
    "words": {
        "apply":     "If you apply now, we will review it.",
        "attend":    "If you attend the interview, you will meet the team.",
        "get":       "If you get the job, you will start a great career.",
        "miss":      "If you miss the deadline, we cannot consider you.",
        "need":      "If you need help, we can offer advice.",
        "send":      "If you send your CV, I will review it.",
        "pass":      "If you pass the interview, we will make an offer.",
        "accept":    "If you accept the offer, you will start next month.",
        "prepare":   "If you prepare well, you will feel confident.",
        "arrive":    "If you arrive early, you will have time to relax.",
    },
    "dialogue": [
        ("c", "What happens if I apply today?"),
        ("m", "If you apply today, I will review your application tomorrow."),
        ("c", "And if my CV is good?"),
        ("m", "If your CV is strong, we will invite you for an interview."),
        ("c", "What if I miss the deadline?"),
        ("m", "If you miss the deadline, we cannot consider your application. So apply now!"),
    ],
},

"L06": {
    "title": "He Was Promoted Last Quarter",
    "character_f": "Carmen",
    "character_m": "Rodrigo",
    "story": """Good afternoon. My name is Carmen López. I am the HR Director at MineSafe.
Last quarter was very positive for our team.
Several employees were promoted. Three people were given new responsibilities.
A new training programme was created. Fifty employees were enrolled.
The new HR system was installed by our IT team.
All contracts were updated by the legal department.
New salary bands were approved by the board.
Performance reviews were completed by all managers.
I am proud of everything that was achieved this quarter.
Next quarter, more improvements will be introduced.""",
    "words": {
        "promoted":   "He was promoted last quarter.",
        "given":      "They were given new responsibilities.",
        "created":    "A programme was created for training.",
        "enrolled":   "Fifty people were enrolled.",
        "installed":  "The new system was installed.",
        "updated":    "All contracts were updated.",
        "approved":   "The new bands were approved.",
        "completed":  "Reviews were completed by all managers.",
        "achieved":   "A lot was achieved this quarter.",
        "introduced": "New systems will be introduced.",
    },
    "dialogue": [
        ("c", "Was anyone promoted this quarter?"),
        ("m", "Yes! Three people were promoted. It was a great quarter."),
        ("c", "Was the new system installed?"),
        ("m", "Yes, it was installed by the IT team last month."),
        ("c", "Were the contracts updated?"),
        ("m", "Yes, all contracts were updated by the legal department."),
    ],
},

"L07": {
    "title": "We Need Someone Who Can Lead",
    "character_f": "Isabella",
    "character_m": "Tomás",
    "story": """Hello. My name is Isabella Chen. I manage recruitment at MineSafe.
We are currently looking for a new manager. We need someone who can lead a team.
The ideal candidate is a person who has strong communication skills.
We need a manager who understands HR processes.
We want someone who can solve problems quickly.
The role requires a person who is organised and detail-focused.
We are looking for someone who has experience in mining or industry.
The candidate who gets this role will manage a team of ten people.
If you know someone who would be perfect, please send us their CV.
The position which interests us most is an HR Business Partner.""",
    "words": {
        "who":      "We need someone who can lead a team.",
        "which":    "The position which interests us is open.",
        "that":     "The candidate that we hire must be organised.",
        "leads":    "We need a person who leads effectively.",
        "understands": "We want someone who understands HR.",
        "manages":  "The manager who manages our team must be strong.",
        "solves":   "We need someone who solves problems.",
        "has":      "We need a candidate who has experience.",
        "knows":    "Someone who knows the industry is ideal.",
        "can":      "We need a person who can communicate well.",
    },
    "dialogue": [
        ("c", "What kind of person are you looking for?"),
        ("m", "We need someone who can lead a team of ten people."),
        ("c", "What skills does the person need?"),
        ("m", "We want someone who has strong HR experience and who can solve problems."),
        ("c", "Is there a specific background that is important?"),
        ("m", "Yes, the candidate who gets this role should know the mining industry."),
    ],
},

"L08": {
    "title": "She Should Have Sent the Report",
    "character_f": "Natalia",
    "character_m": "Javier",
    "story": """Good morning. My name is Natalia Rivas. I am an HR Business Partner.
Yesterday, there was a problem with a performance review.
The manager should have sent the report by Friday. But he did not send it.
He should have communicated the delay to the team. He did not do that either.
The employee should have received feedback before the meeting. She did not.
I think the manager could have handled this better.
He should have prepared the report in advance.
We should have had a clearer process. That was our mistake too.
Next time, all managers must complete reports on time.
We should have learned from this earlier. But it is not too late to improve.""",
    "words": {
        "should have sent":        "She should have sent the report on Friday.",
        "should have communicated": "He should have communicated the delay.",
        "should have received":    "She should have received feedback.",
        "could have handled":      "He could have handled this better.",
        "should have prepared":    "He should have prepared in advance.",
        "should have had":         "We should have had a clearer process.",
        "should have learned":     "We should have learned this earlier.",
        "must complete":           "Managers must complete reports on time.",
        "could have improved":     "We could have improved the process.",
        "should not have":         "He should not have missed the deadline.",
    },
    "dialogue": [
        ("c", "What happened with the report?"),
        ("m", "The manager should have sent it on Friday. But he forgot."),
        ("c", "What should he have done?"),
        ("m", "He should have communicated the delay immediately."),
        ("c", "How could this have been avoided?"),
        ("m", "We could have had a clearer reminder system. We should have done that earlier."),
    ],
},

"L09": {
    "title": "Please Find Attached My CV",
    "character_f": "Paola",
    "character_m": "Sebastián",
    "story": """Good morning. My name is Paola Vargas. I am writing to apply for the position.
Please find attached my CV and cover letter.
I am writing to express my interest in the HR Coordinator role.
I have three years of experience in Human Resources.
I believe I would be an excellent fit for your team.
I have attached all the documents you requested.
Please do not hesitate to contact me if you need further information.
I look forward to hearing from you.
I am available for an interview at your convenience.
Thank you for considering my application.
Best regards, Paola Vargas.""",
    "words": {
        "attached":       "Please find attached my CV.",
        "writing":        "I am writing to apply for the position.",
        "express":        "I write to express my interest.",
        "believe":        "I believe I would be a good fit.",
        "attached (2)":   "I have attached all the documents.",
        "hesitate":       "Please do not hesitate to contact me.",
        "forward":        "I look forward to hearing from you.",
        "available":      "I am available for an interview.",
        "considering":    "Thank you for considering my application.",
        "regarding":      "I am writing regarding the HR position.",
    },
    "dialogue": [
        ("c", "Did you receive her application?"),
        ("m", "Yes, she wrote that she is applying for the coordinator role."),
        ("c", "Did she attach her CV?"),
        ("m", "Yes, she said: please find attached my CV and cover letter."),
        ("c", "When is she available?"),
        ("m", "She wrote that she is available at our convenience."),
    ],
},

"L10": {
    "title": "The Meeting Has Been Cancelled",
    "character_f": "Daniela",
    "character_m": "Mateo",
    "story": """Hello everyone. My name is Daniela Mora. I work in HR Operations.
I need to share some important updates about this week.
The team meeting has been cancelled due to a scheduling conflict.
A new date has been proposed for next Tuesday.
The training session has been postponed to the following week.
The HR software update has been completed successfully.
All employee contracts have been reviewed and signed.
Three new positions have been advertised on our careers page.
The onboarding programme has been updated with new materials.
All changes have been communicated to the team.
Please confirm you have received this message. Thank you.""",
    "words": {
        "cancelled":   "The meeting has been cancelled.",
        "proposed":    "A new date has been proposed.",
        "postponed":   "The session has been postponed.",
        "completed":   "The update has been completed.",
        "reviewed":    "All contracts have been reviewed.",
        "advertised":  "New positions have been advertised.",
        "updated":     "The programme has been updated.",
        "communicated": "Changes have been communicated.",
        "confirmed":   "The date has been confirmed.",
        "approved":    "The budget has been approved.",
    },
    "dialogue": [
        ("c", "Has the meeting been cancelled?"),
        ("m", "Yes, it has been cancelled. A new date has been proposed."),
        ("c", "Has the training been rescheduled?"),
        ("m", "Yes, it has been postponed to next week."),
        ("c", "Have the new positions been advertised?"),
        ("m", "Yes, three new roles have been advertised on our careers page."),
    ],
},

"L11": {
    "title": "I'd Like to Discuss Your Performance",
    "character_f": "Alejandra",
    "character_m": "Ricardo",
    "story": """Good afternoon. My name is Alejandra Ríos. I manage a team at MineSafe.
I would like to talk about our performance review process.
Could you explain your goals for this quarter?
I would like to understand your priorities better.
Could we schedule a meeting for next week?
I would appreciate your feedback on the new system.
Could you send me your self-assessment before Friday?
I would like to discuss some areas for improvement.
Could you work on your communication skills?
I would recommend attending the leadership workshop.
I would like to support your career development. That is important to me.""",
    "words": {
        "would like":    "I would like to discuss your performance.",
        "could you":     "Could you explain your goals?",
        "would appreciate": "I would appreciate your feedback.",
        "could we":      "Could we schedule a meeting?",
        "would recommend": "I would recommend the workshop.",
        "would like to": "I would like to support you.",
        "could work":    "Could you work on your skills?",
        "would suggest": "I would suggest a different approach.",
        "could attend":  "You could attend the leadership course.",
        "would understand": "I would like to understand better.",
    },
    "dialogue": [
        ("c", "I would like to discuss your progress. How do you feel about your work?"),
        ("m", "I think I have improved a lot. Could you give me specific feedback?"),
        ("c", "I would appreciate that question. You have grown significantly."),
        ("m", "Could we set some new goals for next quarter?"),
        ("c", "Absolutely. I would like to support your development. Let us schedule a meeting."),
        ("m", "Could we meet on Thursday? I would prefer the morning."),
    ],
},

"L12": {
    "title": "We've Been Working on This for Months",
    "character_f": "Mariana",
    "character_m": "Eduardo",
    "story": """Hello. My name is Mariana Fuentes. I lead the HR Transformation project.
We have been working on this project for six months.
Our team has been developing a new digital HR platform.
We have been testing the system since January.
The employees have been providing feedback throughout the process.
Some departments have been using the new tools for two months.
I have been presenting progress reports every week.
The IT team has been fixing bugs and improving performance.
We have been planning the full launch for next month.
Everyone has been working very hard. I am proud of our progress.
Soon, all employees will be using the new system. We cannot wait!""",
    "words": {
        "have been working":     "We have been working on this for months.",
        "has been developing":   "The team has been developing the platform.",
        "have been testing":     "We have been testing since January.",
        "have been providing":   "Employees have been providing feedback.",
        "have been using":       "Some teams have been using the new tools.",
        "have been presenting":  "I have been presenting progress reports.",
        "has been fixing":       "IT has been fixing bugs.",
        "have been planning":    "We have been planning the launch.",
        "has been growing":      "The team has been growing steadily.",
        "have been improving":   "We have been improving the process.",
    },
    "dialogue": [
        ("c", "How long have you been working on this project?"),
        ("m", "We have been working on it for six months. It has been challenging."),
        ("c", "Has the team been testing the system?"),
        ("m", "Yes, we have been testing since January. Employees have been giving feedback."),
        ("c", "Have you been planning the launch?"),
        ("m", "Yes! We have been planning it for two months. We launch next month!"),
    ],
},

}  # end LESSONS


# ── GENERATE FUNCTION ────────────────────────────────────────
def gen_wav(text: str, out_path: str, model: str) -> bool:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result = subprocess.run(
        ["piper", "--model", model, "--output_file", out_path],
        input=text.encode("utf-8"),
        capture_output=True
    )
    if result.returncode != 0:
        print(f"  ✗ FAILED: {out_path}\n    {result.stderr.decode()[:120]}")
        return False
    return True


def generate_lesson(lid: str, data: dict) -> dict:
    out_dir = f"{OUT_BASE}/{lid}"
    os.makedirs(out_dir, exist_ok=True)
    generated = {}
    ok = 0; total = 0

    print(f"\n── {lid}: {data['title']} ──")

    # Story (female voice)
    key = "story_maria"
    path = f"{out_dir}/{key}.wav"
    total += 1
    if gen_wav(data["story"], path, MODEL_F):
        ok += 1
        with open(path, "rb") as f:
            generated[key] = f"data:audio/wav;base64,{base64.b64encode(f.read()).decode()}"
        print(f"  ✓ {key}")

    # Words + context sentences (female voice — slow, clear)
    for word, ctx_sentence in data["words"].items():
        # Isolated word
        wkey = f"word_{word.replace(' ', '_')}"
        wpath = f"{out_dir}/{wkey}.wav"
        total += 1
        if gen_wav(word, wpath, MODEL_F):
            ok += 1
            with open(wpath, "rb") as f:
                generated[wkey] = f"data:audio/wav;base64,{base64.b64encode(f.read()).decode()}"

        # Context sentence
        ckey = f"ctx_{word.replace(' ', '_')}"
        cpath = f"{out_dir}/{ckey}.wav"
        total += 1
        if gen_wav(ctx_sentence, cpath, MODEL_F):
            ok += 1
            with open(cpath, "rb") as f:
                generated[ckey] = f"data:audio/wav;base64,{base64.b64encode(f.read()).decode()}"

    # Dialogue (alternate voices by speaker)
    for i, (speaker, line) in enumerate(data["dialogue"], 1):
        dkey = f"dlg_{speaker}{i}"
        dpath = f"{out_dir}/{dkey}.wav"
        model = MODEL_M if speaker == "c" else MODEL_F
        total += 1
        if gen_wav(line, dpath, model):
            ok += 1
            with open(dpath, "rb") as f:
                generated[dkey] = f"data:audio/wav;base64,{base64.b64encode(f.read()).decode()}"

    print(f"  Result: {ok}/{total} files generated")
    return generated


def save_manifest(lid: str, audio_data: dict):
    """Save audio data as JSON for embedding into HTML lesson"""
    out = f"{OUT_BASE}/{lid}/audio_manifest.json"
    with open(out, "w") as f:
        json.dump(audio_data, f)
    size = os.path.getsize(out) // 1024
    print(f"  Manifest: {out} ({size}kb)")


# ── MAIN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "L01"

    if not os.path.exists(MODEL_F):
        print(f"ERROR: Female voice model not found: {MODEL_F}")
        print("Download from: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_US/lessac/medium")
        sys.exit(1)

    if target.upper() == "ALL":
        for lid, data in LESSONS.items():
            audio_data = generate_lesson(lid, data)
            save_manifest(lid, audio_data)
    elif target.upper() in LESSONS:
        lid = target.upper()
        audio_data = generate_lesson(lid, LESSONS[lid])
        save_manifest(lid, audio_data)
    else:
        print(f"Unknown lesson: {target}")
        print(f"Available: {', '.join(LESSONS.keys())} or 'all'")
        sys.exit(1)

    print("\n✓ Audio generation complete.")
    print("  Use audio_manifest.json to embed audio in HTML lessons.")
