"""Service CRUD Mahasiswa dengan penyimpanan in-memory.

Penyimpanan berupa dictionary: {nim: Mahasiswa}. Dictionary
dipilih karena pencarian berdasarkan NIM menjadi O(1) dan
NIM secara alami unik, sehingga duplikat mudah dicegah.
Data hanya hidup selama program berjalan; saat program
berhenti, data hilang. Itu memang maksud "in-memory" pada soal.
"""

from ..model.mahasiswa import Mahasiswa
from ..utils.validasi import validasi_nim, validasi_ipk


class MahasiswaService:
    """Mengelola data Mahasiswa (Create, Read, Update, Delete)."""

    def __init__(self):
        self._data = {}

    # Create
    def tambah(self, nim, nama, prodi, ipk=0.0):
        """Tambah mahasiswa baru. Gagal jika NIM sudah ada."""
        nim = validasi_nim(nim)
        ipk = validasi_ipk(ipk)
        if nim in self._data:
            raise ValueError(f"Mahasiswa dengan NIM {nim} sudah ada")
        mahasiswa = Mahasiswa(nim=nim, nama=nama, prodi=prodi, ipk=ipk)
        self._data[nim] = mahasiswa
        return mahasiswa.to_dict()

    # Read (satu)
    def cari(self, nim):
        """Kembalikan dictionary mahasiswa, atau None jika tidak ada."""
        mahasiswa = self._data.get(validasi_nim(nim))
        return mahasiswa.to_dict() if mahasiswa else None

    # Read (semua)
    def semua(self):
        """Kembalikan list dictionary semua mahasiswa."""
        return [mhs.to_dict() for mhs in self._data.values()]

    # Update
    def ubah(self, nim, nama=None, prodi=None, ipk=None):
        """Ubah field yang diberikan saja; field lain tidak berubah.

        Mengembalikan dictionary terbaru, atau None jika NIM
        tidak ditemukan.
        """
        mahasiswa = self._data.get(validasi_nim(nim))
        if mahasiswa is None:
            return None
        if nama is not None:
            mahasiswa.nama = nama
        if prodi is not None:
            mahasiswa.prodi = prodi
        if ipk is not None:
            mahasiswa.ipk = validasi_ipk(ipk)
        return mahasiswa.to_dict()

    # Delete
    def hapus(self, nim):
        """Hapus mahasiswa. True jika terhapus, False jika tidak ada."""
        return self._data.pop(validasi_nim(nim), None) is not None
