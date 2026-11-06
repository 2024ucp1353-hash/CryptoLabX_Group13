
# MT19937 Stream Cipher and Predictable Token Attack

## 1. Introduction

This project demonstrates the use of the MT19937 pseudorandom number generator in a stream cipher and investigates its security weaknesses.

MT19937 is a Mersenne Twister pseudorandom number generator. It has a large period of 2^19937 - 1 and produces deterministic pseudorandom sequences.

However, MT19937 is not cryptographically secure because its output can be predicted when an attacker obtains sufficient information.

## 2. Objectives

1. Initialize the MT19937 random number generator.
2. Generate an 8-bit keystream for each plaintext byte.
3. Implement XOR-based encryption and decryption.
4. Recover a 16-bit seed using a known-plaintext attack.
5. Generate tokens using Unix timestamps as seeds.
6. Demonstrate a timestamp-based predictable token attack.
7. Verify the recovered seed and regenerated token.

## 3. Project Structure

```text
MT19937_Stream_Cipher/
|
|-- mt19937_cipher.py
|-- timestamp_token.py
|-- predictable_token_attack.py
|-- token_attack_verification.py
|-- README.md
```

## 4. MT19937 Stream Cipher

The generator is initialized using a seed.

For every plaintext byte, one 8-bit keystream value is generated.

Encryption:

    Ciphertext = Plaintext XOR Keystream

Decryption:

    Plaintext = Ciphertext XOR Keystream

The same seed generates the same keystream, allowing the original plaintext to be recovered.

## 5. Known-Plaintext Seed Recovery Attack

The encryption challenge uses:
- A randomly generated 16-bit seed.
- A plaintext containing a sequence of 14 consecutive 'A' characters.
- XOR-based encryption.

### Attack procedure

1. Try every possible 16-bit seed, from 0 to 65535.
2. Generate a candidate keystream for each seed.
3. XOR the candidate keystream with the ciphertext.
4. Search the resulting plaintext for 14 consecutive 'A' characters.
5. When the pattern is found, identify the corresponding seed.
6. Decrypt the ciphertext using the recovered seed.

### Pseudocode

```text
FOR seed = 0 TO 65535:
    Generate candidate keystream
    Decrypt ciphertext using candidate keystream

    IF plaintext contains 14 consecutive 'A':
        Return recovered seed and plaintext

Report failure if no seed matches
```

## 6. Timestamp-Based Token Generation

In this experiment, the current Unix timestamp is used as the MT19937 seed.

The generator produces 16 consecutive 8-bit outputs.

These outputs are combined to create a 16-byte token.

### Pseudocode

```text
timestamp = current Unix timestamp
Initialize MT19937 using timestamp

FOR i = 1 TO 16:
    Generate an 8-bit random value
    Append value to token

Display timestamp and token in hexadecimal
```

## 7. Predictable Token Attack

The weakness is demonstrated by searching a limited timestamp range.

The attacker assumes that the token was generated using a timestamp close to the current time.

The search interval is:

    T - 300 seconds to T + 300 seconds

For every timestamp in this interval:
1. Initialize MT19937 using that timestamp.
2. Generate a candidate 16-byte token.
3. Compare it with the observed token.
4. If both tokens match, the timestamp seed has been recovered.

### Pseudocode

```text
FOR timestamp = T - 300 TO T + 300:

    Initialize MT19937 using timestamp
    Generate candidate 16-byte token

    IF candidate token equals observed token:
        Return recovered timestamp

Report failure if no match is found
```

The search interval contains at most 601 possible timestamps.

## 8. Attack Verification

After recovering the timestamp:

1. Initialize MT19937 again using the recovered timestamp.
2. Generate another 16-byte token.
3. Compare the regenerated token with the original observed token.
4. Verify whether the recovered timestamp matches the original timestamp used in the experiment.

A successful attack should produce:

```text
Seed Recovered Correctly: True
Token Matches Original: True
ATTACK SUCCESSFUL!
```

## 9. Experimental Results

The experiments demonstrate two security weaknesses:

### Experiment 1: Known-Plaintext Attack

- The 16-bit seed space contains 65,536 possible seeds.
- Each possible seed can be tested through brute force.
- The known plaintext pattern helps identify the correct seed.

### Experiment 2: Timestamp-Based Attack

- The timestamp is used directly as the random generator seed.
- The attacker searches a window of 601 possible timestamps.
- The recovered timestamp reproduces the original token.

Actual execution times and recovered values are displayed by the Python programs.

## 10. Why MT19937 Is Not Cryptographically Secure

MT19937 is designed for statistical randomness, not security.

Its limitations include:

1. It is deterministic: the same seed produces the same sequence.
2. Its output is predictable when sufficient information is available.
3. Small seed spaces can be searched using brute force.
4. Timestamp-based seeds are particularly vulnerable because timestamps can often be estimated.
5. It is not designed to protect secret information against an attacker.

For security-sensitive applications, a cryptographically secure random number generator should be used instead.

Python provides the `secrets` module for generating security-sensitive random values.

## 11. Conclusion

The project successfully demonstrates MT19937 stream cipher implementation, known-plaintext seed recovery, timestamp-based token generation, and predictable token recovery.

The experiments show that a pseudorandom number generator suitable for simulations is not necessarily suitable for cryptographic applications.

MT19937 should not be used for generating encryption keys, authentication tokens, or other security-sensitive values.
