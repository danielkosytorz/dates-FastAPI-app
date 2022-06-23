from typing import List, Union

import requests
from fastapi import HTTPException
from tortoise.functions import Count

from src.dates.models import Date, PopularMonth
from src.dates.schemas.schemas import CreateDateSchema


class DateService:
    NUMBERS_API_BASE_URL = "http://numbersapi.com/"

    @classmethod
    async def create_or_update_date(cls, request: CreateDateSchema) -> Date:
        if (
            date := await Date.filter(day=request.day, month=request.month).first()
        ) is not None:
            await cls.update_date_fact(date=date)
            return date

        return await Date.create(
            month=request.month,
            day=request.day,
            fact=cls.get_fact(month=request.month, day=request.day),
        )

    @classmethod
    def get_fact(cls, day: int, month: int) -> str:
        response = requests.get(url=f"{cls.NUMBERS_API_BASE_URL}{month}/{day}/date")
        if not response.ok:
            raise HTTPException(status_code=400, detail="Numbers API error.")
        return response.text

    @classmethod
    async def update_date_fact(cls, date: Date) -> None:
        date.fact = cls.get_fact(day=date.day, month=date.month)
        await date.save()

    @classmethod
    async def delete_date(cls, date_id: int) -> None:
        if (date := await Date.filter(id=date_id).first()) is None:
            raise HTTPException(status_code=404, detail="Date not found.")
        await date.delete()

    @classmethod
    async def get_ranking_of_months(cls) -> Union[list[dict], dict]:
        return (
            await Date.all()
            .group_by("month")
            .annotate(days_checked=Count("day"))
            .values("month", "days_checked")
        )

    @classmethod
    async def create_or_update_popular_month(cls) -> None:
        for month in await cls.get_ranking_of_months():
            if (
                popular_month := await PopularMonth.filter(
                    month=month.get("month")
                ).first()
            ) is not None:
                popular_month.days_checked = month.get("days_checked")
                await popular_month.save()
            else:
                await PopularMonth.create(
                    month=month.get("month"), days_checked=month.get("days_checked")
                )
