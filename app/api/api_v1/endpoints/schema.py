from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from functools import lru_cache
from sqlalchemy.orm import sessionmaker
from app.dependencies import get_database_session
from app.models import DatabaseCredentials
from sqlalchemy.future import select
from sqlalchemy import text

router = APIRouter()

db_engine_cache = {}


def get_engine_cache_key(credentials):
    return f"{credentials.user}:{credentials.password}@{credentials.host}:{credentials.port}/{credentials.dbname}"


@lru_cache
def create_cached_engine(db_url):
    return create_async_engine(db_url)


@router.get("/{database_id}")
async def get_schema(database_id: int, session: AsyncSession = Depends(get_database_session)):
    # Retrieve database credentials
    credentials_result = await session.execute(select(DatabaseCredentials).where(DatabaseCredentials.id == database_id))
    credentials = credentials_result.scalar_one_or_none()

    if credentials is None:
        raise HTTPException(status_code=404, detail="Database credentials not found")

    # Construct the user database URL
    user_db_url = f"postgresql+asyncpg://{credentials.user}:{credentials.password}@{credentials.host}:{credentials.port}/{credentials.dbname}"

    # Check if an engine for these credentials is already cached
    cache_key = get_engine_cache_key(credentials)
    if cache_key not in db_engine_cache:
        db_engine_cache[cache_key] = create_cached_engine(user_db_url)

    user_db_engine = db_engine_cache[cache_key]
    user_session = sessionmaker(user_db_engine, expire_on_commit=False, class_=AsyncSession)

    async with user_session() as user_db_session:
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
        result = await user_db_session.execute(schema_query)
        rows = result.all()

        schema_info = {
            "database_name": credentials.dbname,
            "tables": {}
        }

        for row in rows:
            # Each row here should be a full row object, not just a scalar
            if row.table_schema not in schema_info["tables"]:
                schema_info["tables"][row.table_schema] = {}
            if row.table_name not in schema_info["tables"][row.table_schema]:
                schema_info["tables"][row.table_schema][row.table_name] = []
            schema_info["tables"][row.table_schema][row.table_name].append({
                "column_name": row.column_name,
                "data_type": row.data_type
            })

        return schema_info


@router.get("/search/{database_id}/{table_name}")
async def search_table(database_id: int, table_name: str, primary_session: AsyncSession = Depends(get_database_session)):
    # Retrieve database credentials from the primary database
    credentials_result = await primary_session.execute(select(DatabaseCredentials).where(DatabaseCredentials.id == database_id))
    credentials = credentials_result.scalar_one_or_none()

    if credentials is None:
        raise HTTPException(status_code=404, detail="Database credentials not found")

    # Construct the user database URL
    user_db_url = f"postgresql+asyncpg://{credentials.user}:{credentials.password}@{credentials.host}:{credentials.port}/{credentials.dbname}"

    # Create an engine for the user-specified database
    user_db_engine = create_async_engine(user_db_url)
    user_session_maker = sessionmaker(user_db_engine, expire_on_commit=False, class_=AsyncSession)

    # Use this session to query the user-specified database
    async with user_session_maker() as user_db_session:
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
        result = await user_db_session.execute(search_query, {'table_name': table_name})

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Table not found")

        rows = result.all()
        schema_info = {"database_name": credentials.dbname, "tables": {}}
        for row in rows:
            if row.table_schema not in schema_info["tables"]:
                schema_info["tables"][row.table_schema] = {}
            if row.table_name not in schema_info["tables"][row.table_schema]:
                schema_info["tables"][row.table_schema][row.table_name] = []
            schema_info["tables"][row.table_schema][row.table_name].append({
                "column_name": row.column_name,
                "data_type": row.data_type
            })

        return schema_info
