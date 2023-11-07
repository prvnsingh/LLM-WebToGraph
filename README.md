# LLM-WebToGraph
It is project which uses transformer to scrape the web and LLM to retrieve the identity from the text and store it in neo4j.

Data sources
World Bank - https://www.worldbank.org/en/projects-operations/procurement, https://projects.worldbank.org/en/projects-operations/projects-list
Sam Gov - https://sam.gov/content/opportunities

objective:
Extract entities, a.k.a. Named Entity Recognition (NER), which are going to be the nodes of the knowledge graph.
Extract relations between the entities, a.k.a. Relation Classification (RC), which are going to be the edges of the knowledge graph.


TL:DR:
Change data files in data directory and configure data source.yml file
Edit Env file and provide correct configuration 
Edit Schema file for identities to be recognized
run main.py

Brief:
In this project we have created and interface for populating and retrieving information for graphdb using LLMs.
I have LAMA2 model/openAI model  for NER (name identity recognition) algorithm. Identities are specified in the schema.json file.
I have also used cypher query to generate insights from graphBD. 


Future Scope:
for microservices architecture
    A separate data service which dumps data to S3. This service will ingest data from s3 rather than data directory. The downstream service include Selenium bot that scrape web and download csv from (). 
    

https://python.langchain.com/docs/use_cases/graph/diffbot_graphtransformer
https://python.langchain.com/docs/use_cases/graph/graph_cypher_qa
https://blog.langchain.dev/constructing-knowledge-graphs-from-text-using-openai-functions/