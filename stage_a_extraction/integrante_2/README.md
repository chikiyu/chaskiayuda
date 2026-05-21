# Integrante 2 — Raven99 · INDECI

## Qué te toca extraer

Guías, manuales y datos de emergencias del INDECI (Instituto Nacional de Defensa Civil).  
Esta es la fuente peruana más importante — le da diferenciación local al proyecto.

## Fuentes a cubrir

### PDFs (descargar manualmente)

Ir a https://www.indeci.gob.pe → sección Publicaciones:

| Qué buscar | Por qué sirve |
|---|---|
| Manual EDAN (Evaluación de Daños) | Procedimientos oficiales de respuesta |
| Guía de albergues de emergencia | Derechos y procedimientos en albergues |
| Plan Nacional de GRD | Marco general de gestión de riesgos |
| Guía de evacuación | Protocolos por tipo de desastre |
| Boletines de emergencias | Casos reales recientes en Perú |

**Antes de procesar cada PDF:** abrir, hacer Ctrl+A en una página y pegar en un bloc de notas.
- Si aparece texto legible → se puede extraer con pdfplumber ✅  
- Si no aparece nada → está escaneado ❌ (anotar y pasar al siguiente)

### Datos abiertos (CSV)

Ir a https://www.datosabiertos.gob.pe/organization/indeci  
Buscar datasets sobre: emergencias, desastres, damnificados  
Descargar los CSV disponibles y anotar qué columnas tienen texto útil.

## Cómo extraer texto de los PDFs

```python
import pdfplumber

with pdfplumber.open("manual_edan.pdf") as pdf:
    for i, pagina in enumerate(pdf.pages):
        texto = pagina.extract_text()
        if texto and len(texto) > 100:
            print(f"Página {i+1}: {len(texto)} caracteres")
```

## Formato de salida

Un archivo `indeci.jsonl`:
```json
{"id": "indeci-edan-p12", "fuente": "indeci_pdf", "documento": "manual_edan", "pagina": 12, "tipo_crisis": "general", "texto": "El proceso de evaluación..."}
```

## Dónde subir los datos

**Google Drive del equipo** → carpeta `data/raw/indeci/`

## Qué subir al repo

Solo este README actualizado con:
- Lista de PDFs procesados (nombre, páginas útiles, ¿tenía texto o estaba escaneado?)
- Lista de CSVs descargados con descripción de columnas
- Total de textos extraídos

## Checklist

- [ ] Al menos 5 PDFs revisados (aunque sean escaneados — documentar cuáles)
- [ ] Al menos 3 PDFs con texto extraíble procesados
- [ ] CSVs de datos abiertos descargados y explorados
- [ ] README actualizado con reporte final
