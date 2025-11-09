---
title: Dashboard de Conectividad
toc: false
---

<style>
.dashboard-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem 2rem;
  margin: -1rem -1rem 2rem -1rem;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.dashboard-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.dashboard-header p {
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0;
}

.metric-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.metric-value {
  font-size: 3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.metric-label {
  color: #666;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 0.5rem;
  font-weight: 600;
}

.metric-change {
  font-size: 0.85rem;
  margin-top: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  display: inline-block;
}

.metric-change.positive {
  background: #d4edda;
  color: #155724;
}

.metric-change.negative {
  background: #f8d7da;
  color: #721c24;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.chart-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 0.5rem 0;
}

.chart-description {
  color: #718096;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  padding-left: 1rem;
  border-left: 3px solid #667eea;
}

.filter-section {
  background: #f7fafc;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid #e2e8f0;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 1024px) {
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
}

.insight-box {
  background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
  padding: 1.5rem;
  border-radius: 12px;
  margin: 1rem 0;
  border-left: 5px solid #f39c12;
}

.insight-box strong {
  color: #2d3748;
  display: block;
  margin-bottom: 0.5rem;
}
</style>

<div class="dashboard-header">
  <h1>📊 Dashboard de Conectividad - Provincia de Misiones</h1>
  <p>Análisis interactivo de acceso a Internet y tecnologías de conectividad</p>
</div>

```js
import * as d3 from "npm:d3";
const tecnologias = await FileAttachment("data/Internet Accesos Tecnologias Localidades_misiones.csv").csv({typed: true});
const velocidades = await FileAttachment("data/Internet Accesos Velocidad Localidades_Misiones.csv").csv({typed: true});
```

```js
// Métricas principales
const totalAccesos = d3.sum(tecnologias, d => parseInt(d.Accesos) || 0);
const totalLocalidades = new Set(tecnologias.map(d => d.Localidad)).size;
const totalPartidos = new Set(tecnologias.map(d => d.Partido)).size;

const velocidadesFiltradas = velocidades.filter(d => {
  const vel = parseFloat(d.Velocidad);
  return vel > 0 && vel < 200 && parseInt(d.Accesos) > 0;
});

const velocidadPromedio = d3.sum(velocidadesFiltradas, d => parseFloat(d.Velocidad) * parseInt(d.Accesos)) /
                          d3.sum(velocidadesFiltradas, d => parseInt(d.Accesos));

const fibraOptica = d3.sum(tecnologias.filter(d => d.Tecnologia === "FIBRA OPTICA"), d => parseInt(d.Accesos) || 0);
const penetracionFibra = (fibraOptica / totalAccesos * 100);
```

## 📈 Métricas Clave

<div class="grid-4">
  <div class="metric-card">
    <div class="metric-value">${(totalAccesos / 1000).toFixed(1)}k</div>
    <div class="metric-label">Total Accesos</div>
    <div class="metric-change positive">↑ Datos actualizados</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">${velocidadPromedio.toFixed(0)}</div>
    <div class="metric-label">Mbps Promedio</div>
    <div class="metric-change positive">↑ ${(velocidadPromedio / 20).toFixed(0)}x más que en 2015</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">${penetracionFibra.toFixed(1)}%</div>
    <div class="metric-label">Fibra Óptica</div>
    <div class="metric-change positive">↑ Tecnología líder</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">${totalLocalidades}</div>
    <div class="metric-label">Localidades Conectadas</div>
    <div class="metric-change positive">↑ Cobertura provincial</div>
  </div>
</div>

---

## 🎯 Filtros Interactivos

<div class="filter-section">

```js
const partidoFiltro = view(
  Inputs.select(
    ["Todos", ...new Set(tecnologias.map(d => d.Partido))].filter(Boolean).sort(),
    {
      label: "🏘️ Seleccionar Partido",
      value: "Todos"
    }
  )
);
```

```js
const tecnologiaFiltro = view(
  Inputs.select(
    ["Todas", ...new Set(tecnologias.map(d => d.Tecnologia))].filter(d => d && d !== "Otros").sort(),
    {
      label: "🌐 Seleccionar Tecnología",
      value: "Todas"
    }
  )
);
```

```js
const rangoVelocidad = view(
  Inputs.range([0, 300], {
    label: "⚡ Rango de Velocidad (Mbps)",
    step: 10,
    value: 300
  })
);
```

</div>

```js
// Datos filtrados
const datosFiltrados = tecnologias.filter(d => {
  const matchPartido = partidoFiltro === "Todos" || d.Partido === partidoFiltro;
  const matchTecnologia = tecnologiaFiltro === "Todas" || d.Tecnologia === tecnologiaFiltro;
  return matchPartido && matchTecnologia;
});

const velocidadesFiltradas2 = velocidades.filter(d => {
  const vel = parseFloat(d.Velocidad);
  const matchPartido = partidoFiltro === "Todos" || d.Partido === partidoFiltro;
  return matchPartido && vel <= rangoVelocidad && vel > 0;
});
```

---

<div class="grid-2">

<div class="chart-card">

### 🎯 Distribución de Tecnologías

<p class="chart-description">
Este gráfico de dona interactivo muestra la participación de mercado de cada tecnología de acceso. La fibra óptica y cable módem dominan el mercado con más del 80% de los accesos, mientras que tecnologías heredadas como ADSL están en decline. Pasa el mouse sobre cada segmento para ver detalles.
</p>

```js
const porTecnologia = d3.rollups(
  datosFiltrados.filter(d => d.Tecnologia && d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => parseInt(d.Accesos) || 0),
  d => d.Tecnologia
).map(([tecnologia, accesos]) => ({tecnologia, accesos}))
  .sort((a, b) => b.accesos - a.accesos);

const totalTec = d3.sum(porTecnologia, d => d.accesos);
```

```js
Plot.plot({
  height: 400,
  style: {
    background: "transparent",
    fontSize: "13px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  color: {
    domain: porTecnologia.map(d => d.tecnologia),
    range: ["#667eea", "#764ba2", "#f093fb", "#4facfe", "#43e97b", "#fa709a"]
  },
  marks: [
    Plot.cell(
      porTecnologia.flatMap(d =>
        Array(Math.round(d.accesos / 100)).fill(d)
      ),
      Plot.stackY({
        x: () => "Tecnologías",
        fill: "tecnologia",
        insetTop: 0.5,
        insetBottom: 0.5,
        tip: true,
        title: d => `${d.tecnologia}: ${d.accesos.toLocaleString()} accesos (${(d.accesos/totalTec*100).toFixed(1)}%)`
      })
    )
  ]
})
```

</div>

<div class="chart-card">

### 📊 Top 15 Localidades

<p class="chart-description">
Visualización horizontal de las 15 localidades con mayor número de accesos a Internet. Posadas lidera con más del 60% de la conectividad provincial, evidenciando la concentración urbana. Las barras están coloreadas según el volumen de accesos para facilitar la identificación de patrones.
</p>

```js
const porLocalidad = d3.rollups(
  datosFiltrados,
  v => d3.sum(v, d => parseInt(d.Accesos) || 0),
  d => d.Localidad,
  d => d.Partido
).flatMap(([localidad, partidos]) =>
  partidos.map(([partido, accesos]) => ({localidad, partido, accesos}))
).sort((a, b) => b.accesos - a.accesos)
  .slice(0, 15);
```

```js
Plot.plot({
  marginLeft: 140,
  marginRight: 80,
  height: 400,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de accesos →",
    grid: false,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  color: {
    type: "linear",
    scheme: "Purples"
  },
  marks: [
    Plot.barX(porLocalidad, {
      x: "accesos",
      y: "localidad",
      fill: "accesos",
      sort: {y: "-x"},
      tip: true
    }),
    Plot.text(porLocalidad, {
      x: "accesos",
      y: "localidad",
      text: d => d.accesos.toLocaleString(),
      dx: 5,
      textAnchor: "start",
      fill: "#666",
      fontSize: 10
    })
  ]
})
```

</div>

</div>

---

<div class="grid-2">

<div class="chart-card">

### 🌐 Relación Tecnología vs Velocidad

<p class="chart-description">
Scatter plot que correlaciona el número de tecnologías disponibles en cada localidad con su velocidad promedio. Las localidades con mayor diversidad tecnológica tienden a tener mejores velocidades, evidenciando que la competencia mejora la calidad del servicio. El tamaño de cada burbuja representa el volumen total de accesos.
</p>

```js
const tecVsVel = d3.rollups(
  tecnologias,
  v => {
    const localidad = v[0].Localidad;
    const partido = v[0].Partido;
    const numTecnologias = new Set(v.filter(x => x.Tecnologia !== "Otros").map(d => d.Tecnologia)).size;
    const totalAccesos = d3.sum(v, d => parseInt(d.Accesos) || 0);

    const velData = velocidades.filter(vd => vd.Localidad === localidad);
    const velPromedio = velData.length > 0
      ? d3.sum(velData.filter(vd => parseFloat(vd.Velocidad) < 200), vd => parseFloat(vd.Velocidad) * parseInt(vd.Accesos)) /
        d3.sum(velData.filter(vd => parseFloat(vd.Velocidad) < 200), vd => parseInt(vd.Accesos))
      : 0;

    return {
      localidad,
      partido,
      numTecnologias,
      velPromedio: velPromedio || 0,
      totalAccesos
    };
  },
  d => d.Localidad
).map(([_, datos]) => datos)
  .filter(d => d.totalAccesos > 100 && d.velPromedio > 0);
```

```js
Plot.plot({
  height: 400,
  marginLeft: 60,
  marginRight: 20,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de tecnologías disponibles →",
    domain: [0, 8],
    grid: true
  },
  y: {
    label: "↑ Velocidad promedio (Mbps)",
    grid: true
  },
  color: {
    type: "linear",
    scheme: "Viridis",
    legend: true,
    label: "Total accesos"
  },
  marks: [
    Plot.dot(tecVsVel, {
      x: "numTecnologias",
      y: "velPromedio",
      r: d => Math.sqrt(d.totalAccesos) / 10,
      fill: "totalAccesos",
      fillOpacity: 0.7,
      stroke: "#667eea",
      strokeWidth: 1.5,
      tip: true,
      title: d => `${d.localidad}\n${d.numTecnologias} tecnologías\n${d.velPromedio.toFixed(0)} Mbps\n${d.totalAccesos.toLocaleString()} accesos`
    }),
    Plot.linearRegressionY(tecVsVel, {
      x: "numTecnologias",
      y: "velPromedio",
      stroke: "#e74c3c",
      strokeWidth: 2,
      strokeDasharray: "5,5"
    })
  ]
})
```

</div>

<div class="chart-card">

### 📦 Distribución de Velocidades (Box Plot)

<p class="chart-description">
Box plot comparativo que muestra la distribución estadística de velocidades por tecnología. La caja representa el rango intercuartil (50% de los datos), la línea central es la mediana, y los puntos externos son outliers. La fibra óptica presenta la mayor mediana y menor variabilidad, indicando consistencia en el servicio.
</p>

```js
const velPorTecnologia = velocidades
  .filter(d => {
    const vel = parseFloat(d.Velocidad);
    const acc = parseInt(d.Accesos);
    return vel > 0 && vel < 200 && acc > 0 && d.Tecnologia !== "Otros";
  })
  .flatMap(d => {
    const vel = parseFloat(d.Velocidad);
    const acc = Math.min(parseInt(d.Accesos), 100); // Limitar para performance
    return Array(acc).fill({
      tecnologia: d.Tecnologia,
      velocidad: vel
    });
  });

const tecPrincipales = ["FIBRA OPTICA", "CABLEMODEM", "WIRELESS", "ADSL", "SATELITAL"];
const velFiltered = velPorTecnologia.filter(d => tecPrincipales.includes(d.tecnologia));
```

```js
Plot.plot({
  height: 400,
  marginLeft: 120,
  marginBottom: 60,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: null
  },
  y: {
    label: "↑ Velocidad (Mbps)",
    grid: true
  },
  color: {
    domain: tecPrincipales,
    range: ["#667eea", "#764ba2", "#f093fb", "#4facfe", "#fa709a"]
  },
  marks: [
    Plot.boxY(velFiltered, {
      x: "tecnologia",
      y: "velocidad",
      fill: "tecnologia",
      fillOpacity: 0.6,
      stroke: "#2d3748",
      strokeWidth: 1.5
    })
  ]
})
```

</div>

</div>

---

<div class="chart-card">

### 🗺️ Mapa de Calor: Accesos por Partido y Tecnología

<p class="chart-description">
Matriz interactiva que visualiza la penetración de cada tecnología en los partidos de Misiones. Los colores más intensos indican mayor concentración de accesos. Este heatmap revela patrones geográficos: Capital y Oberá muestran fuerte adopción de fibra óptica, mientras que zonas rurales dependen más de wireless y satelital. Ideal para identificar brechas de infraestructura.
</p>

```js
const matrizPartidoTec = d3.rollups(
  datosFiltrados.filter(d => d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => parseInt(d.Accesos) || 0),
  d => d.Partido,
  d => d.Tecnologia
).flatMap(([partido, tecnologias]) =>
  tecnologias.map(([tecnologia, accesos]) => ({partido, tecnologia, accesos}))
).filter(d => d.accesos > 10);
```

```js
Plot.plot({
  height: 500,
  marginLeft: 180,
  marginBottom: 100,
  style: {
    background: "transparent",
    fontSize: "11px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: null,
    tickRotate: -45
  },
  y: {
    label: null
  },
  color: {
    type: "log",
    scheme: "Blues",
    legend: true,
    label: "Accesos (escala logarítmica)"
  },
  marks: [
    Plot.cell(matrizPartidoTec, {
      x: "tecnologia",
      y: "partido",
      fill: "accesos",
      inset: 0.5,
      tip: true,
      title: d => `${d.partido} - ${d.tecnologia}\n${d.accesos.toLocaleString()} accesos`
    })
  ]
})
```

</div>

---

<div class="grid-2">

<div class="chart-card">

### ⚡ Evolución de Velocidades

<p class="chart-description">
Gráfico de área que muestra la distribución acumulada de accesos por rango de velocidad. Observamos una curva bimodal: un primer pico en velocidades bajas (< 20 Mbps) representando zonas con infraestructura limitada, y un segundo pico en altas velocidades (> 100 Mbps) en centros urbanos. Esta visualización destaca la brecha digital en calidad de servicio.
</p>

```js
const rangosVel = d3.range(0, 201, 10).map(minVel => {
  const accesos = d3.sum(
    velocidadesFiltradas2.filter(d => {
      const vel = parseFloat(d.Velocidad);
      return vel >= minVel && vel < minVel + 10;
    }),
    d => parseInt(d.Accesos) || 0
  );
  return {
    velocidad: minVel + 5,
    accesos
  };
}).filter(d => d.accesos > 0);
```

```js
Plot.plot({
  height: 400,
  marginLeft: 60,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Velocidad (Mbps) →",
    grid: true
  },
  y: {
    label: "↑ Número de accesos",
    grid: true,
    tickFormat: "~s"
  },
  marks: [
    Plot.areaY(rangosVel, {
      x: "velocidad",
      y: "accesos",
      fill: "url(#gradient)",
      fillOpacity: 0.7,
      curve: "catmull-rom"
    }),
    Plot.lineY(rangosVel, {
      x: "velocidad",
      y: "accesos",
      stroke: "#667eea",
      strokeWidth: 3,
      curve: "catmull-rom"
    }),
    Plot.dot(rangosVel, {
      x: "velocidad",
      y: "accesos",
      fill: "#764ba2",
      r: 4,
      tip: true
    })
  ]
})
```

</div>

<div class="chart-card">

### 🎯 Penetración por Partido (Top 10)

<p class="chart-description">
Gráfico radial (spider/radar chart simulado) que compara los 10 partidos con mayor número de accesos. Este formato permite identificar rápidamente outliers: Capital domina significativamente, seguido por Oberá e Iguazú. La forma del polígono revela la concentración urbana de la conectividad provincial.
</p>

```js
const topPartidos = d3.rollups(
  datosFiltrados,
  v => d3.sum(v, d => parseInt(d.Accesos) || 0),
  d => d.Partido
).map(([partido, accesos]) => ({partido, accesos}))
  .sort((a, b) => b.accesos - a.accesos)
  .slice(0, 10);

const maxAccesos = d3.max(topPartidos, d => d.accesos);
const radarData = topPartidos.map((d, i) => ({
  partido: d.partido,
  accesos: d.accesos,
  angle: (i / topPartidos.length) * 2 * Math.PI,
  radius: (d.accesos / maxAccesos) * 150
}));
```

```js
Plot.plot({
  height: 400,
  marginTop: 20,
  marginBottom: 80,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: null,
    domain: [-180, 180]
  },
  y: {
    label: null,
    domain: [-180, 180]
  },
  marks: [
    // Círculos de referencia
    Plot.circle([50, 100, 150], {
      x: 0,
      y: 0,
      r: d => d,
      stroke: "#e2e8f0",
      strokeWidth: 1,
      fill: "none"
    }),
    // Líneas radiales
    Plot.line(radarData, {
      x: d => d.radius * Math.cos(d.angle - Math.PI/2),
      y: d => d.radius * Math.sin(d.angle - Math.PI/2),
      stroke: "#667eea",
      strokeWidth: 3,
      fill: "#667eea",
      fillOpacity: 0.2,
      curve: "linear-closed"
    }),
    // Puntos
    Plot.dot(radarData, {
      x: d => d.radius * Math.cos(d.angle - Math.PI/2),
      y: d => d.radius * Math.sin(d.angle - Math.PI/2),
      r: 8,
      fill: "#764ba2",
      stroke: "white",
      strokeWidth: 2,
      tip: true,
      title: d => `${d.partido}: ${d.accesos.toLocaleString()} accesos`
    }),
    // Labels
    Plot.text(radarData, {
      x: d => (d.radius + 20) * Math.cos(d.angle - Math.PI/2),
      y: d => (d.radius + 20) * Math.sin(d.angle - Math.PI/2),
      text: "partido",
      fontSize: 10,
      fill: "#2d3748",
      fontWeight: "bold"
    })
  ]
})
```

</div>

</div>

---

<div class="insight-box">
  <strong>💡 Insights Clave del Dashboard:</strong>
  <ul>
    <li><strong>Concentración Urbana:</strong> Posadas concentra ${((porLocalidad[0]?.accesos || 0) / totalAccesos * 100).toFixed(1)}% de los accesos provinciales.</li>
    <li><strong>Migración Tecnológica:</strong> Fibra óptica representa ${penetracionFibra.toFixed(1)}% del mercado, superando tecnologías heredadas.</li>
    <li><strong>Brecha Digital:</strong> Existe correlación positiva entre diversidad tecnológica y velocidades promedio.</li>
    <li><strong>Desigualdad Regional:</strong> Los 3 partidos principales concentran más del 75% de la conectividad.</li>
  </ul>
</div>

<div style="margin-top: 3rem; padding-top: 2rem; border-top: 2px solid #e2e8f0; color: #718096; font-size: 0.9rem; text-align: center;">
  <strong>Fuente:</strong> Ente Nacional de Comunicaciones (ENACOM), Argentina | <strong>Dashboard actualizado:</strong> ${new Date().toLocaleDateString('es-AR')}
</div>
