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
                "rows": 3,
                "placeholder": "Contoh: 0,1,2,5"
            }
        )
    )

    dont_cares = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Contoh: 3,4"
            }
        )
    )

    def _parse_numbers(self, value):
        if not value or not str(value).strip():
            return []

        items = []
        for raw_item in str(value).replace(" ", "").split(","):
            if not raw_item:
                continue
            try:
                items.append(int(raw_item))
            except ValueError:
                raise forms.ValidationError("Hanya bilangan bulat yang dipisahkan koma yang diperbolehkan")

        return items

    def clean(self):
        cleaned_data = super().clean()
        variable_count = cleaned_data.get("variable_count")
        minterms = cleaned_data.get("minterms")
        dont_cares = cleaned_data.get("dont_cares")

        if variable_count is None:
            return cleaned_data

        if minterms is None:
            minterms = ""
        if dont_cares is None:
            dont_cares = ""

        try:
            parsed_minterms = self._parse_numbers(minterms)
            parsed_dont_cares = self._parse_numbers(dont_cares)
        except forms.ValidationError as exc:
            raise exc

        error_messages = []

        if parsed_minterms:
            duplicates = sorted({value for value in parsed_minterms if parsed_minterms.count(value) > 1})
            if duplicates:
                error_messages.append("Minterm duplikat tidak diperbolehkan")

        if parsed_dont_cares:
            duplicates = sorted({value for value in parsed_dont_cares if parsed_dont_cares.count(value) > 1})
            if duplicates:
                error_messages.append("Nilai don't care duplikat tidak diperbolehkan")

        max_value = (2 ** variable_count) - 1
        for value in parsed_minterms + parsed_dont_cares:
            if value < 0 or value > max_value:
                error_messages.append(f"Nilai {value} di luar rentang yang diperbolehkan (0 sampai {max_value})")

        overlap = sorted(set(parsed_minterms) & set(parsed_dont_cares))
        if overlap:
            error_messages.append("Minterm dan don't care tidak boleh tumpang tindih")

        if error_messages:
            raise forms.ValidationError(error_messages)

        cleaned_data["parsed_minterms"] = sorted(set(parsed_minterms))
        cleaned_data["parsed_dont_cares"] = sorted(set(parsed_dont_cares))
        return cleaned_data
