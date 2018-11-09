
##########################
#    FETCH RESOURCES     #
##########################


# Import the necessary libraries
from urllib.request import *
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
import multiprocessing
import time
import os


##########################
#    ProgressBar Func    #
##########################
# This code is run last


percentageDupes = []
percentageDupesGPU = []
latestPercent = 0

def reportProgress(blocknum, blocksize, totalsize):

    global percentageDupes
    global percentage
    global latestPercent
    global progressBar
    global progressBarGPU
    global percentageLabelGPU

    style = ttk.Style()
    style.theme_use('alt')
    style.configure("orange.Horizontal.TProgressbar", foreground='orange',background='orange')

    progressBar = ttk.Progressbar(master=progressWindow,style="orange.Horizontal.TProgressbar",length=100,orient=HORIZONTAL,mode='determinate')
    progressBar.place(x=0,y=0)
    progressBarGPU = ttk.Progressbar(master=progressWindow,length=100,orient=HORIZONTAL,mode='determinate')
    progressBarGPU.place(x=0,y=17)
    
    readsofar = blocknum * blocksize
    readsofar = readsofar/1000

    percentage = (readsofar/1940) * 100
    percentage = int(percentage)
    percentage = str(percentage)

    percentage = percentage.replace('.','')
    percentage = percentage.replace('%','')
    latestPercent = int(percentage)+1

    if latestPercent == 101:
        latestPercent = 100

    percentageLabelCPU = Label(master=progressWindow,text=("%d" % latestPercent),font=('Helvetica',8,'bold'),bg='black',fg='white')
    percentageLabelGPU = Label(master=progressWindow,text="0",font=('Helvetica',8,'bold'),bg='black',fg='white')
    percentageLabelCPU.place(x=96,y=0)
    percentageLabelGPU.place(x=96,y=15)
    
    progressBar['value']=latestPercent
    if percentage not in percentageDupes:
        print(percentage+'%')
        percentageDupes.append(percentage)
    progressWindow.update()
        
def reportProgressGPU(blocknum, blocksize, totalsize):

    global percentageDupesGPU
    global percentage
    global latestPercent
    global progressBarGPU

    style = ttk.Style()
    style.theme_use('alt')
    style.configure("orange.Horizontal.TProgressbar", foreground='orange',background='orange')
    
    readsofar = blocknum * blocksize
    readsofar = readsofar/1000

    percentage = (readsofar/1080) * 100
    percentage = int(percentage) 
    percentage = str(percentage)
    
    percentage = percentage.replace('.','')
    percentage = percentage.replace('%','')
    latestPercent = int(percentage)+1

    if latestPercent == 101:
        latestPercent = 100
    progressBarGPU['value']=latestPercent
    percentageLabelGPU.config(text=("%d" % latestPercent))
    
    if percentage not in percentageDupesGPU:
        print(percentage+'%')
        percentageDupesGPU.append(percentage)
    progressWindow.update()
    
    
##########################
#    Initialisation      #
##########################
# This code is run first

    
def fFetchHTML():

    global progressWindow
        
    progressWindow = tk.Tk()
    progressWindow.geometry('120x35')
    progressWindow.configure(bg='black')
    progressWindow.resizable(0,0)
    progressWindow.overrideredirect(1)
    progressWindow.attributes('-topmost','true')

    def centerWindow(pw):
        pw.update_idletasks()
        w = pw.winfo_screenwidth()
        h = pw.winfo_screenheight()
        size = tuple(int(_) for _ in pw.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        pw.geometry("%dx%d+%d+%d" % (size + (x, y)))
    centerWindow(progressWindow)
    
    # Save the HTML documents 
    # CPU first
    print("CPU resources downloading...")
    try:
        urlretrieve("https://www.cpubenchmark.net/CPU_mega_page.html","Resources\passmarkCPU.html",reportProgress)
        print("Download complete")
    except:
        raise
        print("An error occured whilst downloading the resources.")

    # GPU second
    print("GPU resources downloading...")
    try:
        urlretrieve("https://www.videocardbenchmark.net/GPU_mega_page.html","Resources\passmarkGPU.html",reportProgressGPU)
        print("Download complete")
        time.sleep(1)
        progressWindow.destroy()
    except:
        raise
        print("An error occured whilst downloading the resources.")
        print("\nPlease check internet connection...")
        return

    # Remove unnecessary code from the .html
    # Begin work on CPU formatting
    print("\nFormatting CPU resources...")
    filePassmarkCPU = open("Resources\passmarkCPU.html","r+")
    fileCPU_NEW = open("Resources\passmarkTableCPU.txt","w")
    tableCode = []

    # Run a for loop that that will recieve ONLY the names of the CPU's from the HTML document
    for line in filePassmarkCPU:
        if "cpu=" in line:
            # Split the line into chunks
            splitLine = line.split("<")
            # Find the name (It's always at position 5)
            cpuName = splitLine[5]
            # Only print the beginning of the name - not the HTML code
            cpuName = cpuName[cpuName.find('>'):]
            cpuName = cpuName[1:]
            tableCode.append(cpuName)
            
        if "Rank" in line:
            # Split the line into chunks
            splitLine = line.split("<")
            # Find the rank (It's always at position 17)
            cpuRank = splitLine[17]
            # Only print the beginning of the rank's line up until the score itself - not the whole HTML code
            cpuRank = cpuRank[cpuRank.find('>'):]
            cpuRank = cpuRank[3:]
            tableCode.append(cpuRank)
        else:
            continue
    fileCPU_NEW.write(str(tableCode))
    print("Formatting complete")
    filePassmarkCPU.close()

    # Begin work on GPU formatting
    print("\nFormatting GPU resources...")
    filePassmarkGPU = open("Resources\passmarkGPU.html","r+")
    fileGPU_NEW = open("Resources\passmarkTableGPU.txt","w")
    tableCode = []

    # Run a for loop that that will recieve ONLY the names of the GPU's from the HTML document
    for line in filePassmarkGPU:
        if "gpu=" in line:
            # Split the line into chunks
            splitLine = line.split("<")
            # Find the name (It's always at position 5)
            gpuName = splitLine[5]
            # Only print the beginning of the name - not the HTML code
            gpuName = gpuName[gpuName.find('>'):]
            gpuName = gpuName[1:]
            tableCode.append(gpuName)
            
        if "Rank" in line:
            # Split the line into chunks
            splitLine = line.split("<")
            # Find the rank (It's always at position 21)
            gpuRank = splitLine[21]
            # Only print the beginning of the rank's line up until the score itself - not the whole HTML code
            gpuRank = gpuRank[gpuRank.find('>'):]
            gpuRank = gpuRank[3:]
            tableCode.append(gpuRank)
        else:
            continue
        
    # Add Intel HD Graphics to the database
    IntelHD = ("Intel HD Graphics")
    IntelRank = (99999)
    tableCode.append(IntelHD)
    tableCode.append(IntelRank)
    
    fileGPU_NEW.write(str(tableCode))
    print("Formatting complete")
    filePassmarkGPU.close()

    # Output the status of the script / reset the status to 0
    path = "Database\\f_status"
    os.path.join(path, '*')
    status_FILE = open(path,"w+")
    status_FILE.write("0")
    status_FILE.close()
