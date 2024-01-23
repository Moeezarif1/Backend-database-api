# FastAPI Database Schema Extraction API

## Overview

This FastAPI application provides a RESTful API to submit credentials for a SQL database and process all the tables and columns in the database. It supports schema extraction and allows searching for specific table names within a database.

## Features

- Submit and store database credentials securely.
- Retrieve schema information for a given database.
- Search for specific tables within a database schema.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Moeezarif1/Backend-database-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd path/to/your/project
    ```

3. Build and run the containers:

    ```bash
    docker-compose up --build
    ```

The API will be available at `http://localhost:8000`.

## Usage

The API endpoints are described below.

### Submit Database Credentials

- **POST** `/credentials`

    Submit your SQL database credentials for storage.

    ```json
    {
        "dbname": "your_database",
        "user": "your_username",
        "password": "your_password",
        "host": "your_host",
        "port": 5432
    }
    ```

### Retrieve Database Schema Information

- **GET** `/{database_id}`

    Retrieve schema information for the specified database.

### Search for a Table Name

- **GET** `/search/{database_id}/{table_name}`

    Search for a specific table within the database schema.

## Development

To run the application for development, you can use the following command:

```bash
uvicorn main:app --reload



### Notes:

- Replace `https://yourrepositorylink.git` with the actual URL of your GitHub repository.
- Replace `Your Name` and `YourGithubProfile` with your actual name and GitHub profile link.
- Add a `CONTRIBUTING.md` and `LICENSE.md` if you plan to have contributions from others or if you want to make the licensing clear.
- If you have a list of contributors, link to that page or list their names.
- You can also add sections for tests, API documentation links, or any other relevant information that a developer might need to use your project.
- For larger projects, it's common to include additional documentation in the `docs/` directory.
- Adjust any commands or JSON payloads to match the actual usage in your application.
