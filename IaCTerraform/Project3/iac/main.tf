# define a resource group
resource "azurerm_resource_group" "sstk_project" {
    name     = "ResourceGroupSSTK"
    location = "West US 2"
}

# create a virtual network
resource "azurerm_virtual_network" "sstk_vnet" {
    name                = "vnet_terr_sstk"
    address_space       = ["10.0.0.0/16"]
    location            = azurerm_resource_group.sstk_project.location
    resource_group_name = azurerm_resource_group.sstk_project.name
}

# create a subnet inside the virtual network (the network resources are inside the vnet)
resource "azurerm_subnet" "sstk_subnet" {
    name                    = "subnet_terr_sstk"
    resource_group_name     = azurerm_resource_group.sstk_project.name
    virtual_network_name    = azurerm_virtual_network.sstk_vnet.name
    address_prefixes        = ["10.0.1.0/24"]
}

# 10.0.0.0/16 is a much bigger network that covers all the IP addresses of "10.0.x.x"
# while 10.0.1.0/24 is a smaller subnet that covers the addresses of "10.0.1.x"

# configure a network interface
resource "azurerm_network_interface" "sstk_ni" {
    name                = "ni_terr_sstk"
    location            = azurerm_resource_group.sstk_project.location
    resource_group_name = azurerm_resource_group.sstk_project.name

    # IP configuration for network interface
    ip_configuration {
        name = "vm_sstk"
        subnet_id = azurerm_subnet.sstk_subnet.id
        private_id_address_allocation = "Dynamic"
    }
}

# create a virtual machine Linux
resource "azurerm_linux_virtual_machine" "sstk_vm"{
    name                            = "vmsstk"
    resource_group_name             =  azurerm_resource_group.sstk_project.name
    location                        = azurerm_resource_group.sstk_project.location
    size                            = "Standard_F2"
    admin_username                  = "adminuser"
    disable_password_authentication = false
    admin_password                  = "ExHpaQMGesTCjJYRNwPnbk"
    network_interface_ids           = [azurerm_network_interface.sstk_ni.id]

    # OS disk configuration
    os_disk {
        caching                 = "ReadWrite"
        storage_account_type    = "Standard_LRS"
    }

    # OS image source
    source_image_reference {
        publisher   = "Canonical"
        offer       = "0001-com-ubuntu-server-focal"
        sku         = "20_04-lts"
        version     = "latest"
    }
}