resource "aws_internet_gateway" "helpdesk" {
  vpc_id = aws_vpc.helpdesk.id

  tags = {
    Name        = "ai-helpdesk-igw"
    Environment = "lab"
    Project     = "ai-helpdesk-copilot"
  }
}