"""Entitas Mahasiswa.

Mahasiswa direpresentasikan sebagai dataclass agar strukturnya
jelas, sekaligus mudah diubah menjadi dictionary (method to_dict)
untuk disimpan atau ditampilkan.
"""

from dataclasses import dataclass, asdict


@dataclass
class Mahasiswa:
    nim: str
    nama: str
    prodi: str
    ipk: float = 0.0

    def to_dict(self):
        """Kembalikan representasi dictionary dari objek ini."""
        return asdict(self)


if __name__ == "__main__":
    mhs = Mahasiswa(nim="20240001", nama="Mahasiswa Contoh",
                    prodi="SI", ipk=3.5)
    print(mhs)
    print(mhs.to_dict())
