# DBGraphXplore App

DBGraphXplore is an interactive Streamlit application designed to enable users to query a Neo4j database using natural language. It leverages Azure OpenAI for translating user inputs into Cypher queries, allowing seamless database interaction and knowledge retrieval. This tool is particularly useful for database administrators, data scientists, and anyone interested in graph database exploration with minimal Cypher knowledge.

## Features

- **Natural Language to Cypher Query Conversion**: Uses Azure OpenAI to translate user questions into Cypher queries.
- **Interactive Database Exploration**: Allows users to interactively ask questions about the database content.
- **Graph-RAG Search Pipeline**: Integrates a Retrieval-Augmented Generation (RAG) pipeline for enhanced query responses.
- **Real-Time Feedback**: Displays the generated Cypher queries and query results for user verification.

## Requirements

- **Python**: 3.8 or above
- **Streamlit**: For running the web application
- **Neo4j Python Driver**: For connecting to the Neo4j database
- **Azure OpenAI**: For generating Cypher queries from user inputs
- **Environment Variables**: Defined in a `.env` file

## Setup

### Environment Variables

Create a `.env` file in the project root with the following variables:

```dotenv
NEO4J_URI=<Your Neo4j URI>
NEO4J_USERNAME=<Your Neo4j Username>
NEO4J_PASSWORD=<Your Neo4j Password>
AZURE_OPENAI_ENDPOINT=<Your Azure OpenAI Endpoint>
AZURE_OPENAI_API_KEY=<Your Azure OpenAI API Key>
AZURE_OPENAI_API_KEY_VERSION=<Your Azure OpenAI API Key Version>
AZURE_OPENAI_MODEL_NAME=<Your Azure OpenAI Model Name>


### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/DBGraphXplore.git
   cd DBGraphXplore
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run App.py
   ```

## Usage

1. Start the application, which will connect to the specified Neo4j database.
2. Input any question related to the database in natural language.
3. The application translates the question into a Cypher query and retrieves the response from Neo4j.
4. The generated Cypher query and the database response are displayed for easy understanding and verification.

## Error Handling

The application handles several types of errors:
- **RetrieverInitializationError**: Occurs if there is an issue initializing the Cypher query retriever.
- **RagInitializationError**: Raised if there is an issue with the RAG pipeline.
- **SearchValidationError**: Triggered if input validation fails during search.
- **Text2CypherRetrievalError**: Raised if the LLM fails to generate a valid Cypher query.

## Acknowledgments

- Thanks to [Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/) for natural language processing capabilities.
- Thanks to [Streamlit](https://streamlit.io/) for providing an easy-to-use UI framework.
- Special thanks to [Neo4j](https://neo4j.com/) for enabling graph database support and Cypher query language.
