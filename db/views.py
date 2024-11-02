from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import RAPN
from .SearchModel import SearchForm
from django.db import IntegrityError
from django.apps import apps
import inspect
import importlib
import logging
import csv
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Inserimento nuovo paziente
@login_required
def insert_new(request, database_file, form):
    errore = None
    # if this is a POST request we need to process the form data
    # Dobbiamo ottenere il form dal file corretto
    # Questo mi da il nome dell'app: __package__.split(".")[0]

    # Con questa funzione importiamo il file giusto
    library = importlib.import_module(f"{__package__.split('.')[0]}.{database_file}")
    # Con questa funzione otteniamo il form giusto dal file
    class_form = getattr(library, form, None)

    if request.method == "POST":
        # Popoliamo utilizzando il form dell'anagrafica
        url_form = class_form(request.POST)
        # check whether it's valid:
        if url_form.is_valid():
            try:
                lowercasing = url_form.save(commit=False)
                lowercasing.anagraphicSurname = lowercasing.anagraphicSurname.lower()
                lowercasing.anagraphicName = lowercasing.anagraphicName.lower()
                lowercasing.save()
                return redirect("success")
            except IntegrityError as e:
                # Errore nei constraint
                print(f"IntegrityError while saving patient: {e}")
                return render(
                    request,
                    "forms/insert_patient.html",
                    {
                        "form": url_form,
                        "page_title": "New patient - " + database_file,
                        "incoming_url": request.resolver_match.url_name,
                        "errore": "Patient already in the database",
                    },
                )

        # if a GET (or any other method) we'll create a blank form
    else:
        url_form = class_form()

    return render(
        request,
        "forms/insert_patient.html",
        {
            "form": url_form,
            "page_title": "New patient - " + database_file,
            "incoming_url": request.resolver_match.url_name,
        },
    )


# Ricerca del paziente
@login_required
def search_patient(request, database, phase):
    pk_patient = None
    error = None
    print(database)
    # Carichiamo il database/modello
    url_database = apps.get_model(
        __package__.split(".")[0], database
    )  # Il primo campo è il nome dell'app

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                persona = url_database.objects.get(
                    anagraphicName=form.cleaned_data["name"].lower(),
                    anagraphicSurname=form.cleaned_data["surname"].lower(),
                    anagraphicBirthdate=form.cleaned_data["birthdate"],
                )  # Importante cercare nella tabella giusta
                print(persona.pk)
                print("Redirecting to edit_patient")
                return redirect(
                    "edit_patient",
                    pk=persona.pk,
                    edit_phase=phase,
                    database_file=database,
                )
            except url_database.DoesNotExist:
                error = "Patient not found in the database"

    else:
        form = SearchForm()

    return render(
        request,
        "forms/search_patient.html",
        {
            "form": form,
            "page_title": "Search patient - " + database,
            "pk_persona": pk_patient,
            "errore": error,
            "incoming_url": request.resolver_match.url_name,
        },
    )


# Modifica dei dati del paziente
@login_required
def edit_patient(request, database_file, edit_phase, pk):
    # ATTENZIONE: il nome del FILE ED IL NOME DEL MODELLO DEVONO ESSERE UGUALI
    print("Siamo nella modifica dei dati")

    # phase è il nome del form
    # Con questa funzione importiamo il file giusto
    library = importlib.import_module(f"{__package__.split('.')[0]}.{database_file}")
    # Con questa funzione otteniamo il form giusto dal file
    parsed_form = getattr(library, edit_phase, None)

    # Otteniamo il modello di database
    url_database = apps.get_model(
        __package__.split(".")[0], database_file
    )  # Il primo campo è il nome dell'app

    # otteniamo i dati della persona dal database e dalla posizione
    persona = get_object_or_404(url_database, pk=pk)

    if request.method == "POST":
        form = parsed_form(request.POST, instance=persona)
        if form.is_valid():
            form.save()  # Salva le modifiche
            return redirect("success")

    else:
        form = parsed_form(instance=persona)

    # Descrizione dettagliata del form, se c'è
    extracted_page_title = (
        form.get_description if hasattr(form, "get_description") else edit_phase
    )

    return render(
        request,
        "forms/edit_patient.html",
        {
            "form": form,
            "page_title": extracted_page_title,
            "name": persona.anagraphicName,
            "surname": persona.anagraphicSurname,
            "birthdate": persona.anagraphicBirthdate,
            "id": persona.pk,
        },
    )


# Esportazione in csv della tabella
@login_required
def export_csv(request, database):
    # Step 1: Set up the HTTP response with the appropriate CSV headers
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{database}_{datetime.today().strftime("%Y-%m-%d")}.csv"'
    )

    # Step 2: Create a CSV writer
    writer = csv.writer(response)

    # Step 3: Get all field names from MyModel dynamically
    url_database = apps.get_model(
        __package__.split(".")[0], database
    )  # Il primo campo è il nome dell'app
    field_names = [field.name for field in url_database._meta.fields]

    # Step 4: Write the header row with all field names
    writer.writerow(field_names)

    # Step 5: Query all rows and fetch values for each field
    data = url_database.objects.all().values_list(*field_names)

    # Step 6: Write each row of data to the CSV
    for row in data:
        writer.writerow(row)

    # Step 7: Return the response
    return response
