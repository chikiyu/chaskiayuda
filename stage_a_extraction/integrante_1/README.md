# Integrante 1 — ReliefWeb API

**Fuente:** ReliefWeb (OCHA, IFRC, UNICEF, otros)
**Método:** API pública JSON
**Output:** `data/raw/reliefweb/reliefweb.jsonl`
**Meta:** 500–2,000 registros con texto completo

## Fuentes a extraer

| Organización | Filtro API | Prioridad |
|---|---|---|
| OCHA Perú | `source.shortname=OCHA` | Alta |
| Cruz Roja IFRC | `source.shortname=IFRC` | Alta |
| UNICEF Perú | `source.shortname=UNICEF` | Media |
| Todos en español | `language.code=spa` + `country.iso3=PER` | Base |

## Cómo correr

```bash
# Desde la raíz del repo
python stage_a_extraction/integrante_1/extract_reliefweb.py

# Con parámetros personalizados
python stage_a_extraction/integrante_1/extract_reliefweb.py --limite 1000 --desde 2018-01-01
```

## Output esperado

```jsonl
{"id": "rw-123", "fuente": "reliefweb", "org": "OCHA", "fecha": "2023-03-15", "tipo_crisis": "inundacion", "region": "Piura", "titulo": "...", "texto": "...", "licencia": "cc_by", "fecha_extraccion": "2026-05-20"}
```

## Checklist

- [ ] Script corre sin errores
- [ ] Output tiene al menos 500 registros
- [ ] Todos los registros tienen campo `texto` con >200 caracteres
- [ ] Distribución de `tipo_crisis` revisada (no todo inundaciones)
- [ ] Archivo subido a `data/raw/reliefweb/`
