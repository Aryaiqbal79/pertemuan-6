"""Praktik 1: hitung_statistik()

Menerima sebuah list angka dan mengembalikan dictionary berisi
mean, median, modus, range (max - min), dan standard deviation.
Hanya memakai standard library: statistics dan math
(tidak ada library eksternal).
"""

import statistics


def hitung_statistik(data):
    """Hitung statistik deskriptif dari sebuah list angka.

    Parameters
    ----------
    data : list[int | float]
        List angka yang akan dihitung. Tidak boleh kosong dan
        semua elemennya harus berupa angka (bool tidak dihitung
        sebagai angka di sini).

    Returns
    -------
    dict
        {
            "mean": rata-rata,
            "median": nilai tengah,
            "modus": nilai yang paling sering muncul
                     (jika ada lebih dari satu modus, dikembalikan
                     sebagai list),
            "range": max(data) - min(data),
            "standard_deviation": simpangan baku sampel
                     (statistics.stdev, pembagi n - 1).
                     Untuk satu data nilainya 0.0.
        }

    Raises
    ------
    ValueError
        Jika data kosong.
    TypeError
        Jika ada elemen yang bukan angka.
    """
    if not data:
        raise ValueError("data tidak boleh kosong")

    # bool adalah subclass int di Python, jadi disaring eksplisit
    # agar True/False tidak diam-diam dihitung sebagai 1/0.
    if any(isinstance(x, bool) or not isinstance(x, (int, float))
           for x in data):
        raise TypeError("semua elemen data harus berupa angka")

    data = list(data)
    modus_list = statistics.multimode(data)
    modus = modus_list[0] if len(modus_list) == 1 else modus_list

    return {
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "modus": modus,
        "range": max(data) - min(data),
        "standard_deviation": statistics.stdev(data) if len(data) > 1 else 0.0,
    }


if __name__ == "__main__":
    contoh = [70, 80, 80, 90, 100]
    hasil = hitung_statistik(contoh)
    print(f"Data : {contoh}")
    for kunci, nilai in hasil.items():
        print(f"{kunci:20}: {nilai}")

    # Bukti hitung manual untuk contoh di atas:
    # mean   = (70+80+80+90+100) / 5 = 84.0
    # median = nilai tengah setelah diurutkan = 80
    # modus  = 80 (muncul 2 kali, terbanyak)
    # range  = 100 - 70 = 30
    assert hasil["mean"] == 84.0
    assert hasil["median"] == 80
    assert hasil["modus"] == 80
    assert hasil["range"] == 30
    print("Semua assert lolos.")
