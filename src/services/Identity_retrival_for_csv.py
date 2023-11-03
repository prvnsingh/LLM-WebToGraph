from langchain.document_loaders.csv_loader import CSVLoader

from app import utils
from app.llm import LLM
from components.base_component import BaseComponent
from data_services.Neo4jDumper import Neo4jDumper
from datalayer.datapreprocessor import DataPreprocessor


class NameIdentityRetrievalForCsv(BaseComponent):
    def __init__(self, model_name):
        super().__init__('NameIdentityRetrievalForCsv')
        self.sources = utils.read_yaml_file('C:/Users/sejal/Downloads/codin/LLM-WebToGraph/src/datalayer/datasources.yml')
        self.csv_sources = self.sources.get('csv', [])
        self.html_sources = self.sources.get('link', [])
        self.model_name = model_name

    def run(self):
        for csvfile in self.csv_sources:
            # loading the csv using langchain document loader for csv
            loader = CSVLoader(file_path=csvfile)
            data = loader.load()

            # setting up openai model and extracting knowledge graph
            open_ai_llm = LLM(model=self.model_name)
            self.logger.info(f'loading model {open_ai_llm}')
            # just sending last few lines of csv as the token limit is limited of openai api free version.
            # model should  be changed to claude2 (Anthropic) or premium openai api key should be used.
            response = open_ai_llm.run(input_text=data[-1])
            self.logger.info(f'response: {response}')
            # instantiating neo4jBD and dumping the knowledge graph
            neo4j_instance = Neo4jDumper(config_path='app/config.yml')
            neo4j_instance.run(data=response)
            self.logger.info(f'knowledge graph populated successfully')
