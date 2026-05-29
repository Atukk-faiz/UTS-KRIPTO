"""
================================================
SISTEM LOGIN SEDERHANA - HASHING PASSWORD
Materi: MD5 dan SHA-256, Dasar Keamanan Data
================================================
Algoritma:
1. Registrasi  → hash password → simpan JSON
2. Login       → hash input   → bandingkan hash
================================================
"""

import hashlib
import json
import os
from datetime import datetime

# ── Konfigurasi file penyimpanan ──────────────────
DATA_FILE = "users.json"

# ════════════════════════════════════════════════
# FUNGSI HASHING
# ════════════════════════════════════════════════

def hash_md5(password: str) -> str:
    """Menghasilkan hash MD5 dari password."""
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha256(password: str) -> str:
    """Menghasilkan hash SHA-256 dari password."""
    return hashlib.sha256(password.encode()).hexdigest()

# ════════════════════════════════════════════════
# FUNGSI PENYIMPANAN DATA (JSON)
# ════════════════════════════════════════════════

def load_users() -> dict:
    """Memuat data user dari file JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users: dict) -> None:
    """Menyimpan data user ke file JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ════════════════════════════════════════════════
# FUNGSI REGISTRASI
# ════════════════════════════════════════════════

def registrasi():
    """
    Algoritma Registrasi:
    1. Input username dan password
    2. Cek apakah username sudah ada
    3. Hitung hash MD5 dan SHA-256
    4. Simpan data ke JSON (TANPA plaintext password)
    5. Tampilkan hasil hash
    """
    print("\n" + "="*55)
    print("           REGISTRASI AKUN BARU")
    print("="*55)

    username = input("  Masukkan username : ").strip()
    if not username:
        print("  [ERROR] Username tidak boleh kosong.")
        return

    users = load_users()
    if username in users:
        print(f"  [ERROR] Username '{username}' sudah terdaftar.")
        return

    password = input("  Masukkan password  : ").strip()
    if not password:
        print("  [ERROR] Password tidak boleh kosong.")
        return

    # ── Proses Hashing ────────────────────────────
    md5_hash    = hash_md5(password)
    sha256_hash = hash_sha256(password)

    # ── Simpan ke JSON (tanpa plaintext) ──────────
    users[username] = {
        "hash_md5"    : md5_hash,
        "hash_sha256" : sha256_hash,
        "terdaftar"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_users(users)

    # ── Tampilkan Hasil ───────────────────────────
    print("\n   Registrasi Berhasil!")
    print("-"*55)
    print(f"  Username       : {username}")
    print(f"  Password Asli  : {password}")
    print(f"  Hash MD5       : {md5_hash}")
    print(f"  Hash SHA-256   : {sha256_hash}")
    print("-"*55)
    print("    Password asli TIDAK disimpan di sistem.")
    print("="*55)

# ════════════════════════════════════════════════
# FUNGSI LOGIN
# ════════════════════════════════════════════════

def login():
    """
    Algoritma Login:
    1. Input username dan password
    2. Cek apakah username terdaftar
    3. Hash password yang diinput (MD5 & SHA-256)
    4. Bandingkan hash dengan hash tersimpan
    5. Jika cocok → Login berhasil | Jika tidak → Gagal
    """
    print("\n" + "="*55)
    print("              LOGIN PENGGUNA")
    print("="*55)

    username = input("  Username : ").strip()
    password = input("  Password : ").strip()

    users = load_users()

    # ── Cek username ──────────────────────────────
    if username not in users:
        print("\n   Login GAGAL: Username tidak ditemukan.")
        print("="*55)
        return

    # ── Hash password input ───────────────────────
    input_md5    = hash_md5(password)
    input_sha256 = hash_sha256(password)

    stored_md5    = users[username]["hash_md5"]
    stored_sha256 = users[username]["hash_sha256"]

    # ── Verifikasi ────────────────────────────────
    print("\n   Proses Verifikasi Login:")
    print("-"*55)
    print(f"  Password Input    : {password}")
    print(f"  Hash MD5 Input    : {input_md5}")
    print(f"  Hash MD5 Tersimpan: {stored_md5}")
    md5_match = " COCOK" if input_md5 == stored_md5 else " TIDAK COCOK"
    print(f"  Hasil MD5         : {md5_match}")
    print()
    print(f"  Hash SHA256 Input    : {input_sha256}")
    print(f"  Hash SHA256 Tersimpan: {stored_sha256}")
    sha_match = " COCOK" if input_sha256 == stored_sha256 else " TIDAK COCOK"
    print(f"  Hasil SHA-256        : {sha_match}")
    print("-"*55)

    if input_md5 == stored_md5 and input_sha256 == stored_sha256:
        print(f"   LOGIN BERHASIL! Selamat datang, {username}!")
    else:
        print("   LOGIN GAGAL! Password salah.")
    print("="*55)

# ════════════════════════════════════════════════
# FUNGSI LIHAT DATA USER (untuk demonstrasi)
# ════════════════════════════════════════════════

def lihat_data():
    """Menampilkan semua data user yang tersimpan di JSON."""
    print("\n" + "="*55)
    print("         DATA USER TERSIMPAN (JSON)")
    print("="*55)
    users = load_users()
    if not users:
        print("  Belum ada user terdaftar.")
    else:
        for i, (uname, info) in enumerate(users.items(), 1):
            print(f"\n  [{i}] Username    : {uname}")
            print(f"      Hash MD5    : {info['hash_md5']}")
            print(f"      Hash SHA256 : {info['hash_sha256']}")
            print(f"      Terdaftar   : {info['terdaftar']}")
    print("="*55)

# ════════════════════════════════════════════════
# MENU UTAMA
# ════════════════════════════════════════════════

def main():
    while True:
        print("\n" + "="*55)
        print("      SISTEM LOGIN - HASHING MD5 & SHA-256")
        print("="*55)
        print("  [1] Registrasi Akun")
        print("  [2] Login")
        print("  [3] Lihat Data User (JSON)")
        print("  [4] Keluar")
        print("="*55)
        pilihan = input("  Pilih menu [1-4]: ").strip()

        if pilihan == "1":
            registrasi()
        elif pilihan == "2":
            login()
        elif pilihan == "3":
            lihat_data()
        elif pilihan == "4":
            print("\n  Terima kasih. Program selesai.\n")
            break
        else:
            print("\n  [!] Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    main()