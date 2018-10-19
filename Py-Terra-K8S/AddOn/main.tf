provider "azurerm" {
  version = "=1.15.0"
}

provider "helmcmd" {
    "alias" = "kubernetes-stable"
    "chart_source_type" = "repository"
    # When chart_source_type is `repository`, this is the name of the repo
    # whence to get the chart.
    "chart_source" = "stable"
    "debug" = true
    "kube_context" = "OpenInnok8s"
}

resource "helmcmd_release" "plain" {
    provider = "helmcmd.kubernetes-stable"
    name = "ingress-controller"
    chart_name = "nginx-ingress"
    chart_version = "0.12.0"
    namespace = "kube-system"
}

resource "helmcmd_release" "plain" {
    provider = "helmcmd.kubernetes-stable"
    name = "cert-manager"
    chart_name = "cert-manager"
    chart_version = "0.5.0"
    namespace = "kube-system"
}

resource "helmcmd_release" "plain" {
    provider = "helmcmd.kubernetes-stable"
    name = "prometheus"
    chart_name = "prometheus"
    chart_version = "7.3.1"
    namespace = "kube-system"
}

resource "helmcmd_release" "plain" {
    provider = "helmcmd.kubernetes-stable"
    name = "fluentd"
    chart_name = "fluentd"
    chart_version = "1.0.0"
    namespace = "kube-system"
}