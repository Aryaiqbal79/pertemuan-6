"""File main.py: mengimpor dan menggunakan modul utilitas_akademik.

Jalankan dari folder yang sama dengan:
    python main.py

Blok if __name__ == "__main__": memastikan demo di bawah hanya
berjalan saat file ini dieksekusi langsung, bukan saat diimpor
oleh file lain.
"""

from utilitas_akademik import (
    hitung_ipk,
    konversi_nilai_huruf,
    generate_transkrip,
    cetak_transkrip,
)


def main():
    mata_kuliah = [
        {"nama": "Pemrograman Python", "sks": 3, "nilai": "A"},
        {"nama": "Basis Data", "sks": 3, "nilai": "B"},
        {"nama": "Arsitektur SI", "sks": 2, "nilai": "AB"},
    ]

    print("Konversi nilai angka -> huruf:")
    for angka in [92, 82, 77, 71, 66, 55]:
        print(f"  {angka} -> {konversi_nilai_huruf(angka)}")

    print(f"\nIPK: {hitung_ipk(mata_kuliah)}")

    print("\nTranskrip:")
    transkrip = generate_transkrip("Mahasiswa Contoh", "20240001",
                                   mata_kuliah)
    cetak_transkrip(transkrip)


if __name__ == "__main__":
    main()
