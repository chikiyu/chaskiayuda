# Integrante 3 — Sphere Handbook + Estándares Internacionales

**Fuente:** Sphere Handbook 2018 + guías OCHA/IASC
**Método:** Descarga manual del PDF + extracción por capítulo
**Output:** `data/raw/sphere/`
**Meta:** ~300 chunks de estándares + resumen de los 20 más relevantes para DPO

## Descargar el Sphere Handbook

1. Ir a https://spherestandards.org/handbook/
2. Hacer clic en **"Download"** → seleccionar español
3. Guardar como `data/raw/sphere/pdfs/sphere_handbook_2018_sp.pdf`
4. Si no está disponible en español: descargar inglés como `sphere_handbook_2018_en.pdf`

## Capítulos a priorizar (en orden)

| Capítulo | Páginas aprox. | Por qué importa para el DPO |
|---|---|---|
| Cap 2 — Agua y saneamiento (WASH) | 40–60 | Estándares en litros/persona, calidad |
| Cap 3 — Seguridad alimentaria | 40–50 | Nutrición mínima en emergencias |
| Cap 4 — Albergue | 30–40 | Techo de emergencia, materiales |
| Cap 5 — Salud | 40–50 | Atención médica básica en crisis |
| Estándares transversales | 20–30 | Protección, género, participación |

## Cómo correr

```bash
python stage_a_extraction/integrante_3/extract_sphere.py
```

## Output esperado

```
data/raw/sphere/
├── pdfs/                          ← PDF descargado (en .gitignore)
├── sphere_chunks.jsonl            ← texto por página/sección
└── sphere_estandares_clave.json   ← los 20 estándares más importantes (para Stage C)
```

## Checklist

- [ ] PDF descargado y verificado como extraíble (Ctrl+A funciona)
- [ ] Script corrido sin errores
- [ ] `sphere_chunks.jsonl` tiene >200 chunks
- [ ] `sphere_estandares_clave.json` listo para la persona de Stage C (DPO)
- [ ] Documentar si el PDF está en español o inglés
