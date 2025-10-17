from rest_framework.exceptions import APIException

class ServiceError(APIException):
    def __init__(self, error_message, status_code=500):
        self.error_message = error_message
        self.status_code = status_code
        super().__init__(error_message)