variable "mysql_source_ami" {
    description = "The base AMI to use for the build (MySQL)"
    type        = string
    default     = "ami-0d942481c7231eb34"
}

variable "mysql_ami_description" {
  description = "Description for the created AMI"
  type        = string
  default     = "AMI for CSYE6225 Mysql"
}