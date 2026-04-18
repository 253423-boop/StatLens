# 🔬 StatLens — Análisis Estadístico

Aplicación web para cargar cualquier archivo CSV y explorarlo con tablas, gráficas y pruebas estadísticas.  
Desarrollada con Python y Streamlit para la materia de **Probabilidad y Estadística · UP Chiapas**.

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

```
http://localhost:8501
```

### 4. Carga tu CSV

Haz clic en el botón de carga y selecciona cualquier archivo `.csv`.

---

## 📊 Pestañas disponibles

| Pestaña | Contenido |
|---|---|
| **📋 Vista previa** | Tabla completa con buscador y selector de filas |
| **📐 Estadísticas descriptivas** | Media, mediana, desv. est., Q1/Q3, IQR, sesgo; moda y conteos para categóricas |
| **🔢 Frecuencias** | Frec. absoluta, relativa, relativa % y acumulada; intervalos configurables |
| **🧩 Estructura** | Tipo de dato, nulos, % nulos y únicos por columna |
| **📈 Gráficas** | Histograma + curva PDF Normal + análisis de normalidad (Shapiro-Wilk) |
| **🧪 Prueba Z** | Prueba de hipótesis para la media + intervalo de confianza |

---

## 🧪 Pestaña Prueba Z — detalle

Sigue la ruta de decisión del profe Horacio (diap. 3 del PDF de Pruebas de Hipótesis):

1. **Selecciona** la variable numérica a probar
2. **Ingresa μ₀** — el valor que quieres comparar contra la media
3. **Elige el tipo de prueba:**
   - **Dos colas** → H₁: μ ≠ μ₀ (diap. 7)
   - **Cola derecha** → H₁: μ > μ₀ (diap. 5)
   - **Cola izquierda** → H₁: μ < μ₀ (diap. 6)
4. **Fija α** (0.01, 0.05 ó 0.10)
5. La app calcula automáticamente:
   - **Fórmula z** con valores sustituidos paso a paso (diap. 9)
   - **z observado**, **z crítico**, **p-valor**
   - **Intervalo de confianza** x̄ ± z_(α/2) · σ/√n (diap. 13)
   - **Veredicto** claro: ✅ SE ACEPTA H₀ / ❌ SE RECHAZA H₀
   - **Gráfica** N(0,1) con región crítica y p-valor sombreado

> ⚠️ No rechazar H₀ no significa que H₀ sea verdadera (diap. 3).

---

## 🛠 Solución de problemas

**`command not found: streamlit`** → ejecuta `pip install streamlit` primero.

**Puerto ocupado** → usa `streamlit run app.py --server.port 8502`

**Error con matplotlib/scipy** → ejecuta `pip install matplotlib scipy`

---

*Universidad Politécnica de Chiapas · Emmanuel Urbina Guerrero*