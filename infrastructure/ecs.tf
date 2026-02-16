resource "aws_ecs_cluster" "secure_intake_cluster" {
  name = "secure-intake-cluster"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "secure-intake-ecs-task-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_ecs_task_definition" "secure_intake_task" {
  family                   = "secure-intake-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "secure-intake-api"
      image     = "secure-intake-api:latest"
      essential = true

      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "SECRET_KEY"
          value = "replace-in-production"
        }
      ]
    }
  ])
}
