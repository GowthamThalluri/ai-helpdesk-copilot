resource "aws_route_table" "public" {
  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-public-rt"
    Environment = "lab"
    Tier        = "public"
  }
}

resource "aws_route" "public_internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.helpdesk.id
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}



resource "aws_route_table" "app_a" {
  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-app-a-rt"
    Environment = "lab"
    Tier        = "application"
  }
}

resource "aws_route_table" "app_b" {
  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-app-b-rt"
    Environment = "lab"
    Tier        = "application"
  }
}

resource "aws_route_table" "database" {
  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-database-rt"
    Environment = "lab"
    Tier        = "database"
  }
}


resource "aws_route_table_association" "app_a" {
  subnet_id      = aws_subnet.app_a.id
  route_table_id = aws_route_table.app_a.id
}

resource "aws_route_table_association" "app_b" {
  subnet_id      = aws_subnet.app_b.id
  route_table_id = aws_route_table.app_b.id
}

resource "aws_route_table_association" "database_a" {
  subnet_id      = aws_subnet.db_a.id
  route_table_id = aws_route_table.database.id
}

resource "aws_route_table_association" "database_b" {
  subnet_id      = aws_subnet.db_b.id
  route_table_id = aws_route_table.database.id
}