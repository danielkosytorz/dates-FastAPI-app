import os

APP_MODELS = {"dates": ["src.dates.models"]}

app_models_dict = {
    app: {"models": models, "default_connection": "default"}
    for app, models in APP_MODELS.items()
}

app_models_dict["models"] = {
    "models": ["aerich.models"],
    "default_connection": "default",
}

TORTOISE_ORM = {
    "connections": {
        "default": (
            f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
    },
    "apps": app_models_dict,
}
