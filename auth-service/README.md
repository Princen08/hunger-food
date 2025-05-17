# Hungerfood Auth Service

Hungerfood Auth Service is a Node.js-based authentication service for user management, built with Express, MongoDB, and JWT. It provides endpoints for user signup, login, logout, and retrieving the current authenticated user.

## Features

- User authentication with JWT
- Password hashing with bcrypt
- API documentation with Swagger
- MongoDB integration with Mongoose

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
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Base URL
```
http://localhost:<PORT>/auth
```

### Endpoints

#### 1. **Signup**
   - **URL:** `/signup`
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
   - **URL:** `/login`
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
   - **URL:** `/current_user`
   - **Method:** `GET`
   - **Description:** Get the currently authenticated user's information.
   - **Responses:**
     - `200`: Returns the current user's information.
     - `401`: No token provided or invalid token.

#### 4. **Logout**
   - **URL:** `/logout`
   - **Method:** `POST`
   - **Description:** Logout the current user.
   - **Responses:**
     - `200`: Logged out successfully.
     - `401`: Not logged in.

## Swagger API Documentation

The API documentation is available at:
```
http://localhost:<PORT>/api-docs
```

## Scripts

- `npm run start`: Start the application.
- `npm run build`: Build the TypeScript project.
- `npm run dev`: Start the application in development mode with hot-reloading.

## License

This project is licensed under the ISC License.

## Author

Prince Patel