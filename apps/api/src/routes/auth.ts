import { Router } from 'express';
import { prisma } from '../lib/prisma.js';
import { hashPassword, verifyPassword } from '../lib/password.js';
import { signToken } from '../lib/jwt.js';
import { success } from '../lib/response.js';
import { serializeUser } from '../lib/serializers.js';
import { AppError } from '../middleware/errorHandler.js';
import { requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { validate } from '../middleware/validate.js';
import { loginSchema, registerSchema } from '../validators/auth.js';
import { profileUpdateSchema } from '../validators/progress.js';

export const authRouter = Router();

authRouter.post('/register', validate(registerSchema), async (req, res, next) => {
  try {
    const { username, email, password, fullName } = req.body;

    const existing = await prisma.user.findFirst({
      where: { OR: [{ email }, { username }] },
    });
    if (existing) {
      const field = existing.email === email ? 'email' : 'username';
      throw new AppError(409, 'CONFLICT', `A user with this ${field} already exists`);
    }

    const passwordHash = await hashPassword(password);
    const user = await prisma.user.create({
      data: {
        username,
        email,
        passwordHash,
        fullName: fullName ?? null,
      },
    });

    const token = signToken({ userId: user.userId, email: user.email });

    res.status(201).json(
      success({
        user: serializeUser(user),
        token,
      }),
    );
  } catch (error) {
    next(error);
  }
});

authRouter.post('/login', validate(loginSchema), async (req, res, next) => {
  try {
    const { email, password } = req.body;

    const user = await prisma.user.findUnique({ where: { email } });
    if (!user || !(await verifyPassword(password, user.passwordHash))) {
      throw new AppError(401, 'INVALID_CREDENTIALS', 'Invalid email or password');
    }

    await prisma.user.update({
      where: { userId: user.userId },
      data: { lastActive: new Date() },
    });

    const token = signToken({ userId: user.userId, email: user.email });

    res.json(
      success({
        user: serializeUser(user),
        token,
      }),
    );
  } catch (error) {
    next(error);
  }
});

authRouter.post('/logout', requireAuth, (_req, res) => {
  res.json(success({ message: 'Logged out successfully' }));
});

authRouter.get('/me', requireAuth, async (req: AuthenticatedRequest, res, next) => {
  try {
    const user = await prisma.user.findUnique({ where: { userId: req.userId! } });
    if (!user) {
      throw new AppError(404, 'NOT_FOUND', 'User not found');
    }

    res.json(success({ user: serializeUser(user) }));
  } catch (error) {
    next(error);
  }
});

authRouter.put('/profile', requireAuth, validate(profileUpdateSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { fullName, learningLevel, dailyTarget, targetGoal } = req.body;

    const user = await prisma.user.update({
      where: { userId: req.userId! },
      data: {
        ...(fullName !== undefined ? { fullName } : {}),
        ...(learningLevel !== undefined ? { learningLevel } : {}),
        ...(dailyTarget !== undefined ? { dailyTarget } : {}),
        ...(targetGoal !== undefined ? { targetGoal } : {}),
      },
    });

    res.json(success({ user: serializeUser(user) }));
  } catch (error) {
    next(error);
  }
});
