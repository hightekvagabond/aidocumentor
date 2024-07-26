# string_operations.py

def reverse_string(s):
    """
    Reverse the given string.
    """
    return s[::-1]

def count_vowels(s):
    """
    Count the number of vowels in the given string.
    """
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)

def capitalize_words(s):
    """
    Capitalize the first letter of each word in the given string.
    """
    return ' '.join(word.capitalize() for word in s.split())

def main():
    test_string = "hello world"
    print(f"Original string: {test_string}")
    print(f"Reversed: {reverse_string(test_string)}")
    print(f"Vowel count: {count_vowels(test_string)}")
    print(f"Capitalized: {capitalize_words(test_string)}")

if __name__ == "__main__":
    main()