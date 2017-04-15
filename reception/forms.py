from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from reception.models import Reception


class ReceptionForm(forms.ModelForm):
    """"Форма карточки записи на прием к врачу."""

    class Meta:
        model = Reception
        fields = '__all__'

        widgets = {
            'date': DateTimePicker(
                options={
                    "format": "DD.MM.YY",
                }),
        }
