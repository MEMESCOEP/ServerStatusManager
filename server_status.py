### IMPORTS
import io
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import messagebox
from ping3 import ping, verbose_ping
import platform

### VARS
winDimX = 540
winDimY = 500
settleTime = 5
sshuser = ""
sshpass = ""
sshbuttonindex = 0
packetsize = 10
pingtimeout = 200
numberofservers = 0
servers = {}
serverNames = {}
serverReferences = {}
serverResponses = {}
currentResponse = 0
startThread = 0
pingstatus = ""
updateServerStatuses = 0
ws = tk.Tk()
ws.title("Server Status Manager")
ws.geometry(str(winDimX) + "x" + str(winDimY))
ws.resizable(False, False)
my_file = Path("servers.txt")
if my_file.is_file():
    print("Found servers.txt file.")
else:
    messagebox.showerror(title="File Not Found",message="'servers.txt' was not found!")
    exit()

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
    def run(self):
      while True:
          for e in servers:
            hostname = servers[e]
            hostname = hostname.replace("\n","")
            servername = hostname.split("|")
            hostname = hostname.split('|')[0]
            Command="ping -c%d -w%d %s"%(1,1,hostname)
            rsp = subprocess.Popen([Command],shell=True,stdout=subprocess.PIPE) ##["ping -c1 -w1 " + hostname + " > /dev/null"]
            rsp.communicate()
            response = rsp.returncode
            
            if response == 0:
                pingstatus = "ONLINE"
            else:
                pingstatus = "OFFLINE"

            serverResponses[e] = response
            currentResponse = response



def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


pingtext = Label(ws, text="")
pingtext.place(x=0,y=470)
canvas = tk.Canvas(ws, borderwidth=5, background="#ffffff")
frame = tk.Frame(canvas, background="#ffffff")
vsb = tk.Scrollbar(ws, orient="vertical", command=canvas.yview)
hsb = tk.Scrollbar(ws, orient="horizontal", command=canvas.xview)
canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

vsb.grid(row=0,column=0,sticky=N+S+E)
hsb.grid(row=0,column=0,sticky=S)
canvas.grid(row=0,column=0)
canvas.create_window((4,4), window=frame, anchor="nw")
canvas.config(width=winDimX-10, height=winDimY-40)

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

def ssh(button_id):
    wind = Tk()
    wind.geometry("300x200")
    wind.resizable(False,False)
    wind.title("SSH into " + str(str(servers[int(button_id)]).split("|")[0]))
    uname=Label(wind, text="Username:")
    unameinp = Entry(wind)
    passwd=Label(wind, text="Password:")
    passwdinp = Entry(wind, show='*')
    
    uname.pack()
    unameinp.pack()
    passwd.pack()
    passwdinp.pack()
    global sshuser
    global sshpass
    sshuser = unameinp.get()
    sshpass = passwdinp.get()


    def StartSSH():
            my_file = Path("sshauto.dat")
            if my_file.is_file():
                0+0
            else:
                0+0
                f = open("sshauto.dat", "w")
                f.close()
            with open("sshauto.dat", 'w') as f:
                print("Writing creds to file...")
                f.write(passwdinp.get())
                f.close()
            
            server_ip = str(servers[int(button_id)]).split("|")[0]
            
            os.system("ssh " + unameinp.get() + "@" + server_ip + " < sshauto.dat")
            messagebox.showinfo(message="Your SSH session is available via the terminal.")
            os.remove(my_file)
            wind.destroy()


    startcon = Button(wind, text="Start SSH", command=StartSSH)
    startcon.pack()

  

def create_ping_text():
    global numberofservers
    index = 0
    print("Testing Servers before launch...")
    for ipaddr in open("servers.txt").readlines():
        if(ipaddr == "\n"):
            continue
        ipaddr = ipaddr.strip("\n")

        if("|" not in ipaddr):
                messagebox.showinfo(title="No server name specified!", message="No server name was specified for '" + ipaddr + "'.")
                exit()
        elif(len(ipaddr) > 35):
            messagebox.showinfo(title="Server name to long!", message="The server name specified for '" + ipaddr + "' is too long! Please limit your names to 35 characters.")
            exit()
        
        if ipaddr in (None, ''):
            continue
        else:
            

            globals()[f"server_{index}"] = Label(frame, text="") #,bg='#fff', fg='#f00'
            variablename = f"server_{index}"
            hostname = ipaddr
            hostname = hostname.replace("\n","")
            servers[int(index)] = hostname
            hostname = hostname.split('|')[0]
            response = os.system("fping -c 1 -t 300" + " -b 1 -q -r 1 -i 1 " + hostname + " > /dev/null 2>&1")
            # and then check the response...
            if response == 0:
                pingstatus = "online"
            else:
                pingstatus = "offline"

            globals()[f"server_{index}"]["text"] = (str(servers[index])+":"+pingstatus)
            serverReferences[int(index)] = variablename
            globals()[f"server_{index}"].grid(row = index+1, column = 0, sticky = W, pady = 0)
            globals()[f"button_{index}"] = Button(frame, text="SSH(" + str(index) + ")", command=0)
            stri = ''.join(x for x in "SSH(" + str(index) + ")" if x.isdigit())
            globals()[f"button_{index}"].configure(command=lambda s=stri: ssh(s))
            globals()[f"button_{index}"].grid(row=index+1,column=3,padx=100,sticky=NE)
            sshbuttonindex = 0
            index+=1
            numberofservers += 1
    print("Done.")
    

def update_server_status():
        index = 0
        settleTimeCurrent = 0
        """for ipaddr in open("servers.txt").readlines():
        time.sleep(0.01)
        ipaddr = ipaddr.strip("\n")
        if(ipaddr == ""):
            continue"""
        for e in servers:
            
            settleTimeCurrent=e
            print("Current Server Index: " + str(e) + " || Length of 'servers': " + str(len(servers)) + " || Contents of server[" + str(e) + "]: " + str(servers[e]))
            if(settleTimeCurrent < settleTime):
                #if(settleTime < len(servers)):
                #    continue
                0+0
            hostname = servers[e]
            hostname = hostname.replace("\n","")
            servername = hostname.split("|")
            hostname = hostname.split('|')[0]
            #Command=("fping -c1 -t" + str(timeout) + " -b 1 -q -r 1 " + hostname + " > /dev/null 2>&1")
            #rsp = subprocess.Popen([Command],shell=True,stdout=subprocess.PIPE) ##["ping -c1 -w1 " + hostname + " > /dev/null"]
            #rsp.communicate()
            #response = rsp.returncode
            
            #time.sleep(0.05)
            #print(pingtimeout/1000)
            #print(response)
            try:
                response = ping(hostname, timeout = pingtimeout/1000, size=packetsize)
                if(response == False):
                    pingstatus = "OFFLINE"
                elif (response == None):
                    pingstatus = "OFFLINE"
                else:
                    if response >= 0:
                        pingstatus = "ONLINE"
                    #else:
                    #    pingstatus = "OFFLINE"
            
                pingtext["text"] = ("Pinging server: " + (servers[e].split("|")[0]+ "(" + servername[1]+")"))
                serverNames[e] = (servers[e].split("|")[0]+ "(" + servername[1]+")")
                globals()[serverReferences[e]]["text"] = (servers[e].split("|")[0]+ "(" + servername[1] + "):     "+pingstatus)
                x = "OFFLINE"
                if x in (str(servers[index])+":     "+pingstatus):
                    globals()[serverReferences[e]].configure(fg='red')
                else:
                    x = "ONLINE"
                    if x in (str(servers[index])+":     "+pingstatus):
                        globals()[serverReferences[e]].configure(fg='green')

                    

            except:
                
                0+0

            try:
                    ws.update()
            except:
                    exit()


        index+=1
        ws.after(10, update_server_status())
        
def ExitPG():
    ws.destroy()
    exit()

def Start():    
    create_ping_text()
    ws.after(500, update_server_status())
    ws.mainloop()

serverEntry = ""
def AddServer():
    global serverEntry
    wind = tk.Tk()
    wind.geometry("300x200")
    wind.title("Add Server")
    sl = Label(wind, text="Server Name:")
    wind.resizable(False,False)
    sl.pack()
    entry1 = tk.Entry (wind) 
    entry1.pack()
    def writeentry():
        serverEntry = entry1
        print("Writing to file...")
        f = open("servers.txt")
        f.writelines(serverEntry)
        f.close()
        serverEntry = ""
        wind.destroy()
    addsrvbt = Button(wind, text="Add Server", command=writeentry)
    addsrvbt.pack()


def writetofile():
    global serverEntry
   
def ChangeTimeout():
    global serverEntry
    wind = tk.Tk()
    wind.geometry("200x100")
    wind.title("Change Timeout")
    sl = Label(wind, text="Timeout value (ms):")
    wind.resizable(False,False)
    sl.pack()
    entry1 = tk.Entry (wind) 
    entry1.pack()
    def writeentry():
        if(int(entry1.get()) < 100):
            messagebox.showerror(title="Error", message="The timeout value cannot be less then 100!")
            wind.update()
        else:
            global pingtimeout
            serverEntry = entry1.get()
            pingtimeout = int(serverEntry)
            serverEntry = ""
            wind.destroy()
    addsrvbt = Button(wind, text="Apply", command=writeentry)
    addsrvbt.pack()



def ChangePacketSize():
    global serverEntry
    wind = tk.Tk()
    wind.geometry("200x100")
    wind.title("Change Packet Size")
    sl = Label(wind, text="Packet Size (bytes):")
    wind.resizable(False,False)
    sl.pack()
    entry1 = tk.Entry (wind) 
    entry1.pack()
    def writeentry():
        if(int(entry1.get()) < 1):
            messagebox.showerror(title="Error", message="The packet size cannot be less then 1!")
            wind.update()
        else:
            global packetsize
            serverEntry = entry1.get()
            packetsize = int(serverEntry)
            serverEntry = ""
            wind.destroy()
    addsrvbt = Button(wind, text="Apply", command=writeentry)
    addsrvbt.pack()

newtimeout = 200
def options():
    wind = tk.Tk()
    wind.geometry("300x300")
    wind.title("Options")
    sl = Label(wind, text="Options")
    wind.resizable(False,False)
    sl.pack()
    addsrvbt = Button(wind, text="Change ping timeout", command=ChangeTimeout)
    addsrvbt.pack()

    chpngtm = Button(wind, text="Change packet size", command=ChangePacketSize)
    chpngtm.pack()

def ServersMENU():
    wind = tk.Tk()
    wind.geometry("300x300")
    wind.title("Servers")
    sl = Label(wind, text="Servers in 'servers.txt':")
    wind.resizable(False,False)
    for e in serverNames:
        sl["text"] += ("\n" + serverNames[e])
        sl.pack()
        wind.update()


osname = str(platform.system())
if("Windows" in osname):
    os.system("cls")
else:
    os.system("clear")
menubar = Menu(ws)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Options", command=options)
filemenu.add_command(label="Server list", command=ServersMENU)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=ExitPG)
menubar.add_cascade(label="File", menu=filemenu)
ws.config(menu=menubar)
Start()
