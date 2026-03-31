import { NotebookPanel } from '@jupyterlab/notebook';
import { NotebookOp } from './types';

export function collectCells(panel: NotebookPanel): Array<{ cell_type: 'code' | 'markdown'; source: string }> {
  const out: Array<{ cell_type: 'code' | 'markdown'; source: string }> = [];
  const model = panel.content.model;
  if (!model) {
    return out;
  }

  for (let i = 0; i < model.cells.length; i++) {
    const c = model.cells.get(i);
    const cell_type = c.type === 'markdown' ? 'markdown' : 'code';
    out.push({ cell_type, source: c.sharedModel.getSource() });
  }
  return out;
}

export function applyOps(panel: NotebookPanel, ops: NotebookOp[]): void {
  const model = panel.content.model;
  if (!model) {
    throw new Error('Notebook model not available');
  }

  for (const op of ops) {
    if (op.type === 'replace_cell') {
      if (op.index < 0 || op.index >= model.cells.length) {
        throw new Error(`replace_cell index out of range: ${op.index}`);
      }
      const cell = model.cells.get(op.index);
      cell.sharedModel.setSource(op.source ?? '');
      if (op.cell_type && op.cell_type !== cell.type) {
        cell.type = op.cell_type;
      }
      continue;
    }

    if (op.type === 'insert_cell_after') {
      if (op.index < 0 || op.index >= model.cells.length) {
        throw new Error(`insert_cell_after index out of range: ${op.index}`);
      }
      const insertAt = op.index + 1;
      model.sharedModel.insertCell(insertAt, {
        cell_type: op.cell_type || 'code',
        source: op.source ?? ''
      } as any);
    }
  }
}
