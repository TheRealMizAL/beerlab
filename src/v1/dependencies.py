from typing import Annotated

from fastapi import Depends

from core.schemas.security import TokenData
from core.security import get_current_user


async def get_current_active_user(
        current_user: Annotated[TokenData, Depends(get_current_user)]
):
    return current_user
