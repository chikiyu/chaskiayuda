# Integrante 4 — Programas de Gobierno Peruano

**Fuente:** MIDIS, MINSA, MINEDU, MIMP, SIS, Pensión 65
**Método:** Web scraping + descarga de PDFs
**Output:** `data/raw/gobierno/`
**Meta:** 50–100 fichas de programas estructuradas

## Programas a documentar

Para cada programa, llenar la ficha del script. Navegar cada URL:

| Programa | URL | Qué buscar |
|---|---|---|
| MIDIS — Contigo | https://www.midis.gob.pe/index.php/es/programa-contigo | Quién califica, cómo registrarse, transferencias en emergencia |
| Qali Warma | https://www.qaliwarma.gob.pe | Alimentación escolar en emergencias |
| MINSA — Emergencias | https://www.minsa.gob.pe/emergencias/ | Protocolos de salud en crisis |
| MINEDU — Escuelas seguras | https://www.minedu.gob.pe/emergencia/ | Protocolo educativo en desastres |
| MIMP — Protección mujer | https://www.mimp.gob.pe | Servicios para mujeres en crisis |
| SIS — Cobertura emergencia | https://www.sis.gob.pe | Qué cubre el seguro en desastres |
| Pensión 65 en emergencias | https://www.pension65.gob.pe | Adultos mayores en crisis |
| Bono 350 / transferencias | https://www.gob.pe | Bonos de emergencia históricos |

## Cómo correr

```bash
# Scraping automático de páginas web
python stage_a_extraction/integrante_4/extract_gobierno.py

# Solo scraping (sin fichas manuales)
python stage_a_extraction/integrante_4/extract_gobierno.py --modo web
```

## Checklist

- [ ] Al menos 6 programas documentados con ficha completa
- [ ] Cada ficha tiene: nombre, quién califica, cómo acceder, contacto
- [ ] Script de scraping web corrido
- [ ] Output en `data/raw/gobierno/gobierno.jsonl`
