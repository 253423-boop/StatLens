import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats as sp_stats
import google.generativeai as genai
import time

# ══════════════════════════════════════════════════════════════════════════════
# 🔑 GOOGLE GEMINI API KEY 
# ══════════════════════════════════════════════════════════════════════════════
GEMINI_API_KEY = "AIzaSyDbiR1qtAB2cx8ymOBiwNVpuuSj2-yIQP0"

genai.configure(api_key=GEMINI_API_KEY)
# Usamos gemini-3-flash-preview que es el modelo más reciente disponible en tu cuenta
model = genai.GenerativeModel("gemini-3-flash-preview")

def gemini(prompt: str) -> str:
    """Llama a Google Gemini con manejo de cuota."""
    try:
        # Pequeña pausa para no saturar la API gratuita
        time.sleep(1)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "quota" in error_str.lower():
            return "❌ **Límite de velocidad alcanzado**: La versión gratuita permite pocas consultas por minuto. **Espera 30 segundos** y reintenta."
        return f"❌ Error al llamar a Gemini: {e}"

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

data_source = st.radio("Fuente de datos", ["Cargar CSV", "Generar datos sintéticos"], label_visibility="collapsed")

if data_source == "Cargar CSV":
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

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ No se pudo leer el archivo: {e}")
        st.stop()

else:  # Generar datos sintéticos
    st.markdown("#### Generar datos sintéticos")
    dist = st.selectbox("Distribución", ["Normal", "Exponencial", "Uniforme"])
    n = st.slider("Tamaño de muestra (n)", min_value=30, max_value=10000, value=100)
    
    if dist == "Normal":
        mean = st.number_input("Media (μ)", value=0.0, step=0.1)
        std = st.number_input("Desviación estándar (σ)", min_value=0.1, value=1.0, step=0.1)
        data = np.random.normal(mean, std, n)
        df = pd.DataFrame({"Normal": data})
    elif dist == "Exponencial":
        scale = st.number_input("Escala (1/λ)", min_value=0.1, value=1.0, step=0.1)
        data = np.random.exponential(scale, n)
        df = pd.DataFrame({"Exponencial": data})
    else:  # Uniforme
        low = st.number_input("Límite inferior", value=0.0, step=0.1)
        high = st.number_input("Límite superior", value=1.0, step=0.1)
        data = np.random.uniform(low, high, n)
        df = pd.DataFrame({"Uniforme": data})
    
    uploaded_file = type('obj', (object,), {'name': f"Datos sintéticos - {dist}"})()  # Mock object

n_rows, n_cols = df.shape
num_cols   = df.select_dtypes(include="number").columns.tolist()
cat_cols   = df.select_dtypes(include=["object", "string"]).columns.tolist()
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋  Vista previa",
    "📐  Estadísticas descriptivas",
    "🔢  Frecuencias",
    "🧩  Estructura",
    "📈  Gráficas",
    "🧪  Prueba Z",
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

    st.dataframe(display, width='stretch', hide_index=True, height=430)
    st.caption(f"Mostrando {len(display)} de {n_rows} registros · {n_cols} columnas")

    st.markdown("<hr style=\'border:none;border-top:1px solid #E2EAF4;margin:1.2rem 0\'>", unsafe_allow_html=True)
    if st.button("✨ Analizar dataset con IA", key="ia_tab1"):
        muestra = df.head(5).to_string(index=False)
        tipos   = df.dtypes.to_string()
        prompt  = f"""Eres un asistente de estadística para estudiantes universitarios.
Analiza este dataset y responde en español con un resumen ejecutivo breve.

Nombre del archivo: {uploaded_file.name}
Filas: {n_rows} | Columnas: {n_cols}
Variables numéricas: {num_cols}
Variables categóricas: {cat_cols}
Valores nulos totales: {null_total}

Tipos de datos:
{tipos}

Primeras 5 filas:
{muestra}

Describe en 3-5 oraciones: qué tipo de datos contiene el dataset, para qué podría usarse y si hay algo notable en su estructura (nulos, tipos mixtos, columnas interesantes)."""
        with st.spinner("La IA está analizando el dataset..."):
            st.info(gemini(prompt))

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
            width='stretch', hide_index=True,
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
        st.dataframe(cat_summary, width='stretch', hide_index=True,
                     height=min(80 + 40 * len(cat_cols), 380))

    st.markdown("<hr style=\'border:none;border-top:1px solid #E2EAF4;margin:1.2rem 0\'>", unsafe_allow_html=True)
    if st.button("✨ Interpretar estadísticas con IA", key="ia_tab2"):
        resumen_num = df[num_cols].describe().round(4).to_string() if num_cols else "Sin variables numéricas"
        prompt = f"""Eres un asistente de estadística para estudiantes universitarios.
Interpreta las siguientes estadísticas descriptivas en español, de forma clara y educativa.

Dataset: {uploaded_file.name} ({n_rows} filas)
Variables numéricas: {num_cols}
Variables categóricas: {cat_cols}

Estadísticas descriptivas:
{resumen_num}

Redacta 4-6 oraciones ejecutivas comentando: cuáles variables tienen mayor dispersión,
si hay sesgos evidentes, rangos relevantes, y qué variables podrían ser más interesantes para analizar."""
        with st.spinner("La IA está interpretando las estadísticas..."):
            st.info(gemini(prompt))

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
            width='stretch', hide_index=True,
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
            width='stretch', hide_index=True,
            height=min(80 + 40 * len(freq_df), 480),
        )
        st.caption(f"Total: {vc.sum()} registros · {col.nunique()} valores únicos")

    st.markdown("<hr style=\'border:none;border-top:1px solid #E2EAF4;margin:1.2rem 0\'>", unsafe_allow_html=True)
    if st.button("✨ Interpretar frecuencias con IA", key="ia_tab3"):
        tabla_str = freq_df.to_string(index=False)
        prompt = f"""Eres un asistente de estadística para estudiantes universitarios.
Interpreta la siguiente tabla de frecuencias en español de forma clara y educativa.

Variable analizada: {selected_col}
Tipo: {"continua (agrupada en intervalos)" if is_numeric and col.nunique() > 15 else "discreta / categórica"}
Total de registros: {len(col)}

Tabla de frecuencias:
{tabla_str}

Redacta 3-5 oraciones explicando: dónde se concentran los datos (moda o clase modal),
cómo se distribuye la frecuencia acumulada, y si la distribución parece uniforme,
sesgada o bimodal. Usa lenguaje apropiado para un estudiante universitario."""
        with st.spinner("La IA está interpretando las frecuencias..."):
            st.info(gemini(prompt))

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
        width='stretch', hide_index=True,
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
    st.dataframe(dtype_count, width='stretch', hide_index=True, height=180)

    st.markdown("<hr style=\'border:none;border-top:1px solid #E2EAF4;margin:1.2rem 0\'>", unsafe_allow_html=True)
    if st.button("✨ Diagnosticar calidad de datos con IA", key="ia_tab4"):
        struct_str = struct.to_string(index=False)
        prompt = f"""Eres un asistente de estadística para estudiantes universitarios.
Diagnostica la calidad estructural del siguiente dataset en español.

Dataset: {uploaded_file.name}
Filas: {n_rows} | Columnas: {n_cols}
Nulos totales: {null_total}

Estructura de columnas:
{struct_str}

Redacta 4-5 oraciones ejecutivas evaluando: la calidad general del dataset,
columnas con valores nulos o problemas, diversidad de tipos de datos,
y recomendaciones concretas para limpieza o análisis posterior.
Sé directo y usa lenguaje apropiado para un estudiante universitario."""
        with st.spinner("La IA está diagnosticando la calidad del dataset..."):
            st.info(gemini(prompt))

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 · Gráficas
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-title" style="margin-top:.8rem;">Visualización de distribuciones</p>',
                unsafe_allow_html=True)

    if not num_cols:
        st.info("El dataset no contiene columnas numéricas para graficar.")
    else:
        # ── Plot type selector ──
        plot_type = st.selectbox("Tipo de gráfica", ["Histograma", "KDE", "Boxplot"])
        
        # ── Column selector ──
        col_sel = st.selectbox(
            "Variable a graficar",
            num_cols,
            label_visibility="collapsed",
        )
        
        col_data = df[col_sel].dropna()
        mu    = col_data.mean()
        sigma = col_data.std()
        skew  = col_data.skew()
        kurt  = col_data.kurt()   # exceso de curtosis (Fisher)
        n     = len(col_data)
        
        # Outliers
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
        n_outliers = len(outliers)

        # ── Shapiro-Wilk (solo si n <= 5000) ──
        if n <= 5000:
            stat_sw, p_sw = sp_stats.shapiro(col_data)
            shapiro_done  = True
        else:
            shapiro_done  = False

        # ── Layout: chart | analysis ──
        gcol, acol = st.columns([3, 2], gap="large")

        with gcol:
            fig, ax = plt.subplots(figsize=(6.5, 4.2))
            fig.patch.set_facecolor("#F7F9FD")
            ax.set_facecolor("#FFFFFF")

            if plot_type == "Histograma":
                n_bins = st.slider("Número de barras (bins)", min_value=3, max_value=30, value=8,
                                   key="hist_bins")
                # Histogram
                counts, bin_edges, patches = ax.hist(
                    col_data, bins=n_bins,
                    color="#1A56DB", edgecolor="#FFFFFF",
                    linewidth=0.8, alpha=0.88,
                )

                # PDF curve N(µ, σ) overlay
                x_range = np.linspace(col_data.min(), col_data.max(), 300)
                bin_width = bin_edges[1] - bin_edges[0]
                pdf_scaled = sp_stats.norm.pdf(x_range, mu, sigma) * n * bin_width
                ax.plot(x_range, pdf_scaled, color="#E53E3E", linewidth=2,
                        linestyle="--", label=f"PDF Normal N({mu:.1f}, {sigma:.1f})")

                # Mean line
                ax.axvline(mu, color="#1E3A8A", linewidth=1.6,
                           linestyle=":", label=f"Media = {mu:.2f}")

                ax.set_xlabel(col_sel, fontsize=10, color="#0D1B2A")
                ax.set_ylabel("Frecuencia", fontsize=10, color="#0D1B2A")
                ax.set_title(f"Histograma — {col_sel}", fontsize=11,
                             fontweight="bold", color="#0D1B2A", pad=10)
                ax.legend(fontsize=8.5, framealpha=0.7)
                
            elif plot_type == "KDE":
                from scipy.stats import gaussian_kde
                kde = gaussian_kde(col_data)
                x_range = np.linspace(col_data.min(), col_data.max(), 300)
                ax.plot(x_range, kde(x_range), color="#1A56DB", linewidth=2, label="KDE")
                
                # PDF curve N(µ, σ) overlay
                pdf_vals = sp_stats.norm.pdf(x_range, mu, sigma)
                ax.plot(x_range, pdf_vals, color="#E53E3E", linewidth=2,
                        linestyle="--", label=f"PDF Normal N({mu:.1f}, {sigma:.1f})")
                
                # Mean line
                ax.axvline(mu, color="#1E3A8A", linewidth=1.6,
                           linestyle=":", label=f"Media = {mu:.2f}")

                ax.set_xlabel(col_sel, fontsize=10, color="#0D1B2A")
                ax.set_ylabel("Densidad", fontsize=10, color="#0D1B2A")
                ax.set_title(f"KDE — {col_sel}", fontsize=11,
                             fontweight="bold", color="#0D1B2A", pad=10)
                ax.legend(fontsize=8.5, framealpha=0.7)
                
            else:  # Boxplot
                ax.boxplot(col_data, vert=True, patch_artist=True, 
                          boxprops=dict(facecolor="#1A56DB", color="#1A56DB"),
                          medianprops=dict(color="#FFFFFF", linewidth=2),
                          whiskerprops=dict(color="#1A56DB"),
                          capprops=dict(color="#1A56DB"),
                          flierprops=dict(marker='o', color='#E53E3E', markersize=5))
                ax.set_ylabel(col_sel, fontsize=10, color="#0D1B2A")
                ax.set_title(f"Boxplot — {col_sel}", fontsize=11,
                             fontweight="bold", color="#0D1B2A", pad=10)
                # No x labels for single boxplot
                ax.set_xticks([])

            ax.spines[["top", "right"]].set_visible(False)
            ax.spines[["left", "bottom"]].set_color("#CBD5E0")
            ax.tick_params(colors="#64748B", labelsize=8.5)
            if plot_type != "Boxplot":
                ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with acol:
            # ── Normalidad: interpretación basada en las diapositivas del profe ──
            st.markdown("#### 🔍 ¿Se ven normales los datos?")

            # Criterio sesgo
            if   abs(skew) < 0.5:  skew_verdict = ("✅", "Sesgo bajo", "La distribución es aproximadamente simétrica, como una campana.")
            elif abs(skew) < 1.0:  skew_verdict = ("⚠️", "Sesgo moderado", "Hay cierta asimetría; el histograma no es perfectamente simétrico.")
            else:                   skew_verdict = ("❌", "Sesgo alto", "La distribución está claramente sesgada; probablemente **no** es Normal.")

            # Criterio curtosis (exceso)
            if   abs(kurt) < 0.5:  kurt_verdict = ("✅", "Curtosis normal", "La 'altura' de la campana es consistente con una Normal.")
            elif abs(kurt) < 1.5:  kurt_verdict = ("⚠️", "Curtosis moderada", "Las colas difieren un poco de la Normal estándar.")
            else:                   kurt_verdict = ("❌", "Curtosis alta", "Las colas son muy pesadas o muy ligeras; hay diferencia con la Normal.")

            # Shapiro-Wilk
            if shapiro_done:
                if   p_sw > 0.10: sw_verdict = ("✅", f"Shapiro-Wilk p = {p_sw:.4f}", "No se rechaza normalidad (p > 0.10).")
                elif p_sw > 0.05: sw_verdict = ("⚠️", f"Shapiro-Wilk p = {p_sw:.4f}", "Evidencia marginal contra normalidad (0.05 < p ≤ 0.10).")
                else:             sw_verdict = ("❌", f"Shapiro-Wilk p = {p_sw:.4f}", "Se rechaza normalidad (p ≤ 0.05).")
            else:
                sw_verdict = ("ℹ️", "Shapiro-Wilk", "Muestra > 5 000; prueba omitida.")

            # Outliers
            outliers_verdict = ("✅", "Sin outliers", "No hay valores atípicos detectados.") if n_outliers == 0 else ("⚠️", f"{n_outliers} outliers", f"Se detectaron {n_outliers} valores atípicos.")

            checks = [skew_verdict, kurt_verdict, sw_verdict, outliers_verdict]
            positives = sum(1 for c in checks if c[0] == "✅")

            for icon, label, explanation in checks:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2EAF4; border-radius:10px;
                            padding:.75rem 1rem; margin-bottom:.6rem;">
                    <div style="font-weight:600; font-size:.92rem; color:#0D1B2A;">
                        {icon} {label}
                    </div>
                    <div style="font-size:.82rem; color:#64748B; margin-top:.2rem;">
                        {explanation}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Veredicto final ──
            st.markdown("<hr style='border:none;border-top:1px solid #E2EAF4;margin:.8rem 0'>",
                        unsafe_allow_html=True)
            if positives == 4:
                verdict_color, verdict_icon, verdict_text = "#1A56DB", "🔔", "Los datos **se comportan como una distribución Normal**. Puedes usar el modelo N(µ, σ²) de la diapositiva 16 del profe Horacio."
            elif positives >= 3:
                verdict_color, verdict_icon, verdict_text = "#D97706", "🟡", "Los datos son **aproximadamente normales**, con algunas desviaciones. Verifica visualmente si la curva roja se ajusta bien al histograma."
            else:
                verdict_color, verdict_icon, verdict_text = "#DC2626", "🚨", "Los datos **no parecen normales**. Considera otras distribuciones del árbol de decisión (diap. 20): Exponencial, Uniforme o alguna discreta."

            st.markdown(f"""
            <div style="background:#F0F4FF; border-left:4px solid {verdict_color};
                        border-radius:0 10px 10px 0; padding:1rem 1.1rem;">
                <div style="font-size:.95rem; font-weight:600; color:{verdict_color};">
                    {verdict_icon} Veredicto
                </div>
                <div style="font-size:.85rem; color:#0D1B2A; margin-top:.3rem;">
                    {verdict_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Stats mini-table ──
            st.markdown("<br>", unsafe_allow_html=True)
            mini = pd.DataFrame({
                "Parámetro": ["n", "Media (µ)", "Desv. Est. (σ)", "Sesgo", "Curtosis (exc.)", "Q1", "Q3", "IQR", "Outliers"],
                "Valor":     [str(n), f"{mu:.4f}", f"{sigma:.4f}", f"{skew:.4f}", f"{kurt:.4f}", f"{q1:.4f}", f"{q3:.4f}", f"{iqr:.4f}", str(n_outliers)],
            })
            st.dataframe(mini, width='stretch', hide_index=True, height=280)

    st.markdown("<hr style=\'border:none;border-top:1px solid #E2EAF4;margin:1.2rem 0\'>", unsafe_allow_html=True)
    if st.button("✨ Interpretar gráfica con IA", key="ia_tab5"):
        sw_text = f"Shapiro-Wilk: W={stat_sw:.4f}, p={p_sw:.4f}" if shapiro_done else "Shapiro-Wilk: muestra muy grande, omitido"
        prompt = f"""Eres un asistente de estadística para estudiantes universitarios.
Interpreta el análisis de normalidad de la siguiente variable en español.

Variable: {col_sel}
n = {n} | Media = {mu:.4f} | Desv. Est. = {sigma:.4f}
Sesgo = {skew:.4f} | Curtosis (exceso) = {kurt:.4f}
Q1 = {q1:.4f} | Q3 = {q3:.4f} | IQR = {iqr:.4f} | Outliers = {n_outliers}
{sw_text}

Explica en 4-5 oraciones: si la variable sigue una distribución Normal,
qué indican el sesgo y la curtosis, qué dice la prueba Shapiro-Wilk,
si hay outliers y qué implican, y qué distribución del árbol de decisión sería más adecuada si no es Normal
(Exponencial, Uniforme, Binomial, Poisson, etc.). Usa lenguaje para universitarios."""
        with st.spinner("La IA está interpretando la distribución..."):
            st.info(gemini(prompt))

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 · Prueba Z para la media (una muestra)
# Basada en las diapositivas del profe Horacio (UP Chiapas, 14 abril 2026)
# Ruta: diap. 3 → definir H0/H1 → diap. 5/6/7 → calcular z → decidir p-valor
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<p class="section-title" style="margin-top:.8rem;">Prueba Z para la media — una muestra</p>',
                unsafe_allow_html=True)

    if not num_cols:
        st.info("El dataset no contiene columnas numéricas.")
    else:
        # ── Step 1: selección de variable ──────────────────────────────────────
        st.markdown("""
        <div style="background:#EBF2FF;border-left:4px solid #1A56DB;border-radius:0 10px 10px 0;
                    padding:.9rem 1.1rem;margin-bottom:1.2rem;">
            <span style="font-size:.82rem;color:#1E3A8A;font-weight:600;">
            📖 Ruta del profe Horacio (diap. 3): Plantear → H₀/H₁ → fijar α → calcular z → decidir
            </span>
        </div>
        """, unsafe_allow_html=True)

        left_cfg, right_cfg = st.columns([1, 1], gap="large")

        with left_cfg:
            st.markdown("#### ① Selecciona la variable")
            z_col = st.selectbox("Variable numérica", num_cols,
                                 key="z_col", label_visibility="collapsed")
            col_z = df[z_col].dropna()
            n_z   = len(col_z)
            xbar  = col_z.mean()
            s_z   = col_z.std(ddof=1)

            st.markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #E2EAF4;border-radius:10px;
                        padding:.8rem 1.1rem;margin-top:.5rem;">
                <span style="font-size:.78rem;color:#64748B;text-transform:uppercase;
                             letter-spacing:.06em;font-weight:500;">Datos de la muestra</span><br>
                <span style="font-size:.9rem;color:#0D1B2A;">
                n = <b>{n_z}</b> &nbsp;|&nbsp; x̄ = <b>{xbar:.4f}</b> &nbsp;|&nbsp; s = <b>{s_z:.4f}</b>
                </span>
            </div>
            """, unsafe_allow_html=True)

        with right_cfg:
            st.markdown("#### ② Parámetros de la prueba")
            mu0 = st.number_input("Valor hipotético μ₀ (H₀: μ = μ₀)",
                                  value=float(round(xbar, 2)),
                                  format="%.4f", key="z_mu0")
            tipo = st.radio(
                "Tipo de prueba",
                ["Dos colas  (H₁: μ ≠ μ₀)", "Cola derecha  (H₁: μ > μ₀)", "Cola izquierda  (H₁: μ < μ₀)"],
                key="z_tipo",
            )
            alpha = st.select_slider("Nivel de significancia α",
                                     options=[0.01, 0.05, 0.10],
                                     value=0.05, key="z_alpha")
            sigma_opc = st.radio("σ poblacional",
                                 ["Desconocida — usar s muestral (recomendado)",
                                  "Conocida — ingresar valor"],
                                 key="z_sigma_opc")
            sigma_val = s_z
            if sigma_opc.startswith("Conocida"):
                sigma_val = st.number_input("Valor de σ", value=float(round(s_z, 4)),
                                            min_value=0.0001, format="%.4f", key="z_sigma_val")

        st.markdown("<hr style='border:none;border-top:1px solid #E2EAF4;margin:1.4rem 0'>",
                    unsafe_allow_html=True)

        # ── Step 2: cálculos ───────────────────────────────────────────────────
        from scipy.stats import norm as sp_norm

        se      = sigma_val / np.sqrt(n_z)          # error estándar
        z_obs   = (xbar - mu0) / se                 # estadístico z (diap. 9)

        if tipo.startswith("Dos"):
            p_val   = 2 * (1 - sp_norm.cdf(abs(z_obs)))
            z_crit  = sp_norm.ppf(1 - alpha / 2)
            rechaza = abs(z_obs) > z_crit
            h1_str  = f"μ ≠ {mu0}"
            cola    = "bilateral"
        elif tipo.startswith("Cola d"):
            p_val   = 1 - sp_norm.cdf(z_obs)
            z_crit  = sp_norm.ppf(1 - alpha)
            rechaza = z_obs > z_crit
            h1_str  = f"μ > {mu0}"
            cola    = "derecha"
        else:
            p_val   = sp_norm.cdf(z_obs)
            z_crit  = -sp_norm.ppf(1 - alpha)
            rechaza = z_obs < z_crit
            h1_str  = f"μ < {mu0}"
            cola    = "izquierda"

        # Intervalo de confianza (diap. 13: x̄ ± z_α/2 · σ/√n)
        z_ic  = sp_norm.ppf(1 - alpha / 2)
        ic_li = xbar - z_ic * se
        ic_ls = xbar + z_ic * se

        # ── Step 3: mostrar fórmula y resultados ───────────────────────────────
        res_col, plot_col = st.columns([1, 1], gap="large")

        with res_col:
            st.markdown("#### ③ Planteamiento y fórmula")

            # Hipótesis
            st.markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #E2EAF4;border-radius:12px;
                        padding:1rem 1.2rem;margin-bottom:.8rem;">
                <div style="font-size:.78rem;color:#64748B;text-transform:uppercase;
                            letter-spacing:.06em;font-weight:500;margin-bottom:.4rem;">
                    Hipótesis (diap. {"7" if cola=="bilateral" else "5" if cola=="derecha" else "6"})
                </div>
                <div style="font-size:1.05rem;color:#0D1B2A;font-family:Georgia,serif;">
                    H₀ : μ = {mu0} &nbsp;&nbsp;&nbsp; H₁ : {h1_str}
                </div>
                <div style="font-size:.82rem;color:#64748B;margin-top:.3rem;">
                    α = {alpha} &nbsp;|&nbsp; prueba {cola}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Fórmula con valores sustituidos (diap. 9)
            st.markdown(f"""
            <div style="background:#F0F4FF;border:1px solid #BFCFE8;border-radius:12px;
                        padding:1rem 1.2rem;margin-bottom:.8rem;">
                <div style="font-size:.78rem;color:#1E3A8A;text-transform:uppercase;
                            letter-spacing:.06em;font-weight:600;margin-bottom:.5rem;">
                    Fórmula Z (diap. 9)
                </div>
                <div style="font-size:1.1rem;font-family:Georgia,serif;color:#0D1B2A;
                            text-align:center;line-height:2.2;">
                    z &nbsp;=&nbsp;
                    <span style="display:inline-block;text-align:center;vertical-align:middle;">
                        <span style="display:block;border-bottom:2px solid #0D1B2A;
                                     padding:0 .4rem;">&nbsp;x̄ − μ₀&nbsp;</span>
                        <span style="display:block;padding:0 .4rem;">σ / √n</span>
                    </span>
                    &nbsp;=&nbsp;
                    <span style="display:inline-block;text-align:center;vertical-align:middle;">
                        <span style="display:block;border-bottom:2px solid #0D1B2A;
                                     padding:0 .4rem;">&nbsp;{xbar:.4f} − {mu0}&nbsp;</span>
                        <span style="display:block;padding:0 .4rem;">{sigma_val:.4f} / √{n_z}</span>
                    </span>
                    &nbsp;=&nbsp;<b>{z_obs:.4f}</b>
                </div>
                <div style="font-size:.82rem;color:#64748B;margin-top:.4rem;text-align:center;">
                    SE = σ/√n = {sigma_val:.4f}/√{n_z} = <b>{se:.4f}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tabla de valores clave
            tabla_vals = pd.DataFrame({
                "Elemento":       ["z observado", "z crítico", "p-valor", f"IC {int((1-alpha)*100)}%  LI", f"IC {int((1-alpha)*100)}%  LS"],
                "Valor":          [f"{z_obs:.4f}",
                                   f"±{z_crit:.4f}" if cola=="bilateral" else f"{z_crit:.4f}",
                                   f"{p_val:.6f}",
                                   f"{ic_li:.4f}",
                                   f"{ic_ls:.4f}"],
            })
            st.dataframe(tabla_vals, width='stretch', hide_index=True, height=215)

            # ── VEREDICTO ──
            if rechaza:
                st.markdown(f"""
                <div style="background:#FEF2F2;border:2px solid #DC2626;border-radius:14px;
                            padding:1.2rem 1.4rem;margin-top:.8rem;text-align:center;">
                    <div style="font-size:1.6rem;font-weight:800;color:#DC2626;
                                letter-spacing:.5px;">
                        ❌ SE RECHAZA H₀
                    </div>
                    <div style="font-size:.88rem;color:#7F1D1D;margin-top:.4rem;">
                        p-valor ({p_val:.6f}) &lt; α ({alpha})<br>
                        Hay evidencia suficiente para afirmar que <b>μ ≠ {mu0}</b>
                        con {int((1-alpha)*100)}% de confianza.
                    </div>
                    <div style="font-size:.78rem;color:#9CA3AF;margin-top:.3rem;">
                        |z| = {abs(z_obs):.4f} {">" if cola!="bilateral" else ">"} z_crit = {abs(z_crit):.4f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#F0FDF4;border:2px solid #16A34A;border-radius:14px;
                            padding:1.2rem 1.4rem;margin-top:.8rem;text-align:center;">
                    <div style="font-size:1.6rem;font-weight:800;color:#16A34A;
                                letter-spacing:.5px;">
                        ✅ SE ACEPTA H₀
                    </div>
                    <div style="font-size:.88rem;color:#14532D;margin-top:.4rem;">
                        p-valor ({p_val:.6f}) ≥ α ({alpha})<br>
                        No hay evidencia suficiente para rechazar que <b>μ = {mu0}</b>.
                    </div>
                    <div style="font-size:.78rem;color:#9CA3AF;margin-top:.3rem;">
                        |z| = {abs(z_obs):.4f} {"<" if cola!="bilateral" else "<"} z_crit = {abs(z_crit):.4f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Interpretación del IC (diap. 18)
            mu0_en_ic = ic_li <= mu0 <= ic_ls
            st.markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #E2EAF4;border-radius:10px;
                        padding:.75rem 1rem;margin-top:.8rem;">
                <span style="font-size:.78rem;color:#64748B;text-transform:uppercase;
                             letter-spacing:.06em;font-weight:500;">
                    Intervalo de confianza {int((1-alpha)*100)}% (diap. 13/18)
                </span><br>
                <span style="font-size:.92rem;color:#0D1B2A;">
                    ({ic_li:.4f} , {ic_ls:.4f})
                </span><br>
                <span style="font-size:.82rem;color:#64748B;">
                    {"✅ μ₀ = " + str(mu0) + " está DENTRO del IC → consistente con no rechazar H₀."
                      if mu0_en_ic
                      else "❌ μ₀ = " + str(mu0) + " está FUERA del IC → consistente con rechazar H₀."}
                </span>
            </div>
            """, unsafe_allow_html=True)

        # ── Step 4: gráfica N(0,1) con región crítica ──────────────────────────
        with plot_col:
            st.markdown("#### ④ Distribución N(0,1) y región de rechazo")

            fig2, ax2 = plt.subplots(figsize=(5.8, 4.5))
            fig2.patch.set_facecolor("#F7F9FD")
            ax2.set_facecolor("#FFFFFF")

            x_z = np.linspace(-4, 4, 500)
            y_z = sp_norm.pdf(x_z)
            ax2.plot(x_z, y_z, color="#1A56DB", linewidth=2, label="N(0,1)")

            # Región crítica (rojo) y p-valor (naranja) — mismo estilo que diap. 5/6/7
            if cola == "bilateral":
                # Región crítica ±z_crit
                mask_r = x_z >= z_crit
                mask_l = x_z <= -z_crit
                ax2.fill_between(x_z, y_z, where=mask_r, color="#E53E3E", alpha=0.25, label="Región crítica")
                ax2.fill_between(x_z, y_z, where=mask_l, color="#E53E3E", alpha=0.25)
                # p-valor
                if z_obs >= 0:
                    ax2.fill_between(x_z, y_z, where=(x_z >= abs(z_obs)), color="#F97316", alpha=0.45, label="p-valor")
                    ax2.fill_between(x_z, y_z, where=(x_z <= -abs(z_obs)), color="#F97316", alpha=0.45)
                else:
                    ax2.fill_between(x_z, y_z, where=(x_z <= z_obs), color="#F97316", alpha=0.45, label="p-valor")
                    ax2.fill_between(x_z, y_z, where=(x_z >= -z_obs), color="#F97316", alpha=0.45)
                ax2.axvline( z_crit, color="#E53E3E", linewidth=1.5, linestyle="--", label=f"z_crit = ±{z_crit:.3f}")
                ax2.axvline(-z_crit, color="#E53E3E", linewidth=1.5, linestyle="--")
            elif cola == "derecha":
                mask_r = x_z >= z_crit
                ax2.fill_between(x_z, y_z, where=mask_r, color="#E53E3E", alpha=0.25, label="Región crítica")
                ax2.fill_between(x_z, y_z, where=(x_z >= z_obs), color="#F97316", alpha=0.45, label="p-valor")
                ax2.axvline(z_crit, color="#E53E3E", linewidth=1.5, linestyle="--", label=f"z_crit = {z_crit:.3f}")
            else:  # izquierda
                mask_l = x_z <= z_crit
                ax2.fill_between(x_z, y_z, where=mask_l, color="#E53E3E", alpha=0.25, label="Región crítica")
                ax2.fill_between(x_z, y_z, where=(x_z <= z_obs), color="#F97316", alpha=0.45, label="p-valor")
                ax2.axvline(z_crit, color="#E53E3E", linewidth=1.5, linestyle="--", label=f"z_crit = {z_crit:.3f}")

            # z observado
            ax2.axvline(z_obs, color="#1E3A8A", linewidth=2, linestyle=":",
                        label=f"z obs = {z_obs:.3f}")

            ax2.set_xlabel("Estadístico Z", fontsize=9.5, color="#0D1B2A")
            ax2.set_ylabel("Densidad", fontsize=9.5, color="#0D1B2A")
            ax2.set_title(f"Prueba {cola}  (α = {alpha})", fontsize=10.5,
                          fontweight="bold", color="#0D1B2A", pad=8)
            ax2.legend(fontsize=7.8, framealpha=0.8, loc="upper right")
            ax2.set_xlim(-4, 4)
            ax2.spines[["top", "right"]].set_visible(False)
            ax2.spines[["left", "bottom"]].set_color("#CBD5E0")
            ax2.tick_params(colors="#64748B", labelsize=8.5)
            plt.tight_layout()
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)

            # Nota metodológica (cuidado de la diap. 3)
            st.markdown("""
            <div style="background:#FFFBEB;border-left:3px solid #D97706;border-radius:0 8px 8px 0;
                        padding:.7rem 1rem;margin-top:.6rem;">
                <span style="font-size:.8rem;color:#92400E;font-weight:600;">⚠️ Cuidado (diap. 3)</span><br>
                <span style="font-size:.78rem;color:#78350F;">
                    No rechazar H₀ <b>no significa</b> que H₀ sea verdadera;
                    solo indica que no hay evidencia suficiente en esta muestra para descartarla.
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style=\'border:none;border-top:1px solid #E2EAF4;margin:1.2rem 0\'>", unsafe_allow_html=True)
        if st.button("✨ Interpretar prueba Z con IA", key="ia_tab6"):
            resultado = "SE RECHAZA H₀" if rechaza else "SE ACEPTA H₀"
            prompt = f"""Eres un asistente de estadística para estudiantes universitarios.
Interpreta los resultados de esta prueba de hipótesis Z en español, de forma clara y educativa.

Variable analizada: {z_col}
Hipótesis nula: H₀: μ = {mu0}
Hipótesis alternativa: H₁: {h1_str}
Tipo de prueba: {cola}
Nivel de significancia: α = {alpha}

Resultados:
- n = {n_z} | x̄ = {xbar:.4f} | s = {s_z:.4f}
- Error estándar (SE) = {se:.4f}
- z observado = {z_obs:.4f}
- z crítico = {z_crit:.4f}
- p-valor = {p_val:.6f}
- Intervalo de confianza {int((1-alpha)*100)}%: ({ic_li:.4f}, {ic_ls:.4f})
- Decisión: {resultado}

Explica en 4-6 oraciones: qué significa este resultado en el contexto de los datos,
por qué se rechaza o acepta H₀, qué implica el p-valor, qué dice el intervalo de confianza,
y cuál es la conclusión práctica. Usa lenguaje apropiado para un estudiante universitario."""
            with st.spinner("La IA está interpretando la prueba Z..."):
                st.info(gemini(prompt))
