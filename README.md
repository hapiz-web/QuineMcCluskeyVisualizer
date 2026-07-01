# Visualisasi Algoritma Quine-McCluskey

Aplikasi web berbasis Django untuk memvisualisasikan proses penyederhanaan ekspresi Boolean menggunakan algoritma Quine-McCluskey secara interaktif. Aplikasi ini membantu pengguna memahami langkah-langkah penyederhanaan dari input awal hingga ekspresi akhir dengan tampilan yang modern dan edukatif.

## Deskripsi

Proyek ini dikembangkan sebagai media pembelajaran untuk memahami algoritma Quine-McCluskey secara lebih intuitif. Selain menampilkan hasil akhir, aplikasi ini juga menunjukkan proses yang terjadi di setiap tahapan, seperti pengelompokan, kombinasi, prime implicant, essential prime implicant, metode Petrick, serta ekspresi Boolean akhir.

## Screenshot

> Placeholder screenshot
>
> Tambahkan tangkapan layar aplikasi ke folder docs/ untuk memperjelas tampilan antarmuka.

![Placeholder Screenshot](docs/screenshot.png)

## Fitur

- Visualisasi langkah demi langkah algoritma Quine-McCluskey
- Tampilan pengelompokan awal minterm
- Visualisasi iterasi kombinasi
- Tabel dan diagram prime implicant
- Identifikasi essential prime implicant
- Tahapan metode Petrick
- Tampilan hasil ekspresi Boolean akhir
- Validasi input untuk duplikat, overlap, dan nilai di luar rentang
- Antarmuka responsif berbasis Bootstrap 5
- Riwayat perhitungan dengan fitur lihat dan hapus
- Panel statistik hasil komputasi

## Cara Instalasi

1. Clone repository:
   ```bash
   git clone <repository-url>
   cd project
   ```

2. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan migrasi database:
   ```bash
   python manage.py migrate
   ```

## Cara Menjalankan

Jalankan server pengembangan:

```bash
python manage.py runserver
```

Buka browser di alamat berikut:

```text
http://127.0.0.1:8000/
```

## Struktur Folder

```text
project/
├── qm/                  # Aplikasi Django utama untuk form, view, dan integrasi logika
├── quinemccluskey/      # Konfigurasi proyek dan routing utama
├── templates/           # Template HTML untuk halaman home, about, history, dan detail
├── static/              # File CSS, JavaScript, dan aset visual
├── docs/                # Dokumentasi proyek
├── media/               # Direktori media aplikasi
├── db.sqlite3           # Database SQLite
└── manage.py            # Script manajemen Django
```

## Workflow Algoritma

Aplikasi ini mengikuti workflow berikut:

1. Menerima dan memvalidasi input pengguna
2. Mengelompokkan minterm berdasarkan jumlah bit 1 dalam bentuk biner
3. Menggabungkan suku yang kompatibel secara berulang
4. Menghasilkan prime implicant
5. Membangun prime implicant chart
6. Menentukan essential prime implicant
7. Menerapkan metode Petrick bila diperlukan
8. Menghasilkan ekspresi Boolean akhir yang tersederhana

## Teknologi

- Python
- Django
- Bootstrap 5
- SQLite
- HTML
- CSS
- JavaScript

## Cara Penggunaan

1. Buka halaman utama aplikasi.
2. Masukkan jumlah variabel, minterm, dan don't care.
3. Klik tombol untuk memulai proses penyederhanaan.
4. Lihat hasil visualisasi langkah demi langkah yang ditampilkan.
5. Buka halaman riwayat untuk melihat hasil perhitungan sebelumnya.

## Contoh Input

Contoh sederhana:

```text
Jumlah Variabel: 4
Minterm: 0,1,2,5,7,8
Don't Care: 3,4
```

Contoh kompleks:

```text
Jumlah Variabel: 4
Minterm: 0,1,2,5,6,7,8,9,10,14
Don't Care: -
```

## Author

Jarvis
