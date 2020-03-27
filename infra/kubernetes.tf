resource "azurerm_resource_group" "resource-group" {
  location = var.location
  name = "arkivverket"
}

resource "azurerm_kubernetes_cluster" "kubernetes-cluster" {
  name = var.cluster_name
  location = var.location
  resource_group_name = azurerm_resource_group.resource-group.name
  dns_prefix = "arkivverket"

  service_principal {
    client_id = azuread_service_principal.cluster-principal.application_id
    client_secret = random_password.cluster-pw.result
  }

  agent_pool_profile {
    name = var.node_pool_name
    count = var.node_count
    min_count = var.min_node_count
    max_count = var.max_node_count
    type = "VirtualMachineScaleSets"
    enable_auto_scaling = true
    vm_size = var.node_type
  }
}

output "kube_config" {
   value = azurerm_kubernetes_cluster.kubernetes-cluster.kube_config_raw
}