from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class NumericPasswordValidator:
    def validate(self, password, user=None):
        if not password.isdigit():
            raise ValidationError(
                _("This password must contain only numbers."),
                code='password_no_numbers',
            )

    def get_help_text(self):
        return _("Your password must contain only numbers.")
