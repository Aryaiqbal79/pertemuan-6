"""Praktik 5: mengambil data dari public REST API, lalu menganalisisnya
dengan lambda dan higher-order function (map, filter, sorted),
kemudian menyimpan hasilnya ke file JSON dengan modul json.

Sumber data: JSONPlaceholder (https://jsonplaceholder.typicode.com),
API publik gratis yang biasa dipakai untuk latihan dan tidak
memerlukan API key.

Jalankan dari folder praktik:
    python analisis_api.py
Hasilnya tersimpan di hasil_analisis_api.json di folder yang sama.
"""

import json
from pathlib import Path

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
OUTPUT_FILE = Path(__file__).resolve().parent / "hasil_analisis_api.json"


def ambil_data(endpoint):
    """Ambil JSON dari satu endpoint JSONPlaceholder.

    Timeout dipasang agar program tidak menggantung selamanya
    jika jaringan bermasalah, dan HTTP error diubah menjadi
    exception lewat raise_for_status().
    """
    respons = requests.get(f"{BASE_URL}/{endpoint}", timeout=15)
    respons.raise_for_status()
    return respons.json()


def analisis_posts(posts):
    """Analisis list post dengan map, filter, dan sorted + lambda."""
    # map: ubah tiap post mentah menjadi ringkasan yang rapi.
    ringkasan = list(map(
        lambda p: {
            "id": p["id"],
            "user_id": p["userId"],
            "judul": p["title"],
            "panjang_judul": len(p["title"]),
        },
        posts,
    ))

    # filter: hanya post yang judulnya cukup panjang (> 40 karakter).
    judul_panjang = list(filter(
        lambda p: p["panjang_judul"] > 40,
        ringkasan,
    ))

    # sorted: 10 post dengan judul terpanjang, urut menurun.
    judul_terpanjang = sorted(
        ringkasan,
        key=lambda p: p["panjang_judul"],
        reverse=True,
    )[:10]

    # filter di dalam dict comprehension: hitung post per user.
    user_ids = sorted({p["user_id"] for p in ringkasan})
    jumlah_per_user = {
        user_id: len(list(filter(lambda p: p["user_id"] == user_id,
                                 ringkasan)))
        for user_id in user_ids
    }

    return {
        "total_post": len(posts),
        "jumlah_post_per_user": jumlah_per_user,
        "jumlah_judul_panjang_lebih_dari_40_karakter": len(judul_panjang),
        "judul_terpanjang_10": judul_terpanjang,
    }


def main():
    try:
        posts = ambil_data("posts")
    except requests.exceptions.RequestException as exc:
        print(f"Gagal mengambil data dari JSONPlaceholder: {exc}")
        raise SystemExit(1)

    hasil = analisis_posts(posts)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as berkas:
        json.dump(hasil, berkas, indent=2, ensure_ascii=False)

    print(f"Total post             : {hasil['total_post']}")
    print(f"Jumlah post per user   : {hasil['jumlah_post_per_user']}")
    print("Judul panjang (>40)    : "
          f"{hasil['jumlah_judul_panjang_lebih_dari_40_karakter']}")
    print("\n5 judul terpanjang:")
    for item in hasil["judul_terpanjang_10"][:5]:
        print(f"  - ({item['panjang_judul']} karakter) {item['judul']}")
    print(f"\nHasil lengkap tersimpan di: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
