import os
from typing import List, Union

from fastapi import APIRouter, Header, HTTPException
from starlette.responses import Response

from src.dates.models import Date, PopularMonth
from src.dates.schemas.schemas import CreateDateSchema, DateSchema, PopularMonthSchema
from src.dates.services.services import DateService

dates = APIRouter(prefix="/dates")
popular = APIRouter(prefix="/popular")


@dates.get("/")
async def get_dates() -> List[DateSchema]:
    return [DateSchema.from_orm(date) for date in await Date.all()]


@dates.post("/")
async def create_or_update_date(request: CreateDateSchema) -> DateSchema:
    return DateSchema.from_orm(await DateService.create_or_update_date(request=request))


@dates.delete("/{date_id}")
async def delete_date(date_id: int, x_api_key: Union[str, None] = Header(default=None)):
    if x_api_key != os.getenv("X_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    await DateService.delete_date(date_id=date_id)
    return Response(status_code=204)


@popular.get("/")
async def get_popular_months() -> List[PopularMonthSchema]:
    await DateService.create_or_update_popular_month()
    return [
        PopularMonthSchema.from_orm(date)
        for date in await PopularMonth.all().order_by("-days_checked")
    ]
