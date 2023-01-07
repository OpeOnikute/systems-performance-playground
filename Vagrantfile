# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.box_version = "1.0.282"
  config.vm.provision "file", source: "./activity.py", destination: "/home/vagrant/activity.py"
  config.vm.provision :shell, :privileged => false, :path => "scripts/install-bcc.sh"
  config.vm.provision :shell, :privileged => false, :path => "scripts/install-nginx.sh"
  config.vm.network "forwarded_port", guest: 80, host: 8080, id: "nginx"
end