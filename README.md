# ChaskiAyuda 🏔️
LLM post-entrenado para navegación de ayuda humanitaria en Perú  
**SomosNLP Hackathon 2026** · Deadline: 29 mayo

---

## Equipo y responsabilidades

| Integrante | Extracción (Stage A) | Stage siguiente |
|---|---|---|
| Johana | ReliefWeb API | Stage B — SFT |
| Emilio | INDECI | Stage B — SFT |
| Fran | Sphere Handbook | Stage C — DPO |
| Astrid | Programas de gobierno | Stage B — SFT |
| Milton | ONGs + HDX | Stage B — SFT |

---

## Estructura del repo

```
chaskiayuda/
│
├── stage_a_extraction/        ← Cada quien trabaja en su carpeta
│   ├── integrante_1/          Johana  — ReliefWeb
│   ├── integrante_2/          Emilio  — INDECI
│   ├── integrante_3/          Fran    — Sphere Handbook
│   ├── integrante_4/          Astrid  — Programas gobierno
│   └── integrante_5/          Milton  — ONGs + HDX
│
├── stage_b_sft/               Generación del dataset SFT
├── stage_c_dpo/               Generación del dataset DPO
├── stage_d_training/          Entrenamiento del modelo
├── stage_e_demo/              Demo Gradio para HF Spaces
│
├── data/                      ⚠️  NO se sube al repo (.gitignore)
│   ├── raw/                   Datos crudos — compartir por Drive
│   ├── sft/                   Dataset SFT — subir directo a HuggingFace
│   └── dpo/                   Dataset DPO — subir directo a HuggingFace
│
├── .env.example               Plantilla de credenciales
└── requirements.txt           Dependencias
```

---

## Flujo de los datos

```
Cada persona extrae localmente (PDFs, CSVs, JSONL)
        ↓
Comparten archivos crudos por Google Drive
        ↓
Se procesan y convierten al formato de entrenamiento
        ↓
Se suben directo a HuggingFace Hub (entregable del hackathon)
```

Lo que va en GitHub: scripts y READMEs.  
Lo que va en HuggingFace: el dataset procesado y el modelo.  
Lo que va en Drive: archivos crudos intermedios.
