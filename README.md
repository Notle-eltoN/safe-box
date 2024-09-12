# SafeBox: Encrypted File Storage System

## Overview

**SafeBox** is a secure file storage system that allows users to upload and download files with end-to-end encryption. Files are encrypted using AES-256 before they are stored on the server, ensuring that only the owner can access their files. The system also includes user authentication and file management features, making it ideal for applications requiring privacy and data protection.

## Features

- **AES-256 encryption** for secure file storage.
- **JWT-based authentication** for secure login.
- **Encrypted file metadata** to protect sensitive file information.
- **File management API** for upload, download, and delete operations.
- **SQLite for development** and **PostgreSQL** for production environments.

## Installation Guide

### 1. Clone the Repository

```
git clone https://github.com/yourusername/safe-box.git
cd safe-box
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Set Up the Database
For development purposes, SafeBox is configured to use SQLite. You don’t need to do anything for this; the database will be created automatically.

For production, you can configure the database to use PostgreSQL. So after creating a PostgreSQL, edit app/database.py and update the database URL for example like:
```
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost:5432/safebox_db"
```
### 4. Run the FastAPI Server
Start the FastAPI server locally:
```
uvicorn app.main:app --reload
```
The app will now be running at http://127.0.0.1:8000.
You can also access the API documentation at http://127.0.0.1:8000/docs