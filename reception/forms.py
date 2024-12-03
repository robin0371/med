from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput

from reception.models import Reception


class ReceptionForm(forms.ModelForm):
    """"Форма карточки записи на прием к врачу."""

    class Meta:
        model = Reception
        fields = '__all__'

        widgets = {
            'date': DatePickerInput(
                options={
                    "format": "DD.MM.YYYY",
                }),
        }
