# 📊 TA-10 – Simulasi Sistem Kaku (Stiff ODE)

**Mata Kuliah:** Pemodelan dan Simulasi / Metode Numerik  
**Topik:** Simulasi Sistem Kaku (Stiff Ordinary Differential Equations)  
**Studi Kasus:** Penyebaran Demam Berdarah Dengue (DBD) – Model SIR  
**Role:** Simulation Engineer / Numerical Analyst  

---

## 🎯 Tujuan Proyek

Proyek ini bertujuan untuk membuktikan secara **empiris dan visual** bahwa:

1. **Metode eksplisit** (Euler, RK4/RK45) **gagal atau tidak efisien** pada sistem kaku  
2. **Stiff solver implisit** (BDF dan Radau) mampu memberikan solusi yang **stabil dan efisien**  
3. Perbedaan performa solver dianalisis melalui:
   - Stabilitas numerik  
   - Waktu komputasi  
   - Jumlah evaluasi fungsi (*number of function evaluations / nfev*)

---

## 🧠 Konsep Sistem Kaku (Stiff System)

Sistem dikatakan **kaku (stiff)** apabila memiliki **lebih dari satu skala waktu** yang sangat berbeda (proses cepat dan lambat berjalan bersamaan).

Pada kondisi ini:
- Metode eksplisit keluar dari *stability region*  
- Langkah waktu harus sangat kecil → komputasi mahal  
- Metode implisit lebih sesuai karena memanfaatkan informasi Jacobian  

---

## 🗂️ Struktur Proyek

```text
TA10_DBD_StiffODE/
├── app.py                  # Aplikasi web (Streamlit – deploy)
├── main.py                 # Eksperimen numerik (tanpa UI)
├── requirements.txt        # Daftar dependensi Python
├── README.md               # Dokumentasi proyek
│
├── data/
│   └── DATA DBD.csv        # Dataset kasus DBD
│
├── src/
│   ├── models.py           # Model SIR (ODE)
│   ├── explicit_solvers.py # Metode Euler eksplisit
│   ├── stiff_solvers.py    # Solver solve_ivp (RK45, BDF, Radau)
│   ├── dataset.py          # Loader & normalisasi data
│   └── visualization.py   # Utilitas plotting
│
└── output/
    └── *.png               # Grafik hasil simulasi

---

## 📊 Output dan Visualisasi
Aplikasi menampilkan:
❌ Grafik kegagalan metode Euler
✅ Grafik perbandingan RK45 vs BDF vs Radau
📈 Perbandingan model SIR dengan data DBD
📋 Tabel kinerja solver yang memuat:
Metode solver
Waktu komputasi
Jumlah evaluasi fungsi (nfev)
Status keberhasilan
Semua visualisasi ditampilkan dalam dashboard simetris dan interaktif.

---

🚀 Cara Menjalankan Program
1️⃣ Membuat Virtual Environment (Opsional tapi Disarankan)
python -m venv venv
Aktifkan virtual environment (Windows):
venv\Scripts\activate
2️⃣ Instalasi Dependensi
pip install -r requirements.txt
3️⃣ Menjalankan Aplikasi Web (Deploy Lokal)
streamlit run app.py
Aplikasi akan terbuka otomatis di browser.

---

🧪 Contoh Parameter Simulasi
Untuk menghasilkan sistem sangat kaku:
β (Transmission Rate) = 5.0
γ (Recovery Rate) = 0.1
Dengan parameter ini:
Metode Euler gagal (tidak stabil)
RK45 sangat mahal secara komputasi
BDF dan Radau bekerja optimal

---

## 📌 Kesimpulan
Sistem penyebaran DBD dapat dimodelkan sebagai ODE kaku
Metode eksplisit tidak cocok untuk sistem kaku
Solver implisit (BDF dan Radau) merupakan pilihan terbaik
Hasil simulasi konsisten dengan teori kestabilan numerik

---

## 👨‍💻 Catatan Akademik
Proyek ini dikembangkan sebagai bagian dari Tugas Akhir 10 (TA-10)
dan disusun sesuai dengan:
Tujuan pembelajaran mata kuliah
Kaidah numerik dan simulasi
Praktik pemrograman ilmiah mahasiswa Informatika Semester 5

---

## 👨‍💻 Disusun oleh:
Nama: Ardi Kamal Karima
NIM: 301230023
Kelas: 5C / Informatika
