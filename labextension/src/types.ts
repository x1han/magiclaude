export type CellType = 'code' | 'markdown';

export interface NotebookOp {
  type: 'replace_cell' | 'insert_cell_after';
  index: number;
  cell_type?: CellType;
  source: string;
}

export function parseMagic(source: string): { command: '@c' | '@n'; prompt: string } | null {
  const cToken = '@c';
  const nToken = '@n';

  const cFirst = source.indexOf(cToken);
  const nFirst = source.indexOf(nToken);

  if (cFirst === -1 && nFirst === -1) {
    return null;
  }

  const useC = cFirst !== -1 && (nFirst === -1 || cFirst < nFirst);
  const token = useC ? cToken : nToken;
  const command = (useC ? '@c' : '@n') as '@c' | '@n';

  const start = source.indexOf(token);
  const end = source.indexOf(token, start + token.length);
  if (start === -1 || end === -1) {
    return null;
  }

  const prompt = source.slice(start + token.length, end).trim();
  if (!prompt) {
    return null;
  }

  return { command, prompt };
}
