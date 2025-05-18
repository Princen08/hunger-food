import logging
from pymongo import MongoClient, errors
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection details
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("LOG_DB_NAME", "hungerfood")
COLLECTION_NAME = os.getenv("LOG_COLLECTION_NAME", "order_service_logs")

# MongoDB client setup with error handling
try:
    client = MongoClient(
        MONGO_URI, serverSelectionTimeoutMS=5000
    )  # Timeout after 5 seconds
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    # Test the connection
    client.admin.command("ping")
    print("Connected to MongoDB successfully!")
except errors.ServerSelectionTimeoutError as e:
    print(f"Failed to connect to MongoDB: {e}")
    client = None  # Set client to None if connection fails
except Exception as e:
    print(f"An unexpected error occurred while connecting to MongoDB: {e}")
    client = None


class MongoDBHandler(logging.Handler):
    def emit(self, record):
        if client is None:
            # Skip logging if MongoDB connection is not available
            print("MongoDB connection is not available. Skipping log entry.")
            return
        try:
            log_entry = self.format(record)
            log_data = {
                "level": record.levelname,
                "message": record.getMessage(),
                "timestamp": datetime.utcnow(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }
            collection.insert_one(log_data)
        except Exception as e:
            # Handle logging errors gracefully
            print(f"Failed to log to MongoDB: {e}")


# Logger setup
logger = logging.getLogger("order_service_logger")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(console_handler)

# MongoDB handler
if client is not None:
    mongo_handler = MongoDBHandler()
    mongo_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(mongo_handler)
