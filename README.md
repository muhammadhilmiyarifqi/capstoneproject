# EduTrack AI - DBS Coding Camp Capstone Project

EduTrack AI adalah platform berbasis web yang mengintegrasikan Artificial Intelligence (AI) untuk menganalisis, memprediksi, dan memberikan rekomendasi terkait performa akademik siswa. Proyek ini dikembangkan sebagai **Capstone Project** untuk **DBS Coding Camp**.

## 🌟 Fitur Utama

- **Prediksi Performa Akademik**: Menggunakan model Deep Learning (TensorFlow) untuk memprediksi performa siswa berdasarkan fitur-fitur seperti jam belajar, tingkat keterlibatan (engagement), dll.
- **Rekomendasi Berbasis Model AI**: Memberikan saran skenario ("What if?") dan rekomendasi personal bagi siswa/pengguna.
- **Autentikasi Pengguna**: Sistem login dan registrasi menggunakan RESTful API yang aman dengan penyimpanan database PostgreSQL.
- **Dashboard Interaktif**: Antarmuka pengguna (UI) modern dan responsif yang dibangun menggunakan React, Vite, dan Tailwind CSS.
- **Inference Server**: Web server menggunakan FastAPI untuk mengeksekusi model Deep Learning secara efisien.

---

## 🛠️ Tech Stack

### 🎨 Front-End
- **Framework**: React.js (menggunakan Vite)
- **Styling**: Tailwind CSS & DaisyUI
- **HTTP Client**: Axios

### ⚙️ Back-End
- **Framework**: Node.js dengan Express.js
- **Database**: PostgreSQL
- **Architecture**: RESTful API

### 🤖 Artificial Intelligence
- **Framework ML**: TensorFlow / Keras (Functional API / Subclassing)
- **Inference Server**: FastAPI (Python)
- **Generative AI**: Google Gemini API

### 📊 Data Science
- **Environment**: Jupyter Notebook
- **Tasks**: Data Wrangling, Exploratory Data Analysis (EDA), Feature Engineering

---

## 📂 Struktur Proyek

```text
CAPSTONE/
├── AI/                     # Model ML, Skrip Pelatihan, dan Server FastAPI (Python)
├── datascience/            # Notebook (.ipynb) untuk analisis data dan Data Dictionary
├── fullstack/
│   ├── backend/            # Express.js REST API & Integrasi Database
│   └── frontend/           # Aplikasi Web berbasis React.js
└── student_performance_dataset.csv # Dataset utama performa siswa
```
