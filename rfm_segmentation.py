import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

DATABASE_URI = "postgresql://postgres.vjgpbddhviitkyzffchf:yewVnK41JcLcDw4u@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
engine = create_engine(DATABASE_URI)

def injeksi_data_dummy_transaksi():
    """Membuat dan mengunggah data transaksi dummy ke Supabase untuk uji coba"""
    print("Mengecek data transaksi di database...")
    cek_df = pd.read_sql("SELECT COUNT(*) FROM data_transaksi", engine)
    
    if cek_df.iloc[0, 0] == 0:
        print("Tabel transaksi kosong. Menginjeksi data dummy UMKM...")
        hari_ini = datetime.now()
        
        dummy_data = [
            {"id_umkm": "UMKM-001", "tanggal_transaksi": hari_ini - timedelta(days=2), "id_pelanggan": "PEL-001", "total_belanja": 150000, "status_pembelian": True},
            {"id_umkm": "UMKM-001", "tanggal_transaksi": hari_ini - timedelta(days=5), "id_pelanggan": "PEL-001", "total_belanja": 200000, "status_pembelian": True},
            {"id_umkm": "UMKM-001", "tanggal_transaksi": hari_ini - timedelta(days=10), "id_pelanggan": "PEL-001", "total_belanja": 120000, "status_pembelian": True},
            
            {"id_umkm": "UMKM-001", "tanggal_transaksi": hari_ini - timedelta(days=30), "id_pelanggan": "PEL-002", "total_belanja": 50000, "status_pembelian": True},
            {"id_umkm": "UMKM-001", "tanggal_transaksi": hari_ini - timedelta(days=45), "id_pelanggan": "PEL-002", "total_belanja": 75000, "status_pembelian": True},
            
            {"id_umkm": "UMKM-001", "tanggal_transaksi": hari_ini - timedelta(days=90), "id_pelanggan": "PEL-003", "total_belanja": 35000, "status_pembelian": True},
        ]
        
        df_dummy = pd.DataFrame(dummy_data)
        df_dummy.to_sql('data_transaksi', engine, if_exists='append', index=False)
        print("✅ Data transaksi dummy berhasil ditambahkan!\n")

def proses_rfm_dan_kmeans():
    print("Mengambil data transaksi dari Supabase...")
    query = "SELECT id_pelanggan, tanggal_transaksi, total_belanja FROM data_transaksi WHERE status_pembelian = true"
    df = pd.read_sql(query, engine)
    
    # Konversi kolom tanggal menjadi tipe datetime
    df['tanggal_transaksi'] = pd.to_datetime(df['tanggal_transaksi']).dt.date
    tanggal_analisis = df['tanggal_transaksi'].max()
    
    print("Menghitung metrik Recency, Frequency, dan Monetary...")
    rfm = df.groupby('id_pelanggan').agg({
        'tanggal_transaksi': lambda x: (tanggal_analisis - x.max()).days,
        'id_pelanggan': 'count',                                         
        'total_belanja': 'mean'                                           
    }).rename(columns={
        'tanggal_transaksi': 'Recency',
        'id_pelanggan': 'Frequency',
        'total_belanja': 'Monetary'
    }).reset_index()
    
    scaler = MinMaxScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    
    print("Menerapkan algoritma K-Means Clustering...")
    jumlah_cluster = min(len(rfm), 4) 
    
    kmeans = KMeans(n_clusters=jumlah_cluster, random_state=42, n_init=10)
    rfm['Cluster_ID'] = kmeans.fit_predict(rfm_scaled)
    
    print("\n--- HASIL ANALISIS RFM & CLUSTERING ---")
    pd.set_option('display.max_columns', None)
    print(rfm)

if __name__ == "__main__":
    injeksi_data_dummy_transaksi()
    proses_rfm_dan_kmeans()