# ChasquiAyuda 🏔️
**LLM post-entrenado para navegación de ayuda humanitaria en Perú**
SomosNLP Hackathon 2026 · ODS 1 · 2 · 10 · 16

---

## ¿Qué es?

ChasquiAyuda es un modelo de lenguaje post-entrenado (SFT + DPO) que ayuda a personas en situación de crisis a navegar el ecosistema de ayuda humanitaria en Perú. Responde con información accionable: qué ayuda existe, quién la brinda, y cómo acceder a ella.

**Ejemplo:**
> *"Hubo inundaciones en mi comunidad en Piura, perdimos todo. Escuché que hay ayuda pero no sé dónde ir."*
>
> *"Hay varias rutas simultáneas: (1) INDECI línea 115 — gratuita, 24h... (2) Cruz Roja Peruana — busca sus carpas de registro... (3) MIDIS activa el programa Contigo — el registro es siempre gratuito..."*

---

## Equipo

| Handle | Rol en el proyecto |
|---|---|
| @ayayon | Coordinación + Stage D (ML) |
| @Emilio | Stage A — Integrante 1 (ReliefWeb) |
| @Raven99 | Stage A — Integrante 2 (INDECI) |
| @Fran | Stage A — Integrante 3 (Sphere) |
| @Maskuyruru | Stage A — Integrante 4/5 (Gobierno + ONGs) |

---

## Estructura del repositorio

```
chasquiayuda/
├── stage_a_extraction/     # Extracción de fuentes (cada integrante tiene su carpeta)
│   ├── integrante_1/       # ReliefWeb API → reportes humanitarios Perú
│   ├── integrante_2/       # INDECI → guías y datos de emergencias
│   ├── integrante_3/       # Sphere Handbook → estándares internacionales
│   ├── integrante_4/       # Programas gobierno (MIDIS, MINSA, MINEDU...)
│   └── integrante_5/       # ONGs + HDX + CENEPRED/SIGRID
├── stage_b_sft/            # Generación y curaduría del dataset SFT
├── stage_c_dpo/            # Generación y curaduría del dataset DPO
├── stage_d_training/       # Fine-tuning SFT → DPO + evaluación
├── stage_e_demo/           # App Gradio para HuggingFace Spaces
├── utils/                  # Funciones compartidas entre stages
├── notebooks/              # Exploración y análisis
├── data/                   # ⚠️ EN .gitignore — no se sube al repo
│   ├── raw/                # Datos crudos extraídos por cada integrante
│   ├── sft/                # Dataset SFT listo para entrenar
│   └── dpo/                # Dataset DPO listo para entrenar
├── .env.example            # Plantilla de variables de entorno
└── requirements.txt        # Dependencias del proyecto
```

---

## Setup inicial

```bash
git clone https://github.com/ChasquiAyuda/chasquiayuda.git
cd chasquiayuda

python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt

cp .env.example .env
# Editar .env con las keys reales (pedir al coordinador del equipo)
```

---

## Pipeline de datos

```
Stage A: Extracción  →  Stage B: SFT  →  Stage D: Training
                     →  Stage C: DPO  ↗
                                         ↓
                                      Stage E: Demo
```

Ver el [pipeline completo](../somos%20NLP/pipeline-completo.md) para el detalle de cada stage.

---

## Recursos HuggingFace

- Dataset: `ChasquiAyuda/chasquiayuda-dataset` *(pendiente)*
- Modelo: `ChasquiAyuda/chasquiayuda-model` *(pendiente)*
- Demo: `ChasquiAyuda/chasquiayuda-demo` *(pendiente)*

---

## Deadline: 29 mayo 2026
