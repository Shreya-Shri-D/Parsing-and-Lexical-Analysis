#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

void removeNonAlpha(std::string &str) {
    str.erase(std::remove_if(str.begin(), str.end(), [](char c) { return !std::isalpha(c); }), str.end());
    std::transform(str.begin(), str.end(), str.begin(), ::tolower);
}

bool isPalindrome(const std::string &str) {
    int left = 0;
    int right = str.length() - 1;
    while (left < right) {
        if (str[left] != str[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}

int main() {
    std::string sentence;
    std::cout << "Enter a sentence: ";
    std::getline(std::cin, sentence);

    removeNonAlpha(sentence);
    if (isPalindrome(sentence)) {
        std::cout << "The sentence is a palindrome." << std::endl;
    } else {
        std::cout << "The sentence is not a palindrome." << std::endl;
    }
    return 0;
}