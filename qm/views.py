import time

from django.shortcuts import render
from django.shortcuts import redirect

from .forms import QuineMcCluskeyForm
from .models import CalculationHistory
from .algorithms import QuineMcCluskey


def parse_numbers(text):

    if not text.strip():
        return []

    text = text.replace(" ", "")

    result = []

    for item in text.split(","):

        if item == "":
            continue

        result.append(int(item))

    return sorted(set(result))


def home(request):

    result = None

    steps = None

    expression = None

    if request.method == "POST":

        form = QuineMcCluskeyForm(request.POST)

        if form.is_valid():

            variables = form.cleaned_data["variable_count"]

            minterms = parse_numbers(

                form.cleaned_data["minterms"]

            )

            dont_cares = parse_numbers(

                form.cleaned_data["dont_cares"]

            )

            start = time.perf_counter()

            solver = QuineMcCluskey(

                variables,

                minterms,

                dont_cares

            )

            result = solver.solve()

            finish = time.perf_counter()

            execution_time = finish - start

            expression = result["expression"]

            steps = result["steps"]

            CalculationHistory.objects.create(

                variable_count=variables,

                minterms=",".join(

                    map(str, minterms)

                ),

                dont_cares=",".join(

                    map(str, dont_cares)

                ),

                simplified_expression=expression,

                execution_time=execution_time

            )

    else:

        form = QuineMcCluskeyForm()

    context = {

        "form": form,

        "result": result,

        "expression": expression,

        "steps": steps

    }

    return render(

        request,

        "home.html",

        context

    )


def history(request):

    calculations = CalculationHistory.objects.all()

    return render(

        request,

        "history.html",

        {

            "calculations": calculations

        }

    )


def history_detail(request, pk):

    item = CalculationHistory.objects.get(

        pk=pk

    )

    return render(

        request,

        "history_detail.html",

        {

            "item": item

        }

    )


def delete_history(request, pk):

    CalculationHistory.objects.filter(

        pk=pk

    ).delete()

    return redirect(

        "history"

    )


def clear_history(request):

    CalculationHistory.objects.all().delete()

    return redirect(

        "history"

    )