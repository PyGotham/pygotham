# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.define "db" do |db|
        db.vm.box = "ubuntu/trusty64"
        db.vm.network "private_network", ip: "192.168.50.4"
    end

    config.vm.define "web" do |web|
        web.vm.box = "ubuntu/trusty64"
        web.vm.network :forwarded_port, host: 8000, guest: 80
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "ansible/playbook.yml"
    end
end
