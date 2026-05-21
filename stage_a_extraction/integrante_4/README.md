# Integrante 4 — Astrid · Programas de Gobierno

## Qué te toca extraer

Información sobre los programas estatales que se activan en emergencias.  
No necesitas código — puedes hacer esto navegando las webs y copiando la info clave.

## Programas a documentar

Para cada uno, llenar la ficha de abajo:

| Programa | URL |
|---|---|
| MIDIS — Programa Contigo | https://www.midis.gob.pe/index.php/es/programa-contigo |
| Qali Warma (alimentación) | https://www.qaliwarma.gob.pe |
| MINSA — Emergencias | https://www.minsa.gob.pe/emergencias/ |
| MINEDU — Escuelas seguras | https://www.minedu.gob.pe/emergencia/ |
| SIS — Seguro integral de salud | https://www.sis.gob.pe |
| Pensión 65 | https://www.pension65.gob.pe |

## Formato de la ficha (una por programa)

Copiar esto para cada programa y rellenarlo:

```
PROGRAMA: [nombre completo]
MINISTERIO: [MIDIS / MINSA / MINEDU / etc.]
QUIÉN CALIFICA: [quiénes pueden acceder]
CÓMO ACCEDER: [pasos concretos para registrarse o recibir la ayuda]
QUÉ RECIBEN: [qué entrega el programa exactamente]
CONTACTO: [teléfono, web, app]
EN EMERGENCIA: [qué pasa con este programa cuando hay desastre declarado]
```

## Formato de salida

Un archivo `programas_gobierno.jsonl` con una entrada por programa:
```json
{"id": "midis-contigo", "fuente": "gobierno_peruano", "programa": "Programa Contigo", "texto": "El Programa Contigo del MIDIS..."}
```

O si es más fácil, un archivo `.txt` o `.md` con todas las fichas — el equipo lo convierte después.

## Dónde subir los datos

**Google Drive del equipo** → carpeta `data/raw/gobierno/`

## Checklist

- [ ] Al menos 5 programas documentados con ficha completa
- [ ] Cada ficha tiene número de contacto real y pasos concretos
- [ ] Archivo subido al Drive
- [ ] README actualizado con lista de programas cubiertos
