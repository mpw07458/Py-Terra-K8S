import json
import os
import adal
import requests
from AKSTerraform import *
# import pterraform
# from python_terraform import *
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    StorageAccountUpdateParameters,
    Sku,
    Kind
)
from haikunator import Haikunator
# noinspection PyUnresolvedReferences

EAST_US = 'eastus'
GROUP_NAME = 'mpw-azure-group'
STORAGE_ACCOUNT_NAME = Haikunator().haikunate(delimiter='')

variables = {
    "client_id": "6484bac5-b63d-4385-bf53-44ee8144ea83",
    "client_secret": "a030758c-ca55-44f8-9585-412fddbf0196",
    "agent_count": 4,
    "ssh_public_key": "~/.ssh/id_rsa.pub",
    "dns_prefix": "tmpwtest",
    "cluster_name": "tfmpwtest",
    "resource_group_name": "tfmpw-rg",
    "location": "East US",
    "nsg_name": "tfmpw-nsg",
    "vnet_name": "tfmpw-vnet",
    "subnet_name": "tfmpw-subnet",
    "admin_user_name": "tfmpw",
    "vnet_address": "10.1.0.0/16",
    "subnet_prefix": "10.1.0.0/24",
}


def get_credentials():
    subscription_id = os.environ['ARM_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['ARM_CLIENT_ID'],
        secret=os.environ['ARM_CLIENT_SECRET'],
        tenant=os.environ['ARM_TENANT_ID']
    )
    return credentials, subscription_id


def print_item(group):
    """Print an Azure object instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)


def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")


def test_get_APIRequests():
    """
    Get all the API requests for Azure RM
    :return:
    """
    tenant = os.environ['ARM_TENANT_ID']
    authority_url = 'https://login.microsoftonline.com/' + tenant
    client_id = os.environ['ARM_CLIENT_ID']
    client_secret = os.environ['ARM_CLIENT_SECRET']
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
    """
    Create a reqsource Groups with Azure RM API
    :return:
    """
    tenant = os.environ['ARM_TENANT_ID']
    authority_url = 'https://login.microsoftonline.com/' + tenant
    client_id = os.environ['ARM_CLIENT_ID']
    client_secret = os.environ['ARM_CLIENT_SECRET']
    subscription_id = os.environ['ARM_SUBSCRIPTION_ID']
    resource = 'https://management.azure.com/'
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
    headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
    params = {'api-version': '2017-05-10'}
    url = 'https://management.azure.com/subscriptions/' + subscription_id + '/resourcegroups/mpwtestrg'

    data = {'location': 'eastus'}

    r = requests.put(url, data=json.dumps(data), headers=headers, params=params)

    print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
    return


def test_create_StorageAccount():
    """
    Create a reqsource Groups with Azure RM API
    :return:
    """
    # setup credentails
    """Storage management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    credentials, subscription_id = get_credentials()

    resource_client = ResourceManagementClient(credentials, subscription_id)
    storage_client = StorageManagementClient(credentials, subscription_id)

    # You MIGHT need to add Storage as a valid provider for these credentials
    # If so, this operation has to be done only once for each credentials
    resource_client.providers.register('Microsoft.Storage')

    # Create Resource group
    print('Create Resource Group')
    resource_group_params = {'location': 'eastus'}
    print_item(resource_client.resource_groups.create_or_update(GROUP_NAME, resource_group_params))

    # Check availability
    print('Check name availability')
    bad_account_name = 'invalid-or-used-name'
    availability = storage_client.storage_accounts.check_name_availability(bad_account_name)
    print('The account {} is available: {}'.format(bad_account_name, availability.name_available))
    print('Reason: {}'.format(availability.reason))
    print('Detailed message: {}'.format(availability.message))
    print('\n\n')

    # Create a storage account
    print('Create a storage account')
    storage_async_operation = storage_client.storage_accounts.update(
        GROUP_NAME, STORAGE_ACCOUNT_NAME,
        StorageAccountCreateParameters(
           sku=Sku("mpw-storage"),
           kind=Kind.storage,
           location='eastus'
        )
    )

    storage_account = storage_async_operation.result()
    print_item(storage_account)
    print('\n\n')

    # Get storage account properties
    print('Get storage account properties')
    storage_account = storage_client.storage_accounts.get_properties(
        GROUP_NAME, STORAGE_ACCOUNT_NAME)
    print_item(storage_account)
    print("\n\n")

    # List Storage accounts
    print('List storage accounts')
    for item in storage_client.storage_accounts.list():
        print_item(item)
    print("\n\n")

    # List Storage accounts by resource group
    print('List storage accounts by resource group')
    for item in storage_client.storage_accounts.list_by_resource_group(GROUP_NAME):
        print_item(item)
    print("\n\n")

    # Get the account keys
    print('Get the account keys')
    storage_keys = storage_client.storage_accounts.list_keys(GROUP_NAME, STORAGE_ACCOUNT_NAME)
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}
    print('\tKey 1: {}'.format(storage_keys['key1']))
    print('\tKey 2: {}'.format(storage_keys['key2']))
    print("\n\n")

    # Regenerate the account key 1
    print('Regenerate the account key 1')
    storage_keys = storage_client.storage_accounts.regenerate_key(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        'key1')
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}
    print('\tNew key 1: {}'.format(storage_keys['key1']))
    print("\n\n")

    # Update storage account
    print('Update storage account')
    storage_account = storage_client.storage_accounts.update(
        GROUP_NAME, STORAGE_ACCOUNT_NAME,
        StorageAccountUpdateParameters(
            sku=Sku("mpw-storage")
        )
    )
    print_item(storage_account)
    print("\n\n")

    # Delete the storage account
    print('Delete the storage account')
    storage_client.storage_accounts.delete(GROUP_NAME, STORAGE_ACCOUNT_NAME)
    print("\n\n")

    # Delete Resource group and everything in it
    print('Delete Resource Group')
    delete_async_operation = resource_client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("Deleted: {}".format(GROUP_NAME))
    print("\n\n")

    # List usage
    print('List usage')
    for usage in storage_client.usage.list():
        print('\t{}'.format(usage.name.value))

    return

def test_create_AKS_Cluster():
    """
    Create a reqsource Groups with Azure RM API
    :return:
    """
    print("creating cluster")
    aks_tf = AKSTerraform('/Users/michaelwilliams/Documents/GitHub/Py-Terra-K8S/Py-Terra-K8S/Terraform',
                          'cloudshellstoragempw', 'mpwcontainer', variables)
    print("initializing Terraform")
    #AKSTerraform.init()
    #AKSTerraform.plan()
    #AKSTerraform.apply()
    return

if __name__ == "__main__":
    test_get_APIRequests()
    # test_create_ResourceGroup()
    # test_create_StorageAccount()
    test_create_AKS_Cluster()