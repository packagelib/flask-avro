import io

from avro import protocol as a_protocol
from avro.ipc import Responder, FramedReader, FramedWriter
from flask import request, current_app
from flask_avro.exceptions import AvroMessageNotDefined


AVRO_CONTENT_TYPE = "avro/binary"
AVRO_HTTP_METHOD = "POST"


class FlaskAvroEndpoint(Responder):
    """
    Used register avro protocol with view functions.
    """

    def __init__(self, endpoint_name, protocol):
        super(FlaskAvroEndpoint, self).__init__(protocol)

        self.message_handlers = {}
        self.endpoint_name = endpoint_name

    @staticmethod
    def from_filename(endpoint_name, protocol_file_path):
        """
        Creates a AvroAPIEndpoint from protocol file identified by the protocol_file_path.

        :param endpoint_name: The name of the endpoint.
        :param protocol_file_path: The path to the specific protocol file to parse.
        :return: The AvroAPIEndpoint
        :rtype: user_service.helpers.avro.AvroAPIEndpoint
        """

        with open(protocol_file_path) as _file:
            protocol = a_protocol.parse(_file.read())

        endpoint = FlaskAvroEndpoint(endpoint_name, protocol)

        return endpoint

    def register(self, message_name):
        """
        Decorator used to register a function to a specific message in the Avro Protocol. The registered function
        should expect to receive the correct Avro message request. The registered function should also return the
        expected response message.

        :param message_name: The name of protocol message to register.
        :return: The registration function.
        """

        def register_function(fn):
            if message_name not in self.local_protocol.messages:
                raise AvroMessageNotDefined(
                    "Message [{}] not defined in protocol.".format(message_name)
                )

            self.message_handlers[message_name] = fn
            return fn

        return register_function

    def handle_request(self):
        """
        This is the function that is called when the flask route is hit. This is responsible parsing the flask request
        and feeding it into the Avro Protocol object.

        :return: The response or fault response.
        """

        avro_reader = FramedReader(request.stream)
        call_request = avro_reader.read_framed_message()

        response_message = self.respond(call_request)

        with io.BytesIO() as _avro_body:
            avro_writer = FramedWriter(_avro_body)
            avro_writer.write_framed_message(response_message)
            response_body = _avro_body.getvalue()

        return current_app.response_class(
            response_body,
            content_type=AVRO_CONTENT_TYPE
        )

    def invoke(self, local_message, request_message):
        """
        Dispatches the message to the correct handler.

        :param local_message: The local message sent to the endpoint.
        :param request_message: The avro request data message as a dictionary.
        :return: The response body.
        """

        message_name = local_message.name
        handler = self.message_handlers.get(message_name)

        if handler is None:
            raise NotImplemented(
                "Message [{}] not implemented by the current endpoint.".format(local_message)
            )

        return handler(request_message)

    def connect(self, flask_app, url_rule):
        """
        Connects the endpoint with a specific flask application. The rule is the URL rule to follow to access
        this endpoint.

        :param flask_app: The flask app
        :param url_rule: The URL rule to use to attach the endpoint.
        """
        flask_app.add_url_rule(url_rule, self.endpoint_name, self.handle_request, methods=[AVRO_HTTP_METHOD])
