output "instance_ids" {
  value = aws_instance.sstk-instance.*.id  
}