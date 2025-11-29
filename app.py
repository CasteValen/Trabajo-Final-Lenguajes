from fastapi import FastAPI
import pandas as pd
import numpy as np 
import os

# Rutas de los archivos CSV generados por el Notebook
RUTA_ROI_GENERO = "resultados_roi_genero.csv"
RUTA_PRESUPUESTO_RATING = "resultados_presupuesto_rating.csv"
RUTA_CORRELACIONES = "correlaciones_presupuesto_rating.csv"
RUTA_TOP_DIRECTORES = "resultados_mejores_directores.csv"

# Diccionario para almacenar los datos cargados en memoria
DATA = {}

def cargar_datos_para_api():
    """Carga todos los DataFrames y aplica la limpieza final para la API."""
    try:
        # 1. Cargar estadísticas de ROI por Género (Eje 1)
        df_roi = pd.read_csv(RUTA_ROI_GENERO)
        DATA['top_generos'] = df_roi.to_dict(orient='records')
        print(f"✅ Cargado: {RUTA_ROI_GENERO} ({len(df_roi)} filas)")

        # 2. Cargar estadísticas de Presupuesto (Eje 2)
        df_presupuesto = pd.read_csv(RUTA_PRESUPUESTO_RATING) 
        # Reemplaza NaN/Inf por None, que JSON acepta como 'null'.
        df_presupuesto = df_presupuesto.replace([np.inf, -np.inf], np.nan) 
        df_presupuesto_limpio = df_presupuesto.where(pd.notna(df_presupuesto), None) 
        DATA['roi_por_categoria'] = df_presupuesto_limpio.to_dict(orient='records')
        print(f"✅ Cargado: {RUTA_PRESUPUESTO_RATING} ({len(df_presupuesto)} filas)")
        
        # 3. Cargar Correlaciones (Eje 2)
        df_corr = pd.read_csv(RUTA_CORRELACIONES)
        DATA['correlaciones'] = df_corr.to_dict(orient='records')
        print(f"✅ Cargado: {RUTA_CORRELACIONES}")
        
        # 4. Cargar TOP DIRECTORES (Eje 4)
        df_directores = pd.read_csv(RUTA_TOP_DIRECTORES)
        df_directores = df_directores.replace([np.inf, -np.inf], np.nan)
        df_directores_limpio = df_directores.where(pd.notna(df_directores), None) 
        DATA['top_directores'] = df_directores_limpio.to_dict(orient='records')
        print(f"✅ Cargado: {RUTA_TOP_DIRECTORES} ({len(df_directores)} filas)")
        
    except FileNotFoundError as e:
        print(f"❌ ERROR FATAL: Archivo de datos no encontrado: {e.filename}. ¿Corriste el Notebook?")
        raise
    except Exception as e:
        print(f"❌ ERROR FATAL durante la carga/limpieza de datos: {e}")
        raise

# Cargar los datos antes de inicializar la app
cargar_datos_para_api()

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="TMDB Movies Data API",
    description="Mini-API para servir los resultados del análisis exploratorio (Trabajo Final Lenguajes).",
    version="1.0"
)

# DEFINICIÓN DE ENDPOINTS (RUTAS)

# Endpoint 1: Eje 1 (ROI por Género)
@app.get("/top_generos", tags=["Análisis Principal (Eje 1)"])
def get_top_generos():
    """Devuelve las estadísticas de rentabilidad (ROI) por género."""
    return {"resultados": DATA['top_generos']}

# Endpoint 2: Eje 2 (ROI por Categoría de Presupuesto)
@app.get("/roi_por_categoria", tags=["Análisis Principal (Eje 2)"])
def get_roi_por_categoria():
    """Devuelve el rating promedio y el ROI mediano agrupado por categorías de presupuesto."""
    return {"resultados": DATA['roi_por_categoria']}
    
# Endpoint 3: Eje 4 (Directores)
@app.get("/top_directores", tags=["Análisis Principal (Eje 4)"]) 
def get_top_directors():
    """Devuelve el ranking de los 20 directores con mejor rating promedio y métricas de consistencia."""
    return {"resultados": DATA['top_directores']}


# Endpoint 4: Eje 2 (Correlaciones)
@app.get("/correlaciones_rating", tags=["Análisis Secundario"])
def get_correlaciones():
    """Devuelve los coeficientes de correlación entre presupuesto y rating."""
    return {"resultados": DATA['correlaciones']}

# Endpoint de Bienvenida
@app.get("/", include_in_schema=False)
def read_root():
    return {"mensaje": "¡Mini-API activa! Visita /docs para ver los endpoints interactivos."}