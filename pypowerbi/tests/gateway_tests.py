# -*- coding: future_fstrings -*-

import json
from unittest import TestCase

from pypowerbi.gateway import *


class GatewayTests(TestCase):

    def test_gateway_json(self):

        gateway = Gateway(name=f'testGateway')
        self.assertIsNotNone(gateway)

        gateway_json = json.dumps(gateway, cls=GatewayEncoder)
        self.assertIsNotNone(gateway_json)

        expected_json = '{' \
                          '"name": "testGateway", ' \
                        '}'

        self.assertEqual(gateway_json, expected_json)
