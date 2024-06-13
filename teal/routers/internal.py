import logging

from fastapi import APIRouter

from teal.core import is_feature_enabled
from teal.core.internal import AppAdapter
from teal.model.internal import HealthCheck, AppInfo

router = APIRouter(prefix="/app", tags=["app"])
_logger = logging.getLogger("teal.routers.internal")


# router.route_class = CheckUnknownQueryParamsRouter

if is_feature_enabled("TEAL_ROUTE_APP_HEALTH"):
    _logger.info("feature app health is enabled")

    @router.get(
        "/health",
        summary="Health Check",
        response_model=HealthCheck,
    )
    def get_health() -> HealthCheck:
        app = AppAdapter()
        return app.get_health_check()


if is_feature_enabled("TEAL_ROUTE_APP_INFO"):
    _logger.info("feature app info is enabled")

    @router.get(
        "/info",
        summary="Application information's",
        response_model=AppInfo,
    )
    def get_health() -> AppInfo:
        app = AppAdapter()
        return app.get_app_info()
