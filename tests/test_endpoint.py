import os
import unittest
from flask import Flask
from tests import TEST_DIR

from flask_avro import FlaskAvroEndpoint
from flask_avro import AvroMessageNotDefined

from flask_avro.utils.test_client import FlaskAvroTestClient


AVRO_FILE = os.path.join(TEST_DIR, "avro_schema", "test_avro_schema.avpr")


class TestAvroAPIEndpoint(unittest.TestCase):

    def test_cannot_register_unknown_message(self):

        unknown_message_name = "blahblah"
        avro_endpoint = FlaskAvroEndpoint.from_filename(
            "tests",
            AVRO_FILE
        )

        self.assertNotIn(
            unknown_message_name,
            avro_endpoint.local_protocol.messages,
            "Message should not be in the protocol."
        )

        with self.assertRaises(AvroMessageNotDefined):
            @avro_endpoint.register(unknown_message_name)
            def unknown_message_handler():
                pass

    def test_successfully_register_and_handle_message(self):

        known_message_name = "test_send"
        avro_endpoint = FlaskAvroEndpoint.from_filename(
            "tests",
            AVRO_FILE
        )

        self.assertIn(
            known_message_name,
            avro_endpoint.local_protocol.messages,
            "Message should be contained in the protocol."
        )

        expected_to = "Alex"
        expected_from = "Jeff"
        expected_body = "Join me for a beer?"
        expected_response = "Why, of course my good sir!"

        @avro_endpoint.register(known_message_name)
        def handle_test_send(test_message):

            message = test_message["message"]

            self.assertEqual(
                expected_to,
                message["to"],
                "Expected a message to Alex"
            )
            self.assertEqual(
                expected_from,
                message["from"],
                "Expected a message from Jeff"
            )
            self.assertEqual(
                expected_body,
                message["body"]
            )

            return expected_response

        registered_endpoint = "/tests"
        flask_app = Flask(__name__)
        avro_endpoint.connect(flask_app, registered_endpoint)

        client = FlaskAvroTestClient(avro_endpoint.local_protocol, flask_app.test_client(), registered_endpoint)

        request_data = {
            "to": expected_to,
            "from": expected_from,
            "body": expected_body
        }

        response = client.request(known_message_name, {"message": request_data})

        self.assertEqual(expected_response, response)
