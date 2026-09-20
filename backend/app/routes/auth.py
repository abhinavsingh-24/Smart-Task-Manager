from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import authenticate_user, create_user, get_current_user, security

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with validated name, email, and password information.",
)
def register_user(payload: UserCreate):
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match.",
        )

    user = create_user(payload)
    auth_result = authenticate_user(UserLogin(email=payload.email, password=payload.password))
    token_response = TokenResponse(
        access_token=auth_result["access_token"],
        token_type=auth_result["token_type"],
        user=UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            created_at=user["created_at"],
            updated_at=user["updated_at"],
        ),
    )
    return token_response


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and receive a JWT",
    description="Authenticate a user with their email and password and return an access token.",
)
def login_user(payload: UserLogin):
    return authenticate_user(payload)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Return the authenticated user's profile information from the JWT.",
)
def get_current_user_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    current_user = get_current_user(credentials)
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
        created_at=current_user["created_at"],
        updated_at=current_user["updated_at"],
    )
