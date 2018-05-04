import sys
import pprint
import json
import argparse
import logging
from pprint import pprint
from requests import put, post, get, delete, codes
from requests.exceptions import RequestException
from requests.auth import HTTPDigestAuth

def load_json():
    with open("configs/cluster_config.json") as data_file:
        data = json.load(data_file)
    return data

def put_data(base_url, group_id, api_user, api_key, *args):
    base_url = base_url
    #api_key = 'c4735ad6-f435-4217-af74-f6a39ed4c2dc'
    url = "{}/api/public/v1.0/groups/{}".format(base_url, group_id)
    data = load_json()

    auth = HTTPDigestAuth(api_user, api_key)
    logging.info("Executing POST: {}".format(url))
    headers = {'content-type': 'application/json'}
    r = put(base_url,
        auth=auth,
        data=json.dumps(data),
        headers=headers
        )
    #check_response(r)
    logging.debug("%s" % pprint(r.json()))
    #data_file.close
    return r.json()

def check_response(r):
    if r.status_code not in [codes.ok, 202]:
        logging.error("Response Error Code: %s Detail: %s" % (r.status_code, r.json()['detail']))
        raise ValueError(r.json()['detail'])

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_url', required=True)
    parser.add_argument('-g', '--group_id', requied=True)
    parser.add_argument('-u', '--api_user', required=True)
    parser.add_argument('-k', '--api_key', requied=True)
    args = parser.parse_args()

    run = put_data(args.base_url, args.group_id, args.api_user, args.api_key)
