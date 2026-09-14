#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <iomanip>

using namespace std;

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

string create_key() {
return "QWERTYUIOPASDFGHJKLZXCVBNM";
}

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
        ciphertext += ch;
    }
}

return ciphertext;

}

void save_ciphertext(string ciphertext) {
ofstream file("ciphertext.txt");

if (!file) {
    cout << "Error: Could not create ciphertext.txt" << endl;
    return;
}

file << ciphertext;

file.close();


}

void frequency_analysis(string ciphertext) {


int frequency[26] = {0};
int total_letters = 0;

for (char ch : ciphertext) {

    if (isalpha(ch)) {

        char upper_ch = toupper(ch);
        int index = upper_ch - 'A';

        frequency[index]++;
        total_letters++;
    }
}

char letters[26];
int counts[26];

for (int i = 0; i < 26; i++) {
    letters[i] = 'A' + i;
    counts[i] = frequency[i];
}

for (int i = 0; i < 25; i++) {

    for (int j = i + 1; j < 26; j++) {

        if (counts[j] > counts[i]) {

            int temp_count = counts[i];
            counts[i] = counts[j];
            counts[j] = temp_count;

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

cout << "\nMost frequent ciphertext letter(s): ";

int highest = counts[0];

for (int i = 0; i < 26; i++) {

    if (counts[i] == highest) {
        cout << letters[i] << " ";
    }
}

cout << endl;

cout << "Highest frequency: " << highest << endl;

cout << "Total alphabetic characters: "
     << total_letters << endl;


}

void word_frequency_analysis(string ciphertext) {


string words[500];
int counts[500] = {0};

int word_count = 0;
string current_word = "";

for (int i = 0; i <= (int)ciphertext.length(); i++) {

    char ch = '\0';

    if (i < (int)ciphertext.length()) {
        ch = ciphertext[i];
    }

    if (isalpha(ch)) {

        current_word += toupper(ch);
    }
    else {

        if (current_word != "") {

            int found = -1;

            for (int j = 0; j < word_count; j++) {

                if (words[j] == current_word) {
                    found = j;
                    break;
                }
            }

            if (found == -1) {

                words[word_count] = current_word;
                counts[word_count] = 1;
                word_count++;
            }
            else {

                counts[found]++;
            }

            current_word = "";
        }
    }
}

cout << "\n--- Word Frequency Analysis ---" << endl;

cout << "\nOne-letter words:" << endl;

bool found_one = false;

for (int i = 0; i < word_count; i++) {

    if (words[i].length() == 1) {

        cout << words[i] << " -> "
             << counts[i] << endl;

        found_one = true;
    }
}

if (!found_one) {
    cout << "None" << endl;
}

cout << "\nTwo-letter words:" << endl;

bool found_two = false;

for (int i = 0; i < word_count; i++) {

    if (words[i].length() == 2) {

        cout << words[i] << " -> "
             << counts[i] << endl;

        found_two = true;
    }
}

if (!found_two) {
    cout << "None" << endl;
}

cout << "\nThree-letter words:" << endl;

bool found_three = false;

for (int i = 0; i < word_count; i++) {

    if (words[i].length() == 3) {

        cout << words[i] << " -> "
             << counts[i] << endl;

        found_three = true;
    }
}

if (!found_three) {
    cout << "None" << endl;
}

cout << "\nRepeated words:" << endl;

bool repeated_found = false;

for (int i = 0; i < word_count; i++) {

    if (counts[i] > 1) {

        cout << words[i] << " -> "
             << counts[i] << endl;

        repeated_found = true;
    }
}

if (!repeated_found) {
    cout << "No repeated words found." << endl;
}


}

string get_pattern(string word) {


string pattern = "";

int pattern_number[26];

for (int i = 0; i < 26; i++) {
    pattern_number[i] = -1;
}

int next_number = 0;

for (int i = 0; i < (int)word.length(); i++) {

    int index = word[i] - 'A';

    if (pattern_number[index] == -1) {

        pattern_number[index] = next_number;
        next_number++;
    }

    pattern += char('0' + pattern_number[index]);
}

return pattern;


}

void pattern_analysis(string ciphertext) {


string words[500];
string patterns[500];

int word_count = 0;
string current_word = "";

for (int i = 0; i <= (int)ciphertext.length(); i++) {

    char ch = '\0';

    if (i < (int)ciphertext.length()) {
        ch = ciphertext[i];
    }

    if (isalpha(ch)) {

        current_word += toupper(ch);
    }
    else {

        if (current_word != "") {

            words[word_count] = current_word;
            patterns[word_count] = get_pattern(current_word);

            word_count++;

            current_word = "";
        }
    }
}

cout << "\n--- Repeated Letter Pattern Analysis ---" << endl;

bool repeated_found = false;

for (int i = 0; i < word_count; i++) {

    int occurrence = 1;

    for (int j = i + 1; j < word_count; j++) {

        if (patterns[i] == patterns[j]) {
            occurrence++;
        }
    }

    if (occurrence > 1) {

        bool already_printed = false;

        for (int k = 0; k < i; k++) {

            if (patterns[k] == patterns[i]) {

                already_printed = true;
                break;
            }
        }

        if (!already_printed) {

            cout << "Pattern "
                 << patterns[i]
                 << ": ";

            for (int j = 0; j < word_count; j++) {

                if (patterns[j] == patterns[i]) {
                    cout << words[j] << " ";
                }
            }

            cout << endl;

            repeated_found = true;
        }
    }
}

if (!repeated_found) {
    cout << "No repeated patterns found." << endl;
}

}

int main() {


string plaintext = read_plaintext();

if (plaintext == "") {
    return 1;
}

string key = create_key();

string ciphertext = encrypt(plaintext, key);

save_ciphertext(ciphertext);

cout << "Monoalphabetic substitution cipher "
     << "applied successfully." << endl;

cout << "\nPlain alphabet : "
     << "ABCDEFGHIJKLMNOPQRSTUVWXYZ" << endl;

cout << "Cipher alphabet: "
     << key << endl;

cout << "\nCiphertext saved to ciphertext.txt"
     << endl;

cout << "\nCiphertext preview:\n";

if (ciphertext.length() > 300) {

    cout << ciphertext.substr(0, 300)
         << "..." << endl;
}
else {

    cout << ciphertext << endl;
}

frequency_analysis(ciphertext);

word_frequency_analysis(ciphertext);

pattern_analysis(ciphertext);

return 0;


}
