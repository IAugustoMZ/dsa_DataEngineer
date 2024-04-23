output "intance_ids" {
    value = module.sstk-ec2_instances.instance_ids
}

output "bucket_id" {
    value = module.sstk_s3_bucket.bucket_id
}