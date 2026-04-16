# 🔬 StatLens — Análisis Estadístico

Aplicación web para cargar cualquier archivo CSV y explorarlo mediante tablas estadísticas.  
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
pip install streamlit pandas numpy
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

## 📊 Funciones disponibles

| Pestaña | Contenido |
|---|---|
| **Vista previa** | Tabla con búsqueda y selector de filas |
| **Estadísticas descriptivas** | Media, mediana, desv. est., Q1, Q3, IQR, sesgo para variables numéricas; moda y conteos para categóricas |
| **Frecuencias** | Tabla de frecuencia absoluta, relativa y acumulada; intervalos configurables para variables continuas |
| **Estructura** | Tipo de dato, nulos y valores únicos por columna |

---

## 🛠 Solución de problemas

**`command not found: streamlit`** → ejecuta `pip install streamlit` primero.

**Puerto ocupado** → usa `streamlit run app.py --server.port 8502`

---

*Universidad Politécnica de Chiapas · Emmanuel Urbina Guerrero*