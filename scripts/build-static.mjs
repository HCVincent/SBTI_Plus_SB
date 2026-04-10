import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const outputDir = join(root, 'dist');
const entries = ['index.html', 'data', 'image'];

rmSync(outputDir, { recursive: true, force: true });
mkdirSync(outputDir, { recursive: true });

for (const entry of entries) {
  const source = join(root, entry);
  if (!existsSync(source)) {
    throw new Error(`Missing required entry: ${entry}`);
  }

  cpSync(source, join(outputDir, entry), { recursive: true });
}

console.log('Built static site into dist/');
