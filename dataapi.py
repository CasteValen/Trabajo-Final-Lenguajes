from fastapi import FastAPI, HTTPException
from typing import Optional
import pandas as pd
import os

# --------------------------------------------------
# CONFIGURACIÓN INICIAL
# --------------------------------------------------

# Rutas a los archivos resumidos (Paso 8 del plan)
DATA_DIR = "data_api"  # carpeta donde guardaste los CSV de los ejes
FILE_EJE1 = os.path.join(DATA_DIR, "eje1_top_generos_roi.csv")
FILE_EJE2 = os.path.join(DATA_DIR, "eje2_roi_por_pais.csv")
FILE_EJE3 = os.path.join(DATA_DIR, "eje3_resultados.csv")  # opcional / personalizable

app = FastAPI(
    title="Mini API TMDB",
    description="Mini API para exponer los resultados de los ejes de análisis del TP final.",
    version="1.0.0"
)

# --------------------------------------------------
# CARGA DE DATOS EN MEMORIA
# --------------------------------------------------

def cargar_csv_seguro(path: str) -> pd.DataFrame:
    """Carga un CSV y tira un error claro si no existe."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    return pd.read_csv(path)

try:
    df_eje1 = cargar_csv_seguro(FILE_EJE1)
except FileNotFoundError:
    df_eje1 = None

try:
    df_eje2 = cargar_csv_seguro(FILE_EJE2)
except FileNotFoundError:
    df_eje2 = None

# Si tu tercer eje no lo querés en API, podés borrar todo lo relacionado a df_eje3
try:
    df_eje3 = cargar_csv_seguro(FILE_EJE3)
except FileNotFoundError:
    df_eje3 = None

# --------------------------------------------------
# ENDPOINT RAÍZ
# --------------------------------------------------

@app.get("/")
def raiz():
    """
    Endpoint raíz: muestra info básica de la API.
    """
    return {
        "mensaje": "API del Trabajo Final TMDB",
        "endpoints_disponibles": [
            "/top_generos",
            "/roi_por_pais",
            "/eje3"
        ]
    }

# --------------------------------------------------
# ENDPOINT 1: TOP GÉNEROS (EJE 1)
#   Ejemplo de columnas esperadas:
#   genre, roi_promedio, cantidad_peliculas
# --------------------------------------------------

@app.get("/top_generos")
def top_generos(
    limite: int = 10,
    ordenar_por: str = "roi_promedio"
):
    """
    Devuelve el top de géneros según el ROI promedio (o la métrica que elijas).

    Parámetros:
    - limite: cantidad de filas a devolver
    - ordenar_por: columna por la cual ordenar (de mayor a menor)
    """
    if df_eje1 is None:
        raise HTTPException(status_code=500, detail="Datos del Eje 1 no disponibles.")

    if ordenar_por not in df_eje1.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Columna '{ordenar_por}' no existe en los datos del Eje 1."
        )

    df_ordenado = df_eje1.sort_values(by=ordenar_por, ascending=False)
    resultado = df_ordenado.head(limite)

    return {
        "descripcion": "Top géneros según el análisis del Eje 1.",
        "total_registros": int(len(df_eje1)),
        "limite": limite,
        "ordenado_por": ordenar_por,
        "datos": resultado.to_dict(orient="records")
    }

# --------------------------------------------------
# ENDPOINT 2: ROI POR PAÍS (EJE 2)
#   Ejemplo de columnas esperadas:
#   country, roi_promedio, cantidad_peliculas
# --------------------------------------------------

@app.get("/roi_por_pais")
def roi_por_pais(
    min_peliculas: int = 20,
    ordenar_por: str = "roi_promedio"
):
    """
    Devuelve el ROI promedio por país, filtrando países con pocas películas.

    Parámetros:
    - min_peliculas: mínimo de películas para considerar un país
    - ordenar_por: columna por la cual ordenar (de mayor a menor)
    """
    if df_eje2 is None:
        raise HTTPException(status_code=500, detail="Datos del Eje 2 no disponibles.")

    columnas = df_eje2.columns
    if "cantidad_peliculas" not in columnas:
        raise HTTPException(
            status_code=400,
            detail="Se espera una columna 'cantidad_peliculas' en los datos del Eje 2."
        )

    if ordenar_por not in columnas:
        raise HTTPException(
            status_code=400,
            detail=f"Columna '{ordenar_por}' no existe en los datos del Eje 2."
        )

    df_filtrado = df_eje2[df_eje2["cantidad_peliculas"] >= min_peliculas]
    df_ordenado = df_filtrado.sort_values(by=ordenar_por, ascending=False)

    return {
        "descripcion": "ROI promedio por país según el análisis del Eje 2.",
        "min_peliculas": min_peliculas,
        "total_paises_resultado": int(len(df_ordenado)),
        "ordenado_por": ordenar_por,
        "datos": df_ordenado.to_dict(orient="records")
    }

# --------------------------------------------------
# ENDPOINT 3: EJE 3 (GENÉRICO)
#   Acá podés exponer lo que sea tu tercer eje:
#   directores más rentables, décadas más taquilleras, co-actuación, etc.
# --------------------------------------------------

@app.get("/eje3")
def eje3(
    limite: int = 20
):
    """
    Devuelve los resultados del tercer eje de análisis.

    Adaptá nombres de columnas y lógica según tu Eje 3.
    """
    if df_eje3 is None:
        raise HTTPException(status_code=500, detail="Datos del Eje 3 no disponibles.")

    resultado = df_eje3.head(limite)

    return {
        "descripcion": "Resultados del Eje 3 del análisis.",
        "limite": limite,
        "datos": resultado.to_dict(orient="records")
    }
