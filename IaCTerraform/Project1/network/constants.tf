# define availability zones
variable "az_zone_a"{
    type = map

    default = {
        us-east-2 = "us-east-2a"
    }
}

variable "az_zone_b"{
    type = map

    default = {
        us-east-2 = "us-east-2b"
    }
}