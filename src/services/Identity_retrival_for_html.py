from typing import Union, List

from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import BeautifulSoupTransformer
from app import utils
from app.llm import Llm
from components.base_component import BaseComponent
from datalayer.Neo4jDumper import Neo4jDumper


class NameIdentityRetrievalForHtml(BaseComponent):
    def __init__(self, model_name, data_path):

        """
        The __init__ function is called when the class is instantiated.
        It sets up the initial values of all attributes for an instance of a class.
        The self parameter refers to the current instance of a class, and it's required by Python.

        :param self: Represent the instance of the class
        :param model_name: Specify the model name that we want to use for our predictions
        :param data_path: Read the yaml file which contains the links to be scraped
        :return: Nothing
        """
        super().__init__('NameIdentityRetrievalForHtml')
        self.sources = utils.read_yaml_file(data_path)
        self.html_sources = self.sources.get('link', [])
        # instantiating the openai llm model and neo4j connection
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        self.open_ai_llm = Llm(model=model_name)

    def run_async(self, **kwargs):

        """
        The run_async function is used to run the pipeline asynchronously.
            It takes in a list of html sources and extracts knowledge graph from them using openai api.
            The extracted knowledge graph is then dumped into neo4j database.

        :param self: Represent the instance of the object itself
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A list of all the knowledge graphs extracted from the html sources
        """
        for link in self.html_sources:
            loader =AsyncHtmlLoader(link)
            html = loader.load()
            # html = loader.load()
            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["table"])
            self.logger.info(docs_transformed[0].page_content[0:500])

            # setting up openai model and extracting knowledge graph
            self.logger.info(f'loading model {self.open_ai_llm}')

            # just sending last few lines of csv as the token limit is limited of openai api free version.
            # model should  be changed to claude2 (Anthropic) or premium openai api key should be used.
            # response = self.open_ai_llm.extract_and_store_graph(document=docs_transformed[0])
            tokens_cap = len(docs_transformed[0].page_content) - 4
            response = self.open_ai_llm.run(input_text=docs_transformed[0].page_content[tokens_cap:])
            # instantiating neo4jBD and dumping the knowledge graph
            self.neo4j_instance.run(data=response)
            self.logger.info(f'knowledge graph populated successfully for data source: {link}')

    def run(self, input: Union[str, List[float]]) -> str:
        pass
