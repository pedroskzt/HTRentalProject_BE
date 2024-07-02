from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class AlphabeticalPasswordValidator:
    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError(
                _("This password is entirely alphabetical"),
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 numeric character.")


class SpecialCharacterPasswordValidator:
    def __init__(self, special_character_string="!@#$()-+?_=,<>/"):
        self.special_character_string = special_character_string

    def validate(self, password, user=None):
        for character in self.special_character_string:
            if character in password:
                break
        else:
            raise ValidationError(
                _(f"Password is missing a special character: {self.special_character_string}"),
                code="password_missing_special_character",
                params={"special_character_string": self.special_character_string},
            )


    def get_help_text(self):
        return _(
            f"Password must contain at least one special character: {self.special_character_string}"
            % {"special_character_string": self.special_character_string}
        )
