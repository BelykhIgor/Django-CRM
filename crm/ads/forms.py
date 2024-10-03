from django import forms

from ads.models import Ads
from products.models import Products


class CreateAdsForm(forms.ModelForm):
    """
    Форма для создания и редактирования рекламных кампаний (Ads).
    Поля включают наименование, услугу, канал продвижения и рекламный бюджет.
    """

    advertised_service = forms.ModelChoiceField(
        queryset=Products.objects.all(),
        label="Выберите продукт",
        empty_label = 'Выберите продукт',
    )
    class Meta:
        model = Ads
        fields = ["title", "advertised_service", "promotion_channel", "advertising_budget"]

    def __init__(self, *args, **kwargs):
        """
        Переопределяем метод инициализации формы, чтобы гарантировать доступ к полю 'advertised_service'
        и корректное отображение списка продуктов.
        """
        super(CreateAdsForm, self).__init__(*args, **kwargs)
        self.fields['advertised_service'].queryset = Products.objects.all()