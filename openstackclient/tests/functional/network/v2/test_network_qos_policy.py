# Copyright (c) 2016, Intel Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

from openstackclient.tests.functional.network.v2 import common


class NetworkQosPolicyTests(common.NetworkTests):
    """Functional tests for QoS policy. """
    NAME = uuid.uuid4().hex
    HEADERS = ['Name']
    FIELDS = ['name']

    @classmethod
    def setUpClass(cls):
        common.NetworkTests.setUpClass()
        if cls.haz_network:
            opts = cls.get_opts(cls.FIELDS)
            raw_output = cls.openstack(
                'network qos policy create ' +
                cls.NAME +
                opts
            )
            cls.assertOutput(cls.NAME + "\n", raw_output)

    @classmethod
    def tearDownClass(cls):
        if cls.haz_network:
            raw_output = cls.openstack(
                'network qos policy delete ' +
                cls.NAME
            )
            cls.assertOutput('', raw_output)

    def setUp(self):
        super(NetworkQosPolicyTests, self).setUp()
        # Nothing in this class works with Nova Network
        if not self.haz_network:
            self.skipTest("No Network service present")

    def test_qos_policy_list(self):
        opts = self.get_opts(self.HEADERS)
        raw_output = self.openstack('network qos policy list' + opts)
        self.assertIn(self.NAME, raw_output)

    def test_qos_policy_show(self):
        opts = self.get_opts(self.FIELDS)
        raw_output = self.openstack('network qos policy show ' + self.NAME +
                                    opts)
        self.assertEqual(self.NAME + "\n", raw_output)

    def test_qos_policy_set(self):
        self.openstack('network qos policy set --share ' + self.NAME)
        opts = self.get_opts(['shared'])
        raw_output = self.openstack('network qos policy show ' + self.NAME +
                                    opts)
        self.assertEqual("True\n", raw_output)

    def test_qos_policy_default(self):
        self.openstack('network qos policy set --default ' + self.NAME)
        opts = self.get_opts(['is_default'])
        raw_output = self.openstack('network qos policy show ' + self.NAME +
                                    opts)
        self.assertEqual("True\n", raw_output)

        self.openstack('network qos policy set --no-default ' + self.NAME)
        opts = self.get_opts(['is_default'])
        raw_output = self.openstack('network qos policy show ' + self.NAME +
                                    opts)
        self.assertEqual("False\n", raw_output)
