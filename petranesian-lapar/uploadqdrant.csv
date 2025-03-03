import pandas as pd
import qdrant_client
from qdrant_client.http.models import VectorParams

# Initialize Qdrant Client
QDRANT_URL = "https://a3040b4c-5492-488b-8b86-be3eae1626c1.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "u3TZLQzlOMlx4a1w63jUkj2hC_xNLfv3gu2v-jNxunPQlaB56eZMDA"
collection_name = "kantin_menu"

qdrant_client = qdrant_client.QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Ensure collection exists
def ensure_collection():
    collections = qdrant_client.get_collections()
    if collection_name not in [col.name for col in collections.collections]:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance="Cosine")
        )
        print(f"Collection '{collection_name}' created successfully.")

ensure_collection()

# Function to upload data from CSV to Qdrant
def upload_data_from_csv(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Prepare data for Qdrant
    points = []
    for index, row in df.iterrows():
        point = {
            "id": index,  # Use index as ID
            "payload": {
                "kantin": row["Kantin"],
                "stall": row["Nama Stall"],
                "product_name": row["Nama Produk"],
                "harga": row["Harga"],
                "keterangan": row["Keterangan Tambahan"],
                "image_path": row["Gambar"],
                "kategori": row["Kategori"]
            },
            "vector": [0] * 768  # Placeholder for vector, replace with actual embedding if available
        }
        points.append(point)

    # Upload points to Qdrant
    qdrant_client.upsert(collection_name=collection_name, points=points)
    print(f"Uploaded {len(points)} points to Qdrant collection '{collection_name}'.")

if __name__ == "__main__":
    # Specify the path to your CSV file
    csv_file_path = "./docs/menu-kantin.csv"
    upload_data_from_csv(csv_file_path)
