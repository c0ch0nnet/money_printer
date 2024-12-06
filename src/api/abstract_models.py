from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UUIDAbstractModel(models.Model):
    """Абстрактная модель с PK uuid."""
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name=_("Уникальный ключ записи"),
    )

    class Meta:
        abstract = True


class CreatedAbstractModel(models.Model):
    """Абстрактная модель с датой создания."""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата и время создания"),
    )

    class Meta:
        abstract = True


class UpdatedAbstractModel(models.Model):
    """Абстрактная модель с датой с обновления."""
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата и время обновления"),
    )

    class Meta:
        abstract = True


class AuthorAbstractModel(models.Model):
    """Абстрактная модель с автором."""
    author_uuid = models.UUIDField(null=True, verbose_name=_("UUID автора"))

    class Meta:
        abstract = True


class EditorAbstractModel(models.Model):
    """Абстрактная модель с редактором."""
    editor_uuid = models.UUIDField(null=True, verbose_name=_("UUID редактора"))

    class Meta:
        abstract = True


class BaseAbstractModel(
    UUIDAbstractModel,
    CreatedAbstractModel,
    UpdatedAbstractModel,
    AuthorAbstractModel,
    EditorAbstractModel,
):
    """Абстрактная базовая модель."""

    class Meta:
        abstract = True
