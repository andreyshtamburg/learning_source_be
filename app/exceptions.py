class FieldValidationException(Exception):
    """
    Exception to handle field validation errors
    """
    def __init__(self, message='Field validation error', error_field_name='unknown_field', exception_map=None, *args, **kwargs):
        super().__init__(args, **kwargs)
        self.exception_map = exception_map
        self.error_field_name = error_field_name
        self.message = message
