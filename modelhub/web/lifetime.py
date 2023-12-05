from typing import Awaitable, Callable

from fastapi import FastAPI
from fastapi_restful.tasks import repeat_every

from modelhub.core.predictions.ai_models.xgboost import XGBoostModel
from modelhub.core.predictions.trainer import Trainer


def register_startup_event(
    app: FastAPI,
):  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        app.middleware_stack = app.build_middleware_stack()
        pass  # noqa: WPS420

    @app.on_event("startup")
    @repeat_every(seconds=604800)  # 1 week
    def _retrain_models() -> None:
        """
        Retrain models and add a .pickle file to Azure Blob Storage
        """
        print("Queue is working")
        xgboost = XGBoostModel()
        # isolation_forest = IsolationForestModel()
        trainer = Trainer([xgboost])
        print("Created models, training...")
        trainer.train()
        # trainer.evaluate() TODO: create logs and send them somewhere
        print("Models have been retrained")

    return _startup, _retrain_models


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        pass  # noqa: WPS420

    return _shutdown
