# author: z4yt0s
# date: 02.29.2024
# github: https://github.com/z4yt0s/csp

from typing import ClassVar, Tuple, List, Dict

class CreateSecurePasswords:
    """
    CreateSecurePasswords: Handles the creation of strong passwords based on a]
    given phrase pattern.

    Attrubutes:
        DICTIONARY_LETTER (ClassVar[Dict[str, str]]): A dictionary mapping specific
        letters to their corresponding replacements for creating strong passwords.
    """
    DICTIONARY_LETTER: ClassVar[Dict[str, str]] = {
        'a': '4',
        'e': '3',
        'i': '1',
        'o': '0',
        'u': '()',
        's': '$',
    }

    def __init__(self, password: str, separator: str) -> None:
        """
        Initialize the instance of class CreateSecurePassword.

        Args:
            password (str): The password to be strengthened.
            separator (str): The character used as a separator between words.
        
        Attributes:
            chars (Tuple[List[str]]): A tuple contanining list of character obteining
            by splitting the input password using the specified separator
        """
        self.chars: Tuple[List[str]] = [
            [*word] for word in password.split(separator)
        ]

    def create_strong_pass(self) -> str:
        """
        Generate a strong psasword based on the given phrase pattern.

        Returns:
            str: The generated strong password
            
        Description:
            The method iterates throught the characters in each word of the password
            replacing specific letters according to the predifined DICTIONARY_LETTER.
            It also capitalizes the firts letter in each word for additional strength.
        """
        dict_letter = CreateSecurePasswords.DICTIONARY_LETTER
        password: str = ''
        for chars in self.chars:
            caps: bool = False
            for char in chars:
                if char in dict_letter.keys():
                    password += dict_letter.get(char)
                    continue
                if not caps:
                    caps = True
                    password += char.capitalize()
                    continue
                password += char
        return password