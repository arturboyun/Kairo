from __future__ import annotations

from typing import Annotated
from uuid import UUID

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from kairo.application.dto.user import (
    CreateUserDTO,
    GetUserByIdQuery,
)
from kairo.application.interactors.user import (
    CreateUserUseCase,
    GetUserByIdUseCase,
)
from kairo.domain.entities.user import User
from kairo.domain.exceptions import DomainError
from kairo.presentation.http.deps import (
    get_user_by_id_use_case,
    get_user_create_use_case,
)

router = APIRouter(prefix="/api/v1")


@router.get("/")
def read_root() -> dict[str, str]:
    """Root."""
    return {"Hello": "World"}


@router.post("/users")
def create_user(
    user: CreateUserDTO,
    use_case: Annotated[CreateUserUseCase, Depends(get_user_create_use_case)],
) -> User:
    """Create a new user."""
    return use_case(user)


@router.get("/users/{user_id}")
def get_user(
    user_id: UUID,
    use_case: Annotated[GetUserByIdUseCase, Depends(get_user_by_id_use_case)],
) -> User | None:
    """Get a user by ID."""
    return use_case(GetUserByIdQuery(user_id=user_id))


def get_production_app() -> FastAPI:
    """Get the production FastAPI application."""
    app = FastAPI()
    app.include_router(router)

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        """Handle domain errors."""
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )

    return app


def main() -> None:
    """Entry point for the application."""
    uvicorn.run(
        "kairo.presentation.http.application:get_production_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src/kairo"],
        factory=True,
    )
