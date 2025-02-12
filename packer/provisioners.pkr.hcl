build {
  sources = ["source.amazon-ebs.webapp"]

  provisioner "file" {
    source      = "./webapp.zip"
    destination = "/tmp/webapp.zip"
  }

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
    source      = "scripts/start_webapp.sh"
    destination = "/tmp/start_webapp.sh"
  }

  # service file for long-term use
  provisioner "file" {
    source      = "scripts/webapp.service"
    destination = "/tmp/webapp.service"
  }

  provisioner "shell" {
    inline = [
      "chmod +x /tmp/deploy_webapp.sh /tmp/os_init.sh /tmp/setup_user.sh /tmp/start_webapp.sh",
      "sudo /tmp/os_init.sh",
      "sudo /tmp/setup_user.sh",
      "sudo /tmp/deploy_webapp.sh",
      "rm -f /tmp/os_init.sh /tmp/setup_user.sh /tmp/deploy_webapp.sh"
    ]
  }
}