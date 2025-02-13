variable "aws_region" {
  description = "AWS region to deploy in"
  type        = string
  default     = "us-west-2"
}

variable "ami_description" {
  description = "Description for the created AMI"
  type        = string
  default     = "AMI for CSYE6225 WebApp"
}

variable "account_id" {
  description = "AWS account ID to share the AMI with"
  type        = string
  default     = "381492181945"
}


variable "delay_seconds" {
  description = "Delay seconds for AWS polling"
  type        = number
  default     = 30
}

variable "max_attempts" {
  description = "Maximum attempts for AWS polling"
  type        = number
  default     = 50
}

variable "instance_type" {
  description = "Instance type to use for the build instance"
  type        = string
  default     = "t2.micro"
}

variable "source_ami" {
  description = "The base AMI to use for the build"
  type        = string
  default     = "ami-00c257e12d6828491"
}

variable "ssh_username" {
  description = "SSH username to use for connection"
  type        = string
  default     = "ubuntu"
}

variable "subnet_id" {
  description = "Subnet ID in which to launch the instance"
  type        = string
  default     = "subnet-0e2f34f004d42a98c"
}

variable "security_group_id" {
  description = "Security Group ID for the instance"
  type        = string
  default     = "sg-04ff95a026dcaddce"
}

variable "device_name" {
  description = "Device name for the block device mapping"
  type        = string
  default     = "/dev/sda1"
}

variable "volume_size" {
  description = "Volume size (in GB)"
  type        = number
  default     = 8
}

variable "volume_type" {
  description = "Type of the volume (e.g., gp2)"
  type        = string
  default     = "gp2"
}