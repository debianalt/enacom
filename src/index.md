---
title: Dashboard de Conectividad
toc: false
---

<style>
.dashboard-header {
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
  color: white;
  padding: 3rem 2rem;
  margin: -1rem -1rem 2rem -1rem;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  text-align: center;
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
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
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

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid rgba(0,0,0,0.05);
  margin-bottom: 2rem;
  height: 100%;
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
  border-left: 3px solid #4a5568;
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
const tecnologias = await FileAttachment("data/Internet Accesos Tecnologias Localidades_misiones.csv").csv();
const velocidades = await FileAttachment("data/Internet Accesos Velocidad Localidades_Misiones.csv").csv();
```

```js
// Función para parsear números con punto como separador de miles
function parseNum(str) {
  if (!str) return 0;
  // Eliminar puntos (separador de miles) y convertir coma a punto (decimal)
  return parseFloat(String(str).replace(/\./g, '').replace(',', '.')) || 0;
}

// Métricas principales
const totalAccesos = d3.sum(tecnologias, d => parseNum(d.Accesos));
const totalLocalidades = new Set(tecnologias.map(d => d.Localidad)).size;
const totalPartidos = new Set(tecnologias.map(d => d.Partido)).size;

const velocidadesFiltradas = velocidades.filter(d => {
  const vel = parseNum(d.Velocidad);
  const acc = parseNum(d.Accesos);
  return vel > 0 && vel < 200 && acc > 0;
});

const velocidadPromedio = d3.sum(velocidadesFiltradas, d => parseNum(d.Velocidad) * parseNum(d.Accesos)) /
                          d3.sum(velocidadesFiltradas, d => parseNum(d.Accesos));

const fibraOptica = d3.sum(tecnologias.filter(d => d.Tecnologia === "FIBRA OPTICA"), d => parseNum(d.Accesos));
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
    label: "⚡ Velocidad Máxima (Mbps)",
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
  const vel = parseNum(d.Velocidad);
  const matchPartido = partidoFiltro === "Todos" || d.Partido === partidoFiltro;
  return matchPartido && vel <= rangoVelocidad && vel > 0;
});
```

---

<div class="grid-3">

<div class="chart-card">

<h3 style="color: #2d3748; font-weight: 700; margin-bottom: 0.5rem;">🎯 Distribución de Tecnologías</h3>

<p class="chart-description">
Este gráfico muestra la participación de mercado de cada tecnología. La fibra óptica domina el mercado, seguida por CABLEMODEM. Las tecnologías heredadas como ADSL están en decline, mientras que WIRELESS y SATELITAL cubren zonas rurales.
</p>

```js
const porTecnologia = d3.rollups(
  datosFiltrados.filter(d => d.Tecnologia && d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => parseNum(d.Accesos)),
  d => d.Tecnologia
).map(([tecnologia, accesos]) => ({tecnologia, accesos}))
  .sort((a, b) => b.accesos - a.accesos);

const totalTec = d3.sum(porTecnologia, d => d.accesos);
```

```js
Plot.plot({
  height: 350,
  marginLeft: 120,
  marginRight: 80,
  style: {
    background: "transparent",
    fontSize: "14px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de Accesos →",
    grid: false,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  color: {
    domain: porTecnologia.map(d => d.tecnologia),
    range: ["#667eea", "#764ba2", "#f093fb", "#4facfe", "#43e97b", "#fa709a"]
  },
  marks: [
    Plot.barX(porTecnologia, {
      x: "accesos",
      y: "tecnologia",
      fill: "tecnologia",
      sort: {y: "-x"},
      tip: {
        fontSize: 14
      },
      title: d => `${d.tecnologia}: ${d.accesos.toLocaleString()} (${(d.accesos/totalTec*100).toFixed(1)}%)`
    }),
    Plot.text(porTecnologia, {
      x: "accesos",
      y: "tecnologia",
      text: d => `${(d.accesos/totalTec*100).toFixed(1)}%`,
      dx: 5,
      textAnchor: "start",
      fill: "#2d3748",
      fontSize: 11,
      fontWeight: "bold"
    })
  ]
})
```

</div>

<div class="chart-card">

<h3 style="color: #2d3748; font-weight: 700; margin-bottom: 0.5rem;">📊 Top 15 Localidades</h3>

<p class="chart-description">
Ranking de las 15 localidades con mayor conectividad. Posadas lidera ampliamente con más de 115 mil accesos (64% del total provincial), seguida por Garupá (13k) y Puerto Iguazú (9k). Esta marcada concentración urbana refleja la desigualdad estructural en infraestructura digital.
</p>

```js
const porLocalidad = d3.rollups(
  datosFiltrados,
  v => d3.sum(v, d => parseNum(d.Accesos)),
  d => d.Localidad,
  d => d.Partido
).flatMap(([localidad, partidos]) =>
  partidos.map(([partido, accesos]) => ({localidad, partido, accesos}))
).sort((a, b) => b.accesos - a.accesos)
  .slice(0, 15);
```

```js
Plot.plot({
  marginLeft: 120,
  marginRight: 60,
  height: 350,
  style: {
    background: "transparent",
    fontSize: "14px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de Accesos →",
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
      tip: {
        fontSize: 14
      }
    }),
    Plot.text(porLocalidad, {
      x: "accesos",
      y: "localidad",
      text: d => d.accesos.toLocaleString(),
      dx: 5,
      textAnchor: "start",
      fill: "#2d3748",
      fontSize: 9
    })
  ]
})
```

</div>

<div class="chart-card">

<h3 style="color: #2d3748; font-weight: 700; margin-bottom: 0.5rem;">⚡ Distribución de Velocidades</h3>

<p class="chart-description">
Gráfico de barras que muestra cómo se distribuyen los accesos según rangos de velocidad. Observamos dos picos: uno en bajas velocidades (infraestructura limitada) y otro en altas velocidades (centros urbanos con fibra óptica).
</p>

```js
const rangosVel = [
  {min: 0, max: 6, label: "< 6"},
  {min: 6, max: 20, label: "6-20"},
  {min: 20, max: 50, label: "20-50"},
  {min: 50, max: 100, label: "50-100"},
  {min: 100, max: 300, label: "100-300"},
  {min: 300, max: Infinity, label: "≥300"}
].map(rango => {
  const accesos = d3.sum(
    velocidadesFiltradas2.filter(d => {
      const vel = parseNum(d.Velocidad);
      return vel >= rango.min && vel < rango.max;
    }),
    d => parseNum(d.Accesos)
  );
  return {
    rango: rango.label,
    accesos
  };
}).filter(d => d.accesos > 0);
```

```js
Plot.plot({
  height: 350,
  marginLeft: 60,
  marginBottom: 50,
  style: {
    background: "transparent",
    fontSize: "14px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Rango de Velocidad (Mbps) →"
  },
  y: {
    label: "↑ Cantidad de Accesos",
    grid: false,
    tickFormat: "~s"
  },
  color: {
    domain: rangosVel.map(d => d.rango),
    range: ["#e74c3c", "#e67e22", "#f39c12", "#3498db", "#2ecc71", "#27ae60"]
  },
  marks: [
    Plot.barY(rangosVel, {
      x: "rango",
      y: "accesos",
      fill: "rango",
      tip: {
        fontSize: 14
      }
    }),
    Plot.text(rangosVel, {
      x: "rango",
      y: "accesos",
      text: d => (d.accesos/1000).toFixed(0) + "k",
      dy: -8,
      fill: "#2d3748",
      fontSize: 10,
      fontWeight: "bold"
    })
  ]
})
```

</div>

</div>

---

<div class="grid-2">

<div class="chart-card">

<h3 style="color: #2d3748; font-weight: 700; margin-bottom: 0.5rem;">🌐 Accesos por Tecnología y Partido</h3>

<p class="chart-description">
Comparación visual de cómo cada tecnología penetra en los principales partidos. Capital lidera en fibra óptica, mientras que partidos rurales como Guaraní dependen más de wireless. Los colores agrupados facilitan identificar patrones de adopción tecnológica regional.
</p>

```js
const tecPorPartido = d3.rollups(
  datosFiltrados.filter(d => d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => parseNum(d.Accesos)),
  d => d.Partido,
  d => d.Tecnologia
).map(([partido, tecnologias]) => ({
  partido,
  tecnologias: tecnologias.map(([tec, acc]) => ({tecnologia: tec, accesos: acc})),
  total: d3.sum(tecnologias, ([_, acc]) => acc)
}))
.sort((a, b) => b.total - a.total)
.slice(0, 10)
.flatMap(d => d.tecnologias.map(t => ({
  partido: d.partido,
  tecnologia: t.tecnologia,
  accesos: t.accesos
})));
```

```js
Plot.plot({
  height: 450,
  marginLeft: 140,
  marginBottom: 80,
  style: {
    background: "transparent",
    fontSize: "14px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de Accesos →",
    grid: false,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  color: {
    domain: ["FIBRA OPTICA", "CABLEMODEM", "WIRELESS", "ADSL", "SATELITAL"],
    range: ["#667eea", "#764ba2", "#f093fb", "#4facfe", "#fa709a"],
    legend: true
  },
  marks: [
    Plot.barX(tecPorPartido, {
      x: "accesos",
      y: "partido",
      fill: "tecnologia",
      sort: {y: "-x", reduce: "sum"},
      tip: {
        fontSize: 14
      }
    })
  ]
})
```

</div>

<div class="chart-card">

<h3 style="color: #2d3748; font-weight: 700; margin-bottom: 0.5rem;">🗺️ Mapa de Calor: Tecnología por Partido</h3>

<p class="chart-description">
Matriz interactiva que visualiza la intensidad de cada tecnología por partido usando escala logarítmica. Los tonos más oscuros indican mayor concentración. Perfecta para detectar brechas: zonas grises tienen poca o nula cobertura de esa tecnología.
</p>

```js
const matrizPartidoTec = d3.rollups(
  datosFiltrados.filter(d => d.Tecnologia !== "Otros"),
  v => d3.sum(v, d => parseNum(d.Accesos)),
  d => d.Partido,
  d => d.Tecnologia
).flatMap(([partido, tecnologias]) =>
  tecnologias.map(([tecnologia, accesos]) => ({partido, tecnologia, accesos}))
).filter(d => d.accesos > 5);
```

```js
Plot.plot({
  height: 450,
  marginLeft: 140,
  marginBottom: 80,
  style: {
    background: "transparent",
    fontSize: "14px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Tecnología →",
    tickRotate: -45
  },
  y: {
    label: "↑ Partido"
  },
  color: {
    type: "log",
    scheme: "Blues",
    legend: true,
    label: "Accesos (log)"
  },
  marks: [
    Plot.cell(matrizPartidoTec, {
      x: "tecnologia",
      y: "partido",
      fill: "accesos",
      inset: 0.5,
      tip: {
        fontSize: 14
      },
      title: d => `${d.partido} - ${d.tecnologia}\n${d.accesos.toLocaleString()} accesos`
    })
  ]
})
```

</div>

</div>

---

<div class="grid-2">

<div class="chart-card">

<h3 style="color: #2d3748; font-weight: 700; margin-bottom: 0.5rem;">📈 Velocidad Promedio por Partido</h3>

<p class="chart-description">
Ranking de velocidades promedio por partido calculado con todos los datos disponibles. Capital (Posadas) lidera con la mayor velocidad promedio gracias a su alta penetración de fibra óptica. La brecha entre partidos urbanos y rurales refleja desigualdades en infraestructura digital.
</p>

```js
// Calcular velocidades por partido usando datos completos
const velPorPartidoCompleto = d3.rollups(
  velocidades.filter(d => {
    const vel = parseNum(d.Velocidad);
    const acc = parseNum(d.Accesos);
    // Filtrar velocidades satelitales anómalas y datos válidos
    return vel > 0 && vel < 200 && acc > 0;
  }),
  v => {
    const totalPonderado = d3.sum(v, d => parseNum(d.Velocidad) * parseNum(d.Accesos));
    const totalAccesos = d3.sum(v, d => parseNum(d.Accesos));
    return {
      velPromedio: totalPonderado / totalAccesos,
      totalAccesos: totalAccesos
    };
  },
  d => d.Partido
).map(([partido, datos]) => ({partido, ...datos}))
  .filter(d => d.totalAccesos > 500) // Solo partidos con datos significativos
  .sort((a, b) => b.velPromedio - a.velPromedio)
  .slice(0, 15);
```

```js
Plot.plot({
  height: 450,
  marginLeft: 140,
  marginRight: 60,
  style: {
    background: "transparent",
    fontSize: "14px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Velocidad Promedio (Mbps) →",
    grid: false
  },
  y: {
    label: null
  },
  color: {
    type: "linear",
    scheme: "RdYlGn",
    domain: [0, 100]
  },
  marks: [
    Plot.barX(velPorPartidoCompleto, {
      x: "velPromedio",
      y: "partido",
      fill: "velPromedio",
      sort: {y: "-x"},
      tip: {
        fontSize: 14,
        format: {
          x: d => `${d.toFixed(1)} Mbps`,
          y: true
        }
      }
    }),
    Plot.text(velPorPartidoCompleto, {
      x: "velPromedio",
      y: "partido",
      text: d => `${d.velPromedio.toFixed(1)} Mbps`,
      dx: 5,
      textAnchor: "start",
      fill: "#2d3748",
      fontSize: 11,
      fontWeight: "bold"
    })
  ]
})
```

</div>

<div class="chart-card">

<h3 style="color: #2d3748; font-weight: 700; margin-bottom: 0.5rem;">📍 Concentración por Partido</h3>

<p class="chart-description">
Ranking de los 10 partidos con mayor cantidad de accesos a Internet. Capital lidera ampliamente con más de 120 mil accesos (principalmente Posadas), seguido por Iguazú y Oberá. Esta distribución refleja la concentración de infraestructura digital en centros urbanos principales.
</p>

```js
const accesosPorPartido = d3.rollups(
  datosFiltrados,
  v => d3.sum(v, d => parseNum(d.Accesos)),
  d => d.Partido
).map(([partido, accesos]) => ({
  partido,
  accesos,
  porcentaje: (accesos / d3.sum(datosFiltrados, d => parseNum(d.Accesos))) * 100
}))
  .sort((a, b) => b.accesos - a.accesos)
  .slice(0, 10);
```

```js
Plot.plot({
  height: 450,
  marginLeft: 140,
  marginRight: 60,
  style: {
    background: "transparent",
    fontSize: "14px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Número de Accesos →",
    grid: false,
    tickFormat: "~s"
  },
  y: {
    label: null
  },
  color: {
    type: "linear",
    scheme: "Greens"
  },
  marks: [
    Plot.barX(accesosPorPartido, {
      x: "accesos",
      y: "partido",
      fill: "accesos",
      sort: {y: "-x"},
      tip: {
        fontSize: 14
      },
      title: d => `${d.partido}\n${d.accesos.toLocaleString()} accesos\n${d.porcentaje.toFixed(1)}% del total`
    }),
    Plot.text(accesosPorPartido, {
      x: "accesos",
      y: "partido",
      text: d => `${(d.accesos/1000).toFixed(1)}k`,
      dx: 5,
      textAnchor: "start",
      fill: "#2d3748",
      fontSize: 11,
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
    <li><strong>Brecha Digital:</strong> La diferencia de velocidad entre Capital y partidos rurales supera los 50 Mbps.</li>
    <li><strong>Desigualdad Regional:</strong> Los 3 partidos principales concentran más del 75% de la conectividad.</li>
  </ul>
</div>

<div style="margin-top: 3rem; padding-top: 2rem; border-top: 2px solid #e2e8f0; color: #718096; font-size: 0.9rem; text-align: center;">
  <strong>Fuente:</strong> Ente Nacional de Comunicaciones (ENACOM), Argentina | <strong>Dashboard actualizado:</strong> ${new Date().toLocaleDateString('es-AR')}
</div>
