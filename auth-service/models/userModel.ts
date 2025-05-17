import mongoose, { Document, Model } from 'mongoose';
import bcrypt from 'bcrypt';

/**
 * Interface representing a user document in MongoDB.
 */
interface IUser extends Document {
    username: string;
    password: string;
    email: string;
    comparePassword: (password: string) => Promise<boolean>;
}

/**
 * Mongoose schema for the User model.
 */
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});

/**
 * Pre-save hook to hash the password before saving the user document.
 */
userSchema.pre<IUser>('save', async function (next) {
    if (!this.isModified('password')) return next();
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
});

/**
 * Method to compare a plain text password with the hashed password.
 * @param password - Plain text password.
 * @returns A promise that resolves to a boolean indicating if the passwords match.
 */
userSchema.methods.comparePassword = async function (password: string): Promise<boolean> {
    return await bcrypt.compare(password, this.password);
};

const User: Model<IUser> = mongoose.model<IUser>('User', userSchema, 'users');

export default User;