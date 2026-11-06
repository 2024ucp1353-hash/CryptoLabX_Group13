
import secrets
import time

BIT_LENGTH = 512
DEFAULT_ROUNDS = 40


# Commit 1: Generate random odd candidate
def generate_odd_candidate(bit_length=BIT_LENGTH):
    if bit_length < 2:
        raise ValueError("Bit length must be at least 2")

    candidate = secrets.randbits(bit_length)
    candidate |= (1 << (bit_length - 1))
    candidate |= 1

    return candidate


def validate_candidate_properties(candidate, expected_bits=BIT_LENGTH):
    return candidate.bit_length() == expected_bits and candidate % 2 == 1


# Commit 2: Fast modular exponentiation
def modular_exponentiation(base, exponent, modulus):
    if modulus <= 0:
        raise ValueError("Modulus must be positive")

    if exponent < 0:
        raise ValueError("Exponent cannot be negative")

    result = 1
    base %= modulus

    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus

        base = (base * base) % modulus
        exponent >>= 1

    return result % modulus


# Commit 3: Miller-Rabin primality test
def factorize_n_minus_1(n):
    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    return s, d


def is_witness(a, n, s, d):
    x = modular_exponentiation(a, d, n)

    if x == 1 or x == n - 1:
        return False

    for _ in range(s - 1):
        x = modular_exponentiation(x, 2, n)

        if x == n - 1:
            return False

        if x == 1:
            return True

    return True


def miller_rabin_test(n, rounds=DEFAULT_ROUNDS):
    if n < 2:
        return False

    if n in (2, 3):
        return True

    if n % 2 == 0:
        return False

    s, d = factorize_n_minus_1(n)

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2

        if is_witness(a, n, s, d):
            return False

    return True


# Commit 4: Candidate generation loop
def candidate_generation_loop(
    bit_length=BIT_LENGTH,
    rounds=DEFAULT_ROUNDS,
    on_candidate_tested=None
):
    while True:
        candidate = generate_odd_candidate(bit_length)

        is_probable_prime = miller_rabin_test(candidate, rounds)

        if on_candidate_tested is not None:
            on_candidate_tested(candidate, is_probable_prime)

        if is_probable_prime:
            return candidate


# Commits 5 and 6: Prime generation, candidate count and timing
if __name__ == "__main__":

    candidate_count = 0

    def count_candidate(candidate, is_probable_prime):
        global candidate_count
        candidate_count += 1

    print("=" * 60)
    print("       512-BIT MILLER-RABIN PRIME GENERATION")
    print("=" * 60)

    print("\nGenerating probable prime...")
    print("Please wait...\n")

    start_time = time.perf_counter()

    found_prime = candidate_generation_loop(
        bit_length=BIT_LENGTH,
        rounds=DEFAULT_ROUNDS,
        on_candidate_tested=count_candidate
    )

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    print("=" * 60)
    print("              EXPERIMENTAL RESULTS")
    print("=" * 60)

    print(f"\nGenerated Prime:\n{found_prime}")

    print("\nResult Summary:")
    print("-" * 60)
    print(f"{'Parameter':<30} {'Value'}")
    print("-" * 60)
    print(f"{'Assigned bit length':<30} {BIT_LENGTH}")
    print(f"{'Actual bit length':<30} {found_prime.bit_length()}")
    print(f"{'Candidates tested':<30} {candidate_count}")
    print(f"{'Miller-Rabin rounds':<30} {DEFAULT_ROUNDS}")
    print(f"{'Execution time (seconds)':<30} {execution_time:.6f}")
    print("-" * 60)

    print("\nCandidate validation:",
          validate_candidate_properties(found_prime))

    print("Miller-Rabin verification:",
          miller_rabin_test(found_prime, DEFAULT_ROUNDS))

    print("\nPrime generation completed successfully!")
