from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token

from app.modules.auth.repositories.account import AccountRepository
from app.modules.auth.schemas.account import AccountAuth
from app.utils.hash import Hash


class AuthenticateAccount:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, account: AccountAuth):
        account_repository = AccountRepository(self.db)

        existent_account = account_repository.get_one_by_username(account.username)

        if not existent_account:
            raise HTTPException(status_code=404, detail="sessions.account.not_found")

        password_is_valid = Hash().verify(hashed_password=existent_account.password, plain_password=account.password)

        if not password_is_valid:
            raise HTTPException(status_code=400, detail="sessions.account.invalid_user_credentials")

        access_token = create_access_token(
            data={
                "sub": existent_account.username,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
