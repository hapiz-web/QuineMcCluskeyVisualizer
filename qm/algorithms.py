"""
==========================================================
Quine McCluskey Algorithm
Author : Jarvis
==========================================================
"""

from dataclasses import dataclass
from itertools import combinations
from typing import List, Dict, Set


@dataclass
class Implicant:
    bits: str
    minterms: Set[int]
    combined: bool = False

    def __hash__(self):
        return hash((self.bits, tuple(sorted(self.minterms))))

    def __str__(self):
        return f"{self.bits} -> {sorted(self.minterms)}"


class QuineMcCluskey:

    def __init__(self, variables, minterms, dont_cares=None):

        self.variables = variables

        self.minterms = sorted(set(minterms))

        self.dont_cares = sorted(set(dont_cares or []))

        self.all_terms = sorted(
            set(self.minterms + self.dont_cares)
        )

        self.steps = []

        self.prime_implicants = []

        self.essential_prime_implicants = []

        self.expression = ""

    #######################################################
    # Utility
    #######################################################

    def decimal_to_binary(self, value):

        return format(value, f"0{self.variables}b")

    def count_one(self, bits):

        return bits.count("1")

    def differ_by_one_bit(self, a, b):

        diff = 0

        position = -1

        for i in range(len(a)):

            if a[i] != b[i]:

                diff += 1

                position = i

            if diff > 1:

                return False, -1

        return diff == 1, position

    def merge_bits(self, a, b):

        ok, pos = self.differ_by_one_bit(a, b)

        if not ok:

            return None

        result = list(a)

        result[pos] = "-"

        return "".join(result)

    #######################################################
    # Step 1
    #######################################################

    def initial_grouping(self):

        groups = {}

        for value in self.all_terms:

            binary = self.decimal_to_binary(value)

            ones = self.count_one(binary)

            groups.setdefault(ones, [])

            groups[ones].append(

                Implicant(

                    bits=binary,

                    minterms={value}

                )

            )

        self.steps.append({

            "type": "initial",

            "groups": groups

        })

        return groups
        #######################################################
    # Step 2
    #######################################################

    def combine_groups(self, groups):

        new_groups = {}

        used = set()

        keys = sorted(groups.keys())

        for index in range(len(keys) - 1):

            current_group = groups[keys[index]]

            next_group = groups[keys[index + 1]]

            for item1 in current_group:

                for item2 in next_group:

                    merged = self.merge_bits(
                        item1.bits,
                        item2.bits
                    )

                    if merged is None:
                        continue

                    item1.combined = True
                    item2.combined = True

                    new_implicant = Implicant(
                        bits=merged,
                        minterms=item1.minterms.union(
                            item2.minterms
                        )
                    )

                    count = merged.count("1")

                    new_groups.setdefault(
                        count,
                        []
                    )

                    duplicate = False

                    for old in new_groups[count]:

                        if (
                            old.bits == new_implicant.bits
                            and
                            old.minterms == new_implicant.minterms
                        ):
                            duplicate = True
                            break

                    if not duplicate:
                        new_groups[count].append(
                            new_implicant
                        )

        self.steps.append({

            "type": "combine",

            "groups": new_groups

        })

        return new_groups

    #######################################################
    # Collect Prime Implicant
    #######################################################

    def collect_prime_implicants(self, groups):

        for group in groups.values():

            for implicant in group:

                if not implicant.combined:

                    duplicate = False

                    for old in self.prime_implicants:

                        if (
                            old.bits == implicant.bits
                            and
                            old.minterms == implicant.minterms
                        ):

                            duplicate = True
                            break

                    if not duplicate:

                        self.prime_implicants.append(
                            implicant
                        )

    #######################################################
    # Repeat Combine
    #######################################################

    def generate_prime_implicants(self):

        groups = self.initial_grouping()

        while True:

            for g in groups.values():

                for item in g:

                    item.combined = False

            new_groups = self.combine_groups(groups)

            self.collect_prime_implicants(groups)

            if len(new_groups) == 0:
                break

            groups = new_groups

        return self.prime_implicants

    #######################################################
    # Prime Implicant Chart
    #######################################################

    def covers(self, bits, value):

        binary = self.decimal_to_binary(value)

        for b1, b2 in zip(bits, binary):

            if b1 == "-":
                continue

            if b1 != b2:
                return False

        return True

    def build_prime_chart(self):

        chart = {}

        for m in self.minterms:

            chart[m] = []

            for index, implicant in enumerate(
                self.prime_implicants
            ):

                if self.covers(
                    implicant.bits,
                    m
                ):

                    chart[m].append(index)

        self.steps.append({

            "type": "chart",

            "chart": chart

        })

        return chart
    
        #######################################################
    # Essential Prime Implicant
    #######################################################

    def find_essential_prime_implicants(self, chart):

        essential_indexes = set()

        covered = set()

        for minterm, implicants in chart.items():

            if len(implicants) == 1:

                index = implicants[0]

                essential_indexes.add(index)

        for index in essential_indexes:

            implicant = self.prime_implicants[index]

            self.essential_prime_implicants.append(
                implicant
            )

            for minterm in self.minterms:

                if self.covers(
                    implicant.bits,
                    minterm
                ):

                    covered.add(minterm)

        self.steps.append({

            "type": "essential",

            "indexes": essential_indexes,

            "covered": covered

        })

        return covered

    #######################################################
    # Remaining Minterms
    #######################################################

    def remaining_minterms(self, covered):

        remain = []

        for m in self.minterms:

            if m not in covered:

                remain.append(m)

        return remain

    #######################################################
    # Petrick Method
    #######################################################

    def petrick_method(self, remain, chart):

        if len(remain) == 0:

            return []

        products = []

        for m in remain:

            products.append(chart[m])

        expression = [set([i]) for i in products[0]]

        for product in products[1:]:

            new_expression = []

            for term1 in expression:

                for term2 in product:

                    merged = set(term1)

                    merged.add(term2)

                    duplicate = False

                    for exist in new_expression:

                        if exist == merged:

                            duplicate = True
                            break

                    if not duplicate:

                        new_expression.append(merged)

            expression = new_expression

        expression.sort(

            key=lambda x: (
                len(x),
                sum(
                    len(
                        self.prime_implicants[i].bits.replace("-", "")
                    )
                    for i in x
                )
            )

        )

        return list(expression[0])

    #######################################################
    # Boolean Conversion
    #######################################################

    def bits_to_expression(self, bits):

        variables = [

            chr(ord("A") + i)

            for i in range(self.variables)

        ]

        result = []

        for index, bit in enumerate(bits):

            if bit == "-":

                continue

            if bit == "1":

                result.append(

                    variables[index]

                )

            else:

                result.append(

                    variables[index] + "'"

                )

        if len(result) == 0:

            return "1"

        return "".join(result)

    #######################################################
    # Final Expression
    #######################################################

    def build_expression(self, selected):

        terms = []

        for implicant in selected:

            terms.append(

                self.bits_to_expression(
                    implicant.bits
                )

            )

        self.expression = " + ".join(terms)

        return self.expression
    
        #######################################################
    # Solve
    #######################################################

    def solve(self):

        self.steps = []

        self.prime_implicants = []

        self.essential_prime_implicants = []

        self.expression = ""

        self.generate_prime_implicants()

        chart = self.build_prime_chart()

        covered = self.find_essential_prime_implicants(chart)

        remain = self.remaining_minterms(covered)

        selected = list(self.essential_prime_implicants)

        if remain:

            indexes = self.petrick_method(

                remain,

                chart

            )

            for index in indexes:

                implicant = self.prime_implicants[index]

                if implicant not in selected:

                    selected.append(implicant)

        expression = self.build_expression(selected)

        self.steps.append({

            "type": "result",

            "expression": expression

        })

        return {

            "expression": expression,

            "prime_implicants": self.prime_implicants,

            "essential_prime_implicants": selected,

            "steps": self.steps

        }

    #######################################################
    # Getter
    #######################################################

    def get_steps(self):

        return self.steps

    def get_prime_implicants(self):

        return self.prime_implicants

    def get_expression(self):

        return self.expression
