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

  provisioner "shell" {
    inline = [
      "chmod +x /tmp/os_init.sh /tmp/setup_user.sh",
      "sudo /tmp/os_init.sh",
      "sudo /tmp/setup_user.sh",
      "rm -f /tmp/os_init.sh /tmp/setup_user.sh"
    ]
  }

  provisioner "file" {
    source      = "scripts/start_webapp.sh"
    destination = "/opt/webapp/start_webapp.sh"
  }

  # service file for long-term use
  provisioner "file" {
    source      = "scripts/webapp.service"
    destination = "/etc/systemd/system/webapp.service"
  }

  provisioner "shell" {
    inline = [
      "chmod +x /opt/webapp/start_webapp.sh",
      "chmod +x /tmp/deploy_webapp.sh",
      "sudo /tmp/deploy_webapp.sh",
      "rm -f /tmp/deploy_webapp.sh"
    ]
  }
}