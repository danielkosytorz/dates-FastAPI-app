import os
import random

import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from src.dates.models import Date, PopularMonth


def change_month_to_string(month):
    return {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }.get(month)


@pytest.mark.asyncio
async def test_create_date_with_valid_data(async_client: AsyncClient, mocker):
    mocker.patch(
        "src.dates.services.services.DateService.get_fact", return_value="Test Fact"
    )

    response = await async_client.post("/dates/", json={"month": 1, "day": 1})

    assert response.status_code == 200
    assert await Date.all().count() == 1
    date = await Date.first()
    assert response.json() == {
        "id": date.id,
        "month": change_month_to_string(date.month),
        "day": date.day,
        "fact": date.fact,
    }


@pytest.mark.asyncio
async def test_create_date_raise_HTTPException(async_client: AsyncClient, mocker):
    mocker.patch(
        "src.dates.services.services.DateService.get_fact",
        side_effect=HTTPException(status_code=400, detail="Numbers API error."),
    )

    response = await async_client.post("/dates/", json={"month": 1, "day": 1})

    assert response.status_code == 400
    assert response.json() == {"detail": "Numbers API error."}


@pytest.mark.asyncio
async def test_create_date_with_invalid_data(async_client: AsyncClient, mocker):
    mocker.patch(
        "src.dates.services.services.DateService.get_fact", return_value="Test Fact"
    )

    response = await async_client.post("/dates/", json={"month": 13, "day": 32})

    assert response.status_code == 422
    assert await Date.all().count() == 0
    assert (
        response.json().get("detail")[0].get("msg")
        == "ensure this value is less than or equal to 12"
    )


@pytest.mark.asyncio
async def test_create_date_with_invalid_days_in_month(
    async_client: AsyncClient, mocker
):
    mocker.patch(
        "src.dates.services.services.DateService.get_fact", return_value="Test Fact"
    )

    response = await async_client.post("/dates/", json={"month": 2, "day": 30})

    assert response.status_code == 422
    assert await Date.all().count() == 0
    assert response.json().get("detail")[0].get("msg") == "Day is out of range."


@pytest.mark.asyncio
async def test_create_date_for_already_existing_day_and_month(
    async_client: AsyncClient, mocker
):
    date = await Date.create(month=10, day=5, fact="Fact for 10/5")
    mocker.patch(
        "src.dates.services.services.DateService.get_fact", return_value="Test Fact"
    )

    response = await async_client.post(
        "/dates/", json={"month": date.month, "day": date.day}
    )

    assert response.status_code == 200
    assert await Date.all().count() == 1
    date = await Date.first()
    assert date.fact == "Test Fact"
    assert response.json() == {
        "id": date.id,
        "month": change_month_to_string(date.month),
        "day": date.day,
        "fact": date.fact,
    }


@pytest.mark.asyncio
async def test_delete_date_without_api_key(async_client: AsyncClient):
    date = await Date.create(month=10, day=5, fact="Fact for 10/5")
    response = await async_client.delete(f"/dates/{date.id}")

    assert response.status_code == 401
    assert await Date.all().count() == 1
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.asyncio
async def test_delete_date_with_invalid_id(async_client: AsyncClient):
    date = await Date.create(month=10, day=5, fact="Fact for 10/5")
    response = await async_client.delete(
        f"/dates/999", headers={"X-API-KEY": os.getenv("X_API_KEY")}
    )

    assert response.status_code == 404
    assert await Date.all().count() == 1
    assert response.json() == {"detail": "Date not found."}


@pytest.mark.asyncio
async def test_delete_date_with_valid_id(async_client: AsyncClient):
    date = await Date.create(month=10, day=5, fact="Fact for 10/5")
    response = await async_client.delete(
        f"/dates/{date.id}", headers={"X-API-KEY": os.getenv("X_API_KEY")}
    )

    assert response.status_code == 204
    assert await Date.all().count() == 0


@pytest.mark.asyncio
async def test_get_list_of_dates(async_client: AsyncClient):
    date_1 = await Date.create(month=10, day=5, fact="Fact for 10/5")
    date_2 = await Date.create(month=10, day=6, fact="Fact for 10/6")

    response = await async_client.get("/dates/")

    assert response.status_code == 200
    assert await Date.all().count() == 2
    assert response.json() == [
        {
            "id": date_1.id,
            "month": change_month_to_string(date_1.month),
            "day": date_1.day,
            "fact": date_1.fact,
        },
        {
            "id": date_2.id,
            "month": change_month_to_string(date_2.month),
            "day": date_2.day,
            "fact": date_2.fact,
        },
    ]


@pytest.mark.asyncio
async def test_get_list_of_popular_months(async_client: AsyncClient):
    dates = [
        await Date.create(month=i, day=j, fact=f"Fact for {i}/{j}")
        for i in range(1, 13)
        for j in range(1, random.randint(2, 10))
    ]

    response = await async_client.get("/popular/")

    assert response.status_code == 200
    assert await Date.all().count() == len(dates)
    assert response.json() == [
        {
            "id": popular_month.id,
            "month": change_month_to_string(popular_month.month),
            "days_checked": popular_month.days_checked,
        }
        for popular_month in await PopularMonth.all().order_by("-days_checked")
    ]
