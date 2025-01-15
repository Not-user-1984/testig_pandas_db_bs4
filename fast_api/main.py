from fastapi import FastAPI
from api.v1.endpoints.trading import router as trading_router
from core.cache import schedule_cache_reset


def create_app() -> FastAPI:
    app = FastAPI(
        title="SPIMEX Trading Results API",
        description="API for accessing SPIMEX trading results",
        docs_url="/api/docs",
        debug=True,
    )
    app.include_router(trading_router, prefix="/api")

    @app.on_event("startup")
    async def startup():
        schedule_cache_reset()
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
