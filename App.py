import streamlit as st
import os
import dotenv
from neo4j_graphrag.exceptions import RetrieverInitializationError, SearchValidationError, Text2CypherRetrievalError, \
    RagInitializationError
from neo4j_graphrag.generation.types import RagResultModel
from neo4j_graphrag.types import RetrieverResult
from openai import OpenAI

from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.llm import AzureOpenAILLM

from neo4j_graphrag.generation import GraphRAG

load_status = dotenv.load_dotenv(".env")
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

azure_open_ai_uri = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_open_ai_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_open_ai_key_Version = os.getenv("AZURE_OPENAI_API_KEY_VERSION")
azure_open_ai_model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")

st.set_page_config(
    page_title="DBGraphXplore App",
    page_icon="👋",
)

st.sidebar.success("Welcome")
st.title("DBGraphXplore App")

AUTH = (neo4j_username, neo4j_password)

# Connect to Neo4j database
driver = GraphDatabase.driver(neo4j_uri, auth=AUTH)
driver.verify_connectivity()
print("\nConnection established with Neo4j database.")

# Create LLM object
llm = AzureOpenAILLM(
                        azure_endpoint = azure_open_ai_uri,  # update with your endpoint
                        api_key = azure_open_ai_key,  # api_key is optional and can also be set with OPENAI_API_KEY env var
                        api_version = azure_open_ai_key_Version,
                        model_name=azure_open_ai_model_name,
                        model_params=  {
                                            "temperature": 0,
                                        }
                    )

# (Optional) Specify your own Neo4j schema
neo4j_schema = ""

# (Optional) Provide user input/query pairs for the LLM to use as examples
examples = []

# Initialize the retriever
# Text2CypherRetriever Allows for the retrieval of records from a Neo4j database using natural language. Converts a user’s natural language query to a Cypher query using an LLM,
# then retrieves records from a Neo4j database using the generated Cypher query
# Parameters:
# driver (neo4j.Driver) – The Neo4j Python driver.
# llm (neo4j_graphrag.generation.llm.LLMInterface) – LLM object to generate the Cypher query.
# neo4j_schema (Optional[str]) – Neo4j schema used to generate the Cypher query.
# examples (Optional[list[str], optional) – Optional user input/query pairs for the LLM to use as examples.
# custom_prompt (Optional[str]) – Optional custom prompt to use instead of auto generated prompt. Will not include the neo4j_schema or examples args, if provided.
# result_formatter (Optional[Callable[[neo4j.Record], RetrieverResultItem]])
retriever = None
try:
    retriever = Text2CypherRetriever(driver=driver, llm=llm,  neo4j_schema=neo4j_schema, examples=examples) # type: ignore
except RetrieverInitializationError as error:
    print("Error: " + str(error))

# Performs a GraphRAG search using a specific retriever and LLM.
# Initialize the RAG pipeline
# Parameters:
# retriever (Retriever) – The retriever used to find relevant context to pass to the LLM.
# llm (LLMInterface) – The LLM used to generate the answer.
# prompt_template (RagTemplate) – The prompt template that will be formatted with context and user question and passed to the LLM.
rag = None
try:
    rag = GraphRAG(retriever=retriever, llm=llm)
except RagInitializationError as error: #If validation of the input arguments fail.
    print("Error: RagInitializationError, Validation of the input arguments fail" + str(error))

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about database"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Converts text to a Cypher query using an LLM.
            # Generate a Cypher query using the LLM, send it to the Neo4j database, and return the results
            # result:RetrieverResult = retriever.search(query_text=prompt)
            # response = st.write(result.items)

            # This method performs a full RAG search
            # 1. Retrieval: context retrieval
            # 2. Augmentation: prompt formatting
            # 3. Generation: answer generation with LLM

            # Parameters:
            # query_text (str) – The user question
            # examples (str) – Examples added to the LLM prompt.
            # retriever_config (Optional[dict]) – Parameters passed to the retriever search method; e.g.: top_k
            # return_context (bool) – Whether to append the retriever result to the final result (default: False)
            result:RagResultModel = rag.search(query_text=prompt, return_context=True)

            print("Cypher Query: ")
            print(result.retriever_result.metadata['cypher'])
            print("Result: ")
            print(result.answer)

            st.markdown(result.answer)
            #response = st.write(result.answer)
            response = result.answer

            #print("Query Text : "+ prompt)
            #print("Cypher Query: ")
            #$print(str(result.metadata['cypher']))
        except SearchValidationError as error: # If validation of the input arguments fail.
            response = "Error: SearchValidationError, Validation of the input arguments fail. "
            print( response + str(error))
        except Text2CypherRetrievalError as error: # If the LLM fails to generate a correct Cypher query.
            response = "Error: Text2CypherRetrievalError, The LLM fails to generate a correct Cypher query. "
            print(response + str(error))

        st.session_state.messages.append({"role": "assistant", "content": response})
