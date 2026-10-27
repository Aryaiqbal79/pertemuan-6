"""Modul utilitas_akademik.py

Berisi fungsi-fungsi akademik yang bisa dipakai ulang:
- hitung_ipk()
- konversi_nilai_huruf()
- generate_transkrip()

Jalankan file ini langsung (python utilitas_akademik.py) untuk
menjalankan testing singkat di bawah, berkat blok
if __name__ == "__main__": di akhir file.
"""

BOBOT_NILAI = {
    "A": 4.0,
    "AB": 3.5,
    "B": 3.0,
    "BC": 2.5,
    "C": 2.0,
    "D": 1.0,
    "E": 0.0,
}


def _normalisasi_mata_kuliah(mata_kuliah):
    """Ubah tiap item menjadi (nama, sks, nilai_huruf).

    Item boleh berupa dict {"nama": ..., "sks": ..., "nilai": ...}
    atau tuple (nama, sks, nilai) atau (sks, nilai) tanpa nama.
    """
    hasil = []
    for item in mata_kuliah:
        if isinstance(item, dict):
            nama = item.get("nama", "-")
            sks = item["sks"]
            nilai = item["nilai"]
        elif isinstance(item, (list, tuple)) and len(item) == 3:
            nama, sks, nilai = item
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            nama = "-"
            sks, nilai = item
        else:
            raise ValueError(f"Format mata kuliah tidak dikenali: {item!r}")
        nilai = str(nilai).strip().upper()
        if nilai not in BOBOT_NILAI:
            raise ValueError(f"Nilai huruf tidak valid: {nilai!r}")
        if not isinstance(sks, int) or isinstance(sks, bool) or sks <= 0:
            raise ValueError(f"SKS harus bilangan bulat positif: {sks!r}")
        hasil.append((nama, sks, nilai))
    return hasil


def hitung_ipk(mata_kuliah):
    """Hitung IPK dari list mata kuliah.

    IPK = jumlah (bobot nilai x SKS) / jumlah SKS.
    Hasil dibulatkan ke 2 desimal.
    """
    data = _normalisasi_mata_kuliah(mata_kuliah)
    if not data:
        raise ValueError("daftar mata kuliah tidak boleh kosong")
    total_bobot = sum(BOBOT_NILAI[nilai] * sks for _, sks, nilai in data)
    total_sks = sum(sks for _, sks, _ in data)
    return round(total_bobot / total_sks, 2)


def konversi_nilai_huruf(nilai_angka):
    """Konversi nilai angka (0-100) menjadi nilai huruf.

    Skala yang dipakai dan dinyatakan eksplisit di sini:
    >= 85: A, >= 80: AB, >= 75: B, >= 70: BC,
    >= 65: C, >= 60: D, selain itu: E.
    """
    if isinstance(nilai_angka, bool) or not isinstance(
            nilai_angka, (int, float)):
        raise TypeError("nilai_angka harus berupa angka")
    if not 0 <= nilai_angka <= 100:
        raise ValueError("nilai_angka harus berada pada rentang 0-100")
    if nilai_angka >= 85:
        return "A"
    if nilai_angka >= 80:
        return "AB"
    if nilai_angka >= 75:
        return "B"
    if nilai_angka >= 70:
        return "BC"
    if nilai_angka >= 65:
        return "C"
    if nilai_angka >= 60:
        return "D"
    return "E"


def generate_transkrip(nama, nim, mata_kuliah):
    """Susun transkrip sebagai dictionary terstruktur.

    Dictionary ini mudah dicetak, diubah ke JSON, atau
    dipakai modul lain, tanpa mengunci format tampilannya.
    """
    data = _normalisasi_mata_kuliah(mata_kuliah)
    daftar = [
        {
            "nama": nama_mk,
            "sks": sks,
            "nilai_huruf": nilai,
            "bobot": BOBOT_NILAI[nilai],
        }
        for nama_mk, sks, nilai in data
    ]
    return {
        "nama": nama,
        "nim": nim,
        "mata_kuliah": daftar,
        "total_sks": sum(item["sks"] for item in daftar),
        "ipk": hitung_ipk(mata_kuliah),
    }


def cetak_transkrip(transkrip):
    """Cetak transkrip dalam format yang mudah dibaca."""
    print(f"Nama : {transkrip['nama']}")
    print(f"NIM  : {transkrip['nim']}")
    print("-" * 40)
    for mk in transkrip["mata_kuliah"]:
        print(f"{mk['nama']:<30} {mk['sks']} SKS  {mk['nilai_huruf']}")
    print("-" * 40)
    print(f"Total SKS : {transkrip['total_sks']}")
    print(f"IPK       : {transkrip['ipk']}")


if __name__ == "__main__":
    # Testing singkat modul ini secara mandiri.
    contoh = [
        {"nama": "Pemrograman Python", "sks": 3, "nilai": "A"},
        {"nama": "Basis Data", "sks": 3, "nilai": "B"},
        {"nama": "Arsitektur SI", "sks": 2, "nilai": "AB"},
    ]
    # Hitung manual: (4x3 + 3x3 + 3.5x2) / 8 = 28 / 8 = 3.5
    assert hitung_ipk(contoh) == 3.5
    assert konversi_nilai_huruf(88) == "A"
    assert konversi_nilai_huruf(72) == "BC"
    assert konversi_nilai_huruf(50) == "E"

    transkrip = generate_transkrip("Mahasiswa Contoh", "20240001", contoh)
    cetak_transkrip(transkrip)
    print("Semua assert lolos.")
