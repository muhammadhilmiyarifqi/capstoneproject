# EduTrack AI - DBS Coding Camp Capstone Project
absen
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
---
- **Web App (React/Vite)**: [https://edutrack-khaki-sigma.vercel.app/](https://edutrack-khaki-sigma.vercel.app/)
- **Streamlit Dashboard**: [https://edutrack-dashboard-capstone.streamlit.app/](https://edutrack-dashboard-capstone.streamlit.app/)

---

## 📊 Streamlit Dashboard

Dashboard interaktif yang menyajikan visualisasi data performa belajar siswa. **[https://edutrack-dashboard-capstone.streamlit.app/](https://edutrack-dashboard-capstone.streamlit.app/)**

### 💻 Cara Menjalankan Secara Lokal

1. Pastikan library yang diperlukan sudah terinstall:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan server Streamlit:
   ```bash
   streamlit run dashboard.py
   ```
3. Buka browser pada alamat `http://localhost:8501`.

### 🚀 Cara Mendeploy ke Streamlit Cloud

Untuk mempublikasikan dashboard agar dapat diakses oleh publik secara gratis menggunakan **Streamlit Community Cloud**:

1. **Push Perubahan Ke GitHub**:
   Pastikan file `dashboard.py` dan `requirements.txt` yang baru dibuat di root direktori sudah di-commit dan di-push ke repository GitHub Anda:
   ```bash
   git add requirements.txt README.md
   git commit -m "Add requirements.txt and deployment guides for Streamlit"
   git push origin main
   ```

2. **Daftar / Login ke Streamlit Cloud**:
   - Kunjungi [Streamlit Community Cloud](https://share.streamlit.io/).
   - Login menggunakan akun **GitHub** Anda yang terhubung dengan repository proyek ini.

3. **Deploy Aplikasi Baru**:
   - Klik tombol **"Create app"** atau **"New app"** di pojok kanan atas dashboard Streamlit.
   - Isi form konfigurasi sebagai berikut:
     - **Repository**: Pilih repository GitHub capstone proyek ini (misalnya: `muhammadhilmiyarifqi/capstoneproject`).
     - **Branch**: Pilih branch utama (biasanya `main` atau `master`).
     - **Main file path**: Isi dengan `dashboard.py` (karena file dashboard berada di root direktori).
   - Klik **"Deploy!"**.

4. **Tunggu Proses Build**:
   Streamlit Cloud akan otomatis membaca file `requirements.txt`, menginstall dependensi, dan meluncurkan dashboard Anda. Setelah selesai, Anda akan mendapatkan tautan publik gratis untuk dashboard Anda!

