#include <iostream>
#include <fstream>
#include <string>
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

int main() {
    string plaintext = read_plaintext();

    if (plaintext.empty()) {
        cout << "Plaintext is empty." << endl;
        return 1;
    }

    cout << "Plaintext loaded successfully." << endl;
    cout << "Plaintext length: " << plaintext.length() << " characters" << endl;

    cout << "\n--- Plaintext ---\n";
    cout << plaintext << endl;

    return 0;
}