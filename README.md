# TakeoffPK — AI Student Visa Guide for Pakistanis

An AI-powered study abroad assistant helping Pakistani students navigate visa requirements for undergraduate, postgraduate and PhD programs across 7 top countries.

## 🌍 Countries Covered
| # | Country | Visa Types |
|---|---------|-----------|
| 1 | 🇺🇸 USA | F-1 Student Visa (UG, Masters, PhD) |
| 2 | 🇬🇧 UK | Student Visa (UG, PG, PhD) |
| 3 | 🇨🇦 Canada | Study Permit (UG, Masters, PhD) |
| 4 | 🇩🇪 Germany | Student Visa, EU Blue Card, PhD Visa |
| 5 | 🇦🇺 Australia | Student Visa Subclass 500 |
| 6 | 🇹🇷 Turkey | Student Visa, Türkiye Scholarships |

---

## 🛠️ Tech Stack
- **LLM**: Groq (free) — llama-3.3-70b-versatile
- **Embeddings**: HuggingFace Inference API (free)
- **Vector DB**: Pinecone (free starter)
- **Backend**: Flask
- **Deployment**: AWS EC2 t2.micro (free tier) + ECR + GitHub Actions CI/CD

---

## 📁 Project Structure
```
visabot/
├── src/
│   ├── __init__.py
│   ├── helper.py
│   └── prompt.py
├── Data/
│   ├── usa/             ← 4 PDFs
│   ├── uk/              ← 3 PDFs
│   ├── canada/          ← 2 PDFs
│   ├── germany/         ← 4 PDFs
│   ├── australia/       ← 3 PDFs
│   ├── turkey/          ← 3 PDFs
│  
├── templates/
│   └── chat.html
├── app.py
├── store_index.py
├── requirements.txt
├── setup.py
├── Dockerfile
├── .env.example
├── .gitignore
└── .github/
    └── workflows/
        └── main.yaml
```

---

## 📄 PDF Sources

| Country | Official Source |
|---------|----------------|
| 🇺🇸 USA | travel.state.gov, pk.usembassy.gov |
| 🇬🇧 UK | assets.publishing.service.gov.uk |
| 🇨🇦 Canada | ircc.canada.ca |
| 🇩🇪 Germany | germany.info, daad.de |
| 🇦🇺 Australia | immi.homeaffairs.gov.au |
| 🇹🇷 Turkey | islamabad-emb.mfa.gov.tr |

---

## 🚀 How to Run Locally

### Step 1 — Clone the repo
```bash
git clone <your-repo-url>
cd visabot
```

### Step 2 — Create conda environment
```bash
conda create -n TakeoffPK python=3.10 -y
conda activate TakeoffPK
```

### Step 3 — Install requirements
```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env` file
```ini
PINECONE_API_KEY=your_pinecone_key
GROQ_API_KEY=your_groq_key
HUGGINGFACE_API_KEY=your_huggingface_token
```

Get free keys from:
- Pinecone   : https://pinecone.io       (free, no credit card)
- Groq       : https://groq.com          (free, no credit card)
- HuggingFace: https://huggingface.co → Settings → Access Tokens (free)

### Step 5 — Add PDFs to country folders
Download official PDFs and place them in the correct `Data/` subfolder.

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

## ☁️ AWS Deployment (Free Tier — t2.micro)

### Prerequisites
- AWS account (free tier)
- GitHub account
- Docker installed locally

### Step 1 — Create IAM user
Attach these policies:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

Save `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

### Step 2 — Create ECR repository
```
AWS Console → ECR → Create Repository → name: visayaar
Save URI: <account_id>.dkr.ecr.us-east-1.amazonaws.com/TakeoffPK
```

### Step 3 — Launch EC2 instance
- Type: **t2.micro** (free tier eligible)
- OS: Ubuntu 22.04
- Open inbound port **8080** in Security Group

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
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION                 = us-east-1
AWS_ECR_LOGIN_URI          = <account_id>.dkr.ecr.us-east-1.amazonaws.com
ECR_REPOSITORY_NAME        = visayaar
PINECONE_API_KEY
GROQ_API_KEY
HUGGINGFACE_API_KEY
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

App live at: `http://<EC2-public-ip>:8080`

---

## ⚠️ Important
```
# Add to .gitignore — never commit these!
.env
Data/
```

Data/ folder should never be pushed to GitHub as it contains PDFs.
Always verify visa information with official embassies before applying.