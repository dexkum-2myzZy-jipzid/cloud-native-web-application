packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.0, < 2.0.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "webapp" {
  region            = var.aws_region
  instance_type     = var.instance_type
  source_ami        = var.source_ami
  ssh_username      = var.ssh_username
  ami_name          = "csye6225_${formatdate("YYYY_MM_DD_HH_mm", timestamp())}"
  subnet_id         = var.subnet_id
  security_group_id = var.security_group_id
  ami_users         = [var.account_id]
  ami_description   = var.ami_description

  aws_polling {
    delay_seconds = var.delay_seconds
    max_attempts  = var.max_attempts
  }

  launch_block_device_mappings {
    device_name           = var.device_name
    volume_size           = var.volume_size
    volume_type           = var.volume_type
    delete_on_termination = true
  }
}