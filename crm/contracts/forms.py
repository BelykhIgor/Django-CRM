from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from contracts.models import Contracts


class ContractCreateForm(forms.ModelForm):
    """
    Форма для создания нового контракта.

    Эта форма позволяет пользователю вводить информацию о контракте, включая
    название контракта, предоставляемую услугу, файл, даты начала и окончания
    контракта, а также сумму.

    Поля формы:
        title (str): Название контракта.
        service_provided (ForeignKey): Услуга, представленная в контракте (Products).
        file (FileField): Файл контракта, загружаемый пользователем.
        start_date (DateField): Дата начала действия контракта.
        end_date (DateField): Дата окончания действия контракта.
        amount (DecimalField): Сумма контракта.

    Методы:
        Meta: Определяет модель, с которой связана форма, и поля, которые будут включены.
    """
    start_date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Дата начала контракта"
    )
    end_date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Дата окончания контракта"
    )
    class Meta:
        model = Contracts
        fields = "title", "service_provided", "file", "start_date", "end_date", "amount"

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Проверка, что дата начала не меньше текущей даты
        if start_date and start_date < timezone.now().date():
            raise ValidationError("Дата начала контракта не может быть в прошлом.")

        # Проверка, что дата окончания не меньше даты начала
        if start_date and end_date and end_date < start_date:
            raise ValidationError("Дата окончания не может быть раньше даты начала.")

        # Проверка, что контракт не менее 30 дней
        if start_date and end_date and (end_date - start_date).days < 30:
            raise ValidationError("Контракт должен быть действителен минимум 30 дней.")

        return cleaned_data