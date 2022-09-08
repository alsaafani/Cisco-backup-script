import paramiko
import os, sys
import socket
import time
import cmd
import datetime
import errno


def disablePaging(remote_conn):

    remote_conn.send("terminal length 0\n")
    
    time.sleep(1)

    output = remote_conn.recv(1000)

    return output

now =datetime.datetime.now()
user =('Enter your username here')

password =('enter you password here')
port=22

foldername= "%.2i-%.2i-%i" % (now.year,now.month,now.day)



try:
    newfolder= os.mkdir ('/var/log/Ios_backup/'+foldername)
except OSError as e:
    pass




#create foldername with current date#   
foldername= "%.2i-%.2i-%i" % (now.year,now.month,now.day)

#create error folder using foldername above#   

newfoldererro= os.mkdir ('/var/log/Ios_backup/output_files_failure/'+foldername)

#Path of new create folder#
full_path='/var/log/Ios_backup/'+foldername+'/'



#open  IOS_Devices file list
f0 = open('/var/log/Ios_backup/IOS_Devices_list.txt')
#end

def sshConnect():
    for h in f0:
        h = h.strip()
        print("Hostname: " + h)
        ip = h
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:

            ssh.connect(ip,port, user, password, look_for_keys=False)
            
            filename = "%s_DATE_(%.2i-%.2i-%i)_TIME_(h%.2i_m%.2i_s%.2i)" % (ip,now.year,now.month,now.day,now.hour,now.minute,now.second)
               
            f1 = open(full_path +filename + '.txt', 'a')

            chan = ssh.invoke_shell()
            time.sleep(3)
            chan.send('\n\n')
            chan.send('copy run start \n \n \n')
            time.sleep(25)
            
            
            chan.send('\n\n')
            disablePaging(remote_conn)
            time.sleep(2)
            chan.send('\n sh run \n')
            time.sleep(2)
            chan.send('\n\n\n\n\n\n')
            time.sleep(3)
            #save the output in a variable #
            output = chan.recv(999999)
            
            #create a file name with current date and time#
            filename = "%s_DATE_(%.2i-%.2i-%i)_TIME_(h%.2i_m%.2i_s%.2i)" % (ip,now.year,now.month,now.day,now.hour,now.minute,now.second)
            f1.write(output.decode("utf-8") )
            f1.close()
            ssh.close()
            f1.close()

            continue
            
            #catch errors and save them in new folder to reviw later.
        except(AuthenticationException, SSHException, socket.error, socket.timeout) as e:
            
            f1 = open('/var/log/Ios_backup/output_files_failure/'+foldername+'/' + ip + ".txt", "w")
            
            print("SSH Connection Unsuccessful --> unable to establish connection")
            print(e)

            f1.write("Hostname: " + ip + "\n" + str(e) + "\n")
            f1.close()
            
        continue


sshConnect()
