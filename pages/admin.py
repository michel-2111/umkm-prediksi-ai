import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import subprocess
import sys
import csv

st.set_page_config(page_title="Panel Admin – MarketIQ", page_icon="🔒", layout="wide")

# ── CSS KONSISTEN (sama dengan app.py) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── BACKGROUND ── */
.stApp {
    background: #0a0f1e;
    color: #e2e8f0;
}

/* ── HIDE STREAMLIT CHROME (header dipertahankan untuk tombol toggle sidebar) ── */
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; background: transparent !important; }
header [data-testid="stHeader"] { background: transparent; }

/* ── SEMBUNYIKAN NAVIGASI OTOMATIS STREAMLIT (app/admin bawaan) ── */
[data-testid="stSidebarNav"] { display: none !important; }

.block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1400px;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0d1424 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.2rem;
}

/* Sidebar brand */
.sidebar-brand {
    display: flex; align-items: center; gap: 10px;
    padding: 0.8rem 0 1.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 1.2rem;
}
.sidebar-brand-icon {
    font-size: 1.4rem;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 10px; padding: 6px 8px; line-height: 1;
}
.sidebar-brand-name {
    font-size: 1rem; font-weight: 800; color: #f0f4ff;
    line-height: 1.1;
}
.sidebar-brand-sub {
    font-size: 0.65rem; color: #64748b; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.08em;
}

/* Sidebar section label */
.sidebar-section-label {
    font-size: 0.65rem; font-weight: 700;
    color: #475569; text-transform: uppercase;
    letter-spacing: 0.12em; padding: 0 0.4rem;
    margin: 1.2rem 0 0.5rem;
}

/* Nav links */
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"],
[data-testid="stSidebar"] a {
    display: flex !important; align-items: center !important;
    gap: 10px !important;
    background: transparent !important;
    border-radius: 10px !important;
    padding: 0.6rem 0.8rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
    text-decoration: none !important;
    transition: background 0.15s, color 0.15s !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] a:hover {
    background: rgba(255,255,255,0.05) !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] a[aria-current="page"] {
    background: rgba(59,130,246,0.12) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 1rem 0 !important;
}

/* Sidebar status badge */
.sidebar-status {
    display: flex; align-items: center; gap: 8px;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 10px; padding: 0.7rem 0.9rem;
    margin-top: 1rem;
}
.sidebar-status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #10b981; flex-shrink: 0;
    box-shadow: 0 0 6px #10b981;
    animation: pulse-green 2s infinite;
}
@keyframes pulse-green { 0%,100%{opacity:1} 50%{opacity:0.4} }
.sidebar-status-text {
    font-size: 0.72rem; font-weight: 600; color: #34d399; line-height: 1.3;
}
.sidebar-status-sub {
    font-size: 0.65rem; color: #065f46;
}

/* Sidebar version */
.sidebar-footer {
    position: absolute; bottom: 1.5rem; left: 1.2rem; right: 1.2rem;
    font-size: 0.65rem; color: #374151; text-align: center;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 0.8rem;
}

/* Toggle button visibility fix */
[data-testid="collapsedControl"] {
    color: #64748b !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
}

/* ── HERO HEADER ── */
.hero-header {
    background: linear-gradient(135deg, #0f1b35 0%, #131d3a 60%, #0d1828 100%);
    border: 1px solid rgba(99, 179, 237, 0.12);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99, 179, 237, 0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 10%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(167, 139, 250, 0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99, 179, 237, 0.1);
    border: 1px solid rgba(99, 179, 237, 0.25);
    color: #63b3ed;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 5px 12px; border-radius: 999px;
    margin-bottom: 1rem;
}
.hero-badge::before { content: '●'; font-size: 0.5rem; animation: pulse-dot 2s infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:0.3} }

.hero-title {
    font-size: 2.2rem; font-weight: 800;
    color: #f0f4ff; line-height: 1.2;
    margin: 0 0 0.6rem;
}
.hero-subtitle {
    font-size: 0.95rem; color: #94a3b8;
    font-weight: 400; margin: 0;
    max-width: 600px;
}

/* ── METRIC CARDS ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: linear-gradient(145deg, #111827, #0f1724);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 179, 237, 0.2);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 16px 16px 0 0;
}
.metric-card.blue::before  { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.metric-card.green::before { background: linear-gradient(90deg, #10b981, #34d399); }
.metric-card.purple::before{ background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

.metric-icon {
    font-size: 1.5rem; margin-bottom: 0.8rem;
}
.metric-value {
    font-size: 1.6rem; font-weight: 800; color: #f1f5f9;
    font-family: 'JetBrains Mono', monospace; line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.75rem; color: #64748b;
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em;
}
.metric-delta {
    display: inline-block;
    font-size: 0.7rem; font-weight: 600;
    padding: 2px 8px; border-radius: 999px;
    margin-top: 0.6rem;
}
.metric-delta.up   { background: rgba(16,185,129,0.12); color: #34d399; }
.metric-delta.info { background: rgba(99,179,237,0.12); color: #63b3ed; }

/* ── SECTION CARDS ── */
.section-card {
    background: #0f1724;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.section-title {
    font-size: 1.1rem; font-weight: 700; color: #e2e8f0;
    margin-bottom: 0.3rem; display: flex; align-items: center; gap: 8px;
}
.section-desc {
    font-size: 0.82rem; color: #64748b;
    margin-bottom: 1.5rem; line-height: 1.6;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px; padding: 4px; gap: 4px;
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 2rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    padding: 0.6rem 1.4rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* ── FORM & CONTROLS ── */
.stSlider [data-baseweb="slider"] { padding: 0 !important; }
.stSlider label, .stNumberInput label, .stSelectSlider label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.3) !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    opacity: 0.9 !important;
}

/* ── ALERTS ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 12px !important;
    font-size: 0.85rem !important;
}

/* ── RESULT BANNER ── */
.result-banner {
    border-radius: 16px;
    padding: 1.8rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
}
.result-banner.high {
    background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(5,150,105,0.05));
    border: 1px solid rgba(16,185,129,0.2);
}
.result-banner.low {
    background: linear-gradient(135deg, rgba(239,68,68,0.08), rgba(220,38,38,0.05));
    border: 1px solid rgba(239,68,68,0.2);
}
.result-pct {
    font-size: 3rem; font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.result-pct.high { color: #34d399; }
.result-pct.low  { color: #f87171; }
.result-label {
    font-size: 0.9rem; font-weight: 600; margin-top: 0.4rem;
}
.result-label.high { color: #6ee7b7; }
.result-label.low  { color: #fca5a5; }
.result-desc {
    font-size: 0.8rem; color: #94a3b8;
    margin-top: 0.6rem; line-height: 1.6;
}

/* ── SEGMENT TABLE ── */
.segment-item {
    display: flex; align-items: center; gap: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.segment-item:hover { border-color: rgba(255,255,255,0.12); }
.segment-dot {
    width: 10px; height: 10px;
    border-radius: 50%; flex-shrink: 0;
}
.segment-name {
    font-size: 0.85rem; font-weight: 700; color: #e2e8f0;
    flex: 1;
}
.segment-desc {
    font-size: 0.75rem; color: #64748b;
    line-height: 1.4; margin-top: 2px;
}
.segment-action {
    font-size: 0.7rem; font-weight: 600;
    padding: 4px 10px; border-radius: 999px;
    flex-shrink: 0;
}

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── OVERRIDE STREAMLIT METRIC ── */
div[data-testid="metric-container"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

/* ── INPUT FIELDS ── */
.stNumberInput input, .stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🔮</div>
        <div>
            <div class="sidebar-brand-name">MarketIQ</div>
            <div class="sidebar-brand-sub">Kuliner Manado</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Navigasi</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Dashboard Utama", icon="📊")
    st.page_link("pages/admin.py", label="Panel Admin", icon="🔒")

    st.markdown("---")
    st.markdown('<div class="sidebar-section-label">Informasi Sistem</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-status">
        <div class="sidebar-status-dot"></div>
        <div>
            <div class="sidebar-status-text">Sistem Online</div>
            <div class="sidebar-status-sub">Supabase · Real-time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# AUTENTIKASI
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("""
    <div class="hero-header">
        <div class="hero-badge">● Area Terbatas</div>
        <div class="hero-title">🔒 Panel Kontrol Administrator</div>
        <div class="hero-subtitle">Masukkan kata sandi untuk mengakses fitur MLOps dan manajemen data.</div>
    </div>
    """, unsafe_allow_html=True)

    col_login, col_spacer = st.columns([1, 2])
    with col_login:
        st.markdown("""
        <div style="background:#0f1724;border:1px solid rgba(255,255,255,0.07);
            border-radius:16px;padding:1.8rem 2rem;margin-top:0.5rem;">
        """, unsafe_allow_html=True)
        input_password = st.text_input("Kata Sandi Admin", type="password",
            placeholder="Masukkan kata sandi...",
            label_visibility="collapsed")
        login_btn = st.button("🔓 Masuk ke Panel Admin", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

        if login_btn:
            if input_password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("❌ Kata sandi salah. Coba lagi.")

# ==========================================
# KONTEN ADMIN (hanya tampil setelah login)
# ==========================================
if st.session_state['authenticated']:

    # Tombol logout di sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Keluar (Logout)", use_container_width=True):
            st.session_state['authenticated'] = False
            st.rerun()

    # Hero header admin
    st.markdown("""
    <div class="hero-header">
        <div class="hero-badge">● Administrator Aktif</div>
        <div class="hero-title">⚙️ Panel Kontrol & Manajemen MLOps</div>
        <div class="hero-subtitle">Kelola data transaksi, unggah dataset, dan orkestrasi pelatihan ulang model AI secara langsung.</div>
    </div>
    """, unsafe_allow_html=True)

    # Status badge
    total_metric, model_metric, db_metric = st.columns(3)
    st.markdown("""
    <div class="metric-grid">
        <div class="metric-card blue">
            <div class="metric-icon">🔐</div>
            <div class="metric-value">Admin</div>
            <div class="metric-label">Status Sesi Saat Ini</div>
            <span class="metric-delta up">Terautentikasi</span>
        </div>
        <div class="metric-card green">
            <div class="metric-icon">🗄️</div>
            <div class="metric-value">Supabase</div>
            <div class="metric-label">Koneksi Database</div>
            <span class="metric-delta up">Terhubung</span>
        </div>
        <div class="metric-card purple">
            <div class="metric-icon">🤖</div>
            <div class="metric-value">3 Model</div>
            <div class="metric-label">Siap Dilatih Ulang</div>
            <span class="metric-delta info">LSTM · K-Means · Ensemble</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    engine = create_engine(st.secrets["SUPABASE_URI"])

    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "📤  Upload Data Kaggle",
        "🛠  CRUD Transaksi",
        "⚙️  Pelatihan Ulang AI"
    ])

    # ── SUB-TAB 1: UPLOAD ──
    # --- SUB-TAB 1: UPLOAD DATA KAGGLE ---
    # --- SUB-TAB 1: UPLOAD DATA KAGGLE ---
    with sub_tab1:
        st.subheader("📤 Transformasi & Injeksi Dataset")
        
        # 1. Kotak Peringatan Spesifikasi Kolom Wajib
        st.warning("""
        **⚠️ PERINGATAN SPESIFIKASI FORMAT DATA:**
        Sistem menggunakan validasi skema otomatis. Sebelum mengunggah, pastikan file CSV Anda telah disesuaikan di Excel/WPS sehingga memiliki nama kolom **persis** seperti di bawah ini (huruf kecil semua):
        
        * **Untuk Data Transaksi (Kiri):** `id_pelanggan`, `tanggal_transaksi`, `total_belanja`
        * **Untuk Data Ulasan (Kanan):** `teks_ulasan`, `rating`, `tanggal_ulasan`
        """)
        
        # Membagi layar menjadi 2 kolom sejajar
        col1, col2 = st.columns(2)
        
        # ==========================================
        # KOLOM 1: UPLOAD DATA TRANSAKSI PENJUALAN
        # ==========================================
        with col1:
            st.markdown("**🛒 1. Data Transaksi (Penjualan)**")
            uploaded_trx = st.file_uploader("Pilih CSV Transaksi", type=["csv"], key="upload_trx")
            
            if uploaded_trx is not None:
                try:
                    df_raw_trx = pd.read_csv(uploaded_trx, sep=None, engine='python')
                    
                    # Validasi Kompatibilitas Kolom
                    required_trx = ['id_pelanggan', 'tanggal_transaksi', 'total_belanja']
                    missing_trx = [col for col in required_trx if col not in df_raw_trx.columns]
                    
                    if missing_trx:
                        st.error(f"❌ Gagal: Struktur kolom tidak sesuai template! Kurang kolom: {', '.join(missing_trx)}")
                    else:
                        st.success("✅ Struktur data transaksi valid!")
                        st.write("🔍 Pratinjau Data:", df_raw_trx.head(3))
                        
                        if st.button("🔥 Suntik ke data_transaksi"):
                            with st.spinner("Mengunggah ke database..."):
                                df_clean_trx = pd.DataFrame()
                                df_clean_trx['id_pelanggan'] = df_raw_trx['id_pelanggan'].astype(str)
                                df_clean_trx['tanggal_transaksi'] = pd.to_datetime(df_raw_trx['tanggal_transaksi'], errors='coerce')
                                df_clean_trx['total_belanja'] = pd.to_numeric(df_raw_trx['total_belanja'], errors='coerce')
                                df_clean_trx['status_pembelian'] = True
                                
                                # Hapus baris kosong hasil konversi yang gagal
                                df_clean_trx = df_clean_trx.dropna(subset=['tanggal_transaksi', 'total_belanja'])
                                
                                df_clean_trx.to_sql('data_transaksi', engine, if_exists='append', index=False)
                                st.success(f"🚀 Berhasil menyuntikkan {len(df_clean_trx)} baris transaksi baru!")
                except Exception as e:
                    st.error(f"Error pemrosesan: {e}")

        # ==========================================
        # KOLOM 2: UPLOAD DATA ULASAN (SENTIMEN)
        # ==========================================
        # ==========================================
        # KOLOM 2: UPLOAD DATA ULASAN (SENTIMEN)
        # ==========================================
        with col2:
            st.markdown("**⭐ 2. Data Ulasan (Reviews)**")
            uploaded_rev = st.file_uploader("Pilih CSV Ulasan", type=["csv"], key="upload_rev")
            
            if uploaded_rev is not None:
                try:
                    # --- FASE 1: PEMBACAAN & DETEKSI FILE ---
                    raw_bytes = uploaded_rev.read(4096)
                    uploaded_rev.seek(0) # Kembalikan kursor ke awal setelah diintip
                    
                    # Deteksi encoding
                    try:
                        raw_bytes.decode('utf-8')
                        encoding = 'utf-8'
                    except UnicodeDecodeError:
                        encoding = 'latin-1'
                    
                    # Deteksi separator menggunakan csv.Sniffer
                    try:
                        sample = raw_bytes.decode(encoding, errors='replace')
                        dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
                        separator = dialect.delimiter
                    except csv.Error:
                        # Fallback aman jika Sniffer gagal karena data terlalu sedikit/berantakan
                        separator = ','
                    
                    # Baca file menggunakan hasil deteksi (on_bad_lines akan melewati baris yang rusak)
                    df_raw_rev = pd.read_csv(uploaded_rev, sep=separator, encoding=encoding, on_bad_lines='skip')

                    df_raw_rev.columns = df_raw_rev.columns.str.strip().str.replace('"', '').str.lower()
                    
                    # --- FASE 2: VALIDASI KOLOM ---
                    if len(df_raw_rev.columns) < 3:
                        raise ValueError(f"Hanya {len(df_raw_rev.columns)} kolom terdeteksi (Pemisah '{separator}'). Periksa format file CSV Anda.")

                    required_rev = ['teks_ulasan', 'rating', 'tanggal_ulasan']
                    missing_rev = [col for col in required_rev if col not in df_raw_rev.columns]
                    
                    if missing_rev:
                        st.error(f"❌ Gagal: Struktur kolom tidak sesuai template! Kurang kolom: {', '.join(missing_rev)}")
                    else:
                        st.success(f"✅ Struktur data ulasan valid! (Encoding: {encoding}, Pemisah: '{separator}')")
                        st.write("🔍 Pratinjau Data:", df_raw_rev.head(3))
                        
                        # --- FASE 3: PEMBERSIHAN & UNGGAH KE DATABASE ---
                        if st.button("🔥 Suntik ke data_ulasan"):
                            with st.spinner("Mengunggah ke database..."):
                                df_clean_rev = pd.DataFrame()
                                
                                # Cegah NaN berubah menjadi string "nan"
                                df_clean_rev['teks_ulasan'] = df_raw_rev['teks_ulasan'].fillna("").astype(str)
                                
                                # Buang baris yang teks ulasannya benar-benar kosong
                                df_clean_rev = df_clean_rev[df_clean_rev['teks_ulasan'].str.strip() != ""]
                                
                                # Konversi angka dan tanggal
                                df_clean_rev['rating'] = pd.to_numeric(df_raw_rev['rating'], errors='coerce').fillna(3).astype(int)
                                
                                # Biarkan format datetime bawaan Pandas agar kompatibel dengan to_sql SQLAlchemy
                                df_clean_rev['tanggal_ulasan'] = pd.to_datetime(df_raw_rev['tanggal_ulasan'], errors='coerce')
                                
                                # Buang baris yang tanggalnya gagal dikonversi (NaT)
                                df_clean_rev = df_clean_rev.dropna(subset=['tanggal_ulasan'])
                                
                                # Suntikkan ke Supabase
                                df_clean_rev.to_sql('data_ulasan', engine, if_exists='append', index=False)
                                st.success(f"🚀 Berhasil menyuntikkan {len(df_clean_rev)} ulasan baru!")

                except Exception as e:
                    st.error(f"Error pemrosesan: {e}")

    # ── SUB-TAB 2: CRUD ──
    with sub_tab2:
        st.markdown('<div class="section-title">🛠 Manajemen Data Transaksi</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Menampilkan 50 transaksi terbaru. Gunakan fitur hapus dengan hati-hati — tindakan ini tidak dapat dibatalkan.</div>', unsafe_allow_html=True)

        try:
            df_crud = pd.read_sql(
                "SELECT * FROM data_transaksi ORDER BY tanggal_transaksi DESC LIMIT 50", engine
            )
            st.dataframe(df_crud, use_container_width=True, height=380)

            st.markdown("---")
            st.markdown('<div class="section-title" style="font-size:0.9rem;color:#f87171">🗑 Hapus Data Berdasarkan ID Pelanggan</div>', unsafe_allow_html=True)
            col_del1, col_del2 = st.columns([3, 1])
            with col_del1:
                id_hapus = st.text_input("ID Pelanggan", placeholder="Contoh: C001",
                    label_visibility="collapsed")
            with col_del2:
                if st.button("❌ Hapus", type="primary", use_container_width=True):
                    if id_hapus:
                        from sqlalchemy import text
                        with engine.connect() as conn:
                            conn.execute(text(f"DELETE FROM data_transaksi WHERE id_pelanggan = :id"), {"id": id_hapus})
                            conn.commit()
                        st.success(f"Data milik ID **{id_hapus}** berhasil dihapus.")
                        st.rerun()
                    else:
                        st.warning("Masukkan ID pelanggan terlebih dahulu.")
        except Exception as e:
            st.error(f"Gagal memuat data: {e}")

    # ── SUB-TAB 3: RETRAINING ──
    with sub_tab3:
        st.markdown('<div class="section-title">⚙️ Orkestrasi Pelatihan Ulang Model AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Memicu eksekusi <code>train_real_models.py</code> untuk melatih ulang seluruh model (LSTM, Ensemble, K-Means) menggunakan data transaksi terbaru dari Supabase.</div>', unsafe_allow_html=True)

        # Info box sebelum retraining
        st.info("⚠️ Proses ini memakan waktu beberapa menit. Jangan tutup halaman saat eksekusi berlangsung.")

        col_btn, col_spacer2 = st.columns([1, 2])
        with col_btn:
            run_btn = st.button("🚀 Mulai Retraining Semua Model", type="primary", use_container_width=True)

        if run_btn:
            with st.spinner("Mengeksekusi skrip pelatihan model... Harap tunggu."):
                try:
                    result = subprocess.run([sys.executable, "train_real_models.py"], capture_output=True, text=True, encoding="utf-8", timeout=600)
                    if result.returncode == 0:
                        st.success("✅ Pelatihan model selesai dengan sukses!")
                    else:
                        st.error("⚠️ Proses selesai dengan error. Periksa log di bawah.")

                    if result.stdout:
                        st.markdown('<div class="section-title" style="font-size:0.9rem">📋 Output Terminal</div>', unsafe_allow_html=True)
                        st.code(result.stdout, language="bash")
                    if result.stderr:
                        st.markdown('<div class="section-title" style="font-size:0.9rem;color:#f59e0b">⚠️ Warning / Error Log</div>', unsafe_allow_html=True)
                        st.code(result.stderr, language="bash")
                except subprocess.TimeoutExpired:
                    st.error("❌ Proses timeout (>10 menit). Cek server Anda.")
                except Exception as e:
                    st.error(f"Gagal menjalankan skrip: {e}")

    # Footer
    st.markdown("""
    <div style="text-align:center;color:#374151;font-size:0.72rem;padding:1.5rem 0;
        border-top:1px solid rgba(255,255,255,0.05);margin-top:2rem;">
        MarketIQ &nbsp;·&nbsp; Panel Admin &nbsp;·&nbsp; Data via Supabase
    </div>
    """, unsafe_allow_html=True)