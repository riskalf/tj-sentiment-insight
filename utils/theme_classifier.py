import re
from typing import Dict, List, Tuple

# Daftar keyword tiap kategori
TEMA_KEYWORDS = {
    "Bug & Update Sistem": {
        "frasa": [
            "server error", "internal server", "force close",
            "tidak bisa dibuka", "tidak bisa digunakan", "tidak membantu",
            "tidak berguna", "tidak berfungsi", "update mulu", "upgrade mulu",
            "perbaruan mulu", "perbaharuan mulu", "install mulu",
            "susah akses", "susah dibuka", "akses aplikasi", "akses ditolak",
            "sulit digunakan", "sulit dibuka",
        ],
        "kata": [
            "update", "upgrade", "perbarui", "pembaruan", "bug", "error",
            "server", "crash", "loading", "lag", "lambat", "login", "logout",
            "token", "otp", "gangguan", "maintenance", "down", "daftar",
            "register", "tidak bisa", "iklan", "pop up", "buffering",
        ],
    },
    "Tiket & Pembayaran": {
        "frasa": [
            "beli tiket", "isi saldo", "top up", "tap in", "tap out",
            "saldo potong", "virtual account", "dompet digital",
            "scan qrcode", "tiket scan", "tap kartu", "tap tap",
        ],
        "kata": [
            "tiket", "bayar", "pembayaran", "payment", "qris", "qr",
            "qrcode", "barcode", "scan", "saldo", "topup", "refund",
            "transaksi", "debet", "potong", "uang", "astrapay", "gopay",
            "dana", "shopeepay", "kartu", "tjpay",
        ],
    },
    "Tracking & Akurasi Bus": {
        "frasa": [
            "real time", "tidak terdeteksi", "tidak sinkron",
            "tidak muncul", "tracking bus", "tidak sesuai",
            "posisi bus", "data bus", "jam kedatangan", "estimasi jam",
        ],
        "kata": [
            "gps", "tracking", "track", "akurat", "akurasi", "realtime",
            "estimasi", "jadwal", "kedatangan", "posisi", "lokasi",
            "deteksi", "terdeteksi", "terlacak", "sinkron", "goib",
            "stuck", "kelacak",
        ],
    },
    "Informasi Rute & Navigasi": {
        "frasa": [
            "bus nonaktif", "tidak dilalui", "tidak berhenti",
        ],
        "kata": [
            "rute", "jalur", "tujuan", "halte", "koridor", "transit",
            "arah", "navigasi", "peta", "map", "maps", "mikrotrans",
            "jurusan", "trayek",
        ],
    },
    "Layanan Operasional": {
        "frasa": [
            "bus sedikit", "perbanyak bus", "lama datang", "tidak ramah",
        ],
        "kata": [
            "driver", "supir", "sopir", "pramudi", "pramusapa", "petugas",
            "karyawan", "armada", "telat", "terlambat", "tunggu",
            "menunggu", "ngetem", "ditinggal", "ramah", "pelayanan",
            "layanan", "operasional", "ac", "panas", "kebersihan", "bau",
            "antri", "keamanan", "merokok", "sop", "tanggap",
            "fasilitas",
        ],
    },
}

KATEGORI_LAINNYA = "Lainnya"

# Bobot skor
WEIGHT_FRASA = 2
WEIGHT_KATA = 1

# Prioritas jika skor sama
PRIORITAS_TIEBREAK = [
    "Bug & Update Sistem",
    "Tiket & Pembayaran",
    "Tracking & Akurasi Bus",
    "Informasi Rute & Navigasi",
    "Layanan Operasional",
]

_PATTERN_CACHE: dict = {}


def _keyword_pattern(keyword: str) -> "re.Pattern":
    if keyword not in _PATTERN_CACHE:
        _PATTERN_CACHE[keyword] = re.compile(r"\b" + re.escape(keyword) + r"\b")
    return _PATTERN_CACHE[keyword]


def _cari_yang_cocok(keywords: List[str], text: str) -> List[str]:
    """Mengembalikan keyword yang ditemukan."""
    return list(dict.fromkeys(k for k in keywords if _keyword_pattern(k).search(text)))


def _hitung_kecocokan(keywords: List[str], text: str) -> int:
    """Menghitung jumlah kecocokan keyword."""
    return sum(len(_keyword_pattern(k).findall(text)) for k in keywords)


def kategori_keluhan(
    text: str, return_detail: bool = False
) -> Tuple[str, List[str]]:
    """Menentukan kategori keluhan berdasarkan keyword."""
    text_lower = str(text).lower()

    skor: Dict[str, int] = {}
    detail_frasa: Dict[str, int] = {}
    matched_per_kategori: Dict[str, List[str]] = {}

    for kategori, kw in TEMA_KEYWORDS.items():
        jml_frasa = _hitung_kecocokan(kw["frasa"], text_lower)
        jml_kata = _hitung_kecocokan(kw["kata"], text_lower)
        skor[kategori] = WEIGHT_FRASA * jml_frasa + WEIGHT_KATA * jml_kata
        detail_frasa[kategori] = jml_frasa

        matched_per_kategori[kategori] = _cari_yang_cocok(
            kw["frasa"], text_lower
        ) + _cari_yang_cocok(kw["kata"], text_lower)

    skor_maks = max(skor.values())

    if skor_maks == 0:
        hasil = KATEGORI_LAINNYA
    else:
        kandidat = [k for k, v in skor.items() if v == skor_maks]
        if len(kandidat) == 1:
            hasil = kandidat[0]
        else:
            # Prioritaskan jumlah frasa
            maks_frasa = max(detail_frasa[k] for k in kandidat)
            kandidat_frasa = [k for k in kandidat if detail_frasa[k] == maks_frasa]
            if len(kandidat_frasa) == 1:
                hasil = kandidat_frasa[0]
            else:
                # Gunakan urutan prioritas
                hasil = next(
                    (k for k in PRIORITAS_TIEBREAK if k in kandidat_frasa),
                    kandidat_frasa[0],
                )

    keywords_cocok = matched_per_kategori.get(hasil, [])

    if return_detail:
        return hasil, keywords_cocok, skor
    return hasil, keywords_cocok