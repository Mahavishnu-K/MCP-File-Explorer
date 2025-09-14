# 🗂️ MCP File Explorer + AI Agent

An **AI-powered file system explorer** that runs in a **sandboxed environment**, giving an agent the ability to:

✅ List files and directories  
✅ Read file contents  
✅ Write or overwrite files  
✅ Delete files safely  

Built using **Python**, **OpenAI GPT**, and a **secure sandbox layer** to ensure the AI never escapes outside the project directory.

## ✨ Features

- 🔒 **Sandbox Security** – prevents path traversal (`../../`) attacks
- ⚡ **AI Agent Loop** – natural language commands drive file system interactions
- 📂 **File Management Tools** – `list_files`, `read_file`, `write_file`, and `delete_file`
- 🧪 **Unit Tests Included** – pytest suite ensures functionality & security

## 📂 Project Structure

```
.
├── examples/
│   └── run_real_agent.py       # Main entrypoint for running the agent
├── sandbox/                    # Sandboxed working directory
├── src/
│   ├── config.py              # Config & default sandbox path
│   ├── mcp_file_explorer.py   # Core file system wrapper
│   └── __init__.py
├── tests/
│   └── test_mcp_file_explorer.py  # Pytest tests for the explorer
├── .env                       # Store your API keys here
├── requirements.txt
├── README.md
└── venv/                      # Virtual environment
```

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/mcp-file-explorer.git
cd mcp-file-explorer
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in the project root:

```env
GITHUB_API_KEY=your_github_models_api_key
```

## 🧑‍💻 Usage

### Run the AI Agent:

```bash
python -m examples.run_real_agent
```

You'll see:

```
🤖 MCP Agent Initialized. Sandboxed to: sandbox
Type your commands below, or type 'exit' or 'quit' to end the session.
```

### Example Commands:

```
> create a file called hello.txt with content "Hello MCP!"
> read hello.txt
> delete hello.txt
> list files in .
```

## 🧪 Running Tests

```bash
pytest -v
```

## 🔮 Roadmap

- [ ] Add support for editing specific file sections
- [ ] Extend to JSON/YAML structured editing
- [ ] Optional read-only safety mode

## 🤝 Contributing

Contributions are welcome! Please open an issue or PR to discuss improvements.

## 📜 License

MIT License © 2025 [Your Name]

---

🚀 Built with Python + OpenAI GPT, secured with ❤️ for sandboxed AI experimentation.