#!/usr/bin/python #!/usr/bin/env python

import os, argparse, json, logging, time, sys

from api_base import ApiBase
from pprint import pprint

class OpsmanagerApi(ApiBase):
    def __init__(self, base_url, group_id, api_user, api_key):
        super(OpsmanagerApi, self).__init__(base_url, group_id, api_user, api_key)

    def get_alerts(self, base_url, group_id):
        url = "{}/api/public/v1.0/groups/{}/alertConfigs".format(base_url, group_id)
        #cert = 'C:\Users\dxm294\MongoDB\opsmanager.pem'
        #r = get(url, auth=auth, cert=cert, verify=False)
        r = self.get(url)
        data = r
        print(data)
        data1 = data['results']
        keys = ["groupId", "eventTypeName", "enabled", "metricThreshold", "notifications"]
        alerts = [{k:v for k, v in i.items() if k in keys} for i in data1]
        isconfig_dir = os.path.isdir('configs')
        if isconfig_dir == False:
            os.mkdir('configs')

        json_file = os.path.join("configs", 'alert_file.json')
        logging.info("Getting alert configuration from: {}" + "for goupId: {}".format(url, group_id))

        with open('configs/' + 'alert_file.json', 'w') as f:
            json.dump(alerts, f, indent=4)
            logging.debug("{}".format(pprint(alerts)))

    def get_hosts(self, base_url, group_id):
        url = "{}/api/public/v1.0/groups/{}/hosts".format(base_url, group_id)
        r = self.get(url)
        keys = ['id', 'hostname', 'port', 'typeName', 'ipAddress', 'version']
        host_list = r['results']
        host_data = [{k:v for k, v in i.items() if k in keys} for i in host_list]
        return host_data

    def get_databases(self, base_url, group_id):
        hosts = self.get_hosts(base_url, group_id)
        host_tupes = [{v for k, v in i.iteritems() if k in 'id'} for i in hosts]
        id_list = []
        for items in host_tupes:
            for i in items:
                url = "{}/api/public/v1.0/groups/{}/hosts/{}".format(base_url, group_id, i)
                r = self.get(url)
                data = json.dumps(r, sort_keys=True, indent=4)
                print(data)

    def get_clusterConfig(self, base_url, group_id):
        url = "{}/groups/{}/automationConfig".format(self.base_url, self.group_id)
        r = self.get(url)
        data = json.dumps(r, sort_keys=True, indent=4)
        print(data)

    def post_alerts(self):
        pass

    def post_clusterConfig(self):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', '--alerts', action='store_true', help='get a group alert and monitoring configuration')
    parser.add_argument('-D', '--databases', action='store_true', help='get all databse process running for a group')
    parser.add_argument('-C', '--cluster', action='store_true', help='get automation config of a single group')
    parser.add_argument('-b', '--base_url', required=True)
    parser.add_argument('-f', '--file', help='write file to current directory unless absolute path provided')
    parser.add_argument('-g', '--group_id', required=True)
    parser.add_argument('-u', '--api_user', required=True)
    parser.add_argument('-k', '--api_key', required=True)
    args = parser.parse_args()
    run = OpsmanagerApi(args.base_url, args.group_id, args.api_user, args.api_key)

    if args.alerts:
        if args.file:
            directory = os.path.relpath(args.file)
            with open(directory, 'w+') as f:
                sys.stdout = f
                run.get_alerts(args.base_url, args.group_id)
        else:
            run.get_alerts(args.base_url, args.group_id)
    elif args.databases:
        if args.file:
            directory = os.path.relpath(args.file)
            with open(directory, 'w+') as f:
                sys.stdout = f
                run.get_databases(args.base_url, args.group_id)
        else:
            run.get_databases(args.base_url, args.group_id)
    elif args.cluster:
        if args.file:
            directory = os.path.relpath(args.file)
            with open(directory, 'w+') as f:
                sys.stdout = f
                run.get_clusterConfig(args.base_url, args.group_id)
        else:
            run.get_clusterConfig(args.base_url, args.group_id)
