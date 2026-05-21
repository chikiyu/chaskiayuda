"""
Stage E — Demo ChasquiAyuda en Gradio
=======================================
Subir a HuggingFace Spaces para la presentación del hackathon.

Para correr localmente:
    pip install gradio transformers
    python app.py

Para subir a HF Spaces:
    → Crear un Space en huggingface.co/spaces
    → Subir este archivo como app.py
    → Agregar requirements.txt con: gradio, transformers, torch, peft
"""

import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

MODEL_ID = "ChasquiAyuda/chasquiayuda-model"  # cambiar cuando esté listo

DESCRIPCION = """
## ChasquiAyuda 🏔️
**Navegador de ayuda humanitaria para Perú**

Describe tu situación de emergencia y te ayudaré a encontrar los recursos disponibles.

*Información verificada a mayo 2026. Siempre confirmar con las fuentes oficiales.*
"""

EJEMPLOS = [
    "Hubo inundaciones en mi comunidad en Piura, perdimos todo. ¿A dónde podemos ir?",
    "Hubo un sismo fuerte en Arequipa y tenemos miedo de entrar a la casa. ¿Qué hacemos?",
    "No tenemos agua limpia desde hace 2 días después del huaico. ¿Qué podemos hacer?",
    "¿A qué ayuda tenemos derecho si perdimos nuestra casa por un desastre?",
    "¿Cómo registro a mi familia como damnificada para recibir ayuda del gobierno?",
]

# Cargar modelo (se ejecuta al iniciar el Space)
print(f"Cargando modelo: {MODEL_ID}")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    MODELO_LISTO = True
    print("✅ Modelo cargado")
except Exception as e:
    print(f"⚠️  Modelo no disponible aún: {e}")
    MODELO_LISTO = False


def responder(mensaje, historial):
    if not MODELO_LISTO:
        return historial + [[mensaje, "⚠️ El modelo aún no está disponible. Vuelve más tarde."]]

    # Construir el prompt con historial
    mensajes = [{"role": "system", "content": (
        "Eres ChasquiAyuda, un asistente humanitario para Perú. "
        "Ayudas a personas en crisis a encontrar recursos y ayuda disponible. "
        "Responde de forma empática, clara y con información accionable. "
        "Menciona organizaciones reales: INDECI (115), Cruz Roja Perú, MIDIS, MINSA."
    )}]

    for humano, asistente in historial:
        mensajes.append({"role": "user",      "content": humano})
        mensajes.append({"role": "assistant", "content": asistente})
    mensajes.append({"role": "user", "content": mensaje})

    respuesta = pipe(
        mensajes,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
    )[0]["generated_text"][-1]["content"]

    return historial + [[mensaje, respuesta]]


with gr.Blocks(title="ChasquiAyuda") as demo:
    gr.Markdown(DESCRIPCION)

    chatbot = gr.Chatbot(height=450, label="ChasquiAyuda")
    msg = gr.Textbox(
        placeholder="Describe tu situación de emergencia...",
        label="Tu mensaje",
        lines=2,
    )

    with gr.Row():
        enviar = gr.Button("Enviar", variant="primary")
        limpiar = gr.Button("Nueva conversación")

    gr.Examples(
        examples=EJEMPLOS,
        inputs=msg,
        label="Ejemplos de situaciones",
    )

    gr.Markdown("""
    ---
    **Líneas de emergencia en Perú:**
    - INDECI: **115** (gratuita, 24h)
    - Cruz Roja Peruana: **115-4**
    - MINSA: **113** (salud)
    - Línea 100: violencia y emergencia social

    *Este modelo fue desarrollado para el SomosNLP Hackathon 2026.*
    """)

    enviar.click(responder, [msg, chatbot], [chatbot]).then(
        lambda: "", None, msg
    )
    msg.submit(responder, [msg, chatbot], [chatbot]).then(
        lambda: "", None, msg
    )
    limpiar.click(lambda: [], None, chatbot)


if __name__ == "__main__":
    demo.launch()
