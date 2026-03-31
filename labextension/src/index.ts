import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette, showErrorMessage } from '@jupyterlab/apputils';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { requestAPI } from './api';
import { applyOps, collectCells } from './ops';
import { parseMagic, NotebookOp } from './types';

interface ExecuteResponse {
  mode: 'local' | 'remote_mgt';
  summary: string;
  warnings: string[];
  ops: NotebookOp[];
}

interface PluginSettings {
  claude_executable_path: string;
  jcm_mode: 'local' | 'remote_mgt';
  remote_broker_url: string;
}

const COMMAND_ID = 'magiclaude:run-magic';
const PLUGIN_ID = 'magiclaude:plugin';

async function loadSettings(settingRegistry: ISettingRegistry): Promise<PluginSettings> {
  const settings = await settingRegistry.load(PLUGIN_ID);
  const composite = settings.composite as Partial<PluginSettings>;
  return {
    claude_executable_path: composite.claude_executable_path || 'claude',
    jcm_mode: (composite.jcm_mode as 'local' | 'remote_mgt') || 'local',
    remote_broker_url: composite.remote_broker_url || 'http://127.0.0.1:1207'
  };
}

async function runOnActiveNotebook(tracker: INotebookTracker, pluginSettings: PluginSettings) {
  const panel = tracker.currentWidget as NotebookPanel | null;
  if (!panel || !panel.content.activeCell) {
    throw new Error('No active notebook cell');
  }

  const activeIndex = panel.content.activeCellIndex;
  const activeCell = panel.content.activeCell;
  const source = activeCell.model.sharedModel.getSource();
  const parsed = parseMagic(source);
  if (!parsed) {
    throw new Error('Cell must contain @c ... @c or @n ... @n block with instruction text');
  }

  const body = {
    command: parsed.command,
    prompt: parsed.prompt,
    notebook_path: panel.context.path,
    active_cell_index: activeIndex,
    cells: collectCells(panel),
    dry_run: false,
    claude_executable_path: pluginSettings.claude_executable_path,
    jcm_mode: pluginSettings.jcm_mode,
    remote_broker_url: pluginSettings.remote_broker_url
  };

  const data = await requestAPI<ExecuteResponse>('execute', {
    method: 'POST',
    body: JSON.stringify(body)
  });

  applyOps(panel, data.ops || []);
  await panel.context.save();
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker, ISettingRegistry],
  activate: async (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    tracker: INotebookTracker,
    settingRegistry: ISettingRegistry
  ) => {
    let pluginSettings = await loadSettings(settingRegistry);

    app.commands.addCommand(COMMAND_ID, {
      label: 'Run magiclaude (@c...@c / @n...@n)',
      execute: async () => {
        try {
          pluginSettings = await loadSettings(settingRegistry);
          await runOnActiveNotebook(tracker, pluginSettings);
        } catch (err: any) {
          await showErrorMessage('MagiClaude', err?.message || String(err));
        }
      }
    });

    palette.addItem({ command: COMMAND_ID, category: 'Notebook Operations' });
  }
};

export default plugin;
