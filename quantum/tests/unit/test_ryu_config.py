# Copyright (c) 2012 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import unittest

from quantum.openstack.common import cfg
from quantum.plugins.ryu.common import config


class RyuConfigTestCase(unittest.TestCase):
    def test_config(self):
        configs = """[DATABASE]
sql_connection = testlink
reconnect_interval=100
[OVS]
enable_tunneling = True
integration_bridge = mybrint
local_ip = 10.0.0.3
[AGENT]
root_helper = mysudo
polling_interval=50
"""

        (fd, path) = tempfile.mkstemp(prefix='ryu_config', suffix='.ini')

        try:
            os.write(fd, configs)
            os.close(fd)

            conf = config.parse(path)
            self.assertEqual('mybrint', conf.OVS.integration_bridge)
            self.assertEqual('testlink', conf.DATABASE.sql_connection)
            self.assertEqual(100, conf.DATABASE.reconnect_interval)
            self.assertEqual(50, conf.AGENT.polling_interval)
            self.assertEqual('mysudo', conf.AGENT.root_helper)
            self.assertEqual(conf.OVS.integration_bridge,
                             cfg.CONF.OVS.integration_bridge)
        finally:
            os.remove(path)

    def test_defaults(self):
        configs = """
"""

        (fd, path) = tempfile.mkstemp(prefix='ryu_config', suffix='.ini')

        try:
            os.write(fd, configs)
            os.close(fd)

            conf = config.parse(path)
            self.assertEqual('br-int', conf.OVS.integration_bridge)
            self.assertEqual('sqlite://', conf.DATABASE.sql_connection)
            self.assertEqual(2, conf.DATABASE.reconnect_interval)
            self.assertEqual(2, conf.AGENT.polling_interval)
            self.assertEqual('sudo', conf.AGENT.root_helper)
            self.assertEqual('127.0.0.1:6633', conf.OVS.openflow_controller)
            self.assertEqual('127.0.0.1:8080', conf.OVS.openflow_rest_api)
            self.assertEqual(conf.DATABASE.sql_connection,
                             cfg.CONF.DATABASE.sql_connection)
            self.assertEqual(conf.AGENT.root_helper,
                             cfg.CONF.AGENT.root_helper)
        finally:
            os.remove(path)

    def tearDown(self):
        """Clear the test environment"""
        cfg.CONF.reset()
        cfg.CONF.unregister_opts(config.database_opts, "DATABASE")
        cfg.CONF.unregister_opts(config.ovs_opts, "OVS")
        cfg.CONF.unregister_opts(config.agent_opts, "AGENT")
