from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Products


class Ads(models.Model):
    """
    Модель Ads представляет маркетинговую кампанию.

    Атрибуты:
    ----------
    title : str
        Наименование рекламной кампании (не может быть пустым).

    advertised_service : Products
        Связанная услуга, которая рекламируется (связь через OneToOneField с моделью Products).

    promotion_channel : str
        Канал продвижения, используемый для рекламной кампании (например, социальные сети, ТВ и т.д.).

    advertising_budget : Decimal
        Бюджет, выделенный на рекламу. Максимальная сумма — 999999.99.

    Методы:
    -------
    __str__():
        Возвращает строковое представление рекламной кампании (title).
    """

    title = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        verbose_name="Наименование",
    )
    advertised_service = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        verbose_name="Представляемая услуга",
    )
    promotion_channel = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        verbose_name="Канал продвижения",
    )
    advertising_budget = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        verbose_name=('Рекламный бюджет')
    )

    def __str__(self):
        """
        Возвращает строковое представление объекта Ads.

        Returns:
        --------
        str:
            Название рекламной кампании.
        """
        return f'{self.title}'

    class Meta:
        verbose_name_plural = "Маркетинг"
