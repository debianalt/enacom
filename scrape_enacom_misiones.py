#!/usr/bin/env python3
"""
Script para extraer datos de conectividad de ENACOM para la provincia de Misiones
y unificarlos con el shapefile de radios censales 2022.

Fuentes de datos:
- ENACOM: Datos de accesos a internet por tecnología y velocidad por localidad
- Radios Censales 2022: Shapefile de Misiones
"""

import requests
import pandas as pd
import geopandas as gpd
from pathlib import Path
import json
import time
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# API de ENACOM (basada en Junar)
API_BASE = 'http://api.datosabiertos.enacom.gob.ar/api/v2/datastreams'
API_KEY = '44a38fbffd39c9f7d84e8e7dd2e1d02f0950e611'  # API key pública

# Datasets de ENACOM
ENACOM_DATASETS = {
    'tecnologia_localidad': {
        'id': 'ACCES-A-INTER-FIJO-62463',
        'name': 'Accesos a Internet fijo por tecnología y localidad',
        'url_web': 'https://datosabiertos.enacom.gob.ar/dataviews/252830/'
    },
    'velocidad_localidad': {
        'id': 'ACCES-A-INTER-FIJO-16249',
        'name': 'Accesos a Internet fijo por velocidad de bajada y localidad',
        'url_web': 'https://datosabiertos.enacom.gob.ar/dataviews/252829/'
    },
}

# Códigos y nombres de provincia de Misiones
MISIONES_CODES = ['54']  # Código INDEC de Misiones
MISIONES_NAMES = ['Misiones', 'MISIONES']

class EnacomScraper:
    """Clase para extraer y procesar datos de ENACOM"""

    def __init__(self, output_dir='data_enacom'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def download_dataset(self, dataset_id: str, dataset_name: str, limit: int = 50000) -> pd.DataFrame:
        """
        Descarga un dataset de ENACOM usando la API de Junar
        """
        print(f"\nDescargando: {dataset_name}")
        print(f"Dataset ID: {dataset_id}")

        all_data = []
        offset = 0
        batch_size = 5000  # Descargar en lotes

        while True:
            # Construir URL de la API
            # Formato: /api/v2/datastreams/{guid}/data.pjson/?auth_key={auth_key}&limit={limit}&offset={offset}
            api_url = f"{API_BASE}/{dataset_id}/data.pjson/"
            params = {
                'auth_key': API_KEY,
                'limit': batch_size,
                'offset': offset
            }

            try:
                print(f"  Descargando lote {offset//batch_size + 1} (offset: {offset})...", end=" ")
                response = self.session.get(api_url, params=params, timeout=60)

                if response.status_code == 200:
                    data = response.json()

                    # El formato pjson tiene la estructura: {"result": [{...}, {...}]}
                    if 'result' in data and len(data['result']) > 0:
                        batch_data = data['result']
                        all_data.extend(batch_data)
                        print(f"✓ {len(batch_data)} registros")

                        # Si recibimos menos registros que el límite, es el último lote
                        if len(batch_data) < batch_size:
                            break

                        offset += batch_size
                        time.sleep(0.5)  # Pausa entre requests
                    else:
                        print("Sin más datos")
                        break
                else:
                    print(f"✗ Error HTTP {response.status_code}")
                    break

            except Exception as e:
                print(f"✗ Error: {e}")
                break

        if all_data:
            df = pd.DataFrame(all_data)
            print(f"✓ Total descargado: {len(df)} registros con {len(df.columns)} columnas")
            return df
        else:
            print(f"✗ No se pudieron descargar datos")
            return None

    def filter_misiones(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filtra los datos para quedarse solo con Misiones
        """
        if df is None or df.empty:
            return df

        # Buscar columnas que puedan contener información de provincia
        provincia_cols = [col for col in df.columns if 'provincia' in col.lower() or 'prov' in col.lower()]

        if provincia_cols:
            col = provincia_cols[0]
            # Filtrar por nombre o código de provincia
            df_filtered = df[
                df[col].astype(str).str.contains('Misiones', case=False, na=False) |
                df[col].astype(str).isin(MISIONES_CODES)
            ]
            print(f"  Filas filtradas para Misiones: {len(df_filtered)}")
            return df_filtered

        return df

    def save_data(self, df: pd.DataFrame, filename: str):
        """Guarda el dataframe en CSV y JSON"""
        if df is None or df.empty:
            return

        csv_path = self.output_dir / f"{filename}.csv"
        json_path = self.output_dir / f"{filename}.json"

        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        df.to_json(json_path, orient='records', force_ascii=False, indent=2)

        print(f"  Guardado en: {csv_path}")
        print(f"  Guardado en: {json_path}")

    def scrape_all(self):
        """Descarga todos los datasets relevantes"""
        datasets = {}

        for name, info in ENACOM_DATASETS.items():
            df = self.download_dataset(info['id'], info['name'])
            if df is not None:
                print(f"\n  Columnas disponibles: {list(df.columns)}")
                df_misiones = self.filter_misiones(df)
                if df_misiones is not None and not df_misiones.empty:
                    self.save_data(df_misiones, f"misiones_{name}")
                    datasets[name] = df_misiones
            time.sleep(2)  # Pausa entre requests

        return datasets


class ConnectivityProcessor:
    """Clase para procesar y unificar datos de conectividad con radios censales"""

    def __init__(self, shapefile_path: str):
        self.shapefile_path = Path(shapefile_path)
        self.radios_gdf = None
        self.load_shapefile()

    def load_shapefile(self):
        """Carga el shapefile de radios censales"""
        print(f"\nCargando shapefile: {self.shapefile_path}")
        try:
            self.radios_gdf = gpd.read_file(self.shapefile_path)
            print(f"✓ Shapefile cargado: {len(self.radios_gdf)} radios censales")
            print(f"  Columnas: {list(self.radios_gdf.columns)}")
            print(f"  CRS: {self.radios_gdf.crs}")
        except Exception as e:
            print(f"✗ Error al cargar shapefile: {e}")
            raise

    def geocode_localities(self, df: pd.DataFrame) -> gpd.GeoDataFrame:
        """
        Geocodifica localidades usando nominatim u otra fuente
        """
        # Por ahora, retornamos el dataframe sin geocodificar
        # Se puede implementar geocodificación usando geopy o datos del INDEC
        print("\n  Nota: Geocodificación de localidades pendiente")
        return df

    def merge_with_radios(self, connectivity_data: Dict[str, pd.DataFrame],
                         output_path: str):
        """
        Une los datos de conectividad con los radios censales
        """
        print("\nUniendo datos de conectividad con radios censales...")

        if self.radios_gdf is None:
            print("✗ Shapefile no cargado")
            return

        # Crear una copia del GeoDataFrame
        result_gdf = self.radios_gdf.copy()

        # Identificar columnas de localidad y departamento en el shapefile
        loc_cols = [col for col in result_gdf.columns if 'loc' in col.lower() or 'localidad' in col.lower()]
        dep_cols = [col for col in result_gdf.columns if 'dep' in col.lower() or 'departamento' in col.lower()]

        print(f"  Columnas de localidad encontradas: {loc_cols}")
        print(f"  Columnas de departamento encontradas: {dep_cols}")

        # Procesar cada dataset de conectividad
        for dataset_name, df in connectivity_data.items():
            if df is None or df.empty:
                continue

            print(f"\n  Procesando dataset: {dataset_name}")
            print(f"    Registros: {len(df)}")
            print(f"    Columnas: {list(df.columns)[:10]}...")  # Mostrar primeras 10 columnas

            # Intentar encontrar columnas de localidad en el dataset de ENACOM
            loc_cols_enacom = [col for col in df.columns if 'localidad' in col.lower()]
            if loc_cols_enacom:
                print(f"    Columna de localidad ENACOM: {loc_cols_enacom[0]}")

                # Crear tabla resumen por localidad
                if dataset_name == 'tecnologia_localidad':
                    # Buscar columnas de tecnología y accesos
                    tech_cols = [col for col in df.columns if 'tecnolog' in col.lower() or 'tipo' in col.lower()]
                    access_cols = [col for col in df.columns if 'acces' in col.lower() or 'cantidad' in col.lower()]

                    if tech_cols and access_cols:
                        # Crear pivot table por localidad y tecnología
                        summary = df.groupby(loc_cols_enacom[0]).sum(numeric_only=True)
                        print(f"    Resumen creado con {len(summary)} localidades")

                elif dataset_name == 'velocidad_localidad':
                    # Buscar columnas de velocidad y accesos
                    speed_cols = [col for col in df.columns if 'veloc' in col.lower() or 'bajada' in col.lower()]
                    access_cols = [col for col in df.columns if 'acces' in col.lower() or 'cantidad' in col.lower()]

                    if speed_cols and access_cols:
                        summary = df.groupby(loc_cols_enacom[0]).sum(numeric_only=True)
                        print(f"    Resumen creado con {len(summary)} localidades")

        # Agregar estadísticas generales a nivel provincial
        print("\n  Agregando estadísticas a nivel provincial...")
        for dataset_name, df in connectivity_data.items():
            if df is not None and not df.empty:
                # Calcular totales y promedios
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    prefix = dataset_name.replace('_localidad', '')
                    result_gdf[f'{prefix}_total'] = df[numeric_cols].sum().sum()
                    result_gdf[f'{prefix}_promedio'] = df[numeric_cols].mean().mean()

        # Asegurar que el directorio de salida existe
        output_path = Path(output_path)
        output_path.mkdir(exist_ok=True)

        # Guardar el resultado en múltiples formatos
        try:
            result_gdf.to_file(output_path / "radios_censales_misiones_conectividad.shp")
            print(f"\n✓ Shapefile guardado: {output_path / 'radios_censales_misiones_conectividad.shp'}")
        except Exception as e:
            print(f"✗ Error guardando shapefile: {e}")

        try:
            result_gdf.to_file(output_path / "radios_censales_misiones_conectividad.geojson",
                              driver='GeoJSON')
            print(f"✓ GeoJSON guardado: {output_path / 'radios_censales_misiones_conectividad.geojson'}")
        except Exception as e:
            print(f"✗ Error guardando GeoJSON: {e}")

        # También guardar como CSV sin geometría para análisis
        try:
            result_df = result_gdf.drop(columns='geometry')
            result_df.to_csv(output_path / "radios_censales_misiones_conectividad.csv", index=False)
            print(f"✓ CSV guardado: {output_path / 'radios_censales_misiones_conectividad.csv'}")
        except Exception as e:
            print(f"✗ Error guardando CSV: {e}")

        return result_gdf


def main():
    """Función principal"""
    print("="*80)
    print("EXTRACCIÓN DE DATOS DE CONECTIVIDAD DE ENACOM - PROVINCIA DE MISIONES")
    print("="*80)

    # Paso 1: Scraping de datos de ENACOM
    print("\n[1/3] Descargando datos de ENACOM...")
    scraper = EnacomScraper(output_dir='data_enacom')
    datasets = scraper.scrape_all()

    # Paso 2: Procesar radios censales
    print("\n[2/3] Procesando radios censales...")
    shapefile_path = 'radios_misiones_2022/json.shp'
    processor = ConnectivityProcessor(shapefile_path)

    # Paso 3: Unificar datos
    print("\n[3/3] Unificando datos...")
    result = processor.merge_with_radios(datasets, output_path='output')

    print("\n" + "="*80)
    print("✓ PROCESO COMPLETADO")
    print("="*80)


if __name__ == "__main__":
    main()
