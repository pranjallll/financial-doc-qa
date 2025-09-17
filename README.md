📊 Financial Document Q&A App
This project is a Streamlit-based application that allows users to upload financial documents (PDF, Excel, or text) and interactively ask questions about the content. The app uses LangChain and OpenAI embeddings to chunk, index, and query financial data in natural language.

🚀 Features
📂 Upload financial documents (PDF, Excel, or text).
🔍 Automatic text extraction and chunking.
💾 Vector-based storage with FAISS for fast retrieval.
🤖 Ask natural language questions about the uploaded document.
🎯 Provides meaningful insights from financial statements such as balance sheets, income statements, etc.

⚙️ Setup Instructions
1. Clone the repository
```bash git clone https://github.com/pranjallll/financial-doc-qa.git```
cd financial-doc-qa
2. Create a virtual environment

```bash python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows   
``` 
3. Install dependencies
```bash pip install -r requirements.txt```

4. Add your OpenAI API Key
```bash Create a .env file in the project root:
OPENAI_API_KEY=your_api_key_here
```

5. Run the app
``` bash streamlit run app.py ```

🖥️ Usage Instructions
1. Launch the app with streamlit run app.py.
2. Upload a financial document (PDF/Excel).
3. Type a question in the text box, e.g.:
"What is the total revenue for 2023?"
"How much are the current liabilities?"
"What is the net profit margin?"
The app will process the document and return an answer.

🎯 Success Criteria
✅ Users can upload a financial document.
✅ The system extracts and processes the data into chunks.
✅ Users can query the document with natural language questions.
✅ Answers are meaningful, relevant, and based on the uploaded file.
📌 Example Questions You Can Ask
"What are the total assets in the balance sheet?"
"How much cash is available?"
"What is the shareholder’s equity?"
"Compare current liabilities vs. long-term liabilities."

🛠️ Tech Stack
Python 3.10+
Streamlit for UI
LangChain for document processing
FAISS for vector storage
OpenAI Embeddings for semantic search

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.