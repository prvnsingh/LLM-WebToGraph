#!/usr/bin/env python
# coding: utf-8

# # BYO Knowledge Graph
# 
# The notebook shows the use of open source APIs to create knowledge graph and key phrase metadata for [LangChain](https://github.com/hwchase17/langchain) [Document](https://github.com/hwchase17/langchain/blob/1ff7c958b0a84b08c84eebba958b5b3fb0e6e409/langchain/schema.py#L269). 
# 
# More details of the code can be found below:
# 
# - [**EntityExtractor**](../../../../slangchain/nlp/ner/entity_extractor.py): Uses [Spacy](https://spacy.io/) to extract [named entities](https://machinelearningknowledge.ai/named-entity-recognition-ner-in-spacy-library/) in text.
# 
# - [**KnowledgeGraph**](../../../../slangchain/nlp/ner/knowledge_graph.py): Heavily inspired by [knowledge graph generation](https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa) using HuggingFace's [Bablescape model](https://huggingface.co/Babelscape/rebel-large).
# 
# - [**KeyPhraseExtractor**](../../../../slangchain/nlp/ner/phrase_extractor.py): Uses HuggingFace [ml6team's key phrase extractor model](https://huggingface.co/ml6team/keyphrase-extraction-distilbert-inspec) to extract important key phrases from the text.
# 
# If you haven't already done so, instructions to setup the environment can be found [here](../../../../README.md).

# ## Setup Parameters

# In[ ]:


import os
chunk_size = 256
chunk_overlap = 30
os.environ["OPENAI_API_KEY"] = ""
os.environ["PINECONE_API_KEY"] = ""
os.environ["PINECONE_ENV"] = ""


# ## Sample Data
# 
# Let's first load some sample data

# In[2]:


from langchain.document_loaders.html import WikipediaLoader

loader = WikipediaLoader(query="LeBron James")
documents = loader.load()


# Split the documents into chunks

# In[3]:


from langchain.text_splitter import TokenTextSplitter

text_splitter = TokenTextSplitter(
  chunk_size = chunk_size,
  chunk_overlap = chunk_overlap
)
split_documents = text_splitter.split_documents(documents)


# ## Content Tagging and Knowledge Graph
# 
# Let's now instantiate the classes required to create the tags and knowledge graphs. It might take awhile to download the models from hugging face initially, but you'll only have to do it once:
# 
# - [**EntityExtractor**](../../../../slangchain/nlp/ner/entity_extractor.py): Uses [Spacy](https://spacy.io/) to extract [named entities](https://machinelearningknowledge.ai/named-entity-recognition-ner-in-spacy-library/) in text.
# 
# - [**KnowledgeGraph**](../../../../slangchain/nlp/ner/knowledge_graph.py): Inspired by [knowledge graph generation](https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa) using HuggingFace's [Bablescape model](https://huggingface.co/Babelscape/rebel-large).
# 
# - [**KeyPhraseExtractor**](../../../../slangchain/nlp/ner/phrase_extractor.py): Uses HuggingFace [ml6team's key phrase extractor model](https://huggingface.co/ml6team/keyphrase-extraction-distilbert-inspec) to extract important key phrases from the text.
# 

# In[4]:

import spacy
from slangchain.nlp.ner.entity_extractor import EntityExtractor
from slangchain.nlp.ner.phrase_extractor import KeyPhraseExtractor
from slangchain.nlp.ner.knowledge_graph import KnowledgeGraph

kg_kwargs = {"max_length": chunk_size + 100}

entity_extractor = EntityExtractor()
knowledge_graph = KnowledgeGraph(**kg_kwargs)
key_phrase_extractor = KeyPhraseExtractor()


# Create the tags and knowledge graph per Document chunk.
# 
# The document tags are a combination of the outputs from [**EntityExtractor**](../../../../slangchain/nlp/ner/entity_extractor.py) (persons organisations, and locations) and [**KeyPhraseExtractor**](../../../../slangchain/nlp/ner/phrase_extractor.py) generates the key phrases from the content/text.
# 
# Unlike [OpenSearch](https://opensearch.org/), Pinecone does not allow searches over a list of Dictionary objects. As a workaround, we have mapped the Knowledge graph's subjects, relations and objects as list of strings. We're open to suggestions as to how we could better structure the entity relationships within the metadata payload.

# In[11]:


for document in split_documents:
  entity_extractor.inference(document.page_content)
  persons = entity_extractor.persons
  organisations = entity_extractor.organisations
  locations = entity_extractor.locations

  key_phrases = key_phrase_extractor.inference(document.page_content)
  entity_relations = knowledge_graph.inference(document.page_content)

  tags = persons + organisations + locations + key_phrases
  tags = list({i for i in tags})
  document.metadata.update({
    "tags": tags,
    "subjects": list({i["subject"] for i in entity_relations}),
    "relations": list({i["relation"] for i in entity_relations}),
    "objects": list({i["object"] for i in entity_relations}),
  })


# As per the print out below, the tags and knowledge graph metadata have been added to the documents.

# In[13]:


print(f'Content: {split_documents[0].page_content}\n')
print(f'Tags: {split_documents[0].metadata["tags"]}\n')
print(f'Subjects: {split_documents[0].metadata["subjects"]}\n')
print(f'Relations: {split_documents[0].metadata["relations"]}\n')
print(f'Objects: {split_documents[0].metadata["objects"]}\n')


# In[14]:


split_documents[0].metadata


# ## Creating our self-querying retriever
# Now we can instantiate our retriever. To do this we'll need to have a Pinecone instance. To use Pinecone, you must have an API key. 
# Here are the [installation instructions](https://docs.pinecone.io/docs/quickstart).
# 

# In[15]:


import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone


document_content_description = "Content of Wikipedia page"
llm = OpenAI(temperature=0)
embedding = OpenAIEmbeddings()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV")  # next to api key in console
)

index_name = "kg-slangchain-demo"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)
vectordb = Pinecone.from_documents(split_documents, embedding, index_name=index_name)


# Now we can instantiate our retriever. To do this we'll need to provide some information upfront about the metadata fields that our documents support and a short description of the document contents.

# In[16]:


from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.chains import RetrievalQA

metadata_field_info=[
    AttributeInfo(
        name="title",
        description="The Wikipedia page title", 
        type="string", 
    ),
    AttributeInfo(
        name="summary",
        description="The Wikipedia page summary", 
        type="string", 
    ),
    AttributeInfo(
        name="source",
        description="The Wikipedia page source url", 
        type="string", 
    ),
    AttributeInfo(
        name="tags",
        description="List of delimited Key word phrases from the content",
        type="string or list[string]"
    ),
    AttributeInfo(
        name="subjects",
        description="List of Subject Knowledge graph entities from the content",
        type='''list[string]'''
    ),
    AttributeInfo(
        name="relations",
        description="List of Subject Knowledge graph entities from the content",
        type='''list[string]'''
    ),
    AttributeInfo(
        name="objects",
        description="List of Subject Knowledge graph entities from the content",
        type='''list[string]'''
    )
]

retriever = SelfQueryRetriever.from_llm(
    llm, vectordb, document_content_description, metadata_field_info, verbose=True
)
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True
)


# ## Testing it Out

# ### Query on Knowledge Graph Objects
# 
# An example query based on Knowledge Graph objects

# In[93]:


qa_chain("Lebron James achievements where objects is regular season")


# ### Query on Knowlege Graph Subjects
# 
# An example query based on Knowledge Graph subjects

# In[82]:


qa_chain("Lebron James playing age where subjects is Amateur Athletic Union")


# ### Query on Knowlege Graph Relations
# 
# An example query based on Knowledge Graph relations

# In[84]:


qa_chain("Lebron James draft year where relations is point in time")


# ### Query on Knowlege Graph Key Combinations
# 
# An example query based on Knowledge Graph key combinations (objects, subjects and relations)

# In[91]:


qa_chain("Lebron James achievements where relations is point in time and subjects is Finals and objects is 2016")


# ### Query on Tags
# 
# An example query based on Tags

# In[87]:


qa_chain("Lebron James losses where tags is finals")

