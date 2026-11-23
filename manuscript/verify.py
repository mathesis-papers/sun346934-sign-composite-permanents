import itertools
import json
import math
from pathlib import Path
import random
from collections import Counter


def matching_square_sum(values):
    if not values:
        return 1
    first = values[0]
    return sum(
        (first - values[index]) ** 2
        * matching_square_sum(values[1:index] + values[index + 1:])
        for index in range(1, len(values))
    )


def squared_sum_expansion(order):
    coefficients = {(0, 0): 1}
    for value in range(1, order + 1):
        updated = dict(coefficients)
        for (linear_degree, square_degree), coefficient in coefficients.items():
            linear_key = (linear_degree + 1, square_degree)
            square_key = (linear_degree, square_degree + 1)
            updated[linear_key] = updated.get(linear_key, 0) + value * coefficient
            updated[square_key] = updated.get(square_key, 0) + value ** 2 * coefficient
        coefficients = updated
    return sum(
        2 ** mixed * math.factorial(mixed) * math.factorial(row_square)
        * math.factorial(order - mixed - row_square)
        * coefficients[(mixed, row_square)]
        * coefficients[(mixed, order - mixed - row_square)]
        for mixed in range(order + 1)
        for row_square in range(order - mixed + 1)
    )


def elementary(values):
    coefficients = [1]
    for value in values:
        coefficients.append(0)
        for degree in range(len(coefficients) - 1, 0, -1):
            coefficients[degree] += value * coefficients[degree - 1]
    return coefficients


def additive_permanent(row_values, column_values):
    order = len(row_values)
    assert len(column_values) == order
    row_coefficients = elementary(row_values)
    column_coefficients = elementary(column_values)
    return sum(
        math.factorial(degree) * math.factorial(order - degree)
        * row_coefficients[degree] * column_coefficients[order - degree]
        for degree in range(order + 1)
    )


def subset_permanent(matrix):
    order = len(matrix)
    assert all(len(row) == order for row in matrix)
    values = [0] * (1 << order)
    values[0] = 1
    for mask in range(1, 1 << order):
        row_index = mask.bit_count() - 1
        remaining = mask
        while remaining:
            column_bit = remaining & -remaining
            column_index = column_bit.bit_length() - 1
            values[mask] += matrix[row_index][column_index] * values[mask ^ column_bit]
            remaining ^= column_bit
    return values[-1]


def permutation_permanent(matrix):
    order = len(matrix)
    return sum(
        math.prod(matrix[row_index][permutation[row_index]] for row_index in range(order))
        for permutation in itertools.permutations(range(order))
    )


def difference_value(half_order):
    values = list(range(1, 2 * half_order + 1))
    return additive_permanent(values, [-value for value in values])


def positive_value(half_order):
    square_coefficients = elementary([(2 * index - 1) ** 2 for index in range(1, half_order + 1)])
    numerator = sum(
        math.factorial(2 * degree) * math.factorial(2 * half_order - 2 * degree)
        * square_coefficients[degree] * square_coefficients[half_order - degree]
        for degree in range(half_order + 1)
    )
    denominator = 2 ** (2 * half_order)
    assert numerator % denominator == 0
    return numerator // denominator


def is_prime(number):
    return number >= 2 and all(number % divisor for divisor in range(2, math.isqrt(number) + 1))


def main():
    root = Path(__file__).resolve().parent
    data = {}
    for line in (root / 'oeis-a346934.txt').read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        index, value = line.split()
        data[int(index)] = int(value)
    assert sorted(data) == list(range(1, 131))
    sequence_values = {}
    for half_order in range(1, 131):
        value = difference_value(half_order)
        assert value == data[half_order]
        assert (-1) ** half_order * value == positive_value(half_order) > 0
        modulus = 2 * half_order + 1
        assert value % modulus == (2 if is_prime(modulus) else 0)
        sequence_values[half_order] = value
    difference_cases = 0
    for order in range(13):
        matrix = [[row_index - column_index for column_index in range(order)] for row_index in range(order)]
        value = subset_permanent(matrix)
        assert value == additive_permanent(list(range(order)), [-index for index in range(order)])
        if order <= 8:
            assert value == permutation_permanent(matrix)
        if order % 2:
            assert value == 0
        elif order:
            assert value == sequence_values[order // 2]
        else:
            assert value == 1
        difference_cases += 1
    generator = random.Random(346934)
    additive_cases = 0
    for order in range(10):
        for sample_index in range(12):
            row_values = [generator.randrange(-7, 8) for index in range(order)]
            column_values = [generator.randrange(-7, 8) for index in range(order)]
            matrix = [[row_value + column_value for column_value in column_values] for row_value in row_values]
            expected = additive_permanent(row_values, column_values)
            assert subset_permanent(matrix) == expected
            modulus = order + 1
            if modulus >= 2 and not is_prime(modulus) and modulus != 4:
                assert expected % modulus == 0
            if order <= 6:
                assert permutation_permanent(matrix) == expected
            additive_cases += 1
    factorials = [math.factorial(index) for index in range(501)]
    split_tests = 0
    for modulus in range(2, 502):
        residues = [
            factorials[degree] * factorials[modulus - 1 - degree] % modulus
            for degree in range(modulus)
        ]
        universal = all(residue == 0 for residue in residues)
        assert universal == (not is_prime(modulus) and modulus != 4)
        split_tests += modulus
    exceptional_matrix = [[row_value + column_value for column_value in [0, 1, 1]] for row_value in [1, 0, 0]]
    assert permutation_permanent(exceptional_matrix) == 2
    sum_cases = 0
    for half_order in range(1, 131):
        order = 2 * half_order
        value = additive_permanent(list(range(1, order + 1)), list(range(1, order + 1)))
        assert (value - sequence_values[half_order]) % (order + 1) == 0
        sum_cases += 1
    reciprocal_primes = [3, 5, 7, 11, 13]
    for prime in reciprocal_primes:
        modulus = prime ** 2
        matrix = [
            [0 if row_index == column_index else pow(row_index - column_index, -1, modulus)
             for column_index in range(1, prime)]
            for row_index in range(1, prime)
        ]
        assert (subset_permanent(matrix) - (-1) ** ((prime - 1) // 2)) % modulus == 0
    matching_multisets = 0
    for order in [2, 4, 6, 8]:
        for values in itertools.combinations_with_replacement([-1, 0, 1], order):
            expected = (-1) ** (order // 2) * math.factorial(order // 2) * matching_square_sum(values)
            actual = additive_permanent(values, [-value for value in values])
            assert actual == expected
            assert (actual == 0) == (max(Counter(values).values()) > order // 2)
            matching_multisets += 1
    matching_generator = random.Random(34693402)
    matching_samples = 0
    for order in [2, 4, 6, 8, 10]:
        for sample_index in range(20):
            values = [matching_generator.randrange(-5, 6) for index in range(order)]
            expected = (-1) ** (order // 2) * math.factorial(order // 2) * matching_square_sum(values)
            actual = additive_permanent(values, [-value for value in values])
            assert actual == expected
            assert (actual == 0) == (max(Counter(values).values()) > order // 2)
            matching_samples += 1
    universal_gcd_cases = 0
    least_common_multiple = 1
    for order in range(501):
        least_common_multiple = math.lcm(least_common_multiple, order + 1)
        actual = math.gcd(*(factorials[degree] * factorials[order - degree] for degree in range(order + 1)))
        assert actual == math.factorial(order + 1) // least_common_multiple
        if order <= 12:
            for degree in range(order + 1):
                row_values = [1] * degree + [0] * (order - degree)
                column_values = [1] * (order - degree) + [0] * degree
                assert additive_permanent(row_values, column_values) == factorials[degree] * factorials[order - degree]
        universal_gcd_cases += 1
    power_cases = 0
    for modulus in range(2, 102):
        if is_prime(modulus) or modulus == 4:
            continue
        for exponent in range(5):
            values = [pow(index, exponent, modulus) for index in range(1, modulus)]
            assert additive_permanent(values, values) % modulus == 0
            assert additive_permanent(values, [-value for value in values]) % modulus == 0
            power_cases += 1
    odd_primes = [prime for prime in range(3, 200, 2) if is_prime(prime)]
    for prime in odd_primes:
        modulus = prime ** 2
        values = list(range(1, prime + 1))
        assert additive_permanent(values, values) % modulus == prime
        half_order = (prime - 1) // 2
        squares = [index ** 2 for index in range(1, half_order + 1)]
        assert (additive_permanent(squares, squares) - (-1) ** (half_order - 1) * 2 * math.factorial(half_order)) % prime == 0
    for order in range(9):
        matrix = [[(row + column) ** 2 for column in range(1, order + 1)] for row in range(1, order + 1)]
        assert subset_permanent(matrix) == squared_sum_expansion(order)
    output = {
        'status': 'PASS',
        'arithmetic': 'Unbounded Python integers; no floating-point arithmetic.',
        'sequence_and_positive_formula': {'range_n': [1, 130], 'cases': 130, 'source': 'https://oeis.org/A346934/b346934.txt'},
        'prime_and_composite_congruences': {'range_n': [1, 130], 'cases': 130},
        'difference_matrix_subset_checks': {'range_order': [0, 12], 'cases': difference_cases},
        'difference_matrix_permutation_checks': {'range_order': [0, 8], 'cases': 9},
        'additive_matrix_checks': {'range_order': [0, 9], 'samples_per_order': 12, 'cases': additive_cases, 'seed': 346934, 'entry_component_range': [-7, 7]},
        'additive_matrix_permutation_checks': {'range_order': [0, 6], 'cases': 84},
        'factorial_split_classification': {'range_modulus': [2, 501], 'moduli': 500, 'splits': split_tests},
        'sum_matrix_congruence': {'range_n': [1, 130], 'cases': sum_cases},
        'cited_reciprocal_congruence': {'primes': reciprocal_primes, 'modulus': 'p^2', 'cases': 5, 'reference': 'https://arxiv.org/abs/2605.19502v1; Theorem 2 (12)'},
        'matching_identity_multisets': {'orders': [2, 4, 6, 8], 'alphabet': [-1, 0, 1], 'cases': matching_multisets, 'equality_criterion': True},
        'matching_identity_samples': {'orders': [2, 4, 6, 8, 10], 'samples_per_order': 20, 'component_range': [-5, 5], 'seed': 34693402, 'cases': matching_samples, 'equality_criterion': True},
        'universal_gcd': {'range_order': [0, 500], 'cases': universal_gcd_cases, 'binary_witness_range_order': [0, 12]},
        'power_sum_and_difference': {'range_modulus': [2, 101], 'range_exponent': [0, 4], 'cases': power_cases, 'moduli': 'composite, excluding 4'},
        'sum_prime_square_congruence': {'primes': odd_primes, 'cases': len(odd_primes), 'modulus': 'p^2'},
        'half_order_square_sum_prime_congruence': {'primes': odd_primes, 'cases': len(odd_primes), 'modulus': 'p'},
        'squared_sum_expansion': {'range_order': [0, 8], 'cases': 9},
        'exception_q4': {'row_values': [1, 0, 0], 'column_values': [0, 1, 1], 'permanent': 2},
        'first_values': [sequence_values[index] for index in range(1, 7)],
        'coverage': 'Finite exact checks of the displayed identities and examples; the all-order results have written proofs in note.tex.'
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
