from tortoise import fields
from tortoise.models import Model
from tortoise.validators import MinValueValidator, MaxValueValidator


class Date(Model):
    month = fields.IntField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = fields.IntField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    fact = fields.CharField(max_length=300)

    class Meta:
        unique_together = ("month", "day")


class PopularMonth(Model):
    month = fields.IntField(
        validators=[MinValueValidator(1), MaxValueValidator(12)], unique=True
    )
    days_checked = fields.IntField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(31)]
    )
