from django.db import models
from django.utils.translation import gettext_lazy as _


class Products(models.Model):
    """
    Модель для представления продукта или услуги.

    Атрибуты:
        title (CharField): Наименование продукта или услуги. Максимальная длина - 50 символов.
        description (TextField): Описание продукта или услуги. Поле индекcируется в базе данных.
        price (DecimalField): Цена продукта или услуги. Максимум 8 цифр, 2 из них после запятой.

    Методы:
        description_short: Возвращает короткую версию описания (не более 48 символов).
        __str__: Возвращает строковое представление продукта (название).
    """
    title = models.CharField(max_length=50, null=False, blank=True, verbose_name="Наименование")
    description = models.TextField(null=False, blank=True, verbose_name=('Описание'), db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_('Цена'))

    @property
    def description_short(self) -> str:
        """
        Возвращает короткую версию описания (до 48 символов). Если описание короче 48 символов,
        возвращается полное описание.

        Returns:
            str: Сокращённая версия описания, если оно длиннее 48 символов.
        """
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + "..."

    def __str__(self):
        """
        Возвращает строковое представление продукта, которое отображает его название.

        Returns:
            str: Название продукта.
        """
        return f'{self.title}'

    class Meta:
        verbose_name_plural = "Продукты и услуги"
