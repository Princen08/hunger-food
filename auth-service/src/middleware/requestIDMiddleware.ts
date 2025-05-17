import { v4 as uuidv4 } from 'uuid';
import { Request, Response, NextFunction } from 'express';

export const requestIdMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const requestId = uuidv4(); // Generate a unique ID
  res.setHeader('X-Request-Id', requestId); // Optionally, send it in the response headers
  next();
};