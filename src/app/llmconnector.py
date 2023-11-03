import os

from dotenv import load_dotenv
from langchain.llms import HuggingFacePipeline
from torch import bfloat16
from transformers import AutoTokenizer, pipeline

load_dotenv()

# begin initializing HF items, need auth token for these
hf_auth = os.getenv("HF_AUTH_TOKEN")
print(hf_auth)

# For hugging face models using HuggingFacePipeline
model_id = 'meta-llama/Llama-2-7b-hf'
task = 'text-generation'
tokenizer = AutoTokenizer.from_pretrained(model_id)
pipeline = pipeline(
    task=task,
    model='ValiantLabs/ShiningValiant',
    tokenizer=tokenizer,
    torch_dtype=bfloat16,
    device_map="auto",
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
#
# For quantized models
# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
# bnb_config = transformers.BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type='nf4',
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_compute_dtype=bfloat16
# )
# print(transformers.is_bitsandbytes_available())
llm = HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature': 0})
#
from langchain.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain = prompt | llm

question = "What is electroencephalography?"

print(chain.invoke({"question": question}))
# schema = get_schema()
# chain = create_extraction_chain(schema,llm)
# print(chain.run())