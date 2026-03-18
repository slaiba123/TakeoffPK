# ============================================================
# Unit Tests for VisaYaar Bot
# Run locally: pytest tests/ -v
# ============================================================

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if we are running in CI (GitHub Actions)
IN_CI = os.environ.get("CI") == "true"


# ── Test 1: Prompt exists and is valid ──────────────────────
def test_prompt_exists():
    from src.prompt import system_prompt
    assert system_prompt is not None
    assert len(system_prompt) > 100, "Prompt is too short"


def test_prompt_contains_countries():
    from src.prompt import system_prompt
    countries = ["USA", "UK", "Canada", "Germany", "Australia", "Turkey"]
    for country in countries:
        assert country in system_prompt, f"Prompt missing country: {country}"


def test_prompt_contains_disclaimer():
    from src.prompt import system_prompt
    assert "verify" in system_prompt.lower(), "Prompt should include verification disclaimer"


def test_prompt_contains_study_levels():
    from src.prompt import system_prompt
    levels = ["undergraduate", "postgraduate", "PhD"]
    for level in levels:
        assert level.lower() in system_prompt.lower(), f"Prompt missing study level: {level}"


# ── Test 2: Helper functions exist ──────────────────────────
def test_helper_functions_exist():
    from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
    assert callable(load_pdf_file)
    assert callable(text_split)
    assert callable(download_hugging_face_embeddings)


def test_text_split_works():
    from src.helper import text_split
    from langchain_core.documents import Document

    fake_docs = [
        Document(page_content="This is a test document about UK student visa requirements. " * 20),
        Document(page_content="Canada study permit requirements for Pakistani students. " * 20),
    ]
    chunks = text_split(fake_docs)
    assert len(chunks) > 0, "text_split should return chunks"
    assert len(chunks) >= 2, "Should create multiple chunks from long text"


def test_chunk_size():
    from src.helper import text_split
    from langchain_core.documents import Document

    long_doc = Document(page_content="word " * 1000)
    chunks = text_split([long_doc])
    for chunk in chunks:
        assert len(chunk.page_content) <= 600, "Chunks should not exceed max size"


# ── Test 3: Project structure ────────────────────────────────
def test_flask_app_creates():
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_check", "app.py")
    assert spec is not None, "app.py should exist"


def test_requirements_file_exists():
    assert os.path.exists("requirements.txt"), "requirements.txt must exist"


def test_dockerfile_exists():
    assert os.path.exists("Dockerfile"), "Dockerfile must exist"


def test_env_example_exists():
    assert os.path.exists(".env.example"), ".env.example must exist"


def test_env_example_has_required_keys():
    with open(".env.example", "r") as f:
        content = f.read()
    assert "PINECONE_API_KEY" in content
    assert "GROQ_API_KEY" in content
    assert "HUGGINGFACE_API_KEY" in content


# ── Test 4: Data folder — skip in CI (PDFs not on GitHub) ────
@pytest.mark.skipif(IN_CI, reason="Data/ folder with PDFs not available in CI environment")
def test_data_folder_exists():
    assert os.path.exists("Data"), "Data/ folder must exist"


@pytest.mark.skipif(IN_CI, reason="Data/ folder with PDFs not available in CI environment")
def test_country_folders_exist():
    countries = ["usa", "uk", "canada", "germany", "australia", "turkey", "saudi_arabia"]
    for country in countries:
        path = os.path.join("Data", country)
        assert os.path.exists(path), f"Data/{country}/ folder must exist"


@pytest.mark.skipif(IN_CI, reason="Data/ folder with PDFs not available in CI environment")
def test_pdfs_exist_in_data():
    import glob
    pdfs = glob.glob("Data/**/*.pdf", recursive=True)
    assert len(pdfs) > 0, "At least one PDF must exist in Data/ folder"
    print(f"\n   Found {len(pdfs)} PDFs in Data/")