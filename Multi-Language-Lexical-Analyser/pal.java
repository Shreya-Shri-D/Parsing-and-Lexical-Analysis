import java.util.Scanner;

public class PalindromeChecker {

    public static String removeNonAlpha(String str) {
        StringBuilder cleaned = new StringBuilder();
        for (char c : str.toCharArray()) {
            if (Character.isLetter(c)) {
                cleaned.append(Character.toLowerCase(c));
            }
        }
        return cleaned.toString();
    }

    public static boolean isPalindrome(String str) {
        int left = 0;
        int right = str.length() - 1;
        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter a sentence: ");
        String sentence = scanner.nextLine();
        scanner.close();

        String cleanedSentence = removeNonAlpha(sentence);
        if (isPalindrome(cleanedSentence)) {
            System.out.println("The sentence is a palindrome.");
        } else {
            System.out.println("The sentence is not a palindrome.");
        }
    }
}
