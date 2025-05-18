import nodemailer from 'nodemailer';
import logger from '../utils/logger'; // Assuming you have a logger utility

import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const transporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    auth: {
        user: process.env.EMAIL_NAME, // Your email address
        pass: process.env.EMAIL_PASS, // Your email password or app-specific password
    },
});

export const sendOTPEmail = async (email: string, otp: string): Promise<void> => {
    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: email,
        subject: 'Hungerfood (Verification): Your OTP Code',
        html: `
      <h1>Your OTP Code</h1>
      <p>Use the following OTP to complete your action:</p>
      <h2>${otp}</h2>
      <p>This OTP is valid for 5 minutes.</p>
    `,
    };

    try {
        await transporter.sendMail(mailOptions);
        logger.info(`OTP email sent successfully to ${email}`);
    } catch (error: any) {
        logger.error(`Failed to send OTP email to ${email}: ${error.message}`);
        throw new Error('Failed to send OTP email');
    }
};
