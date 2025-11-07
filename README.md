# Extracción de Datos de Conectividad ENACOM - Misiones

Este proyecto extrae y procesa datos de conectividad de ENACOM para la provincia de Misiones y los unifica con el shapefile de radios censales 2022.

## Fuentes de Datos

### 1. ENACOM - Datos de Conectividad

Los siguientes datasets están disponibles en el portal de ENACOM:

#### a) Accesos a Internet fijo por tecnología y localidad
- **URL**: https://indicadores.enacom.gob.ar/DatosAbiertos/Internet/accesos-tecnologias-localidades
- **Archivo sugerido**: `internet_accesos_tecnologia_localidad.xlsx` o `.csv`
- **Contenido**: Cantidad de accesos al servicio de Internet fija por tipo de tecnología para cada localidad declarada

#### b) Accesos a Internet fijo por velocidad de bajada y localidad
- **URL**: https://indicadores.enacom.gob.ar/DatosAbiertos/Internet/accesos-velocidad-rango-localidades
- **Archivo sugerido**: `internet_accesos_velocidad_localidad.xlsx` o `.csv`
- **Contenido**: Cantidad de accesos al servicio de Internet fija por rangos de velocidad de bajada para cada localidad

### 2. Radios Censales 2022 - Misiones

- **Ubicación**: `radios_misiones_2022/json.shp`
- **Contenido**: Shapefile con 2,028 radios censales de la provincia de Misiones
- **CRS**: EPSG:4326 (WGS84)

## Instrucciones de Uso

### Opción 1: Descarga Manual (Recomendado)

1. **Descargar datos de ENACOM manualmente:**

   a) Visita: https://indicadores.enacom.gob.ar/DatosAbiertos/Internet/default

   b) Descarga los siguientes archivos en formato Excel (.xlsx) o CSV:
      - Accesos a Internet por tecnología y localidad
      - Accesos a Internet por velocidad de bajada y localidad

   c) Coloca los archivos descargados en el directorio `data_enacom/` con los nombres:
      - `internet_accesos_tecnologia_localidad.xlsx` (o `.csv`)
      - `internet_accesos_velocidad_localidad.xlsx` (o `.csv`)

2. **Ejecutar el script de procesamiento:**
   ```bash
   python3 procesar_datos_manuales.py
   ```

### Opción 2: Scraping Automático (En desarrollo)

```bash
python3 scrape_enacom_misiones.py
```

**Nota**: El scraping automático puede tener limitaciones debido a restricciones de la API de ENACOM.

## Estructura de Archivos

```
enacom/
├── README.md                           # Este archivo
├── requirements.txt                    # Dependencias Python
├── scrape_enacom_misiones.py          # Script de scraping automático
├── procesar_datos_manuales.py         # Script para procesar archivos manuales
├── data_enacom/                       # Datos descargados de ENACOM
│   ├── internet_accesos_tecnologia_localidad.xlsx
│   └── internet_accesos_velocidad_localidad.xlsx
├── radios_misiones_2022/              # Shapefile de radios censales
│   └── json.shp
└── output/                            # Resultados procesados
    ├── radios_censales_misiones_conectividad.shp
    ├── radios_censales_misiones_conectividad.geojson
    └── radios_censales_misiones_conectividad.csv
```

## Dependencias

Instalar con:
```bash
pip install -r requirements.txt
```

Paquetes necesarios:
- pandas >= 2.0.0
- geopandas >= 0.13.0
- requests >= 2.31.0
- openpyxl >= 3.1.0 (para leer archivos Excel)
- shapely >= 2.0.0
- pyproj >= 3.5.0

## Resultados

El script genera tres archivos de salida en el directorio `output/`:

1. **radios_censales_misiones_conectividad.shp** - Shapefile con datos de conectividad
2. **radios_censales_misiones_conectividad.geojson** - Formato GeoJSON para web mapping
3. **radios_censales_misiones_conectividad.csv** - Tabla de datos sin geometría

## Limitaciones Conocidas

- La API de ENACOM puede requerir autenticación o tener límites de tasa
- Los datos de conectividad están agregados por localidad, no por radio censal
- Se requiere geocodificación adicional para match espacial preciso entre localidades y radios

## Fuente y Citación

Al utilizar estos datos, se debe citar a ENACOM como fuente:

> **Fuente**: ENACOM - Ente Nacional de Comunicaciones
> https://enacom.gob.ar/datosabiertos

Los datos provienen de registros administrativos presentados por los prestadores bajo declaración jurada, conforme a la normativa vigente.

## Contacto y Contribuciones

Para reportar problemas o sugerir mejoras, por favor abre un issue en el repositorio.
