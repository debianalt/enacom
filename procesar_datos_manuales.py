#!/usr/bin/env python3
"""
Script para procesar archivos descargados manualmente de ENACOM
y unificarlos con el shapefile de radios censales 2022 de Misiones.

Uso:
1. Descargar archivos de ENACOM manualmente desde:
   https://indicadores.enacom.gob.ar/DatosAbiertos/Internet/default

2. Colocar los archivos en data_enacom/ con los nombres:
   - internet_accesos_tecnologia_localidad.xlsx (o .csv)
   - internet_accesos_velocidad_localidad.xlsx (o .csv)

3. Ejecutar: python3 procesar_datos_manuales.py
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
import sys
import warnings
warnings.filterwarnings('ignore')


class DataProcessor:
    """Procesa datos de ENACOM y radios censales"""

    def __init__(self, data_dir='data_enacom', shapefile_path='radios_misiones_2022/json.shp'):
        self.data_dir = Path(data_dir)
        self.shapefile_path = Path(shapefile_path)
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)

        self.radios_gdf = None
        self.enacom_data = {}

    def load_enacom_files(self):
        """Carga archivos de ENACOM (Excel o CSV)"""
        print("\n" + "="*80)
        print("CARGANDO DATOS DE ENACOM")
        print("="*80)

        files_to_load = [
            ('tecnologia', 'internet_accesos_tecnologia_localidad'),
            ('velocidad', 'internet_accesos_velocidad_localidad'),
        ]

        for key, filename_base in files_to_load:
            print(f"\nBuscando: {filename_base}...")

            # Intentar cargar Excel o CSV
            for ext in ['.xlsx', '.xls', '.csv']:
                filepath = self.data_dir / f"{filename_base}{ext}"
                if filepath.exists():
                    print(f"  Encontrado: {filepath}")
                    try:
                        if ext == '.csv':
                            df = pd.read_csv(filepath, encoding='utf-8-sig')
                        else:
                            df = pd.read_excel(filepath)

                        print(f"  ✓ Cargado: {len(df)} registros, {len(df.columns)} columnas")
                        print(f"    Columnas: {list(df.columns)[:5]}...")

                        # Filtrar solo Misiones
                        df_misiones = self.filter_misiones(df)
                        if df_misiones is not None and not df_misiones.empty:
                            self.enacom_data[key] = df_misiones
                            print(f"    Registros de Misiones: {len(df_misiones)}")
                        break
                    except Exception as e:
                        print(f"  ✗ Error cargando archivo: {e}")
            else:
                print(f"  ⚠ No encontrado. Por favor descargue el archivo manualmente.")

        if not self.enacom_data:
            print("\n✗ No se cargaron datos de ENACOM.")
            print("  Por favor descargue los archivos manualmente y colóquelos en data_enacom/")
            return False

        return True

    def filter_misiones(self, df):
        """Filtra datos para la provincia de Misiones"""
        if df is None or df.empty:
            return df

        # Buscar columnas de provincia
        prov_cols = [col for col in df.columns if 'provincia' in col.lower() or 'prov' in col.lower()]

        if prov_cols:
            col = prov_cols[0]
            df_filtered = df[df[col].astype(str).str.contains('Misiones', case=False, na=False)]
            return df_filtered

        return df

    def load_shapefile(self):
        """Carga el shapefile de radios censales"""
        print("\n" + "="*80)
        print("CARGANDO SHAPEFILE DE RADIOS CENSALES")
        print("="*80)

        try:
            self.radios_gdf = gpd.read_file(self.shapefile_path)
            print(f"\n✓ Shapefile cargado: {len(self.radios_gdf)} radios censales")
            print(f"  Columnas: {list(self.radios_gdf.columns)}")
            print(f"  CRS: {self.radios_gdf.crs}")
            return True
        except Exception as e:
            print(f"✗ Error cargando shapefile: {e}")
            return False

    def analyze_data(self):
        """Analiza y muestra estadísticas de los datos"""
        print("\n" + "="*80)
        print("ANÁLISIS DE DATOS")
        print("="*80)

        for key, df in self.enacom_data.items():
            print(f"\n--- Dataset: {key} ---")
            print(f"Registros: {len(df)}")
            print(f"Columnas: {len(df.columns)}")

            # Identificar columnas clave
            localidad_cols = [col for col in df.columns if 'localidad' in col.lower()]
            accesos_cols = [col for col in df.columns if 'acces' in col.lower() or 'cantidad' in col.lower()]

            if localidad_cols:
                print(f"Columna de localidad: {localidad_cols[0]}")
                n_localidades = df[localidad_cols[0]].nunique()
                print(f"Número de localidades únicas: {n_localidades}")
                print(f"Ejemplos: {df[localidad_cols[0]].head(3).tolist()}")

            if accesos_cols:
                print(f"Columnas de accesos: {accesos_cols[:3]}")
                # Calcular totales
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    total = df[numeric_cols].sum().sum()
                    print(f"Total accesos (suma): {total:,.0f}")

    def create_summary_statistics(self):
        """Crea estadísticas resumen por localidad"""
        print("\n" + "="*80)
        print("CREANDO ESTADÍSTICAS RESUMEN")
        print("="*80)

        summaries = {}

        for key, df in self.enacom_data.items():
            # Encontrar columna de localidad
            loc_cols = [col for col in df.columns if 'localidad' in col.lower()]

            if loc_cols:
                loc_col = loc_cols[0]
                print(f"\n{key}: Agrupando por {loc_col}")

                # Crear resumen por localidad
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    summary = df.groupby(loc_col)[numeric_cols].sum()
                    summaries[key] = summary
                    print(f"  ✓ Resumen creado: {len(summary)} localidades")

                    # Guardar resumen
                    summary_path = self.output_dir / f"resumen_{key}_por_localidad.csv"
                    summary.to_csv(summary_path)
                    print(f"  Guardado: {summary_path}")

        return summaries

    def merge_data(self):
        """Une los datos de ENACOM con los radios censales"""
        print("\n" + "="*80)
        print("UNIFICANDO DATOS CON RADIOS CENSALES")
        print("="*80)

        if self.radios_gdf is None:
            print("✗ Shapefile no cargado")
            return None

        # Crear una copia del GeoDataFrame
        result_gdf = self.radios_gdf.copy()

        # Agregar estadísticas provinciales
        print("\nAgregando estadísticas a nivel provincial...")

        for key, df in self.enacom_data.items():
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                # Calcular totales
                total = df[numeric_cols].sum().sum()
                promedio = df[numeric_cols].mean().mean()

                result_gdf[f'{key}_total'] = total
                result_gdf[f'{key}_promedio'] = promedio

                print(f"  {key}: total={total:,.0f}, promedio={promedio:,.2f}")

        # Guardar resultados
        print("\n" + "="*80)
        print("GUARDANDO RESULTADOS")
        print("="*80)

        # Shapefile
        try:
            shp_path = self.output_dir / "radios_censales_misiones_conectividad.shp"
            result_gdf.to_file(shp_path)
            print(f"\n✓ Shapefile: {shp_path}")
        except Exception as e:
            print(f"✗ Error guardando shapefile: {e}")

        # GeoJSON
        try:
            geojson_path = self.output_dir / "radios_censales_misiones_conectividad.geojson"
            result_gdf.to_file(geojson_path, driver='GeoJSON')
            print(f"✓ GeoJSON: {geojson_path}")
        except Exception as e:
            print(f"✗ Error guardando GeoJSON: {e}")

        # CSV
        try:
            csv_path = self.output_dir / "radios_censales_misiones_conectividad.csv"
            result_df = result_gdf.drop(columns='geometry')
            result_df.to_csv(csv_path, index=False)
            print(f"✓ CSV: {csv_path}")
        except Exception as e:
            print(f"✗ Error guardando CSV: {e}")

        return result_gdf

    def save_enacom_data(self):
        """Guarda los datos filtrados de ENACOM"""
        print("\nGuardando datos de ENACOM filtrados para Misiones...")
        for key, df in self.enacom_data.items():
            csv_path = self.output_dir / f"enacom_misiones_{key}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"  ✓ {csv_path}")


def main():
    """Función principal"""
    print("="*80)
    print("PROCESAMIENTO DE DATOS DE CONECTIVIDAD ENACOM - MISIONES")
    print("="*80)

    processor = DataProcessor()

    # Paso 1: Cargar archivos de ENACOM
    if not processor.load_enacom_files():
        print("\n⚠ INSTRUCCIONES:")
        print("  1. Visite: https://indicadores.enacom.gob.ar/DatosAbiertos/Internet/default")
        print("  2. Descargue los archivos de accesos por tecnología y velocidad")
        print("  3. Colóquelos en data_enacom/ con los nombres indicados en README.md")
        sys.exit(1)

    # Paso 2: Cargar shapefile
    if not processor.load_shapefile():
        sys.exit(1)

    # Paso 3: Analizar datos
    processor.analyze_data()

    # Paso 4: Crear estadísticas resumen
    summaries = processor.create_summary_statistics()

    # Paso 5: Unificar con radios censales
    result = processor.merge_data()

    # Paso 6: Guardar datos de ENACOM
    processor.save_enacom_data()

    print("\n" + "="*80)
    print("✓ PROCESO COMPLETADO")
    print("="*80)
    print(f"\nRevise los resultados en el directorio: output/")


if __name__ == "__main__":
    main()
