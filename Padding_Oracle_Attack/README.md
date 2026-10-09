# Lab Assignment 7: Padding Oracle Attack on AES-CBC

**Course**: Cryptography Laboratory (22CPP307)  
**Repository**: `CryptoLabX_Group13`  
**Topic**: Padding Oracle Attack on AES-CBC mode using PKCS#7 Padding  

---

## 👥 Team Members (Group 13)

- **Ayush Sthapak** (2024UCP1353)
- **Rishika Vijay** (2024UCP1398)

---

## 🎯 Objective & Scenario

Demonstrate how an attacker can decrypt an arbitrary **AES-CBC encrypted ciphertext** byte-by-byte without knowing or accessing the secret AES encryption key ($K$), by exploiting a **Padding Oracle** vulnerability.

### Scenario Constraints
- The AES key $K$ is kept strictly private within the oracle.
- The attacker only has access to:
  1. The ciphertext $C = (C_1, C_2, \dots, C_n)$ and Initialization Vector ($IV$).
  2. An oracle function `oracle(ciphertext, iv)` that returns `True` if the decrypted ciphertext has valid PKCS#7 padding, and `False` otherwise.
- No ready-made padding oracle libraries are used.

---

## 🧠 Theoretical Foundations

### 1. AES in Cipher Block Chaining (CBC) Mode
In AES-CBC mode, plaintext is partitioned into 16-byte blocks $P_1, P_2, \dots, P_n$.

#### Encryption:
$$C_0 = IV$$
$$C_i = E_K(P_i \oplus C_{i-1}) \quad \text{for } i \ge 1$$

#### Decryption:
$$P_i = D_K(C_i) \oplus C_{i-1} \quad \text{for } i \ge 1$$
where $D_K(C_i)$ represents the raw block cipher decryption output (known as the **Intermediate State** $I_i$):
$$I_i = D_K(C_i)$$
$$P_i = I_i \oplus C_{i-1}$$

### 2. PKCS#7 Padding
AES operates on fixed blocks of 16 bytes ($B = 16$). If the plaintext length is not an exact multiple of 16, PKCS#7 appends $L$ bytes, each having value $L$, where $1 \le L \le 16$:
- 1 byte missing: append `0x01`
- 2 bytes missing: append `0x02 0x02`
- 3 bytes missing: append `0x03 0x03 0x03`
- ...
- 16 bytes missing (or exact multiple of 16): append a full 16-byte padding block `0x10 ... 0x10` (16 bytes of value 16).

### 3. Role of the Padding Oracle
When a server decrypts received data, it removes the PKCS#7 padding. If the padding bytes do not match the expected format (e.g. invalid padding length or mismatched repeated bytes), the server rejects the request. 

If the server leaks this validation failure through:
- A distinct error message (e.g., `InvalidPaddingException` vs `BadMACException`),
- A specific HTTP status code (e.g., 500 Internal Error vs 403 Forbidden), or
- A timing side-channel,

it acts as a **Padding Oracle** (Vaudenay's Attack, 2002).

---

## 🔍 Attack Mechanics: Why Modifying $C_{i-1}$ Works

The vulnerability stems directly from the CBC decryption equation:
$$P'_i = D_K(C_i) \oplus C'_{i-1} = I_i \oplus C'_{i-1}$$

Notice that:
1. $I_i = D_K(C_i)$ is **completely constant** because $C_i$ and the key $K$ do not change.
2. Modifying byte $j$ in the preceding ciphertext block $C'_{i-1}[j]$ **directly flips the exact same byte** in the decrypted block $P'_i[j]$:
   $$P'_i[j] = I_i[j] \oplus C'_{i-1}[j]$$

By crafting specific values for $C'_{i-1}$, an attacker can systematically force $P'_i$ to end with valid PKCS#7 padding values.

---

## ⚙️ Byte-by-Byte Right-to-Left Recovery Algorithm

To decrypt target block $C_i$ using previous block $C_{i-1}$ (for $C_1$, $C_0 = IV$):

We recover bytes from **right to left** (index $j = 15, 14, \dots, 0$):

1. **Target Padding Value**: $\text{pad\_val} = 16 - j$.
2. **Tail Adjustment**: For all bytes already recovered ($k = j + 1 \dots 15$), we set:
   $$C'_{i-1}[k] = I_i[k] \oplus \text{pad\_val}$$
   This guarantees that the decrypted tail $P'_i[k] = \text{pad\_val}$.
3. **Byte Guessing**: We iterate guess $g \in [0, 255]$ for $C'_{i-1}[j]$:
   $$C'_{i-1}[j] = g$$
   and send $(C'_{i-1}, C_i)$ to the padding oracle.
4. **Oracle Response**:
   When the oracle returns `True`:
   $$P'_i[j] = \text{pad\_val}$$
   $$I_i[j] \oplus g = \text{pad\_val} \implies I_i[j] = g \oplus \text{pad\_val}$$
5. **Plaintext Extraction**:
   With $I_i[j]$ known, the original plaintext byte is recovered instantly:
   $$P_i[j] = I_i[j] \oplus C_{i-1}[j]$$

*(Note: When $\text{pad\_val} = 1$, an accidental multi-byte padding like `0x02 0x02` is disambiguated by flipping byte $j-1$ and re-querying).*

---

## 📊 Attack Complexity & Query Analysis

| Metric | Traditional Brute Force | Padding Oracle Attack |
| :--- | :--- | :--- |
| **Search Space** | All $2^{128}$ possible keys | 256 guesses per byte |
| **Query Complexity** | $O(2^{128}) \approx 3.4 \times 10^{38}$ | $O(256 \times N)$ where $N$ is byte length |
| **Average Queries / Byte** | $\sim 2^{127}$ | **$\sim 128$ queries / byte** |
| **Execution Time** | Billions of years | **< 1 second** |

### Experimental Results on Sample Run
- **Ciphertext Length**: 80 bytes (5 blocks: $IV, C_1, C_2, C_3, C_4, C_5$)
- **Total Plaintext Recovered**: 67 bytes (unpadded)
- **Total Oracle Queries**: 9,747 queries
- **Observed Average Queries / Byte**: **121.84** (closely matches theoretical $\approx 128$)
- **Recovered Plaintext**:
  ```text
  Cryptography Lab 7: Padding Oracle Attack demonstration on AES-CBC!
  ```

---

## 🛡️ Security Recommendations & Countermeasures

Padding oracle vulnerabilities can be prevented by adopting the following best practices:

### 1. Use Authenticated Encryption with Associated Data (AEAD) *(Recommended)*
- Replace unauthenticated CBC mode with modern AEAD ciphers such as:
  - **AES-GCM** (Galois/Counter Mode)
  - **ChaCha20-Poly1305**
- AEAD ciphers compute a cryptographic authentication tag over both the ciphertext and metadata. If ciphertext tampering occurs, the authentication tag fails and decryption is aborted before any padding check occurs.

### 2. Implement Encrypt-then-MAC (EtM)
- If CBC mode must be used (e.g. legacy system constraints), compute a Message Authentication Code (HMAC-SHA256) over $(IV \parallel \text{Ciphertext})$.
- **Verification Rule**: Verify the HMAC in constant time **before** decrypting or examining padding. If the MAC is invalid, discard the message immediately.

### 3. Uniform Error Handling & Constant-Time Processing
- Never return distinct error messages for padding errors vs decryption or integrity errors.
- Return a single generic error (e.g. `400 Bad Request` or `Decryption Failed`).
- Ensure padding checking executes in constant time to prevent timing-based side channels.

---

## 🚀 How to Run the Program

```bash
# Run the complete padding oracle attack demonstration
python3 Padding_Oracle_Attack/padding_oracle.py
```
