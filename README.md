# 🔬 StatLens — Análisis Estadístico

Aplicación web para cargar cualquier archivo CSV y explorarlo mediante tablas y gráficas estadísticas.  
Desarrollada con Python y Streamlit para la materia de **Probabilidad y Estadística**.

---

## 🗂 Archivos del proyecto

```
statlens/
├── app.py       ← la aplicación
└── README.md
```

---

## ✅ Requisitos previos

- **Python 3.8 o superior** — verifica con `python --version`

---

## 🚀 Instalación y ejecución

### 1. Instala las dependencias

```bash
pip install streamlit pandas numpy matplotlib scipy
```

### 2. Inicia la aplicación

```bash
streamlit run app.py
```

### 3. Abre el navegador

Streamlit abre la app automáticamente. Si no, ve a:

```
http://localhost:8501
```

### 4. Carga tu CSV

Haz clic en el botón de carga y selecciona cualquier archivo `.csv`.

---

## 📊 Pestañas disponibles

| Pestaña | Contenido |
|---|---|
| **Vista previa** | Tabla completa con buscador y selector de filas |
| **Estadísticas descriptivas** | Media, mediana, desv. est., Q1, Q3, IQR, sesgo para numéricas; moda y conteos para categóricas |
| **Frecuencias** | Frec. absoluta, relativa, relativa % y acumulada; intervalos configurables para variables continuas |
| **Estructura** | Tipo de dato, nulos, % nulos y valores únicos por columna |
| **Gráficas** | Histograma azul con curva PDF Normal superpuesta + análisis automático de normalidad |

### Sobre la pestaña Gráficas

- Selecciona cualquier variable numérica del CSV.
- Ajusta el número de barras con el slider.
- La curva roja punteada muestra cómo se vería si los datos siguieran una distribución **Normal N(µ, σ)**.
- El panel lateral evalúa automáticamente tres criterios:
  - **Sesgo** — qué tan simétrica es la distribución (diap. 4 del profe).
  - **Curtosis** — qué tan "puntiaguda" o "plana" es la campana (diap. 16).
  - **Prueba Shapiro-Wilk** — contraste formal de normalidad (diap. 22–23).
- Un veredicto final indica si conviene modelar con Normal o explorar otras distribuciones del árbol de decisión (diap. 20).

---

## 🛠 Solución de problemas

**`command not found: streamlit`** → ejecuta `pip install streamlit` primero.

**Puerto ocupado** → usa `streamlit run app.py --server.port 8502`

**Error con matplotlib/scipy** → ejecuta `pip install matplotlib scipy`

---

*Universidad Politécnica de Chiapas · Emmanuel Urbina Guerrero*