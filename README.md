# Py-Terra-K8S
 A framework written in Python which utilizes Terrafrom to deploy an AKS managed kubernetes cluster in Azure

Prerequisites - 

Ensure you have Azure CLI installed

Ensure you have an account that points to NBC Universal Innovation Azure

Ensure you have Python 3.7 installed

Ensure azure-mgmt-resource and azure-mgmt-storage packages are Installed

AKSTerraform package is included opensource written in Python 3.7

Additonal instructions are below for AKS Terraform

Disclaimer-

This has been test on Mac OSX so far, shoule work on Linux/Ubuntu

Getting Started
These instructions will get you a copy of the project up and running on your local Mac OSX for development and testing purposes. 

Prerequisites
What things you need to install the software and how to install them

Install python version 3.7
for mac OSX command line "brew install python3"
At ubuntu command line "sudo apt-get update"
                       "sudo apt-get install python3.7"

requirements.txt has python modules needed For version 0.95 python 3.7 requires: azure-mgmt-resource>=1.1.0
azure-mgmt-storage>=1.0.0 

Requires AKSTerraform package

Usage of AKSTerraform

Example variables (Example)

Terraform_Dir = "/Users/michaelwilliams/Documents/GitHub/Py-Terra-K8S/Py-Terra-K8S/Terraform"
Addon_Dir = "/Users/michaelwilliams/Documents/GitHub/Py-Terra-K8S/Py-Terra-K8S/Addon"
AKS_Storage_Account = "ssaopaks00"
AKS_Storage_Container = "ssaopakscontainer"

tf_aks_variables = {
    "client_id": "XXX-REDACTED-XXX",
    "client_secret": "XXX-REDACTED-XXX",
    "agent_count": 4,
    "ssh_public_key": "~/.ssh/id_rsa.pub",
    "dns_prefix": "OpenInno",
    "cluster_name": "OpenInnok8s",
    "resource_group_name": "RG-Inno-GP-OpenPlatform-AKS",
    "location": "West US",
    "nsg_name": "OpenInno-nsg",
    "vnet_name": "VNT-Inno-GP-OpenPlatform-AKS",
    "subnet_name": "SUB-Inno-GP-OpenPlatform-AKSAuto-00",
    "log_workspace_id": "XXX-REDACTED-XXX",
    "admin_user_name": "OpenInnoAdmin",
    "vnet_address": "172.16.0.0/22",
    "subnet_prefix": "172.16.0.0/24",
    "service_cidr": "172.16.1.0/24",
    "bridge_cidr": "172.17.0.1/16",
    "dns_svc_ip": "172.16.1.10"
}

Example Call

For AKS Cluster
AKSTerraform(Terraform_Dir, AKS_Storage_Account, AKS_Storage_Container, tf_aks_variables)

For AKS Addons
AKSTerraform(AddOn_Dir, AKS_Storage_Account, AKS_Storage_Container, tf_aks_variables={})


Version
latest version 0 Build 0.93

Authors
Michael (Mike) P. Williams

License
This project is licensed under the Apache License - see the LICENSE.md file for details

© 2018 GitHub, Inc.
