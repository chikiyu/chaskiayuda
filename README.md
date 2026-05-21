# ChasquiAyuda 🏔️
LLM post-entrenado para navegación de ayuda humanitaria en Perú  
**SomosNLP Hackathon 2026** · Deadline: 29 mayo

---

## Equipo y responsabilidades

| Integrante | Extracción (Stage A) | Stage siguiente |
|---|---|---|
| @ayayon | — | Stage D — Entrenamiento |
| @Emilio | ReliefWeb API | Stage B — SFT |
| @Raven99 | INDECI | Stage B — SFT |
| @Fran | Sphere Handbook | Stage C — DPO |
| @Maskuyruru | Gobierno + ONGs/HDX | Stage B — SFT |

---

## Estructura del repo

```
chasquiayuda/
│
├── stage_a_extraction/        ← Cada quien trabaja en su carpeta
│   ├── integrante_1/          Emilio   — ReliefWeb
│   ├── integrante_2/          Raven99  — INDECI
│   ├── integrante_3/          Fran     — Sphere Handbook
│   ├── integrante_4/          Maskuyruru — Programas gobierno
│   └── integrante_5/          Maskuyruru — ONGs + HDX
│
├── stage_b_sft/               Generación del dataset SFT
├── stage_c_dpo/               Generación del dataset DPO
├── stage_d_training/          Entrenamiento del modelo
├── stage_e_demo/              Demo Gradio para HF Spaces
│
├── data/                      ⚠️  NO se sube al repo (.gitignore)
│   ├── raw/                   Datos crudos de Stage A
│   ├── sft/                   Dataset SFT listo
│   └── dpo/                   Dataset DPO listo
│
├── .env.example               Plantilla de credenciales
└── requirements.txt           Dependencias
```

---

## Cómo unirte al repo

1. Pedirle a @ayayon que te agregue como colaborador
2. `git clone https://github.com/ayayon/chasquiayuda.git`
3. Crear tu rama: `git checkout -b stage-a/integrante-X`
4. Trabajar en tu carpeta `stage_a_extraction/integrante_X/`
5. Subir: `git add . && git commit -m "..." && git push`

---

## Regla de oro

**Los datos no van en el repo.** Solo van los scripts, READMEs y reportes.  
Los archivos de datos (`.jsonl`, `.csv`, `.pdf`) van en el Google Drive del equipo.
