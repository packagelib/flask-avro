# Flask Avro
This is a simple AVRO IPC endpoint registration extension for Flask.

For information about AVRO checkout:

* [https://avro.apache.org/](https://avro.apache.org/)
* [http://avro.apache.org/docs/current/spec.html](http://avro.apache.org/docs/current/spec.html)

# Usage
This extension allows you to register a AVRO protocol to a specific URL route. This allows you to handle the messages defined in the protocol.

Given a AVRO protocol `test.avpr`:

```
{
    "namespace": "org.avro",
    "protocol": "Test",

    "types": [
        {
            "name": "Message",
            "type": "record",
            "fields": [
                {
                    "name": "from",
                    "type": "string"
                },
                {
                    "name": "body",
                    "type": "string"
                }
            ]
        }
    ],

    "messages": {
        "echo_message": {
            "request": [
                {
                    "name":"message",
                    "type":"Message"
                }
            ],
            "response": "string",
            "errors": []
        }
    }
}
```

An example of a simple Flask app that implements logic for the message `echo_message`, you could do the following:

```
from flask import Flask
from flask.ext.avro import FlaskAvroEndpoint

test_avro_endpoint = FlaskAvroEndpoint.from_filename("test", "test.avpr")

@test_avro_endpoint.register("echo_message"):
def handle_test_send(request_message):

    return request_message.get("body")


app = Flask(__name__)

test_avro_endpoint.connect(app, "/")
    
```

The above code registers a function that will handle the request message when the endpoint receives a message for `echo_message`. The function is responsible for also returning the correct object that is required as response of the protocol.

In order to interact with endpoint, the client would use the AVRO IPC `Requestor` API for your specific language.

For Python, you'll have to install the `avro` package with pip and then your client could look like this:

```
from avro.protocol import protocol
from avro.ipc import Requestor, HTTPTransceiver


TEST_PROTOCOL = protocol.parse(open("test.avpr").read()) 
client = HTTPTransceiver("localhost", 9090)
requestor = Requestor(TEST_PROTOCOL, client)

test_message = {
    "from": "Ground Control",
    "body": "Take your protein pills and put your helmet on"
}


response = requestor.request("echo_message", test_message)

client.close()
```

# Test Helpers

This module also includes a test helper to test your Avro endpoints. Normally, when you test your views, you'll want to use the `test_flask_app.test_client()` to generate requests to your view endpoints. However, creating AVRO request messages is a little cumbersome.

To help facilitate testing, there is a test utility class `flask.ext.avro.util.FlaskAvroTestClient`. This is a convenience wrapper around the test_client.

Example usage:

```
from unittest import TestCase
from flask.ext.avro.util import FlaskAvroTestClient

from avro.protocol import protocol

TEST_PROTOCOL = protocol.parse(open("test.avpr").read()) 

class TestAvroEndpoint(TestCase):

    def setUp(self):
        # Generate your test app or pull a created one
        ...
        self.app = test_app
    
    def test_endpoint(self):
    
        client = FlaskAvroTestClient(TEST_PROTOCOL, self.app.test_client(), "/")
        
        test_body = "Take your protein pills and put your helmet on"
        test_message = test_message = {
            "from": "Ground Control",
            "body": test_body
        }
        
        response = client.request("echo_message", test_message)
        
        self.assertEqual(test_body, response)

```

