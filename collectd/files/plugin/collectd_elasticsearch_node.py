#!/usr/bin/python
# Copyright 2016 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if __name__ == '__main__':
    import collectd_fake as collectd
else:
    import collectd

import collectd_elasticsearch_base as base

NAME = 'elasticsearch'


class ElasticsearchNodePlugin(base.ElasticsearchBase):
    def __init__(self, *args, **kwargs):
        super(ElasticsearchNodePlugin, self).__init__(*args, **kwargs)
        self.plugin = NAME

    def itermetrics(self):
        stats = self.query_api('_nodes/_local/stats').get(
            'nodes', {}).values()[0]
        yield {
            'type_instance': 'documents',
            'values': stats['indices']['docs']['count']
        }
        yield {
            'type_instance': 'documents_deleted',
            'values': stats['indices']['docs']['deleted']
        }
        # TODO: collectd more metrics
        # See https://www.elastic.co/guide/en/elasticsearch/guide/current/
        # _monitoring_individual_nodes.html


plugin = ElasticsearchNodePlugin(collectd)


def config_callback(conf):
    plugin.config_callback(conf)


def read_callback():
    plugin.read_callback()

if __name__ == '__main__':
    collectd.load_configuration(plugin)
    plugin.read_callback()
else:
    collectd.register_config(config_callback)
    collectd.register_read(read_callback)
