# Integrante 3 — Fran · Sphere Handbook

## Qué te toca extraer

El Sphere Handbook es el estándar internacional de respuesta humanitaria.  
Esta fuente es la base de los pares DPO — define qué es una **buena** respuesta.

## Paso 1 — Descargar el PDF

1. Ir a https://spherestandards.org/handbook/
2. Clic en **Download** → elegir español (o inglés si no hay español)
3. Guardar como `sphere_handbook_2018_sp.pdf`
4. Verificar: Ctrl+A en cualquier página → debe copiar texto legible

## Paso 2 — Qué capítulos procesar

Prioridad alta (procesar completo):

| Capítulo | Tema | Para qué sirve |
|---|---|---|
| Cap 2 | Agua y saneamiento (WASH) | Estándares de agua en emergencias |
| Cap 3 | Seguridad alimentaria | Nutrición mínima en crisis |
| Cap 4 | Albergue | Derechos a techo de emergencia |
| Cap 5 | Salud | Atención médica básica |

Prioridad media (si hay tiempo):
- Estándares transversales: protección, género, participación

## Paso 3 — Extraer el texto

```python
import pdfplumber

chunks = []
with pdfplumber.open("sphere_handbook_2018_sp.pdf") as pdf:
    for i, pagina in enumerate(pdf.pages):
        texto = pagina.extract_text()
        if texto and len(texto) > 150:
            chunks.append({"pagina": i+1, "texto": texto.strip()})

print(f"Total páginas útiles: {len(chunks)}")
```

## Paso 4 — El mini-documento más importante

Al terminar, crear un archivo `sphere_estandares_clave.md` con los **20 estándares más concretos** del Sphere. Ejemplo del formato:

```
ESTÁNDAR: Agua mínima
VALOR: 15 litros por persona por día (3 litros en supervivencia inmediata)
APLICACIÓN: Si alguien pregunta sobre agua en emergencia, la respuesta correcta debe mencionar este número

ESTÁNDAR: Distancia al punto de agua
VALOR: Máximo 500 metros desde el albergue
APLICACIÓN: Si alguien dice que el punto de agua está lejos, mencionar este estándar
```

Este archivo lo usará la persona de Stage C (DPO) como referencia.

## Formato de salida

Dos archivos en Google Drive → `data/raw/sphere/`:
- `sphere_chunks.jsonl` — texto extraído página por página
- `sphere_estandares_clave.md` — los 20 estándares más citables (redactado a mano)

## Checklist

- [ ] PDF descargado y verificado como extraíble
- [ ] Capítulos 2-5 procesados
- [ ] `sphere_chunks.jsonl` en el Drive (>200 chunks)
- [ ] `sphere_estandares_clave.md` redactado con al menos 15 estándares
- [ ] README actualizado
