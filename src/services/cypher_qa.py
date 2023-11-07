from langchain.chains import GraphCypherQAChain
from app.llm import Llm
from components.base_component import BaseComponent
from datalayer.Neo4jDumper import Neo4jDumper


class CypherQa(BaseComponent):
    def __init__(self, model_name):
        super().__init__('cypher_qa')
        # instantiating the openai llm model and neo4j connection
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        self.open_ai_llm = Llm(model=model_name)
        # schema = utils.read_yaml_file('services/schemaN.yml')
        # graph_schema = construct_schema(schema,[],[])
        print(self.neo4j_instance.graph.schema)
        self.cypher_chain = GraphCypherQAChain.from_llm(
            cypher_llm=self.open_ai_llm.llm,
            qa_llm=self.open_ai_llm.llm,
            graph=self.neo4j_instance.graph,
            # validate_cypher=True,  # Validate relationship directions
            verbose=True,
        )

    def run(self, text):
        return self.cypher_chain.run(text)
