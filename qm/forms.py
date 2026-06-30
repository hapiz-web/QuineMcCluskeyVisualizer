from django import forms


class QuineMcCluskeyForm(forms.Form):

    variable_count = forms.IntegerField(
        min_value=1,
        max_value=32,
        label="Jumlah Variabel"
    )

    minterms = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3
            }
        )
    )

    dont_cares = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3
            }
        )
    )