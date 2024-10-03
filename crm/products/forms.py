from django import forms

from products.models import Products


class CreateProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продукта.

    Эта форма использует модель `Products` и включает следующие поля:
    - title: Название продукта.
    - description: Описание продукта.
    - price: Цена продукта.

    Класс Meta:
        model (Products): Модель, на основе которой создается форма.
        fields (list): Поля модели, которые будут отображаться в форме.
    """

    class Meta:
        model = Products
        fields = ['title', 'description', 'price']
