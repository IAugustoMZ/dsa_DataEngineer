# define the ALB DNS output
output "alb_dns_name" {
    value = aws_lb.sstk-ecs-alb.dns_name
}
