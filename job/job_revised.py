import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.readers.file import CSVReader
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core import Settings
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import ReActAgent
from typing import Optional
from llama_index.core import PromptTemplate
from llama_index.llms.gemini import Gemini

import nest_asyncio
import sys
import logging
import requests

nest_asyncio.apply()

# Initialize logging
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Initialize settings
system_prompt = """
You are a multi-lingual career advisor expert who has knowledge based on 
real-time data. You will always try to be helpful and try to help them 
answering their question. If you don't know the answer, say that you DON'T
KNOW.

You primary job is to help students find jobs related to their interests from the Jobstreet Platform.
"""

Settings.llm = Gemini(
    model="models/gemini-2.0-flash",
    api_key="AIzaSyD6iVXg3LFrSTA5gEJ4tmY2UniNdAZqcxo",  # Replace with your own API key
    system_prompt=system_prompt, temperature=0
)
Settings.embed_model = OllamaEmbedding(base_url="http://127.0.0.1:11434", model_name="mxbai-embed-large:latest")

# Main Program
st.title("RAG Test")

# Initialize chat history if empty
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Mau tahu apa tentang pekerjaan?"}
    ]

def job_json_to_natural_language(json_data):
    """Converts the given JSON data into natural language for multiple job listings."""
    output = ""
    for job in json_data["data"]:
        advertiser_description = job["advertiser"]["description"]
        company_name = job.get("companyName", advertiser_description)
        title = job["title"]
        locations = ", ".join([loc["label"] for loc in job["locations"]])
        listing_date_display = job["listingDateDisplay"]
        teaser = job["teaser"]
        work_types = ", ".join(job["workTypes"])
        work_arrangements = ", ".join([wa["label"]["text"] for wa in job["workArrangements"]["data"]])
        classification_description = job["classifications"][0]["classification"]["description"]
        subclassification_description = job["classifications"][0]["subclassification"]["description"]

        job_description = f"""
    Lowongan pekerjaan dipublikasikan oleh {advertiser_description} ({company_name}).
    Posisi yang ditawarkan adalah {title} di {locations}.
    Lowongan ini dipublikasikan {listing_date_display}.
    Deskripsi singkat pekerjaan: {teaser}.
    Tipe pekerjaan: {work_types}.
    Penempatan kerja: {work_arrangements}.
    Klasifikasi pekerjaan: {classification_description} - {subclassification_description}.
    """

        output += job_description + "\n---\n"

    return output.rstrip("\n---")  # Remove trailing newline and separator

# Declare Tools
def search_jobstreet(keyword: str) -> str:
    """Searches the JobStreet database for matching entries."""
    r = requests.get("https://id.jobstreet.com/api/jobsearch/v5/search", params={
        "siteKey": "ID-Main",
        "sourcesystem": "houston",
        "page": "1",
        "worktype": "242",
        "sortmode": "ListedDate",
        "pageSize": "32",
        "include": "seodata,joracrosslink,gptTargeting,pills",
        "locale": "id-ID",
        "keywords": keyword,
        "baseKeywords": keyword
    })

    data = r.json()
    output = f"# Hasil Pencarian Pekerjaan untuk '{keyword}'\n{job_json_to_natural_language(data)}"
    return output

search_jobstreet_tool = FunctionTool.from_defaults(fn=search_jobstreet)

# Initialize the chat engine
if "chat_engine" not in st.session_state.keys():
    init_history = [
        ChatMessage(role=MessageRole.ASSISTANT, content="Halo! Mau tahu apa tentang lowongan pekerjaan?"),
    ]
    memory = ChatMemoryBuffer.from_defaults(token_limit=32768)
    st.session_state.chat_engine = ReActAgent.from_tools(
        [search_jobstreet_tool],
        chat_mode="react",
        verbose=True,
        memory=memory,
        llm=Settings.llm
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Apa yang ingin Anda cari?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if the user is asking about jobs

    with st.chat_message("assistant"):
        with st.spinner("Mencari pekerjaan..."):
                response = search_jobstreet(prompt)  # Call the synchronous function
                st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
