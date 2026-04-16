import streamlit as st
import pandas as pd
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StatLens",
    page_icon="🔬",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F7F9FD;
    color: #0D1B2A;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; padding-bottom: 3rem; max-width: 1180px; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #1A56DB 0%, #1E3A8A 100%);
    border-radius: 18px;
    padding: 2.6rem 3rem 2.2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: ''; position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero::after {
    content: ''; position: absolute;
    bottom: -40px; left: 42%;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero-wordmark {
    font-family: 'DM Serif Display', serif;
    color: #FFFFFF;
    font-size: 2.3rem;
    margin: 0 0 0.2rem;
    line-height: 1.1;
    letter-spacing: -0.5px;
}
.hero-wordmark span { color: rgba(255,255,255,0.5); font-style: italic; }
.hero-sub {
    color: rgba(255,255,255,0.65);
    font-size: 0.9rem;
    margin: 0;
    font-weight: 300;
    letter-spacing: .02em;
}

/* Stat chips */
.stats-row { display: flex; gap: 1rem; margin-bottom: 1.6rem; flex-wrap: wrap; }
.stat-chip {
    background: #FFFFFF;
    border: 1px solid #E2EAF4;
    border-radius: 10px;
    padding: 0.9rem 1.4rem;
    flex: 1; min-width: 130px;
    box-shadow: 0 1px 4px rgba(26,86,219,0.06);
}
.stat-chip .label {
    font-size: 0.72rem; color: #64748B;
    text-transform: uppercase; letter-spacing: .07em; font-weight: 500;
}
.stat-chip .value {
    font-size: 1.5rem; font-weight: 600;
    color: #1A56DB; line-height: 1.2;
}

/* Section titles */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem; color: #0D1B2A;
    margin: 0 0 0.75rem;
}
.section-divider {
    border: none; border-top: 1px solid #E2EAF4;
    margin: 1.8rem 0 1.4rem;
}

[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.stAlert { border-radius: 10px; }

[data-testid="stFileUploader"] > div {
    background: #FFFFFF !important;
    border: 2px dashed #BFCFE8 !important;
    border-radius: 14px !important;
    padding: 1.6rem !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F0F4FB; }
::-webkit-scrollbar-thumb { background: #BFCFE8; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-wordmark">🔬 StatLens <span>— análisis estadístico</span></div>
    <p class="hero-sub">Carga cualquier CSV y explora tus datos · Probabilidad y Estadística</p>
</div>
""", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Cargar datos</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "CSV",
    type=["csv"],
    help="Sube cualquier archivo en formato CSV",
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center; padding:3.5rem 0; color:#94A3B8;">
        <div style="font-size:3rem; margin-bottom:.6rem;">📂</div>
        <p style="font-size:1rem; font-weight:500; color:#64748B; margin:0;">
            Sube un archivo CSV para comenzar
        </p>
        <p style="font-size:0.83rem; color:#94A3B8; margin:.4rem 0 0;">
            Compatible con cualquier CSV separado por comas
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load CSV ──────────────────────────────────────────────────────────────────
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"❌ No se pudo leer el archivo: {e}")
    st.stop()

n_rows, n_cols = df.shape
num_cols   = df.select_dtypes(include="number").columns.tolist()
cat_cols   = df.select_dtypes(include="object").columns.tolist()
null_total = int(df.isnull().sum().sum())

# ── Stats chips ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-row">
    <div class="stat-chip">
        <div class="label">Registros</div>
        <div class="value">{n_rows}</div>
    </div>
    <div class="stat-chip">
        <div class="label">Variables</div>
        <div class="value">{n_cols}</div>
    </div>
    <div class="stat-chip">
        <div class="label">Numéricas</div>
        <div class="value">{len(num_cols)}</div>
    </div>
    <div class="stat-chip">
        <div class="label">Categóricas</div>
        <div class="value">{len(cat_cols)}</div>
    </div>
    <div class="stat-chip">
        <div class="label">Valores nulos</div>
        <div class="value">{null_total}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.success(f"✅ **{uploaded_file.name}** cargado correctamente")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋  Vista previa",
    "📐  Estadísticas descriptivas",
    "🔢  Frecuencias",
    "🧩  Estructura",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 · Vista previa
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-title" style="margin-top:.8rem;">Datos cargados</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        search = st.text_input("Buscar", placeholder="🔍 Filtra por cualquier valor…",
                               label_visibility="collapsed")
    with c2:
        row_opts   = sorted(set([10, 25, 50, 100, n_rows]))
        row_labels = [str(r) if r != n_rows else f"Todos ({n_rows})" for r in row_opts]
        chosen_label = st.selectbox("Filas", row_labels, index=0, label_visibility="collapsed")
        chosen_rows  = row_opts[row_labels.index(chosen_label)]

    display = df.copy()
    if search:
        mask = display.apply(
            lambda c: c.astype(str).str.contains(search, case=False, na=False)
        ).any(axis=1)
        display = display[mask]
    display = display.head(chosen_rows)

    st.dataframe(display, use_container_width=True, hide_index=True, height=430)
    st.caption(f"Mostrando {len(display)} de {n_rows} registros · {n_cols} columnas")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 · Estadísticas descriptivas
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title" style="margin-top:.8rem;">Variables numéricas</p>',
                unsafe_allow_html=True)

    if not num_cols:
        st.info("El dataset no contiene columnas numéricas.")
    else:
        desc = df[num_cols].describe().T
        desc.index.name = "Variable"
        desc = desc.reset_index()
        desc["sesgo"] = [round(df[c].skew(), 4) for c in num_cols]
        desc["IQR"]   = [round(df[c].quantile(0.75) - df[c].quantile(0.25), 4) for c in num_cols]
        desc.columns  = ["Variable", "N", "Media", "Desv. Est.", "Mín",
                         "Q1 (25%)", "Mediana", "Q3 (75%)", "Máx", "Sesgo", "IQR"]
        st.dataframe(
            desc.style.format({c: "{:.4f}" for c in desc.columns if c != "Variable"}),
            use_container_width=True, hide_index=True,
            height=min(80 + 40 * len(num_cols), 520),
        )
        st.caption("N = valores no nulos · IQR = rango intercuartílico · Sesgo = asimetría de Fisher")

    if cat_cols:
        st.markdown('<hr class="section-divider"><p class="section-title">Variables categóricas — resumen</p>',
                    unsafe_allow_html=True)
        cat_summary = pd.DataFrame({
            "Variable":   cat_cols,
            "Registros":  [df[c].count() for c in cat_cols],
            "Únicos":     [df[c].nunique() for c in cat_cols],
            "Moda":       [df[c].mode().iloc[0] if not df[c].mode().empty else "—" for c in cat_cols],
            "Frec. moda": [df[c].value_counts().iloc[0] if not df[c].value_counts().empty else 0 for c in cat_cols],
            "Nulos":      [df[c].isnull().sum() for c in cat_cols],
        })
        st.dataframe(cat_summary, use_container_width=True, hide_index=True,
                     height=min(80 + 40 * len(cat_cols), 380))

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 · Tablas de frecuencia
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title" style="margin-top:.8rem;">Tabla de frecuencias</p>',
                unsafe_allow_html=True)

    selected_col = st.selectbox("Variable", df.columns.tolist(), label_visibility="collapsed")
    col = df[selected_col].dropna()
    is_numeric = pd.api.types.is_numeric_dtype(col)

    if is_numeric and col.nunique() > 15:
        n_bins = st.slider("Número de intervalos (clases)", min_value=3, max_value=20, value=7)
        counts, edges = np.histogram(col, bins=n_bins)
        freq_df = pd.DataFrame({
            "Clase":              [f"[{edges[i]:.2f}, {edges[i+1]:.2f})" for i in range(len(counts))],
            "Marca de clase":     [(edges[i] + edges[i+1]) / 2 for i in range(len(counts))],
            "Frec. absoluta":     counts,
            "Frec. relativa":     counts / counts.sum(),
            "Frec. relativa %":   counts / counts.sum() * 100,
            "Frec. acumulada":    counts.cumsum(),
            "Frec. acum. rel. %": counts.cumsum() / counts.sum() * 100,
        })
        st.dataframe(
            freq_df.style.format({
                "Marca de clase":     "{:.4f}",
                "Frec. relativa":     "{:.4f}",
                "Frec. relativa %":   "{:.2f}%",
                "Frec. acum. rel. %": "{:.2f}%",
            }),
            use_container_width=True, hide_index=True,
            height=min(80 + 40 * n_bins, 480),
        )
        st.caption(f"Total: {counts.sum()} registros · {n_bins} clases")
    else:
        vc = col.value_counts().sort_index()
        freq_df = pd.DataFrame({
            "Valor":              vc.index,
            "Frec. absoluta":     vc.values,
            "Frec. relativa":     vc.values / vc.sum(),
            "Frec. relativa %":   vc.values / vc.sum() * 100,
            "Frec. acumulada":    vc.values.cumsum(),
            "Frec. acum. rel. %": vc.values.cumsum() / vc.sum() * 100,
        })
        st.dataframe(
            freq_df.style.format({
                "Frec. relativa":     "{:.4f}",
                "Frec. relativa %":   "{:.2f}%",
                "Frec. acum. rel. %": "{:.2f}%",
            }),
            use_container_width=True, hide_index=True,
            height=min(80 + 40 * len(freq_df), 480),
        )
        st.caption(f"Total: {vc.sum()} registros · {col.nunique()} valores únicos")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 · Estructura
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title" style="margin-top:.8rem;">Columnas del dataset</p>',
                unsafe_allow_html=True)

    struct = pd.DataFrame({
        "#":        range(1, n_cols + 1),
        "Columna":  df.columns,
        "Tipo":     df.dtypes.astype(str).values,
        "No nulos": df.count().values,
        "Nulos":    df.isnull().sum().values,
        "% nulos":  (df.isnull().sum().values / n_rows * 100),
        "Únicos":   df.nunique().values,
    })
    st.dataframe(
        struct.style.format({"% nulos": "{:.1f}%"}),
        use_container_width=True, hide_index=True,
        height=min(80 + 40 * n_cols, 520),
    )

    if null_total > 0:
        st.warning(f"⚠️ El dataset contiene **{null_total}** valor(es) nulo(s) en total.")
    else:
        st.success("✅ No hay valores nulos en el dataset.")

    st.markdown('<hr class="section-divider"><p class="section-title">Resumen de tipos</p>',
                unsafe_allow_html=True)
    dtype_count = df.dtypes.astype(str).value_counts().reset_index()
    dtype_count.columns = ["Tipo", "Columnas"]
    st.dataframe(dtype_count, use_container_width=True, hide_index=True, height=180)