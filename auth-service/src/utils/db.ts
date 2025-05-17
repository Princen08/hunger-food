import mongoose from 'mongoose';
import logger from './logger';

export const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI as string);
    logger.info('MongoDB connected successfully');
  } catch (error: any) {
    logger.error(`MongoDB connection error: ${error.message}`);
    process.exit(1);
  }
};