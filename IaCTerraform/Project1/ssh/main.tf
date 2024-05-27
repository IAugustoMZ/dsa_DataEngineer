# setting of the ssh key

# variables
variable "project" {}
variable "environment" {}

# set algorithm for private key criptography
resource "tls_private_key" "ssh_private_key" {
  algorithm = "RSA"
  rsa_bits = "4096"
}

# local file to store the private key
resource "local_file" "ssh_private_key" {
  content  = tls_private_key.ssh_private_key.private_key_pem
  filename = "generated/ssh/deployer"
}

# local fil to store the public key
resource "local_file" "ssh_public_key" {
  content  = tls_private_key.ssh_private_key.public_key_openssh
  filename = "generated/ssh/deployer.pub"
}

resource "aws_key_pair" "deployer" {
    key_name = "${var.project}-${var.environment}-deployer"
    public_key = tls_private_key.ssh_private_key.public_key_openssh
}

# outputs
output "deployer_key_name" {
  value = aws_key_pair.deployer.key_name
}

output "deployer_key_pem"{
    value = tls_private_key.ssh_private_key.private_key_pem
}