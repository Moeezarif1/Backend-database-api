from fastapi import APIRouter, HTTPException
from app.dependencies import async_session
from app.models import DatabaseCredentials
from sqlalchemy.future import select
from sqlalchemy import create_engine
from sqlalchemy import text

router = APIRouter()


@router.get("/{database_id}")
async def get_schema(database_id: int):
    async with async_session() as session:
        # Retrieve database credentials
        credentials_result = await session.execute(select(DatabaseCredentials).where(DatabaseCredentials.id == database_id))
        credentials = credentials_result.scalar_one_or_none()

        if credentials is None:
            raise HTTPException(status_code=404, detail="Database credentials not found")

        # Establish a connection to the specified database
        db_engine = create_engine(f"postgresql://{credentials.user}:{credentials.password}@{credentials.host}:{credentials.port}/{credentials.dbname}")
        connection = db_engine.connect()

        # Query to fetch schema information, focusing on user-defined tables
        schema_query = """
        SELECT
            table_schema,
            table_name,
            column_name,
            data_type
        FROM
            information_schema.columns
        WHERE
            table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY
            table_schema,
            table_name,
            ordinal_position;
        """
        result = connection.execute(schema_query)

        # Format the results
        schema_info = {
            "database_name": credentials.dbname,
            "tables": {}
        }
        for row in result:
            if row.table_schema not in schema_info["tables"]:
                schema_info["tables"][row.table_schema] = {}
            if row.table_name not in schema_info["tables"][row.table_schema]:
                schema_info["tables"][row.table_schema][row.table_name] = []
            schema_info["tables"][row.table_schema][row.table_name].append({
                "column_name": row.column_name,
                "data_type": row.data_type
            })

        connection.close()
        return schema_info


@router.get("/search/{database_id}/{table_name}")
async def search_table(database_id: int, table_name: str):
    async with async_session() as session:
        # Retrieve database credentials
        credentials_result = await session.execute(select(DatabaseCredentials).where(DatabaseCredentials.id == database_id))
        credentials = credentials_result.scalar_one_or_none()

        if credentials is None:
            raise HTTPException(status_code=404, detail="Database credentials not found")

        # Establish a connection to the specified database
        db_engine = create_engine(f"postgresql://{credentials.user}:{credentials.password}@{credentials.host}:{credentials.port}/{credentials.dbname}")
        connection = db_engine.connect()

        # Query to search for the specified table
        search_query = text("""
        SELECT
            table_schema,
            table_name,
            column_name,
            data_type
        FROM
            information_schema.columns
        WHERE
            table_schema NOT IN ('pg_catalog', 'information_schema')
            AND table_name = :table_name
        ORDER BY
            table_schema,
            table_name,
            ordinal_position;
        """)
        result = connection.execute(search_query, {'table_name': table_name})


        if result.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="Table not found")

        schema_info = {"database_name": credentials.dbname, "tables": {}}
        for row in result:
            if row.table_schema not in schema_info["tables"]:
                schema_info["tables"][row.table_schema] = {}
            if row.table_name not in schema_info["tables"][row.table_schema]:
                schema_info["tables"][row.table_schema][row.table_name] = []
            schema_info["tables"][row.table_schema][row.table_name].append({
                "column_name": row.column_name,
                "data_type": row.data_type
            })

        connection.close()
        return schema_info

