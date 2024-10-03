from django.db import models

from contracts.models import Contracts
from leads.models import Leads


class Customers(models.Model):
    """
    Модель представляет клиента (Customers), который был преобразован из потенциального клиента (Lead)
    и имеет контракт с компанией.

    Атрибуты:
        lead (OneToOneField): Связь один-к-одному с моделью Leads.
        Определяет, какой потенциальный клиент был преобразован в данного клиента.

        contract (OneToOneField): Связь один-к-одному с моделью Contracts.
        Определяет контракт, связанный с данным клиентом.
    """
    lead = models.OneToOneField(Leads, on_delete=models.CASCADE, verbose_name="Потенциальный клиент")
    contract = models.OneToOneField(Contracts, on_delete=models.CASCADE, verbose_name="Контракт")

    class Meta:
        verbose_name_plural = "Активные клиенты"


