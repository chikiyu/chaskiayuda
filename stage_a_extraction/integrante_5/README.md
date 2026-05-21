# Integrante 5 — Milton · ONGs + HDX + CENEPRED

## Qué te toca extraer

Contenido de organizaciones humanitarias que operan en Perú + datasets de HDX.

## Fuentes web a scrapear / copiar

Navegar cada URL y copiar el contenido relevante sobre respuesta a emergencias en Perú:

| Organización | URL | Qué buscar |
|---|---|---|
| Cruz Roja Peruana | https://www.cruzroja.org.pe | Servicios, líneas, guías de respuesta |
| Cáritas Perú | https://www.caritasperu.org.pe | Programas de ayuda humanitaria |
| WFP Perú | https://www.wfp.org/countries/peru | Seguridad alimentaria en emergencias |
| CARE Perú | https://www.care.org.pe | Respuesta comunitaria |
| CENEPRED publicaciones | https://www.cenepred.gob.pe/web/publicaciones/ | Evaluación de riesgos por región |

## HDX — Datasets estructurados

1. Ir a https://data.humdata.org
2. Buscar: `Peru emergency` o `Peru humanitarian`
3. Filtrar por: formato CSV, actualizado después de 2018
4. Descargar los 3-5 más relevantes
5. Abrirlos y anotar qué columnas tienen texto útil (no solo números)

**Lo que buscamos en los CSV de HDX:**
- Columnas con descripciones de tipo de ayuda distribuida
- Organizaciones que respondieron a qué crisis
- Regiones afectadas con descripción de la situación

## Formato de salida

Para webs: un archivo `ongs.jsonl` con el texto extraído de cada organización  
Para HDX: los CSV descargados + un `hdx_resumen.md` explicando qué tiene cada uno

## Dónde subir los datos

**Google Drive del equipo** → carpeta `data/raw/ongs_hdx/`

## Checklist

- [ ] Cruz Roja Peruana — contenido sobre servicios de emergencia extraído
- [ ] Al menos 2 ONGs más documentadas
- [ ] Al menos 3 CSV de HDX descargados y explorados
- [ ] `hdx_resumen.md` explicando qué hay en cada CSV
- [ ] README actualizado
