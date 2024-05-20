# define an ECS cluster - depends on a variables file
resource "aws_ecs_cluster" "sstk-ecs-cluster" {
  name = "${var.project_name}-${var.environment}-ecs-cluster"
}

# define a group of logs for CloudWatch - depends on a variables file
resource "aws_cloudwatch_log_group" "sstk-ecs-log-group" {
  name = "/ecs/${var.project_name}-${var.environment}-task-definition"
}

# define an ECS task definition with necessary configuration,
# including a container definition - depends on a variables file
resource "aws_ecs_task_definition" "sstk-ecs-task-definition" {
  family                    = "${var.project_name}-${var.environment}-task-definition"
  network_mode              = "awsvpc"
  requires_compatibilities  = [ "FARGATE" ]     # serverless computing
  cpu                       = var.cpu
  memory                    = var.memory
  execution_role_arn        = "arn:aws:iam::${var.aws_account_id}:role/ecsTaskExecutionRole"
  task_role_arn             = "arn:aws:iam::${var.aws_account_id}:role/ecsTaskExecutionRole"

  container_definitions = jsonencode([
    {
        name      = "${var.project_name}-${var.environment}-container"
        image     = var.docker_image_name
        essential : true
        portMappings = [
            {
                containerPort = tonumber(var.container_port)
                hostPort      = tonumber(var.container_port)
                protocol      = "tcp"
                appProtocol   = "http"
            }
        ],

        # add env variables of the S3
        environmentFiles = [
            {
                value = var.s3_env_vars_file_arn
                type  = "s3"
            }
        ],

        # configure AWS CloudWatch logging
        logConfiguration = {
            logDriver = "awslogs"
            options = {
                "awslogs-create-group"  = "true"
                "awslogs-group"         = aws_cloudwatch_log_group.sstk-ecs-log-group.name
                "awslogs-region"        = var.awslogs_region
                "awslogs-stream-prefix" = "ecs"
                }
            }
        }
    ])
}

# defines an ECS resource service with Fargate launch type and
# network configuration - depends on a variables file
resource "aws_ecs_service" "sstk-ecs-service" {
  name            = "${var.project_name}-${var.environment}-service"
  cluster         = aws_ecs_cluster.sstk-ecs-cluster.id
  task_definition = aws_ecs_task_definition.sstk-ecs-task-definition.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    assign_public_ip    = true      # we want to connect from the internet
    subnets             = [ module.vpc.public_subnets[0] ]
    security_groups     = [ module.container_security_group.security_group_id ]
  }

  # configures the service to use an Application Load Balancer
  health_check_grace_period_seconds = 0
    load_balancer {
        target_group_arn = aws_lb_target_group.sstk-ecs-target-group.arn
        container_name   = "${var.project_name}-${var.environment}-container"
        container_port   = var.container_port
    }
}

# defines an Application Load Balancer
resource "aws_lb" "sstk-ecs-alb" {
    name                = "${var.project_name}-${var.environment}-alb"
    internal            = false     # this application is public
    load_balancer_type  = "application"
    security_groups     = [ module.alb-security_group.security_group_id ]
    subnets             = [ module.vpc.public_subnets[0] , module.vpc.public_subnets[1] ]
  
}

# defines a target group for the Application Load Balancer
resource "aws_lb_target_group" "sstk-ecs-target-group" {
    name                = "${var.project_name}-${var.environment}-target-group"
    port                = var.container_port
    protocol            = "HTTP"
    target_type         = "ip"
    vpc_id              = module.vpc.vpc_id

    health_check {
        path                = var.health_check_path
        protocol            = "HTTP"
        matcher             = "200-299"
        interval            = 30
        timeout             = 5
        healthy_threshold   = 5
        unhealthy_threshold = 2
    }
}

# defines a listener for the Application Load Balancer
resource "aws_lb_listener" "sstk-ecs-listener" {
    load_balancer_arn = aws_lb.sstk-ecs-alb.arn
    port              = 80
    protocol          = "HTTP"

    # forwards requests to the target group
    default_action {
        type             = "forward"
        target_group_arn = aws_lb_target_group.sstk-ecs-target-group.arn
    }
}
