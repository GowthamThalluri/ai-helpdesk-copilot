resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.helpdesk.id
  cidr_block              = "10.20.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = false

  tags = {
    Name        = "ai-helpdesk-public-a"
    Environment = "lab"
    Tier        = "public"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.helpdesk.id
  cidr_block              = "10.20.2.0/24"
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = false

  tags = {
    Name        = "ai-helpdesk-public-b"
    Environment = "lab"
    Tier        = "public"
  }
}

resource "aws_subnet" "app_a" {
  vpc_id                  = aws_vpc.helpdesk.id
  cidr_block              = "10.20.11.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = false

  tags = {
    Name        = "ai-helpdesk-app-a"
    Environment = "lab"
    Tier        = "application"
  }
}

resource "aws_subnet" "app_b" {
  vpc_id                  = aws_vpc.helpdesk.id
  cidr_block              = "10.20.12.0/24"
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = false

  tags = {
    Name        = "ai-helpdesk-app-b"
    Environment = "lab"
    Tier        = "application"
  }
}

resource "aws_subnet" "db_a" {
  vpc_id                  = aws_vpc.helpdesk.id
  cidr_block              = "10.20.21.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = false

  tags = {
    Name        = "ai-helpdesk-db-a"
    Environment = "lab"
    Tier        = "database"
  }
}

resource "aws_subnet" "db_b" {
  vpc_id                  = aws_vpc.helpdesk.id
  cidr_block              = "10.20.22.0/24"
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = false

  tags = {
    Name        = "ai-helpdesk-db-b"
    Environment = "lab"
    Tier        = "database"
  }
}