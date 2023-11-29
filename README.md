# LLM-WebToGraph

LLM-WebToGraph is a powerful project that harnesses the capabilities of Langchain and OpenAI's Language Models (LLMs) to scrape data from various sources on the web, transforming it into a structured knowledge graph. This knowledge graph is then populated into a Neo4j Aura Database, providing an efficient way to store, query, and retrieve information using cypher query and LLMs. With the synergy of Langchain, OpenAI LLMs, and Neo4j, this project offers a robust solution for knowledge management and retrieval.

## Architecture
![design](https://github.com/prvnsingh/LLM-WebToGraph/blob/main/design.jpg?raw=true)

## Working directory
![Directory Tree](https://github.com/prvnsingh/LLM-WebToGraph/blob/main/dirTree.jpg?raw=true)

## Demo snapshot
![Demo snapshot](https://github.com/prvnsingh/LLM-WebToGraph/blob/main/working.jpg?raw=true)

## Overview

The LLM-WebToGraph project combines several key components to achieve its goal:

1. **Langchain:** A language model designed for natural language understanding and generation, powering the core of the project.

2. **OpenAI's Language Models (LLMs):** These models are used to extract and process data from various sources, converting unstructured data into structured knowledge.

3. **Neo4j Aura Database:** The project stores the structured knowledge graph in a Neo4j Aura Database, allowing for efficient storage and retrieval.

4. **FastAPI:** To expose an API for interacting with the project and to check its health status.

5. **Streamlit:** For building a user-friendly interface to query and visualize the knowledge graph.

## Features

- Web scraping from various sources, such as web links and CSV files.
- Data transformation and extraction using OpenAI LLM (gpt-3.5-turbo).
- Population of a structured knowledge graph in Neo4j Aura Database.
- FastAPI-based health check API to monitor the application's status.
- Streamlit web application for querying and visualizing the knowledge graph.

## Getting Started
1. Configuring the data sources
   - Update the data files .csv in the data directory.
   - Update the links of html in datasource.yml
2. Setup environment variables
   - Add credentials in .env file like openAI api key and neo4jDB password or add environment variables.

3. Configure the schema.yml for identities and relationships
   - Modify the schema.yml to specify the identities to be recognized.
4. Run the streamlit UI and FASTAPI app.
   - build docker and run the image with env file
~~~sh
   sudo docker run --env-file .env -p 8501:8501 -p 8000:8000 image_name 
~~~
To access the application
~~~html
http://localhost:8501/
~~~

To check backend APIs, access the swagger at
```html
http://localhost:8000/docs
```
 

## Contributing

Contributions to the LLM-WebToGraph project are welcome! If you'd like to contribute, please follow these guidelines:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and ensure tests pass.
- Submit a pull request.

## Future Scope
In the future, the project can be extended with a microservices architecture, including:

A separate data service responsible for ingesting data from S3.
Utilization of a Selenium bot to scrape the web and download CSV files.
Integration with more data sources for enhanced knowledge graph creation.

## References
- [Langchain Graph Transformer Documentation](https://python.langchain.com/docs/use_cases/graph/diffbot_graphtransformer)
- [Langchain Cypher Query Documentation](https://python.langchain.com/docs/use_cases/graph/graph_cypher_qa)
- [Blog Post: Constructing Knowledge Graphs from Text](https://blog.langchain.dev/constructing-knowledge-graphs-from-text-using-openai-functions/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, feel free to contact us at [prvns1997@gmail.com](mailto:prvns1997@email.com).
