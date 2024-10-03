from django import forms
from django.core.validators import RegexValidator

from leads.models import Leads


class CreateLeadsForm(forms.ModelForm):
    """
    Форма для создания нового потенциального клиента (Leads).

    Эта форма используется для валидации и создания записей потенциальных клиентов в базе данных.

    Атрибуты:
        phone_number (CharField): Поле для ввода номера телефона с валидацией на длину (до 11 цифр)
        и формат (должен соответствовать шаблону номера телефона в формате '+7999332244').

    Класс Meta:
        model (Leads): Модель Leads, на основе которой создается форма.
        fields (tuple): Поля модели, которые будут отображаться в форме и подлежат вводу пользователем:
            - first_name: Имя клиента.
            - last_name: Фамилия клиента.
            - phone_number: Номер телефона клиента с дополнительной валидацией.
            - email: Электронная почта клиента.
            - promotion_channel: Связь с рекламной кампанией, через которую был привлечен клиент.
    """
    phone_number = forms.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\+7[(]\d{3}[)]\d{7}$',
                message="Номер телефона должен быть в формате: '+7(999)332244'."
            )
        ],
        label="Номер телефона",
    )
    class Meta:
        model = Leads
        fields = "first_name", "last_name", "phone_number", "email", "promotion_channel"

