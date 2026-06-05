import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

def siapkan_data_deret_waktu():
    """Membuat data sintetis penjualan harian selama 2 tahun dengan pola musiman"""
    print("Menyiapkan dataset deret waktu (Time-Series)...")
    np.random.seed(42)
    hari = pd.date_range(start='2024-01-01', periods=730, freq='D')
    
    waktu = np.arange(len(hari))
    pola_musiman = 50000 * np.sin(waktu / 15) 
    
    efek_weekend = np.where(hari.dayofweek >= 5, 40000, 0)
    
    penjualan_harian = 150000 + pola_musiman + efek_weekend + np.random.normal(0, 5000, len(hari))
    
    penjualan_harian = np.maximum(penjualan_harian, 50000)
    
    df = pd.DataFrame({'Tanggal': hari, 'Total_Penjualan': penjualan_harian})
    df.set_index('Tanggal', inplace=True)
    return df

def latih_model_lstm():
    df = siapkan_data_deret_waktu()
    data_penjualan = df['Total_Penjualan'].values.reshape(-1, 1)
    
    print("Melakukan normalisasi data (MinMaxScaler)...")
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
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    print("Membangun arsitektur LSTM Neural Network...")
    model = Sequential()
    
    model.add(LSTM(units=64, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    
    model.add(LSTM(units=64))
    model.add(Dropout(0.2))
    
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    print("Memulai pelatihan model (Training Process)... Harap tunggu sebentar.")
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
    
    print("\nMelakukan prediksi pada data pengujian...")
    prediksi_scaled = model.predict(X_test)
    prediksi_rupiah = scaler.inverse_transform(prediksi_scaled)
    y_test_rupiah = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    rmse = math.sqrt(mean_squared_error(y_test_rupiah, prediksi_rupiah))
    mae = mean_absolute_error(y_test_rupiah, prediksi_rupiah)
    
    print("\n--- HASIL EVALUASI MODEL LSTM ---")
    print(f"Target MAE Proposal : Kurang dari Rp15.000")
    print(f"Hasil RMSE (Root Mean Squared Error) : Rp{rmse:,.2f}")
    print(f"Hasil MAE (Mean Absolute Error)      : Rp{mae:,.2f}")
    
    if mae < 15000:
        print("✅ STATUS: MEMENUHI TARGET ERROR PROPOSAL!")
    else:
        print("⚠️ STATUS: ERROR MASIH DI ATAS TARGET, BUTUH LEBIH BANYAK EPOCHS (Contoh: naikkan ke 50 atau 100)")

if __name__ == "__main__":
    latih_model_lstm()