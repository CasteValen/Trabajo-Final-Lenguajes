# Trabajo Final Lenguajes 2025: Análisis de la Industria Cinematográfica (TMDB 5000)

## 1. Descripción General del Proyecto

[cite_start]Este trabajo aplica técnicas de preprocesamiento y **Análisis Exploratorio de Datos (EDA)** sobre el dataset TMDB 5000 para descubrir patrones en la industria del cine (presupuestos, rentabilidad, rating y directores)[cite: 5].

El trabajo final consiste en cuatro entregables:
1.  [cite_start]El **Notebook** (`.ipynb`) con el análisis completo[cite: 21].
2.  [cite_start]El **Informe académico** (`.pdf`)[cite: 28].
3.  [cite_start]El **Video explicativo** de los hallazgos y la demo de la API[cite: 35].
4.  [cite_start]La **Mini-API local** para exponer los resultados clave[cite: 39].

## 2. Mini-API Local (FastAPI)

[cite_start]El objetivo de la API es servir los resultados resumidos del análisis (archivos CSV generados por el Notebook) en formato JSON, cumpliendo con el requisito integrador del curso[cite: 41].

### Archivos de Datos Servidos

La API (`app.py`) carga y sirve los siguientes archivos CSV/JSON generados por el Notebook:

* `resultados_roi_genero.csv` (Eje 1)
* `resultados_presupuesto_rating.csv` (Eje 2)
* `correlaciones_presupuesto_rating.csv` (Eje 2)
* `resultados_mejores_directores.csv` (Eje 4)

### Instrucciones de Ejecución

Para levantar el servidor local y acceder a los resultados, **debes estar en la carpeta principal del proyecto** (`Trabajo Final Lenguajes`):

1.  **Instalación de Dependencias:** Asegúrate de que el entorno virtual (`venv`) esté creado y que las librerías (`fastapi`, `uvicorn`, `pandas`, etc.) estén instaladas:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Activar el Entorno Virtual (PowerShell):** Este paso es obligatorio para que el sistema reconozca `uvicorn`.
    ```powershell
    . .\venv\Scripts\Activate.ps1
    ```

3.  **Ejecutar el Servidor:** Con el entorno activo (`(venv)` visible), inicia la API.
    ```bash
    uvicorn app:app --reload
    ```

### Endpoints de Resultados

Con el servidor activo (en `http://127.0.0.1:8000`), se puede acceder a la documentación interactiva en `/docs` para probar las rutas:

| Endpoint | Contenido (Eje de Análisis) |
| :--- | :--- |
| **`/top_generos`** | Estadísticas de Rentabilidad (ROI) por Género (Eje 1). |
| **`/roi_por_categoria`** | Estadísticas de Rating y ROI por Categoría de Presupuesto (Eje 2). |
| **`/top_directores`** | Ranking de Directores por Rating Promedio y consistencia (Eje 4). |
| **`/correlaciones_rating`**| Coeficientes de correlación (Pearson y Spearman) del Eje 2. |