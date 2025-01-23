import sqlite3

# Fungsi untuk Koneksi ke database (buat file baru jika belum ada)
def create_connection():
    conn = sqlite3.connect("pemilu.db")
    return conn

# Fungsi untuk membuat tabel pemilu jika belum ada
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pemilu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_calon TEXT NOT NULL,
        jumlah_pemilih INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print("Tabel 'pemilu' berhasil dibuat!")

# fungsi delete table
def delete_table(table_name='pemilu'):
    conn = create_connection()
    cursor = conn.cursor()

    # Perintah SQL untuk menghapus tabel
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    conn.commit()
    conn.close()
    print(f"Tabel '{table_name}' telah dihapus.")


# Fungsi untuk menambahkan data
def add_data(nama_calon, jumlah_pemilih):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO pemilu (nama_calon, jumlah_pemilih)
    VALUES (?, ?)
    """, (nama_calon, jumlah_pemilih))
    conn.commit()
    conn.close()



def delete_all_data():
    """
    Menghapus seluruh data dalam tabel pemilu.
    """
    conn = create_connection()
    cursor = conn.cursor()

    # Perintah SQL untuk menghapus seluruh data di tabel
    cursor.execute("DELETE FROM pemilu")

    conn.commit()
    conn.close()
    print("Semua data dalam tabel 'pemilu' telah dihapus.")

if __name__ == "__main__":
    delete_all_data()