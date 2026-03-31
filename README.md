# magiclaude ✨

**The magic touch of Claude in your Jupyter Notebook.**

magiclaude is a lightweight JupyterLab assistant that uses Claude to edit or generate notebook content from inline trigger blocks.

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

### 1) Install Python package

```bash
pip install -e .
```

### 2) Build frontend extension

```bash
cd labextension
npm install
npm run build
```

### 3) (Optional) Run remote broker

```bash
uvicorn magiclaude_broker.app:app --host 127.0.0.1 --port 1207
```

### 4) Start JupyterLab

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
