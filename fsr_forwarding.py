""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """
import sys, json, hashlib, hmac, base64, ssl
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from http.client import HTTPException
from datetime import datetime
import os
from os.path import join

DEFAULT_ALGORITHM = 'sha256'
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def connector(data_dict):
    host_uri = 'icon.cybersponse.com'
    full_uri = 'https://' + host_uri + '/api/triggers/1/ManageEngine'

    key_path = join(os.path.dirname(os.path.abspath(__file__)), 'keys')
    with open(join(key_path, 'APPLIANCE_PUBLIC_KEY'), 'r') as public:
        public_key = public.read().strip()
    with open(join(key_path, 'APPLIANCE_PRIVATE_KEY'), 'r') as private:
        private_key = private.read().strip().encode()

    verb = 'POST'
    if data_dict:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        data = json.dumps(data_dict)
        print("data ", data)
        payload = data.encode('utf-8')
        digest_method = hashlib.new(DEFAULT_ALGORITHM)
        digest_method.update(payload)
        hashed_payload = digest_method.hexdigest()

        raw_fingerprint = "{0}.{1}.{2}.{3}.{4}".format(DEFAULT_ALGORITHM,
                                                       verb,
                                                       timestamp,
                                                       full_uri,
                                                       hashed_payload)
        hashed = hmac.new(private_key, raw_fingerprint.encode(),
                          hashlib.sha256)
        hashedFingerprint = hashed.hexdigest()
        header = base64.b64encode(
            '{0};{1};{2};{3}'.format(DEFAULT_ALGORITHM, timestamp, public_key,
                                     hashedFingerprint).encode())
        headers = {
            'Host': host_uri,
            'Authorization': 'CS {}'.format(header.decode())
        }
        try:
            req = Request(full_uri, payload, headers)
            response = urlopen(req, context=ctx)
            response_data = response.read()
            print("Response: ", response_data)
        except HTTPError as e:
            print("Error", e.reason)
            x = 'HTTPError = ' + str(e.code)
        except URLError as e:
            print('URLError = ' + str(e.reason))
            x = 'URLError = ' + str(e.reason)
        except HTTPException as e:
            print('HTTPException')
            x = 'HTTPException'
        except Exception:
            import traceback
            print('generic exception: ' + traceback.format_exc())
            x = 'Generic Exception = ' + traceback.format_exc()


def main(argv):
    file_Path = sys.argv[1]
    with open(file_Path) as data_file:
        data_dict = json.load(data_file)
        print("Data is: ", data_dict)
    connector(data_dict)


if __name__ == "__main__":
    main(sys.argv)
