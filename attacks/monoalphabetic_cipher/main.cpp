#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <iomanip>
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

// Perform frequency analysis on ciphertext
void frequency_analysis(string ciphertext) {
    int frequency[26] = {0};
    int total_letters = 0;

    // Count frequency of each alphabetic character
    for (char ch : ciphertext) {
        if (isalpha(ch)) {
            char upper_ch = toupper(ch);
            int index = upper_ch - 'A';

            frequency[index]++;
            total_letters++;
        }
    }

    // Store letters and their frequencies
    char letters[26];
    int counts[26];

    for (int i = 0; i < 26; i++) {
        letters[i] = 'A' + i;
        counts[i] = frequency[i];
    }

    // Sort letters by frequency in descending order
    for (int i = 0; i < 25; i++) {
        for (int j = i + 1; j < 26; j++) {

            if (counts[j] > counts[i]) {

                // Swap frequency
                int temp_count = counts[i];
                counts[i] = counts[j];
                counts[j] = temp_count;

                // Swap corresponding letter
                char temp_letter = letters[i];
                letters[i] = letters[j];
                letters[j] = temp_letter;
            }
        }
    }

    cout << "\n--- Ciphertext Letter Frequency Analysis ---" << endl;

    cout << "\nLetter\tCount\tPercentage" << endl;
    cout << "-----------------------------" << endl;

    for (int i = 0; i < 26; i++) {

        double percentage = 0;

        if (total_letters > 0) {
            percentage = (counts[i] * 100.0) / total_letters;
        }

        cout << letters[i] << "\t"
             << counts[i] << "\t"
             << fixed << setprecision(2)
             << percentage << "%" << endl;
    }

    // Identify the most frequent letter(s)
    cout << "\nMost frequent ciphertext letter(s): ";

    int highest = counts[0];

    for (int i = 0; i < 26; i++) {
        if (counts[i] == highest) {
            cout << letters[i] << " ";
        }
    }

    cout << endl;
    cout << "Highest frequency: " << highest << endl;
    cout << "Total alphabetic characters: " << total_letters << endl;
}

int main() {

    // Step 1: Read plaintext
    string plaintext = read_plaintext();

    if (plaintext.empty()) {
        cout << "Plaintext is empty." << endl;
        return 1;
    }

    // Step 2: Create substitution key
    string key = create_key();

    // Step 3: Encrypt plaintext
    string ciphertext = encrypt(plaintext, key);

    // Step 4: Save ciphertext
    save_ciphertext(ciphertext);

    cout << "Monoalphabetic substitution cipher applied successfully."
         << endl;

    // Display substitution key
    cout << "\n--- Substitution Key ---" << endl;
    cout << "Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ" << endl;
    cout << "Cipher: " << key << endl;

    cout << "\nCiphertext saved to ciphertext.txt" << endl;

    // Display ciphertext preview
    cout << "\n--- Ciphertext Preview ---" << endl;

    if (ciphertext.length() > 500) {
        cout << ciphertext.substr(0, 500) << "..." << endl;
    }
    else {
        cout << ciphertext << endl;
    }

    // Step 5: Perform frequency analysis
    frequency_analysis(ciphertext);

    return 0;
}