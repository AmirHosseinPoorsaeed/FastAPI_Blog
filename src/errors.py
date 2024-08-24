from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class BlogException(Exception):
    pass


class InvalidCredantials(BlogException):
    pass


class UserAlreadyExists(BlogException):
    pass


class UserNotFound(BlogException):
    pass


class InvalidToken(BlogException):
    pass


class PasswordIncorrect(BlogException):
    pass


class PasswordNotMatch(BlogException):
    pass


class AccessTokenRequired(BlogException):
    pass


class RefreshTokenRequired(BlogException):
    pass


class InvalidToken(BlogException):
    pass


class InvalidScheme(BlogException):
    pass


class BlogNotFound(BlogException):
    pass


class BlogAlreadyExists(BlogException):
    pass


class ReviewNotFound(BlogException):
    pass


class TagNotFound(BlogException):
    pass


class TagAlreadyExists(BlogException):
    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: BlogException):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        InvalidCredantials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                'message': 'Incorrect username or password',
                'error_code': 'invalid_credentials'
            },
        ),
    )
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                'message': 'User with this email and username already exists',
                'error_code': 'user_exists'
            },
        ),
    )
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                'message': 'User not found',
                'error_code': 'user_not_found'
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                'message': 'Token is invalid or expired',
                'resolution': 'Please get new token',
                'error_code': 'invalid_token'
            },
        ),
    )
    app.add_exception_handler(
        PasswordIncorrect,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                'message': 'Password is not correct',
                'error_code': 'password_incorrect'
            },
        ),
    )
    app.add_exception_handler(
        PasswordNotMatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                'message': 'Password do not match',
                'error_code': 'password_do_not_match'
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                'message': 'Please provide a valid access token',
                'resolution': 'Please get an access token',
                'error_code': 'access_token_required'
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                'message': 'Please provide a valid refresh token',
                'resolution': 'Please get an refresh token',
                'error_code': 'refresh_token_required'
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                'message': 'Token is invalid Or expired',
                'resolution': 'Please get new token',
                'error_code': 'invalid_token'
            },
        ),
    )
    app.add_exception_handler(
        InvalidScheme,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                'message': 'Token scheme is invalid',
                'resolution': 'Please get new token',
                'error_code': 'invalid_scheme'
            },
        ),
    )
    app.add_exception_handler(
        BlogNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                'message': 'Blog not found',
                'error_code': 'blog_not_found'
            },
        ),
    )
    app.add_exception_handler(
        BlogAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                'message': 'Blog with this slug already exists',
                'error_code': 'blog_exists'
            },
        ),
    )
    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                'message': 'Review not found',
                'error_code': 'review_not_found'
            },
        ),
    )
    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                'message': 'Tag not found',
                'error_code': 'tag_not_found'
            },
        ),
    )
    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                'message': 'Tag with this title already exists',
                'error_code': 'tag_exists'
            },
        ),
    )
    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
