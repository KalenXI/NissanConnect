import requests
import argparse
import uuid
import sys
from uplink import Consumer, get, post, Path, Query, json, Field

class Nissan(Consumer):
    def __init__(self, base_url, username, password):
        super(Nissan, self).__init__(base_url=base_url)

        self.api_key = self.login(username, password)
        self.account_id = self.api_key['account_id']
        conversationId = str(uuid.uuid1())
        print(self.api_key['access_token'])
        self.session.headers['CV-ConversationId'] = conversationId
        self.session.headers['Authorization'] = "Bearer " + self.api_key['access_token']
        self.session.headers['CV-ApiKey'] = self.api_key['CVApiKey']
        self.session.headers['CV-AppType'] = "MOBILE"

    def login(self, username, password):
        loginuser = 'NISNNAVCS/' + username
        r = requests.post('https://mobile.telematics.net/login/token', headers={'CV-APPID': 'cv.nissan.connect.us.android.25'}, json={'username': loginuser, 'password': password})
        print(r.json())
        return r.json()

    ### Information Commands ###
    @get("subscription/accounts/niscust:nis:{accountId}/vehicles/{vin}")
    def getVehicleInfo(self, accountId, vin): pass

    ### Remote Commands ###
    @json
    @post("remote/accounts/niscust:nis:{accountId}/vehicles/{vin}/remote-horn-and-lights")
    def executeHornLightsCommand(self, accountId, command:Field, vin): pass

    @json
    @post("remote/accounts/niscust:nis:{accountId}/vehicles/{vin}/remote-engine")
    def executeRemoteEngineCommand(self, accountId, command: Field, vin, pin: Field): pass

    @json
    @post("remote/accounts/niscust:nis:{accountId}/vehicles/{vin}/remote-door")
    def executeDoorCommand(self, accountId, command: Field, vin, pin: Field): pass

parser = argparse.ArgumentParser(description='Nissan ConnectServices command line interface.')
subparsers = parser.add_subparsers(title="commands", dest='command')

#Start command
start_parser = subparsers.add_parser('start', help='Start car')
start_parser.add_argument('-u', dest='user', metavar='user', required=True, help='username')
start_parser.add_argument('-p', dest='password', metavar='pass', required=True, help='password')
start_parser.add_argument('-pin', required=True, help='pin for secure commands')
start_parser.add_argument('-vin', required=True, help='car VIN')

#Stop command
stop_parser = subparsers.add_parser('stop', help='Stop car')
stop_parser.add_argument('-u', dest='user', metavar='user', required=True, help='username')
stop_parser.add_argument('-p', dest='password', metavar='pass', required=True, help='password')
stop_parser.add_argument('-pin', required=True, help='pin for secure commands')
stop_parser.add_argument('-vin', required=True, help='car VIN')

#Lock command
lock_parser = subparsers.add_parser('lock', help='Lock car doors')
lock_parser.add_argument('-u', dest='user', metavar='user', required=True, help='username')
lock_parser.add_argument('-p', dest='password', metavar='pass', required=True, help='password')
lock_parser.add_argument('-pin', required=True, help='pin for secure commands')
lock_parser.add_argument('-vin', required=True, help='car VIN')

#Unlock command
unlock_parser = subparsers.add_parser('unlock', help='Unlock car doors')
unlock_parser.add_argument('-u', dest='user', metavar='user', required=True, help='username')
unlock_parser.add_argument('-p', dest='password', metavar='pass', required=True, help='password')
unlock_parser.add_argument('-pin', required=True, help='pin for secure commands')
unlock_parser.add_argument('-vin', required=True, help='car VIN')

#Horn_Light command
horn_light_parser = subparsers.add_parser('horn_light', help='Sound car horn and flash lights.')
horn_light_parser.add_argument('-u', dest='user', metavar='user', required=True, help='username')
horn_light_parser.add_argument('-p', dest='password', metavar='pass', required=True, help='password')
horn_light_parser.add_argument('-vin', required=True, help='car VIN')

#Light_only command
light_only_parser = subparsers.add_parser('light_only', help='Flash lights')
light_only_parser.add_argument('-u', dest='user', metavar='user', required=True, help='username')
light_only_parser.add_argument('-p', dest='password', metavar='pass', required=True, help='password')
light_only_parser.add_argument('-vin', required=True, help='car VIN')

#get_vehicle_info command
get_vehicle_info_parser = subparsers.add_parser('get_vehicle_info', help='Get information about vehicle and subscriptions.')
get_vehicle_info_parser.add_argument('-u', dest='user', metavar='user', required=True, help='username')
get_vehicle_info_parser.add_argument('-p', dest='password', metavar='pass', required=True, help='password')
get_vehicle_info_parser.add_argument('-vin', required=True, help='car VIN')

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

nissan = Nissan('https://prd.api.telematics.net/m/', args.user, args.password)

if args.command == 'start':
    print(nissan.executeRemoteEngineCommand(nissan.account_id, "START", args.vin, args.pin).text)
elif args.command == 'stop':
    print(nissan.executeRemoteEngineCommand(nissan.account_id, "STOP", args.vin, args.pin).text)
elif args.command == 'lock':
    print(nissan.executeDoorCommand(nissan.account_id, "LOCK", args.vin, args.pin).text)
elif args.command == 'unlock':
    print(nissan.executeDoorCommand(nissan.account_id, "UNLOCK", args.vin, args.pin).text)
elif args.command == 'horn_light':
    print(nissan.executeHornLightsCommand(nissan.account_id, "HORN_LIGHT", args.vin).text)
elif args.command == 'light_only':
    print(nissan.executeHornLightsCommand(nissan.account_id, "LIGHT_ONLY", args.vin).text)
elif args.command == 'get_vehicle_info':
    print(nissan.getVehicleInfo(nissan.account_id, args.vin).json())