#!/usr/bin/env pyhton

import logging, argparse, json, sys, os

from pprint import pprint


def get_config(base_url, group_id, api_user, api_key, *args):
    url = "{}/api/public/v1.0/groups/{}/{}".format(base_url, group_id, "automationConfig")
    auth = super().HTTPDigestAuth(api_user, api_key)
    cert = ''
    r = get(url, auth=auth) #cert=cert, verify=False)
    data = json.loads(r.text)
    pprint(data)


    keys = ["mongoDbVersions", "monitoringVersions", "backupVersions",
     "processes", "replicaSets", "sharding"]
    options = [{k:v for k, v in data.iteritems() if k in keys} for i in data]
    isconfig_dir = os.path.isdir('configs')
    if isconfig_dir == False:
        os.mkdir('configs')

    config_file = os.path.join("configs", "cluster_config.json")
    #logging.info("Getting cluster configuration from groupid: {}".format(group_id))

    with open('configs/cluster_config.json', 'w') as f:
        json.dump(options, f, indent=4)
        check_response(r)
        #logging.debug({}.format(pprint(options))


#def check_response(r):
#    if r.status_code not in [codes.ok, 200]:
#        logging.error("Response Error Code: {} Detail: {}".format(r.status_code, r.json()))
#        raise ValueError(r.json())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Gets the group curent cluster configuration')
    parser.add_argument('-b', '--base_url', required=True, help='your opsmanager URL')
    parser.add_argument('-g', '--group_id', required=True, help='group id')
    parser.add_argument('-u', '--api_user', required=True, help='ldap user id')
    parser.add_argument('-k', '--api_key', required=True, help='an opsmanager api access key')
    parser.add_argument('-v', '--verbose', help='outputs logging information', action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.info("Getting cluster configuration from groupid: {}".format(args.group_id))

    consutruct = GetClusterConfig()

    run = consutruct.get(args.base_url, args.group_id, args.api_user, args.api_key)
