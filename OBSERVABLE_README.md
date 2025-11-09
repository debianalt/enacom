# Visualizaciones ENACOM con Observable Framework

Este proyecto contiene visualizaciones científicas y elegantes de los datos de conectividad a Internet de ENACOM para la provincia de Misiones, Argentina.

## 📊 Contenido

El proyecto incluye tres páginas principales:

1. **Inicio** (`/`): Análisis general de conectividad con resúmenes estadísticos
2. **Tecnologías** (`/tecnologias`): Análisis detallado de tecnologías de acceso
3. **Velocidades** (`/velocidades`): Análisis de velocidades de conexión y brecha digital

## 🚀 Instalación y Uso

### Prerrequisitos

- Node.js 18 o superior
- npm o yarn

### Instalación

1. Clona el repositorio (o haz pull de los cambios):
```bash
git pull origin claude/observable-variables-analysis-011CUxWSikCwgvjzPnRHkbL2
```

2. Instala las dependencias:
```bash
npm install
```

### Ejecutar el servidor de desarrollo

```bash
npm run dev
```

Esto iniciará el servidor en `http://localhost:3000`

### Construir para producción

```bash
npm run build
```

Esto generará el sitio estático en la carpeta `dist/`

## 📁 Estructura del Proyecto

```
enacom/
├── src/
│   ├── index.md              # Página principal
│   ├── tecnologias.md        # Análisis de tecnologías
│   ├── velocidades.md        # Análisis de velocidades
│   └── data/                 # Datos CSV
│       ├── Internet Accesos Tecnologias Localidades_misiones.csv
│       └── Internet Accesos Velocidad Localidades_Misiones.csv
├── observablehq.config.js    # Configuración de Observable
└── package.json              # Dependencias del proyecto
```

## 📈 Visualizaciones Incluidas

### Página Principal
- Resumen estadístico general (total de accesos, localidades, partidos)
- Distribución de accesos por tecnología
- Top 10 localidades por número de accesos
- Análisis de velocidades de conexión
- Mapa de calor de tecnologías por partido

### Tecnologías
- Tabla comparativa de estadísticas por tecnología
- Participación de mercado (gráfico de barras apiladas y torta)
- Selector interactivo por tecnología
- Análisis de cobertura y diversidad tecnológica
- Comparación ADSL vs Fibra Óptica

### Velocidades
- Estadísticas descriptivas (promedio ponderado, mediana)
- Distribución de velocidades por rangos
- Top localidades por velocidad promedio
- Análisis de brecha digital
- Velocidades más contratadas
- Selector interactivo por partido
- Mapa de calor de velocidades por localidad

## 🎨 Características

- **Interactividad**: Selectores para filtrar datos por tecnología o partido
- **Tooltips**: Información detallada al pasar el mouse
- **Diseño Responsivo**: Se adapta a diferentes tamaños de pantalla
- **Gráficos Científicos**: Escalas apropiadas, ejes etiquetados, leyendas claras
- **Paletas de Colores**: Esquemas de colores profesionales y accesibles

## 📊 Datos

Los datos provienen de ENACOM (Ente Nacional de Comunicaciones) y contienen información sobre:

- Accesos a Internet por tecnología (ADSL, Cable Módem, Fibra Óptica, Wireless, Satelital)
- Velocidades de conexión en Mbps
- Distribución geográfica por localidades y partidos de Misiones

## 🔧 Personalización

Para modificar las visualizaciones, edita los archivos `.md` en la carpeta `src/`.
El framework utiliza:

- **D3.js**: Para manipulación de datos
- **Observable Plot**: Para gráficos
- **Inputs**: Para controles interactivos

## 📝 Notas

- Los datos están actualizados según la última información disponible de ENACOM
- Las velocidades están expresadas en Mbps (Megabits por segundo)
- Se filtran algunos valores atípicos para mejorar la visualización

## 🤝 Contribuciones

Para contribuir o reportar problemas, por favor abre un issue o pull request en el repositorio.

---

**Creado con Observable Framework** - https://observablehq.com/framework
