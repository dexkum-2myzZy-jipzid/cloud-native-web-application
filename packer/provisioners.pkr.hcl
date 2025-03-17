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
    source      = "./webapp.service"
    destination = "/tmp/webapp.service"
  }

  provisioner "file" {
    source      = "./nginx.conf"
    destination = "/tmp/nginx.conf"
  }

  # cloudwatch
  provisioner "file" {
    source      = "scripts/amazon-cloudwatch-agent.json"
    destination = "/tmp/amazon-cloudwatch-agent.json"
  }

  provisioner "file" {
    source      = "scripts/setup_cloudwatch.sh"
    destination = "/tmp/setup_cloudwatch.sh"
  }

  provisioner "shell" {
    inline = [
      "chmod +x /tmp/deploy_webapp.sh /tmp/os_init.sh /tmp/setup_user.sh /tmp/setup_cloudwatch.sh",
      "sudo /tmp/os_init.sh",
      "sudo /tmp/setup_user.sh",
      "sudo /tmp/deploy_webapp.sh",
      "sudo /tmp/setup_cloudwatch.sh"
      "rm -f /tmp/os_init.sh /tmp/setup_user.sh /tmp/deploy_webapp.sh /tmp/nginx.conf /tmp/setup_cloudwatch.sh"
    ]
  }
}