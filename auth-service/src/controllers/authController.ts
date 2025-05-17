import { Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import User from '../models/userModel';

import logger from '../utils/logger';

const COOKIE_NAME = 'access-token';

/**
 * Controller for handling authentication-related operations.
 */
class AuthController {
    /**
     * Handles user signup.
     * @param req - Express request object containing `email`, `username`, and `password` in the body.
     * @param res - Express response object.
     */
    async signup(req: Request, res: Response) {
        try {
            const { email, username, password } = req.body;
            // Check if email already exists
            const existingUser = await User.findOne({ email });
            if (existingUser) {
                logger.warn(`User with email ${email} already exists`);
                return res.status(409).json({ message: 'User with provided email already exists' });
            }
            // Create a new user and generate a JWT token
            const user = await User.create({ email, username, password });
            logger.info(`User signed up successfully: ${req.body.email}`);

            const newToken = jwt.sign({ id: user._id }, process.env.JWT_SECRET || 'secret', { expiresIn: '1h' });
            res.cookie(COOKIE_NAME, newToken, { httpOnly: true, sameSite: 'strict' });
            res.status(201).json({ message: 'Signup successful' });
        } catch (error: any) {
            logger.error(`Signup error: ${error.message}`);
            res.status(500).send('Internal Server Error');
        }
    }
    /**
     * Handles user login.
     * @param req - Express request object containing `email` and `password` in the body.
     * @param res - Express response object.
     */
    async login(req: Request, res: Response) {
        try {
            const { email, password } = req.body;

            // Find the user by email
            const user = await User.findOne({ email });
            if (!user) {
                logger.error(`User with given email/password not found`);
                return res.status(401).json({ message: "Email or password does not match. Please try again" });
            }

            // Compare the provided password with the stored hashed password
            const passwordMatch = await bcrypt.compare(password, user.password);
            if (!passwordMatch) {
                logger.error(`User with given email/password not found`);
                return res.status(401).json({ message: "Email or password does not match. Please try again" });
            }
            logger.info(`User logged in successfully: ${req.body.email}`);
            // Generate a new JWT token
            const newToken = jwt.sign({ id: user._id }, process.env.JWT_SECRET || 'secret', { expiresIn: '1h' });
            res.cookie(COOKIE_NAME, newToken, { httpOnly: true, sameSite: 'strict' });
            res.status(201).json({ message: 'Login successful' });
        } catch (error: any) {
            logger.error(`Login error: ${error.message}`);
            res.status(401).send('Invalid credentials');
        }
    }

    /**
     * Retrieves the currently authenticated user.
     * @param req - Express request object containing the JWT token in cookies.
     * @param res - Express response object.
     */
    async getCurrentUser(req: Request, res: Response) {
        const token = req.cookies?.[COOKIE_NAME];
        if (!token) {
            return res.status(401).json({ message: 'User is not logged in' });
        }
        try {
            // Verify the JWT token
            const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret') as { id: string };
            const user = await User.findById(decoded.id);
            if (user) {
                res.json({ username: user.username });
            } else {
                res.status(404).json({ message: 'User not found' });
            }
        } catch (err) {
            res.status(401).json({ message: 'Invalid token' });
        }
    }

    /**
     * Logs out the currently authenticated user.
     * @param req - Express request object containing the JWT token in cookies.
     * @param res - Express response object.
     */
    async logout(req: Request, res: Response) {
        const token = req.cookies?.[COOKIE_NAME];
        if (!token) {
            return res.status(401).json({ message: 'Not logged in' });
        }

        // Clear the authentication cookie
        res.clearCookie(COOKIE_NAME);
        logger.info(`User logged out successfully`);
        res.status(200).json({ message: 'Logged out successfully' });
    }
}

export const authController = new AuthController();