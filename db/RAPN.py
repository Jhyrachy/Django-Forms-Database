from django.db import models
from django.forms import ModelForm, DateInput

# Sezione per le strutture dell'autocompletamento
GENDER = [
    ("F", "Female"),
    ("M", "Male"),
]
ETHNICITY = [
    ("Caucasian", "Caucasian"),
    ("Asian", "Asian"),
    ("African", "African"),
    ("Other", "Other"),
]


# Modello di database
class RAPN(models.Model):
    class Meta:
        # Controllo sull'unicità del paziente
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "anagraphicSurname",
                    "anagraphicName",
                    "anagraphicBirthdate",
                ],
                name="unique_patient",
            )
        ]

    # Scheda anagrafica
    anagraphicSurname = models.CharField(
        max_length=50,
        verbose_name="Surname",
        help_text="<i>Patient Surname</i><br>",
    )
    anagraphicName = models.CharField(
        max_length=50,
        verbose_name="Name",
        help_text="<i>Patient name</i><br>",
    )
    anagraphicBirthdate = models.DateField(
        verbose_name="Birthdate", help_text="Patient birthdate<br>"
    )
    anagraphicGender = models.CharField(
        max_length=10,
        choices=GENDER,
        verbose_name="Gender",
        help_text="Patient gender<br>",
    )

    # Anamnesi preoperatoria
    anamnesisEthnicity = models.CharField(
        max_length=50,
        choices=ETHNICITY,
        verbose_name="Ethnicity",
        help_text="Patient ethnicity<br>",
        null=True,
        blank=True,
    )
    anamnesisWeight = models.IntegerField(
        verbose_name="Weight",
        help_text="Patient weight in Kg<br>",
        null=True,
        blank=True,
    )
    anamnesisHeight = models.IntegerField(
        verbose_name="Height",
        help_text="Patient height in cm<br>",
        null=True,
        blank=True,
    )


##Inizio dei form


# Scheda anagrafica
class rapn_ana(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}


# Anamnsi preoperatoria
class rapn_preop(ModelForm):
    def get_description(self):
        return "Preoperative anamnesis of RAPN"

    class Meta:
        model = RAPN
        fields = [
            "anamnesisEthnicity",
            "anamnesisWeight",
            "anamnesisHeight",
        ]


class rapn_lesion_1(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}


class rapn_lesion_2(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}


class rapn_intraop(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}


class rapn_postop_1(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}


class rapn_postop_2(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}


class rapn_histology(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}


class rapn_followup(ModelForm):
    class Meta:
        model = RAPN
        fields = [
            "anagraphicSurname",
            "anagraphicName",
            "anagraphicBirthdate",
            "anagraphicGender",
        ]
        widgets = {"anagraphicBirthdate": DateInput(attrs={"type": "date"})}
