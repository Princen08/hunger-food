import express from 'express';
import bodyParser from 'body-parser';
import cookiesParser from 'cookie-parser';
import dotenv from 'dotenv';
import swaggerUi from 'swagger-ui-express';
import swaggerJsdoc from 'swagger-jsdoc';

import authRoutes from './routes/authRoutes';
import logger from './utils/logger';
import { connectDB } from './utils/db';

// Swagger configuration options
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Hungerfood Auth API',
      version: '1.0.0',
      description: 'API documentation for Hungerfood authentication service',
    },
  },
  apis: ['**/routes/*.ts'], // Path to the API docs
};

// Load environment variables from .env file
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON and URL-encoded data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Middleware to parse cookies
app.use(cookiesParser());

// Route for authentication-related endpoints
app.use('/auth', authRoutes);

// Middleware to handle CORS (Cross-Origin Resource Sharing)
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*'); // Allow all origins
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// Log incoming requests
app.use((req, res, next) => {
  logger.info(`Incoming request: ${req.method} ${req.url}`);
  next();
});

// Log unhandled errors
app.use((err: any, req: any, res: any, next: any) => {
  logger.error(`Unhandled error: ${err.message}`);
  res.status(500).send('Internal Server Error');
});

// Enable trust proxy to correctly interpret the X-Forwarded-For header
app.set('trust proxy', 1); // Use '1' if your app is behind one proxy (e.g., a load balancer)

// Connect to MongoDB using Mongoose
connectDB()

// Start the Express server
app.listen(PORT, () => {
  logger.info(`Server is running on http://localhost:${PORT}`);
});

// Swagger setup for API documentation
const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));