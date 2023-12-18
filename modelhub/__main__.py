import logging

import uvicorn

from modelhub.gunicorn_runner import GunicornApplication
from modelhub.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    logging.basicConfig(level=logging.INFO)
    if settings.reload:
        uvicorn.run(
            "modelhub.web.application:get_app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            factory=True,
            log_level="info",
        )
    else:
        # We choose gunicorn only if reload
        # option is not used, because reload
        # feature doesn't work with Uvicorn workers.
        GunicornApplication(
            "modelhub.web.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            access_log_format='%r "-" %s "-" %Tf',  # noqa: WPS323
        ).run()


if __name__ == "__main__":
    main()
