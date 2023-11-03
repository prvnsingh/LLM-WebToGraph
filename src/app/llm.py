import os

import backoff
import openai  # for OpenAI API calls
from dotenv import load_dotenv
from langchain.chains import create_extraction_chain
from langchain.chat_models import ChatOpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from app import utils
from components.base_component import BaseComponent

load_dotenv()


def get_schema():
    schema = utils.read_yaml_file('services/schema.yml')
    return schema


class LLM(BaseComponent):
    def __init__(self, model: str):
        super().__init__('LLM')
        self.model = model
        # self.llm = HuggingFaceHub(repo_id='ValiantLabs/ShiningValiant', task='text-generation',
        #                           huggingfacehub_api_token=os.getenv('HF_AUTH_TOKEN'),
        #                           model_kwargs={"temperature": 0, "max_length": 64})
        self.llm = ChatOpenAI(temperature=0, model_name=model, openai_api_key=os.getenv('OPENAI_API_KEY'))

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def run(self, input_text):
        schema = get_schema()
        self.logger.info(f'schema: {schema}')
        chain = create_extraction_chain(schema, self.llm)
        return chain.run(input_text)
