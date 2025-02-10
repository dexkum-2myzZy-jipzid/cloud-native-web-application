build {
  sources = ["source.amazon-ebs.webapp"]

  # Copy webapp.zip to EC2
  provisioner "file" {
    source      = "./webapp.zip"
    destination = "/tmp/webapp.zip"
  }

  # Copy all script files to EC2
  provisioner "file" {
    source      = "scripts/os_init.sh"
    destination = "/tmp/os_init.sh"
  }

  provisioner "file" {
    source      = "scripts/setup_user.sh"
    destination = "/tmp/setup_user.sh"
  }

  provisioner "file" {
    source      = "scripts/deploy_webapp.sh"
    destination = "/tmp/deploy_webapp.sh"
  }

  provisioner "file" {
    source      = "scripts/webapp.service"
    destination = "/tmp/webapp.service"
  }

  # Execute scripts
  provisioner "shell" {
    inline = [
      "chmod +x /tmp/os_init.sh /tmp/setup_user.sh /tmp/deploy_webapp.sh",
      "sudo /tmp/os_init.sh",
      "sudo /tmp/setup_user.sh",
      "sudo /tmp/deploy_webapp.sh"
    ]
  }
}