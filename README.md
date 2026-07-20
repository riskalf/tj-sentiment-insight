# 🚌 TJ Sentiment Insight

**TJ Sentiment Insight** merupakan prototipe aplikasi berbasis web untuk menganalisis sentimen ulasan pengguna aplikasi **TJ: Transjakarta** di Google Play Store. Aplikasi ini menggunakan model **IndoBERT** hasil *fine-tuning* untuk melakukan klasifikasi sentimen, serta dilengkapi dengan deteksi tema keluhan berbasis *keyword matching*.

Prototipe ini dikembangkan sebagai implementasi tahap **Deployment** pada penelitian skripsi Program Studi Sains Data.

---

## ✨ Fitur

- Analisis sentimen ulasan (positif atau negatif) menggunakan model IndoBERT.
- Deteksi tema keluhan secara otomatis untuk ulasan yang diprediksi negatif.
- Menampilkan hasil preprocessing teks.
- Menampilkan perbandingan antara rating pengguna dan hasil prediksi model.
- Antarmuka interaktif menggunakan Streamlit.

---

## 📄 Halaman Aplikasi

### 🏠 Beranda
Menampilkan ringkasan penelitian, metrik model, statistik data, dan alur penelitian berdasarkan CRISP-DM.

### 🔎 Analisis Sentimen
Halaman utama untuk melakukan analisis sentimen. Pengguna dapat memasukkan teks ulasan dan memperoleh hasil prediksi sentimen beserta tema keluhan yang terdeteksi.

### ℹ️ Tentang Proyek
Berisi metodologi penelitian, perbandingan model SVM dan IndoBERT, kategori tema keluhan, serta batasan penelitian.

---

## 📁 Struktur Proyek

```text
tj-sentiment-insight/
├── app.py
├── requirements.txt
├── assets/
│   └── style.css
├── data/
│   └── kamuskatabaku.xlsx
├── pages/
│   ├── 1_Analisis_Sentimen.py
│   └── 2_Tentang_Proyek.py
└── utils/
    ├── model.py
    ├── preprocessing.py
    ├── theme_classifier.py
    └── ui.py
```

---

## 🤖 Model

Model klasifikasi sentimen menggunakan **IndoBERT** yang telah melalui proses *fine-tuning* pada data ulasan aplikasi TJ: Transjakarta.

Model disimpan pada Hugging Face Model Hub dan dimuat secara otomatis oleh aplikasi saat digunakan.

---

## 📊 Dataset

- Sumber data: Google Play Store
- Objek penelitian: Aplikasi **TJ: Transjakarta**
- Jumlah data: 2.000 ulasan
- Klasifikasi sentimen: Positif dan Negatif

---

## 🚀 Menjalankan Aplikasi

Clone repository ini kemudian jalankan perintah berikut.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Aplikasi akan berjalan pada:

```
http://localhost:8501
```

---

## ⚠️ Batasan

- Klasifikasi sentimen hanya terdiri dari dua kelas, yaitu positif dan negatif.
- Ulasan dengan rating 3 (netral) tidak digunakan dalam proses pelatihan model.
- Deteksi tema keluhan menggunakan metode *keyword matching* (*rule-based*), bukan model klasifikasi terpisah.
- Prototipe ini dikembangkan sebagai media demonstrasi hasil penelitian dan tidak terhubung dengan sistem operasional resmi TJ: Transjakarta.

---

## 👩‍🎓 Penulis

**Riska Alifia Putri**  
NIM 15210004  
Program Studi Sains Data  
Universitas Nusa Mandiri  
2026
