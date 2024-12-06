import datetime
from optparse import Option

from django.db import models

# Create your models here.
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import APIException, ValidationError


class Instrument(models.Model):
    """Список поддерживаемых инструментов"""

    name = models.CharField(max_length=10, verbose_name=("Название инструмента"))
    quote_currency = models.CharField(max_length=10, verbose_name=("Валюта котировки"))
    lot = models.FloatField(verbose_name=("Минимальный размер лота"))
    tick_size = models.FloatField(verbose_name=("Минимальное изменения цены"))
    taker_commission = models.FloatField(null=True, verbose_name=("Коммиссия текера"))
    maker_commission = models.FloatField(null=True, verbose_name=("Коммиссия мекера"))

    class Meta:
        verbose_name = "Инструменты"
        verbose_name_plural = "Инструменты"


class Platform(models.Model):
    """Список поддерживаемых бирж"""

    name = models.CharField(max_length=20, verbose_name=("Название биржи"))
    url = models.CharField(null=True, max_length=200, verbose_name=("Адрес"))
    trade_session_start = models.TimeField(default=datetime.time(00, 00), verbose_name=("Начало торговой сессии"))
    trade_session_stop = models.TimeField(default=datetime.time(23, 59), verbose_name=("Окончание торговой сессии"))


class InstrumentPlatform(models.Model):
    """M2M модель бирж и инструментов"""

    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
    )

    # def __str__(self):
    #     return self.id

    class Meta:
        db_table = "api_instrument_platform"
        verbose_name = "Связь инструмента и биржи"
        verbose_name_plural = "Связь инструмента и биржи"

class Manager(models.Model):
    """Настройки"""

    instrument_platform = models.ForeignKey(InstrumentPlatform,
                                            verbose_name=("Связки платформы и инструмента"),
                                            on_delete=models.CASCADE)
    order_spread = models.FloatField(verbose_name=("Спред"))
    order_step = models.FloatField(verbose_name=("Шаг сетки"))
    start_step = models.FloatField(verbose_name=("Шаг первой позиции"))
    order_size = models.FloatField(verbose_name=("Размер ордера"))
    grid_depth = models.FloatField(verbose_name=("Максимальная допустимая глубина"))
    grid_side = models.FloatField(verbose_name=("Направление открытия сделки"))
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        manager = Manager.objects.filter(user=self.user, instrument_platform=self.instrument_platform_id).first()
        if manager:
            raise ValidationError(f'Для инструмента {self.instrument_platform_id} уже есть manager/{manager.id}/')
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    # def __str__(self):
    #     return str(self.instrument_platform)

    class Meta:
        verbose_name = "Боты"
        verbose_name_plural = "Боты"


class Trade(models.Model):
    """Сделки"""

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    price = models.FloatField()
    size_orig = models.FloatField()
    size = models.FloatField()
    side = models.CharField(max_length=10)
    fee = models.FloatField()
    trade_id = models.IntegerField()
    timestamp = models.IntegerField()

    def __str__(self):
        return f'{self.trade_id}'

    class Meta:
        verbose_name = "Сделки"
        verbose_name_plural = "Сделки"


# class Trade(Updateable, db.Model):
#     __tablename__ = "trades"
#
#     id = sqla.Column(sqla.Integer, primary_key=True)
#     price = sqla.Column(sqla.Float)
#     size_orig = sqla.Column(sqla.Float)
#     size = sqla.Column(sqla.Float)
#     side = sqla.Column(sqla.String(8))
#     fee = sqla.Column(sqla.Float)
#     fee_currency = sqla.Column(sqla.String())
#     trade_id = sqla.Column(sqla.Integer, unique=True)
#     timestamp = sqla.Column(sqla.BigInteger)
#     manager_id = sqla.Column(sqla.Integer, sqla.ForeignKey("managers.id"), index=True)
#
#     manager = sqla_orm.relationship("Manager", back_populates="trade")
#
#     def __repr__(self):  # pragma: no cover
#         return f"{self.trade_id} {self.price}@{self.size} {self.side}"