import math
import os
import sys
from typing import Dict, Any, Tuple
import numpy as np
import scipy.stats as stats

# ==============================================================================
# Advanced Statistical Randomness Tests (NIST SP 800-22 Standard)
# ==============================================================================

def compute_serial_correlation(data_bytes: bytes) -> float:
    """
    Computes the serial correlation coefficient (r) between adjacent bytes.

    Formula:
        r = sum((x_i - mean) * (x_{i+1} - mean)) / sum((x_i - mean)^2)

    Interpretation:
        For ideal random sequences, adjacent values are completely independent,
        resulting in r close to 0.0 (|r| < 0.005 for 1 MiB sample).
    """
    arr = np.frombuffer(data_bytes, dtype=np.uint8).astype(np.float64)
    n = len(arr)
    if n < 2:
        return 0.0

    mean_val = np.mean(arr)
    diff = arr - mean_val
    numerator = np.sum(diff[:-1] * diff[1:])
    denominator = np.sum(diff ** 2)

    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def compute_chi_square(data_bytes: bytes) -> Tuple[float, float, bool]:
    """
    Performs the Pearson's Chi-Square Goodness-of-Fit test for byte uniformity.

    For 1 MiB (1,048,576 bytes) across 256 byte values:
        Expected frequency per byte E = 1,048,576 / 256 = 4096.0
        Degrees of freedom df = 256 - 1 = 255

    Returns:
        (chi2_statistic, p_value, passed)
        Passed if p_value >= 0.01 (confidence level 99%).
    """
    arr = np.frombuffer(data_bytes, dtype=np.uint8)
    n = len(arr)
    observed_counts = np.bincount(arr, minlength=256)
    expected_count = n / 256.0

    chi2_stat = float(np.sum((observed_counts - expected_count) ** 2 / expected_count))
    df = 255
    p_value = float(stats.chi2.sf(chi2_stat, df=df))
    passed = bool(p_value >= 0.01)

    return chi2_stat, p_value, passed


def compute_monobit_test(data_bytes: bytes) -> Tuple[int, int, float, float, bool]:
    """
    Performs the NIST SP 800-22 Monobit (Frequency) Test.

    Evaluates the balance of zeros and ones across the entire bit sequence.
    For 1 MiB, total bits n = 8,388,608.

    Test Statistic:
        S_n = (number of 1s) - (number of 0s)
        s_obs = |S_n| / sqrt(n)
        P-value = erfc(s_obs / sqrt(2))

    Returns:
        (ones_count, zeros_count, s_obs, p_value, passed)
        Passed if p_value >= 0.01.
    """
    arr = np.frombuffer(data_bytes, dtype=np.uint8)
    bits = np.unpackbits(arr)
    n_bits = len(bits)

    ones_count = int(np.sum(bits))
    zeros_count = n_bits - ones_count
    s_n = int(ones_count - zeros_count)
    s_obs = float(abs(s_n) / math.sqrt(n_bits))
    p_value = float(math.erfc(s_obs / math.sqrt(2.0)))
    passed = bool(p_value >= 0.01)

    return ones_count, zeros_count, s_obs, p_value, passed


def compute_runs_test(data_bytes: bytes) -> Tuple[int, float, float, bool]:
    """
    Performs the NIST SP 800-22 Runs Test.

    Tests whether the number of runs of consecutive zeros and ones of various
    lengths is consistent with a truly random sequence.

    Pre-test:
        Proportion of ones pi = ones / n. If |pi - 0.5| >= 2 / sqrt(n), test fails immediately.

    Test Statistic:
        V_n = 1 + sum(bit_k != bit_{k+1})
        P-value = erfc(|V_n - 2*n*pi*(1-pi)| / (2 * sqrt(2*n) * pi * (1-pi)))

    Returns:
        (total_runs, expected_runs, p_value, passed)
        Passed if p_value >= 0.01.
    """
    arr = np.frombuffer(data_bytes, dtype=np.uint8)
    bits = np.unpackbits(arr)
    n_bits = len(bits)

    ones_count = int(np.sum(bits))
    pi = ones_count / n_bits

    # Pre-test frequency check
    if abs(pi - 0.5) >= (2.0 / math.sqrt(n_bits)):
        return 0, 0.0, 0.0, False

    # Count observed transitions
    runs_obs = int(1 + np.sum(bits[:-1] != bits[1:]))
    expected_runs = 2.0 * n_bits * pi * (1.0 - pi)
    denominator = 2.0 * math.sqrt(2.0 * n_bits) * pi * (1.0 - pi)
    z = abs(runs_obs - expected_runs) / denominator
    p_value = float(math.erfc(z))
    passed = bool(p_value >= 0.01)

    return runs_obs, expected_runs, p_value, passed


def run_comprehensive_statistical_suite(filepath: str) -> Dict[str, Any]:
    """
    Executes the full suite of advanced statistical tests on a given binary dataset.
    """
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        data = f.read()

    total_bytes = len(data)
    total_bits = total_bytes * 8

    # Run tests
    sc = compute_serial_correlation(data)
    chi2_stat, p_chi2, pass_chi2 = compute_chi_square(data)
    ones, zeros, s_obs, p_monobit, pass_monobit = compute_monobit_test(data)
    runs_obs, runs_exp, p_runs, pass_runs = compute_runs_test(data)

    all_passed = pass_chi2 and pass_monobit and pass_runs and (abs(sc) < 0.01)

    return {
        "filename": filename,
        "total_bytes": total_bytes,
        "total_bits": total_bits,
        "serial_correlation": sc,
        "chi_square": {
            "statistic": chi2_stat,
            "degrees_of_freedom": 255,
            "p_value": p_chi2,
            "passed": pass_chi2
        },
        "monobit": {
            "ones": ones,
            "zeros": zeros,
            "s_obs": s_obs,
            "p_value": p_monobit,
            "passed": pass_monobit
        },
        "runs": {
            "observed_runs": runs_obs,
            "expected_runs": runs_exp,
            "p_value": p_runs,
            "passed": pass_runs
        },
        "overall_verdict": "PASSED (Cryptographically Statistically Random)" if all_passed else "FAILED"
    }


def format_results_report(results: Dict[str, Any]) -> str:
    """
    Formats the statistical test suite output into a readable report.
    """
    report = []
    report.append("=" * 65)
    report.append(f"  STATISTICAL ANALYSIS REPORT: {results['filename']}")
    report.append("=" * 65)
    report.append(f"File Size               : {results['total_bytes']:,} bytes ({results['total_bits']:,} bits)")
    report.append(f"Serial Correlation (r)  : {results['serial_correlation']:.6f} (Ideal: ~0.000000)")
    report.append("-" * 65)
    report.append(f"1. Chi-Square Test (df=255):")
    report.append(f"   - Chi^2 Statistic    : {results['chi_square']['statistic']:.2f}")
    report.append(f"   - P-value            : {results['chi_square']['p_value']:.4f}")
    report.append(f"   - Verdict (p >= 0.01): {'PASS' if results['chi_square']['passed'] else 'FAIL'}")
    report.append("-" * 65)
    report.append(f"2. NIST Monobit (Frequency) Test:")
    report.append(f"   - Total Ones (1s)    : {results['monobit']['ones']:,} ({results['monobit']['ones']/results['total_bits']*100:.2f}%)")
    report.append(f"   - Total Zeros (0s)   : {results['monobit']['zeros']:,} ({results['monobit']['zeros']/results['total_bits']*100:.2f}%)")
    report.append(f"   - S_obs Statistic    : {results['monobit']['s_obs']:.4f}")
    report.append(f"   - P-value            : {results['monobit']['p_value']:.4f}")
    report.append(f"   - Verdict (p >= 0.01): {'PASS' if results['monobit']['passed'] else 'FAIL'}")
    report.append("-" * 65)
    report.append(f"3. NIST Runs Test:")
    report.append(f"   - Observed Runs      : {results['runs']['observed_runs']:,}")
    report.append(f"   - Expected Runs      : {results['runs']['expected_runs']:,.1f}")
    report.append(f"   - P-value            : {results['runs']['p_value']:.4f}")
    report.append(f"   - Verdict (p >= 0.01): {'PASS' if results['runs']['passed'] else 'FAIL'}")
    report.append("=" * 65)
    report.append(f"Overall Evaluation      : {results['overall_verdict']}")
    report.append("=" * 65)
    return "\n".join(report)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    targets = ["linux_urandom.bin", "openssl_rand.bin", "windows_cng.bin"]

    print("[*] Running Advanced Statistical Randomness Tests (NIST SP 800-22 Suite)\n")
    for target in targets:
        path = os.path.join(data_dir, target)
        if os.path.exists(path):
            res = run_comprehensive_statistical_suite(path)
            print(format_results_report(res))
            print()
        else:
            print(f"[-] Dataset {target} not found at {path}")
