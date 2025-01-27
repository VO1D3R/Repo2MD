# Repo2MD 📂→📄

Convert GitHub repositories, Hugging Face spaces, or local directories into structured Markdown files for LLM analysis.

## Features

- 🌳 Visual file tree generation
- 🔗 Supports both remote (GitHub/HF) and local repositories
- 📄 Preserves code structure with syntax highlighting
- 🚫 Auto-excludes `.git` directories
- ⚡ Handles large files (skips >1MB files)
- 📦 Lightweight with no external dependencies

## Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/Repo2MD.git
cd Repo2MD
```

2. Ensure you have:
- Python 3.6+
- Git installed (for repository cloning)

## Usage

### For remote repositories:
```bash
python repo_to_md.py https://github.com/username/repo output.md
```

### For local directories:
```bash
python repo_to_md.py ./path/to/directory output.md
```

### Example Output Structure:
```markdown
# Repository Structure


project/
├── src/
│   ├── __init__.py
│   └── main.py
└── README.md


## File: src/main.py

```python
def main():
    print("Hello World!")
```

...

## Configuration

Modify these values in the code:
- `max_size` (default 1MB) - Change file size limit
- File extensions - Add new languages in `get_language()`

## Limitations

- ❗ Binary files are skipped
- 📁 Nested git repos not handled
- 🔒 Permission-restricted files skipped
- 🌐 Only common text formats supported

## Contributing

Contributions welcome! Please:
1. Open an issue to discuss changes
2. Fork the repository
3. Create a feature branch
4. Submit a PR
