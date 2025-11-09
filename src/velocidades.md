# Análisis de Velocidades de Conexión

Análisis detallado de las velocidades de acceso a Internet en la provincia de Misiones.

```js
import * as d3 from "npm:d3";
```

```js
const velocidades = await FileAttachment("data/Internet Accesos Velocidad Localidades_Misiones.csv").csv({typed: true});
```

## Estadísticas Descriptivas de Velocidad

```js
// Calcular velocidad promedio ponderada
const velocidadesFiltradas = velocidades.filter(d => {
  const vel = parseFloat(d.Velocidad);
  return vel > 0 && vel < 200 && d.Accesos > 0; // Filtrar velocidad 226.5 (satelital)
});

const velocidadPromedioPonderada = d3.sum(velocidadesFiltradas, d =>
  parseFloat(d.Velocidad) * d.Accesos
) / d3.sum(velocidadesFiltradas, d => d.Accesos);

const velocidadMediana = d3.median(
  velocidadesFiltradas.flatMap(d => Array(d.Accesos || 0).fill(parseFloat(d.Velocidad)))
);

const totalAccesosVel = d3.sum(velocidades, d => d.Accesos || 0);
```

<div class="grid grid-cols-3" style="margin: 2rem 0;">
  <div class="card">
    <h2 style="font-size: 2.5rem; margin: 0; color: #4169e1;">${velocidadPromedioPonderada.toFixed(1)} Mbps</h2>
    <p style="color: #666; margin: 0.5rem 0 0 0;">Velocidad Promedio Ponderada</p>
  </div>
  <div class="card">
    <h2 style="font-size: 2.5rem; margin: 0; color: #228b22;">${velocidadMediana?.toFixed(1) || 'N/A'} Mbps</h2>
    <p style="color: #666; margin: 0.5rem 0 0 0;">Velocidad Mediana</p>
  </div>
  <div class="card">
    <h2 style="font-size: 2.5rem; margin: 0; color: #dc143c;">${totalAccesosVel.toLocaleString()}</h2>
    <p style="color: #666; margin: 0.5rem 0 0 0;">Total de Accesos</p>
  </div>
</div>

## Distribución de Velocidades

```js
// Crear rangos de velocidad
const rangosVelocidad = [
  {min: 0, max: 1, label: "< 1 Mbps", color: "#d62728"},
  {min: 1, max: 6, label: "1-6 Mbps", color: "#ff7f0e"},
  {min: 6, max: 10, label: "6-10 Mbps", color: "#ffbb78"},
  {min: 10, max: 20, label: "10-20 Mbps", color: "#98df8a"},
  {min: 20, max: 50, label: "20-50 Mbps", color: "#2ca02c"},
  {min: 50, max: 100, label: "50-100 Mbps", color: "#1f77b4"},
  {min: 100, max: 300, label: "100-300 Mbps", color: "#9467bd"},
  {min: 300, max: Infinity, label: "≥ 300 Mbps", color: "#8c564b"}
];

const distribucionVelocidad = rangosVelocidad.map(rango => {
  const accesos = d3.sum(
    velocidades.filter(d => {
      const vel = parseFloat(d.Velocidad);
      return vel >= rango.min && vel < rango.max && d.Accesos > 0;
    }),
    d => d.Accesos || 0
  );
  return {
    rango: rango.label,
    accesos,
    color: rango.color,
    porcentaje: (accesos / totalAccesosVel) * 100
  };
}).filter(d => d.accesos > 0);
```

```js
Plot.plot({
  title: "Distribución de Accesos por Rango de Velocidad",
  marginBottom: 80,
  height: 450,
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
    Plot.barY(distribucionVelocidad, {
      x: "rango",
      y: "accesos",
      fill: "color",
      tip: true,
      title: d => `${d.rango}\n${d.accesos.toLocaleString()} accesos (${d.porcentaje.toFixed(1)}%)`
    }),
    Plot.text(distribucionVelocidad, {
      x: "rango",
      y: "accesos",
      text: d => `${d.porcentaje.toFixed(1)}%`,
      dy: -10,
      fontSize: 11,
      fontWeight: "bold"
    })
  ]
})
```

## Velocidades por Localidad

```js
// Calcular velocidad promedio por localidad
const velocidadPorLocalidad = d3.rollups(
  velocidadesFiltradas,
  v => ({
    velocidadPromedio: d3.sum(v, d => parseFloat(d.Velocidad) * d.Accesos) / d3.sum(v, d => d.Accesos),
    totalAccesos: d3.sum(v, d => d.Accesos),
    partido: v[0].Partido
  }),
  d => d.Localidad
).map(([localidad, datos]) => ({localidad, ...datos}))
  .filter(d => d.totalAccesos > 50)
  .sort((a, b) => b.velocidadPromedio - a.velocidadPromedio)
  .slice(0, 20);
```

```js
Plot.plot({
  title: "Top 20 Localidades por Velocidad Promedio (mín. 50 accesos)",
  marginLeft: 150,
  height: 500,
  x: {
    label: "Velocidad Promedio (Mbps)",
    grid: true
  },
  y: {
    label: null
  },
  color: {
    type: "linear",
    scheme: "RdYlGn",
    label: "Velocidad (Mbps)"
  },
  marks: [
    Plot.barX(velocidadPorLocalidad, {
      x: "velocidadPromedio",
      y: "localidad",
      fill: "velocidadPromedio",
      sort: {y: "-x"},
      tip: true,
      title: d => `${d.localidad}\nVelocidad: ${d.velocidadPromedio.toFixed(1)} Mbps\nAccesos: ${d.totalAccesos.toLocaleString()}`
    }),
    Plot.text(velocidadPorLocalidad, {
      x: "velocidadPromedio",
      y: "localidad",
      text: d => `${d.velocidadPromedio.toFixed(1)} Mbps`,
      dx: 10,
      textAnchor: "start",
      fontSize: 10
    })
  ]
})
```

## Análisis de Brecha Digital

```js
// Identificar localidades con baja velocidad
const localidadesBajaVelocidad = d3.rollups(
  velocidades,
  v => ({
    velocidadPromedio: d3.sum(v, d => parseFloat(d.Velocidad) * d.Accesos) / d3.sum(v, d => d.Accesos),
    totalAccesos: d3.sum(v, d => d.Accesos),
    partido: v[0].Partido,
    accesosBajaVel: d3.sum(v.filter(x => parseFloat(x.Velocidad) < 10), d => d.Accesos)
  }),
  d => d.Localidad
).map(([localidad, datos]) => ({
  localidad,
  ...datos,
  porcentajeBajaVel: (datos.accesosBajaVel / datos.totalAccesos) * 100
}))
  .filter(d => d.totalAccesos > 30 && d.porcentajeBajaVel > 50)
  .sort((a, b) => b.porcentajeBajaVel - a.porcentajeBajaVel)
  .slice(0, 15);
```

```js
Plot.plot({
  title: "Brecha Digital: Localidades con Mayor Porcentaje de Conexiones < 10 Mbps",
  marginLeft: 150,
  height: 450,
  x: {
    label: "Porcentaje de Accesos < 10 Mbps",
    domain: [0, 100],
    grid: true
  },
  y: {
    label: null
  },
  marks: [
    Plot.barX(localidadesBajaVelocidad, {
      x: "porcentajeBajaVel",
      y: "localidad",
      fill: "#dc143c",
      sort: {y: "-x"},
      tip: true,
      title: d => `${d.localidad}\n${d.porcentajeBajaVel.toFixed(1)}% < 10 Mbps\nTotal accesos: ${d.totalAccesos.toLocaleString()}`
    }),
    Plot.text(localidadesBajaVelocidad, {
      x: "porcentajeBajaVel",
      y: "localidad",
      text: d => `${d.porcentajeBajaVel.toFixed(1)}%`,
      dx: 10,
      textAnchor: "start",
      fontSize: 10,
      fontWeight: "bold"
    })
  ]
})
```

## Distribución de Velocidades Específicas

```js
// Top velocidades más comunes
const velocidadesComunes = d3.rollups(
  velocidades.filter(d => parseFloat(d.Velocidad) > 0 && parseFloat(d.Velocidad) < 200),
  v => d3.sum(v, d => d.Accesos || 0),
  d => parseFloat(d.Velocidad)
).map(([velocidad, accesos]) => ({velocidad, accesos}))
  .sort((a, b) => b.accesos - a.accesos)
  .slice(0, 15);
```

```js
Plot.plot({
  title: "Top 15 Velocidades Más Contratadas",
  marginBottom: 60,
  height: 400,
  x: {
    label: "Velocidad (Mbps)",
    tickRotate: -45
  },
  y: {
    label: "Número de Accesos",
    grid: true,
    tickFormat: "~s"
  },
  marks: [
    Plot.barY(velocidadesComunes, {
      x: d => d.velocidad.toString(),
      y: "accesos",
      fill: "#4169e1",
      tip: true,
      title: d => `${d.velocidad} Mbps: ${d.accesos.toLocaleString()} accesos`
    }),
    Plot.text(velocidadesComunes, {
      x: d => d.velocidad.toString(),
      y: "accesos",
      text: d => d.accesos.toLocaleString(),
      dy: -10,
      fontSize: 10,
      fontWeight: "bold"
    })
  ]
})
```

## Selector Interactivo: Análisis por Partido

```js
const partidoSeleccionado = view(Inputs.select(
  [...new Set(velocidades.map(d => d.Partido))].sort(),
  {label: "Seleccionar Partido", value: "Capital"}
));
```

```js
const datosPartido = velocidades.filter(d => d.Partido === partidoSeleccionado);

const distribPartido = rangosVelocidad.map(rango => {
  const accesos = d3.sum(
    datosPartido.filter(d => {
      const vel = parseFloat(d.Velocidad);
      return vel >= rango.min && vel < rango.max && d.Accesos > 0;
    }),
    d => d.Accesos || 0
  );
  const total = d3.sum(datosPartido, d => d.Accesos || 0);
  return {
    rango: rango.label,
    accesos,
    color: rango.color,
    porcentaje: total > 0 ? (accesos / total) * 100 : 0
  };
}).filter(d => d.accesos > 0);
```

```js
Plot.plot({
  title: `Distribución de Velocidades en ${partidoSeleccionado}`,
  marginBottom: 80,
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
    Plot.barY(distribPartido, {
      x: "rango",
      y: "accesos",
      fill: "color",
      tip: true,
      title: d => `${d.rango}: ${d.accesos.toLocaleString()} (${d.porcentaje.toFixed(1)}%)`
    }),
    Plot.text(distribPartido, {
      x: "rango",
      y: "accesos",
      text: d => d.porcentaje.toFixed(1) + "%",
      dy: -10,
      fontSize: 11,
      fontWeight: "bold"
    })
  ]
})
```

## Heatmap: Velocidad vs Localidad

```js
// Crear matriz de velocidad por localidad (top localidades)
const topLocalidadesVel = [...new Set(
  velocidades
    .map(d => d.Localidad)
    .filter(l => {
      const total = d3.sum(velocidades.filter(v => v.Localidad === l), v => v.Accesos || 0);
      return total > 100;
    })
)].slice(0, 20);

const matrizVelLocalidad = velocidades
  .filter(d => topLocalidadesVel.includes(d.Localidad) && parseFloat(d.Velocidad) > 0 && parseFloat(d.Velocidad) < 200)
  .map(d => ({
    localidad: d.Localidad,
    velocidad: parseFloat(d.Velocidad),
    accesos: d.Accesos || 0
  }));
```

```js
Plot.plot({
  title: "Mapa de Calor: Velocidades Disponibles por Localidad",
  marginLeft: 150,
  marginBottom: 60,
  height: 600,
  width: 900,
  x: {
    label: "Velocidad (Mbps)",
    tickRotate: -45
  },
  y: {
    label: null
  },
  color: {
    type: "log",
    scheme: "YlOrRd",
    label: "Accesos (escala log)"
  },
  marks: [
    Plot.cell(matrizVelLocalidad, {
      x: d => d.velocidad.toString(),
      y: "localidad",
      fill: "accesos",
      tip: true,
      inset: 0.5,
      title: d => `${d.localidad}\n${d.velocidad} Mbps: ${d.accesos.toLocaleString()} accesos`
    })
  ]
})
```

---

*Análisis basado en datos de ENACOM - Las velocidades están expresadas en Mbps (Megabits por segundo)*
