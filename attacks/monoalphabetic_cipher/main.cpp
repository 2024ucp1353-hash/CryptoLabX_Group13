#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
using namespace std;

// Read plaintext from file
string read_plaintext() {
    ifstream file("plaintext.txt");

    if (!file) {
        cout << "Error: Could not open plaintext.txt" << endl;
        return "";
    }

    string text;
    string line;

    while (getline(file, line)) {
        text += line;
        text += '\n';
    }

    file.close();
    return text;
}

// Create a fixed monoalphabetic substitution key
string create_key() {
    return "QWERTYUIOPASDFGHJKLZXCVBNM";
}

// Encrypt plaintext using the substitution key
string encrypt(string plaintext, string key) {
    string ciphertext = "";

    for (char ch : plaintext) {
        if (isalpha(ch)) {
            bool is_upper = isupper(ch);

            char upper_ch = toupper(ch);
            int index = upper_ch - 'A';

            char encrypted_char = key[index];

            if (!is_upper) {
                encrypted_char = tolower(encrypted_char);
            }

            ciphertext += encrypted_char;
        }
        else {
            // Keep spaces, punctuation and numbers unchanged
            ciphertext += ch;
        }
    }

    return ciphertext;
}

// Save ciphertext to file
void save_ciphertext(string ciphertext) {
    ofstream file("ciphertext.txt");

    if (!file) {
        cout << "Error: Could not create ciphertext.txt" << endl;
        return;
    }

    file << ciphertext;
    file.close();
}

int main() {
    string plaintext = read_plaintext();

    if (plaintext.empty()) {
        cout << "Plaintext is empty." << endl;
        return 1;
    }

    string key = create_key();

    string ciphertext = encrypt(plaintext, key);

    save_ciphertext(ciphertext);

    cout << "Monoalphabetic substitution cipher applied successfully." << endl;

    cout << "\n--- Substitution Key ---" << endl;
    cout << "Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ" << endl;
    cout << "Cipher: " << key << endl;

    cout << "\nCiphertext saved to ciphertext.txt" << endl;

    cout << "\n--- Ciphertext Preview ---" << endl;

    // Display first 500 characters
    if (ciphertext.length() > 500)
        cout << ciphertext.substr(0, 500) << "..." << endl;
    else
        cout << ciphertext << endl;

    return 0;
}
