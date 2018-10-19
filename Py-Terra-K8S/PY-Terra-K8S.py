from AKSTerraform import *

Terraform_Dir = "/Users/michaelwilliams/Documents/GitHub/Py-Terra-K8S/Py-Terra-K8S/Terraform"
Addon_Dir = "/Users/michaelwilliams/Documents/GitHub/Py-Terra-K8S/Py-Terra-K8S/Addon"
AKS_Storage_Account = "ssaopaks00"
AKS_Storage_Container = "ssaopakscontainer"

tf_aks_variables = {
    "client_id": "168f8ef0-c532-45f3-af0b-12934bebd639",
    "client_secret": "okcDpETZgekzT59euC4I52kjuNmD3SR9WR42G07+SVE=",
    "agent_count": 4,
    "ssh_public_key": "~/.ssh/id_rsa.pub",
    "dns_prefix": "OpenInno",
    "cluster_name": "OpenInnok8s",
    "resource_group_name": "RG-Inno-GP-OpenPlatform-AKS",
    "location": "West US",
    "nsg_name": "OpenInno-nsg",
    "vnet_name": "VNT-Inno-GP-OpenPlatform-AKS",
    "subnet_name": "SUB-Inno-GP-OpenPlatform-AKSAuto-00",
    "log_workspace_id": "5f5ff417-9c32-4b94-93b1-6d793d067428",
    "admin_user_name": "OpenInnoAdmin",
    "vnet_address": "172.16.0.0/22",
    "subnet_prefix": "172.16.0.0/24",
    "service_cidr": "172.16.1.0/24",
    "bridge_cidr": "172.17.0.1/16",
    "dns_svc_ip": "172.16.1.10"
}

def test_create_addon_cluster():
    """
    Test creation of a AKS Cluster
    :return:
    """
    tf_aks_variables = {}
    print("Creating AKS cluster with Terraform")
    AKSTerraform(Addon_Dir, AKS_Storage_Account, AKS_Storage_Container, tf_aks_variables)
    print("Initializing Terraform")
    return

def test_create_aks_cluster():
    """
    Test creation of a AKS Cluster
    :return:
    """
    print("Creating AKS cluster with Terraform")
    AKSTerraform(Terraform_Dir, AKS_Storage_Account, AKS_Storage_Container, tf_aks_variables)
    print("Initializing Terraform")
    return


if __name__ == "__main__":
    test_create_aks_cluster()
    # test_cluster_addon()