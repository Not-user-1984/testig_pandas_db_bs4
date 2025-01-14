from fastapi import FastAPI
from infrastructure.repositories.trading_repository_impl import TradingRepositoryImpl
from domain.services.trading_service import TradingService
from application.services.trading_app_service import TradingAppService
from application.api.endpoints.trading import router as trading_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="SPIMEX Trading Results API",
        description="API for accessing SPIMEX trading results",
        docs_url="/api/docs",
        debug=True,
    )

    trading_repository = TradingRepositoryImpl()
    trading_service = TradingService(trading_repository)
    trading_app_service = TradingAppService(trading_service)

    app.include_router(trading_router, prefix="/api/v1")

    app.dependency_overrides[TradingAppService] = lambda: trading_app_service

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
