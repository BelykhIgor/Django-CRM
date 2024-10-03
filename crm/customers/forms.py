from django import forms

from customers.models import Customers


class CustomersCreateForm(forms.ModelForm):
    """
    Форма для создания или редактирования клиента (Customers).

    Эта форма предоставляет возможность связать клиента с потенциальным клиентом (Lead)
    и контрактом (Contract).

    Атрибуты:
       model (Customers): Модель, с которой работает форма.
       fields (tuple): Список полей, включенных в форму:
           - lead: Потенциальный клиент (Leads), который будет преобразован в клиента.
           - contract: Контракт (Contracts), который связан с данным клиентом.

    Методы:
       Meta: Определяет метаданные для формы, включая модель и список полей.
    """
    class Meta:
        model = Customers
        fields = "lead", "contract"