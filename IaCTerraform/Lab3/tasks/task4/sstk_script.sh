#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo bash -c 'echo This is the third web server from SSTK cretated by Terraform > /var/www/html/index.html'