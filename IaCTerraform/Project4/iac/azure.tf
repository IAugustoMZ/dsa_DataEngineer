# create a resource group in Azure
resource "azurerm_resource_group" "SSTKrg" {
    name        = "SSTK-resource-group"
    location    = "eastus"
}

# creates a virtual network inside the resource group
resource "azurerm_virtual_network" "SSTKvn" {
    name                = "sstkVNet"
    resource_group_name = azurerm_resource_group.SSTKrg.name
    location            = azurerm_resource_group.SSTKrg.location
    address_space       = ["10.0.0.0/16"]
}

# creates a subnet inside the virtual network
resource "azurerm_subnet" "SSTKsn" {
    name = "sstkSubnet"
    resource_group_name = azurerm_resource_group.SSTKrg.name
    virtual_network_name = azurerm_virtual_network.SSTKvn.name
    address_prefixes = ["10.0.1.0/24"]
}

# creates a public IP address
resource "azurerm_public_ip" "SSTKip" {
    name = "sstkPublicIP"
    location = "azurerm_resource_group.SSTKrg.location
    resource_group_name = azurerm_resource_group.name
    allocation_method = "Dynamic"
}

# creates a network interface
resource "azurerm_network_interface" "SSTKni" {
    name                = "sstkNIC"
    location            = azurerm_resource_group.SSTKrg.location
    resource_group_name = azurerm_resource_group.SSTKrg.name

    ip_configuration {
        name                          = "sstkIPConfig"
        subnet_id                     = azurerm_subnet.SSTKsn.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_ip          = azurerm_public_ip.SSTKip.id
    }
}

# creates a virtual machine
resource "azurerm_virtual_machine" "SSTKvm"{
    name                    = "SSTK-deployed"
    location                = azurerm_resource_group.SSTKrg.location
    resource_group_name     = azurerm_resource_group.SSTKrg.name
    vm_size                 = "Standard_B1s"
    network_interface_ids   = [azurerm_network_interface.SSTKrg.id]

    storage_image_reference{
        publisher   = "Canonical"
        offer       = "UbuntuServer"
        sku         = "20.04-LTS"
        version     = "latest"
    }

    os_profile {
        computer_name   = "sstk-deployed"
        admin_username  = "sstkadmin"
        admin_password  = "Password123!"
    }

    storage_os_disk {
        name = "osdisk"
        caching = "ReadWrite"
        create_option = "FromImage"
        managed_disk_type = "Premium_LRS"
    }

    os_profile_linux_config{
        disable_password_authentication = false
    }
}