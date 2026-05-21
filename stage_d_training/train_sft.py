"""
Stage D — Fine-tuning SFT con QLoRA
=====================================
Entrena Qwen2.5-7B-Instruct sobre el dataset SFT de ChasquiAyuda.

Uso:
    python train_sft.py           # entrenamiento completo
    python train_sft.py --test    # prueba rápida (verifica que el entorno funciona)
"""

import argparse
import os
from dotenv import load_dotenv

load_dotenv()

HF_DATASET = "ChasquiAyuda/chasquiayuda-dataset"
HF_MODEL_OUT = "ChasquiAyuda/chasquiayuda-sft"
MODEL_BASE = "Qwen/Qwen2.5-7B-Instruct"


def verificar_entorno():
    """Carga el modelo en 4-bit para verificar que la GPU funciona."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    print(f"GPU disponible: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    print(f"\nCargando {MODEL_BASE} en 4-bit...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_BASE)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_BASE,
        quantization_config=bnb_config,
        device_map="auto",
    )
    print("✅ Modelo cargado correctamente — entorno listo para entrenar")

    # Test de inferencia básica
    inputs = tokenizer("Hola, soy ChasquiAyuda", return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=20)
    print(f"Test de inferencia: {tokenizer.decode(outputs[0], skip_special_tokens=True)}")

    return model, tokenizer


def entrenar_sft(test_mode=False):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig
    from trl import SFTTrainer, SFTConfig
    from datasets import load_dataset

    # Cargar dataset
    print(f"Cargando dataset: {HF_DATASET}")
    dataset = load_dataset(HF_DATASET)
    train_ds = dataset["train"]
    eval_ds  = dataset.get("validation", dataset["train"].select(range(100)))

    if test_mode:
        train_ds = train_ds.select(range(50))
        eval_ds  = eval_ds.select(range(10))
        print("MODO TEST: usando 50 ejemplos")

    # Configuración 4-bit
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_BASE)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_BASE,
        quantization_config=bnb_config,
        device_map="auto",
    )

    # LoRA
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules="all-linear",
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        peft_config=lora_config,
        args=SFTConfig(
            output_dir="./outputs/sft",
            num_train_epochs=1 if test_mode else 3,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            warmup_ratio=0.1,
            lr_scheduler_type="cosine",
            logging_steps=25,
            eval_steps=100,
            save_strategy="epoch",
            bf16=True,
            report_to="none",  # cambiar a "wandb" si quieren tracking
        ),
    )

    print("Iniciando SFT...")
    trainer.train()

    if not test_mode:
        print(f"Subiendo modelo a {HF_MODEL_OUT}...")
        trainer.model.push_to_hub(HF_MODEL_OUT, token=os.getenv("HF_TOKEN"))
        print("✅ Modelo SFT subido")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",
                        help="Modo test: verifica entorno con 50 ejemplos")
    args = parser.parse_args()

    if args.test:
        verificar_entorno()
    else:
        entrenar_sft(test_mode=False)
