build {
  sources = ["source.amazon-ebs.mysql"]

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
      "chmod +x /tmp/setup_cloudwatch.sh",
      "sudo /tmp/setup_cloudwatch.sh",
      "rm -f /tmp/setup_cloudwatch.sh"
    ]
  }
}