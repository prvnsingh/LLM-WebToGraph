from langchain.document_loaders import AsyncChromiumLoader, AsyncHtmlLoader
from langchain.document_transformers import BeautifulSoupTransformer
from app import utils
from app.llm import LLM
from components.base_component import BaseComponent
from data_services.Neo4jDumper import Neo4jDumper


class NameIdentityRetrievalForHtml(BaseComponent):
    def __init__(self, model_name, data_path):
        super().__init__('NameIdentityRetrievalForHtml')
        self.sources = utils.read_yaml_file(data_path)
        self.html_sources = self.sources.get('link', [])
        # instantiating the openai llm model and neo4j connection
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        self.open_ai_llm = LLM(model=model_name)

    def run_async(self, **kwargs):
        for link in self.html_sources:
            loader =AsyncHtmlLoader(link)
            html = loader.load()
            # html = loader.load()
            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["table"])
            self.logger.info(docs_transformed[0].page_content[0:500])

            # setting up openai model and extracting knowledge graph
            self.logger.info(f'loading model {self.open_ai_llm}')
            tokens_cap = len(docs_transformed[0].page_content) - 4

            # just sending last few lines of csv as the token limit is limited of openai api free version.
            # model should  be changed to claude2 (Anthropic) or premium openai api key should be used.
            response = self.open_ai_llm.run(input_text=docs_transformed[0].page_content[tokens_cap:])
            # instantiating neo4jBD and dumping the knowledge graph
            self.neo4j_instance.run(data=response)
            self.logger.info(f'knowledge graph populated successfully for data source: {link}')
