# Copyright (c) 2013 OpenStack Foundation
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

from neutron.common import constants
from neutron.extensions import portbindings
from neutron.openstack.common import log
from neutron.plugins.ml2 import driver_api as api
from neutron.plugins.ml2.drivers import mech_agent

LOG = log.getLogger(__name__)


class LinuxbridgeMechanismDriver(mech_agent.AgentMechanismDriverBase):
    """Attach to networks using linuxbridge L2 agent.

    The LinuxbridgeMechanismDriver integrates the ml2 plugin with the
    linuxbridge L2 agent. Port binding with this driver requires the
    linuxbridge agent to be running on the port's host, and that agent
    to have connectivity to at least one segment of the port's
    network.
    """

    def __init__(self):
        super(LinuxbridgeMechanismDriver, self).__init__(
            constants.AGENT_TYPE_LINUXBRIDGE,
            portbindings.VIF_TYPE_BRIDGE,
            True)

    def check_segment_for_agent(self, segment, agent):
        mappings = agent['configurations'].get('interface_mappings', {})
        LOG.debug(_("Checking segment: %(segment)s "
                    "for mappings: %(mappings)s"),
                  {'segment': segment, 'mappings': mappings})
        network_type = segment[api.NETWORK_TYPE]
        if network_type == 'local':
            return True
        elif network_type in ['flat', 'vlan']:
            return segment[api.PHYSICAL_NETWORK] in mappings
        else:
            return False
