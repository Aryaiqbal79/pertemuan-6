"""Demo package sistem_informasi: CRUD Mahasiswa in-memory.

Jalankan dari folder praktik:
    python demo_sistem_informasi.py
"""

from sistem_informasi.service.mahasiswa_service import MahasiswaService


def main():
    service = MahasiswaService()

    print("CREATE:")
    print(service.tambah("20240001", "Mahasiswa Contoh", "SI", 3.5))
    print(service.tambah("20240002", "Mahasiswa Kedua", "TI", 3.2))

    print("\nREAD (semua):")
    for mhs in service.semua():
        print(" ", mhs)

    print("\nREAD (satu, NIM 20240001):")
    print(" ", service.cari("20240001"))

    print("\nUPDATE (IPK 20240001 menjadi 3.75):")
    print(" ", service.ubah("20240001", ipk=3.75))

    print("\nDELETE (NIM 20240002):")
    print("  Terhapus:", service.hapus("20240002"))
    print("  Sisa data:", service.semua())


if __name__ == "__main__":
    main()
