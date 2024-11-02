from django.db import models
from django.forms import ModelForm, DateInput


class SearchFields(models.Model):
    surname = models.CharField(verbose_name="Surname", max_length=100)
    name = models.CharField(verbose_name="Name", max_length=100)
    birthdate = models.DateField(verbose_name="Birthdate")


# Classe per la ricerca
class SearchForm(ModelForm):
    class Meta:
        model = SearchFields
        fields = "__all__"
        widgets = {"birthdate": DateInput(attrs={"type": "date"})}
