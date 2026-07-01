import time

from django.shortcuts import render
from django.shortcuts import redirect

from .forms import QuineMcCluskeyForm
from .models import CalculationHistory
from .algorithms import QuineMcCluskey


def parse_numbers(text):

    if not text or not str(text).strip():
        return []

    text = str(text).replace(" ", "")

    result = []

    for item in text.split(","):

        if item == "":
            continue

        result.append(int(item))

    return sorted(set(result))


def _covers(bits, value, variables):
    binary = format(value, f"0{variables}b")

    for bit, target in zip(bits, binary):
        if bit == "-":
            continue
        if bit != target:
            return False

    return True


def _serialize_groups(groups):
    return [
        {
            "count": key,
            "implicants": [
                {
                    "bits": implicant.bits,
                    "minterms": sorted(implicant.minterms),
                }
                for implicant in groups[key]
            ],
        }
        for key in sorted(groups.keys())
    ]


def _build_visualization(result, variables, minterms, dont_cares):
    steps = result.get("steps", [])
    prime_implicants = result.get("prime_implicants", [])
    essential_selected = result.get("essential_prime_implicants", [])

    initial_step = next((step for step in steps if step["type"] == "initial"), None)
    combination_steps = [step for step in steps if step["type"] == "combine"]
    chart_step = next((step for step in steps if step["type"] == "chart"), None)
    essential_step = next((step for step in steps if step["type"] == "essential"), None)

    initial_groups = []
    if initial_step:
        initial_groups = _serialize_groups(initial_step["groups"])

    combination_iterations = []
    for index, step in enumerate(combination_steps, start=1):
        combination_iterations.append(
            {
                "iteration": index,
                "groups": _serialize_groups(step["groups"]),
            }
        )

    prime_table = []
    selected_bits = {implicant.bits for implicant in essential_selected}

    for implicant in prime_implicants:
        covered_terms = [
            term for term in minterms if _covers(implicant.bits, term, variables)
        ]
        prime_table.append(
            {
                "bits": implicant.bits,
                "minterms": sorted(implicant.minterms),
                "covered_terms": covered_terms,
                "selected": implicant.bits in selected_bits,
            }
        )

    prime_chart = {
        "headers": [implicant.bits for implicant in prime_implicants],
        "rows": [],
    }
    for minterm in minterms:
        prime_chart["rows"].append(
            {
                "minterm": minterm,
                "covers": [
                    _covers(implicant.bits, minterm, variables)
                    for implicant in prime_implicants
                ],
            }
        )

    essential_items = []
    if essential_step:
        for index in sorted(essential_step.get("indexes", [])):
            implicant = prime_implicants[index]
            covered_terms = [
                term for term in minterms if _covers(implicant.bits, term, variables)
            ]
            essential_items.append(
                {
                    "bits": implicant.bits,
                    "minterms": sorted(implicant.minterms),
                    "covered_terms": covered_terms,
                }
            )

    remaining_minterms = []
    petrick_steps = []
    if essential_step:
        covered = set(essential_step.get("covered", []))
        remaining_minterms = [term for term in minterms if term not in covered]

    if remaining_minterms and chart_step:
        chart = chart_step["chart"]
        candidates = [{index} for index in chart[remaining_minterms[0]]]
        petrick_steps.append(
            {
                "title": f"Start with minterm {remaining_minterms[0]}",
                "candidates": [sorted(combo) for combo in candidates],
            }
        )

        for minterm in remaining_minterms[1:]:
            new_candidates = []
            for combo in candidates:
                for index in chart[minterm]:
                    merged = set(combo)
                    merged.add(index)
                    new_candidates.append(merged)
            candidates = new_candidates
            petrick_steps.append(
                {
                    "title": f"Combine with minterm {minterm}",
                    "candidates": [sorted(combo) for combo in candidates],
                }
            )

        unique_candidates = []
        seen = set()
        for combo in candidates:
            key = frozenset(combo)
            if key not in seen:
                seen.add(key)
                unique_candidates.append(combo)

        def cost(combo):
            literal_count = sum(
                len(prime_implicants[index].bits.replace("-", "")) for index in combo
            )
            return (len(combo), literal_count)

        best_combo = min(unique_candidates, key=cost) if unique_candidates else []
        petrick_steps.append(
            {
                "title": "Choose the minimum-cost cover",
                "candidates": [sorted(combo) for combo in unique_candidates],
                "best": sorted(best_combo),
            }
        )

    return {
        "initial_groups": initial_groups,
        "combination_iterations": combination_iterations,
        "prime_table": prime_table,
        "prime_chart": prime_chart,
        "essential_items": essential_items,
        "remaining_minterms": remaining_minterms,
        "petrick_steps": petrick_steps,
        "final_expression": result.get("expression", ""),
    }


def home(request):

    result = None

    steps = None

    expression = None

    visualization = None

    stats = None

    form = QuineMcCluskeyForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            variables = form.cleaned_data["variable_count"]

            minterms = form.cleaned_data.get("parsed_minterms", [])
            dont_cares = form.cleaned_data.get("parsed_dont_cares", [])

            try:
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

                visualization = _build_visualization(
                    result,
                    variables,
                    minterms,
                    dont_cares,
                )

                stats = {
                    "variables": variables,
                    "minterms": len(minterms),
                    "dont_cares": len(dont_cares),
                    "prime_implicants": len(result.get("prime_implicants", [])),
                    "essential_prime_implicants": len(result.get("essential_prime_implicants", [])),
                    "iterations": len([step for step in result.get("steps", []) if step.get("type") == "combine"]),
                    "execution_time_ms": round(execution_time * 1000, 2),
                }

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
            except Exception:
                form.add_error(None, "The calculation could not be completed. Please check your input and try again.")

    context = {

        "form": form,

        "result": result,

        "expression": expression,

        "steps": steps,

        "visualization": visualization,

        "stats": stats,

    }

    return render(

        request,

        "home.html",

        context

    )


def about(request):
    return render(
        request,
        "about.html",
        {
            "page_title": "About Quine-McCluskey",
        },
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