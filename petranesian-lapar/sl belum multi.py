import os
from fuzzywuzzy import process
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
import nest_asyncio
nest_asyncio.apply()

# initialize node parser
splitter = SentenceSplitter(chunk_size=512)

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# System prompt for the assistant
system_prompt = """
Anda adalah pelayan kantin yang ramah yang dapat mengarahkan pengguna mencari makanan/minuman yang tepat.
Anda tidak perlu menyebutkan atau membuat pernyataan yang mengatakan Anda tidak dapat menampilkan gambar jika gambar berhasil ditemukan.
Tugas Anda adalah untuk menjawab dengan relevansi sesuai menu dan menyarankan gambar jika sesuai.
Jawablah semua dalam Bahasa Indonesia.
Tugas Anda adalah untuk menjadi pelayan kantin yang ramah yang dapat mengarahkan user.
Kantin yang Anda layani adalah kantin kampus Universitas Kristen Petra Surabaya.
Pada Universitas Kristen Petra terdapat 2 gedung utama yang setiap gedungnya memiliki kantin,
yaitu Gedung P dan W.
"""

Settings.llm = Ollama(model="llama3.1:latest", base_url="http://127.0.0.1:11434", system_prompt=system_prompt)
Settings.embed_model = OllamaEmbedding(base_url="http://127.0.0.1:11434", model_name="mxbai-embed-large:latest")


@st.cache_resource(show_spinner="Mempersiapkan data kantin – sabar ya.")
def load_data(vector_store=None):
    with st.spinner(text="Mempersiapkan data kantin – sabar ya."):
        csv_parser = CSVReader(concat_rows=False)
        file_extractor = {".csv": csv_parser}

        # Read & load document from folder
        reader = SimpleDirectoryReader(
            input_dir="./docs",
            recursive=True,
            file_extractor=file_extractor,

            # Suppress file metadata, not sure if this works or not.
            file_metadata=lambda x: {}
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


# Function to search and display images based on user input
def find_image(user_input):
    image_folder = './images'  # Update with the correct folder path
    all_images = os.listdir(image_folder)
    # Fuzzy search for matching images based on user input
    best_match, score = process.extractOne(user_input, all_images)
    if score > 50:  # You can adjust the threshold as needed
        return os.path.join(image_folder, best_match)
    return None


# Main Program
st.title("Petranesian Lapar 🍕")
st.write("Data partial hanya tersedia untuk Gedung P dan W.")
retriever = load_data()

# Initialize chat history if empty
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Halo! Lagi mau makan/minum apaan? 😉"}
    ]

# Initialize the chat engine
if "chat_engine" not in st.session_state.keys():
    # Initialize with custom chat history
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
                "{context_str}"
                "\n\nInstruksi: Gunakan riwayat obrolan sebelumnya, atau konteks di atas, untuk berinteraksi dan membantu pengguna. Hanya jawab dengan kantin/menu yang sesuai. Jika tidak menemukan makanan atau minuman yang sesuai, maka katakan bahwa tidak menemukan."
            ),
        condense_prompt=""" 
Diberikan suatu percakapan (antara User dan Assistant) dan pesan lanjutan dari User,
Ubah pesan lanjutan menjadi pertanyaan independen yang mencakup semua konteks relevan
dari percakapan sebelumnya. Pertanyaan independen/standalone question cukup 1 kalimat saja. Informasi yang penting adalah makanan/minuman yang dicari, nama stall, dan letak gedung. Contoh standalone question: "Saya mencari jus jambu di Gedung P".

<Chat History>
{chat_history}

<Follow Up Message>
{question}

<Standalone question>""",
        memory=memory,
        retriever=retriever,
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

    with st.chat_message("assistant"):
        with st.spinner("Berpikir..."):
            response_stream = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response_stream.response_gen)

        # Only search for an image if the user explicitly asks for it
        if "gambar" in prompt.lower():
            image_path = find_image(prompt)
            if image_path:
                st.image(image_path, caption=f"Image for '{prompt}'", use_column_width=True)
            else:
                st.write("Tidak ada gambar yang ditemukan.")
        
        # Add the assistant's response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response_stream.response})
