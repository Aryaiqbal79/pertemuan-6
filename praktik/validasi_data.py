"""Praktik 2: validasi_data()

Menerima dictionary data dan dictionary schema validasi, lalu
mengembalikan tuple (is_valid, errors).

Format schema
-------------
schema = {
    "nama": {"type": str, "required": True},
    "usia": {"type": int, "required": True, "min": 0, "max": 120},
    "ipk":  {"type": (int, float), "min": 0.0, "max": 4.0},
    "prodi": {"type": str, "choices": ["SI", "TI", "PGSD"]},
}

Aturan yang didukung per field:
- "type"     : tipe yang diharapkan (satu tipe atau tuple tipe)
- "required" : True berarti field wajib ada dan tidak boleh None
- "min"/"max": batas nilai untuk angka, atau batas panjang
               untuk str/list (dipakai sesuai jenis datanya)
- "choices"  : daftar nilai yang diperbolehkan

Fleksibilitas tambahan:
- *args   : fungsi validator tambahan. Setiap fungsi menerima
             dictionary data dan mengembalikan pesan error
             (str), list pesan error, atau None jika lolos.
- **kwargs: opsi, misalnya allow_extra=False untuk menolak
             field yang tidak ada di schema.
"""

import re


def _cek_tipe(nilai, tipe_yang_diharapkan):
    """Cek tipe dengan pengecualian bool untuk int.

    Di Python, bool adalah subclass int, sehingga tanpa
    pengecualian ini True akan lolos sebagai int. Untuk
    validasi data, perilaku itu biasanya tidak diinginkan.
    """
    if isinstance(nilai, bool):
        tipe_tuple = (tipe_yang_diharapkan
                      if isinstance(tipe_yang_diharapkan, tuple)
                      else (tipe_yang_diharapkan,))
        return bool in tipe_tuple
    return isinstance(nilai, tipe_yang_diharapkan)


def validasi_data(data, schema, *args, **kwargs):
    """Validasi dictionary data terhadap schema.

    Returns
    -------
    tuple[bool, list[str]]
        (is_valid, errors). is_valid True hanya jika errors kosong.
    """
    if not isinstance(data, dict):
        return False, ["data harus berupa dictionary"]
    if not isinstance(schema, dict):
        return False, ["schema harus berupa dictionary"]

    errors = []
    allow_extra = kwargs.get("allow_extra", True)

    for field, aturan in schema.items():
        wajib = aturan.get("required", False)

        if field not in data or data[field] is None:
            if wajib:
                errors.append(f"Field '{field}' wajib diisi.")
            continue

        nilai = data[field]

        # 1. Tipe data
        tipe = aturan.get("type")
        if tipe is not None and not _cek_tipe(nilai, tipe):
            nama_tipe = (", ".join(t.__name__ for t in tipe)
                         if isinstance(tipe, tuple) else tipe.__name__)
            errors.append(
                f"Field '{field}' harus bertipe {nama_tipe}, "
                f"tetapi mendapat {type(nilai).__name__}.")
            continue  # tidak masuk akal cek rentang jika tipenya salah

        # 2. Rentang nilai (angka) atau panjang (str/list)
        if "min" in aturan or "max" in aturan:
            if isinstance(nilai, (int, float)):
                pembanding, label = nilai, "nilai"
            elif isinstance(nilai, (str, list)):
                pembanding, label = len(nilai), "panjang"
            else:
                pembanding, label = None, None
            if pembanding is not None:
                if "min" in aturan and pembanding < aturan["min"]:
                    errors.append(
                        f"Field '{field}': {label} minimal "
                        f"{aturan['min']}, tetapi mendapat {nilai}.")
                if "max" in aturan and pembanding > aturan["max"]:
                    errors.append(
                        f"Field '{field}': {label} maksimal "
                        f"{aturan['max']}, tetapi mendapat {nilai}.")

        # 3. Daftar nilai yang diperbolehkan
        if "choices" in aturan and nilai not in aturan["choices"]:
            errors.append(
                f"Field '{field}' harus salah satu dari "
                f"{aturan['choices']}, tetapi mendapat {nilai!r}.")

        # 4. Pola regex (opsional, untuk str seperti email)
        if "pattern" in aturan and isinstance(nilai, str):
            if not re.fullmatch(aturan["pattern"], nilai):
                errors.append(
                    f"Field '{field}' tidak sesuai format yang diharapkan.")

    # 5. Field tambahan yang tidak ada di schema
    if not allow_extra:
        for field in data:
            if field not in schema:
                errors.append(f"Field '{field}' tidak dikenal di schema.")

    # 6. Validator tambahan dari *args
    for validator in args:
        hasil = validator(data)
        if hasil is None:
            continue
        if isinstance(hasil, str):
            errors.append(hasil)
        else:
            errors.extend(hasil)

    return (len(errors) == 0, errors)


def _validator_ipk_konsisten(data):
    """Contoh validator tambahan: jika prodi SI, ipk minimal 2.0."""
    if data.get("prodi") == "SI" and isinstance(data.get("ipk"), (int, float)):
        if data["ipk"] < 2.0:
            return "Untuk prodi SI, IPK minimal 2.0."
    return None


if __name__ == "__main__":
    schema_mahasiswa = {
        "nama": {"type": str, "required": True, "min": 3},
        "usia": {"type": int, "required": True, "min": 17, "max": 60},
        "ipk": {"type": (int, float), "min": 0.0, "max": 4.0},
        "prodi": {"type": str, "choices": ["SI", "TI", "PGSD"]},
    }

    data_benar = {"nama": "Arya", "usia": 20, "ipk": 3.5, "prodi": "SI"}
    print("Data benar :", validasi_data(data_benar, schema_mahasiswa))

    data_salah = {"usia": "dua puluh", "ipk": 4.5, "prodi": "Hukum"}
    print("Data salah :", validasi_data(data_salah, schema_mahasiswa))

    # Contoh *args (validator tambahan) dan **kwargs (allow_extra):
    print("Dengan validator tambahan :",
          validasi_data({"nama": "Budi", "usia": 20, "ipk": 1.5,
                         "prodi": "SI"},
                        schema_mahasiswa, _validator_ipk_konsisten))
    print("Menolak field ekstra :",
          validasi_data({**data_benar, "hobi": "membaca"},
                        schema_mahasiswa, allow_extra=False))

    assert validasi_data(data_benar, schema_mahasiswa) == (True, [])
    assert validasi_data(data_salah, schema_mahasiswa)[0] is False
    print("Semua assert lolos.")
