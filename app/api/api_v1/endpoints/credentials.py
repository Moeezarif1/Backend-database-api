from fastapi import APIRouter
from app.dependencies import async_session
from app.models import DatabaseCredentials
from app.schemas import Credentials

router = APIRouter()

@router.post("/credentials")
async def add_credentials(credentials: Credentials):
    async with async_session() as session:
        # Encrypt the password before storing
        new_credentials = DatabaseCredentials(
            user=credentials.user,
            password=credentials.password,  # This will automatically hash the password
            host=credentials.host,
            dbname=credentials.dbname,
            port=credentials.port
        )
        session.add(new_credentials)
        await session.commit()
        return {"message": "Credentials added successfully", "id": new_credentials.id}

