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

[comment]: <> (```bash)

[comment]: <> (uvicorn main:app --reload)



### Notes:

- Replace `https://github.com/Moeezarif1/Backend-database-api.git` with the actual URL of your GitHub repository.
- Replace `Your Name` and `YourGithubProfile` with your actual name and GitHub profile link.
- Add a `CONTRIBUTING.md` and `LICENSE.md` if you plan to have contributions from others or if you want to make the licensing clear.
- If you have a list of contributors, link to that page or list their names.
- You can also add sections for tests, API documentation links, or any other relevant information that a developer might need to use your project.
- For larger projects, it's common to include additional documentation in the `docs/` directory.
- Adjust any commands or JSON payloads to match the actual usage in your application.





### High-Level System Diagram

System primarily consists of the following components:

1. **FastAPI Application**: This is the core of your system, handling all API requests and responses.
2. **PostgreSQL Database**: This database stores your application's data, particularly the `DBCredentials` table.
3. **Client**: Represents users or systems that interact with your API.

The interaction between these components can be illustrated as follows:

- The **Client** sends requests to the **FastAPI Application**.
- The **FastAPI Application** processes these requests. When data related to database credentials is required, it interacts with the **PostgreSQL Database**.
- The **PostgreSQL Database** stores and retrieves the `DBCredentials` data as requested by the FastAPI Application.

#### Diagram Representation

1. **Client**
   - Sends HTTP requests (POST, GET).
2. **FastAPI Application**
   - Receives requests from the Client.
   - Processes requests, involving querying or updating the database.
   - Sends back responses to the Client.
3. **PostgreSQL Database**
   - Stores `DBCredentials` table.
   - Handles queries from the FastAPI Application.

The **Client** ↔ **FastAPI Application** interaction is over HTTP, while the **FastAPI Application** ↔ **PostgreSQL Database** interaction involves database queries.

### Data Model

For the `DBCredentials` table in your PostgreSQL database, the data model could look something like this:

- **DBCredentials Table**
  - `id`: Integer, Primary Key.
  - `user`: String, the username for the database.
  - `password`: String, the hashed password for the database.
  - `host`: String, the host address of the database.
  - `dbname`: String, the name of the database.
  - `port`: Integer, the port number for the database connection.

Each row in this table represents a set of credentials for accessing a particular database. When your FastAPI application needs to access a database, it retrieves the relevant credentials from this table.

#### Note:
- The `password` field should ideally store a hashed version of the actual password for security reasons.
- Depending on your application's requirements, you might need additional fields for things like connection options or extra metadata.

### Brief documentation on the endpoints of your API

- API documentation is available at http://localhost:8000/redoc

### High-level answers to the following questions:

1. Auth0, we provide a sophisticated and flexible authentication solution. Auth0 
excels in offering a vast array of features such as social logins, multi-factor 
authentication, and support for various identity providers. This not only streamlines 
the user authentication experience but also ensures robust security standards are 
upheld, essential for modern web applications.

2. To effectively manage a high volume of traffic, I would advocate for a cloud-based
 infrastructure with auto-scaling capabilities to dynamically adjust resources based
  on real-time demand. Alongside this, optimizing the database performance through the
   implementation of read replicas and strategic caching mechanisms would be key. 
   The deployment of load balancers would also be instrumental in efficiently 
   distributing incoming traffic across multiple servers, ensuring high availability


3. If faced with the challenge of adapting our system to support databases 
   with up to 10,000 tables or even those with a million columns across 100,000 
   tables, our design approach would undergo significant modifications to ensure 
   efficient and scalable operations. Firstly, we would integrate advanced batch 
   processing techniques to manage schema information retrieval in increments, 
   preventing any timeouts due to excessively long queries. Caching strategies 
   would also play a crucial role, particularly for infrequently changing schema
   information, to reduce redundant queries and alleviate the load on both our system 
   and the user databases.
   Incorporating asynchronous processing would be essential to facilitate multiple 
   concurrent connections to various databases without impeding the API service's 
   responsiveness. For the vast amounts of data expected in the responses, we would
   implement pagination to deliver the schema information in manageable segments, thus
   ensuring that our API remains swift and the data transfer to clients is practical.