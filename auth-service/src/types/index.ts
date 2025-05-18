export interface User {
    id: string;
    username: string;
    email: string;
    password: string; // In a real application, this should be hashed
}

export interface AuthRequest extends Request {
    user?: User; // This will hold the authenticated user information
}
