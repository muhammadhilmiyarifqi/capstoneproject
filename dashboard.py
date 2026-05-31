import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

def _inject_theme_css(theme: str) -> None:
    if theme == "Dark":
        palette = {
            "app_bg": "#0b1220",
            "text": "#e5e7eb",
            "muted": "#9ca3af",
            "card_bg": "#0f172a",
            "card_border": "rgba(148, 163, 184, 0.18)",
            "sidebar_bg": "#0b1220",
            "sidebar_border": "rgba(148, 163, 184, 0.22)",
            "accent_1": "#60a5fa",
            "accent_2": "#34d399",
            "accent_3": "#a78bfa",
            "accent_4": "#fb7185",
        }
    else:
        palette = {
            "app_bg": "#f8fafc",
            "text": "#0f172a",
            "muted": "#64748b",
            "card_bg": "#ffffff",
            "card_border": "rgba(15, 23, 42, 0.10)",
            "sidebar_bg": "#e0f2fe",
            "sidebar_border": "rgba(15, 23, 42, 0.10)",
            "accent_1": "#2563eb",
            "accent_2": "#16a34a",
            "accent_3": "#7c3aed",
            "accent_4": "#db2777",
        }

    st.markdown(
        f"""
<style>
    :root {{
        --app-bg: {palette['app_bg']};
        --text: {palette['text']};
        --muted: {palette['muted']};
        --card-bg: {palette['card_bg']};
        --card-border: {palette['card_border']};
        --sidebar-bg: {palette['sidebar_bg']};
        --sidebar-border: {palette['sidebar_border']};
        --accent-1: {palette['accent_1']};
        --accent-2: {palette['accent_2']};
        --accent-3: {palette['accent_3']};
        --accent-4: {palette['accent_4']};
    }}

    [data-testid="stAppViewContainer"] {{
        background: var(--app-bg);
        color: var(--text);
    }}

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] span {{
        color: var(--text);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background: var(--sidebar-bg);
        border-right: 1px solid var(--sidebar-border);
    }}

    [data-testid="stSidebar"] * {{
        color: var(--text);
    }}

    .sidebar-title {{
        font-size: 1.1rem;
        font-weight: 700;
        padding: 10px 12px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.35);
        border: 1px solid var(--sidebar-border);
        margin-bottom: 10px;
    }}

    .section-title {{
        color: var(--text);
        margin-top: 26px;
        margin-bottom: 14px;
        font-weight: 700;
        border-bottom: 2px solid var(--accent-1);
        padding-bottom: 8px;
        font-size: 1.15rem;
    }}

    .metric-card {{
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 10px 24px rgba(2, 6, 23, 0.08);
        text-align: left;
    }}

    .metric-card[data-accent="a1"] {{ border-left: 6px solid var(--accent-1); }}
    .metric-card[data-accent="a2"] {{ border-left: 6px solid var(--accent-2); }}
    .metric-card[data-accent="a3"] {{ border-left: 6px solid var(--accent-3); }}
    .metric-card[data-accent="a4"] {{ border-left: 6px solid var(--accent-4); }}

    .metric-value {{
        font-size: 2rem;
        font-weight: 800;
        color: var(--text);
        line-height: 1.1;
        margin-top: 2px;
    }}

    .metric-label {{
        font-size: 0.85rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    /* Tighten Streamlit spacing a bit */
    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }}

    /* Make widgets feel a bit more “cardy” inside sidebar */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] > div {{
        font-weight: 600;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

DATA_PATH = Path(__file__).resolve().parent / "datascience" / "StudentPerformanceFactors_analysis.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

try:
    df = load_data()
except FileNotFoundError:
    st.error(f"Dataset tidak ditemukan di {DATA_PATH}. Harap jalankan proses ekspor dataset dari notebook terlebih dahulu.")
    st.stop()

# Order Performance_Category globally
if 'Performance_Category' in df.columns:
    df['Performance_Category'] = pd.Categorical(df['Performance_Category'], categories=['Low', 'Medium', 'High'], ordered=True)

# ==========================================
# SIDEBAR FILTERS
# ==========================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

with st.sidebar:
    st.markdown('<div class="sidebar-title">Settings</div>', unsafe_allow_html=True)
    theme_mode = st.radio("Mode", ["Light", "Dark"], index=0 if st.session_state.theme_mode == "Light" else 1)
    st.session_state.theme_mode = theme_mode

_inject_theme_css(st.session_state.theme_mode)

st.sidebar.markdown('<div class="sidebar-title">Filter Data</div>', unsafe_allow_html=True)

# Categorical filters
cat_cols = ['Performance_Category', 'Gender', 'School_Type', 'Motivation_Level', 'Family_Income', 'Parental_Involvement']
filters = {}

for col in cat_cols:
    if col in df.columns:
        options = df[col].dropna().unique().tolist()
        # Sort options if applicable
        if col == 'Performance_Category':
            options = ['Low', 'Medium', 'High']
        filters[col] = st.sidebar.multiselect(f"{col}", options=options, default=options)

# Numerical filters
num_cols = ['Hours_Studied', 'Attendance', 'Exam_Score']
num_filters = {}

for col in num_cols:
    if col in df.columns:
        min_val = float(df[col].min())
        max_val = float(df[col].max())
        num_filters[col] = st.sidebar.slider(f"{col}", min_value=min_val, max_value=max_val, value=(min_val, max_val))

# Apply filters
df_filtered = df.copy()

for col, selected in filters.items():
    df_filtered = df_filtered[df_filtered[col].isin(selected)]

for col, (min_val, max_val) in num_filters.items():
    df_filtered = df_filtered[(df_filtered[col] >= min_val) & (df_filtered[col] <= max_val)]

if df_filtered.empty:
    st.warning(" Tidak ada data yang cocok dengan filter yang dipilih.")
    st.stop()

# ==========================================
# MAIN DASHBOARD
# ==========================================
st.title("Student Performance Analytics")
st.markdown("Dashboard ini menyajikan insight mendalam menggunakan visualisasi yang sederhana dan mudah dipahami.")

# Key Metrics
st.markdown('<div class="section-title">Key Metrics</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card" data-accent="a1">
        <div class="metric-value">{len(df_filtered):,}</div>
        <div class="metric-label">Total Siswa</div>
    </div>
    """, unsafe_allow_html=True)

avg_score = df_filtered['Exam_Score'].mean() if 'Exam_Score' in df_filtered.columns else 0
with col2:
    st.markdown(f"""
    <div class="metric-card" data-accent="a2">
        <div class="metric-value">{avg_score:.2f}</div>
        <div class="metric-label">Rata-rata Exam Score</div>
    </div>
    """, unsafe_allow_html=True)

if 'Performance_Category' in df_filtered.columns:
    perf_counts = df_filtered['Performance_Category'].value_counts(normalize=True) * 100
    high_pct = perf_counts.get('High', 0)
    low_pct = perf_counts.get('Low', 0)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" data-accent="a3">
            <div class="metric-value">{high_pct:.1f}%</div>
            <div class="metric-label">Siswa High Performance</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card" data-accent="a4">
            <div class="metric-value">{low_pct:.1f}%</div>
            <div class="metric-label">Siswa Low Performance</div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# INSIGHT 1: JAM BELAJAR & KEHADIRAN
# ==========================================
st.markdown('<div class="section-title">Pengaruh Jam Belajar & Kehadiran</div>', unsafe_allow_html=True)

col1_1, col1_2 = st.columns(2)

with col1_1:
    st.markdown("**Korelasi Numerik dengan Ujian**")
    numeric_df = df_filtered.select_dtypes(include="number")
    if 'Exam_Score' in numeric_df.columns and len(numeric_df.columns) > 1:
        corr = numeric_df.corr()['Exam_Score'].drop('Exam_Score').sort_values()
        st.bar_chart(corr)

with col1_2:
    st.markdown("**Rata-rata Jam Belajar & Kehadiran (Scaled) per Kategori**")
    if 'Hours_Studied' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        perf_means = df_filtered.groupby('Performance_Category', observed=True)[['Hours_Studied', 'Attendance']].mean()
        # Scale attendance agar bisa dibandingkan dengan jam belajar dalam satu grafik
        perf_means['Attendance'] = perf_means['Attendance'] / 10
        st.bar_chart(perf_means)


# ==========================================
# INSIGHT 2: TUTORING & EKSTRAKURIKULER
# ==========================================
st.markdown('<div class="section-title">Pengaruh Tutoring & Ekstrakurikuler</div>', unsafe_allow_html=True)
col2_1, col2_2 = st.columns(2)

with col2_1:
    st.markdown("**Jumlah Siswa berdasarkan Sesi Tutoring**")
    if 'Tutoring_Sessions' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        tutor_perf = df_filtered.groupby(['Tutoring_Sessions', 'Performance_Category'], observed=True).size().unstack()
        st.bar_chart(tutor_perf)

with col2_2:
    st.markdown("**Jumlah Siswa berdasarkan Ekstrakurikuler**")
    if 'Extracurricular_Activities' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        extra_perf = df_filtered.groupby(['Extracurricular_Activities', 'Performance_Category'], observed=True).size().unstack()
        st.bar_chart(extra_perf)


# ==========================================
# INSIGHT 3: TIDUR & ORANG TUA
# ==========================================
st.markdown('<div class="section-title">Kualitas Tidur & Keterlibatan Orang Tua</div>', unsafe_allow_html=True)
col3_1, col3_2 = st.columns(2)

with col3_1:
    st.markdown("**Rata-rata Jam Tidur per Kategori Performa**")
    if 'Sleep_Hours' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        sleep_means = df_filtered.groupby('Performance_Category', observed=True)['Sleep_Hours'].mean()
        st.bar_chart(sleep_means)

with col3_2:
    st.markdown("**Jumlah Siswa berdasarkan Keterlibatan Orang Tua**")
    if 'Parental_Involvement' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        parent_perf = df_filtered.groupby(['Parental_Involvement', 'Performance_Category'], observed=True).size().unstack()
        st.bar_chart(parent_perf)


# ==========================================
# INSIGHT 4: INTERVENSI AKADEMIK (GAP ANALYSIS)
# ==========================================
st.markdown('<div class="section-title">Peluang Intervensi Akademik (Gap Analysis)</div>', unsafe_allow_html=True)
st.markdown("Persentase selisih (*gap*) nilai fitur antara siswa **High Performance** dan **Low Performance**.")

if 'Performance_Category' in df_filtered.columns:
    high_df = df_filtered[df_filtered['Performance_Category'] == 'High']
    low_df = df_filtered[df_filtered['Performance_Category'] == 'Low']
    
    if not high_df.empty and not low_df.empty:
        metrics_to_compare = ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Sleep_Hours', 'Tutoring_Sessions']
        available_metrics = [m for m in metrics_to_compare if m in df.columns]
        
        gap_data = []
        for m in available_metrics:
            high_val = high_df[m].mean()
            low_val = low_df[m].mean()
            gap_pct = ((high_val - low_val) / low_val) * 100 if low_val > 0 else 0
            gap_data.append({
                'Metric': m,
                'Gap (%)': gap_pct
            })
        
        gap_df = pd.DataFrame(gap_data)
        gap_df.set_index('Metric', inplace=True)
        gap_df = gap_df.sort_values('Gap (%)', ascending=True)

        st.bar_chart(gap_df['Gap (%)'])
    else:
        st.info("Pilih setidaknya data Low dan High performance di Sidebar untuk melihat Gap Analysis.")

