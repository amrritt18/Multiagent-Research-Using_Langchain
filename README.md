# Multi-Agent Research Assistant Using LangChain

An AI-powered research assistant that automates web research using a multi-agent workflow. It searches for relevant information, extracts webpage content, generates a structured research report, and evaluates the report using an AI critic.

## Features

- **Web Search:** Retrieves relevant sources using Tavily Search.
- **Web Content Extraction:** Extracts useful information from webpages using Trafilatura and BeautifulSoup.
- **Research Report Generation:** Generates structured reports using a Groq-hosted language model.
- **Report Evaluation:** Reviews the generated report and provides feedback on its quality.
- **Interactive UI:** Provides a Streamlit interface for submitting research topics and viewing results.
- **Download Reports:** Exports the research report, critic feedback, or complete research results in Markdown format.

## Workflow

1. **Search Agent** — searches the web for relevant sources.
2. **Reader Agent** — extracts and summarizes information from selected webpages.
3. **Writer Chain** — generates a structured research report.
4. **Critic Chain** — evaluates the report and suggests improvements.

## Tech Stack

- Python
- LangChain
- Groq LLM
- Tavily Search API
- Requests
- BeautifulSoup
- Trafilatura
- Readability
- Streamlit
- uv

## Project Structure

```text
Multiagent-Research-Using_Langchain/
├── src/
│   ├── agents/
│   │   └── agents.py
│   ├── tools/
│   │   └── tools.py
│   └── pipeline/
│       └── pipeline.py
├── app.py
├── main.py
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Multiagent-Research-Using_Langchain
```

### 2. Install dependencies

Install [uv](https://docs.astral.sh/uv/) if it is not already installed.

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholders with your own API keys.

## Usage

### Run the Streamlit application

```bash
uv run streamlit run app.py
```

Open the local URL displayed in your terminal, enter a research topic, and click **Start Research**.

### Run from the terminal

```bash
uv run python main.py
```

## Example Research Topics

- Recent applications of multi-agent AI systems
- Applications of artificial intelligence in healthcare
- Recent developments in autonomous robotics
- AI agents for automated software development

## Future Improvements

- Add source verification and stronger evidence grounding.
- Implement iterative report refinement based on critic feedback.
- Display real-time progress for each pipeline stage.
- Add research quality metrics and evaluation benchmarks.
- Support exporting reports in PDF format.

## Security

- Keep API keys in your local `.env` file.
- Never commit `.env` or other files containing secrets to GitHub.
- Use a `.gitignore` file to exclude sensitive files and local environments.

## License

This project is intended for educational and research purposes.
