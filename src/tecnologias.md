# Análisis Detallado de Tecnologías

Análisis profundo de las diferentes tecnologías de acceso a Internet en la provincia de Misiones.

```js
import * as d3 from "npm:d3";
```

```js
const tecnologias = await FileAttachment("data/Internet Accesos Tecnologias Localidades_misiones.csv").csv({typed: true});
```

## Comparativa de Tecnologías

```js
// Estadísticas por tecnología
const estatsTec = d3.rollups(
  tecnologias.filter(d => d.Tecnologia !== "Otros"),
  v => ({
    totalAccesos: d3.sum(v, d => d.Accesos || 0),
    localidades: new Set(v.map(d => d.Localidad)).size,
    promedioAccesos: d3.mean(v, d => d.Accesos || 0),
    mediana: d3.median(v, d => d.Accesos || 0),
    desviacion: d3.deviation(v, d => d.Accesos || 0)
  }),
  d => d.Tecnologia
).map(([tecnologia, stats]) => ({tecnologia, ...stats}))
  .sort((a, b) => b.totalAccesos - a.totalAccesos);
```

```js
display(Inputs.table(estatsTec, {
  columns: [
    "tecnologia",
    "totalAccesos",
    "localidades",
    "promedioAccesos",
    "mediana",
    "desviacion"
  ],
  header: {
    tecnologia: "Tecnología",
    totalAccesos: "Total Accesos",
    localidades: "Localidades",
    promedioAccesos: "Promedio",
    mediana: "Mediana",
    desviacion: "Desv. Estándar"
  },
  format: {
    totalAccesos: d => d.toLocaleString(),
    promedioAccesos: d => d?.toFixed(1) || "N/A",
    mediana: d => d?.toFixed(1) || "N/A",
    desviacion: d => d?.toFixed(1) || "N/A"
  },
  width: {
    tecnologia: 150
  }
}))
```

## Participación de Mercado

```js
const participacion = estatsTec.map(d => ({
  tecnologia: d.tecnologia,
  accesos: d.totalAccesos,
  porcentaje: (d.totalAccesos / d3.sum(estatsTec, e => e.totalAccesos)) * 100
}));
```

```js
Plot.plot({
  title: "Participación de Mercado por Tecnología",
  height: 500,
  marginTop: 40,
  marginBottom: 40,
  marks: [
    Plot.barY(participacion,
      Plot.stackY({
        x: () => "Misiones",
        y: "accesos",
        fill: "tecnologia",
        tip: true,
        title: d => `${d.tecnologia}: ${d.accesos.toLocaleString()} (${d.porcentaje.toFixed(1)}%)`
      })
    ),
    Plot.ruleY([0])
  ],
  color: {
    legend: true,
    scheme: "Tableau10"
  },
  y: {
    label: "Accesos",
    grid: true,
    tickFormat: "~s"
  },
  x: {
    label: null
  }
})
```

```js
// Gráfico de torta mejorado
const pie = d3.pie()
  .value(d => d.accesos)
  .sort((a, b) => b.accesos - a.accesos);

const arc = d3.arc()
  .innerRadius(0)
  .outerRadius(200);

const labelArc = d3.arc()
  .innerRadius(140)
  .outerRadius(140);

const pieData = pie(participacion);
```

```js
{
  const width = 500;
  const height = 500;

  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [-width / 2, -height / 2, width, height])
    .attr("style", "max-width: 100%; height: auto;");

  const color = d3.scaleOrdinal()
    .domain(participacion.map(d => d.tecnologia))
    .range(d3.schemeTableau10);

  svg.append("g")
    .selectAll("path")
    .data(pieData)
    .join("path")
      .attr("fill", d => color(d.data.tecnologia))
      .attr("d", arc)
      .attr("stroke", "white")
      .attr("stroke-width", 2)
    .append("title")
      .text(d => `${d.data.tecnologia}: ${d.data.accesos.toLocaleString()} (${d.data.porcentaje.toFixed(1)}%)`);

  svg.append("g")
    .attr("font-family", "sans-serif")
    .attr("font-size", 12)
    .attr("font-weight", "bold")
    .attr("text-anchor", "middle")
    .selectAll("text")
    .data(pieData)
    .join("text")
      .attr("transform", d => `translate(${labelArc.centroid(d)})`)
      .selectAll("tspan")
      .data(d => [d.data.tecnologia, `${d.data.porcentaje.toFixed(1)}%`])
      .join("tspan")
        .attr("x", 0)
        .attr("y", (d, i) => `${i * 1.1}em`)
        .attr("fill", "white")
        .text(d => d);

  return svg.node();
}
```

## Evolución Geográfica por Tecnología

```js
// Selector de tecnología
const tecnologiaSeleccionada = view(Inputs.select(
  [...new Set(tecnologias.map(d => d.Tecnologia))].filter(t => t !== "Otros").sort(),
  {label: "Seleccionar Tecnología", value: "FIBRA OPTICA"}
));
```

```js
const datosTecnologia = tecnologias
  .filter(d => d.Tecnologia === tecnologiaSeleccionada && d.Accesos > 0)
  .sort((a, b) => b.Accesos - a.Accesos)
  .slice(0, 20);
```

```js
Plot.plot({
  title: `Top 20 Localidades con ${tecnologiaSeleccionada}`,
  marginLeft: 150,
  height: 500,
  x: {
    label: "Número de Accesos",
    grid: true,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  color: {
    type: "linear",
    scheme: "Blues"
  },
  marks: [
    Plot.barX(datosTecnologia, {
      x: "Accesos",
      y: "Localidad",
      fill: "Accesos",
      sort: {y: "-x"},
      tip: true
    }),
    Plot.text(datosTecnologia, {
      x: "Accesos",
      y: "Localidad",
      text: d => d.Accesos.toLocaleString(),
      dx: 10,
      textAnchor: "start",
      fontSize: 10
    })
  ]
})
```

## Cobertura Tecnológica

```js
// Análisis de cobertura: cuántas tecnologías hay por localidad
const coberturaLocalidad = d3.rollups(
  tecnologias,
  v => ({
    tecnologias: new Set(v.map(d => d.Tecnologia)).size,
    totalAccesos: d3.sum(v, d => d.Accesos || 0),
    partido: v[0].Partido
  }),
  d => d.Localidad
).map(([localidad, datos]) => ({localidad, ...datos}))
  .sort((a, b) => b.tecnologias - a.tecnologias)
  .slice(0, 30);
```

```js
Plot.plot({
  title: "Diversidad Tecnológica: Localidades con Mayor Número de Tecnologías",
  marginLeft: 150,
  height: 600,
  x: {
    label: "Número de Tecnologías Disponibles",
    grid: true,
    domain: [0, 8]
  },
  y: {
    label: null
  },
  marks: [
    Plot.barX(coberturaLocalidad, {
      x: "tecnologias",
      y: "localidad",
      fill: "tecnologias",
      sort: {y: "-x"},
      tip: true
    }),
    Plot.text(coberturaLocalidad, {
      x: "tecnologias",
      y: "localidad",
      text: d => `${d.tecnologias} (${d.totalAccesos.toLocaleString()} accesos)`,
      dx: 10,
      textAnchor: "start",
      fontSize: 9
    })
  ],
  color: {
    type: "linear",
    scheme: "Greens",
    label: "Tecnologías"
  }
})
```

## Comparación ADSL vs Fibra Óptica

```js
const adslVsFibra = d3.rollups(
  tecnologias.filter(d => d.Tecnologia === "ADSL" || d.Tecnologia === "FIBRA OPTICA"),
  v => {
    const adsl = v.find(x => x.Tecnologia === "ADSL");
    const fibra = v.find(x => x.Tecnologia === "FIBRA OPTICA");
    return {
      adsl: adsl?.Accesos || 0,
      fibra: fibra?.Accesos || 0,
      total: (adsl?.Accesos || 0) + (fibra?.Accesos || 0)
    };
  },
  d => d.Localidad
).map(([localidad, datos]) => ({localidad, ...datos}))
  .filter(d => d.total > 100)
  .sort((a, b) => b.total - a.total)
  .slice(0, 15);
```

```js
Plot.plot({
  title: "Migración Tecnológica: ADSL vs Fibra Óptica en Principales Localidades",
  marginLeft: 150,
  height: 500,
  x: {
    label: "Número de Accesos",
    grid: true,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  color: {
    domain: ["ADSL", "FIBRA OPTICA"],
    range: ["#dc143c", "#228b22"],
    legend: true
  },
  marks: [
    Plot.barX(adslVsFibra.flatMap(d => [
      {localidad: d.localidad, tecnologia: "ADSL", accesos: d.adsl},
      {localidad: d.localidad, tecnologia: "FIBRA OPTICA", accesos: d.fibra}
    ]), Plot.groupY(
      {x: "sum"},
      {
        x: "accesos",
        y: "localidad",
        fill: "tecnologia",
        tip: true
      }
    ))
  ]
})
```

---

*Los datos reflejan el estado actual de la infraestructura de telecomunicaciones en Misiones*
