import getpass
import telnetlib

user = input('Enter your telnet username: ')
password = getpass.getpass()

f = open('devices_ip')      # File needs to contain the ip address of devices to backup

for IP in f:
    IP=IP.strip()
    print ('Get running config from Switch ' + (IP))
    HOST = IP
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b'Username: ')
    tn.write(user.encode('ascii') + b'\n')
    if password:
        tn.read_until(b'Password: ')
        tn.write(password.encode('ascii') + b'\n')  
        
    tn.write(b"terminal length 0\n")    # Cisco terminal displays output without any breaks
    tn.write(b"show run\n")
    tn.write(b'exit\n')

    readoutput = tn.read_all()     # Stores console output into a variable
    saveoutput = open("switch" + HOST, "w")     # Opens a read/write file -> "w"
    saveoutput.write(readoutput.decode('ascii'))    # Write output into the created file
    saveoutput.write("\n")      # Carriage return
    saveoutput.close    # Closes the file
