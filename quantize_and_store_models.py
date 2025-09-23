# Script to download, quantize, and store multiple models for local use
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# List of recommended models to store locally
RECOMMENDED_MODELS = [
    "distilgpt2"
]

for model_name in RECOMMENDED_MODELS:
    print(f"\nProcessing {model_name}...")
    local_dir = f"quantized_{model_name.replace('/', '_')}"
    if os.path.exists(local_dir):
        print(f"Already exists: {local_dir}")
        continue
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True,
            device_map="auto"
        )
        model.save_pretrained(local_dir)
        tokenizer.save_pretrained(local_dir)
        print(f"Saved quantized model to {local_dir}")
    except Exception as e:
        print(f"Failed to process {model_name}: {e}")
print("\nAll done!")
