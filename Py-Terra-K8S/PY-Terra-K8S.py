import subprocess
import sys

from AKSTerraform import *

Terraform_Dir = "/Users/michaelwilliams/Documents/GitHub/Py-Terra-K8S/Py-Terra-K8S/Terraform"
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
    "admin_user_name": "OpenInnoAdmin",
    "vnet_address": "172.16.0.0/22",
    "subnet_prefix": "172.16.0.0/24",
    "service_cidr": "172.16.1.0/24",
    "bridge_cidr": "172.17.0.1/16",
    "dns_svc_ip": "172.16.1.10"
}


def tf_command_helper_sys(cmd):
    """
    Terraform Command Helper - sends shell scripts to Shell
    :param cmd:
    :return:
    """
    print(cmd)
    try:
        retcode = subprocess.call([cmd], shell=True)
        if retcode < 0:
            print(sys.stderr, "Child was terminated by signal", -retcode)
        else:
            print(sys.stderr, "Child returned", retcode)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)


def tf_command_helper(cmd):
    """
    Terraform Command Helper -  sends non-executable
    shell commands to a command Shell
    :param cmd:
    :return:
    """
    print(cmd)
    try:
        retcode = subprocess.call([cmd], shell=True)
        if retcode < 0:
            print(sys.stderr, "Child was terminated by signal", -retcode)
        else:
            print(sys.stderr, "Child returned", retcode)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)


def test_configure_helm():
    """
    Test configuration of helm
    :return:
    """
    helm_config()
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
    # test_configure_helm()
