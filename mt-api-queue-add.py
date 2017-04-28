import socket
from rosapi import Core

# hardcoded items
lst = []
new = []
count = 0
# name of IPTV server
dom = "cdn.nexttvnet.ru"

mikrot="213.79.126.58"
user="nnk"
psw="alwest5747"
print "test"
# resolve domain address
def check_name():
    check = socket.gethostbyname(dom)
    print check
    if check:
        new.append(check)
        
check_name()
# check if the new IP exist in the file test.txt
if len(new)>0:
    with open("test.txt", "r") as old:
        for line in old:
            # append all IPs to the lst for future checking on Mikrotik
            lst.append(line.strip())
            if line.strip()==new[0].strip():
                # if duplicate found
                count+=1
    old.close()
	
# add IP to the list in file
if count==0:
    with open("test.txt", "a") as fl:
        for item in new:
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
                    res1 = a.response_handler(a.talk(["/queue/simple/print", "?target=1.1.1.1/32", "=.proplist=.id",]))
                    print "REFERENCE queue number - ", res1
                    #print res1[0][".id"]
                    res = a.response_handler(a.talk(["/queue/simple/print", "?target=" + que + "/32",  "=.proplist=.id",]))
                    #print "I found this queue already exist - ", res
                except:
                    print "WARNING! Script can't check if the queue exist! Restart the script"

                else:
                    if len(res)==0:
                        print "...adding new queue..."
                        try:
                            oper = a.response_handler(a.talk(["/queue/simple/add", "=target=" + que, "=max-limit=1G/1G", "=place-before=" + res1[0][".id"], "=comment=This queue was added by SCRIPT"],))
                            print "Result of adding new QUEUE - ", oper, "\n"
                            res2 = a.response_handler(a.talk(["/queue/simple/print", "?target=" + que + "/32", "=.proplist=.id",]))
                            #print "Result of checking the num of new QUEUE -", res2, "\n"
                            #print "TRY TO MOVE", que, "num", res2[0][".id"], "before que num", res1[0][".id"]
                            #res3 = a.response_handler(a.talk(["/queue/simple/move", "=.id=" + res2[0][".id"], "=.id=" + res1[0][".id"]],))
                            #print "RESULT OF MOVING", res3
                        except:
                            print "\n WARNING! the queue was not added. Restart the script"
                    
                        else:
                            if oper=="ERROR":
                                print "Warning! The queue can't be installed! Unknown error from Router"
                            else:
                                print "SUCCESS! queue for " + que + " has been installed"
                    else:
                        print "WARNING! The queue you're adding already exists!"
    
if len(new)>0:
    mt_conn()
