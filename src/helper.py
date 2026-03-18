from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import glob as glob_module
import os


# Extract Data From PDF Files in all country subdirectories
def load_pdf_file(data):
    all_documents = []
    # Manually find all PDFs recursively (fixes Windows glob issue)
    pdf_files = glob_module.glob(os.path.join(data, "**", "*.pdf"), recursive=True)
    print(f"📄 Found {len(pdf_files)} PDF files")
    for pdf_path in pdf_files:
        print(f"   Loading: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        all_documents.extend(loader.load())
    return all_documents


# Split the Data into Text Chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


# Get HuggingFace Inference API Embeddings (no local model download)
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",  # returns 384 dimensions
        huggingfacehub_api_token=os.environ.get('HUGGINGFACE_API_KEY')
    )
    return embeddings