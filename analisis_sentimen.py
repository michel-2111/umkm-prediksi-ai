import pandas as pd
from sqlalchemy import create_engine
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nltk.download('vader_lexicon', quiet=True)

DATABASE_URI = "postgresql://postgres.vjgpbddhviitkyzffchf:yewVnK41JcLcDw4u@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
engine = create_engine(DATABASE_URI)

def ambil_data_ulasan():
    """Mengambil data ulasan dari Supabase"""
    print("Mengambil data dari Supabase...")
    query = "SELECT id_ulasan, id_umkm, teks_ulasan FROM data_ulasan"
    df = pd.read_sql(query, engine)
    return df

def bersihkan_teks(teks):
    """Membersihkan teks dari simbol dan tanda baca"""
    if pd.isna(teks):
        return ""
    teks = teks.lower()
    teks = re.sub(r'[^a-z\s]', '', teks)
    # Hapus spasi berlebih
    teks = re.sub(r'\s+', ' ', teks).strip()
    return teks

def proses_sentimen():
    df = ambil_data_ulasan()
    
    if df.empty:
        print("⚠️ Tabel ulasan kosong. Pastikan scraper sudah dijalankan.")
        return

    print(f"Berhasil memuat {len(df)} ulasan. Memulai Data Preparation...")

    print("Membersihkan teks dan melakukan stemming (mungkin butuh waktu beberapa detik)...")
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    
    df['teks_bersih'] = df['teks_ulasan'].apply(bersihkan_teks)
    df['teks_stem'] = df['teks_bersih'].apply(stemmer.stem)

    sia = SentimentIntensityAnalyzer()
    
    custom_lexicon = {
        'enak': 2.5,
        'sedap': 3.0,
        'mantap': 2.5,
        'segar': 2.0,
        'fresh': 2.0,
        'cepat': 1.5,
        'lambat': -2.0,
        'lama': -1.5,
        'kurang': -1.5,
        'biasa': 0.0,
        'mahal': -1.0,
        'murah': 1.5
    }
    sia.lexicon.update(custom_lexicon)

    print("Menghitung skor sentimen...")
    df['skor_sentimen'] = df['teks_stem'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    def kategorikan_sentimen(skor):
        if skor >= 0.05:
            return 'Positif'
        elif skor <= -0.05:
            return 'Negatif'
        else:
            return 'Netral'
            
    df['kategori_sentimen'] = df['skor_sentimen'].apply(kategorikan_sentimen)

    print("\n--- HASIL ANALISIS SENTIMEN ---")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', 50)
    print(df[['teks_ulasan', 'teks_stem', 'skor_sentimen', 'kategori_sentimen']])

if __name__ == "__main__":
    proses_sentimen()