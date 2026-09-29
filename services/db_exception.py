from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def handle_database_error(db, error):

    db.rollback()

    if isinstance(error, IntegrityError):
        raise HTTPException(
            status_code=400,
            detail="Database constraint violation"
        )

    raise error