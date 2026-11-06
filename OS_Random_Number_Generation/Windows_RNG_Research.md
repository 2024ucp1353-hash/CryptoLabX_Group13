# Windows Random Number Generation Mechanism (CNG Architecture)

## 1. Introduction

Microsoft Windows provides cryptographically secure pseudorandom number generation through its **Cryptography Next Generation (CNG)** architecture. Introduced in Windows Vista and Windows Server 2008 to replace the legacy CryptoAPI (CAPI), CNG provides a modular cryptographic subsystem designed to meet modern security baselines, including FIPS 140-2/140-3 compliance and NSA Suite B algorithms.

Within modern Windows systems, random number generation is handled in kernel space by the system cryptographic driver (`ksecdd.sys`), exposing high-performance, non-blocking, and unpredictable random bytes to both user-mode applications and kernel-mode services.

---

## 2. Windows CNG Architecture

The Windows CNG architecture separates cryptographic algorithm interfaces from their underlying implementations via a provider model:

```text
+-----------------------------------------------------------+
|                   User Mode Applications                  |
|     (C/C++ Win32, .NET CLR, PowerShell, Web Browsers)     |
+-----------------------------------------------------------+
                             |
                    BCrypt APIs (bcrypt.dll)
                             |
+----------------------------v------------------------------+
|                     Kernel Mode Core                      |
|                      (ksecdd.sys)                         |
|   +---------------------------------------------------+   |
|   |          Entropy Pool & Collection Engine         |   |
|   +---------------------------------------------------+   |
|                             |                             |
|   +-------------------------v-------------------------+   |
|   |         AES-CTR DRBG (NIST SP 800-90A)            |   |
|   +---------------------------------------------------+   |
+-----------------------------------------------------------+
```

### Key Architectural Layers:
1. **User Mode Interface (`bcrypt.dll`)**: Exposes the user-level cryptographic primitives. Function calls such as `BCryptGenRandom` transition securely into the kernel.
2. **Kernel Driver (`ksecdd.sys`)**: Hosts the centralized entropy pool and CSPRNG state engines. Centralizing generator state in kernel memory prevents unauthorized user-mode inspection and memory tampering.
3. **Hardware Abstraction Layer (HAL)**: Interfaces directly with hardware roots of trust, such as TPM chips, hardware performance counters, and CPU-level entropy instructions (`RDRAND`/`RDSEED`).

---

## 3. The `BCryptGenRandom` API

The core Windows API for obtaining cryptographic random bytes is `BCryptGenRandom`, declared in `<bcrypt.h>`:

```c
NTSTATUS BCryptGenRandom(
    BCRYPT_ALG_HANDLE hAlgorithm,
    PUCHAR            pbBuffer,
    ULONG             cbBuffer,
    ULONG             dwFlags
);
```

### Parameters & Usage:
- **`hAlgorithm`**: Handle to an algorithm provider opened using `BCryptOpenAlgorithmProvider(..., BCRYPT_RNG_ALGORITHM, ...)`.
- **`pbBuffer`**: Pointer to the target memory buffer that receives the generated random bytes.
- **`cbBuffer`**: The number of bytes to generate.
- **`dwFlags`**: Behavior flags modifying how the random bytes are produced:
  - **`BCRYPT_USE_SYSTEM_PREFERRED_RNG`**: Instructs the function to use the default system-preferred RNG. When this flag is passed, `hAlgorithm` must be set to `NULL`, eliminating the overhead of opening and closing an algorithm provider handle.
  - **`BCRYPT_RNG_USE_ENTROPY_IN_BUFFER`**: Allows caller-provided seed data in `pbBuffer` to be XORed into the entropy pool as additional environmental noise before generation.

---

## 4. System-Preferred RNG

Using the flag `BCRYPT_USE_SYSTEM_PREFERRED_RNG` is the modern, recommended pattern for all Win32 cryptographic development:

1. **Handle-Free Execution**: The caller does not need to maintain or synchronize an algorithm provider handle across threads.
2. **Global Kernel State**: Connects directly to the singleton kernel CSPRNG maintained by `ksecdd.sys`.
3. **Optimized Concurrency**: The kernel driver maintains per-processor state caches to minimize spinlock contention across multi-core server processors.

---

## 5. Underlying Cryptographic Algorithm (AES-CTR DRBG)

In modern Windows versions (Windows 10, Windows 11, Windows Server 2016+), the system CSPRNG implements the **CTR_DRBG** construction based on **AES-256** specified in **NIST SP 800-90A**:

- **Primitive**: Counter Mode Deterministic Random Bit Generator using AES with 256-bit keys (`AES-256-CTR`).
- **Internal State**: Consists of:
  - A 256-bit encryption key ($K$).
  - A 128-bit counter block ($V$).
- **Generation Mechanism**:
  1. Increment counter $V$.
  2. Compute output block: $Block_i = \text{AES}_{K}(V)$.
  3. Emit requested pseudorandom byte slice.
- **State Transition & Rekeying**:
  After servicing requests, the generator automatically updates its internal key $K$ using newly produced pseudo-random blocks and environmental entropy, destroying the prior key to enforce forward secrecy.

---

## 6. Entropy Harvesting & Collection Mechanisms

Windows continuously gathers environmental unpredictability into an internal raw entropy pool before feeding it through conditioning hashes to seed the DRBG:

- **Interrupt Timing**: High-resolution timestamps of hardware interrupts generated by disk controllers, network cards, and keyboard/mouse inputs.
- **Processor Execution Jitter**: Cycle count differences obtained via the `RDTSC` (Read Time-Stamp Counter) instruction.
- **Hardware Random Number Generators**: Direct hardware instructions including Intel/AMD `RDRAND` and `RDSEED`.
- **Trusted Platform Module (TPM)**: Cryptographic hardware random sources built into the TPM 2.0 module.
- **Operating System Telemetry**: Internal kernel scheduler latency, thread context-switch timings, and system performance counters (`QueryPerformanceCounter`).

---

## 7. .NET Cryptographic RNG

Modern .NET applications (across .NET Core, .NET 5+, and modern .NET Framework) utilize the managed wrapper `System.Security.Cryptography.RandomNumberGenerator`:

```csharp
using System.Security.Cryptography;

// Generate 1 MiB of secure random data
byte[] buffer = new byte[1048576];
using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
{
    rng.GetBytes(buffer);
}
```

### Execution Pathway:
1. `.NET` `RandomNumberGenerator.Create()` instantiates the default platform cryptographic provider.
2. On Windows platforms, the CLR runtime makes a direct P/Invoke transition to `BCryptGenRandom` passing `BCRYPT_USE_SYSTEM_PREFERRED_RNG`.
3. Non-cryptographic generators (e.g., `System.Random`) use linear congruential or simple subtractive algorithms and must **never** be used for security-critical functions such as key generation, salts, IVs, or authentication tokens.

---

## 8. Forward Secrecy and Backtracking Resistance

Windows CNG incorporates strict backtracking resistance and prediction resistance:

- **Backtracking Resistance (Forward Secrecy)**: Even if an attacker were to achieve full kernel memory readout at time $T_1$, they cannot compute any outputs generated prior to $T_1$. The generator immediately updates and overwrites its key state following each output generation.
- **Prediction Resistance**: The kernel driver continuously mixes fresh entropy into the DRBG state, preventing attackers from predicting future outputs once the state is updated.
- **FIPS 140-3 Validation**: The entire CNG RNG sub-module is formally certified under NIST CAVP and CMVP validation standards.

---

## 9. Conclusion

The Windows CNG random number generator represents an enterprise-grade, FIPS-compliant cryptographic subsystem:
- Built around NIST SP 800-90A AES-CTR DRBG.
- Backed by diverse kernel-level entropy collection.
- Accessible via clean, high-performance Win32 (`BCryptGenRandom`) and .NET (`RandomNumberGenerator`) APIs.

---

## References

1. Microsoft Docs – BCryptGenRandom function: https://learn.microsoft.com/en-us/windows/win32/api/bcrypt/nf-bcrypt-bcryptgenrandom
2. Microsoft Docs – Cryptography Next Generation (CNG): https://learn.microsoft.com/en-us/windows/win32/seccng/cng-portal
3. NIST SP 800-90A Rev. 1: Recommendation for Random Number Generation Using Deterministic Random Bit Generators: https://csrc.nist.gov/publications/detail/sp/800-90a/rev-1/final
4. Microsoft Security – Windows 10/11 Random Number Generation Architecture: https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/
