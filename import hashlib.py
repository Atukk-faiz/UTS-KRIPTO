import hashlib
import json
import os

# File untuk menyimpan data user
DATA_FILE = "users.json"

def load_users():
    """Memuat data user dari file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Menyimpan data user ke file"""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Mengubah password menjadi hash SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    """Melakukan registrasi user baru"""
    users = load_users()
    
    if username in users:
        print(f"[GAGAL] Username '{username}' sudah terdaftar!")
        return False
    
    hashed = hash_password(password)
    users[username] = hashed
    save_users(users)
    
    print(f"\n[REGISTRASI BERHASIL]")
    print(f"  Username      : {username}")
    print(f"  Hash Password : {hashed}")
    return True

def login(username, password):
    """Melakukan login user"""
    users = load_users()
    
    if username not in users:
        print(f"\n[STATUS LOGIN] GAGAL - Username '{username}' tidak ditemukan!")
        return False
    
    hashed_input = hash_password(password)
    
    print(f"\n[VERIFIKASI PASSWORD]")
    print(f"  Hash Input    : {hashed_input}")
    print(f"  Hash Tersimpan: {users[username]}")
    
    if hashed_input == users[username]:
        print(f"\n[STATUS LOGIN] BERHASIL - Selamat datang, {username}!")
        return True
    else:
        print(f"\n[STATUS LOGIN] GAGAL - Password salah!")
        return False

def main():
    print("=" * 55)
    print("   SISTEM REGISTRASI & LOGIN DENGAN SHA-256")
    print("=" * 55)
    
    while True:
        print("\nMenu:")
        print("  1. Registrasi")
        print("  2. Login")
        print("  3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ").strip()
        
        if pilihan == "1":
            print("\n--- REGISTRASI USER ---")
            username = input("Masukkan username: ").strip()
            password = input("Masukkan password: ").strip()
            register(username, password)
        
        elif pilihan == "2":
            print("\n--- LOGIN USER ---")
            username = input("Masukkan username: ").strip()
            password = input("Masukkan password: ").strip()
            login(username, password)
        
        elif pilihan == "3":
            print("\nProgram selesai. Sampai jumpa!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()