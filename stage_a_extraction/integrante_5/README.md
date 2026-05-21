# Integrante 5 — ONGs + HDX + CENEPRED/SIGRID

**Fuente:** Cruz Roja Peruana, Cáritas, HDX datasets, CENEPRED
**Método:** Web scraping + descarga CSV de HDX + CENEPRED PDFs
**Output:** `data/raw/ongs_hdx/`
**Meta:** 20–40 documentos + 3-5 CSVs de HDX útiles

## Fuentes a cubrir

| Fuente | URL | Qué extraer |
|---|---|---|
| Cruz Roja Peruana | https://www.cruzroja.org.pe | Guías primeros auxilios, respuesta desastres, contactos |
| Cáritas Perú | https://www.caritasperu.org.pe | Ayuda humanitaria sociedad civil, programas |
| WFP Perú | https://www.wfp.org/countries/peru | Seguridad alimentaria, distribución en emergencias |
| CENEPRED publicaciones | https://www.cenepred.gob.pe/web/publicaciones/ | Evaluación riesgos por región |
| HDX — Perú crisis | https://data.humdata.org (buscar "Peru") | CSVs con datos estructurados |
| CARE Perú | https://www.care.org.pe | Respuesta comunitaria |

## HDX — Cómo filtrar los datasets útiles

En `data.humdata.org`, buscar "Peru" y priorizar datasets con:
- ✅ Formato CSV (descargable directo)
- ✅ Columnas con texto descriptivo (no solo números)
- ✅ Actualizado después de 2018
- ✅ Relacionado con: emergencias, personas afectadas, distribución de ayuda
- ❌ Descartar: solo coordenadas, solo IDs, solo estadísticas sin contexto

## Cómo correr

```bash
python stage_a_extraction/integrante_5/extract_ongs_hdx.py
```

## Checklist

- [ ] Cruz Roja Peruana — al menos 3 páginas de contenido extraído
- [ ] HDX — al menos 3 CSVs descargados y explorados
- [ ] CENEPRED — al menos 2 PDFs procesados
- [ ] Output en `data/raw/ongs_hdx/`
