resource "aws_vpc" "helpdesk" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "ai-helpdesk-vpc"
    Environment = "lab"
    Project     = "ai-helpdesk-copilot"
  }
}