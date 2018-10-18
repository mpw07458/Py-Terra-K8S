provider "azurerm" {
  version = "=1.15.0"
}

provider "kubernetes" {
  host                   = "${azurerm_kubernetes_cluster.k8s.kube_config.0.host}"
  username               = "${azurerm_kubernetes_cluster.k8s.kube_config.0.username}"
  password               = "${azurerm_kubernetes_cluster.k8s.kube_config.0.password}"
  client_certificate     = "${base64decode(azurerm_kubernetes_cluster.k8s.kube_config.0.client_certificate)}"
  client_key             = "${base64decode(azurerm_kubernetes_cluster.k8s.kube_config.0.client_key)}"
  cluster_ca_certificate = "${base64decode(azurerm_kubernetes_cluster.k8s.kube_config.0.cluster_ca_certificate)}"
}

provider "helmcmd" {
    "alias" = "kubernetes-stable"
    "chart_source_type" = "repository"
    "chart_source" = "stable"
    "debug" = true
    "kubeconfig" = "~/.kube/config/${var.cluster_name}"
}

resource "helmcmd_release" "plain" {
    provider = "helmcmd.kubernetes-stable"
    name = "ingress-controller"
    chart_name = "nginx-ingress"
    chart_version = "0.12.0"
    namespace = "kube-system"
}