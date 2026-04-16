# 1. Install Ollama from https://ollama.com → then pull a model
ollama pull mistral

# 2. Python packages
pip install fastapi uvicorn pandas openpyxl chromadb sentence-transformers


mtdr-assistant/
├── clean_excel.py
├── app.py
├── index.html
└── start.bat

first time setup run once 
# 1. Install Ollama from https://ollama.com, then:
ollama pull mistral

# 2. Install Python dependencies:
pip install fastapi uvicorn pandas openpyxl chromadb sentence-transformers httpx

# 3. Clean and index your Excel:
python clean_excel.py --file "Your MTDR Records.xlsx"
