import adal
import requests
import os
import json


def test_get_APIRequests():
    '''
    Get all the API requests for Azure RM
    :return:
    '''

    tenant = os.environ['TENANT']
    authority_url = 'https://login.microsoftonline.com/' + tenant
    client_id = os.environ['CLIENTID']
    client_secret = os.environ['CLIENTSECRET']
    resource = 'https://management.azure.com/'
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
    headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
    params = {'api-version': '2016-06-01'}
    url = 'https://management.azure.com/' + 'subscriptions'

    r = requests.get(url, headers=headers, params=params)

    print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
    return


def test_create_ResourceGroup():
    '''
    Create a reqsource Groups with Azure RM API
    :return:
    '''
    tenant = os.environ['TENANT']
    authority_url = 'https://login.microsoftonline.com/' + tenant
    client_id = os.environ['CLIENTID']
    client_secret = os.environ['CLIENTSECRET']
    resource = 'https://management.azure.com/'
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
    headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
    params = {'api-version': '2017-05-10'}
    url = 'https://management.azure.com/subscriptions/<subscription_id>/resourcegroups/mytestrg'

    data = {'location': 'northeurope'}

    r = requests.put(url, data=json.dumps(data), headers=headers, params=params)

    print(json.dumps(r.json(), indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    test_get_APIRequests()
    test_create_ResourceGroup()