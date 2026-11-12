resource "aws_security_group" "alb_sg" {
  name        = "ai-helpdesk-alb-sg"
  description = "Security group for the application load balancer"

  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-alb-sg"
    Environment = "lab"
    Tier        = "public"
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb_sg.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"

  description = "Allow HTTP traffic"
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb_sg.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"

  description = "Allow HTTPS traffic"
}


resource "aws_security_group" "app_sg" {
  name        = "ai-helpdesk-app-sg"
  description = "Security group for FastAPI application servers"

  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-app-sg"
    Environment = "lab"
    Tier        = "application"
  }
}


resource "aws_vpc_security_group_ingress_rule" "app_from_alb" {
  security_group_id = aws_security_group.app_sg.id

  referenced_security_group_id = aws_security_group.alb_sg.id
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"

  description = "Allow traffic from ALB to FastAPI"
}


resource "aws_vpc_security_group_egress_rule" "alb_to_app" {
  security_group_id = aws_security_group.alb_sg.id

  referenced_security_group_id = aws_security_group.app_sg.id
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"

  description = "Allow ALB to forward traffic to FastAPI"
}


resource "aws_security_group" "db_sg" {
  name        = "ai-helpdesk-db-sg"
  description = "Security group for PostgreSQL database"

  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-db-sg"
    Environment = "lab"
    Tier        = "database"
  }
}

resource "aws_vpc_security_group_ingress_rule" "db_from_app" {
  security_group_id = aws_security_group.db_sg.id

  referenced_security_group_id = aws_security_group.app_sg.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"

  description = "Allow PostgreSQL traffic from application servers"
}


resource "aws_vpc_security_group_egress_rule" "app_to_db" {
  security_group_id = aws_security_group.app_sg.id

  referenced_security_group_id = aws_security_group.db_sg.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"

  description = "Allow application servers to connect to PostgreSQL"
}