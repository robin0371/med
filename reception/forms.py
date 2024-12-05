from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

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
                }
             ),
             'time': TimePickerInput(
                options={
                    "format": "HH:mm",
                    "enabledHours": [9, 10, 11, 12, 13, 14, 15, 16, 17],
                    "stepping": 15,
                }
             )
        }

