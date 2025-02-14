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

# System prompt for the assistant
system_prompt = """
Anda adalah pelayan kantin yang ramah yang dapat mengarahkan pengguna mencari makanan/minuman yang tepat.
Jawablah semua dalam Bahasa Indonesia.
Kantin yang Anda layani adalah kantin kampus Universitas Kristen Petra Surabaya.
"""

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

# Store product images in Qdrant
def store_images_in_qdrant():
    csv_file_path = './docs/menu-kantin.csv'
    if not os.path.exists(csv_file_path):
        print("CSV file not found!")
        return
    
    df = pd.read_csv(csv_file_path)
    
    for index, row in df.iterrows():
        product_name = row['Nama Produk']
        image_path = row['Gambar']
        
        if isinstance(image_path, str) and os.path.exists(image_path):
            vector = embed_model.get_text_embedding(product_name)
            qdrant_client.upsert(
                collection_name=collection_name,
                points=[{
                    "id": index,
                    "vector": vector,
                    "payload": {
                        "product_name": product_name,
                        "image_path": image_path,
                        "kantin": row.get("Kantin", "Tidak diketahui"),
                        "stall": row.get("Nama Stall", "Tidak diketahui"),
                        "harga": row.get("Harga", "Tidak diketahui"),
                        "keterangan": row.get("Keterangan", "")
                    }
                }]
            )
store_images_in_qdrant()

# Function to search data in Qdrant (Hybrid Matching)
def find_menu(user_input, filter_price=None):
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

            if user_input.lower() in product_name.lower():
                filtered_results.append(item_data)
            else:
                menu_data.append(item_data)

    # Apply price filter if specified
    if filter_price is not None:
        menu_data = [item for item in menu_data if item["harga_numerik"] is not None and item["harga_numerik"] <= filter_price]

    return filtered_results if filtered_results else menu_data

# Main Program
st.title("Petranesian Lapar 🍕")
st.write("Data partial hanya tersedia untuk Gedung P dan W.")
retriever = load_data()

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
if message["role"] == "assistant" and "image_data" in message:
            image_data = message["image_data"]
            st.image(image_data[0][0], caption=f"{image_data[0][1]}", use_column_width=True)


if prompt := st.chat_input(placeholder="Mau makan/minum apa?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    match = re.search(r"(bawah|below)\s*(\d+)", prompt.lower())
    filter_price = int(match.group(2)) if match else None

    response = st.session_state.chat_engine.chat(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

        menu_data = find_menu(prompt, filter_price)
        for item in menu_data:
            st.write(f"**{item['product_name']}**")
            st.write(f"📍 Kantin: {item['kantin']} | 🏪 Stall: {item['stall']}")
            st.write(f"**{item['product_name']}** – 💰 {item['harga']}")
            st.image(item["image_path"], use_container_width=True)

