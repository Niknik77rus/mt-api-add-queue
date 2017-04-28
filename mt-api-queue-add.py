import socket
from rosapi import Core

# hardcoded items
lst = []
#lst for new found addresses
new_ip = []
count = 0

# name of IPTV server
dom = "cdn.nexttvnet.ru"
mikrot="213.79.126.58"
user="nnk"
psw="alwest5747"

# resolve domain address
def check_name():
    check = socket.gethostbyname(dom)
    print check
    if check:
        new_ip.append(check)

# check if the new IP exist in the file test.txt
def compare_ip(count):
    with open("test.txt", "r") as old:
        for line in old:
        # append all IPs to the lst for future checking on Mikrotik
            lst.append(line.strip())
            if line.strip()==new_ip[0].strip():
            # if duplicate found
                count+=1
    old.close()

# add IP to the list in file
def add_new_ip():
    with open("test.txt", "a") as fl:
        for item in new_ip:
            fl.write(item + '\n')


def mt_conn():    
    try: 
        a = Core(mikrot) 
    except: 
        print "WARNING! no connection to the router! Check IP-address reachability and API status on the router"
    else:
        try:
            a.login(user, psw)
        except:
            print "WARNING! Login unsucsessful. Please, check your credentials and restart the script."
        else:    
            print "\nLogin successful"         
            for que in lst:
                print "Trying to add queue - ", que, "\n"
                try:
                    ref_que = a.response_handler(a.talk(["/queue/simple/print", "?target=1.1.1.1/32", "=.proplist=.id",]))
                    chk_que = a.response_handler(a.talk(["/queue/simple/print", "?target=" + que + "/32",  "=.proplist=.id",]))

                except:
                    print "WARNING! Script can't check if the queue exist! Restart the script"

                else:
                    if len(chk_que)==0:
                        print "...adding new queue..."
                        try:
                            oper = a.response_handler(a.talk(["/queue/simple/add", "=target=" + que, "=max-limit=1G/1G", "=place-before=" + ref_que[0][".id"], "=comment=This queue was added by SCRIPT"],))
                            print "Result of adding new QUEUE - ", oper, "\n"

                        except:
                            print "\n WARNING! the queue was not added. Restart the script"
                    
                        else:
                            if oper=="ERROR":
                                print "Warning! The queue can't be installed! Unknown error from Router"
                            else:
                                print "SUCCESS! queue for " + que + " has been installed"
                    else:
                        print "WARNING! The queue you're adding already exists!"


#main loop
check_name()
if len(new_ip)>0:
    compare_ip(count)
if count == 0:
    add_new_ip()
if len(new_ip)>0:
    mt_conn()
