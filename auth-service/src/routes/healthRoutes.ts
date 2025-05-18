import { Router } from 'express';

const router = Router();

/**
 * @openapi
 * /health:
 *   get:
 *     summary: Health check endpoint
 *     tags:
 *       - Health
 *     responses:
 *       200:
 *         description: Service is healthy
 */
router.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP', timestamp: new Date().toISOString() });
});

export default router;
