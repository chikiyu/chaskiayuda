---
license: apache-2.0
base_model: Qwen/Qwen2.5-7B-Instruct
language:
- es
tags:
- dpo
- qlora
- alignment
- humanitarian
- peru
- disaster-response
- somosnlp-hackathon-2026
- peft
library_name: peft
pipeline_tag: text-generation
---

# ChasquiAyuda — Asistente Humanitario para Perú 🏔️

Modelo post-entrenado con **DPO + QLoRA** para respuesta humanitaria en español,
especializado en el contexto peruano. Desarrollado para el
**[SomosNLP Hackathon 2026](https://somosnlp.org/hackathon)**.

**ODS:** 11 (Ciudades sostenibles) · 13 (Acción climática) · 10 (Reducción de desigualdades)

---

## El problema

Cuando ocurre un desastre en Perú, las personas afectadas enfrentan una doble
crisis: el desastre en sí y la desinformación sobre qué ayuda les corresponde
y cómo acceder a ella. Los modelos genéricos responden con lenguaje burocrático
e inaplicable al contexto peruano.

## La solución

ChasquiAyuda responde con:
- **Empatía** — reconoce la situación antes de dar información
- **Pasos accionables** — concretos y ejecutables ahora mismo
- **Recursos reales** — INDECI (115), Cruz Roja Peruana (01-266-6978),
  SAMU (106), MIDIS, MINSA, Línea 100

## Ejemplo

**Input:**
> "Hubo inundaciones en mi comunidad en Piura, perdimos todo. ¿Qué hacemos?"

**ChasquiAyuda:**
> "Entendemos que están viviendo una situación muy difícil. Hay varias rutas simultáneas:
> 1. **INDECI — línea 115** (gratuita, 24h): reporta daños y te informan de puntos
>    de distribución activos en tu zona.
> 2. **Cruz Roja Peruana** (01-266-6978): busca sus carpas de registro en los
>    primeros días — distribuyen kits de higiene y agua.
> 3. **MIDIS — Programa Contigo**: se activa automáticamente en emergencias
>    declaradas. El registro es gratuito, nadie puede cobrarte.
> ¿En qué distrito exactamente estás? Así confirmo qué operaciones están activas."

**Modelo base (Qwen2.5-7B sin entrenar):**
> "Contacte a las autoridades locales o al gobierno regional para informarles
> sobre la situación y solicitar ayuda de emergencia..."

---

## Métricas

| Métrica | Modelo base | ChasquiAyuda DPO |
|---------|-------------|------------------|
| Reward Accuracy | 50.0% | **96.8%** |
| Mean Reward Margin | — | **0.4212** |
| Mean R(chosen) | — | -2.0887 |
| Mean R(rejected) | — | -2.5099 |

**Mejora relativa: +94% vs modelo base**

### Curva de entrenamiento

| Step | Training Loss |
|------|--------------|
| 10 | 0.3064 |
| 20 | 0.0598 |
| 30 | 0.0182 |
| 40 | 0.0044 |
| 50 | 0.0092 |
| 60 | 0.0043 |

---

## Dataset

Entrenado con **[ChasquiAyuda DPO Dataset](https://huggingface.co/datasets/somosnlp-hackathon-2026/chaskiayuda-dataset-dpo)**
— 620 pares chosen/rejected derivados de 8 fuentes:

| Fuente | Pares | Rol en DPO |
|--------|-------|------------|
| Sphere Handbook 2018 | 180 | Define el `chosen` (estándares min.) |
| INDECI (manuales oficiales) | 140 | Procedimientos peruanos oficiales |
| Programas gobierno Perú | 110 | MIDIS, MINSA, MINEDU, SIS, Pensión 65 |
| ReliefWeb / OCHA | 90 | Contexto de crisis reales en Perú |
| CHS 2024 | 30 | Accountability y participación |
| ONGs (Cruz Roja, Cáritas, CARE) | 40 | Primeros auxilios y respuesta comunit. |
| HDX / IDMC | 30 | Eventos reales de desplazamiento Perú |
| Fenómeno El Niño 2026 | 42 | Preparación/respuesta/recuperación FEN |

---

## Cómo usar

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch

# 1. Cargar modelo base
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4"
)
base = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

# 2. Aplicar adaptador ChasquiAyuda
model = PeftModel.from_pretrained(
    base,
    "somosnlp-hackathon-2026/chaskiayuda-model"
)

# 3. Generar respuesta
SYSTEM = ("Eres ChasquiAyuda, un asistente humanitario para Perú. "
          "Responde con empatía, pasos concretos y recursos reales.")

messages = [
    {"role": "system", "content": SYSTEM},
    {"role": "user",   "content": "Hubo un terremoto en Arequipa. ¿Qué hacemos?"}
]
text = tokenizer.apply_chat_template(messages, tokenize=False,
                                      add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=300,
                          temperature=0.3, do_sample=True)
print(tokenizer.decode(out[0][inputs.input_ids.shape[1]:],
                        skip_special_tokens=True))
```

---

## Detalles técnicos

| Parámetro | Valor |
|-----------|-------|
| Modelo base | Qwen/Qwen2.5-7B-Instruct |
| Técnica | DPO + QLoRA |
| LoRA rank (r) | 16 |
| LoRA alpha | 32 |
| Quantización | 4-bit NF4 (bitsandbytes) |
| Beta DPO | 0.1 |
| Épocas | 1 |
| Batch efectivo | 8 (batch=1, grad_accum=8) |
| Learning rate | 5e-5 |
| GPU | T4 16GB (Google Colab) |
| Tiempo entrenamiento | 2h 42min |
| Huella CO₂ | ~0.08 kg CO₂eq (estimado) |


---

## Librerías utilizadas

| Librería | Rol |
|----------|-----|
| `transformers` | Carga del modelo base y generación |
| `trl` | DPOTrainer para el entrenamiento por preferencias |
| `peft` | QLoRA — adaptadores de bajo rango |
| `bitsandbytes` | Cuantización 4-bit NF4 |
| `accelerate` | Distribución en GPU |
| `datasets` | Carga y procesamiento del dataset |
| `codecarbon` | Medición de huella de carbono |

## Pruebas realizadas

**Entrenamiento v1 (este modelo):**
- 1 época · 620 pares · T4 16GB · 2h 42min
- Resultado: Reward Accuracy 96.8% · Margin 0.4212
- Warning detectado: mismatch en tokenización por chat template no aplicado
  al prompt antes del DPO — corregido en código final

**Intento v2 (no completado):**
- Configuración mejorada: 2 épocas, beta=0.2, lr=3e-5, chat template fix
- Interrumpido por OOM en T4 al aumentar `max_length` a 768
- El modelo v1 ya muestra métricas sólidas → se mantiene como versión final

## Impacto ambiental

Medido con **[CodeCarbon](https://github.com/mlco2/codecarbon)**
integrado en el entrenamiento.

- **Hardware:** NVIDIA T4 16GB (Google Colab)
- **Duración:** 2h 42min (1 época, 620 pares)
- **CO₂ estimado:** ~0.08 kg CO₂eq
- **Referencia:** equivale a ~0.5 km en coche

Para minimizar el impacto: QLoRA 4-bit reduce el cómputo vs entrenamiento
completo; 1 sola época en lugar de múltiples iteraciones.

---

## Limitaciones

- Información verificada a mayo–junio 2026 — confirmar con fuentes oficiales
- Solo español — no cubre quechua, aymara ni otras lenguas originarias
- Sin acceso a información en tiempo real sobre crisis activas
- Optimizado para Perú — no generalizar a otros países sin validación
- Requiere GPU para inferencia razonablemente rápida (mín. 16GB VRAM con 4-bit)

## Sesgos

El dataset sobrerepresenta inundaciones (25%) respecto a otros desastres.
Las fuentes internacionales (Sphere, CHS) pueden no reflejar capacidades
reales de respuesta en zonas remotas de Perú.

## Impacto ambiental

Entrenado en Google Colab (T4, mix energético EE.UU.).
Huella estimada: ~0.08 kg CO₂eq para 1 época sobre 620 pares.

---

## Notebooks

- [`chaskiayuda_training.ipynb`](./chaskiayuda_training.ipynb) — entrenamiento DPO completo
- Dataset: [somosnlp-hackathon-2026/chaskiayuda-dataset-dpo](https://huggingface.co/datasets/somosnlp-hackathon-2026/chaskiayuda-dataset-dpo)
- Demo: [somosnlp-hackathon-2026/chaskiayuda-demo](https://huggingface.co/spaces/somosnlp-hackathon-2026/chaskiayuda-demo)

---

*ChasquiAyuda · SomosNLP Hackathon 2026 · Apache 2.0*
