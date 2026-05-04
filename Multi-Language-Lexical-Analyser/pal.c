#include <stdio.h>
#include <string.h>
#include <ctype.h>

void removeNonAlpha(char* str) {
    int i, j = 0;
    char temp[strlen(str) + 1];
    for (i = 0; str[i] != '\0'; i++) {
        if (isalpha(str[i])) {
            temp[j++] = tolower(str[i]);
        }
    }
    temp[j] = '\0';
    strcpy(str, temp);
}

int isPalindrome(char* str) {
    int left = 0;
    int right = strlen(str) - 1;
    while (left < right) {
        if (str[left] != str[right]) {
            return 0;
        }
        left++;
        right--;
    }
    return 1;
}

int main() {
    char sentence[1000];
    printf("Enter a sentence: ");
    fgets(sentence, sizeof(sentence), stdin);
    sentence[strcspn(sentence, "\n")] = '\0';  // Remove the newline character

    removeNonAlpha(sentence);
    if (isPalindrome(sentence)) {
        printf("The sentence is a palindrome.\n");
    } else {
        printf("The sentence is not a palindrome.\n");
    }
    return 0;
}
