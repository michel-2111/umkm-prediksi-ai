import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def siapkan_data_training():
    np.random.seed(42)
    jumlah_data = 1000
    
    data = {
        'Recency': np.random.randint(0, 90, jumlah_data),
        'Frequency': np.random.randint(1, 20, jumlah_data),
        'Monetary': np.random.randint(15000, 500000, jumlah_data),
        'Skor_Sentimen': np.random.uniform(-1.0, 1.0, jumlah_data)
    }
    
    df = pd.DataFrame(data)
    
    probabilitas_beli = (
        (90 - df['Recency']) / 90 * 0.3 + 
        (df['Frequency'] / 20) * 0.4 + 
        ((df['Skor_Sentimen'] + 1) / 2) * 0.3
    )
    
    df['Niat_Beli'] = (probabilitas_beli > 0.5).astype(int)
    
    return df

def latih_model_ensemble():
    print("Memuat dataset training...")
    df = siapkan_data_training()
    
    X = df[['Recency', 'Frequency', 'Monetary', 'Skor_Sentimen']]
    y = df['Niat_Beli']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Membangun arsitektur Ensemble Machine Learning...")
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight='balanced', random_state=42)
    xgb = XGBClassifier(learning_rate=0.1, n_estimators=200, max_depth=6, eval_metric='logloss', random_state=42)
    lr = LogisticRegression(max_iter=1000, random_state=42)
    
    ensemble_model = VotingClassifier(
        estimators=[('Random Forest', rf), ('XGBoost', xgb), ('Logistic Regression', lr)],
        voting='soft',
        weights=[0.4, 0.4, 0.2]
    )
    
    print("Melatih model dengan data (Training Process)...")
    ensemble_model.fit(X_train, y_train)
    
    print("Melakukan prediksi pada data pengujian...")
    y_pred = ensemble_model.predict(X_test)
    
    akurasi = accuracy_score(y_test, y_pred)
    print("\n--- HASIL EVALUASI MODEL ---")
    print(f"Akurasi Model : {akurasi * 100:.2f}%")
    print(f"Target Proposal: > 85.00%")
    
    if akurasi >= 0.85:
        print("✅ STATUS: MEMENUHI TARGET PROPOSAL!")
    else:
        print("⚠️ STATUS: BUTUH TUNING HYPERPARAMETER")
        
    print("\nLaporan Klasifikasi Lengkap:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    latih_model_ensemble()