import express from 'express';
import bodyParser from 'body-parser';
import cookiesParser from 'cookie-parser';
import dotenv from 'dotenv';
import mongoose from 'mongoose';
import swaggerUi from 'swagger-ui-express';
import swaggerJsdoc from 'swagger-jsdoc';

import authRoutes from '../routes/authRoutes';

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

// Connect to MongoDB using Mongoose
mongoose.connect(process.env.MONGODB_URI as string)
  .then(() => console.log('MongoDB connected')) // Log success message
  .catch(err => console.error('MongoDB connection error:', err)); // Log error message

// Start the Express server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

// Swagger setup for API documentation
const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));