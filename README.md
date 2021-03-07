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


# reg_service:
  1. accept client (4 times)
  2. return IPs sequentially 
# clients:
  1. connect to reg_service
  2. recieve IPs (which are available)
  3. send hellow to available IPs
  4. wait hellows from clients, that connected after him
  
  

