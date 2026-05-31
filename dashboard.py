import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

import numpy as np

st.set_page_config(page_title="Dashboard Analisa Performa Belajar Siswa", layout="wide", page_icon="🎓")

# ==========================================
# KAMUS TERJEMAHAN
# ==========================================
TRANSLATE = {
    'Hours_Studied': 'Jam Belajar', 'Attendance': 'Kehadiran',
    'Previous_Scores': 'Skor Sebelumnya', 'Sleep_Hours': 'Jam Tidur',
    'Tutoring_Sessions': 'Sesi Tutoring', 'Extracurricular_Activities': 'Ekstrakurikuler',
    'Parental_Involvement': 'Keterlibatan Ortu', 'Physical_Activity': 'Aktivitas Fisik',
    'School_Type': 'Tipe Belajar', 'Family_Income': 'Pendapatan Keluarga',
    'Teacher_Quality': 'Kualitas Guru', 'Peer_Influence': 'Pengaruh Teman',
    'Learning_Disabilities': 'Kesulitan Belajar', 'Access_to_Resources': 'Akses Sumber Daya',
    'Distance_from_Home': 'Jarak dari Rumah', 'Motivation_Level': 'Tingkat Motivasi',
    'Internet_Access': 'Akses Internet', 'Family_Background': 'Latar Belakang Keluarga',
    'Gender': 'Jenis Kelamin', 'Exam_Score': 'Skor Ujian',
    'Low': 'Rendah', 'Medium': 'Sedang', 'High': 'Tinggi',
    'Yes': 'Ya', 'No': 'Tidak',
    'Gap (%)': 'Gap (%)'
}

def t(text):
    """Translate a text using the translation dictionary."""
    return TRANSLATE.get(text, text)

def _translate_data(data):
    """Translate index and columns of a DataFrame/Series."""
    if isinstance(data, pd.DataFrame):
        return data.rename(columns=TRANSLATE, index=TRANSLATE)
    elif isinstance(data, pd.Series):
        s = data.rename(index=TRANSLATE)
        s.name = TRANSLATE.get(s.name, s.name)
        return s
    return data

def _center_plot(fig):
    """Display a figure centered in a Streamlit column layout."""
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.pyplot(fig, use_container_width=True)

def _style_ax(ax):
    """Apply common axis styling."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', color='#d3d3d3', alpha=0.7)
    ax.set_axisbelow(True)

# ==========================================
# FUNGSI GRAFIK KHUSUS
# ==========================================

def plot_horizontal_bar(data, ylabel=''):
    """Horizontal bar chart — ideal for korelasi & gap analysis."""
    data = _translate_data(data)
    fig, ax = plt.subplots(figsize=(7, max(3.5, len(data) * 0.45)))
    
    vals = data.values if isinstance(data, pd.Series) else data.iloc[:, 0].values
    colors = ['#EF4444' if v < 0 else ('#2563EB' if abs(v) == max(abs(vals)) else '#93C5FD') for v in vals]
    
    bars = ax.barh(range(len(data)), vals, color=colors, edgecolor='white', height=0.6)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index, fontsize=10)
    ax.invert_yaxis()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', color='#d3d3d3', alpha=0.7)
    ax.set_axisbelow(True)
    if ylabel:
        ax.set_xlabel(ylabel, fontsize=10, color='#555')
    

    
    ax.axvline(x=0, color='#888', linewidth=0.8, linestyle='-')
    fig.tight_layout()
    _center_plot(fig)

def plot_grouped_bar(data, ylabel='Jumlah Siswa'):
    """Grouped vertical bar chart — ideal for comparing categories side by side."""
    data = _translate_data(data)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    color_map = {
        'Rendah': '#EF4444',
        'Sedang': '#F59E0B',
        'Tinggi': '#10B981'
    }
    fallback_colors = ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#0EA5E9']
    
    x = np.arange(len(data.index))
    n_cols = len(data.columns)
    width = 0.7 / n_cols
    
    for i, col in enumerate(data.columns):
        offset = (i - n_cols/2 + 0.5) * width
        c = color_map.get(col, fallback_colors[i % len(fallback_colors)])
        bars = ax.bar(x + offset, data[col], width, label=col, color=c, edgecolor='white')
        

    
    ax.set_xticks(x)
    ax.set_xticklabels(data.index, rotation=0, ha='center', fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10, color='#555')
    ax.legend(frameon=False, fontsize=10, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=n_cols)
    _style_ax(ax)
    fig.tight_layout()
    _center_plot(fig)

def plot_single_bar(data, ylabel=''):
    """Single-color vertical bar chart with highlight on the max value."""
    data = _translate_data(data)
    fig, ax = plt.subplots(figsize=(6, 4))
    
    vals = data.values
    max_idx = np.argmax(vals)
    bar_colors = ['#2563EB' if i == max_idx else '#93C5FD' for i in range(len(vals))]
    
    bars = ax.bar(range(len(data)), vals, color=bar_colors, edgecolor='white', width=0.6)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data.index, rotation=0, ha='center', fontsize=10)
    for i, (bar, v) in enumerate(zip(bars, vals)):
        if i == max_idx:
            ax.text(bar.get_x() + bar.get_width()/2, v + max(vals) * 0.01,
                    f'{v:.2f}', ha='center', va='bottom', fontsize=9, color='#333', fontweight='bold')
    
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color='#555')
    _style_ax(ax)
    fig.tight_layout()
    _center_plot(fig)

def plot_violin(data, x_col, y_col, ylabel=''):
    """Violin plot to show distribution differences across categories."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    palette = {'Low': '#EF4444', 'Medium': '#F59E0B', 'High': '#10B981'}
    order = [c for c in ['Low', 'Medium', 'High'] if c in data[x_col].unique()]
    if not order:
        order = None
        
    sns.violinplot(data=data, x=x_col, y=y_col, order=order, palette=palette, inner="quartile", ax=ax, linewidth=1.2)
    
    ax.set_xlabel('Kategori Performa', fontsize=10, color='#555')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color='#555')
        
    _style_ax(ax)
    fig.tight_layout()
    _center_plot(fig)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f4f6f9;
    }
    .section-card {
        background-color: #ffffff;
        border: 1px solid #bed5ea;
        border-radius: 12px;
        padding: 20px 25px;
        margin: 40px 0 25px 0;
        text-align: left;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .section-card h3 {
        margin: 0 0 8px 0;
        color: #003366;
        font-size: 24px;
        font-weight: 700;
    }
    .section-card p {
        margin: 0;
        color: #1a5276;
        font-size: 14px;
        font-weight: 400;
    }
    .chart-title {
        text-align: center;
        font-weight: 700;
        font-size: 16px;
        color: #103450;
        background-color: white;
        border: 1px solid #cbd4dc;
        border-radius: 6px;
        padding: 8px 15px;
        margin: 20px auto 10px auto;
        width: fit-content;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .insight-box {
        background-color: #eaf4fb;
        border-left: 4px solid #1a5276;
        padding: 12px 18px;
        border-radius: 0 6px 6px 0;
        margin: 5px auto 20px auto;
        max-width: 600px;
        font-size: 14px;
        color: #1a5276;
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path(__file__).resolve().parent / "datascience" / "StudentPerformanceFactors_analysis.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    if 'Performance_Category' not in df.columns and 'Exam_Score' in df.columns:
        low_threshold = df['Exam_Score'].quantile(0.33)
        high_threshold = df['Exam_Score'].quantile(0.66)
        
        def categorize_performance(score):
            if score <= low_threshold: return 'Low'
            elif score <= high_threshold: return 'Medium'
            else: return 'High'
            
        df['Performance_Category'] = df['Exam_Score'].apply(categorize_performance)
    return df

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Dataset tidak ditemukan di {DATA_PATH}. Harap jalankan proses ekspor dataset dari notebook terlebih dahulu.")
    st.stop()

# Order Performance_Category globally
if 'Performance_Category' in df.columns:
    df['Performance_Category'] = pd.Categorical(df['Performance_Category'], categories=['Low', 'Medium', 'High'], ordered=True)

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filter Data")

# Categorical filters
cat_cols = [
    'Performance_Category', 'School_Type', 'Gender', 
    'Parental_Involvement', 'Internet_Access', 'Extracurricular_Activities'
]
filters = {}

sidebar_titles = {
    'Performance_Category': 'Kategori Performa',
    'School_Type': 'Tipe Belajar',
    'Gender': 'Jenis Kelamin',
    'Parental_Involvement': 'Keterlibatan Ortu',
    'Internet_Access': 'Akses Internet',
    'Extracurricular_Activities': 'Ekstrakurikuler'
}

opt_map = {
    'Low': 'RENDAH', 'Medium': 'SEDANG', 'High': 'TINGGI',
    'Public': 'PUBLIK', 'Private': 'PRIVAT',
    'Male': 'LAKI-LAKI', 'Female': 'PEREMPUAN',
    'Yes': 'YA', 'No': 'TIDAK'
}

for col in cat_cols:
    if col in df.columns:
        display_name = sidebar_titles.get(col, col.replace('_', ' '))
        
        options = df[col].dropna().unique().tolist()
        # Sort options properly if it's Performance_Category
        if col == 'Performance_Category':
            options = ['Low', 'Medium', 'High']
            
        radio_options = ['Semua'] + options
        
        selected_val = st.sidebar.radio(
            f"Filter {display_name}",
            options=radio_options,
            index=0,
            horizontal=True,
            format_func=lambda x: "SEMUA" if x == 'Semua' else opt_map.get(str(x), str(x).upper())
        )
        
        if selected_val == 'Semua':
            filters[col] = options
        else:
            filters[col] = [selected_val]
            
        st.sidebar.markdown("---")


# Apply filters
df_filtered = df.copy()

for col, selected in filters.items():
    df_filtered = df_filtered[df_filtered[col].isin(selected)]

if df_filtered.empty:
    st.warning(" Tidak ada data yang cocok dengan filter yang dipilih.")
    st.stop()


# ==========================================
# MAIN DASHBOARD: BANNER
# ==========================================

avg_score = df_filtered['Exam_Score'].mean() if 'Exam_Score' in df_filtered.columns else 0
med_score = df_filtered['Exam_Score'].median() if 'Exam_Score' in df_filtered.columns else 0
if 'Performance_Category' in df_filtered.columns:
    perf_counts = df_filtered['Performance_Category'].value_counts(normalize=True) * 100
    high_pct = perf_counts.get('High', 0)
    low_pct = perf_counts.get('Low', 0)
else:
    high_pct, low_pct = 0, 0

st.markdown(f"""
<div style="background-color: #bed5ea; padding: 40px 30px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
<h1 style="color: #103450; margin-bottom: 10px; font-size: 32px; font-weight: bold;">Dashboard Analisa Performa Belajar Siswa</h1>

<div style="background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.08);">
<div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
<div style="flex: 1; border-right: 1px solid #e0e6ed;">
<p style="margin: 0; color: #7f8c8d; font-weight: bold; font-size: 12px; text-transform: uppercase;">Total Siswa</p>
<h2 style="margin: 5px 0 0 0; color: #103450; font-size: 32px;">{len(df_filtered):,}</h2>
</div>
<div style="flex: 1; border-right: 1px solid #e0e6ed;">
<p style="margin: 0; color: #7f8c8d; font-weight: bold; font-size: 12px; text-transform: uppercase;">Rata-rata Skor</p>
<h2 style="margin: 5px 0 0 0; color: #103450; font-size: 32px;">{avg_score:.2f}</h2>
</div>
<div style="flex: 1; border-right: 1px solid #e0e6ed;">
<p style="margin: 0; color: #7f8c8d; font-weight: bold; font-size: 12px; text-transform: uppercase;">Performa Tinggi</p>
<h2 style="margin: 5px 0 0 0; color: #103450; font-size: 32px;">{high_pct:.1f}%</h2>
</div>
<div style="flex: 1;">
<p style="margin: 0; color: #7f8c8d; font-weight: bold; font-size: 12px; text-transform: uppercase;">Performa Rendah</p>
<h2 style="margin: 5px 0 0 0; color: #103450; font-size: 32px;">{low_pct:.1f}%</h2>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# INSIGHT 1: JAM BELAJAR & KEHADIRAN
# ==========================================
st.markdown('''
<div class="section-card">
    <h3>Faktor Paling Berpengaruh Terhadap Performa Belajar</h3>
    <p>Korelasi dan tingkat pengaruh masing-masing variabel terhadap skor ujian siswa</p>
</div>
''', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Korelasi Variabel yang Mempengaruhi Performa", "Pengaruh Jam Belajar & Kehadiran Terhadap Performa"])

with tab1:
    numeric_df = df_filtered.select_dtypes(include="number")
    if 'Exam_Score' in numeric_df.columns and len(numeric_df.columns) > 1:
        corr = numeric_df.corr()['Exam_Score'].drop('Exam_Score').sort_values(ascending=False)
        plot_horizontal_bar(corr, ylabel='Koefisien Korelasi')
        


with tab2:
    if 'Hours_Studied' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        perf_means = df_filtered.groupby('Performance_Category')[['Hours_Studied', 'Attendance']].mean()
        plot_grouped_bar(perf_means, ylabel='Rata-rata Nilai')
        



# ==========================================
# INSIGHT 2: DISTRIBUSI VARIABEL LAINNYA
# ==========================================
st.markdown('''
<div class="section-card">
    <h3>Distribusi Data Variabel yang Mempengaruhi Performa</h3>
    <p>Eksplorasi komposisi dan penyebaran data berdasarkan performa siswa</p>
</div>
''', unsafe_allow_html=True)

tabs = st.tabs([
    "Sesi Tutoring", "Ekstrakurikuler", "Akses Sumber Daya", 
    "Tingkat Motivasi", "Akses Internet", "Pendapatan Keluarga", 
    "Kualitas Guru", "Jenis Kelamin"
])

with tabs[0]:
    if 'Tutoring_Sessions' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        tutor_perf = df_filtered.groupby(['Tutoring_Sessions', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(tutor_perf, ylabel='Jumlah Siswa')

with tabs[1]:
    if 'Extracurricular_Activities' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        extra_perf = df_filtered.groupby(['Extracurricular_Activities', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(extra_perf, ylabel='Jumlah Siswa')

with tabs[2]:
    if 'Access_to_Resources' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        access_perf = df_filtered.groupby(['Access_to_Resources', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(access_perf, ylabel='Jumlah Siswa')

with tabs[3]:
    if 'Motivation_Level' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        mot_perf = df_filtered.groupby(['Motivation_Level', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(mot_perf, ylabel='Jumlah Siswa')

with tabs[4]:
    if 'Internet_Access' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        net_perf = df_filtered.groupby(['Internet_Access', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(net_perf, ylabel='Jumlah Siswa')

with tabs[5]:
    if 'Family_Income' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        inc_perf = df_filtered.groupby(['Family_Income', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(inc_perf, ylabel='Jumlah Siswa')

with tabs[6]:
    if 'Teacher_Quality' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        teach_perf = df_filtered.groupby(['Teacher_Quality', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(teach_perf, ylabel='Jumlah Siswa')

with tabs[7]:
    if 'Gender' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        gender_perf = df_filtered.groupby(['Gender', 'Performance_Category']).size().unstack(fill_value=0)
        plot_grouped_bar(gender_perf, ylabel='Jumlah Siswa')
        



# ==========================================
# INSIGHT 3: PROFIL SISWA DENGAN PERFORMA RENDAH
# ==========================================
st.markdown('''
<div class="section-card">
    <h3>Distribusi Perbedaan Siswa Performa Rendah dan Tinggi</h3>
    <p>Perbandingan karakteristik profil siswa yang unggul dan yang membutuhkan bantuan</p>
</div>
''', unsafe_allow_html=True)

tabs_bq2 = st.tabs(["Jam Belajar", "Kehadiran", "Skor Sebelumnya", "Keterlibatan Orang Tua", "Tingkat Motivasi", "Akses Sumber Daya"])

with tabs_bq2[0]:
    if 'Hours_Studied' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        plot_violin(df_filtered, x_col='Performance_Category', y_col='Hours_Studied', ylabel='Jam Belajar')

with tabs_bq2[1]:
    if 'Attendance' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        plot_violin(df_filtered, x_col='Performance_Category', y_col='Attendance', ylabel='Persentase Kehadiran (%)')

with tabs_bq2[2]:
    if 'Previous_Scores' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        plot_violin(df_filtered, x_col='Performance_Category', y_col='Previous_Scores', ylabel='Skor Sebelumnya')

with tabs_bq2[3]:
    if 'Parental_Involvement' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        parent_perf = df_filtered.groupby(['Parental_Involvement', 'Performance_Category']).size().unstack(fill_value=0)
        # Reorder if necessary
        if 'Low' in parent_perf.index:
            parent_perf = parent_perf.reindex(['Low', 'Medium', 'High'])
        plot_grouped_bar(parent_perf, ylabel='Jumlah Siswa')

with tabs_bq2[4]:
    if 'Motivation_Level' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        mot_perf = df_filtered.groupby(['Motivation_Level', 'Performance_Category']).size().unstack(fill_value=0)
        if 'Low' in mot_perf.index:
            mot_perf = mot_perf.reindex(['Low', 'Medium', 'High'])
        plot_grouped_bar(mot_perf, ylabel='Jumlah Siswa')

with tabs_bq2[5]:
    if 'Access_to_Resources' in df_filtered.columns and 'Performance_Category' in df_filtered.columns:
        acc_perf = df_filtered.groupby(['Access_to_Resources', 'Performance_Category']).size().unstack(fill_value=0)
        if 'Low' in acc_perf.index:
            acc_perf = acc_perf.reindex(['Low', 'Medium', 'High'])
        plot_grouped_bar(acc_perf, ylabel='Jumlah Siswa')
        



# ==========================================
# INSIGHT 4: INTERVENSI AKADEMIK (GAP ANALYSIS)
# ==========================================
st.markdown('''
<div class="section-card">
    <h3>Peluang Intervensi Akademik</h3>
    <p>Analisis kesenjangan (gap) untuk memprioritaskan tindakan belajar</p>
</div>
''', unsafe_allow_html=True)
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
        gap_df = gap_df.sort_values('Gap (%)', ascending=False)

        plot_horizontal_bar(gap_df['Gap (%)'], ylabel='Gap (%)')

    else:
        st.info("Pilih setidaknya data Low dan High performance di Sidebar untuk melihat Gap Analysis.")

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div style="text-align: center; margin-top: 60px; padding: 20px; border-top: 1px solid #e0e6ed; color: #7f8c8d; font-size: 14px;">
    <strong>Copyright © EduTrack - 2026</strong>
</div>
""", unsafe_allow_html=True)
