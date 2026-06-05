from sqlalchemy import create_engine
import pandas as pd

DATABASE_URI = "postgresql://postgres.vjgpbddhviitkyzffchf:yewVnK41JcLcDw4u@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

def test_connection():
    try:
        engine = create_engine(DATABASE_URI)
        
        with engine.connect() as connection:
            print("✅ BERHASIL: Python berhasil terhubung ke Supabase PostgreSQL!")
            
    except Exception as e:
        print("❌ ERROR: Gagal terhubung ke Supabase.")
        print(f"Detail Error: {e}")

if __name__ == "__main__":
    test_connection()