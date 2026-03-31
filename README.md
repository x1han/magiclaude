# magiclaude

The magic touch of Claude in your Jupyter Notebook.

magiclaude 是一个轻量的 JupyterLab 智能助手扩展，通过 `@c ... @c` 或 `@n ... @n` 指令块触发 Claude，自动改写当前单元格或在下方生成多个单元格。

## Features

- Block trigger syntax in notebook cells:
  - `@c ... @c`: edit current cell
  - `@n ... @n`: notebook-level edit and generation
- Local/remote routing:
  - local node Claude CLI
  - remote mgt broker via tunnel
- Strict JSON patch mode:
  - `replace_cell`
  - `insert_cell_after`
- Settings UI in JupyterLab:
  - `claude_executable_path`
  - `jcm_mode`
  - `remote_broker_url`

## Project Layout

- `magiclaude/` — Jupyter server extension
- `labextension/` — JupyterLab frontend extension
- `magiclaude_broker/` — remote broker service

## Quick Start

### 1) Install Python package

```bash
pip install -e .
```

### 2) Build frontend

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

## n10 -> mgt tunnel

On n10:

```bash
ssh -N -L 1207:127.0.0.1:1207 <user>@<mgt-host>
```

Then set `remote_broker_url` to `http://127.0.0.1:1207`.

## Trigger Usage

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
