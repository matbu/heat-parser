#   Copyright 2020 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import json

class Resource(object):

    PROPERTIES = {}
    TYPE = {}

    def __init__(self, name, dict):
        self.resource_name = name
        self._set_properties_from_dict(dict)

    def set_properties(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _set_properties_from_dict(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def _resolv_default(self, value):
        if isinstance(value, dict):
            if value.get('default') is not None:
                return value.get('default')
            else:
                # if dict and no default value then return empty string
                return ''
        return value


class NeutronNetwork(Resource):


    def to_ansible_task(self):
        # Map to os_neutron module:
        # https://docs.ansible.com/ansible/latest/modules/os_network_module.html
        ANSIBLE_MAP = {'- name': 'OS Neutron Network',
                       'os_neutron':{'name': self._resolv_default(self.name),
                                 'shared': self._resolv_default(self.shared)}
                       }

        return ANSIBLE_MAP

    def resource_type(self):
        return {'type': 'OS::Neutron::Net'}


class NeutronSubnet(Resource):

    def to_ansible_task(self):
        pass


class NovaServer(Resource):

    def to_ansible_task(self):
        ANSIBLE_MAP = {'- name': 'OS Nova Server',
                       'os_server':{'name': self._resolv_default(self.name),
                                    'image': self._resolv_default(self.image),
                                    'key_name': self._resolv_default(self.key_name),
                                    'flavor': self._resolv_default(self.flavor)}
                       }

        return ANSIBLE_MAP

    def resource_type(self):
        return {'type': 'OS::Nova::Server'}


class NeutronSecGroup(Resource):

    def to_ansible_task(self):
        pass
