# 🔬 StatLens — Análisis Estadístico con IA

Aplicación web para cargar cualquier CSV y explorarlo con tablas, gráficas,
pruebas estadísticas e interpretaciones automáticas con Gemini AI.
Desarrollada con Python y Streamlit · **Probabilidad y Estadística · UP Chiapas**

---

## 🗂 Archivos del proyecto

```
statlens/
├── app.py       ← la aplicación
└── README.md
```

---

## 🔑 Paso 1 — Agregar tu API Key de Gemini

1. Ve a **https://aistudio.google.com/app/apikey** (gratis con cuenta Google)
2. Crea una nueva API key y cópiala
3. Abre `app.py` con cualquier editor de texto
4. Busca la **línea 14** y reemplaza el texto entre comillas:

```python
# ANTES
GEMINI_API_KEY = "PEGA_TU_API_KEY_AQUI"

# DESPUÉS
GEMINI_API_KEY = "AIzaSyAbc123XYZ..."
```

5. Guarda el archivo

> Sin la API key los botones ✨ muestran un aviso, pero todo lo demás funciona normal.

---

## 🚀 Paso 2 — Instalar y correr

```bash
pip install streamlit pandas numpy matplotlib scipy requests
streamlit run app.py
```

Abre el navegador en **http://localhost:8501** y sube tu CSV.

---

## 📊 Pestañas y funciones de IA

| Pestaña | Qué hace | Botón ✨ IA |
|---|---|---|
| 📋 Vista previa | Tabla con buscador y selector de filas | Resumen ejecutivo del dataset |
| 📐 Estadísticas descriptivas | Media, mediana, desv. est., Q1/Q3, IQR, sesgo | Interpreta dispersiones y sesgos |
| 🔢 Frecuencias | Tabla completa con frec. acumulada e intervalos | Explica la distribución de frecuencias |
| 🧩 Estructura | Tipos de dato, nulos y valores únicos | Diagnostica calidad del dataset |
| 📈 Gráficas | Histograma + curva Normal + Shapiro-Wilk | Interpreta normalidad y sugiere distribución |
| 🧪 Prueba Z | Prueba de hipótesis completa con gráfica N(0,1) | Explica el resultado en lenguaje simple |

---

## 🧪 Cómo usar la Prueba Z

Sigue la ruta del profe Horacio (diap. 3):

1. Selecciona la variable numérica
2. Escribe el valor μ₀ que quieres comparar contra la media
3. Elige el tipo: dos colas / cola derecha / cola izquierda
4. Fija α (0.01, 0.05 ó 0.10)
5. La app muestra fórmula paso a paso, z observado, z crítico, p-valor,
   intervalo de confianza y el veredicto claro:
   - ✅ SE ACEPTA H₀
   - ❌ SE RECHAZA H₀

---

## 🛠 Solución de problemas

| Problema | Solución |
|---|---|
| command not found: streamlit | pip install streamlit |
| Puerto ocupado | streamlit run app.py --server.port 8502 |
| Error matplotlib/scipy | pip install matplotlib scipy |
| Botón IA no responde | Verifica la API key en la línea 14 de app.py |
| Error 400 de Gemini | La API key está mal copiada, revísala |

---

*Universidad Politécnica de Chiapas · Emmanuel Urbina Guerrero*