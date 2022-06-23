from pydantic import BaseModel, conint, root_validator


class CreateDateSchema(BaseModel):
    month: conint(ge=1, le=12)
    day: conint(ge=1, le=31)

    @root_validator()
    def validate_date(cls, values: dict) -> dict:
        if values.get("day") > {
            1: 31,
            2: 29,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }.get(values.get("month")):
            raise ValueError("Day is out of range.")
        return values


class DateSchema(BaseModel):
    id: int
    month: int
    day: int
    fact: str

    class Config:
        orm_mode = True

    @root_validator()
    def change_month_to_string(cls, values):
        values["month"] = {
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
        }.get(values.get("month"))
        return values


class PopularMonthSchema(BaseModel):
    id: int
    month: int
    days_checked: int

    class Config:
        orm_mode = True

    @root_validator()
    def change_month_to_string(cls, values):
        values["month"] = {
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
        }.get(values.get("month"))
        return values
