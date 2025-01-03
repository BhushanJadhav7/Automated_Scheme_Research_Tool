# Automated_Scheme_Research_Tool
A Streamlit-based web app to fetch, process, and summarize government scheme information. Users can input URLs, generate concise summaries, and interact through queries.

## Features

- **Web Content Extraction:** Fetches content from URLs entered by the user.
- **Text Preprocessing:** Splits large text into token-safe chunks (up to 3000 tokens) for OpenAI API compatibility.
- **Semantic Search:** Uses FAISS for efficient similarity searches over the indexed documents.
- **Question Answering:** Queries relevant content using the OpenAI API to retrieve accurate answers to user queries.
- **User-Friendly Interface:** A simple and intuitive Streamlit UI for easy interaction.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/automated-scheme-research-tool.git
   cd automated-scheme-research-tool
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add OpenAI API Key:**
   Create a `.config` file in the root directory and paste your OpenAI API key:
   ```
   YOUR_OPENAI_API_KEY
   ```

4. **Run the Application:**
   ```bash
   streamlit run main.py
   ```

## Usage

1. **Input URLs:**
   Enter the URLs of web pages containing scheme-related information into the text area in the sidebar.
   
2. **Process Content:**
   Click the "Process URLs" button to fetch and index the content.

3. **Ask Questions:**
   Use the query input to ask questions related to the schemes. The tool will provide answers based on the indexed data.

4. **View Results:**
   See the answer and the relevant content extracted from the web pages.

## Technology Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Web Scraping:** [langchain.document_loaders](https://python.langchain.com/)
- **Text Processing:** Recursive text splitting for OpenAI API compatibility.
- **Semantic Search:** [FAISS](https://github.com/facebookresearch/faiss)
- **Natural Language Processing:** OpenAI's GPT models via their API.

## Limitations

- The free-tier OpenAI API limits the number of tokens and requests.
- Requires properly structured URLs to retrieve meaningful content.
- Performance depends on the quality of web page content and API responses.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss proposed changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the interactive UI.
- [FAISS](https://github.com/facebookresearch/faiss) for semantic search.
- [OpenAI](https://openai.com/) for language processing capabilities.
- [LangChain](https://python.langchain.com/) for content loading and embeddings.

## Demo Link

You can view the live demo of the app here:

[App Demo](https://automated-scheme-research-tool.streamlit.app/)
