# DSMPF_peer
Distributed game cities

# Vagrant_file
run:
1. **vagrant init**
  It will create Vagrantfile, put configs there
2. **vagran up**
  run VM
3. **vagrant ssh 'name of the vm (ex regservice or client1** 
go to **cd /** then **cd vagrant**

4. run python file **python name.py**


reg_service:
  accept 4 client and return them IPs sequentially 
clients:
  connect to reg_service
  recieve IPs (which are available)
  send hellow to available IPs
  wait hellows from clients, that connected after him
  
  

