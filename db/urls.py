from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView  # Template

from . import views

# la home è definita nel file url principale

urlpatterns = [
    # Inserimento nuovo paziente
    path(
        "<str:database_file>/<str:form>/new_patient",
        views.insert_new,
        name="new_patient",
    ),
    # Ricerca paziente
    path(
        "<str:database>/search_patient/<str:phase>",
        views.search_patient,
        name="search_patient",
    ),
    # La ricerca farà redirect alla modifica
    path(
        "<str:database_file>/edit_patient/<str:edit_phase>/<int:pk>",
        views.edit_patient,
        name="edit_patient",
    ),  # Modifica dati
    # Successo dell'inserimento
    path(
        "success",
        TemplateView.as_view(template_name="success.html"),
        name="success",
    ),
    # Esportazione dei dati in csv
    path(
        "<str:database>/export",
        views.export_csv,
        name="export",
    ),
    # Home
    path(
        "", TemplateView.as_view(template_name="db_home.html"), name="db_home"
    ),  # Definizione della home
]
