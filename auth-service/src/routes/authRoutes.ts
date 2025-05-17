import { Router } from 'express';
import { authController } from '../controllers/authController';
import { rateLimiter } from '../middleware/rateLimiterMiddleware';
import { validateSignup, validateLogin } from '../middleware/userInputValidationMiddleware';

const router = Router();

/**
 * @openapi
 * /auth/signup:
 *   post:
 *     summary: Register a new user
 *     tags:
 *       - Auth
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - username
 *               - email
 *               - password
 *             properties:
 *               username:
 *                 type: string
 *               email:
 *                 type: string
 *               password:
 *                 type: string
 *     responses:
 *       201:
 *         description: Signup successful
 *       409:
 *         description: User with provided email already exists
 */
router.post('/signup', rateLimiter, validateSignup, authController.signup.bind(authController));
/**
 * @openapi
 * /auth/login:
 *   post:
 *     summary: Login a user
 *     tags:
 *       - Auth
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               email:
 *                 type: string
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Login successful
 *       401:
 *         description: Invalid credentials
 */
router.post('/login', rateLimiter, validateLogin, authController.login.bind(authController));
/**
 * @openapi
 * /auth/current_user:
 *   get:
 *     summary: Get current authenticated user
 *     tags:
 *       - Auth
 *     responses:
 *       200:
 *         description: Current user info
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 username:
 *                   type: string
 *       401:
 *         description: No token provided or invalid token
 */
router.get('/current_user', rateLimiter, authController.getCurrentUser.bind(authController));
/**
 * @openapi
 * /auth/logout:
 *   post:
 *     summary: Logout the current user
 *     tags:
 *       - Auth
 *     responses:
 *       200:
 *         description: Logged out successfully
 */
router.post('/logout', rateLimiter, authController.logout.bind(authController));

/**
 * @openapi
 * /auth/verify-otp:
 *   post:
 *     summary: Verify the OTP sent to the user's email
 *     tags:
 *       - Auth
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - otp
 *             properties:
 *               email:
 *                 type: string
 *                 description: The email address of the user
 *               otp:
 *                 type: string
 *                 description: The OTP sent to the user's email
 *     responses:
 *       200:
 *         description: OTP verified successfully
 *       400:
 *         description: Invalid or expired OTP
 *       404:
 *         description: User not found
 *       500:
 *         description: Internal server error
 */
router.post('/verify-otp', rateLimiter, authController.verifyOTP.bind(authController));

export default router;