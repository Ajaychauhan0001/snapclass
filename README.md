# snapclass
AI-powered attendance system using real-time face recognition and voice authentication to automate and secure attendance tracking.

# 📸 Snap Class — AI & Biometric Attendance System

<div align="center">
  <img src="assets/student_icon.png" width="90" alt="Snap Class Logo" />
  <h3>Smart, automated classroom tracking powered by Multi-Modal Biometrics.</h3>
  
  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://snapclass-branch.streamlit.app/)
  [![Python](https://img.shields.io/badge/Python-3.9+-5865F2.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
  [![Database](https://img.shields.io/badge/Database-Supabase-3ECF8E.svg?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)
  [![UI Customization](https://img.shields.io/badge/UI-Custom_CSS-EB459E.svg?style=flat-square)](src/ui/base_layout.py)
</div>

---

## 🚀 Live Demo

Try the live application deployed on Streamlit Cloud here:
👉 [Snap Class Live App](https://snapclass-branch.streamlit.app/)

---

## 📌 Project Overview

**Snap Class** is an intelligent, multi-modal biometric classroom management and attendance tracking system. Traditional roll calls are slow and error-prone. Snap Class solves this by utilizing **AI-powered facial recognition** and **voice embedding analysis** to capture, identify, and log student attendance instantly.

The system features secure separation between Student and Teacher portals, integrated with a cloud database and lightweight deep learning pipelines optimized for fast execution.

---

## 📊 Application Structure & Portals

The application uses `st.session_state` routing to cleanly divide user flows into two specialized environments:

### Features Used per Portal

| Portal | Feature / Component | Description |
| :--- | :--- | :--- |
| **🧑‍🎓 Student Portal** | **FaceID Login & Registration** | Scan face via web camera to log in or register a new profile with multiple face angles. |
| **🧑‍🎓 Student Portal** | **Voice Enrollment** | Optional voiceprint registration using custom phrase recordings. |
| **🧑‍🎓 Student Portal** | **Course Enrollment** | Fast subject enrollment via custom dialog screens with absolute tracking indicators. |
| **👩‍🏫 Teacher Portal** | **Secure Authentication** | Cryptographically secured credentials utilizing bcrypt password hashing. |
| **👩‍🏫 Teacher Portal** | **🤖 AI Face Analysis** | Select a subject, snap or upload classroom photos, and run high-resolution InsightFace scanning. |
| **👩‍🏫 Teacher Portal** | **🎙️ Voice Attendance** | Run a separate biometric voice-check for bulk processing or fallback validation. |
| **👩‍🏫 Teacher Portal** | **📊 Interactive Records** | Deep data aggregation displaying localized timelines and real-time present/total ratios. |

---

## 🛠️ Technologies & AI Pipelines Used

* **Streamlit Framework**: Drives page conditional logic, dialog modules (`st.dialog`), and instant application re-runs.
* **InsightFace (`buffalo_l`)**: Core computer vision model running face detection and generating 512-dimensional normalized embeddings over a high-resolution scanning canvas (`1280x1280`).
* **Resemblyzer & Librosa**: Drives voice feature extraction, signal splitting, and voice-print embedding comparison via audio arrays.
* **Supabase**: Serves as the cloud database engine managing relational records for logins, enrollment links, and raw float vectors.
* **Bcrypt**: Encrypts and validates teacher administrative profiles securely.

---
🌐 Database Relational Map
The system maps data seamlessly inside Supabase Storage Engine across 4 fundamental sheets:

🗃️ teachers: Stores encrypted identification data (username, password, name).

🗃️ students: Stores identification maps alongside high-dimensional embedding metrics (face_embedding, voice_embedding).

🗃️ subjects: Tracks assigned subjects referencing specific teacher identities.

🗃️ attendance_logs: Chronologically maps structural output data (student_id, subject_id, timestamp, is_present).

snapclass/
│
├── assets/                  # Main UI graphical vector icon elements
│   ├── student_icon.png
│   └── teacher_icon.png
│
├── src/
│   ├── components/          # Structural dialog UI blocks (add_photo, enroll_dialog)
│   ├── database/            # Backend architecture config & query utilities (db.py, config.py)
│   ├── pipelines/           # AI Core processing centers (face_pipeline.py, voice_pipeline.py)
│   ├── screen/              # Interface layout state managers (home_screen.py, student_screen.py)
│   └── ui/                  # Dynamic structural template configurations (base_layout.py)
│
├── app.py                   # Global execution entry point file
├── requirements.txt         # Package ecosystem setup requirements
└── README.md                # Structural project description manual

🎯 Future Improvements
🤖 Edge Processing: Compress model weights to support native client-side calculations directly over cell phone browsers.

📈 Advanced Analytics Dashboards: Build interactive Pandas charts tracking long-term student attendance patterns and class skip metrics.

⚡ Real-Time Video Streams: Switch from flat image uploads to live continuous WebRTC stream processing for instant roll calls.

📚 Key Learnings
Through building Snap Class, I mastered:

Relational database engineering involving large multidimensional array objects (float8[]).

Dynamic state routing across deep multi-nested component flows using Streamlit hooks.

Multi-modal feature processing combining voice audio frames and computer vision embeddings.

Overriding default presentation behaviors using low-level target injection scripts to protect usability across all themes.

👨‍💻 Author
Ajay Chauhan — Developed with passion using Python, Biometric ML Systems, and Custom Streamlit Architecture.
