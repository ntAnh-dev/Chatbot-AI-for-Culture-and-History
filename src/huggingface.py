from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.environ.get('HF_TOKEN')

models = [
    {
        "provider": "together",
        "model": "deepseek-ai/DeepSeek-R1"
    },
    {
        "provider": "hf-inference",
        "model": "Qwen/QwQ-32B"
    },
    {
        "provider": "fireworks-ai",
        "model": "deepseek-ai/DeepSeek-V3-0324"
    },
    {
        "provider": "cerebras",
        "model": "meta-llama/Llama-3.3-70B-Instruct"
    }
]

def getClient(provider):
    return InferenceClient(
        provider=provider,
        api_key=HF_TOKEN
    )

def getOutput(provider, model, input):
    client = getClient(provider=provider)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": input
            }
        ],
        max_tokens=None,
    )

    return completion.choices[0].message