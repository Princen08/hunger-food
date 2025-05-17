import speakeasy from 'speakeasy';
import logger from './logger'; // Assuming you have a logger utility

export const generateOTP = (): string => {
  try {
    return speakeasy.totp({
      secret: process.env.OTP_SECRET || 'secret', // Use a secure secret
      encoding: 'base32',
      digits: 6, // Length of the OTP
      step: 300, // OTP is valid for 5 minutes (300 seconds)
    });
  } catch (error: any) {
    logger.error(`Error generating OTP: ${error.message}`);
    throw new Error('Failed to generate OTP');
  }
};

const otpStore: { [key: string]: string } = {}; // Key-value store for OTPs

export const saveOTP = (email: string, otp: string): void => {
  try {
    otpStore[email] = otp;
    setTimeout(() => delete otpStore[email], 300000); // Delete OTP after 5 minutes
    logger.info(`OTP saved successfully for email: ${email}`);
  } catch (error: any) {
    logger.error(`Error saving OTP for email ${email}: ${error.message}`);
    throw new Error('Failed to save OTP');
  }
};

export const getOTP = (email: string): string | undefined => {
  try {
    const otp = otpStore[email];
    if (!otp) {
      logger.warn(`No OTP found for email: ${email}`);
    }
    return otp;
  } catch (error: any) {
    logger.error(`Error retrieving OTP for email ${email}: ${error.message}`);
    throw new Error('Failed to retrieve OTP');
  }
};