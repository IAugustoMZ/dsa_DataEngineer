output "instance_public_dns" {
    value = aws_instance.sstk_ml_api.public_dns
}