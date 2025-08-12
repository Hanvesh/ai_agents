class MissingParameterException(Exception):
    def __init__(self, parameter_name):
        self.parameter_name = parameter_name
        self.message = f"The parameter '{parameter_name}' is missing or empty."
        super().__init__(self.message)