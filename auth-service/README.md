# Hungerfood Auth Service

Hungerfood Auth Service is a Node.js-based authentication service for user management, built with Express, MongoDB, and JWT. It provides endpoints for user signup, login, logout, OTP verification, and retrieving the current authenticated user.

## Features

- User authentication with JWT
- Password hashing with bcrypt
- OTP generation and email delivery for user verification
- API documentation with Swagger
- MongoDB integration with Mongoose
- Rate limiting for enhanced security
- Request ID middleware for better observability
- Logging with Winston and MongoDB integration
- Health check endpoint for service monitoring

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/hungerfood-auth-service.git
   cd hungerfood-auth-service/auth-service
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory and configure the following environment variables:
   ```env
   MONGODB_URI=<your-mongodb-uri>
   JWT_SECRET=<your-jwt-secret>
   PORT=<your-port>
   EMAIL_NAME=<your-email-address>
   EMAIL_PASS=<your-email-password>
   OTP_SECRET=<your-otp-secret>
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Base URL
```
http://localhost:<PORT>
```

### Endpoints

#### 1. **Signup**
   - **URL:** `/auth/signup`
   - **Method:** `POST`
   - **Description:** Register a new user.
   - **Request Body:**
     ```json
     {
       "username": "string",
       "email": "string",
       "password": "string"
     }
     ```
   - **Responses:**
     - `201`: Signup successful.
     - `409`: User with provided email already exists.

#### 2. **Login**
   - **URL:** `/auth/login`
   - **Method:** `POST`
   - **Description:** Login a user.
   - **Request Body:**
     ```json
     {
       "email": "string",
       "password": "string"
     }
     ```
   - **Responses:**
     - `200`: Login successful.
     - `401`: Invalid credentials.

#### 3. **Get Current User**
   - **URL:** `/auth/current_user`
   - **Method:** `GET`
   - **Description:** Get the currently authenticated user's information.
   - **Responses:**
     - `200`: Returns the current user's information.
     - `401`: No token provided or invalid token.

#### 4. **Logout**
   - **URL:** `/auth/logout`
   - **Method:** `POST`
   - **Description:** Logout the current user.
   - **Responses:**
     - `200`: Logged out successfully.
     - `401`: Not logged in.

#### 5. **Verify OTP**
   - **URL:** `/auth/verify-otp`
   - **Method:** `POST`
   - **Description:** Verify the OTP sent to the user's email.
   - **Request Body:**
     ```json
     {
       "email": "string",
       "otp": "string"
     }
     ```
   - **Responses:**
     - `200`: OTP verified successfully.
     - `400`: Invalid or expired OTP.
     - `404`: User not found.

#### 6. **Health Check**
   - **URL:** `/health`
   - **Method:** `GET`
   - **Description:** Check the health of the service.
   - **Responses:**
     - `200`: Service is healthy.
     - Example Response:
       ```json
       {
         "status": "UP",
         "timestamp": "2023-10-01T12:00:00.000Z"
       }
       ```

## Swagger API Documentation

The API documentation is available at:
```
http://localhost:<PORT>/api-docs
```

## Logging

The service uses Winston for logging, with logs stored in both the console and MongoDB. Logs include timestamps, log levels, and request IDs for better observability.

## Scripts

- `npm run start`: Start the application.
- `npm run build`: Build the TypeScript project.
- `npm run dev`: Start the application in development mode with hot-reloading.

## Deployment

The service is configured for deployment on Vercel. The `vercel.json` file specifies the build and routing configuration.

## License

This project is licensed under the ISC License.

## Author

Prince Patel