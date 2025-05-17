import { createLogger, format, transports } from 'winston';
import 'winston-mongodb';

const logger = createLogger({
  level: 'info',
  format: format.combine(
    format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    format.printf(({ timestamp, level, message, requestId }) =>
      requestId
        ? `${timestamp} [${level.toUpperCase()}] [Request ID: ${requestId}]: ${message}`
        : `${timestamp} [${level.toUpperCase()}]: ${message}`
    )
  ),
  transports: [
    new transports.Console(), // Log to the console
    new transports.MongoDB({
      level: 'info', // Log level to store in MongoDB
      db: process.env.MONGODB_URI || 'mongodb://localhost:27017/logs', // MongoDB connection URI
      collection: 'auth_service_logs', // Collection name for logs
      format: format.combine(
        format.timestamp(),
        format.json() // Store logs in JSON format
      ),
    }),
  ],
});

export default logger;