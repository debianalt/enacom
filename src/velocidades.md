---
title: Análisis de Velocidades
toc: true
---

# Análisis de Velocidades de Conexión

<div class="note" style="background: #f8f9fa; padding: 1.5rem; border-left: 4px solid #0066cc; margin: 2rem 0;">

Este análisis examina la distribución de velocidades de acceso a Internet en Misiones, identificando disparidades en calidad de servicio y evidenciando la brecha digital en términos de ancho de banda disponible.

</div>

```js
import * as d3 from "npm:d3";
const velocidades = await FileAttachment("data/Internet Accesos Velocidad Localidades_Misiones.csv").csv({typed: true});
```

---

## Estadísticas Descriptivas

```js
const velocidadesFiltradas = velocidades.filter(d => {
  const vel = parseFloat(d.Velocidad);
  const acc = parseInt(d.Accesos);
  return vel > 0 && vel < 200 && acc > 0;
});

const totalAccesos = d3.sum(velocidades, d => parseInt(d.Accesos) || 0);

const velocidadPromedio = velocidadesFiltradas.length > 0
  ? d3.sum(velocidadesFiltradas, d => parseFloat(d.Velocidad) * parseInt(d.Accesos)) /
    d3.sum(velocidadesFiltradas, d => parseInt(d.Accesos))
  : 0;

const velocidadMediana = d3.median(
  velocidadesFiltradas.flatMap(d =>
    Array(Math.min(parseInt(d.Accesos) || 0, 1000)).fill(parseFloat(d.Velocidad))
  )
);

const accesosBajaVelocidad = d3.sum(
  velocidades.filter(d => parseFloat(d.Velocidad) < 20),
  d => parseInt(d.Accesos) || 0
);

const accesosAltaVelocidad = d3.sum(
  velocidades.filter(d => parseFloat(d.Velocidad) >= 100 && parseFloat(d.Velocidad) < 200),
  d => parseInt(d.Accesos) || 0
);
```

<div class="grid grid-cols-4" style="margin: 2rem 0;">
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #0066cc; margin-bottom: 0.5rem;">
      ${velocidadPromedio.toFixed(0)}
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      Mbps Promedio
    </div>
  </div>
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #0066cc; margin-bottom: 0.5rem;">
      ${velocidadMediana?.toFixed(0) || "—"}
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      Mbps Mediana
    </div>
  </div>
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #cc0000; margin-bottom: 0.5rem;">
      ${(accesosBajaVelocidad/totalAccesos*100).toFixed(0)}%
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      < 20 Mbps
    </div>
  </div>
  <div class="card" style="padding: 2rem; text-align: center; background: white; border: 1px solid #e0e0e0;">
    <div style="font-size: 3rem; font-weight: 300; color: #00aa00; margin-bottom: 0.5rem;">
      ${(accesosAltaVelocidad/totalAccesos*100).toFixed(0)}%
    </div>
    <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
      ≥ 100 Mbps
    </div>
  </div>
</div>

---

## Distribución por Rangos de Velocidad

```js
const rangosVelocidad = [
  {min: 0, max: 6, label: "< 6 Mbps", color: "#cc0000"},
  {min: 6, max: 20, label: "6-20 Mbps", color: "#ff6600"},
  {min: 20, max: 50, label: "20-50 Mbps", color: "#ffaa00"},
  {min: 50, max: 100, label: "50-100 Mbps", color: "#99c2e6"},
  {min: 100, max: 300, label: "100-300 Mbps", color: "#0066cc"},
  {min: 300, max: Infinity, label: "≥ 300 Mbps", color: "#004499"}
];

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
    color: rango.color,
    porcentaje: (accesos / totalAccesos) * 100
  };
}).filter(d => d.accesos > 0);
```

```js
Plot.plot({
  marginLeft: 100,
  marginRight: 80,
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
  marks: [
    Plot.barY(distribucionVelocidad, {
      x: "rango",
      y: "accesos",
      fill: "color",
      tip: {
        format: {
          x: true,
          y: true
        }
      }
    }),
    Plot.text(distribucionVelocidad, {
      x: "rango",
      y: "accesos",
      text: d => `${d.porcentaje.toFixed(1)}%`,
      dy: -10,
      fill: "#666",
      fontSize: 11,
      fontWeight: "bold"
    }),
    Plot.ruleY([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Interpretación:** La distribución muestra polarización: ${(accesosBajaVelocidad/totalAccesos*100).toFixed(0)}% de conexiones bajo 20 Mbps coexisten con ${(accesosAltaVelocidad/totalAccesos*100).toFixed(0)}% sobre 100 Mbps. Esta bimodalidad evidencia una brecha digital significativa en calidad de servicio.

</div>

---

## Velocidades por Localidad

```js
const velocidadPorLocalidad = d3.rollups(
  velocidadesFiltradas,
  v => ({
    velocidadPromedio: d3.sum(v, d => parseFloat(d.Velocidad) * parseInt(d.Accesos)) /
                       d3.sum(v, d => parseInt(d.Accesos)),
    totalAccesos: d3.sum(v, d => parseInt(d.Accesos)),
    partido: v[0]?.Partido || ""
  }),
  d => d.Localidad
)
  .map(([localidad, datos]) => ({localidad, ...datos}))
  .filter(d => d.totalAccesos > 100)
  .sort((a, b) => b.velocidadPromedio - a.velocidadPromedio)
  .slice(0, 20);
```

```js
Plot.plot({
  marginLeft: 150,
  marginRight: 100,
  marginTop: 40,
  marginBottom: 50,
  height: 550,
  style: {
    background: "transparent",
    fontSize: "12px",
    fontFamily: "system-ui, -apple-system, sans-serif"
  },
  x: {
    label: "Velocidad promedio (Mbps) →",
    labelAnchor: "right",
    labelOffset: 40,
    grid: false,
    line: true,
    tickSize: 0
  },
  y: {
    label: null,
    tickSize: 0,
    line: false
  },
  color: {
    type: "linear",
    scheme: "RdYlGn",
    domain: [0, 150]
  },
  marks: [
    Plot.barX(velocidadPorLocalidad, {
      x: "velocidadPromedio",
      y: "localidad",
      fill: "velocidadPromedio",
      sort: {y: "-x"},
      tip: {
        format: {
          x: d => `${d.toFixed(1)} Mbps`,
          y: true,
          fill: false
        }
      }
    }),
    Plot.text(velocidadPorLocalidad, {
      x: "velocidadPromedio",
      y: "localidad",
      text: d => `${d.velocidadPromedio.toFixed(0)} Mbps`,
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

**Interpretación:** ${velocidadPorLocalidad[0]?.localidad} lidera con ${velocidadPorLocalidad[0]?.velocidadPromedio.toFixed(0)} Mbps promedio. El rango entre la localidad más rápida y la 20ª (${velocidadPorLocalidad[19]?.velocidadPromedio.toFixed(0)} Mbps) es de ${(velocidadPorLocalidad[0]?.velocidadPromedio - velocidadPorLocalidad[19]?.velocidadPromedio).toFixed(0)} Mbps, evidenciando disparidades significativas. Análisis limitado a localidades con >100 accesos para robustez estadística.

</div>

---

## Brecha Digital: Localidades con Conexiones Lentas

```js
const localidadesBajaVelocidad = d3.rollups(
  velocidades,
  v => ({
    velocidadPromedio: d3.sum(v, d => parseFloat(d.Velocidad) * parseInt(d.Accesos)) /
                       d3.sum(v, d => parseInt(d.Accesos)),
    totalAccesos: d3.sum(v, d => parseInt(d.Accesos)),
    partido: v[0]?.Partido || "",
    accesosBajos: d3.sum(v.filter(x => parseFloat(x.Velocidad) < 10), d => parseInt(d.Accesos))
  }),
  d => d.Localidad
)
  .map(([localidad, datos]) => ({
    localidad,
    ...datos,
    porcentajeBajo: (datos.accesosBajos / datos.totalAccesos) * 100
  }))
  .filter(d => d.totalAccesos > 50 && d.porcentajeBajo > 30)
  .sort((a, b) => b.porcentajeBajo - a.porcentajeBajo)
  .slice(0, 15);
```

```js
Plot.plot({
  marginLeft: 150,
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
    label: "Porcentaje de accesos < 10 Mbps →",
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
  marks: [
    Plot.barX(localidadesBajaVelocidad, {
      x: "porcentajeBajo",
      y: "localidad",
      fill: "#cc0000",
      sort: {y: "-x"},
      tip: {
        format: {
          x: d => `${d.toFixed(1)}%`,
          y: true
        }
      }
    }),
    Plot.text(localidadesBajaVelocidad, {
      x: "porcentajeBajo",
      y: "localidad",
      text: d => `${d.porcentajeBajo.toFixed(0)}%`,
      dx: 5,
      textAnchor: "start",
      fill: "#666",
      fontSize: 10,
      fontWeight: "bold"
    }),
    Plot.ruleX([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Brecha digital:** ${localidadesBajaVelocidad.length} localidades presentan >30% de conexiones bajo 10 Mbps. ${localidadesBajaVelocidad[0]?.localidad} lidera con ${localidadesBajaVelocidad[0]?.porcentajeBajo.toFixed(0)}% de conexiones lentas, limitando acceso a servicios digitales modernos (streaming HD, videoconferencia, educación en línea).

</div>

---

## Velocidades Más Contratadas

```js
const velocidadesComunes = d3.rollups(
  velocidades.filter(d => {
    const vel = parseFloat(d.Velocidad);
    return vel > 0 && vel < 200;
  }),
  v => d3.sum(v, d => parseInt(d.Accesos) || 0),
  d => parseFloat(d.Velocidad)
)
  .map(([velocidad, accesos]) => ({velocidad, accesos}))
  .sort((a, b) => b.accesos - a.accesos)
  .slice(0, 12);
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
  marks: [
    Plot.barY(velocidadesComunes, {
      x: d => `${d.velocidad}`,
      y: "accesos",
      fill: "#0066cc",
      tip: {
        format: {
          x: d => `${d} Mbps`,
          y: true
        }
      }
    }),
    Plot.text(velocidadesComunes, {
      x: d => `${d.velocidad}`,
      y: "accesos",
      text: d => (d.accesos / 1000).toFixed(0) + "k",
      dy: -8,
      fill: "#666",
      fontSize: 10,
      fontWeight: "bold"
    }),
    Plot.ruleY([0], {stroke: "#666", strokeWidth: 1})
  ]
})
```

<div class="note" style="background: #f8f9fa; padding: 1rem; margin: 1rem 0; font-size: 0.9rem; color: #666;">

**Preferencias del mercado:** ${velocidadesComunes[0]?.velocidad} Mbps es el plan más contratado (${(velocidadesComunes[0]?.accesos / totalAccesos * 100).toFixed(1)}% del mercado), seguido por ${velocidadesComunes[1]?.velocidad} Mbps (${(velocidadesComunes[1]?.accesos / totalAccesos * 100).toFixed(1)}%). Los tres planes más populares concentran ${(d3.sum(velocidadesComunes.slice(0,3), d => d.accesos) / totalAccesos * 100).toFixed(0)}% del mercado.

</div>

---

## Análisis por Partido

```js
const partidoSelector = view(
  Inputs.select(
    [...new Set(velocidades.map(d => d.Partido))].filter(Boolean).sort(),
    {
      label: "Seleccionar partido",
      value: "Capital"
    }
  )
);
```

```js
const datosPartido = velocidades.filter(d => d.Partido === partidoSelector);

const distribPartido = rangosVelocidad.map(rango => {
  const accesos = d3.sum(
    datosPartido.filter(d => {
      const vel = parseFloat(d.Velocidad);
      const acc = parseInt(d.Accesos);
      return vel >= rango.min && vel < rango.max && acc > 0;
    }),
    d => parseInt(d.Accesos) || 0
  );
  const total = d3.sum(datosPartido, d => parseInt(d.Accesos) || 0);
  return {
    rango: rango.label,
    accesos,
    color: rango.color,
    porcentaje: total > 0 ? (accesos / total) * 100 : 0
  };
}).filter(d => d.accesos > 0);

const totalPartido = d3.sum(distribPartido, d => d.accesos);
const velocidadPromedioPartido = d3.sum(
  datosPartido.filter(d => parseFloat(d.Velocidad) < 200),
  d => parseFloat(d.Velocidad) * parseInt(d.Accesos)
) / d3.sum(
  datosPartido.filter(d => parseFloat(d.Velocidad) < 200),
  d => parseInt(d.Accesos)
);
```

<div class="card" style="padding: 1.5rem; background: white; border: 1px solid #e0e0e0; margin: 1rem 0;">
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
    <div>
      <div style="font-size: 2rem; font-weight: 300; color: #0066cc;">${totalPartido.toLocaleString()}</div>
      <div style="color: #666; font-size: 0.85rem; margin-top: 0.5rem;">Total Accesos</div>
    </div>
    <div>
      <div style="font-size: 2rem; font-weight: 300; color: #0066cc;">${velocidadPromedioPartido.toFixed(0)}</div>
      <div style="color: #666; font-size: 0.85rem; margin-top: 0.5rem;">Mbps Promedio</div>
    </div>
    <div>
      <div style="font-size: 2rem; font-weight: 300; color: #0066cc;">${new Set(datosPartido.map(d => d.Localidad)).size}</div>
      <div style="color: #666; font-size: 0.85rem; margin-top: 0.5rem;">Localidades</div>
    </div>
  </div>
</div>

```js
Plot.plot({
  marginLeft: 100,
  marginRight: 80,
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
  marks: [
    Plot.barY(distribPartido, {
      x: "rango",
      y: "accesos",
      fill: "color",
      tip: {
        format: {
          x: true,
          y: true
        }
      }
    }),
    Plot.text(distribPartido, {
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

**${partidoSelector}:** Velocidad promedio de ${velocidadPromedioPartido.toFixed(0)} Mbps. El rango más común es ${distribPartido.sort((a,b) => b.accesos - a.accesos)[0]?.rango} con ${distribPartido.sort((a,b) => b.accesos - a.accesos)[0]?.porcentaje.toFixed(0)}% de los accesos.

</div>

---

<div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e0e0e0; color: #999; font-size: 0.85rem;">

**Fuente:** Ente Nacional de Comunicaciones (ENACOM), Argentina
**Nota metodológica:** Velocidades >200 Mbps (típicamente satelitales) excluidas del cálculo de promedios. Análisis de brecha digital limitado a localidades con >50 accesos.

</div>
