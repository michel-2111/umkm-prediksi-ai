from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import time
from datetime import datetime

DATABASE_URI = "postgresql://postgres.vjgpbddhviitkyzffchf:yewVnK41JcLcDw4u@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
engine = create_engine(DATABASE_URI)

def scrape_ulasan_umkm(url_produk, id_umkm):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    print(f"Membuka halaman: {url_produk}")
    
    try:
        driver.get(url_produk)
        time.sleep(5) 
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data_ulasan = []
        
        print("Mengekstrak data ulasan...")
        
        dummy_reviews = [
            {"id_umkm": id_umkm, "tanggal_ulasan": datetime.now().date(), "teks_ulasan": "Rasa sambal roanya enak sekali, pas pedasnya!", "rating": 5},
            {"id_umkm": id_umkm, "tanggal_ulasan": datetime.now().date(), "teks_ulasan": "Pengiriman agak lambat tapi tinutuannya masih fresh.", "rating": 4},
            {"id_umkm": id_umkm, "tanggal_ulasan": datetime.now().date(), "teks_ulasan": "Biasa saja, kurang bumbu khas Minahasa.", "rating": 3}
        ]
        data_ulasan.extend(dummy_reviews)

    except Exception as e:
        print(f"❌ Error saat proses web scraping: {e}")
    finally:
        driver.quit()
        
    df = pd.DataFrame(data_ulasan)
    
    if not df.empty:
        print(f"Menyiapkan {len(df)} baris data untuk dikirim ke Supabase...")
        try:
            df.to_sql('data_ulasan', engine, if_exists='append', index=False)
            print("✅ BERHASIL: Data ulasan telah tersimpan ke tabel Supabase!")
        except Exception as e:
            print(f"❌ Gagal menyimpan ke database: {e}")
    else:
        print("⚠️ Tidak ada data ulasan yang berhasil diekstrak.")

if __name__ == "__main__":
    URL_TARGET = "https://www.google.com"
    ID_UMKM_TARGET = "UMKM-001"
    
    scrape_ulasan_umkm(URL_TARGET, ID_UMKM_TARGET)