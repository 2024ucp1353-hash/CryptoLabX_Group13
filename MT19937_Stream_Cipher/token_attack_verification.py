
import time

from predictable_token_attack import (
    generate_token_from_timestamp,
    predict_timestamp_seed,
    TIME_WINDOW
)


def run_experiment():

    print("=" * 60)
    print("       MT19937 TOKEN ATTACK - VERIFICATION")
    print("=" * 60)

    # Generate the original token
    original_timestamp = int(time.time())
    observed_token = generate_token_from_timestamp(original_timestamp)

    print("\nOriginal Timestamp:", original_timestamp)
    print("Observed Token:", observed_token.hex())

    # Attacker knows only the approximate current time
    center_timestamp = int(time.time())

    start_timestamp = center_timestamp - TIME_WINDOW
    end_timestamp = center_timestamp + TIME_WINDOW

    print("\nSearch Interval:")
    print("Start:", start_timestamp)
    print("End:", end_timestamp)

    # Perform the timestamp attack
    start = time.time()

    recovered_timestamp, timestamps_tested = predict_timestamp_seed(
        observed_token, center_timestamp
    )

    elapsed_time = time.time() - start

    print("\n---------- EXPERIMENTAL RESULTS ----------")
    print("Total Timestamps Tested:", timestamps_tested)
    print("Time Taken: {:.6f} seconds".format(elapsed_time))

    if recovered_timestamp is None:
        print("\nAttack Failed: No matching timestamp found.")
        return

    # Regenerate token using recovered timestamp
    regenerated_token = generate_token_from_timestamp(
        recovered_timestamp
    )

    print("\nRecovered Timestamp:", recovered_timestamp)
    print("Original Timestamp:", original_timestamp)

    print("\nRegenerated Token:", regenerated_token.hex())

    # Verify the recovered seed and token
    seed_correct = recovered_timestamp == original_timestamp
    token_matches = regenerated_token == observed_token

    print("\n---------- VERIFICATION ----------")
    print("Seed Recovered Correctly:", seed_correct)
    print("Token Matches Original:", token_matches)

    if seed_correct and token_matches:
        print("\nATTACK SUCCESSFUL!")
        print("The original token was reproduced exactly.")
    else:
        print("\nVERIFICATION FAILED.")


if __name__ == "__main__":
    run_experiment()
