import logging
from typing import Callable

from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

_logger = logging.getLogger("teal.http")


class CheckUnknownQueryParamsRouter(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        known_params = [param.name for param in self.dependant.query_params]

        async def custom_route_handler(request: Request) -> Response:
            unknown_params = [
                qp for qp in request.query_params if qp not in known_params
            ]

            if any(unknown_params):
                _logger.debug(
                    f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}"
                )
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}",
                )

            return await original_route_handler(request)

        return custom_route_handler


def create_json_response(content, background: BackgroundTask = None):
    return JSONResponse(content=content, background=background)


def create_json_err_response_from_exception(
    ex: Exception, background: BackgroundTask = None
):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"{ex}",
        },
        background=background,
    )


def create_json_err_response(
    code: int, message: str, background: BackgroundTask = None
):
    return JSONResponse(
        status_code=code,
        content={
            "message": message,
        },
        background=background,
    )
