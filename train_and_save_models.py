import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def eksport_model_ensemble():
    print("=== 1. MEMULAI PROSES SERIALISASI MODEL ENSEMBLE ===")
    np.random.seed(42)
    jumlah_data = 1000
    
    data = {
        'Recency': np.random.randint(0, 90, jumlah_data),
        'Frequency': np.random.randint(1, 20, jumlah_data),
        'Monetary': np.random.randint(15000, 500000, jumlah_data),
        'Skor_Sentimen': np.random.uniform(-1.0, 1.0, jumlah_data)
    }
    df = pd.DataFrame(data)
    probabilitas_beli = ((90 - df['Recency']) / 90 * 0.3) + ((df['Frequency'] / 20) * 0.4) + (((df['Skor_Sentimen'] + 1) / 2) * 0.3)
    df['Niat_Beli'] = (probabilitas_beli > 0.5).astype(int)
    
    X = df[['Recency', 'Frequency', 'Monetary', 'Skor_Sentimen']]
    y = df['Niat_Beli']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight='balanced', random_state=42)
    xgb = XGBClassifier(learning_rate=0.1, n_estimators=200, max_depth=6, eval_metric='logloss', random_state=42)
    lr = LogisticRegression(max_iter=1000, random_state=42)
    
    ensemble_model = VotingClassifier(
        estimators=[('Random Forest', rf), ('XGBoost', xgb), ('Logistic Regression', lr)],
        voting='soft',
        weights=[0.4, 0.4, 0.2]
    )
    
    ensemble_model.fit(X_train, y_train)
    
    nama_file_ensemble = 'model_ensemble.joblib'
    joblib.dump(ensemble_model, nama_file_ensemble)
    print(f"✅ BERHASIL: Model Ensemble telah disimpan sebagai '{nama_file_ensemble}'\n")

def eksport_model_lstm():
    print("=== 2. MEMULAI PROSES SERIALISASI MODEL LSTM ===")
    np.random.seed(42)
    hari = pd.date_range(start='2024-01-01', periods=730, freq='D')
    waktu = np.arange(len(hari))
    
    pola_musiman = 50000 * np.sin(waktu / 15)
    efek_weekend = np.where(hari.dayofweek >= 5, 40000, 0)
    penjualan_harian = 150000 + pola_musiman + efek_weekend + np.random.normal(0, 5000, len(hari))
    penjualan_harian = np.maximum(penjualan_harian, 50000)
    
    data_penjualan = penjualan_harian.reshape(-1, 1)
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data_penjualan)
    
    lookback = 30
    X, y = [], []
    for i in range(lookback, len(data_scaled)):
        X.append(data_scaled[i-lookback:i, 0])
        y.append(data_scaled[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    split = int(len(X) * 0.8)
    X_train, y_train = X[:split], y[:split]
    
    model = Sequential()
    model.add(LSTM(units=64, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=64))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    print("Melatih jaringan saraf LSTM selama 100 putaran...")
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)
    
    nama_file_lstm = 'model_lstm.h5'
    nama_file_scaler = 'scaler_lstm.joblib'
    
    model.save(nama_file_lstm)
    joblib.dump(scaler, nama_file_scaler)
    
    print(f"✅ BERHASIL: Model LSTM telah disimpan sebagai '{nama_file_lstm}'")
    print(f"✅ BERHASIL: Scaler data telah disimpan sebagai '{nama_file_scaler}'\n")

if __name__ == "__main__":
    start_time = datetime.now()
    eksport_model_ensemble()
    eksport_model_lstm()
    duration = datetime.now() - start_time
    print(f"🎉 SEMUA TAHAPAN SELESAI! Waktu eksekusi total: {duration.total_seconds():.2f} detik.")
    print("Periksa folder Anda, pastikan tiga file baru telah terbentuk dengan aman.")