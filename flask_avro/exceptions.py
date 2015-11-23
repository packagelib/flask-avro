
class FlaskAvroException(Exception):
    """
    Top level exception for this module.
    """


class AvroMessageNotDefined(FlaskAvroException):
    """
    When trying to register a message in the protocol that is not defined.
    """


class AvroMessageNotImplemented(FlaskAvroException):
    """
    When a client tries to call a message that is not currently implemented by the endpoint.
    """
