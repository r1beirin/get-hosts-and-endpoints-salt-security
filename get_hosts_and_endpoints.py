import requests
import csv
import argparse

def toCSV(requests, filename):
    print(f'[CSV] Writing to {filename}...')
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=requests[0].keys())
        writer.writeheader()

        for request in requests:
            writer.writerow(request)
    print(f'[CSV] Done writing to {filename}...')

def getEndpoints(apiToken):
    print('[ENDPOINTS] Initiate collecting endpoints...')
    offset = 0
    limit = 100
    allEndpoints = []

    while True:
        print(f'[ENDPOINTS] Collecting endpoints from offset {offset}...')
        host = f'https://api.secured-api.com/v1/inventory/endpoints?limit={limit}&offset={offset}'
        headers = {
            'Authorization': f'Bearer {apiToken}',
            'Content-Type': 'application/json',
        }

        response = requests.get(host, headers=headers)
        resp = response.json()

        if not resp['response']:
            break

        allEndpoints.extend(resp['response'])
        offset += limit
    print('[ENDPOINTS] Done collecting endpoints...')
    toCSV(allEndpoints, 'endpoints.csv')

def getHosts(apiToken):
    print('[HOSTS] Initiate collecting hosts...')
    offset = 0
    limit = 100
    allHosts = []

    while True:
        print(f'[HOSTS] Collecting hosts from offset {offset}...')
        host = f'https://api.secured-api.com/v1/inventory/hosts?limit={limit}&offset={offset}'
        headers = {
            'Authorization': f'Bearer {apiToken}',
            'Content-Type': 'application/json',
        }

        response = requests.get(host, headers=headers)
        resp = response.json()

        if not resp['response']:
            break

        allHosts.extend(resp['response'])
        offset += limit

    print('[HOSTS] Done collecting hosts...')
    toCSV(allHosts, 'hosts.csv')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("token")
    args = parser.parse_args()
    
    getHosts(args.token)
    getEndpoints(args.token)

if __name__ == '__main__':
    main()