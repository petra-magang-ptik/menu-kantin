import os
import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, Document
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.retrievers import QueryFusionRetriever
import nest_asyncio
import mysql.connector
from decimal import Decimal  # Import Decimal for type checking

# Apply nest_asyncio for async compatibility
nest_asyncio.apply()

# Initialize node parser
splitter = SentenceSplitter(chunk_size=512)

# Configure logging
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# System prompt for the assistant
system_prompt = """
Anda adalah pelayan kantin yang ramah yang dapat mengarahkan pengguna mencari makanan/minuman yang tepat.
Anda tidak perlu menyebutkan atau membuat pernyataan yang mengatakan Anda tidak dapat menampilkan gambar jika gambar berhasil ditemukan.
Jawablah semua dalam Bahasa Indonesia.
Tugas Anda adalah untuk menjadi pelayan kantin yang ramah yang dapat mengarahkan user.
Kantin yang Anda layani adalah kantin kampus Universitas Kristen Petra Surabaya.
"""

Settings.llm = Ollama(model="llama3.1:latest", base_url="http://127.0.0.1:11434", system_prompt=system_prompt)
Settings.embed_model = OllamaEmbedding(base_url="http://127.0.0.1:11434", model_name="mxbai-embed-large:latest")

# Function to fetch data from MySQL database
def fetch_data_from_db():
    conn = mysql.connector.connect(
        host='sql12.freesqldatabase.com',
        user='sql12765612',
        password='9KwSC9nIKL',
        database='sql12765612'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kantin")  # Replace with your table name
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Function to convert Decimal to float for JSON serialization
def convert_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(v) for v in obj]
    return obj

@st.cache_resource(show_spinner="Mempersiapkan data kantin – sabar ya.")
def load_data():
    with st.spinner(text="Mempersiapkan data kantin – sabar ya."):
        rows = fetch_data_from_db()
        
        # Convert rows to Document objects
        documents = []
        for row in rows:
            # Convert Decimal fields to float for JSON serialization
            row = convert_decimals(row)
            
            doc_text = (
                f"Gedung: {row['Gedung']}, "
                f"Stall: {row['Nama_Stall']}, "
                f"Menu: {row['Nama_Produk']}, "
                f"Harga: {row['Harga']}, "
                f"Keterangan: {row['Keterangan_Tambahan']}, "
                f"Kategori: {row['Kategori']}"
            )
            # Create a Document object with the text and metadata
            doc = Document(
                text=doc_text,
                metadata={
                    "Gedung": row["Gedung"],
                    "Nama_Stall": row["Nama_Stall"],
                    "Nama_Produk": row["Nama_Produk"],
                    "Harga": row["Harga"],
                    "Keterangan_Tambahan": row["Keterangan_Tambahan"],
                    "Kategori": row["Kategori"],
                    "Gambar": row["Gambar"]  # Ensure this matches the column name in your database
                }
            )
            documents.append(doc)

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

# Function to search and display images based on user input with 75% similarity
def find_image(user_input):
    # Fetch data from the database
    rows = fetch_data_from_db()
    
    # Initialize list to hold image paths and product names
    image_data = []

    # Check each entry in the rows
    for row in rows:
        product_name = row['Nama_Produk']
        
        # Use fuzzywuzzy to compare similarity
        similarity = fuzz.partial_ratio(user_input.lower(), product_name.lower())
        
        if similarity >= 75:  # Check if similarity is at least 75%
            image_path = row['Gambar']
            # Ensure the image path is valid
            if isinstance(image_path, str):
                # Convert relative path to absolute path if necessary
                if not os.path.isabs(image_path):
                    image_path = os.path.join(os.getcwd(), image_path)
                if os.path.exists(image_path):
                    image_data.append((image_path, product_name))
                else:
                    st.warning(f"Image path does not exist: {image_path}")
            else:
                st.warning(f"Invalid image path type: {type(image_path)}")
    
    return image_data if image_data else None

# Main Program
st.title("Petranesian Lapar 🍕")
st.write("Data partial hanya tersedia untuk Gedung P dan W.")
retriever = load_data()

# Initialize chat history if empty
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Lagi mau makan/minum apaan? 😉"}
    ]

# Initialize the chat engine
if "chat_engine" not in st.session_state.keys():
    init_history = [
        ChatMessage(role=MessageRole.ASSISTANT, content="Halo! Lagi mau makan/minum apaan? 😉"),
    ]
    memory = ChatMemoryBuffer.from_defaults(token_limit=16384)
    st.session_state.chat_engine = CondensePlusContextChatEngine(
        verbose=True,
        system_prompt=system_prompt,
        context_prompt=( 
            "Anda adalah pelayan kantin yang ramah yang dapat mengarahkan user ketika mencari makanan dan stall kantin.\n"
            "Format dokumen pendukung: gedung letak kantin, nama stall, nama produk, harga, keterangan\n"
            "Ini adalah dokumen yang mungkin relevan terhadap konteks:\n\n"
            "{context_str}\n\n"
            "Instruksi: Gunakan riwayat obrolan sebelumnya, atau konteks di atas, untuk berinteraksi dan membantu pengguna."
        ),
        condense_prompt=""" 
Diberikan suatu percakapan (antara User dan Assistant) dan pesan lanjutan dari User,
Ubah pesan lanjutan menjadi pertanyaan independen yang mencakup semua konteks relevan dari percakapan sebelumnya.
""",
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
            for img_path, product_name in image_data:
                # Display the image using st.image
                st.image(img_path, caption=f"{product_name}", use_container_width=True)

# User input
if prompt := st.chat_input(placeholder="Mau makan/minum apa?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.chat_engine.chat(prompt)
    message = {"role": "assistant", "content": response}

    with st.chat_message("assistant"):
        st.markdown(response)
       
        # Attempt to find and display images for the user's input
        image_data = find_image(prompt)
        if image_data:
            message['image_data'] = image_data  # Store image data in the message
            for img_path, product_name in image_data:
                # Display the image using st.image
                st.image(img_path, caption=f"{product_name}", use_container_width=True)
        else:
            st.markdown("Tidak ada gambar yang ditemukan untuk menu tersebut. Silakan memilih menu lainnya.")
    st.session_state.messages.append(message)