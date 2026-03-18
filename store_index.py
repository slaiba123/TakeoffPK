# from src.helper import load_pdf_file, text_split
# from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
# from pinecone.grpc import PineconeGRPC as Pinecone
# from pinecone import ServerlessSpec
# from langchain_pinecone import PineconeVectorStore
# from dotenv import load_dotenv
# import os

# load_dotenv()

# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# # Use HuggingFace Inference API instead of loading model locally (saves ~800MB RAM)
# embeddings = HuggingFaceInferenceAPIEmbeddings(
#     api_key=HUGGINGFACE_API_KEY,
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# extracted_data = load_pdf_file(data='Data/')
# text_chunks = text_split(extracted_data)

# pc = Pinecone(api_key=PINECONE_API_KEY)

# index_name = "medicalbot"

# # Create index only if it doesn't exist
# existing_indexes = [i.name for i in pc.list_indexes()]
# if index_name not in existing_indexes:
#     pc.create_index(
#         name=index_name,
#         dimension=384,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1"
#         )
#     )

# # Embed and upsert into Pinecone
# docsearch = PineconeVectorStore.from_documents(
#     documents=text_chunks,
#     index_name=index_name,
#     embedding=embeddings,
# )

# print("✅ Pinecone index created and embeddings stored successfully!")

from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["HUGGINGFACE_API_KEY"] = HUGGINGFACE_API_KEY

extracted_data = load_pdf_file(data='Data/')
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"

# Create index only if it doesn't already exist
existing_indexes = [i.name for i in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"✅ Created new Pinecone index: {index_name}")
else:
    print(f"ℹ️  Index '{index_name}' already exists, skipping creation.")

# Embed each chunk and upsert into Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)

print("✅ Embeddings stored in Pinecone successfully!")