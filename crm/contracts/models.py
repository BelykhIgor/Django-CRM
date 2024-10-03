from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from products.models import Products


class Contracts(models.Model):
    """
    Модель контракта.

    Эта модель описывает контракт между компанией и клиентом, включая
    информацию о предоставляемых услугах, дате заключения, сроках действия
    контракта, сумме и менеджере, который отвечает за контракт.

    Атрибуты:
        title (str): Название контракта.
        service_provided (ForeignKey): Услуга, представленная в контракте (Products).
        file (FileField): Файл контракта.
        date (DateTimeField): Дата заключения контракта (автоматически устанавливается).
        start_date (DateField): Дата начала действия контракта.
        end_date (DateField): Дата окончания действия контракта.
        amount (DecimalField): Сумма контракта.
        manager (ForeignKey): Менеджер, ответственный за контракт (User).

    Методы:
        __str__(): Возвращает строковое представление контракта, включающее
                    название контракта и предоставляемую услугу.
    """
    title = models.CharField(max_length=25, null=False, blank=True, verbose_name="Название")
    service_provided = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name="Представляемая услуга"
    )
    file = models.FileField(upload_to='uploaded_files/')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заключения контракта')
    start_date = models.DateField(verbose_name="Дата начала действия контракта", default=timezone.now)
    end_date = models.DateField(verbose_name="Дата окончания действия контракта", default=timezone.now)
    amount = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=('Сумма'))
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Менеджер")

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    def __str__(self):
        return f'{self.title}, {self.service_provided}'
