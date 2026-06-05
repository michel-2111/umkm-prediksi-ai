import pandas as pd
import numpy as np
from sqlalchemy import create_engine

DATABASE_URI = "postgresql://postgres.vjgpbddhviitkyzffchf:yewVnK41JcLcDw4u@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
engine = create_engine(DATABASE_URI)

def proses_dan_upload_ulasan():
    print("Membaca file ulasan Kaggle (tokopedia_product_reviews_2025.csv)...")
    try:
        df_raw = pd.read_csv('tokopedia_product_reviews_2025.csv')
        
        df_clean = pd.DataFrame()
        df_clean['id_umkm'] = df_raw['shop_id'].astype(str).apply(lambda x: f"UMKM-{x[:4]}") # Format ID
        df_clean['tanggal_ulasan'] = pd.to_datetime(df_raw['review_date']).dt.date
        df_clean['teks_ulasan'] = df_raw['review_text']
        df_clean['rating'] = pd.to_numeric(df_raw['rating'], errors='coerce').fillna(3).astype(int)
        
        df_clean = df_clean.dropna(subset=['teks_ulasan'])
        
        df_clean = df_clean.sample(n=min(10000, len(df_clean)), random_state=42)
        
        print(f"Mengunggah {len(df_clean)} data ulasan ke Supabase...")
        df_clean.to_sql('data_ulasan', engine, if_exists='append', index=False)
        print("✅ Data Ulasan BERHASIL diunggah!")
        
    except FileNotFoundError:
        print("❌ File 'tokopedia_product_reviews_2025.csv' tidak ditemukan di folder.")
    except Exception as e:
        print(f"❌ Error upload ulasan: {e}")

def proses_dan_upload_transaksi():
    print("\nMembaca file transaksi Kaggle (all_months_clean.csv)...")
    try:
        df_raw = pd.read_csv('all_months_clean.csv', sep=';', on_bad_lines='skip', low_memory=False)
        
        df_raw = df_raw.sample(n=min(10000, len(df_raw)), random_state=42).reset_index(drop=True)
        
        df_clean = pd.DataFrame()
        
        np.random.seed(42)
        daftar_umkm = [f'UMKM-{str(i).zfill(3)}' for i in range(1, 51)]
        df_clean['id_umkm'] = np.random.choice(daftar_umkm, size=len(df_raw))
        
        daftar_pelanggan = [f'PEL-{str(i).zfill(4)}' for i in range(1, 1501)]
        df_clean['id_pelanggan'] = np.random.choice(daftar_pelanggan, size=len(df_raw))
        
        df_clean['tanggal_transaksi'] = pd.to_datetime(df_raw['Waktu Pesanan Dibuat'], format='mixed').dt.date
        df_clean['total_belanja'] = pd.to_numeric(df_raw['Total Pembayaran'], errors='coerce').fillna(50000)
        
        df_clean['status_pembelian'] = True 
        
        print(f"Mengunggah {len(df_clean)} data transaksi ke Supabase...")
        df_clean.to_sql('data_transaksi', engine, if_exists='append', index=False)
        print("✅ Data Transaksi BERHASIL diunggah!")
        
    except FileNotFoundError:
        print("❌ File 'all_months_clean.csv' tidak ditemukan di folder.")
    except Exception as e:
        print(f"❌ Error upload transaksi: {e}")

if __name__ == "__main__":
    print("=== MEMULAI PIPELINE ETL KAGGLE KE SUPABASE ===")
    proses_dan_upload_ulasan()
    proses_dan_upload_transaksi()
    print("=== PIPELINE SELESAI ===")