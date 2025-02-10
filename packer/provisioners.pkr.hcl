build {
  sources = ["source.amazon-ebs.webapp"]

  # Copy webapp.zip to EC2
  provisioner "file" {
    source      = "./webapp.zip"
    destination = "/tmp/webapp.zip"
  }

  # Copy all script files to EC2
  provisioner "file" {
    source      = "scripts/setup_user.sh"
    destination = "/tmp/setup_user.sh"
  }

  provisioner "file" {
    source      = "scripts/install_dependencies.sh"
    destination = "/tmp/install_dependencies.sh"
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
      "chmod +x /tmp/setup_user.sh /tmp/install_dependencies.sh /tmp/deploy_webapp.sh",
      "sudo /tmp/setup_user.sh",
      "sudo /tmp/install_dependencies.sh",
      "sudo /tmp/deploy_webapp.sh"
    ]
  }
}