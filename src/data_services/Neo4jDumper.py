from neo4j import GraphDatabase

from app import utils
from components.base_component import BaseComponent


def _dump_data_to_neo4j(tx, data):
    for key, value in data.items():
        # Creating a node for each key-value pair (identity-relationship pair)
        tx.run()


class Neo4jDumper(BaseComponent):
    def __init__(self, config_path):
        super().__init__('Neo4jDumper')
        config = utils.read_yaml_file(config_path)
        self.uri = config.get('neo4j').get('uri')
        self.username = config.get('neo4j').get('username')
        self.password = config.get('neo4j').get('password')

    def dump_data(self, tx, data):
        for key, value in data.items():
            # Create a node for each key-value pair
            tx.run(query="CREATE (n:Node {key: $key, value: $value})", key=key, value=value)
            self.logger.info(f"Dumped data for {key}: {value} to neo4j")

    def run(self, data):
        try:
            with GraphDatabase.driver(self.uri, auth=(self.username, self.password)) as driver:
                with driver.session() as session:
                    self.dump_data(session, data)
            self.logger.info("Neo4j database connected successfully. and data dumped successfully.")
            return driver.session()
        except Exception as e:
            self.logger.error(f"Error while connecting to neo4j: {str(e)}")
