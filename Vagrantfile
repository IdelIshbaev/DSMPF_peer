# -*- mode: ruby -*-
# vi: set ft=ruby :
BOX_PATH = 'hadoop_image.box'

Vagrant.configure("2") do |config|

 config.vm.define "regservice" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.hostname = "regservice"
   subconfig.vm.network :private_network, ip: "10.0.0.11"
   subconfig.vm.network "forwarded_port", guest: 8088, host: 8088
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "client1" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "client1"
   subconfig.vm.network :private_network, ip: "10.0.0.12"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "client2" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "client2"
   subconfig.vm.network :private_network, ip: "10.0.0.13"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "client3" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "client3"
   subconfig.vm.network :private_network, ip: "10.0.0.14"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "client4" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "client4"
   subconfig.vm.network :private_network, ip: "10.0.0.15"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

end