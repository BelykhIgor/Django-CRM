from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    name_validator = RegexValidator(
        regex=r'^[а-яА-ЯёЁa-zA-Z]+$',
        message='Имя может содержать только русские или английские буквы.'
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, validators=[name_validator], verbose_name="Имя")
    last_name = models.CharField(max_length=50, validators=[name_validator], verbose_name="Фамилия")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    email = models.EmailField(blank=True, verbose_name="Почта")

    def __str__(self):
        return self.user.username
