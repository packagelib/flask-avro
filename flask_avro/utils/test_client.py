"""
Helper class for wrapping the test client object from Flask in order to hit Avro endpoints in a
test context.
"""
from io import BytesIO
from StringIO import StringIO as StringReader
from flask_avro.endpoint import AVRO_CONTENT_TYPE
from avro.ipc import FramedReader, FramedWriter, Requestor


class FlaskAvroTestClient(Requestor):
    """
    Flask wrapper for the Avro Requestor object. This allows you to communicate with the Flask stack in
    a tests environment. This simplifies testing your endpoints.
    """

    def __init__(self, local_protocol, flask_client, endpoint_url):

        client = FlaskTestClientTransceiver(flask_client, endpoint_url)
        super(FlaskAvroTestClient, self).__init__(local_protocol, client)


class FlaskTestClientTransceiver(object):
    """
    This implements the transceive method that is used by the Requestor. It is responsible for serializing
    the request and response data.
    """

    def __init__(self, flask_client, endpoint_url):
        self.client = flask_client
        self.url = endpoint_url

    @property
    def remote_name(self):
        return "localhost"

    def transceive(self, request):

        with BytesIO() as _b:
            req_body_buffer = FramedWriter(_b)
            req_body_buffer.write_framed_message(request)
            req_body = _b.getvalue()

        response = self.client.post(
            self.url,
            data=req_body,
            content_type=AVRO_CONTENT_TYPE
        )

        avro_reader = FramedReader(StringReader(response.data))
        framed_message = avro_reader.read_framed_message()
        return framed_message

