# TRAINING-GUIDE.md  
Version: 1.0  
Author: Kay (Taras Khamardiuk)  
Date: 2025-05-28  

---

Overview

This document is a complete, user-centered guide to running AIPOS — the AI Personal Operational System — using ChatGPT and a single configuration file.

AIPOS is not a chatbot. It’s a controlled interface that lets you shape ChatGPT into a predictable, logic-driven assistant for technical tasks like scripting, documentation, and process planning.

No installation is needed. No coding knowledge is required to begin. Once you load AIPOS, the AI behaves exactly how the config says — and nothing more.

---

What You Need

1. A ChatGPT Plus account (GPT-4o model recommended)
2. A prebuilt configuration file (example: aipos-cfg-base-cynical.txt)
3. Any text editor (Notepad, Sublime, VS Code) to open the config file
4. A clean browser or mobile app session with ChatGPT

Optional:
- A GitHub repository or local folder to store your outputs
- A reliable place to keep your configuration files for reuse

Note:
AIPOS is stateless. It does not persist across sessions. You must paste your configuration every time you start a new session.

---

How AIPOS Works (Concept)

Each configuration file (`aipos-cfg-*.txt`) defines:
- What the AI's role is
- What tone and output style it should use
- What types of tasks it can perform
- What behavior is and isn’t allowed
- What commands are available to the user

This allows you to reuse a known “mental state” of the AI across any task, in any session — consistently and on command.

---

Mobile Compatibility

AIPOS is fully usable on mobile devices. All configuration pastes and runtime commands work in both the ChatGPT mobile app and browser. If a large config fails to paste cleanly, break it into two parts and paste them in sequence. Disable formatting features like smart quotes or autocorrect to avoid input errors.

---

Step-by-Step: Using AIPOS

Step 1 — Load the Configuration

1. Open the configuration file in your text editor.
2. Select all content and copy it (from the first line to the last).
3. Paste it into ChatGPT (as a single message).
4. Then type:

aiposrun

ChatGPT will confirm the session is now locked into its AIPOS role.

Step 2 — Tell It What You Want

Immediately after running `aiposrun`, provide a task. This can be:
- A file-related request (e.g., convert data, clean folder, merge reports)
- A script idea or fix you want generated
- A Markdown document you need written
- A plan or checklist you want the AI to build

AIPOS is designed to respond like a command-line automation assistant, not a conversation partner.

Be clear. You don’t need fluff.

Step 3 — Understand the Output Rules

Unless explicitly changed in the config, all AIPOS output will follow strict rules:

- Output is plain text, not styled or rendered
- Responses are copy-paste ready — usable in Git, scripts, terminal, docs
- Each output ends with a standardized footer that includes:
  - Role
  - Tone
  - Date
  - Declared session goal
- There are no summaries, wrap-ups, or “let me know” phrases
- There’s no guessing tone or switching moods mid-stream

This is enforced to keep your outputs professional and repeatable.

---

Available Commands (After aiposrun)

You can use the following commands once AIPOS is running:

buildscript [module]  
→ Creates a Python script block or module for a named task (e.g., buildscript pdfmerger)

makedoc [topic]  
→ Generates a Markdown document on the specified topic (e.g., makedoc project-intro)

generateplan  
→ Produces a modular plan for automating a task or organizing work

aiposvalidate  
→ Checks whether your session is still honoring the original config

aiposrepair  
→ Fixes footer problems or tone drift

aiposfooter  
→ Re-displays the most recent valid session footer for inspection or copying

---

If Things Break (Repair Logic)

If AIPOS stops behaving correctly (becomes too chatty, loses tone, breaks structure), use:

aiposvalidate  
aiposrepair  
aiposfooter  

If that doesn’t work — just re-paste the full config and retype:

aiposrun

This will fully reset the session.

---

Example Session (What Success Looks Like)

User:  
[pastes full config file]

AI:  
Config loaded. Ready for aiposrun.

User:  
aiposrun

AI:  
Session activated.  
Role: Data Automation Engineer  
Tone: Cynical  
Goal: Deliver modular automation workflow

User:  
buildscript csv-cleaner

AI:  
[responds with full Python script as plain text, ending with valid footer]

---

Recommended Folder Structure

You should store your configs and outputs in a clean repo or folder. Example structure:

/aipos-public-eng-main/  
├── README.md  
├── TRAINING-GUIDE.md  
├── NAMING-RULES.md  
├── aipos-cfg-base-cynical.txt  
├── aipos-cfg-data-automation.txt  
├── aipos-command-and-settings-reference.md  
├── aipos-mobile-version-guide.md  
├── aipos-interpreter.txt  
└── aipos-method-card.md  

This makes your logic portable, explainable, and ready for reuse or collaboration.

---

What Not To Do

- Do not paste partial config files — the system will break silently
- Do not use formatting tools in ChatGPT (headers, bullets, markdown toggle)
- Do not manually add summaries or “thank you” lines — it disrupts output clarity
- Do not expect the AI to remember prior context — it doesn’t
- Do not overwrite config tone unless you’ve explicitly planned for it

---

Final Reminder

AIPOS is not here to chat.  
It is a behavioral framework for controlled, predictable, and scalable AI tasking.

You define how it behaves.  
You control what it outputs.  
You reset it when it forgets.  
And you use it when reliability matters.

If it drifts — reload.  
If it works — deploy.
