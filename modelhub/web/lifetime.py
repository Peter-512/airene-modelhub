from typing import Awaitable, Callable

from fastapi import FastAPI
from fastapi_restful.tasks import repeat_every

from modelhub.core.predictions.ai_models.xgboost import XGBoostRegressorModel
from modelhub.core.predictions.ai_models.xgboost_classifier import (
    XGBoostClassifierModel,
)
from modelhub.core.predictions.predictor import Predictor
from modelhub.core.predictions.trainer import Trainer
from modelhub.services.busservice import BusServiceAccessPoint
from modelhub.static.utils import format_predictions_for_queue


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
        xgboost = XGBoostRegressorModel()
        xgboost_classifier = XGBoostClassifierModel()
        trainer = Trainer([xgboost, xgboost_classifier])
        trainer.train()
        print("Models retrained")

    @app.on_event("startup")
    @repeat_every(seconds=600)  # 10 minutes
    async def _listen_to_queue() -> None:
        """
        Listen to the queue and predict values
        """
        bus_service_ap = BusServiceAccessPoint()
        predictor = Predictor()
        # TODO: 50 is a test number so the queue doesn't explode
        aggregated_messages = await bus_service_ap.receive_messages(n=50)
        predictions = predictor.predict_batch(aggregated_messages)
        formatted_predictions = format_predictions_for_queue(
            predictions,
            aggregated_messages,
        )
        await bus_service_ap.send_messages(formatted_predictions)

    return _startup, _listen_to_queue, _retrain_models


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
