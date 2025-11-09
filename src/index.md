# Análisis de Conectividad ENACOM - Provincia de Misiones

Este análisis presenta una visualización científica y detallada de los datos de conectividad a Internet en la provincia de Misiones, Argentina, basado en datos de ENACOM (Ente Nacional de Comunicaciones).

```js
import * as d3 from "npm:d3";
```

```js
// Cargar datos de tecnologías
const tecnologias = await FileAttachment("data/Internet Accesos Tecnologias Localidades_misiones.csv").csv({typed: true});
```

```js
// Cargar datos de velocidades
const velocidades = await FileAttachment("data/Internet Accesos Velocidad Localidades_Misiones.csv").csv({typed: true});
```

## Resumen Estadístico General

```js
const totalAccesos = d3.sum(tecnologias, d => d.Accesos || 0);
const totalLocalidades = new Set(tecnologias.map(d => d.Localidad)).size;
const totalPartidos = new Set(tecnologias.map(d => d.Partido)).size;
```

<div class="grid grid-cols-3" style="margin: 2rem 0;">
  <div class="card">
    <h2 style="font-size: 2.5rem; margin: 0; color: #4169e1;">${totalAccesos.toLocaleString()}</h2>
    <p style="color: #666; margin: 0.5rem 0 0 0;">Total de Accesos</p>
  </div>
  <div class="card">
    <h2 style="font-size: 2.5rem; margin: 0; color: #228b22;">${totalLocalidades}</h2>
    <p style="color: #666; margin: 0.5rem 0 0 0;">Localidades</p>
  </div>
  <div class="card">
    <h2 style="font-size: 2.5rem; margin: 0; color: #dc143c;">${totalPartidos}</h2>
    <p style="color: #666; margin: 0.5rem 0 0 0;">Partidos</p>
  </div>
</div>

## Distribución de Accesos por Tecnología

```js
// Agrupar por tecnología
const porTecnologia = d3.rollups(
  tecnologias.filter(d => d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => d.Accesos || 0),
  d => d.Tecnologia
).map(([tecnologia, accesos]) => ({tecnologia, accesos}))
  .sort((a, b) => b.accesos - a.accesos);
```

```js
Plot.plot({
  title: "Accesos a Internet por Tecnología",
  marginLeft: 120,
  height: 400,
  x: {
    label: "Número de Accesos",
    grid: true,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  marks: [
    Plot.barX(porTecnologia, {
      x: "accesos",
      y: "tecnologia",
      fill: "#4169e1",
      sort: {y: "-x"},
      tip: true
    }),
    Plot.text(porTecnologia, {
      x: "accesos",
      y: "tecnologia",
      text: d => d.accesos.toLocaleString(),
      dx: -10,
      fill: "white",
      fontSize: 12,
      fontWeight: "bold"
    })
  ]
})
```

## Distribución Geográfica: Top 10 Localidades

```js
// Top 10 localidades por accesos
const porLocalidad = d3.rollups(
  tecnologias,
  v => d3.sum(v, d => d.Accesos || 0),
  d => d.Localidad,
  d => d.Partido
).flatMap(([localidad, partidos]) =>
  partidos.map(([partido, accesos]) => ({localidad, partido, accesos}))
).sort((a, b) => b.accesos - a.accesos)
  .slice(0, 10);
```

```js
Plot.plot({
  title: "Top 10 Localidades por Número de Accesos",
  marginLeft: 150,
  height: 450,
  x: {
    label: "Número de Accesos",
    grid: true,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  color: {
    legend: true,
    scheme: "Category10"
  },
  marks: [
    Plot.barX(porLocalidad, {
      x: "accesos",
      y: "localidad",
      fill: "partido",
      sort: {y: "-x"},
      tip: true
    }),
    Plot.text(porLocalidad, {
      x: "accesos",
      y: "localidad",
      text: d => d.accesos.toLocaleString(),
      dx: 10,
      textAnchor: "start",
      fontSize: 11
    })
  ]
})
```

## Análisis de Velocidades de Conexión

```js
// Procesar velocidades
const velocidadesAgrupadas = d3.rollups(
  velocidades.filter(d => d.Velocidad > 0 && d.Velocidad !== "0"),
  v => ({
    accesos: d3.sum(v, d => d.Accesos || 0),
    count: v.length
  }),
  d => {
    const vel = parseFloat(d.Velocidad);
    if (vel < 1) return "< 1 Mbps";
    if (vel < 10) return "1-10 Mbps";
    if (vel < 20) return "10-20 Mbps";
    if (vel < 50) return "20-50 Mbps";
    if (vel < 100) return "50-100 Mbps";
    if (vel < 300) return "100-300 Mbps";
    return "≥ 300 Mbps";
  }
).map(([rango, datos]) => ({rango, ...datos}));

// Orden correcto
const ordenRangos = [
  "< 1 Mbps",
  "1-10 Mbps",
  "10-20 Mbps",
  "20-50 Mbps",
  "50-100 Mbps",
  "100-300 Mbps",
  "≥ 300 Mbps"
];

const velocidadesOrdenadas = ordenRangos
  .map(rango => velocidadesAgrupadas.find(v => v.rango === rango))
  .filter(v => v);
```

```js
Plot.plot({
  title: "Distribución de Accesos por Rango de Velocidad",
  marginBottom: 60,
  height: 400,
  x: {
    label: "Rango de Velocidad",
    tickRotate: -45
  },
  y: {
    label: "Número de Accesos",
    grid: true,
    tickFormat: "~s"
  },
  marks: [
    Plot.barY(velocidadesOrdenadas, {
      x: "rango",
      y: "accesos",
      fill: "#228b22",
      tip: true
    }),
    Plot.text(velocidadesOrdenadas, {
      x: "rango",
      y: "accesos",
      text: d => d.accesos.toLocaleString(),
      dy: -10,
      fontSize: 11,
      fontWeight: "bold"
    })
  ]
})
```

## Penetración Tecnológica por Partido

```js
// Matriz de tecnología por partido
const matrizTecPartido = d3.rollups(
  tecnologias.filter(d => d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => d.Accesos || 0),
  d => d.Partido,
  d => d.Tecnologia
).flatMap(([partido, tecnologias]) =>
  tecnologias.map(([tecnologia, accesos]) => ({partido, tecnologia, accesos}))
);
```

```js
Plot.plot({
  title: "Mapa de Calor: Tecnologías por Partido",
  marginLeft: 200,
  marginBottom: 100,
  height: 600,
  x: {
    label: "Tecnología",
    tickRotate: -45
  },
  y: {
    label: null
  },
  color: {
    type: "log",
    scheme: "YlGnBu",
    label: "Accesos (escala log)"
  },
  marks: [
    Plot.cell(matrizTecPartido, {
      x: "tecnologia",
      y: "partido",
      fill: "accesos",
      tip: true,
      inset: 0.5
    })
  ]
})
```

---

*Datos actualizados de ENACOM - Ente Nacional de Comunicaciones de Argentina*
