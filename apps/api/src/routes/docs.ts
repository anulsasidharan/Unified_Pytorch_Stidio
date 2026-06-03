import { Router } from 'express';
import swaggerUi from 'swagger-ui-express';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse as parseYaml } from 'yaml';

const __dirname = dirname(fileURLToPath(import.meta.url));
const openapiPath = join(__dirname, '../../../../docs/openapi.yaml');

export const docsRouter = Router();

let spec: Record<string, unknown>;
try {
  spec = parseYaml(readFileSync(openapiPath, 'utf8')) as Record<string, unknown>;
} catch {
  spec = {
    openapi: '3.0.3',
    info: { title: 'DSA Studio API', version: '0.1.0' },
    paths: {},
  };
}

docsRouter.get('/openapi.json', (_req, res) => {
  res.json(spec);
});

docsRouter.use('/', swaggerUi.serve);
docsRouter.get('/', swaggerUi.setup(spec, { explorer: true }));
