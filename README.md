# End-to-end Medical Chatbot — Generative AI

## Tech Stack
- **LLM**: Groq (free) — llama3-8b-8192
- **Embeddings**: HuggingFace Inference API (free) — all-MiniLM-L6-v2
- **Vector DB**: Pinecone (free starter)
- **Backend**: Flask
- **Deployment**: AWS EC2 t2.micro (free tier) + ECR + GitHub Actions CI/CD

---

## Project Structure
```
medicalbot/
├── src/
│   ├── __init__.py
│   ├── helper.py
│   └── prompt.py
├── Data/               ← put your PDF files here (not committed to GitHub)
├── templates/
│   └── chat.html
├── app.py
├── store_index.py
├── requirements.txt
├── setup.py
├── Dockerfile
├── .env                ← create this locally, never commit to GitHub
└── .github/
    └── workflows/
        └── main.yaml
```

---

## How to Run Locally

### Step 1 — Clone the repo
```bash
git clone <your-repo-url>
cd <project-folder>
```

### Step 2 — Create conda environment
```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

### Step 3 — Install requirements
```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env` file in root directory
```ini
PINECONE_API_KEY=your_pinecone_key
GROQ_API_KEY=your_groq_key
HUGGINGFACE_API_KEY=your_huggingface_token
```

Get free keys from:
- Pinecone  : https://pinecone.io       (free starter, no credit card)
- Groq      : https://groq.com          (free tier, no credit card)
- HuggingFace: https://huggingface.co → Settings → Access Tokens (free)

### Step 5 — Add your PDF files
```
Place your PDF files inside the Data/ folder
```

### Step 6 — Store embeddings in Pinecone (run once only)
```bash
python store_index.py
```

### Step 7 — Run the app
```bash
python app.py
```
Open: http://localhost:8080

---

## AWS Deployment (Free Tier — t2.micro)

### Prerequisites
- AWS account (free tier)
- GitHub account
- Docker installed locally (for testing)

### Step 1 — Create IAM user in AWS Console
Attach these policies:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

Save the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

### Step 2 — Create ECR repository
```
AWS Console → ECR → Create Repository → name: medicalbot
Save the URI: <account_id>.dkr.ecr.us-east-1.amazonaws.com/medicalbot
```

### Step 3 — Launch EC2 instance
- Type: t2.micro (free tier eligible)
- OS: Ubuntu 22.04
- Open inbound port 8080 in Security Group

### Step 4 — Install Docker on EC2
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

### Step 5 — Configure EC2 as GitHub self-hosted runner
```
GitHub repo → Settings → Actions → Runners → New self-hosted runner → Linux
Run the commands shown one by one on your EC2 instance
```

### Step 6 — Add GitHub Secrets
```
Go to: GitHub repo → Settings → Secrets and variables → Actions → New secret

Add these 8 secrets:
AWS_ACCESS_KEY_ID          ← from IAM user
AWS_SECRET_ACCESS_KEY      ← from IAM user
AWS_REGION                 = us-east-1
AWS_ECR_LOGIN_URI          = <account_id>.dkr.ecr.us-east-1.amazonaws.com
ECR_REPOSITORY_NAME        = medicalbot
PINECONE_API_KEY           ← from pinecone.io
GROQ_API_KEY               ← from groq.com
HUGGINGFACE_API_KEY        ← from huggingface.co
```

### Step 7 — Push to GitHub
```bash
git add .
git commit -m "initial commit"
git push origin main
```
GitHub Actions will automatically:
1. Build Docker image
2. Push to ECR
3. Pull on EC2
4. Run the container

Your app will be live at: `http://<EC2-public-ip>:8080`

---

## Important — Add to .gitignore
```
.env
Data/
__pycache__/
*.pyc
.pytest_cache/
```