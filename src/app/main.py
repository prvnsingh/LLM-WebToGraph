import json

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app import utils
from services.Identity_retrival_for_csv import NameIdentityRetrievalForCsv

app = FastAPI(
    title="LLM-WebToGraph",
    description="""This project using langchain and OpenAI LLM to transform data from different sources (web 
    links/csv) to knowledge graph and store then in neo4j DB.""",
    version="0.1.0",
)


@app.get("/generate_tags")
async def generate_tags():
    ner = NameIdentityRetrievalForCsv(model_name='gpt-3.5-turbo', data_path='datalayer/datasources.yml')
    ner.run()
    return HTMLResponse(content='Successfully generated the knowledge from the data sources!!!', status_code=200)

# health check route
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == '__main__':
    app_config = utils.read_yaml_file('app/config.yml')
    load_dotenv()
    uvicorn.run(app, port=app_config.get('port'), host=app_config.get('host'))
