import { Router } from 'express';
import { authRouter } from './auth.js';
import { chatRouter } from './chat.js';
import { docsRouter } from './docs.js';
import { healthRouter } from './health.js';
import { importRouter } from './import.js';
import { progressRouter } from './progress.js';
import { questionsRouter } from './questions.js';
import { revisionRouter } from './revision.js';
import { submitRouter } from './submit.js';
import { topicsRouter } from './topics.js';

export const apiRouter = Router();

apiRouter.use(healthRouter);
apiRouter.use('/docs', docsRouter);
apiRouter.use('/auth', authRouter);
apiRouter.use(submitRouter);
apiRouter.use('/topics', topicsRouter);
apiRouter.use('/questions', questionsRouter);
apiRouter.use('/progress', progressRouter);
apiRouter.use('/revision', revisionRouter);
apiRouter.use('/import', importRouter);
apiRouter.use('/chat', chatRouter);
