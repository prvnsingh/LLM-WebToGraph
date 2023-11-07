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
    """
    The get_schema function reads the schema.yml file and returns a dictionary of the schema.

    :return: The schema
    :doc-author: Trelent
    """
    schema = utils.read_yaml_file('services/schema.yml')
    return schema


class Llm(BaseComponent):

    def __init__(self, model: str):
        super().__init__('Lllm')
        self.model = model
        # for huggingface hub models
        # self.llm = HuggingFaceHub(repo_id='ValiantLabs/ShiningValiant', task='text-generation',
        #                           huggingfacehub_api_token=os.getenv('HF_AUTH_TOKEN'),
        #                           model_kwargs={"temperature": 0, "max_length": 64})
        self.llm = ChatOpenAI(temperature=0, model_name=model, openai_api_key=os.getenv('OPENAI_API_KEY'))

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def run(self, input_text):
        """
        The run function is the main entry point for your component.
        It will be called with a string of text to process, and should return a dictionary of results.
        The keys in this dictionary are the names of slots that you defined in your schema.

        :param self: Represent the instance of the class
        :param input_text: Pass the text that we want to extract entities from
        :return: A dictionary with the following structure:
        """
        schema = get_schema()
        self.logger.info(f'schema: {schema}')
        chain = create_extraction_chain(schema, self.llm)
        llm_response = chain.run(input_text)
        self.logger.info(f'llm_response: {llm_response}')
        return llm_response
