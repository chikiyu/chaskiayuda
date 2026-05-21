# Integrante 1 — Emilio · ReliefWeb

## Qué te toca extraer

Reportes humanitarios sobre Perú en español desde ReliefWeb.  
Es la fuente más grande — necesitamos 500 a 1,000 textos.

**URL base:** https://reliefweb.int/country/per  
**API:** https://api.reliefweb.int/v2/reports  

## Cómo hacerlo

### Opción A — Script (recomendado)
Hay un script en el pipeline-completo del proyecto. Necesita:
- Python + `pip install requests`
- Llamar a la API con filtros: `country=PER`, `language=spa`, desde 2015

### Opción B — Manual (si la API da problemas)
1. Ir a https://reliefweb.int/country/per
2. Filtrar por idioma: español
3. Copiar el texto de los reportes más relevantes

## Qué tipos de crisis priorizar

- Inundaciones / El Niño (los más comunes en Perú)
- Sismos / terremotos
- Deslizamientos / huaicos
- Sequías / heladas
- Epidemias (dengue, etc.)

Intentar tener al menos 100 textos de cada tipo.

## Formato de salida

Un archivo `reliefweb.jsonl` donde cada línea es:
```json
{"id": "rw-123", "fuente": "reliefweb", "titulo": "...", "fecha": "2023-03-15", "tipo_crisis": "inundacion", "texto": "El texto completo aquí..."}
```

## Dónde subir los datos

**Google Drive del equipo** → carpeta `data/raw/reliefweb/`  
(los datos NO van en GitHub)

## Qué subir al repo

Solo este README actualizado con:
- Cuántos textos extrajiste
- Qué fechas cubren
- Distribución por tipo de crisis
- Problemas que encontraste

## Checklist

- [ ] Al menos 500 textos con cuerpo completo (>200 caracteres)
- [ ] Distribuidos en al menos 4 tipos de crisis
- [ ] Archivo `reliefweb.jsonl` subido al Drive
- [ ] README actualizado con el reporte final
