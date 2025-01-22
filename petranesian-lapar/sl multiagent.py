import os
import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.readers.file import CSVReader
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.retrievers import QueryFusionRetriever
import nest_asyncio
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

nest_asyncio.apply()

# Initialize node parser
splitter = SentenceSplitter(chunk_size=512)

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

@st.cache_resource(show_spinner="Mempersiapkan data kantin – sabar ya.")
def load_data():
    with st.spinner(text="Mempersiapkan data kantin – sabar ya."):
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

# Function to search and display images based on user input with 90% similarity
def find_image(user_input):
    image_folder = './images'  # Update with the correct folder path
    csv_file_path = './docs/menu-kantin.csv'
    
    # Load the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Initialize list to hold image paths and product names
    image_data = []

    # Check each entry in the 'Nama Produk' column
    for index, row in df.iterrows():
        product_name = row['Nama Produk']
        
        # Use fuzzywuzzy to compare similarity
        similarity = fuzz.partial_ratio(user_input.lower(), product_name.lower())
        
        if similarity >= 90:  # Check if similarity is at least 90%
            image_path = row['Gambar']
            if isinstance(image_path, str) and os.path.exists(image_path):
                image_data.append((image_path, product_name))
            elif isinstance(image_path, str):
                st.error(f"Image not found at {image_path}.")
    
    if image_data:
        return image_data
    return None

# Food Recommendation Agent
class FoodRecommendationAgent:
    def __init__(self):
        self.model_name = "t5-small"  # Valid Hugging Face model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def run(self, prompt, user_preferences=None):
        if user_preferences:
            prompt = f"Based on your preferences for {user_preferences}, what would you recommend to eat?"
        else:
            prompt = "What would you recommend to eat?"

        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        decoded_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_text.strip()

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
            st.image(image_data[0][0], caption=f"{image_data[0][1]}", use_column_width=True)

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
            for image_path, product_name in image_data:
                st.image(image_path, caption=f"{product_name}", use_column_width=True)
                message['image_data'] = image_data
    st.session_state.messages.append(message)
