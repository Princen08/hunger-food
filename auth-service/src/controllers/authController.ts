import { Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

import User from '../models/userModel';
import { generateOTP, getOTP, saveOTP } from '../utils/otpUtils';
import { sendOTPEmail } from '../utils/sendOTPEmail';
import logger from '../utils/logger';

const COOKIE_NAME = 'access-token';

/**
 * Controller for handling authentication-related operations.
 */
class AuthController {
    /**
     * Handles user signup.
     * Generates an OTP, sends it to the user's email, and creates a new user with `isVerified: false`.
     * @param req - Express request object containing `email`, `username`, and `password` in the body.
     * @param res - Express response object.
     */
    async signup(req: Request, res: Response) {
        try {
            const { email, username, password } = req.body;

            if (!email || !username || !password) {
                return res.status(400).json({ message: 'Email, username, and password are required' });
            }

            // Check if email already exists
            const existingUser = await User.findOne({ email });
            if (existingUser && existingUser.isVerified) {
                logger.warn(`User with email ${email} already exists`);
                return res.status(409).json({ message: 'User with provided email already exists' });
            }

            // Generate OTP
            const otp = generateOTP();

            // Save OTP temporarily
            saveOTP(email, otp);

            // Send OTP to the user's email
            await sendOTPEmail(email, otp);

            // Create a new user and generate a JWT token
            if (!existingUser) {
                await User.create({ email, username, password, isVerified: false });
            }
            return res.status(201).json({
                message: 'Signup successful. Please verify the OTP sent to your email.',
            });
        } catch (error: any) {
            logger.error(`Signup error: ${error.message}`);
            res.status(500).send('Internal Server Error');
        }
    }

    /**
     * Handles user login.
     * Authenticates the user by verifying the email and password, and generates a JWT token.
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
     * Decodes the JWT token from cookies and fetches the user details.
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
     * Clears the authentication cookie.
     * @param req - Express request object containing the JWT token in cookies.
     * @param res - Express response object.
     */
    async logout(req: Request, res: Response) {
        try {
            const token = req.cookies?.[COOKIE_NAME];
            if (!token) {
                return res.status(401).json({ message: 'Not logged in' });
            }
            // Clear the authentication cookie
            res.clearCookie(COOKIE_NAME);
            logger.info(`User logged out successfully`);
            res.status(200).json({ message: 'Logged out successfully' });
        } catch (error: any) {
            logger.error(`Logout error: ${error.message}`);
            return res.status(500).json({ message: 'Internal Server Error' });
        }
    }

    /**
     * Verifies the OTP sent to the user's email.
     * Marks the user as verified if the OTP is valid.
     * @param req - Express request object containing `email` and `otp` in the body.
     * @param res - Express response object.
     */
    async verifyOTP(req: Request, res: Response) {
        try {
            const { email, otp } = req.body;

            if (!email || !otp) {
                logger.warn('Email or OTP not provided in verifyOTP request');
                return res.status(400).json({ message: 'Email and OTP are required' });
            }

            // Retrieve the OTP from the store
            const storedOTP = getOTP(email);
            if (!storedOTP) {
                logger.warn(`OTP expired or not found for email: ${email}`);
                return res.status(400).json({ message: 'OTP expired or not found' });
            }

            if (storedOTP !== otp) {
                logger.warn(`Invalid OTP provided for email: ${email}`);
                return res.status(400).json({ message: 'Invalid OTP' });
            }

            // Mark the user as verified
            const user = await User.findOneAndUpdate(
                { email },
                { isVerified: true },
            );

            if (!user) {
                logger.error(`User not found for email: ${email}`);
                return res.status(404).json({ message: 'User not found' });
            }

            logger.info(`Email verified successfully for user: ${email}`);

            const newToken = jwt.sign({ id: user._id }, process.env.JWT_SECRET || 'secret', { expiresIn: '1h' });
            res.cookie(COOKIE_NAME, newToken, { httpOnly: true, sameSite: 'strict' });
            res.status(200).json({ message: 'Email verified successfully' });
        } catch (error: any) {
            logger.error(`Error in verifyOTP for email: ${req.body?.email || 'unknown'}, Error: ${error.message}`);
            res.status(500).json({ message: 'Internal Server Error', error: error.message });
        }
    }
}

export const authController = new AuthController();