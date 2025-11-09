---
title: Conectividad a Internet en Misiones
toc: true
---

# Análisis de Conectividad a Internet en Misiones

<div class="note" style="background: #f8f9fa; padding: 1.5rem; border-left: 4px solid #0066cc; margin: 2rem 0;">

Este análisis examina el estado de la conectividad a Internet en la provincia de Misiones, Argentina, utilizando datos oficiales del Ente Nacional de Comunicaciones (ENACOM). Se enfoca en la distribución geográfica de tecnologías de acceso y velocidades de conexión, identificando patrones de desarrollo digital y brechas en la infraestructura.

</div>

```js
import * as d3 from "npm:d3";
```

```js
const tecnologias = await FileAttachment("data/Internet Accesos Tecnologias Localidades_misiones.csv").csv({typed: true});
const velocidades = await FileAttachment("data/Internet Accesos Velocidad Localidades_Misiones.csv").csv({typed: true});
```

---

## Resumen Ejecutivo

```js
const totalAccesos = d3.sum(tecnologias, d => parseInt(d.Accesos) || 0);
const totalLocalidades = new Set(tecnologias.map(d => d.Localidad)).size;
const totalPartidos = new Set(tecnologias.map(d => d.Partido)).size;

// Velocidad promedio ponderada
const velocidadesFiltradas = velocidades.filter(d => {
  const vel = parseFloat(d.Velocidad);
  return vel > 0 && vel < 200 && parseInt(d.Accesos) > 0;
});

const velocidadPromedio = velocidadesFiltradas.length > 0
  ? d3.sum(velocidadesFiltradas, d => parseFloat(d.Velocidad) * parseInt(d.Accesos)) /
    d3.sum(velocidadesFiltradas, d => parseInt(d.Accesos))
  : 0;
```

<div class="grid grid-cols-4" style="margin: 2rem 0;">
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #0066cc; margin-bottom: 0.5rem;">
      ${(totalAccesos / 1000).toFixed(0)}k
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      Total Accesos
    </div>
  </div>
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #0066cc; margin-bottom: 0.5rem;">
      ${totalLocalidades}
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      Localidades
    </div>
  </div>
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #0066cc; margin-bottom: 0.5rem;">
      ${totalPartidos}
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      Partidos
    </div>
  </div>
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #0066cc; margin-bottom: 0.5rem;">
      ${velocidadPromedio.toFixed(0)}
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      Mbps Promedio
    </div>
  </div>
</div>

---

## Distribución de Tecnologías de Acceso

```js
const porTecnologia = d3.rollups(
  tecnologias.filter(d => d.Tecnologia && d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => parseInt(d.Accesos) || 0),
  d => d.Tecnologia
)
  .map(([tecnologia, accesos]) => ({tecnologia, accesos}))
  .sort((a, b) => b.accesos - a.accesos);

const totalTec = d3.sum(porTecnologia, d => d.accesos);
```

```js
Plot.plot({
  marginLeft: 140,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 50,
  height: 400,
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
    domain: porTecnologia.map(d => d.tecnologia),
    range: ["#0066cc", "#99c2e6", "#666666", "#b3b3b3", "#e6e6e6"]
  },
  marks: [
    Plot.barX(porTecnologia, {
      x: "accesos",
      y: "tecnologia",
      fill: "tecnologia",
      sort: {y: "-x"},
      tip: {
        format: {
          x: true,
          y: true,
          fill: false
        }
      }
    }),
    Plot.text(porTecnologia, {
      x: "accesos",
      y: "tecnologia",
      text: d => `${d.accesos.toLocaleString()} (${(d.accesos/totalTec*100).toFixed(1)}%)`,
      dx: 5,
      textAnchor: "start",
      fill: "#666",
      fontSize: 11
    }),
    Plot.ruleX([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Interpretación:** La fibra óptica y el cable módem dominan el mercado con ${((porTecnologia[0]?.accesos || 0)/totalTec*100).toFixed(0)}% y ${((porTecnologia[1]?.accesos || 0)/totalTec*100).toFixed(0)}% respectivamente. La persistencia de tecnologías satelitales (${((porTecnologia.find(d => d.tecnologia === "SATELITAL")?.accesos || 0)/totalTec*100).toFixed(1)}%) indica zonas con limitaciones de infraestructura terrestre.

</div>

---

## Concentración Geográfica de Accesos

```js
const porLocalidad = d3.rollups(
  tecnologias,
  v => d3.sum(v, d => parseInt(d.Accesos) || 0),
  d => d.Localidad,
  d => d.Partido
)
  .flatMap(([localidad, partidos]) =>
    partidos.map(([partido, accesos]) => ({localidad, partido, accesos}))
  )
  .sort((a, b) => b.accesos - a.accesos)
  .slice(0, 15);
```

```js
Plot.plot({
  marginLeft: 140,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 50,
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
    legend: true,
    scheme: "Blues",
    type: "linear"
  },
  marks: [
    Plot.barX(porLocalidad, {
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
    Plot.text(porLocalidad, {
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

**Interpretación:** Posadas concentra ${((porLocalidad[0]?.accesos || 0)/totalAccesos*100).toFixed(1)}% del total provincial, evidenciando una marcada centralización urbana. Las 15 principales localidades representan ${(d3.sum(porLocalidad, d => d.accesos)/totalAccesos*100).toFixed(1)}% de los accesos totales.

</div>

---

## Distribución de Velocidades de Conexión

```js
const rangosVelocidad = [
  {min: 0, max: 6, label: "< 6 Mbps"},
  {min: 6, max: 20, label: "6-20 Mbps"},
  {min: 20, max: 50, label: "20-50 Mbps"},
  {min: 50, max: 100, label: "50-100 Mbps"},
  {min: 100, max: 300, label: "100-300 Mbps"},
  {min: 300, max: Infinity, label: "≥ 300 Mbps"}
];

const totalAccesosVel = d3.sum(velocidades, d => parseInt(d.Accesos) || 0);

const distribucionVelocidad = rangosVelocidad.map(rango => {
  const accesos = d3.sum(
    velocidades.filter(d => {
      const vel = parseFloat(d.Velocidad);
      const acc = parseInt(d.Accesos);
      return vel >= rango.min && vel < rango.max && acc > 0;
    }),
    d => parseInt(d.Accesos) || 0
  );
  return {
    rango: rango.label,
    accesos,
    porcentaje: (accesos / totalAccesosVel) * 100
  };
}).filter(d => d.accesos > 0);
```

```js
Plot.plot({
  marginLeft: 80,
  marginRight: 60,
  marginTop: 40,
  marginBottom: 60,
  height: 400,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: null,
    tickSize: 0,
    line: true
  },
  y: {
    label: "Número de accesos →",
    labelAnchor: "top",
    labelOffset: 40,
    grid: false,
    line: true,
    tickFormat: "~s",
    tickSize: 0
  },
  color: {
    domain: distribucionVelocidad.map(d => d.rango),
    range: ["#cc0000", "#ff6666", "#99c2e6", "#0066cc", "#004499", "#002266"]
  },
  marks: [
    Plot.barY(distribucionVelocidad, {
      x: "rango",
      y: "accesos",
      fill: "rango",
      tip: {
        format: {
          x: true,
          y: true,
          fill: false
        }
      }
    }),
    Plot.text(distribucionVelocidad, {
      x: "rango",
      y: "accesos",
      text: d => `${d.porcentaje.toFixed(1)}%`,
      dy: -8,
      fill: "#666",
      fontSize: 11,
      fontWeight: "bold"
    }),
    Plot.ruleY([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Interpretación:** ${distribucionVelocidad.find(d => d.rango.includes("100"))?.porcentaje.toFixed(0) || 0}% de conexiones superan 100 Mbps, mientras que ${(distribucionVelocidad.filter(d => d.rango.includes("<") || d.rango.includes("6-20")).reduce((sum, d) => sum + d.porcentaje, 0)).toFixed(0)}% permanecen bajo 20 Mbps, indicando una brecha digital significativa en velocidad de acceso.

</div>

---

<div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e0e0e0; color: #999; font-size: 0.85rem;">

**Fuente:** Ente Nacional de Comunicaciones (ENACOM), Argentina
**Nota metodológica:** Los datos incluyen todas las tecnologías de acceso fijo a Internet. Velocidades satelitales (>200 Mbps) filtradas para análisis de velocidad promedio.

</div>
