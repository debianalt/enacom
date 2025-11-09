---
title: Análisis de Tecnologías
toc: true
---

# Análisis de Tecnologías de Acceso

<div class="note" style="background: #f8f9fa; padding: 1.5rem; border-left: 4px solid #0066cc; margin: 2rem 0;">

Este análisis examina la distribución y penetración de tecnologías de acceso a Internet en Misiones, identificando patrones de modernización tecnológica y disparidades en la disponibilidad de infraestructura avanzada.

</div>

```js
import * as d3 from "npm:d3";
const tecnologias = await FileAttachment("data/Internet Accesos Tecnologias Localidades_misiones.csv").csv({typed: true});
```

---

## Estadísticas por Tecnología

```js
const estatsTec = d3.rollups(
  tecnologias.filter(d => d.Tecnologia && d.Tecnologia !== "Otros"),
  v => ({
    totalAccesos: d3.sum(v, d => parseInt(d.Accesos) || 0),
    localidades: new Set(v.map(d => d.Localidad)).size,
    promedioAccesos: d3.mean(v, d => parseInt(d.Accesos) || 0),
    mediana: d3.median(v, d => parseInt(d.Accesos) || 0)
  }),
  d => d.Tecnologia
)
  .map(([tecnologia, stats]) => ({tecnologia, ...stats}))
  .sort((a, b) => b.totalAccesos - a.totalAccesos);
```

```js
display(
  Inputs.table(estatsTec, {
    columns: [
      "tecnologia",
      "totalAccesos",
      "localidades",
      "promedioAccesos",
      "mediana"
    ],
    header: {
      tecnologia: "Tecnología",
      totalAccesos: "Total Accesos",
      localidades: "Localidades",
      promedioAccesos: "Promedio",
      mediana: "Mediana"
    },
    format: {
      totalAccesos: d => d.toLocaleString(),
      promedioAccesos: d => d?.toFixed(0) || "—",
      mediana: d => d?.toFixed(0) || "—"
    },
    width: {
      tecnologia: 140,
      totalAccesos: 120,
      localidades: 100,
      promedioAccesos: 100,
      mediana: 100
    },
    layout: "auto"
  })
)
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Interpretación:** La mediana de accesos por localidad revela concentración: fibra óptica muestra ${estatsTec.find(d => d.tecnologia === "FIBRA OPTICA")?.mediana?.toFixed(0) || "—"} accesos/localidad (mediana), indicando despliegue focalizado en centros urbanos. Tecnologías satelitales presentan menor concentración con ${estatsTec.find(d => d.tecnologia === "SATELITAL")?.mediana?.toFixed(0) || "—"} accesos/localidad, típico de cobertura rural dispersa.

</div>

---

## Participación de Mercado

```js
const totalMercado = d3.sum(estatsTec, d => d.totalAccesos);
const participacion = estatsTec.map(d => ({
  tecnologia: d.tecnologia,
  accesos: d.totalAccesos,
  porcentaje: (d.totalAccesos / totalMercado) * 100
}));
```

```js
Plot.plot({
  marginLeft: 120,
  marginRight: 100,
  marginTop: 40,
  marginBottom: 50,
  height: 400,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Participación de mercado (%) →",
    labelAnchor: "right",
    labelOffset: 40,
    grid: false,
    line: true,
    tickSize: 0,
    domain: [0, 100]
  },
  y: {
    label: null,
    tickSize: 0,
    line: false
  },
  color: {
    domain: participacion.map(d => d.tecnologia),
    range: ["#0066cc", "#004499", "#666666", "#99c2e6", "#b3b3b3"]
  },
  marks: [
    Plot.barX(participacion, {
      x: "porcentaje",
      y: "tecnologia",
      fill: "tecnologia",
      sort: {y: "-x"},
      tip: {
        format: {
          x: d => `${d.toFixed(1)}%`,
          y: true,
          fill: false
        }
      }
    }),
    Plot.text(participacion, {
      x: "porcentaje",
      y: "tecnologia",
      text: d => `${d.porcentaje.toFixed(1)}%`,
      dx: 5,
      textAnchor: "start",
      fill: "#666",
      fontSize: 11,
      fontWeight: "bold"
    }),
    Plot.ruleX([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Interpretación:** ${participacion[0]?.tecnologia} domina con ${participacion[0]?.porcentaje.toFixed(1)}%, seguida por ${participacion[1]?.tecnologia} (${participacion[1]?.porcentaje.toFixed(1)}%). La concentración de las dos principales tecnologías (${(participacion[0]?.porcentaje + participacion[1]?.porcentaje).toFixed(1)}% del mercado) indica un patrón oligopólico típico del sector telecomunicaciones.

</div>

---

## Análisis por Tecnología Seleccionada

```js
const tecnologiaSelector = view(
  Inputs.select(
    estatsTec.map(d => d.tecnologia),
    {
      label: "Seleccionar tecnología",
      value: "FIBRA OPTICA"
    }
  )
);
```

```js
const datosTecnologia = tecnologias
  .filter(d => d.Tecnologia === tecnologiaSelector && parseInt(d.Accesos) > 0)
  .map(d => ({
    localidad: d.Localidad,
    partido: d.Partido,
    accesos: parseInt(d.Accesos) || 0
  }))
  .sort((a, b) => b.accesos - a.accesos)
  .slice(0, 20);
```

```js
Plot.plot({
  marginLeft: 140,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 50,
  height: 550,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de accesos →",
    labelAnchor: "right",
    labelOffset: 40,
    grid: false,
    line: true,
    tickFormat: "~s",
    tickSize: 0
  },
  y: {
    label: null,
    tickSize: 0,
    line: false
  },
  color: {
    type: "linear",
    scheme: "Blues"
  },
  marks: [
    Plot.barX(datosTecnologia, {
      x: "accesos",
      y: "localidad",
      fill: "accesos",
      sort: {y: "-x"},
      tip: {
        format: {
          x: true,
          y: true,
          fill: false
        }
      }
    }),
    Plot.text(datosTecnologia, {
      x: "accesos",
      y: "localidad",
      text: d => d.accesos.toLocaleString(),
      dx: 5,
      textAnchor: "start",
      fill: "#666",
      fontSize: 10
    }),
    Plot.ruleX([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Localidades principales:** ${datosTecnologia.slice(0, 3).map(d => d.localidad).join(", ")} concentran ${(d3.sum(datosTecnologia.slice(0, 3), d => d.accesos) / d3.sum(datosTecnologia, d => d.accesos) * 100).toFixed(0)}% de los accesos ${tecnologiaSelector} entre las 20 principales localidades.

</div>

---

## Diversidad Tecnológica por Localidad

```js
const coberturaLocalidad = d3.rollups(
  tecnologias,
  v => ({
    tecnologias: new Set(v.filter(x => x.Tecnologia !== "Otros").map(d => d.Tecnologia)).size,
    totalAccesos: d3.sum(v, d => parseInt(d.Accesos) || 0),
    partido: v[0]?.Partido || ""
  }),
  d => d.Localidad
)
  .map(([localidad, datos]) => ({localidad, ...datos}))
  .filter(d => d.totalAccesos > 50)
  .sort((a, b) => b.tecnologias - a.tecnologias)
  .slice(0, 25);
```

```js
Plot.plot({
  marginLeft: 140,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 50,
  height: 600,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de tecnologías disponibles →",
    labelAnchor: "right",
    labelOffset: 40,
    grid: false,
    line: true,
    tickSize: 0,
    domain: [0, 7]
  },
  y: {
    label: null,
    tickSize: 0,
    line: false
  },
  color: {
    type: "linear",
    scheme: "Greens",
    domain: [1, 7]
  },
  marks: [
    Plot.barX(coberturaLocalidad, {
      x: "tecnologias",
      y: "localidad",
      fill: "tecnologias",
      sort: {y: "-x"},
      tip: {
        format: {
          x: true,
          y: true,
          fill: false
        }
      }
    }),
    Plot.text(coberturaLocalidad, {
      x: "tecnologias",
      y: "localidad",
      text: d => d.tecnologias,
      dx: 5,
      textAnchor: "start",
      fill: "#666",
      fontSize: 11,
      fontWeight: "bold"
    }),
    Plot.ruleX([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Interpretación:** Localidades con mayor diversidad tecnológica (${coberturaLocalidad[0]?.tecnologias} tecnologías en ${coberturaLocalidad[0]?.localidad}) típicamente presentan mayor competencia y mejores opciones para usuarios. ${coberturaLocalidad.filter(d => d.tecnologias >= 5).length} localidades disponen de 5+ tecnologías, indicando mercados más desarrollados.

</div>

---

## Comparación ADSL vs Fibra Óptica

```js
const adslVsFibra = d3.rollups(
  tecnologias.filter(d => d.Tecnologia === "ADSL" || d.Tecnologia === "FIBRA OPTICA"),
  v => {
    const adsl = v.find(x => x.Tecnologia === "ADSL");
    const fibra = v.find(x => x.Tecnologia === "FIBRA OPTICA");
    return {
      adsl: parseInt(adsl?.Accesos) || 0,
      fibra: parseInt(fibra?.Accesos) || 0,
      total: (parseInt(adsl?.Accesos) || 0) + (parseInt(fibra?.Accesos) || 0)
    };
  },
  d => d.Localidad
)
  .map(([localidad, datos]) => ({localidad, ...datos}))
  .filter(d => d.total > 100)
  .sort((a, b) => b.fibra - a.fibra)
  .slice(0, 15);
```

```js
Plot.plot({
  marginLeft: 140,
  marginRight: 100,
  marginTop: 40,
  marginBottom: 70,
  height: 500,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de accesos →",
    labelAnchor: "right",
    labelOffset: 40,
    grid: false,
    line: true,
    tickFormat: "~s",
    tickSize: 0
  },
  y: {
    label: null,
    tickSize: 0,
    line: false
  },
  color: {
    domain: ["Fibra", "ADSL"],
    range: ["#0066cc", "#cc6600"],
    legend: true
  },
  marks: [
    Plot.barX(
      adslVsFibra.flatMap(d => [
        {localidad: d.localidad, tipo: "Fibra", accesos: d.fibra},
        {localidad: d.localidad, tipo: "ADSL", accesos: d.adsl}
      ]),
      {
        x: "accesos",
        y: "localidad",
        fill: "tipo",
        sort: {y: "-x", reduce: "sum"},
        tip: {
          format: {
            x: true,
            y: true,
            fill: false
          }
        }
      }
    ),
    Plot.ruleX([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Migración tecnológica:** ${adslVsFibra.filter(d => d.fibra > d.adsl).length} de ${adslVsFibra.length} localidades principales muestran predominio de fibra óptica sobre ADSL, evidenciando transición hacia tecnologías de mayor capacidad. Ratio promedio fibra/ADSL: ${(d3.sum(adslVsFibra, d => d.fibra) / d3.sum(adslVsFibra, d => d.adsl)).toFixed(1)}:1.

</div>

---

<div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e0e0e0; color: #999; font-size: 0.85rem;">

**Fuente:** Ente Nacional de Comunicaciones (ENACOM), Argentina
**Nota:** El análisis excluye la categoría "Otros" para mayor claridad. Localidades con <50 accesos excluidas del análisis de diversidad.

</div>
