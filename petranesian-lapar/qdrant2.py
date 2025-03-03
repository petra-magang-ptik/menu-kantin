# chatbot.py
import os
import sys
import logging
import pandas as pd
import qdrant_client
import streamlit as st
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.readers.file import CSVReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.retrievers import QueryFusionRetriever
import nest_asyncio
from qdrant_client.http.models import VectorParams
import re
import requests
import json
from auth import register_user, login_user  # Import authentication functions

nest_asyncio.apply()

# Initialize Qdrant Client
QDRANT_URL = "https://a3040b4c-5492-488b-8b86-be3eae1626c1.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "u3TZLQzlOMlx4a1w63jUkj2hC_xNLfv3gu2v-jNxunPQlaB56eZMDA"

qdrant_client = qdrant_client.QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Ensure collection exists
collection_name = "kantin_menu"
def ensure_collection():
    collections = qdrant_client.get_collections()
    if collection_name not in [col.name for col in collections.collections]:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance="Cosine")
        )
        print(f"Collection '{collection_name}' created successfully.")
ensure_collection()

vector_store = QdrantVectorStore(client=qdrant_client, collection_name=collection_name)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Embedding model
embed_model = OllamaEmbedding(base_url="http://127.0.0.1:11434", model_name="nomic-embed-text:latest")

# Initialize node parser
splitter = SentenceSplitter(chunk_size=512)

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# System prompt for Gemini assistant
system_prompt = """
Anda adalah pelayan kantin yang ramah yang dapat mengarahkan pengguna mencari makanan/minuman yang tepat.
Anda tidak perlu menyebutkan atau membuat pernyataan yang mengatakan Anda tidak dapat menampilkan gambar jika gambar berhasil ditemukan.
Tugas Anda adalah untuk menjawab dengan relevansi sesuai menu dan menyarankan gambar jika sesuai tidak perlu memberikan path dari gambar.
Jawablah semua dalam Bahasa Indonesia.
Tugas Anda adalah untuk menjadi pelayan kantin yang ramah yang dapat mengarahkan user.
Kantin yang Anda layani adalah kantin kampus Universitas Kristen Petra Surabaya.
Pada Universitas Kristen Petra terdapat 2 gedung utama yang setiap gedungnya memiliki kantin, yaitu Gedung P dan W.
"""

# Set up the Gemini API key
API_KEY = "AIzaSyD6iVXg3LFrSTA5gEJ4tmY2UniNdAZqcxo"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# Function to communicate with Gemini API
def get_gemini_response(user_input):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": system_prompt + "\n" + user_input}]}]  # Add system prompt before user input
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Error: Unable to get a response."

Settings.llm = Ollama(model="llama3.1:latest", base_url="http://127.0.0.1:11434", system_prompt=system_prompt)
Settings.embed_model = embed_model

@st.cache_resource(show_spinner="Mempersiapkan data kantin – sabar ya.")
def load_data():
    csv_parser = CSVReader(concat_rows=False)
    file_extractor = {".csv": csv_parser}

    reader = SimpleDirectoryReader(
        input_dir="./docs",
        recursive=True,
        file_extractor=file_extractor
    )
    documents = reader.load_data()

    for doc in documents:
        doc.excluded_llm_metadata_keys = ["filename", "extension"]

    nodes = splitter.get_nodes_from_documents(documents, show_progress=True)

    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index_retriever = index.as_retriever(similarity_top_k=8)
    bm25_retriever = BM25Retriever.from_defaults(
        nodes=nodes,
        similarity_top_k=16,
    )

    return QueryFusionRetriever(
        [index_retriever, bm25_retriever],
        num_queries=2,
        use_async=True,
        similarity_top_k=24
    )

# Function to search data in Qdrant (Hybrid Matching)
def find_menu(user_input, filter_price=None, stall_name=None):
    query_vector = embed_model.get_text_embedding(user_input)  # Convert query to vector

    # Search for best matches in Qdrant collection
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=100  # Increase limit for better coverage
    )

    menu_data = []
    filtered_results = []

    for result in results:
        payload = result.payload
        if payload:
            product_name = payload.get("product_name", "")
            image_path = payload.get("image_path", "")
            kantin = payload.get("kantin", "Tidak diketahui")
            stall = payload.get("stall", "Tidak diketahui")
            harga = payload.get("harga", "Tidak diketahui")
            keterangan = payload.get("keterangan", "")

            # Convert price to numeric value
            harga_numerik = None
            if isinstance(harga, (int, float)):
                harga_numerik = float(harga)
            elif isinstance(harga, str):
                harga_cleaned = re.sub(r"[^\d]", "", harga)  # Remove non-numeric characters
                if harga_cleaned.isdigit():
                    harga_numerik = float(harga_cleaned)

            item_data = {
                "product_name": product_name,
                "image_path": image_path,
                "kantin": kantin,
                "stall": stall,
                "harga": harga,
                "harga_numerik": harga_numerik,
                "keterangan": keterangan
            }

            # Filter by product name or stall name if provided
            if stall_name:
                if stall_name.lower() in stall.lower():
                    filtered_results.append(item_data)
            elif user_input.lower() in product_name.lower():
                filtered_results.append(item_data)
            else:
                menu_data.append(item_data)

    # Apply price filter if specified
    if filter_price is not None:
        menu_data = [item for item in menu_data if item["harga_numerik"] is not None and item["harga_numerik"] <= filter_price]

    return filtered_results if filtered_results else menu_data

# Function to get all stalls
def get_all_stalls():
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=[0] * 768,  # Dummy vector to get all items
        limit=1000  # Adjust limit as necessary
    )

    stalls = set()  # Use a set to avoid duplicates
    for result in results:
        payload = result.payload
        if payload:
            stall = payload.get("stall", "Tidak diketahui")
            stalls.add(stall)

    return list(stalls)

# Function to clean user input
def clean_user_input(user_input):
    # Define a regex pattern to match variations of "gambar"
    pattern = r"\b(gambar|gmbr|image|gmb)\b"
    # Remove the matched patterns from the user input
    cleaned_input = re.sub(pattern, "", user_input, flags=re.IGNORECASE).strip()
    return cleaned_input

# Function to analyze user input and determine search type
def analyze_user_input(user_input):
    if "list stall" in user_input.lower() or "daftar stall" in user_input.lower():
        return "list_stalls"
    elif "kantin" in user_input.lower():
        return "kantin"
    elif "stall" in user_input.lower():
        stall_match = re.search(r"stall\s+(\w+)", user_input, re.IGNORECASE)
        if stall_match:
            return "stall", stall_match.group(1)  # Return stall name
    return "product_name"

# Main Program
st.title("Petranesian Lapar 🍕")
st.write("Data partial hanya tersedia untuk Gedung P dan W.")

# User Authentication
st.sidebar.title("User  Authentication")
auth_option = st.sidebar.selectbox("Choose an option", ["Login", "Register"])

if auth_option == "Register":
    username = st.sidebar.text_input("Username")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        message = register_user(username, email, password)
        st.sidebar.success(message)

elif auth_option == "Login":
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        message, username, email = login_user(email, password)
        if message == "Login successful.":
            st.session_state['username'] = username  # Store username in session state
            st.session_state['email'] = email  # Store email in session state
        st.sidebar.success(message)

# Proceed with chatbot only if user is logged in
if 'email' in st.session_state:
    st.title(f"Welcome, {st.session_state['username']}!")
    retriever = load_data()
    st.write("Jika ingin mencari stall ketik 'stall'")
    st.write("Jika ingin mencari makanan ketik langsung makanan yang ingin di cari")
    st.write("Jika ingin mencari harga ketik dibawah ..(harga)..")

    # Chat session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Halo! Lagi mau makan/minum apaan? 😉"}]

    if "chat_engine" not in st.session_state.keys():
        memory = ChatMemoryBuffer.from_defaults(token_limit=8192)
        st.session_state.chat_engine = CondensePlusContextChatEngine(
            verbose=True,
            system_prompt=system_prompt,
            memory=memory,
            retriever=retriever,
            llm=Settings.llm
        )

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display previous images if any
    if "previous_images" in st.session_state:
        num_columns = 3  # Number of columns in the grid
        columns = st.columns(num_columns)
        for i, item in enumerate(st.session_state.previous_images):
            col = columns[i % num_columns]  # Cycle through columns for each image
            with col:
                st.image(item["image_path"], width=250)
                st.markdown(f"**{item['product_name']}**")
                st.markdown(f"Harga: {item['harga']}")
                st.markdown(f"Stall: {item['stall']}")
                st.markdown(f"Kantin: {item['kantin']}")

    if prompt := st.chat_input(placeholder="Mau makan/minum apa?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Clean user input to ignore variations of "gambar"
        cleaned_prompt = clean_user_input(prompt)

        # Analyze user input to determine search type
        search_type = analyze_user_input(cleaned_prompt)

        match = re.search(r"(\d+)", cleaned_prompt)
        if match:
            max_price = float(match.group(1))
        else:
            max_price = None

        # Initialize filtered_results
        filtered_results = []

        # Perform search based on the determined search type
        if search_type == "list_stalls":
            all_stalls = get_all_stalls()
            stalls_message = "Daftar Stall:\n" + "\n".join(all_stalls)
            st.session_state.messages.append({"role": "assistant", "content": stalls_message})

            with st.chat_message("assistant"):
                st.markdown(stalls_message)
        elif search_type == "product_name":
            filtered_results = find_menu(cleaned_prompt, filter_price=max_price)
        elif isinstance(search_type, tuple) and search_type[0] == "stall":
            stall_name = search_type[1]
            # First, find items in the specified stall
            filtered_results = find_menu(cleaned_prompt, stall_name=stall_name)
            # Then, filter by price
            if max_price is not None:
                filtered_results = [item for item in filtered_results if item["harga_numerik"] is not None and item["harga_numerik"] <= max_price]
        elif search_type == "kantin":
            filtered_results = find_menu(cleaned_prompt, filter_price=max_price)  # Adjust this to search by kantin if needed

        # Only proceed if filtered_results is defined
        if filtered_results:
            response = get_gemini_response(cleaned_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)

            # Save the current images to session state for the next query
            st.session_state.previous_images = filtered_results

            num_columns = 3  # Number of columns in the grid
            columns = st.columns(num_columns)
            for i, item in enumerate(filtered_results):
                col = columns[i % num_columns]  # Cycle through columns for each image
                with col:
                    st.image(item["image_path"], width=250)
                    st.markdown(f"**{item['product_name']}**")
                    st.markdown(f"Harga: {item['harga']}")
                    st.markdown(f"Stall: {item['stall']}")
                    st.markdown(f"Kantin: {item['kantin']}")
else:
    st.sidebar.warning("Please log in to access the chatbot.")