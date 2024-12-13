# DocuGenie 📚✨

DocuGenie is an intelligent document processing and querying system that allows users to interact with their documents through natural language conversations. It combines advanced document processing with AI-powered querying capabilities to make document interaction more intuitive and efficient.

## Features 🚀

- **Document Processing**
  - PDF document upload and processing
  - Multiple document format support 
  (PDF, DOCX, Markdown, CSV, Excel, PPTX, Url)
  - Automatic document sectioning
  - Text extraction and analysis
  - Document status tracking

- **Intelligent Querying**
  - Natural language queries
  - Context-aware responses
  - GPT-powered document analysis
  - Semantic search capabilities

- **Chat Interface**
  - Persistent chat history
  - Interactive document exploration
  - Context retention across conversations
  - User session management

## Technology Stack 💻

- **Backend Framework**: FastAPI
- **Database**: PgVector (PostgreSQL)
- **Frontend**: React.js, Tailwind CSS

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/imontdev25/docugenie.git
cd docugenie/backend
```

2. Set up virtual environment:
```bash
poetry shell
```

3. Install dependencies:
```bash
poetry install --only-main
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation 📖

### Document Management

```bash
POST /api/v1/documents/upload
GET /api/v1/documents/{doc_uuid}/status
GET /api/v1/documents/{doc_uuid}/sections
```

### Query and Chat

```bash
POST /api/v1/query
GET /api/v1/documents/{doc_uuid}/chat-history
DELETE /api/v1/documents/{doc_uuid}/chat-history
```

## Environment Variables 🔑

```env
# nessary env variables
POSTGRES_URI
LOGFIRE_TOKEN
LOGFIRE_PROJECT
AZURE_API_KEY
AZURE_API_VERSION
AZURE_ENDPOINT
GEMINI_API_KEY
```

## Frontend 🖥️

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Environment variables:
```bash
API_URL=http://localhost:8000
```

3. Run the frontend:
```bash
npm run dev
```

## Deployment 🚀

### Docker

1. Build the Docker image:
```bash
docker build -t docugenie .
```

2. Run the Docker container:
```bash
docker run -d -p 8000:8000 docugenie
```


## Usage Examples 💡

### Upload Document
```python
import requests

files = {'file': open('document.pdf', 'rb')}
response = requests.post('http://localhost:8000/api/v1/documents/upload', files=files)
doc_uuid = response.json()['doc_uuid']
```

### Query Document
```python
query_data = {
    "query": "What are the main points discussed?",
    "doc_uuid": doc_uuid
}
response = requests.post('http://localhost:8000/api/v1/query', json=query_data)
```

## Development 🔧


### Code Style
```bash
# Format code
ruff check app/ --unsafe-fixes --fix

```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Project Structure 📁

```
docugenie/
├── frontend/
├── backend/
└── README.md
```


## Roadmap 🗺️

- [ ] Multi-document comparison
- [ ] API rate limiting
- [ ] Batch processing
- [ ] Export functionality
- [ ] Chat history fix

## License 📄

This project is licensed under the License - see the [LICENSE](LICENSE) file for details.

---


_Made with ❤️ by Bhavik_
