# MagiClaude ✨

**The magic touch of Claude in your Jupyter Notebook.**

MagiClaude is a lightweight JupyterLab assistant that uses Claude to edit or generate notebook content from inline trigger blocks.

## Features 🚀

- Trigger syntax directly in notebook cells:
  - `@c ... @c` → edit the current cell
  - `@n ... @n` → notebook-level generation/editing
- Flexible routing modes:
  - local Claude CLI execution
  - remote broker execution
- Strict JSON operation mode:
  - `replace_cell`
  - `insert_cell_after`
- JupyterLab Settings UI support:
  - `claude_executable_path`
  - `jcm_mode`
  - `remote_broker_url`

## Project Layout 🧩

- `magiclaude/` — Jupyter server extension
- `labextension/` — JupyterLab frontend extension
- `magiclaude_broker/` — optional remote broker service

## Quick Start ⚙️

### 0) Install Claude Code CLI (prerequisite)

```bash
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
```

### 1) Get the source code

Clone this repository first:

```bash
git clone git@github.com:x1han/MagiClaude.git
cd MagiClaude
```

### 2) Install Python package

```bash
pip install -e .
```

### 3) Build frontend extension

```bash
cd labextension
npm install
npm run build
```

### 4) (Optional) Run remote broker

```bash
uvicorn magiclaude_broker.app:app --host 127.0.0.1 --port 1207
```

### 5) Start JupyterLab

```bash
jupyter lab
```

## Trigger Usage 🪄

In an active notebook cell:

```python
@c
Refactor this cell into small reusable functions and add type hints.
@c
```

or

```python
@n
Continue this notebook by adding data cleaning, training, and evaluation cells.
@n
```
