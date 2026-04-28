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


offline 
pip install --no-index --find-links=offline_packages -r requirements.txt

STEP-BY-STEP INSTALL (OFFICE LAPTOP)
🔹 STEP 1: Copy files from phone

From your mentor’s phone → copy to laptop:

project.zip
models.zip
OllamaSetup.exe

👉 Paste them anywhere, e.g.:

Desktop/
🔹 STEP 2: Extract files

Right-click each:

project.zip → Extract All
models.zip → Extract All
📁 After extraction you should have:
Desktop/
├── project/
├── models/
├── OllamaSetup.exe
🔹 STEP 3: Install Ollama

Double click:

OllamaSetup.exe

Install normally.

🔹 STEP 4: Initialize Ollama (IMPORTANT)

Open Command Prompt:

ollama serve

👉 Wait 5–10 sec → then close it

This creates:

C:\Users\<your_user>\.ollama\
🔹 STEP 5: Paste model

Copy:

Desktop/models/

Paste into:

C:\Users\<your_user>\.ollama\
📁 Final should be:
C:\Users\<your_user>\.ollama\models
🔹 STEP 6: Verify model

Open terminal:

ollama list
✅ You should see:
gemma:2b
🔹 Test it:
ollama run gemma:2b

Type:

hello

👉 If it responds → PERFECT ✅

🔹 STEP 7: Install Python libraries (OFFLINE)

Go to your project folder:

cd Desktop\project

Run:

pip install --no-index --find-links=offline_packages -r requirements.txt
🔹 STEP 8: Run your project
Option 1 (easy):

Double click:

start.bat
Option 2 (manual):
ollama serve

Open new terminal:

cd Desktop\project
uvicorn app:app --host 127.0.0.1 --port 8000
🔹 STEP 9: Open UI

Browser:

http://127.0.0.1:8000
