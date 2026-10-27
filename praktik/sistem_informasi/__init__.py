"""Package sistem_informasi.

Subpackage:
- model   : definisi entitas Mahasiswa
- service : logika CRUD Mahasiswa (penyimpanan in-memory)
- utils   : fungsi validasi pendukung

Penggunaan:
    from sistem_informasi.service.mahasiswa_service import MahasiswaService
"""

from .service.mahasiswa_service import MahasiswaService
from .model.mahasiswa import Mahasiswa

__all__ = ["Mahasiswa", "MahasiswaService"]
