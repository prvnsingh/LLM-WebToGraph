from langchain.document_loaders.csv_loader import CSVLoader
from app import utils
from app.llm import Llm
from components.base_component import BaseComponent
from datalayer.Neo4jDumper import Neo4jDumper


class NameIdentityRetrievalForCsv(BaseComponent):
    def __init__(self, model_name, data_path):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all its attributes.
        The self parameter refers to an instance of a class, and it's required in order for Python to know which object you're referring to.

        :param self: Represent the instance of the class
        :param model_name: Instantiate the openai llm model
        :param data_path: Read the yaml file which contains the path to all csv files
        :return: The instance of the class
        """
        super().__init__('NameIdentityRetrievalForCsv')
        self.sources = utils.read_yaml_file(data_path)
        self.csv_sources = self.sources.get('csv', [])
        # instantiating the openai llm model and neo4j connection
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        self.open_ai_llm = Llm(model=model_name)

    def run(self, **kwargs):
        """
        The run function is the main function of this module. It takes in a list of csv files and extracts knowledge graph from them using openai api.
        The knowledge graph is then dumped into neo4j database.

        :param self: Represent the instance of the class
        :return: A tuple of the following:
        """
        for csvfile in self.csv_sources:
            # loading the csv using langchain document loader for csv
            loader = CSVLoader(file_path=csvfile)
            data = loader.load()

            # setting up openai model and extracting knowledge graph
            self.logger.info(f'loading model {self.open_ai_llm}')
            # just sending last few lines of csv as the token limit is limited of openai api free version.
            # model should  be changed to claude2 (Anthropic) or premium openai api key should be used.
            # response = self.open_ai_llm.extract_and_store_graph(document=data[-1])
            response = self.open_ai_llm.run(input_text=data[-1])
            # instantiating neo4jBD and dumping the knowledge graph
            self.neo4j_instance.run(data=response)
            self.logger.info(f'knowledge graph populated successfully for data source: {csvfile}')
