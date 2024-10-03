from django.core.validators import RegexValidator
from django.db import models

from ads.models import Ads


class Leads(models.Model):
    """
    Модель Lead (Потенциальный клиент).

    Эта модель представляет потенциального клиента с следующими полями:

    Атрибуты:
        first_name (CharField): Имя клиента. Валидируется на наличие только русских или английских букв.
        last_name (CharField): Фамилия клиента. Валидируется на наличие только русских или английских букв.
        phone_number (CharField): Номер телефона клиента. Должен содержать от 8 до 11 цифр и соответствовать формату '+999999999'.
        email (EmailField): Уникальный адрес электронной почты клиента.
        promotion_channel (ForeignKey): Ссылка на рекламную кампанию, через которую был привлечен клиент.

    Методы:
        __str__: Возвращает строковое представление клиента в формате "Имя Фамилия".
        """
    name_validator = RegexValidator(
        regex=r'^[а-яА-ЯёЁa-zA-Z]+$',
        message='Имя может содержать только русские или английские буквы.'
    )
    first_name = models.CharField(
        max_length=50,
        validators=[name_validator],
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50,
        validators=[name_validator],
        verbose_name="Фамилия"
    )

    phone_number = models.CharField(
        max_length=14,
        validators=[RegexValidator(regex=r'^\+7[(]\d{3}[)]\d{7}$',
                                   message="Номер телефона должен быть в формате: +7(921)6543210. Допустимо до 14 цифр.")],
        verbose_name="Номер телефона"
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Электронная почта"
    )

    promotion_channel = models.ForeignKey(
        Ads,
        on_delete=models.CASCADE,
        verbose_name="Название рекламной кампании",
        null=False,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Потенциальные клиенты"