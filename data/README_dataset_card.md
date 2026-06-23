---
license: cc-by-4.0
---

# ChasquiAyuda DPO — Alineamiento Humanitario Perú

Dataset de preferencias (DPO) para entrenar un asistente de respuesta 
humanitaria en español, especializado en el contexto peruano.
Desarrollado para el **[SomosNLP Hackathon 2026](https://somosnlp.org/hackathon)**.

---

## Motivación

Cuando ocurre un desastre en Perú, las personas afectadas enfrentan 
una doble crisis: el desastre en sí y la desinformación sobre a qué 
ayuda tienen derecho y cómo acceder a ella. Los asistentes de IA 
genéricos dan respuestas vagas o inaplicables al contexto peruano.

ChasquiAyuda entrena un modelo para responder con información 
**accionable, empática y culturalmente apropiada** para Perú: 
números reales (INDECI 115), programas reales (Programa Contigo, SIS), 
y estándares humanitarios verificables (Sphere, CHS 2024).

---

## Formato del dataset

Cada registro sigue el formato estándar DPO:

```python
{
  "prompt":   "Pregunta de una persona afectada por un desastre en Perú",
  "chosen":   "Respuesta de calidad: empática, con pasos concretos y recursos reales",
  "rejected": "Respuesta insuficiente: vaga, burocrática o sin contexto peruano"
}
```

---

## Fuentes de datos y construcción

El dataset se construyó combinando **8 fuentes** de diferente naturaleza:

### Fuentes de estándares internacionales (definen el `chosen`)

| Fuente | Descripción | Licencia | Pares aprox. |
|--------|-------------|----------|--------------|
| Sphere Handbook 2018 — capítulos 2–5 | Estándares mínimos internacionales de respuesta humanitaria: agua/saneamiento, alimentación, albergue y salud | CC-BY | 180 |
| [Core Humanitarian Standard 2024] — compromisos 1, 4, 5 | Norma Humanitaria Esencial 2024: calidad, participación comunitaria y mecanismos de queja/retroalimentación | CC-BY | 30 |

### Fuentes peruanas oficiales

| Fuente | Descripción | Licencia | Pares aprox. |
|--------|-------------|----------|--------------|
| INDECI — Manual EDAN, guías de albergue y evacuación | Procedimientos oficiales del Instituto Nacional de Defensa Civil: evaluación de daños, derechos del damnificado, protocolos de respuesta | Dominio público Perú | 140 |
| Programas sociales del Estado peruano — MIDIS, MINSA, MINEDU, MIMP, SIS, Pensión 65 | Información sobre acceso a programas de ayuda estatal activables en emergencias, requisitos, contactos y protocolos | Dominio público Perú | 110 |

### Fuentes de contexto de crisis reales

| Fuente | Descripción | Licencia | Pares aprox. |
|--------|-------------|----------|--------------|
| ReliefWeb / OCHA  — reportes 2016–2026 en español | Reportes situacionales de crisis reales en Perú: inundaciones El Niño, sismos, huaicos, sequías, epidemias | CC-BY | 90 |
| Cruz Roja Peruana, Cáritas Perú, CARE Perú, Plan International Perú | Guías de primeros auxilios, respuesta comunitaria, protección de poblaciones vulnerables en emergencias | Mixta (uso educativo) | 40 |
| HDX / IDMC — `idmc_idu_events_peru` | Registro de desplazamientos internos en Perú con datos de INDECI: 5,082 eventos reales con ubicación, tipo de desastre y número de desplazados | CC-BY | 30 |

### Fuentes para el nuevo Fenomeno del niño 2026

| Fuente | Descripción | Pares aprox. |
|--------|-------------|--------------|
| SENAMHI + proceso EDAN + medios 2026 — Fenómeno El Niño | Alertas, proyecciones e impactos del FEN 2026 en Perú (proyectado como uno de los más intensos en décadas). Cubre fases de preparación, respuesta y recuperación con contexto geográfico específico por región  | 42 |

**Total generado:** ~620 pares  

---

## Criterios de calidad DPO

### Qué hace a un `chosen` de calidad
1. **Empatía primero:** reconoce la situación antes de dar información
2. **Accionabilidad inmediata:** pasos concretos numerados ejecutables ahora
3. **Recursos reales de Perú:** menciona al menos uno con contacto directo  
   (INDECI 115, Cruz Roja 01-266-6978, etc.)
4. **Estándares verificables:** cuando aplica, cita valores del Sphere o CHS  
   (ej: "mínimo 15 litros de agua por persona al día")
5. **Contexto peruano:** adapta a geografía (costa/sierra/selva), instituciones  
   locales, y realidad socioeconómica peruana
6. **Continuidad:** pregunta de seguimiento o recurso adicional al final
7. **Longitud:** mínimo 80 palabras

### Qué hace a un `rejected` realista 
1. Algo que un chatbot genérico o portal de gobierno mal diseñado diría
2. Lenguaje burocrático: "contacte a las autoridades competentes"
3. Sin recursos concretos ni pasos ejecutables
4. Podría aplicar a cualquier país, no específicamente a Perú

### Proceso de revisión
- **Generación:** asistida por LLM (Gemini Pro, Gemini pro deep research) con prompts especializados  
  por tipo de fuente y tipo de crisis
- **Revisión manual:** cada par fue revisado para verificar que el contraste  
  chosen/rejected sea claro pero no exagerado, y que el chosen sea  
  técnicamente correcto según las fuentes originales

---

## Estadísticas

### Distribución por tipo de crisis

| Tipo | Pares aprox. | % |
|------|-------------|---|
| Inundación / El Niño | ~140 | 25% |
| Terremoto / sismo | ~110 | 20% |
| Agua, saneamiento e higiene | ~85 | 15% |
| Albergue y desplazamiento | ~70 | 13% |
| Programas sociales en emergencia | ~65 | 12% |
| Deslizamiento / huaico | ~45 | 8% |
| Salud en emergencias | ~30 | 5% |
| Sequía / helada / friaje | ~15 | 2% |


### División train/test
- **train:** 90% (~504 pares)
- **test:** 10% (~56 pares) — separado antes de entrenamiento, no contaminado

---

## Uso

```python
from datasets import load_dataset

dataset = load_dataset("somosnlp-hackathon-2026/chaskiayuda-dataset-dpo")

# Ejemplo de un par
print(dataset["train"][0])
# {
#   "prompt": "Hubo inundaciones en mi comunidad en Piura, perdimos todo...",
#   "chosen": "Entendemos que estás viviendo una situación muy difícil...",
#   "rejected": "En caso de inundación, contacte a las autoridades locales..."
# }
```

---

## Limitaciones

- **Temporal:** información verificada a mayo–junio 2026. Números de teléfono  
  y programas pueden cambiar — confirmar con fuentes oficiales antes de usar  
  en producción.
- **Idioma:** solo español. No cubre lenguas originarias (quechua, aymara,  
  ashaninka) a pesar de su relevancia en zonas de alto riesgo.
- **Geografía:** enfocado en Perú. No generalizar a otros países sin validación.
- **Tiempo real:** el modelo no tiene acceso a información en tiempo real  
  sobre crisis activas — solo conocimiento del entrenamiento.
- **Sesgo de fuentes:** las fuentes internacionales (Sphere, CHS) pueden  
  no reflejar siempre las capacidades reales de respuesta en zonas remotas.
- **Generación asistida:** aunque revisados manualmente, algunos pares pueden  
  contener imprecisiones en detalles específicos de programas o contactos.


---

*Dataset construido para el SomosNLP Hackathon 2026 · Licencia CC-BY-4.0*  
*Fuentes primarias bajo sus respectivas licencias — ver tabla de fuentes*
