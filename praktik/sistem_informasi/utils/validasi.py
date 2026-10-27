"""Fungsi validasi sederhana untuk entitas Mahasiswa."""


def validasi_nim(nim):
    """NIM harus berupa string tidak kosong (hanya digit)."""
    if not isinstance(nim, str) or not nim.strip() or not nim.isdigit():
        raise ValueError("NIM harus berupa string digit yang tidak kosong")
    return nim.strip()


def validasi_ipk(ipk):
    """IPK harus berupa angka pada rentang 0.0-4.0."""
    if isinstance(ipk, bool) or not isinstance(ipk, (int, float)):
        raise TypeError("IPK harus berupa angka")
    if not 0.0 <= float(ipk) <= 4.0:
        raise ValueError("IPK harus berada pada rentang 0.0-4.0")
    return float(ipk)


if __name__ == "__main__":
    print(validasi_nim("20240001"))
    print(validasi_ipk(3.5))
