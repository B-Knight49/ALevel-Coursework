
### Importing necessary files and modules ###

# Import TKINTER for GUI # 
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Import OS and SYS to access system information #
import os
import sys
import math

# Import TIME and SUBPROCESS to monitor external factors/outputs #
import time
import subprocess

# Import other scripts and plugins #
import fetch_HTML
import SHA512_Hash
import PLUGIN_pypyodbc
import shutil

# Configure pypyodbc
PLUGIN_pypyodbc.lowercase = False

# Import WMI for hardware information # 
import PLUGIN_wmi

##########################
#    Initialisation      #
##########################

def __init__():

    global mw
    global entryUser
    global entryPass
    global entryUserConfig
    global entryPassConfig
    global pyDb
    global timesIncorrect
    global loginButton
    global permissionWindow

    global timesLooped
    global gifFrames

    global alreadyCreatedSystem
    global alreadyCreatedGames
    global alreadyCreatedAbout
    global alreadyCreatedOther
    
    ### Database configuration ###
    
    print("Configuring database...")
    pyDb = PLUGIN_pypyodbc
    UsrDet = "Database\\UsrDet.accdb"
    if os.path.exists(UsrDet):
        print("Already Created database\n")
    else:
        try:
            pyDb.win_create_mdb("Database\\UsrDet.accdb")
            print("Created Database")
            print("Configuring Tables...")
            DbConn = pyDb.win_connect_mdb("Database\\UsrDet.accdb")
            DbCursor = DbConn.cursor()
            # Creating the two different tables and creating a relationship between them using CONSTRAINTS and keys
            DbCursor.execute('CREATE TABLE Credentials (ID INTEGER CONSTRAINT PK_ID PRIMARY KEY, Usernames CHAR(32), Hash CHAR(64), Code INTEGER);').commit()
            print("Created Table Credentials\n")
            DbCursor.execute('CREATE TABLE Permissions (ID INTEGER NOT NULL CONSTRAINT FK_ID REFERENCES Credentials (ID), Admin INTEGER);').commit()
            print("Created Table Permissions\n")
        except:
            raise
    
    # Initialize variables
    currentUser = ""
    userWhitelist = ""
    usernameEntry = ""
    rowHash = ["",""]
    rowHash[0] = ""
    rowHash[1] = ""
    
    # Create the Master Window (MW)
    mw = tk.Tk()
    mw.geometry('440x250')
    mw.iconbitmap('Images\\favicon.ico')
    mw.title("Social Club Login")
    mw.resizable(0,0)
    timesLooped = 0

    # Center the login window
    def centerWindow(mw):
        mw.update_idletasks()
        w = mw.winfo_screenwidth()
        h = mw.winfo_screenheight()
        size = tuple(int(_) for _ in mw.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        mw.geometry("%dx%d+%d+%d" % (size + (x, y)))

    # Call the function that centers the window
    centerWindow(mw)

    # Configure the general aesthetics of the login window 
    mw.configure(bg='black')

    # Import the social club logo
    socialLogoLogin = PhotoImage(master=mw,file='Images\\social_clublogo.ppm')
    socialLogoLogin.image = socialLogoLogin
    socialLogoLabel = Label(master=mw,image=socialLogoLogin,bd=0)
    socialLogoLabel.place(x=155,y=20)

    # Create the username entry and check to see when the user has clicked on the entry box
    entryUserConfig = StringVar()
    entryUser = Entry(master=mw, bd=0,textvariable=entryUserConfig, width=30,fg='#A9A9A9',font=('Helvetica',10))
    entryUser.place(x=120,y=90)
    entryUser.insert(0,"Username")

    # Define the function to see if the username box has been clicked on and - if it equals "Username" - clear it. If the Password box is empty, fill it with "Password"
    def isUsernameFocused():
        if entryUser.get() == "Username":
            entryUser.delete(0,END)
            entryUser.config(fg='black')

        if entryPass.get() == "":
            entryPass.insert(0,"Password")
            entryPass.config(fg='#A9A9A9',show="")

    # Create the password entry and check to see when the user has clicked on the entry box
    entryPassConfig = StringVar()
    entryPass = Entry(master=mw, bd=0, width=30,fg='#A9A9A9',font=('Helvetica',10),textvariable=entryPassConfig)
    entryPass.place(x=120,y=110)
    entryPass.insert(0,"Password")

    # Define the function to see if the password box has been clicked on and - if it equals "Password" - clear it. If the Username box is empty, fill it with "Username"
    def isPassFocused():
        if entryPass.get() == "Password":
            entryPass.delete(0,END)
            entryPass.config(fg='black',show="*")
                    
        if entryUser.get() == "":
            entryUser.insert(0,"Username")
            entryUser.config(fg='#A9A9A9')

    # Bind the primary mouse button and ENTER to the entry boxes to call a function when they're clicked on
    entryUser.bind("<Button-1>",lambda x: isUsernameFocused())
    entryPass.bind("<Button-1>",lambda x: isPassFocused())
    entryPass.bind("<Return>",lambda x: fCheckPass())

    # Change the password to asterisks if the user uses TAB to highlight the entry widget
    def on_typingPass(*args):
        entryPass.config(fg='black',show="*")
    entryPassConfig.trace_variable("w",on_typingPass)
    
    def on_typingUser(*args):
        entryUser.config(fg='black')
    entryUserConfig.trace_variable("w",on_typingUser)


##########################
#    Widget Remover      #
##########################

        
    def removeWidgets(widget):

        widget.destroy()


##########################
#  Password Verification #
##########################


    timesIncorrect = 0
    def fCheckPass():

        global timesIncorrect
        global correctPassword
        global loginButton
        global currentUser
        
        # Create the function that throws the errors if the entered info is incorrect
        def fIncorrectPassword():

            global timesIncorrect
            global incorrectText
            global loginButton

            if timesIncorrect == 5:
                
                def resetLogin():
                    
                    global timesIncorrect
                    
                    loginButton.config(state=NORMAL)
                    timesIncorrect = 0
                    removeWidgets(maxAttempts)
                    removeWidgets(incorrectText)
                    print("Lock out ended\n")

                print("\nMaximum attempts reached.")
                loginButton.config(state=DISABLED)
                maxAttempts = Label(master=mw,text="Maximum attempts reached! Please wait 10 seconds...",font=('Helvetica',8),fg='red',bg='black')
                maxAttempts.place(x=100,y=205)
                mw.after(10000,resetLogin)
            else:
                timesIncorrect += 1
                if timesIncorrect > 1:
                    print("Incorrect Password")
                else:
                    print("Incorrect Password")
                    incorrectText = Label(master=mw,text="Incorrect Username or Password",font=('Helvetica',8),fg='red',bg='black')
                    incorrectText.place(x=140,y=185)

        # Check to see if the password box is empty to prevent errors being raised
        passwordEntry = entryPass.get()
        if passwordEntry == "" or passwordEntry == "Password":
            print("Password box is empty")
            return

        # HASH the password the user entered and compare it
        passwordEntry = SHA512_Hash.fGetHash(passwordEntry)
        
        # Check if the password is correct
        DbConn = pyDb.win_connect_mdb("Database\\UsrDet.accdb")
        DbCursor = DbConn.cursor()
        
        usernameEntry = entryUser.get()
        if usernameEntry == "" or usernameEntry == "Username":
            print("Username box empty")
            return
            
        DbCursor.execute("SELECT Usernames, Hash FROM Credentials WHERE Usernames = ?;",[usernameEntry,])
        
        while True:
            rowHash = DbCursor.fetchone()
            if rowHash != None:
                rowUsername = rowHash[0].replace(" ","")
                if rowUsername == usernameEntry:
                    if rowHash:
                        correctPassword = rowHash[1]
                        correctPassword = correctPassword.replace(" ","")
                        currentUser = rowHash[0]
                        break
                    else:
                        print("Incorrect Username")
                        correctPassword = None
                        break
                else:
                    continue
            else:
                print("Error!")
                correctPassword = None
                break
        print("Successfully converted entered password to hash")

        if timesIncorrect < 5:
            if passwordEntry == correctPassword:
                correctLogin = Label(master=mw,text="Correct Credentials - Logging in...",font=('Helvetica',8),fg='#A9A9A9',bg='black')
                correctLogin.place(x=140,y=185)
                print("Correct Password")
                print()
                print(" === IF A LARGE CHANGE HAS BEEN MADE, SAVE THE FILE AS A NEW VERSION NUMBER ===")
                print(" === IF A LARGE CHANGE HAS BEEN MADE, SAVE THE FILE AS A NEW VERSION NUMBER ===")
                print(" === IF A LARGE CHANGE HAS BEEN MADE, SAVE THE FILE AS A NEW VERSION NUMBER ===")
                print(" === IF A LARGE CHANGE HAS BEEN MADE, SAVE THE FILE AS A NEW VERSION NUMBER ===")
                print()
                fTopLevelLoading()
            else:
                fIncorrectPassword()
        else:
            fIncorrectPassword()

    # Create the login button for the user to press after they've entered their password
    loginButton = tk.Button(master=mw,bd=0,text="SIGN IN",font=('Helvetica',10), bg='black',fg='white',activebackground='black',activeforeground='white', relief=FLAT, command=fCheckPass)
    loginButton.place(x=140,y=150)


##########################
#  Database Registration #
##########################


    def databaseRegister(username,password,security):

        # Connect to db
        DbConn = pyDb.win_connect_mdb("Database\\UsrDet.accdb")
        DbCursor = DbConn.cursor()

        # Convert the password given to hash
        password = SHA512_Hash.fGetHash(password)

        # Get the next available ID
        DbCursor.execute("SELECT ID FROM Credentials;")
        lastID = 0
        
        while True:
            row = DbCursor.fetchone()
            if row:
                lastID = row[0]
            else:
                nextID = lastID + 1
                print("Next available ID:",nextID)
                break
        
        # Check if the username is already in use
        DbCursor.execute("SELECT Usernames FROM Credentials;")
        usernamesList = []
        
        while True:
            rowUsername = DbCursor.fetchone()
            if rowUsername:
                rowUsername = rowUsername[0]
                rowUsername = rowUsername.replace(" ","")
                usernamesList.append(rowUsername)
            else:
                break

        if username in usernamesList:
            print("Username already taken!")
            usernameTaken = Label(master=signUpWindow,text="Username already taken!",font=('Helvetica',8),fg='red',bg='black')
            usernameTaken.place(x=205,y=350)

        else:
            DbCursor.execute('INSERT INTO Credentials (ID, Usernames, Hash, Code) values (?,?,?,?);',[nextID,username,password,security]).commit()
            DbCursor.execute('INSERT INTO Permissions (Admin) values (0);').commit()
            DbCursor.close()
        
            removeWidgets(signUpWindow)
            fCheckPass()

            accountCreatedLabel = Label(master=mw,text="Account creation successful!",font=('Helvetica',8),fg='green',bg='black')
            accountCreatedLabel.place(x=145,y=210)


##########################
#    Sign Up Window      #
##########################


    ## Register the details the user entered ##
    def fRegistration():

        global usernameSignUp
        global passwordSignUp
        global securityCode

        # Create an error label for each error

        errorPass = Label(master=signUpWindow,text="You must create a password!",font=('Helvetica',8),fg='red',bg='black')
        errorUser1 = Label(master=signUpWindow,text="You must create a username!",font=('Helvetica',8),fg='red',bg='black')
        errorCode2 = Label(master=signUpWindow,text="Your security code must be 4 digits!",font=('Helvetica',8),fg='red',bg='black')
        
        # Make sure the entry boxes are not empty

        usernameBox = usernameSignUp.get()
        passwordBox = passwordSignUp.get()
        securityBox = securityCode.get()

        if passwordBox == "password" or passwordBox == "Password":
            print("Please enter a stronger password!")
            passwordSignUp.delete(0,END)
            return
        if usernameBox == "":
            print("errorUser1")
            errorUser1.place(x=190,y=350)
            return
        elif passwordBox == "":
            print("errorUserPass")
            errorPass.place(x=190,y=350)
            return
        elif len(securityBox) <4:
            print("errorCode2")
            errorCode2.place(x=190,y=350)
            return
        else:
            databaseRegister(usernameBox,passwordBox,securityBox)

    # Create the window and widgets on it
    def fSignUp():

        global signUpWindow
        global usernameSignUp
        global passwordSignUp
        global securityCode
        global securityCheck

        signUpWindow = Toplevel(master=mw,height=500,width=550,bg='black')
        signUpWindow.resizable(0,0)
        signUpWindow.iconbitmap('Images\\favicon.ico')
        signUpWindow.title("Social Club Account Creation")
        
        signUpLOGO = PhotoImage(file='Images\social_clublogo.ppm')
        signUpLOGO.image = signUpLOGO
        
        signUpLabel = Label(master=signUpWindow,image=signUpLOGO,bd=0)
        signUpLabel.place(x=215,y=20)

        # Create the CREATE ACCOUNT title
        createAccount = Label(master=signUpWindow,text="CREATE ACCOUNT:",font=('Helvetica',11,'underline','bold'),fg='white',bg='black')
        createAccount.place(x=130,y=105)
        
        # Create the entry boxes
        usernameSignUp = Entry(master=signUpWindow,width=30)
        passwordSignUp = Entry(master=signUpWindow,width=30,show="*")
        securityCheck = StringVar()
        securityCode = Entry(master=signUpWindow,width=10,textvariable=securityCheck)

        usernameSignUp.place(x=215,y=165)
        passwordSignUp.place(x=215,y=195)
        securityCode.place(x=215,y=238)

        usernameLabel = Label(master=signUpWindow,text="USERNAME:",font=('Helvetica',9),fg='white',bg='black')
        passwordLabel = Label(master=signUpWindow,text="PASSWORD:",font=('Helvetica',9),fg='white',bg='black')
        securityLabel = Label(master=signUpWindow,text="SECURITY\n CODE:*",font=('Helvetica',9),fg='white',bg='black')

        usernameLabel.place(x=132,y=165)
        passwordLabel.place(x=130,y=195)
        securityLabel.place(x=135,y=225)

        createAccount2 = Button(master=signUpWindow,bd=0,image=roundedRectangle,text="JOIN NOW",font=('Helvetica',9,'bold'),bg='black',activebackground='black',relief=FLAT,compound=CENTER,command=fRegistration)
        createAccount2.place(x=230,y=300)

        securityDescription = Label(master=signUpWindow,text='''*Your 4-Digit security code will be used if you forget your password and need to recover your account.
    It should remain a secret and should be something you'll easily remember that is secure at the same time.
    Try avoid using commonly used combinations of numbers such as '1234' or '1111', etc...''',font=('Helvetica',7),fg='#A9A9A9',bg='black')
        securityDescription.place(x=45,y=400)

        usernameSignUp.bind("<Return>",lambda x: fRegistration())
        passwordSignUp.bind("<Return>",lambda x: fRegistration())
        securityCode.bind("<Return>",lambda x: fRegistration())
        
        # Check the length of the security information entered
        # Check to see if the security code contains numbers
        def on_typing(*args):
            validDigits = ["0","1","2","3","4","5","6","7","8","9","0"]
            digits = securityCheck.get()
            currentDigit = ""

            # Tells the function to only process one number at a time
            if len(digits) == 0:
                currentDigit = digits[0:0]
            elif len(digits) == 1:
                currentDigit = digits[0:1]
            elif len(digits) == 2:
                currentDigit = digits[1:2]
            elif len(digits) == 3:
                currentDigit = digits[2:3]
            elif len(digits) == 4:
                currentDigit = digits[3:4]
            else:
                securityCheck.set(digits[:4])

            # First number is always empty. Create an exception for it
            if currentDigit == "":
                return
            if currentDigit not in validDigits:    
                securityCheck.set(digits[:len(digits)-1])
        securityCheck.trace_variable("w",on_typing)

    # Check if CREATE ACCOUNT window is open
    def fCreateAccountChecks():

        global signUpWindow
        
        print("Checking...")
        try:
            isOpened = signUpWindow.winfo_exists()
            if isOpened == 1:
                print("Create account already open")
                return
            else:
                print("Returned 0 - Continuing...")
                fSignUp()
        except:
            print("Continuing...")
            fSignUp()

    # Create the 'JOIN SOCIAL CLUB' button
    roundedRectangle = PhotoImage(master=mw,file='Images\\roundedRectangle.ppm')
    roundedRectangle.image = roundedRectangle

    createAccount = Button(master=mw,bd=0,image=roundedRectangle,text="JOIN NOW",font=('Helvetica',9,'bold'),bg='black',activebackground='black',relief=FLAT,compound=CENTER,command=fCreateAccountChecks)
    createAccount.place(x=220,y=140)

    # Import the loading gif
    gifFrames = [PhotoImage(file='Images\Loading_icon.gif',format = 'gif -index %i' %(i)) for i in range(0,36)]


##########################
#   Sign Out Function    #
##########################


    def fSignOUT():

        global pw
        global permissionWindow
        
        path = "Database\\f_status"
        os.path.join(path, '*')
        status_FILE = open(path,"r+")
        htmlSTATUS = status_FILE.read()
        status_FILE.close()

        if htmlSTATUS == "1":
            print("Can't sign out now")
            return
        else:
            print("Signing out...")
            removeWidgets(pw)
            try:
                removeWidgets(permissionWindow)
            except:
                print()
            __init__()



##########################################
##########################################
##                                      ##
##     MAIN PROGRAM INITALISATION       ##
##                                      ##
##########################################
##########################################



    # Setting up some variables
    # Creating checks to see what tab has been created or not
    alreadyCreatedSystem = [False]
    alreadyCreatedGames = [False]
    alreadyCreatedAbout = [False]
    alreadyCreatedOther = [False]

    # Setup an external file to be imported into different scripts and functions. Prevents 'cyclical dependency' 
    path = "Database\\f_status"
    os.path.join(path, '*')

    status_FILE = open(path,"w")
    status_FILE.write('0')
    status_FILE.close()

    # Create the main program window which will give the user the ability to interact with the program
    def fProgramWindow():

        global pw
        global currentUser
        global alreadyCreatedSystem
        global alreadyCreatedGames
        global alreadyCreatedAbout
        global alreadyCreatedOther
        global htmlSTATUS
        global gifFrames
        global userWhitelist
        global overlayWindow
        
        # Make the Program Window (PW)
        pw = tk.Tk()
        pw.geometry('1200x700')
        pw.title("Rockstar Games - Requirements")
        pw.iconbitmap('Images\\favicon.ico')
        pw.attributes('-topmost', True)
        pw.attributes('-topmost', False)
        pw.resizable(0,0)
        pw.withdraw()

        # Center the login window
        def centerWindow(pw):
            pw.update_idletasks()
            w = pw.winfo_screenwidth()
            h = pw.winfo_screenheight()
            size = tuple(int(_) for _ in pw.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            pw.geometry("%dx%d+%d+%d" % (size + (x, y)))
        centerWindow(pw)
        
        # Create the tabs in the window/notebook
        tabMasterWindow = ttk.Notebook(pw)
        
        tabSys1 = ttk.Frame(tabMasterWindow,width=0)
        tabGame2 = ttk.Frame(tabMasterWindow,width=0)
        tabAbout3 = ttk.Frame(tabMasterWindow,width=0)
        tabOther4 = ttk.Frame(tabMasterWindow,width=0)

        tabMasterWindow.add(tabSys1,state='hidden',text='System Information')
        tabMasterWindow.add(tabGame2,state='hidden',text='Games List')
        tabMasterWindow.add(tabAbout3,state='hidden',text='About')
        tabMasterWindow.add(tabOther4,state='hidden',text='Other')

        # Create the Canvas for the background picture
        pwCanvas = Canvas(master=tabMasterWindow,width=1200,height=700,highlightthickness=0)
        pwCanvas.pack(expand=YES, fill=BOTH)

        # Place the background on the Canvas
        pw.background = PhotoImage(master=pwCanvas, file='Images\\rockstar-background.ppm')
        pwCanvas.create_image(0,0,image=pw.background,anchor=NW)

        # Draws the tab bar
        tabMasterWindow.pack(fill='both', expand='yes')

        # Apply labels/information to notebook tabs
        sysLabel = Label(tabSys1, text="System Information")
        gameLabel = Label(tabGame2, text="Games List")
        aboutLabel = Label(tabAbout3, text="About")
        otherLabel = Label(tabOther4, text="Other")

        sysLabel.pack
        sysLabel.pack()
        gameLabel.pack()
        aboutLabel.pack()
        otherLabel.pack()

        # Create a semi-transparent overlay when loading hardware tests

        def overlayFunction():

            global overlayWindow
            
            overlayWindow = tk.Tk()
            overlayLabel = Label(overlayWindow,text="Loading...",bg='black',font=('Helvetica',30),fg='#A9A9A9')
            overlayWindow.geometry('+250+250')
            overlayWindow.overrideredirect(True)
            overlayWindow.lift()
            overlayWindow.attributes('-alpha', 0.5)
            overlayLabel.pack()

            # Center the overlay window
            def centerWindow(overlayWindow):
                overlayWindow.update_idletasks()
                w = overlayWindow.winfo_screenwidth()
                h = overlayWindow.winfo_screenheight()
                size = tuple(int(_) for _ in overlayWindow.geometry().split('+')[0].split('x'))
                x = w/2 - size[0]/2
                y = 10
                overlayWindow.geometry("%dx%d+%d+%d" % (size + (x,y)))

            # Python needs to call the function twice so that it is actually centered?
            # Need to call return before mainloop to stop Python from hanging/freezing
            # Mainloop needs to be used so that the window is transparent
                
            centerWindow(overlayWindow)
            centerWindow(overlayWindow)
            return
            overlayWindow.mainloop()


        ##########################
        #    Retrieve Hardware   #
        ##########################

        
        # Create the function which gets the user's information
        def retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD):

            wmi = PLUGIN_wmi

            # Retrieve computer information, HDD information and processor information
            hardware = wmi.WMI()
            computer_info = hardware.Win32_ComputerSystem()[0]
            proc_info = hardware.Win32_Processor()[0]
            hard_info = hardware.Win32_LogicalDisk()[0]

            # Convert the free space to GB
            freeSpace = int(hard_info.FreeSpace)
            freeSpace = (freeSpace/1073741824)
            freeSpace = math.ceil(freeSpace)

            # gpu_info is always Integrated Graphics (e.g Intel HD Graphics)
            # gpu_info2 is always Dedicated Graphics (e.g NVIDIA GTX 1080)
            # Try get the dedicated GPU - if an error is raised, use the integrated GPU 
            gpu_info = hardware.Win32_VideoController()[0]
            gpu_info2 = hardware.Win32_VideoController()[1]
            
            if "Driver" in gpu_info.Name or "Graphics" in gpu_info.Name:
                gpu_infoFinal = gpu_info2
            if "Driver" in gpu_info2.Name or "Graphics" in gpu_info2.Name:
                gpu_infoFinal = gpu_info
            else:
                gpu_infoFinal = gpu_info2
            
            # Use OS information to get RAM as a float - round it up to the nearest one
            os_info = hardware.Win32_OperatingSystem()[0]
            system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
            system_ram = math.ceil(system_ram)

            # Print the information gathered from the user's system replacing unecessary words
            proc_name = proc_info.Name.replace(" CPU","")
            proc_name = proc_name.replace("(TM)","")
            proc_name = proc_name.replace("(R)","")
            
            gpu_name = gpu_infoFinal.Name.replace("(TM)","")
            gpu_name = gpu_name.replace("NVIDIA ","")
            gpu_name = gpu_name.replace("AMD ","")
            gpu_name = gpu_name.replace("(R)","")

            print()
            print("CPU:",proc_name)
            print("GPU:",gpu_name)
            print("RAM:",str(system_ram)+"GB")
            print("HDD:",str(freeSpace)+"GB")
            print()

            # Open the database of hardware and get the rank of the user's hardware
            cpuText = open("Resources\passmarkTableCPU.txt","r+")
            cpuList = cpuText.read()
            
            cpuList = cpuList.replace("[","")
            cpuList = cpuList.replace("]","")
            cpuList = cpuList.replace("'","")
            cpuList = cpuList.replace(", ",",")
            cpuList = cpuList.split(",")
            
            cpuPos = cpuList.index(proc_name)
            cpuRank = cpuList[cpuPos+1]

            # Repeat for graphics card
            gpuText = open("Resources\passmarkTableGPU.txt","r+")
            gpuList = gpuText.read()
            
            gpuList = gpuList.replace("[","")
            gpuList = gpuList.replace("]","")
            gpuList = gpuList.replace("'","")
            gpuList = gpuList.replace(", ",",")
            gpuList = gpuList.split(",")
            
            gpuPos = gpuList.index(gpu_name)
            gpuRank = gpuList[gpuPos+1]

            # Return the real names and ranks of each piece of hardware
            rCPU = cpuRank
            rGPU = gpuRank
            rRAM = system_ram
            rHDD = freeSpace

            uCPU = proc_info.Name
            uGPU = gpu_infoFinal.Name
            uRAM = system_ram
            uHDD = freeSpace

            return uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD
        
        
        ##########################
        #    Create NAV Bar      #
        ##########################
        

        # Import the image to be used when a tab has been selected
        NAVimageSelected = PhotoImage(master=pw,file='Images\\NAV-BarSelected.ppm')

        # Import the image to be used in the NAV Bar
        NAVimage = PhotoImage(master=pw,file='Images\\NAV-Bar.PPM')

        # Apply my information to the bottom left of the program
        authorBanner = Label(master=pw,image=NAVimage,width=600,height=30,bd=0,anchor=SW)
        authorBanner2 = Label(master=pw,image=NAVimage,width=600,height=30,bd=0,anchor=SW)
        authorInfo = Label(master=pw,text="© SCOTT CRAWLEY\n POST 16 CS",fg='#A9A9A9',bg='black',bd=0,font=('Helvetica',6,'bold'))
        
        authorBanner.place(x=0,y=674)
        authorBanner2.place(x=600,y=674)
        authorInfo.place(x=10,y=676)

        # Add the currently signed in user to the bottom right
        userWhitelist = currentUser
        currentUser = currentUser.upper()
        currentUser = currentUser.replace(" ","")
        currentInfo = Label(master=pw,text="Logged in as:",font=('Helvetica',7,'bold'),fg='#A9A9A9',bg='black')

        # Create a context menu (right-click menu)
        def popupMenu(event):
            userLoggedMENU.post(event.x_root, event.y_root)
        
        userLoggedIn = Menubutton(master=pw,text=currentUser,font=('Helvetica',7,'bold','underline'),bg='black',fg='white',relief=FLAT,bd=0,activebackground='#e5e5e5')
        userLoggedMENU = Menu(userLoggedIn,tearoff=0,bg='black',fg='#A9A9A9',activeforeground='white',activebackground='black',relief=SUNKEN)
        userLoggedMENU.add_command(label="SIGN OUT",font=('Helvetica',9,'bold'),command=fSignOUT)

        # Bind both left-click and right-click to the menu
        # Make sure the context menu only appears when clicking the button
        userLoggedIn.bind("<Button-3>", popupMenu)
        userLoggedIn.bind("<Button-1>", popupMenu)
        
        userLoggedIn.place(x=1100,y=679)
        currentInfo.place(x=1035,y=679)


        ##########################
        #      TAB CREATION      #
        ##########################
        
        
        def resetCanvas(canvas,boolVar,scrollbar,frame):

            # Resets the canvas on given tab
            removeWidgets(canvas)
            removeWidgets(scrollbar)
            removeWidgets(frame)
            boolVar[0] = False
            return boolVar
        
        def fNAVSys():

            ### SYSTEM INFORMATION TAB ###
            
            global alreadyCreatedSystem
            global systemCanvas
            global systemScrollbar
            global systemFrame
            global hardwareFrame
            
            fResetNAVSelection()
            pw.title("R* Requirement Tool - System Information")
            systemInfoNAV.config(fg='white',image=NAVimageSelected)
            tabMasterWindow.select(tabSys1)

            if alreadyCreatedSystem[0] == False:
                print(">Created systemCanvas")
                alreadyCreatedSystem[0] = True

                systemFrame = Frame(master=pwCanvas,width=600,height=620)
                systemFrame.pack(side=BOTTOM)
                systemScrollbar = Scrollbar(master=systemFrame)
                systemCanvas = Canvas(master=systemFrame,width=600,height=620,bg='white')
                hardwareFrame = Frame(master=systemCanvas,width=620,height=820,bg='white')

                systemCanvas.pack(side=BOTTOM)
                systemCanvas.create_window((0,0),window=hardwareFrame,anchor=NW)

                print("System",str(alreadyCreatedSystem))
                print()
                
                ##################### ADD TO THE TAB CANVAS BELOW HERE #####################
                
                objectFrame = PhotoImage(master=hardwareFrame,file='Images\\rectangleBackground.ppm')
                objectFrame.image = objectFrame

                # Processor Information
                CPUtitle = Label(master=hardwareFrame,text="PROCESSOR (CPU):",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=W,pady=10)
                CPUtitle.place(x=0,y=0)

                CPUUser = Label(master=hardwareFrame,text="YOUR CPU:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                CPUUser.place(x=0,y=39)
                CPURequired = Label(master=hardwareFrame,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                CPURequired.place(x=0,y=96)
                
                # RAM Information
                RAMtitle = Label(master=hardwareFrame,text="MEMORY (RAM):",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=W,pady=10)
                RAMtitle.place(x=0,y=145)

                RAMUser = Label(master=hardwareFrame,text="YOUR RAM:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                RAMUser.place(x=0,y=184)
                RAMRequired = Label(master=hardwareFrame,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                RAMRequired.place(x=0,y=241)
                
                # Graphics Card Information
                GPUtitle = Label(master=hardwareFrame,text="GRAPHICS CARD (GPU):",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=W,pady=10)
                GPUtitle.place(x=0,y=290)

                GPUUser = Label(master=hardwareFrame,text="YOUR GPU:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                GPUUser.place(x=0,y=329)
                GPURequired = Label(master=hardwareFrame,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                GPURequired.place(x=0,y=386)

                # Hard Drive Space Available
                HDDtitle = Label(master=hardwareFrame,text="HARD DRIVE (HDD):",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=W,pady=10)
                HDDtitle.place(x=0,y=435)

                HDDUser = Label(master=hardwareFrame,text="YOUR HDD:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                HDDUser.place(x=0,y=474)
                HDDRequired = Label(master=hardwareFrame,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                HDDRequired.place(x=0,y=531)

            else:
                print("already created window: SYS")
                print()
                return

        def _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD):

            global hardwareFrame
            global overlayWindow

            crossImage = PhotoImage(master=hardwareFrame,file="Images\\cross.ppm")
            crossImage.image = crossImage
            tickImage = PhotoImage(master=hardwareFrame,file="Images\\tick.ppm")
            tickImage.image = tickImage

            if cpuRank < rCPU:
                crossImageCPU = Label(hardwareFrame,image=crossImage,bd=0)
                crossImageCPU.place(x=500,y=70)
            else:
                tickImageCPU = Label(hardwareFrame,image=tickImage,bd=0)
                tickImageCPU.place(x=500,y=70)

            if gpuRank < rGPU:
                crossImageGPU = Label(hardwareFrame,image=crossImage,bd=0)
                crossImageGPU.place(x=500,y=360)
            else:
                tickImageGPU = Label(hardwareFrame,image=tickImage,bd=0)
                tickImageGPU.place(x=500,y=360)

            if ramRank > rRAM:
                crossImageRAM = Label(hardwareFrame,image=crossImage,bd=0)
                crossImageRAM.place(x=500,y=210)
            else:
                tickImageRAM = Label(hardwareFrame,image=tickImage,bd=0)
                tickImageRAM.place(x=500,y=210)

            if hddRank > rHDD:
                crossImageHDD = Label(hardwareFrame,image=crossImage,bd=0)
                crossImageHDD.place(x=500,y=505)
            else:
                tickImageHDD = Label(hardwareFrame,image=tickImage,bd=0)
                tickImageHDD.place(x=500,y=505)

            CPU.place(x=0,y=110)
            GPU.place(x=0,y=400)
            RAM.place(x=0,y=258)
            HDD.place(x=0,y=548)

            lCPU = Label(master=hardwareFrame,text=uCPU,font=('Helvetica',10))
            lGPU = Label(master=hardwareFrame,text=uGPU,font=('Helvetica',10))
            lRAM = Label(master=hardwareFrame,text=str(uRAM)+"GB RAM",font=('Helvetica',10))
            lHDD = Label(master=hardwareFrame,text=str(uHDD)+"GB Free Space",font=('Helvetica',10))

            lCPU.place(x=0,y=53)
            lGPU.place(x=0,y=343)
            lRAM.place(x=0,y=198)
            lHDD.place(x=0,y=488)

            removeWidgets(overlayWindow)


        ##########################
        #   Game Requirements    #
        ##########################


        def fViceCity():

            global hardwareFrame

            print("Vice City chosen")
            print("Getting hardware information...")
            overlayFunction()

            # Assign the user's hardware information to some labels
    
            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Pentium III @ 800 MHz (1 CPU) or AMD Athlon @ 800 MHz (1 CPU)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="32MB NVIDIA GeForce2 MX",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="128 MB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="1GB Free Space",font=('Helvetica',10))

            cpuRank = 2474
            gpuRank = 1566
            ramRank = 0.128
            hddRank = 1

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)
            
        def fMidnightClub():

            global hardwareFrame

            print("Midnight Club chosen")
            print("Getting hardware information...")
            overlayFunction()
            
            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()
            
            CPU = Label(master=hardwareFrame,text="Intel Pentium III @ 800 MHz (1 CPU) or AMD Athlon @ 800 MHz (1 CPU)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="32MB NVIDIA GeForce2 MX",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="128 MB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="1.5GB Free Space",font=('Helvetica',10))

            cpuRank = 2474
            gpuRank = 1566
            ramRank = 0.128
            hddRank = 1.5

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fMaxPayne2():

            global hardwareFrame

            print("Max Payne 2 chosen")
            print("Getting hardware information...")
            overlayFunction()
            
            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Celeron @ 1.2 GHz (1 CPU) or 1.2 GHz AMD Duron (1 CPU)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="64MB NVIDIA GeForce2 MX",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="256 MB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="1.5GB Free Space",font=('Helvetica',10))

            cpuRank = 2612
            gpuRank = 1566
            ramRank = 0.256
            hddRank = 1.5

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fSanAndreas():

            global hardwareFrame
            
            print("San Andreas chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()
            
            CPU = Label(master=hardwareFrame,text="Intel Pentium III @ 1.0 GHz (1 CPU) or AMD Athlon @ 800 MHz (1 CPU)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="64MB NVIDIA GeForce3",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="256 MB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="3.6GB Free Space",font=('Helvetica',10))

            cpuRank = 2474
            gpuRank = 1566
            ramRank = 0.256
            hddRank = 3.6

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)
            
        def fLibertyCityStories():

            global hardwareFrame
            
            print("Grand Theft Auto: Liberty City Stories chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Pentium III @ 1.0 GHz (1 CPU) or AMD Athlon @ 800 MHz (1 CPU)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="64MB NVIDIA GeForce3",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="256 MB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="2GB Free Space",font=('Helvetica',10))

            cpuRank = 2612
            gpuRank = 1566
            ramRank = 0.256
            hddRank = 2

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)
            
        def fBully():

            global hardwareFrame

            print("Bully chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Pentium 4 @ 3.0 GHz (1 CPU) or AMD Athlon 3000 (1 CPU)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="256MB NVIDIA GeForce 7300",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="1 GB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="4.7GB Free Space",font=('Helvetica',10))

            cpuRank = 2572
            gpuRank = 1276
            ramRank = 1
            hddRank = 4.7

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fManhunt():

            global hardwareFrame

            print("Manhunt 2 chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Pentium 4 @ 1.7 GHz (1 CPU) or AMD Athlon 3000 (1 CPU)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="128MB NVIDIA 6200GT",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="512 MB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="4GB Free Space",font=('Helvetica',10))

            cpuRank = 2572
            gpuRank = 1336
            ramRank = 0.512
            hddRank = 4

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fGTA4():

            global hardwareFrame

            print("Grand Theft Auto IV chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Core 2 Duo @ 1.8 GHz (2 CPUs) or AMD Athlon X2 64 2.4GHz (2 CPUs)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="256MB NVIDIA 7900",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="1 GB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="16GB Free Space",font=('Helvetica',10))

            cpuRank = 2333
            gpuRank = 990
            ramRank = 1
            hddRank = 16

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fGTA4v2():

            global hardwareFrame

            print("Grand Theft Auto: EFLC chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Core 2 Duo @ 1.8 GHz (2 CPUs) or AMD Athlon X2 64 2.4GHz (2 CPUs)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="256MB NVIDIA 7900",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="1 GB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="16GB Free Space",font=('Helvetica',10))

            cpuRank = 2333
            gpuRank = 990
            ramRank = 1
            hddRank = 16

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fNoire():

            global hardwareFrame
            
            print("L.A. Noire chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Core 2 Duo @ 2.2 GHz (2 CPUs) or AMD Dual Core 2.4 GHz (2 CPUs)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="512MB NVIDIA 8600",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="2 GB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="16GB Free Space",font=('Helvetica',10))

            cpuRank = 1995
            gpuRank = 963
            ramRank = 2
            hddRank = 16

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fMaxPayne3():

            global hardwareFrame

            print("Max Payne 3 chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Dual Core @ 2.4 GHz (2 CPUs) AMD Dual Core 2.4 GHz (2 CPUs)",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="512MB NVIDIA 8600 GT",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="2 GB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="35GB Free Space",font=('Helvetica',10))

            cpuRank = 1755
            gpuRank = 999
            ramRank = 2
            hddRank = 35

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fGTA5():

            global hardwareFrame

            print("Grand Theft Auto V chosen")
            print("Getting hardware information...")
            overlayFunction()

            uCPU = " "
            uGPU = " "
            uRAM = " "
            uHDD = " "
            rCPU = 0
            rGPU = 0
            rRAM = 0
            rHDD = 0

            hardwareList = retrieveHardware(uCPU,uGPU,uRAM,uHDD,rCPU,rGPU,rRAM,rHDD)
            hardwareList = list(hardwareList)

            uCPU = hardwareList[0]
            uGPU = hardwareList[1]
            uRAM = hardwareList[2]
            uHDD = hardwareList[3]

            fNAVSys()

            CPU = Label(master=hardwareFrame,text="Intel Core 2 Quad Q6600 @ 2.4 GHz or AMD Phenom 9850 Quad-Core @ 2.5GHz",font=('Helvetica',10))
            GPU = Label(master=hardwareFrame,text="1GB NVIDIA 9800 GT",font=('Helvetica',10))
            RAM = Label(master=hardwareFrame,text="4 GB RAM",font=('Helvetica',10))
            HDD = Label(master=hardwareFrame,text="72GB Free Space",font=('Helvetica',10))

            cpuRank = 1100
            gpuRank = 628
            ramRank = 4
            hddRank = 72

            rCPU = int(hardwareList[4])
            rGPU = int(hardwareList[5])
            rRAM = int(hardwareList[6])
            rHDD = int(hardwareList[7])

            _gameInit_(CPU,GPU,RAM,HDD,rCPU,rGPU,rRAM,rHDD,cpuRank,gpuRank,ramRank,hddRank,uCPU,uGPU,uRAM,uHDD)

        def fNAVGames():

            ### GAMES SELECTION TAB ### 

            global alreadyCreatedGames
            global gamesCanvas
            global gamesScrollbar
            global gamesFrame
            global buttonsFrame
            global scrollNum
            
            fResetNAVSelection()
            pw.title("R* Requirement Tool - Games List")
            gamesListNAV.config(fg='white',image=NAVimageSelected)
            tabMasterWindow.select(tabGame2)

            if alreadyCreatedGames[0] == False:
                print(">Created gamesCanvas")
                alreadyCreatedGames[0] = True

                # Create the Frame and Canvas for the scrollbar
                gamesFrame = Frame(master=pwCanvas,width=600,height=620)
                gamesFrame.pack(side=BOTTOM)
                gamesScrollbar = Scrollbar(master=gamesFrame)
                gamesCanvas = Canvas(master=gamesFrame,width=600,height=620,yscrollcommand=gamesScrollbar.set,highlightthickness=0,bg='white')
                gamesCanvas.config(scrollregion=[0,0,600,1050])
                buttonsFrame = Frame(master=gamesCanvas,width=600,height=1000,bg='white')
                gamesScrollbar.config(command=gamesCanvas.yview,width=10)
                gamesScrollbar.pack(side=RIGHT,fill=Y)
                
                gamesCanvas.pack(side=BOTTOM)
                gamesCanvas.create_window((0,0),window=buttonsFrame,anchor=NW)

                # Creating the function which allows us to use the mousewheel to control the scrollbar
                scrollNum = 0

                def mouseWheel(event):
                    global scrollNum
                    if alreadyCreatedGames[0] == True:
                        def delta(event):
                            if event.num == 5 or event.delta < 0:
                                #print(event.delta)
                                return 1
                            return -1
                        scrollNum += delta(event)
                        gamesCanvas.yview_scroll(delta(event),UNITS)

                pw.bind("<MouseWheel>",mouseWheel)
                print("Games",str(alreadyCreatedGames))
                print()

                ##################### ADD TO THE TAB CANVAS BELOW HERE #####################

                # Add the button for Grand Theft Auto: Vice City (2002)
                viceCover = PhotoImage(master=buttonsFrame,file="Images\\VC_Cover.ppm")
                viceCover.image = viceCover

                viceButton = Button(master=buttonsFrame,image=viceCover,width=150,height=200,relief=GROOVE,command=fViceCity)
                viceButton.place(x=30,y=20)

                # Add the button for Midnight Club II (2003)
                midnightCover = PhotoImage(master=buttonsFrame,file="Images\\Midnight_Cover.ppm")
                midnightCover.image = midnightCover

                midnightButton = Button(master=buttonsFrame,image=midnightCover,width=150,height=200,relief=GROOVE,command=fMidnightClub)
                midnightButton.place(x=230,y=20)

                # Add the button for Max Payne 2 (2003)
                max2Cover = PhotoImage(master=buttonsFrame,file="Images\\Max2_Cover.ppm")
                max2Cover.image = max2Cover

                max2Button = Button(master=buttonsFrame,image=max2Cover,width=150,height=200,relief=GROOVE,command=fMaxPayne2)
                max2Button.place(x=430,y=20)

                # Add the button for Grand Theft Auto: San Andreas (2004)
                saCover = PhotoImage(master=buttonsFrame,file="Images\\SA_Cover.ppm")
                saCover.image = saCover

                saButton = Button(master=buttonsFrame,image=saCover,width=150,height=200,relief=GROOVE,command=fSanAndreas)
                saButton.place(x=30,y=270)

                # Add the button for Grand Theft Auto: Liberty City Stories (2005)
                lscCover = PhotoImage(master=buttonsFrame,file="Images\\LCS_Cover.ppm")
                lscCover.image = lscCover

                lscButton = Button(master=buttonsFrame,image=lscCover,width=150,height=200,relief=GROOVE,command=fLibertyCityStories)
                lscButton.place(x=230,y=270)

                # Add the button for Bully (2006)
                bullyCover = PhotoImage(master=buttonsFrame,file="Images\\Bully_Cover.ppm")
                bullyCover.image = bullyCover

                bullyButton = Button(master=buttonsFrame,image=bullyCover,width=150,height=200,relief=GROOVE,command=fBully)
                bullyButton.place(x=430,y=270)

                # Add the button for Manhunt 2 (2007)
                manhuntCover = PhotoImage(master=buttonsFrame,file="Images\\Manhunt_Cover.ppm")
                manhuntCover.image = manhuntCover

                manhuntButton = Button(master=buttonsFrame,image=manhuntCover,width=150,height=200,relief=GROOVE,command=fManhunt)
                manhuntButton.place(x=30,y=520)

                # Add the button for Grand Theft Auto IV (2008)
                gta4Cover = PhotoImage(master=buttonsFrame,file="Images\\GTA4_Cover.ppm")
                gta4Cover.image = gta4Cover

                gta4Button = Button(master=buttonsFrame,image=gta4Cover,width=150,height=200,relief=GROOVE,command=fGTA4)
                gta4Button.place(x=230,y=520)

                # Add the button for Grand Theft Auto: EFLC (2009)
                eflcCover = PhotoImage(master=buttonsFrame,file="Images\\GTAEFLC_Cover.ppm")
                eflcCover.image = eflcCover

                eflcButton = Button(master=buttonsFrame,image=eflcCover,width=150,height=200,relief=GROOVE,command=fGTA4v2)
                eflcButton.place(x=430,y=520)

                # Add the button for L.A. Noire (2011)
                noireCover = PhotoImage(master=buttonsFrame,file="Images\\L.A_Cover.ppm")
                noireCover.image = noireCover

                noireButton = Button(master=buttonsFrame,image=noireCover,width=150,height=200,relief=GROOVE,command=fNoire)
                noireButton.place(x=30,y=770)

                # Add the button for Max Payne 3 (2012)
                maxpayneCover = PhotoImage(master=buttonsFrame,file="Images\\Max3_Cover.ppm")
                maxpayneCover.image = maxpayneCover

                maxpayneButton = Button(master=buttonsFrame,image=maxpayneCover,width=150,height=200,relief=GROOVE,command=fMaxPayne3)
                maxpayneButton.place(x=230,y=770)

                # Add the button for Grand Theft Auto V (2013)
                gta5Cover = PhotoImage(master=buttonsFrame,file="Images\\GTAV_Cover.ppm")
                gta5Cover.image = gta5Cover

                gta5Button = Button(master=buttonsFrame,image=gta5Cover,width=150,height=200,relief=GROOVE,command=fGTA5)
                gta5Button.place(x=430,y=770)
                
            else:
                print("already created window: GAMES")
                print()
                return

        def fNAVAbout():

            ### ABOUT TAB ###

            global alreadyCreatedAbout
            global aboutCanvas
            global aboutScrollbar
            global aboutFrame
            
            fResetNAVSelection()
            pw.title("R* Requirement Tool - About Page")
            aboutProgramNAV.config(fg='white',image=NAVimageSelected)
            tabMasterWindow.select(tabAbout3)

            if alreadyCreatedAbout[0] == False:
                print(">Created aboutCanvas")
                alreadyCreatedAbout[0] = True

                aboutFrame = Frame(master=pwCanvas,width=600,height=620)
                aboutFrame.pack(side=BOTTOM)
                aboutScrollbar = Scrollbar(master=pwCanvas)
                aboutScrollbar.pack(side=RIGHT,fill=Y)
                aboutCanvas = Canvas(master=aboutFrame,bg='white',width=600,height=620,yscrollcommand = aboutScrollbar.set)
                aboutCanvas.pack(side=BOTTOM)
                aboutScrollbar.config(command=aboutCanvas.yview,width=5)

                print("About",str(alreadyCreatedAbout))
                print()

                ##################### ADD TO THE TAB CANVAS BELOW HERE #####################

                ### Guide ###
                guideTitle = Label(master=aboutCanvas,text="Guide/Tutorial",font=("Helvetica",15),width=320,anchor=W,pady=20,bg='#3d3d3d',fg='#a9a9a9')
                guideTitle.place(x=0,y=7)

                introLabel = Label(master=aboutCanvas,text='''On the [SYSTEM INFORMATION] tab there are four categories containing information that determines
whether or not your system will be able to run your chosen game. Both your RAM and
FREE SPACE need to be greater than the required amounts but, as for your PROCESSOR and
GRAPHICS CARD, the program will calculate everything for you using Online resources.''',font=("Helvetica",10),anchor=W,justify=LEFT,width=320)

                stepsLabel = Label(master=aboutCanvas,text='''----------------------------------------------------------------------------------------------------------------------------------------------------------------------
1 - Begin by going to the [GAMES LIST] tab and choosing a game.\n
2 - Wait for the program to finish gathering your system information.\n
3 - Once completed, you will be taken to the [SYSTEM INFORMATION] tab automatically.\n
4 - From here you will see either a TICK or CROSS next to each category\n
5 - A full set of ticks indicate you can run the game. Any less and it's very unlikely you'll be able to.''',font=("Helvetica",9),anchor=W,justify=LEFT,width=320)
                introLabel.place(x=0,y=74)
                stepsLabel.place(x=0,y=141)

                ### Info ###
                infoProgram = Label(master=aboutCanvas,text="Information",font=("Helvetica",15),width=320,anchor=W,pady=20,bg='#3d3d3d',fg='#a9a9a9')
                infoProgram.place(x=0,y=300)

                sourcesLabel = Label(master=aboutCanvas,text='''Hardware rankings taken from:
CPU's - https://www.cpubenchmark.net/CPU_mega_page.html
GPU's - https://www.videocardbenchmark.net/GPU_mega_page.html
\nData Storage:
Microsoft Access 2010
\nExternal Python Plugins:
- Pypyodbc: Database connection tool
- WMI and pyWin32: Hardware information
- HTML Fetcher: Written by me
- Password Hasher: Written by me
\nImages/Assets created by me. Rockstar logo's and game covers taken from Google.''',font=("Helvetica",10),anchor=W,justify=LEFT,width=320)
                sourcesLabel.place(x=0,y=367)
            else:
                print("already created window: ABOUT")
                print()
                return

        def fNAVOther():

            ### OTHER TAB ###

            global alreadyCreatedOther
            global otherCanvas
            global otherScrollbar
            global otherFrame
            global userWhitelist
            global adminUsers
            global htmlSTATUS
            global tempRemove
            global adminLabel
            global adminLabel2
            
            fResetNAVSelection()
            pw.title("R* Requirement Tool - Other")
            otherInfoNAV.config(fg='white',image=NAVimageSelected)
            tabMasterWindow.select(tabOther4)

            if alreadyCreatedOther[0] == False:
                print(">Created otherCanvas")
                alreadyCreatedOther[0] = True

                otherFrame = Frame(master=pwCanvas,width=600,height=620)
                otherFrame.pack(side=BOTTOM)
                otherScrollbar = Scrollbar(master=pwCanvas)
                otherScrollbar.pack(side=RIGHT,fill=Y)
                otherCanvas = Canvas(master=otherFrame,bg='white',width=600,height=620,yscrollcommand=otherScrollbar.set)
                otherCanvas.pack(side=BOTTOM)
                otherScrollbar.config(command=otherCanvas.yview,width=5)

                print("Other",str(alreadyCreatedOther))
                print()

                def removeTempFiles(htmlSTATUS):
                    global tempRemove
                    if htmlSTATUS == "1":
                        tempRemove.config(state=DISABLED)
                        return
                    try:
                        shutil.rmtree("__pycache__")
                        os.remove("Resources\\passmarkCPU.html")
                        os.remove("Resources\\passmarkGPU.html")
                        print("Temporary files removed")
                    except:
                        print("Temporary files removed")

                    try:
                        removeWidgets(noTemp)
                    except:
                        print()

                    noTemp = Label(otherCanvas,text="Temp Files Removed",bg='#3d3d3d',fg='green',font=("Helvetica",10))
                    noTemp.place(x=440,y=195)

                def fProgressBarWindow():

                    global htmlSTATUS
                    global adminUsers
                    global userWhitelist
                    global tempRemove
                        
                    path = "Database\\f_status"
                    os.path.join(path, '*')
                    status_FILE = open(path,"r+")
                    htmlSTATUS = status_FILE.read()
                    status_FILE.close()
                    
                    if htmlSTATUS == "0":
                        path = "Database\\f_status"
                        os.path.join(path, '*')
                        status_FILE = open(path,"w")
                        status_FILE.write("1")
                        status_FILE.close()
                        htmlSTATUS = "1"
                        removeTempFiles(htmlSTATUS)
                        fetch_HTML.fFetchHTML()
                        tempRemove.config(state=NORMAL)
                    elif htmlSTATUS == "1":
                        print("Already running")
                    else:
                        print("Error in file f_status")
                    pw.update()

                def managePerms():

                    global permissionWindow
                    
                    permissionWindow = tk.Tk()
                    permissionWindow.geometry("350x150")
                    permissionWindow.config(bg='black')
                    permissionWindow.title("User Permissions")
                    permissionWindow.iconbitmap('Images\\favicon.ico')
                    permissionWindow.attributes('-topmost', True)
                    permissionWindow.attributes('-topmost', False)
                    permissionWindow.resizable(0,0)

                    DbConn = pyDb.win_connect_mdb("Database\\UsrDet.accdb")
                    DbCursor = DbConn.cursor()      
                    DbCursor.execute("SELECT Usernames FROM Credentials;")

                    usernameList = []
                    while True:
                        username = DbCursor.fetchone()
                        if username != None:
                            if username:
                                username = username[0]
                                username = username.replace("(","")
                                username = username.replace("[","")
                                username = username.replace("'","")
                                username = username.replace(")","")
                                username = username.replace("]","")
                                usernameList.append(username)
                                continue
                            else:
                                break
                        else:
                            break
                    
                    varOptions = tk.StringVar()
                    userOptions = ttk.Combobox(permissionWindow,textvariable=varOptions,width=25,height=50)
                    userOptions.bind('<<ComboboxSelected>>')
                    userOptions['values'] = (usernameList)
                    userOptions.set('--Select User--')
                    userOptions.place(x=110,y=20)
                    permissionWindow.withdraw()
                    permissionWindow.deiconify()

                    def fmakeAdmin():
                        global currentAdmin
                        global notUser
                        global madeAdmin
                        global removeLabel
                        global notAdmin
                        selectedUser = varOptions.get()
                        DbCursor.execute("SELECT Usernames, Admin FROM Credentials;")

                        while True:
                            adminCheck = DbCursor.fetchone()
                            if adminCheck != None:
                                if adminCheck[0] == selectedUser:
                                    adminInt = adminCheck[1]
                            else:
                                break
                        if selectedUser != "--Select User--":
                            try:
                                if adminInt == 1:
                                    print("User already Admin")
                                    try:
                                        removeWidgets(currentAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notUser)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(madeAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(removeLabel)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notAdmin)
                                    except:
                                        print()
                                    currentAdmin = Label(permissionWindow,text="User already admin",font=("Helvetica",10),fg='red',bg='black')
                                    currentAdmin.place(x=120,y=120)
                                elif adminInt == None:
                                    try:
                                        removeWidgets(currentAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notUser)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(madeAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(removeLabel)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notAdmin)
                                    except:
                                        print()
                                    notUser = Label(permissionWindow,text="That is not a user!",bg='black',fg='red',font=("Helvetica",10))
                                    notUser.place(x=120,y=120)
                                    print("Not a correct username")
                                else:
                                    # Have to use StrComp to prevent updating same usernames with differemt capitalisation 
                                    print("Added user to admin")
                                    try:
                                        removeWidgets(currentAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notUser)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(madeAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(removeLabel)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notAdmin)
                                    except:
                                        print()
                                    madeAdmin = Label(permissionWindow,text="Added user to Admin",font=("Helvetica",10),fg='green',bg='black')
                                    madeAdmin.place(x=120,y=120)
                                    DbCursor.execute("UPDATE Credentials SET Admin = 1 WHERE StrComp([Usernames],(?),0) = 0;",[selectedUser]).commit()
                            except:
                                print("Not a correct username!")
                                try:
                                    removeWidgets(currentAdmin)
                                except:
                                    print()
                                try:
                                    removeWidgets(notUser)
                                except:
                                    print()
                                try:
                                    removeWidgets(madeAdmin)
                                except:
                                    print()
                                try:
                                    removeWidgets(removeLabel)
                                except:
                                    print()
                                try:
                                    removeWidgets(notAdmin)
                                except:
                                    print()
                                notUser = Label(permissionWindow,text="That is not a user!",bg='black',fg='red',font=("Helvetica",10))
                                notUser.place(x=120,y=120)
                                print("Not a correct username")
                        else:
                            print("That is not a user!")
                            notUser = Label(permissionWindow,text="That is not a user!",bg='black',fg='red',font=("Helvetica",10))
                            notUser.place(x=120,y=120)

                    def fremoveAdmin():
                        global currentAdmin
                        global notUser
                        global madeAdmin
                        global removeLabel
                        global notAdmin
                        selectedUser = varOptions.get()
                        DbCursor.execute("SELECT Usernames, Admin FROM Credentials;")

                        while True:
                            adminCheck = DbCursor.fetchone()
                            if adminCheck != None:
                                if adminCheck[0] == selectedUser:
                                    adminInt = adminCheck[1]
                            else:
                                break
                        if selectedUser != "--Select User--":
                            try:
                                if adminInt == 0:
                                    print("User not an Admin")
                                    try:
                                        removeWidgets(currentAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notUser)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(madeAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(removeLabel)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notAdmin)
                                    except:
                                        print()
                                    notAdmin = Label(permissionWindow,text="User not an admin",font=("Helvetica",10),fg='red',bg='black')
                                    notAdmin.place(x=120,y=120)
                                elif adminInt == None:
                                    try:
                                        removeWidgets(currentAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notUser)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(madeAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(removeLabel)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notAdmin)
                                    except:
                                        print()
                                    notUser = Label(permissionWindow,text="That is not a user!",bg='black',fg='red',font=("Helvetica",10))
                                    notUser.place(x=120,y=120)
                                    print("Not a correct username")
                                else:
                                    # Have to use StrComp to prevent updating same usernames with differemt capitalisation 
                                    print("Removed user from Admin")
                                    try:
                                        removeWidgets(currentAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notUser)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(madeAdmin)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(removeLabel)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(notAdmin)
                                    except:
                                        print()
                                    removeLabel = Label(permissionWindow,text="Removed user from Admin",font=("Helvetica",10),fg='green',bg='black')
                                    removeLabel.place(x=100,y=120)
                                    DbCursor.execute("UPDATE Credentials SET Admin = 0 WHERE StrComp([Usernames],(?),0) = 0;",[selectedUser]).commit()
                            except:
                                print("Not a correct username")
                                try:
                                    removeWidgets(currentAdmin)
                                except:
                                    print()
                                try:
                                    removeWidgets(notUser)
                                except:
                                    print()
                                try:
                                    removeWidgets(madeAdmin)
                                except:
                                    print()
                                try:
                                    removeWidgets(removeLabel)
                                except:
                                    print()
                                try:
                                    removeWidgets(notAdmin)
                                except:
                                    print()
                                notUser = Label(permissionWindow,text="That is not a user!",bg='black',fg='red',font=("Helvetica",10))
                                notUser.place(x=120,y=120)
                                print("Not a correct username")
                        else:
                            print("That is not a user!")
                            notUser = Label(permissionWindow,text="That is not a user!",bg='black',fg='red',font=("Helvetica",10))
                            notUser.place(x=120,y=120)

                    userLabel = Label(permissionWindow,text="USER:",font=("Helvetica",10),bg='black',fg='white')
                    userLabel.place(x=60,y=20)
                    makeAdmin = Button(permissionWindow,text="Make Admin",font=("Helvetica",10),bg='black',fg='white',relief=FLAT,bd=0,command=fmakeAdmin)
                    makeAdmin.place(x=80,y=80)
                    removeAdmin = Button(permissionWindow,text="Remove Admin",font=("Helvetica",10),bg='black',fg='white',relief=FLAT,bd=0,command=fremoveAdmin)
                    removeAdmin.place(x=180,y=80)

                def checkPermsWindow():
                    global permissionWindow
                    print("Checking...")
                    try:
                        isOpened = permissionWindow.winfo_exists()
                        if isOpened == 1:
                            print("Perms Manager already open")
                            return
                        else:
                            print("Returned 0 - Continuing...")
                            managePerms()
                    except:
                        print("Continuing...")
                        managePerms()

                def removeDatabaseFunc():
                    global userWhitelist
                    global adminLabel
                    global adminLabel2
                    try:
                        adminUser.config(state=DISABLED)
                        resetDatabase.config(state=DISABLED)
                        recoverPassword.config(state=DISABLED)
                        os.remove("Database\\UsrDet.accdb")
                        print("Reset database")
                        noData = Label(otherCanvas,text="Database Removed",bg='#3d3d3d',fg='green',font=("Helvetica",10))
                        noData.place(x=470,y=355)
                        noData2 = Label(otherCanvas,text="Database Removed",bg='#3d3d3d',fg='green',font=("Helvetica",10))
                        noData2.place(x=470,y=275)
                        noData3 = Label(otherCanvas,text="Database Removed",bg='#3d3d3d',fg='green',font=("Helvetica",10))
                        noData3.place(x=470,y=435)
                    except:
                        try:
                            removeWidgets(adminLabel)
                            removeWidgets(adminLabel2)
                        except:
                            print()
                        print("Files do not exist")
                        noData = Label(otherCanvas,text="Database Removed",bg='#3d3d3d',fg='green',font=("Helvetica",10))
                        noData.place(x=470,y=355)
                        noData2 = Label(otherCanvas,text="Database Removed",bg='#3d3d3d',fg='green',font=("Helvetica",10))
                        noData2.place(x=470,y=275)
                        noData3 = Label(otherCanvas,text="Database Removed",bg='#3d3d3d',fg='green',font=("Helvetica",10))
                        noData3.place(x=470,y=435)

                def exitProgram():
                    global permissionWindow
                    try:
                        permissionWindow.destroy()
                    except:
                        print()
                    pw.destroy()

                def resetPassword():

                    global windowResetPass
                    global userWhitelist
                    global securityBox

                    global wrongCode
                    global spacesPass
                    global badPass
                    global noPass
                    global correctCode
                    global boxEmpty
                    
                    windowResetPass = tk.Tk()
                    windowResetPass.config(bg='black')
                    windowResetPass.geometry("350x150")
                    windowResetPass.title("Reset Password")
                    windowResetPass.iconbitmap('Images\\favicon.ico')
                    windowResetPass.attributes('-topmost', True)
                    windowResetPass.attributes('-topmost', False)
                    windowResetPass.resizable(0,0)

                    def changePassword():

                        global wrongCode
                        global spacesPass
                        global badPass
                        global noPass
                        global correctCode
                        global boxEmpty
                        
                        newPassword = passwordBox.get()
                        DbConn = pyDb.win_connect_mdb("Database\\UsrDet.accdb")
                        DbCursor = DbConn.cursor()

                        if newPassword != "" or "Password":
                            if " " not in newPassword:
                                if len(newPassword) != 0:
                                    newPassword = SHA512_Hash.fGetHash(newPassword)
                                    DbCursor.execute("UPDATE Credentials SET Hash = (?) WHERE StrComp([Usernames],(?),0) = 0;",[newPassword,userWhitelist]).commit()
                                    try:
                                        removeWidgets(boxEmpty)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(correctCode)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(noPass)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(wrongCode)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(spacesPass)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(badPass)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(updatedLabel)
                                    except:
                                        print()
                                    print("Updated password")
                                    updatedLabel = Label(windowResetPass,text="Updated Password",bg='black',fg='green',font=("Helvetica",10))
                                    updatedLabel.place(x=100,y=125)
                                    return
                                else:
                                    try:
                                        removeWidgets(boxEmpty)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(correctCode)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(noPass)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(wrongCode)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(spacesPass)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(badPass)
                                    except:
                                        print()
                                    try:
                                        removeWidgets(updatedLabel)
                                    except:
                                        print()
                                    noPass = Label(windowResetPass,text="Please enter a password",bg='black',fg='red',font=("Helvetica",10))
                                    noPass.place(x=100,y=125)
                                    print("Please enter a password")
                                    return
                            else:
                                try:
                                    removeWidgets(boxEmpty)
                                except:
                                    print()
                                try:
                                    removeWidgets(correctCode)
                                except:
                                    print()
                                try:
                                    removeWidgets(noPass)
                                except:
                                    print()
                                try:
                                    removeWidgets(wrongCode)
                                except:
                                    print()
                                try:
                                    removeWidgets(spacesPass)
                                except:
                                    print()
                                try:
                                    removeWidgets(badPass)
                                except:
                                    print()
                                try:
                                    removeWidgets(updatedLabel)
                                except:
                                    print()
                                spacesPass = Label(windowResetPass,text="Can NOT have spaces",bg='black',fg='red',font=("Helvetica",10))
                                spacesPass.place(x=100,y=125)
                                print("Password can NOT contain spaces")
                                return
                        else:
                            try:
                                removeWidgets(boxEmpty)
                            except:
                                print()
                            try:
                                removeWidgets(correctCode)
                            except:
                                print()
                            try:
                                removeWidgets(noPass)
                            except:
                                print()
                            try:
                                removeWidgets(wrongCode)
                            except:
                                print()
                            try:
                                removeWidgets(spacesPass)
                            except:
                                print()
                            try:
                                removeWidgets(badPass)
                            except:
                                print()
                            try:
                                removeWidgets(updatedLabel)
                            except:
                                print()
                            badPass = Label(windowResetPass,text="Not acceptable password",bg='black',fg='red',font=("Helvetica",10))
                            badPass.place(x=100,y=125)
                            print("Not an acceptable password")
                            return

                    def checkCode():
                        global windowResetPass
                        global wrongCode
                        global spacesPass
                        global badPass
                        global noPass
                        global correctCode
                        global boxEmpty
                        if len(securityBox.get()) != 0:
                            databaseCode = int(securityBox.get())
                        else:
                            try:
                                removeWidgets(boxEmpty)
                            except:
                                print()
                            try:
                                removeWidgets(correctCode)
                            except:
                                print()
                            try:
                                removeWidgets(noPass)
                            except:
                                print()
                            try:
                                removeWidgets(wrongCode)
                            except:
                                print()
                            try:
                                removeWidgets(spacesPass)
                            except:
                                print()
                            try:
                                removeWidgets(badPass)
                            except:
                                print()
                            try:
                                removeWidgets(updatedLabel)
                            except:
                                print()
                            print("Security Code Box Empty")
                            boxEmpty = Label(windowResetPass,text="Security Box is empty",bg='black',fg='red',font=("Helvetica",10))
                            boxEmpty.place(x=100,y=125)
                            return
                        
                        DbConn = pyDb.win_connect_mdb("Database\\UsrDet.accdb")
                        DbCursor = DbConn.cursor()      
                        DbCursor.execute("SELECT Usernames, Code, Hash FROM Credentials;")

                        while True:
                            code = DbCursor.fetchone()
                            if code != None:
                                if code[0] == userWhitelist:
                                    if code[1] == databaseCode:
                                        try:
                                            removeWidgets(boxEmpty)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(correctCode)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(noPass)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(wrongCode)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(spacesPass)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(badPass)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(updatedLabel)
                                        except:
                                            print()
                                        print("Correct security code")
                                        passwordBox.config(state=NORMAL)
                                        passwordButton.config(state=NORMAL)
                                        securityButton.config(state=DISABLED)
                                        correctCode = Label(windowResetPass,text="Correct Code",bg='black',fg='green',font=("Helvetica",10))
                                        correctCode.place(x=140,y=125)
                                    else:
                                        try:
                                            removeWidgets(boxEmpty)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(correctCode)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(noPass)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(wrongCode)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(spacesPass)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(badPass)
                                        except:
                                            print()
                                        try:
                                            removeWidgets(updatedLabel)
                                        except:
                                            print()
                                        wrongCode = Label(windowResetPass,text="Incorrect Security Code",bg='black',fg='red',font=("Helvetica",10))
                                        wrongCode.place(x=100,y=125)
                                        print("Incorrect Security Code")
                                else:
                                    continue
                            else:
                                break
                            
                    securityVar = StringVar()
                    securityBox = Entry(windowResetPass,textvariable=securityVar)
                    securityBox.place(x=150,y=20)

                    securityButton = Button(windowResetPass,text="Submit Code",bg='black',fg='white',bd=0,command=checkCode)
                    securityButton.place(x=75,y=100)

                    passwordBox = Entry(windowResetPass,state=DISABLED,disabledbackground='#a9a9a9')
                    passwordBox.place(x=150,y=60)
                    passwordButton = Button(windowResetPass,state=DISABLED,text="Submit Password",bg='black',fg='white',bd=0,command=changePassword)
                    passwordButton.place(x=175,y=100)

                    securityLabel = Label(windowResetPass,text="Security Code:",font=("Helvetica",10),bg='black',fg='white')
                    passwordLabel = Label(windowResetPass,text="New Password:",font=("Helvetica",10),bg='black',fg='white')
                    securityLabel.place(x=50,y=20)
                    passwordLabel.place(x=50,y=60)

                    def on_typing(*args):
                        validDigits = ["0","1","2","3","4","5","6","7","8","9","0"]
                        digits = securityVar.get()
                        currentDigit = ""

                        # Tells the function to only process one number at a time
                        if len(digits) == 0:
                            currentDigit = digits[0:0]
                        elif len(digits) == 1:
                            currentDigit = digits[0:1]
                        elif len(digits) == 2:
                            currentDigit = digits[1:2]
                        elif len(digits) == 3:
                            currentDigit = digits[2:3]
                        elif len(digits) == 4:
                            currentDigit = digits[3:4]
                        else:
                            securityVar.set(digits[:4])

                        # First number is always empty. Create an exception for it
                        if currentDigit == "":
                            return
                        if currentDigit not in validDigits:    
                            securityVar.set(digits[:len(digits)-1])
                    securityVar.trace_variable("w",on_typing)

                # Check if CHANGE PASS window is open
                def checkPassWindow():
                    global windowResetPass
                    print("Checking if CHANGE PASSWORD window is open...")
                    try:
                        isOpened = windowResetPass.winfo_exists()
                        if isOpened == 1:
                            print("Change Password already open")
                            return
                        else:
                            print("Returned 0 - Continuing...")
                            resetPassword()
                    except:
                        print("It's not, continuing...")
                        resetPassword()

                htmlSTATUS = None
                
                ##################### ADD TO THE TAB CANVAS BELOW HERE #####################

                updateResources = Button(master=otherCanvas,text="Update Essential Databases",font=("Helvetica",15),width=320,anchor=W,pady=20,command=fProgressBarWindow,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                updateResources.place(x=0,y=7)

                signOut = Button(master=otherCanvas,text="Sign Out",font=("Helvetica",15),width=320,anchor=W,pady=20,command=fSignOUT,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                signOut.place(x=0,y=87)

                tempRemove = Button(master=otherCanvas,text="Remove Temporary Files",font=("Helvetica",15),width=320,anchor=W,pady=20,command=lambda: removeTempFiles(htmlSTATUS),bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                tempRemove.place(x=0,y=167)

                adminUser = Button(master=otherCanvas,text="User Permissions",font=("Helvetica",15),width=320,anchor=W,pady=20,command=checkPermsWindow,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                adminUser.place(x=0,y=247)

                resetDatabase = Button(master=otherCanvas,text="Reset Database",font=("Helvetica",15),width=320,anchor=W,pady=20,command=removeDatabaseFunc,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                resetDatabase.place(x=0,y=327)

                recoverPassword = Button(master=otherCanvas,text="Change Password",font=("Helvetica",15),width=320,anchor=W,pady=20,command=checkPassWindow,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                recoverPassword.place(x=0,y=407)

                exitProgram = Button(master=otherCanvas,text="Exit Program",font=("Helvetica",15),width=320,anchor=W,pady=20,command=exitProgram,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                exitProgram.place(x=0,y=487)

                bottomBorder = Button(master=otherCanvas,text="",width=320,anchor=W,pady=20,bg='black',relief=FLAT,state=DISABLED,activebackground='#3d3d3d')
                bottomBorder.place(x=0,y=567)

                resetDatabase.config(state=DISABLED)
                adminUser.config(state=DISABLED)

                try:
                    # Enable the admin actions for certain users
                    DbConn = pyDb.win_connect_mdb("Database\\UsrDet.accdb")
                    DbCursor = DbConn.cursor()      
                    DbCursor.execute("SELECT Usernames, Admin FROM Credentials;")
                except:
                    print("Database doesn't exist error")
                    adminCheck = 0

                while True:
                    try:
                        adminCheckDB = DbCursor.fetchone()
                    except:
                        print("Database doesn't exist error")
                        removeDatabaseFunc()
                        break
                    if adminCheckDB != None:
                        if adminCheckDB[0] == userWhitelist:
                            adminCheck = adminCheckDB[1]
                    else:
                        break
                    
                if adminCheck == 1:
                    resetDatabase.config(state=NORMAL)
                    adminUser.config(state=NORMAL)
                else:
                    adminLabel = Label(master=otherCanvas,text="Admin Only",font=("Helvetica",10),fg='red',bg='#3d3d3d')
                    adminLabel.place(x=470,y=355)
                    adminLabel2 = Label(master=otherCanvas,text="Admin Only",font=("Helvetica",10),fg='red',bg='#3d3d3d')
                    adminLabel2.place(x=470,y=275)
            else:
                print("already created window: OTHER")
                print()


        ##########################
        #   Reset Tabs Function  #
        ##########################
        
        
        def fResetNAVSelection():
            
            # Resets the tab selection and closes any opened canvas

            global alreadyCreatedSystem
            global alreadyCreatedGames
            global alreadyCreatedAbout
            global alreadyCreatedOther

            global systemScrollbar
            global gamesScrollbar
            global aboutScrollbar
            global otherScrollbar

            global systemFrame
            global gamesFrame
            global aboutFrame
            global otherFrame 
            
            if alreadyCreatedSystem[0] == True:
                canvas='system'
                print("Resetting systemCanvas...")
                print("-Deleted Canvas-",canvas)
                print()
                resetCanvas(systemCanvas,alreadyCreatedSystem,systemScrollbar,systemFrame)

            if alreadyCreatedGames[0] == True:
                canvas='games'
                print("Resetting gamesCanvas...")
                print("-Deleted Canvas-",canvas)
                print()
                resetCanvas(gamesCanvas,alreadyCreatedGames,gamesScrollbar,gamesFrame)

            if alreadyCreatedAbout[0] == True:
                canvas='about'
                print("Resetting aboutCanvas...")
                print("-Deleted Canvas-",canvas)
                print()
                resetCanvas(aboutCanvas,alreadyCreatedAbout,aboutScrollbar,aboutFrame)
            
            if alreadyCreatedOther[0] == True:
                canvas='other'
                print("Resetting otherCanvas...")
                print("-Deleted Canvas-",canvas)
                print()
                resetCanvas(otherCanvas,alreadyCreatedOther,otherScrollbar,otherFrame)
            
            systemInfoNAV.config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=NAVimage)
            gamesListNAV.config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=NAVimage)
            aboutProgramNAV.config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=NAVimage)
            otherInfoNAV.config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=NAVimage)
            
        # Creating the buttons in the NAV bar
        systemInfoNAV = tk.Button(master=pw,compound=LEFT,command=fNAVSys,bg='#A9A9A9')
        gamesListNAV = tk.Button(master=pw,compound=LEFT,command=fNAVGames,bg='#A9A9A9')
        aboutProgramNAV = tk.Button(master=pw,compound=LEFT,command=fNAVAbout,bg='#A9A9A9')
        otherInfoNAV = tk.Button(master=pw,compound=LEFT,command=fNAVOther,bg='#A9A9A9')
        
        # Configure the buttons to show the image and adjust the design of it to be professional
        systemInfoNAV.config(image=NAVimage,relief=FLAT,text='SYSTEM\n INFORMATION',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')
        gamesListNAV.config(image=NAVimage,relief=FLAT,text='GAMES LIST',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')
        aboutProgramNAV.config(image=NAVimage,relief=FLAT,text='ABOUT',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')
        otherInfoNAV.config(image=NAVimage,relief=FLAT,text='OTHER',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')

        systemInfoNAV.image = NAVimage
        gamesListNAV.image = NAVimage
        aboutProgramNAV.image = NAVimage
        otherInfoNAV.image = NAVimage
        
        # Packing the buttons in a NAV bar
        systemInfoNAV.place(x=290,y=0,height=80,width=200)
        gamesListNAV.place(x=480,y=0,height=80,width=200)
        aboutProgramNAV.place(x=670,y=0,height=80,width=200)
        otherInfoNAV.place(x=860,y=0,height=80,width=200)

        # Select the first tab once the NAV bar is setup
        tabMasterWindow.select(tabSys1)
        fNAVSys()

        # Add the banner to the top left and right corners in order to extend the NAV bar for aesthetic reasons
        socialClubNAVL = Label(master=pw,image=NAVimage,compound=CENTER)
        socialClubNAVL.image = NAVimage
        socialClubNAVL.place(x=0,y=0,height=80,width=290)

        socialClubNAVR = Label(master=pw,image=NAVimage,compound=CENTER)
        socialClubNAVR.image = NAVimage
        socialClubNAVR.place(x=1060,y=0,height=80,width=140)
        
        # Create the Social Club logo and put it into the top left corner 
        socialClubLogo = PhotoImage(master=pw,file='Images\\social_clublogo.ppm')
        socialClubLogo.image = socialClubLogo

        # Make the label which will place the social club logo
        socialClubLabel = Label(master=pw,image=socialClubLogo,bd=0)
        socialClubLabel.place(x=20,y=15)

        
    ##########################
    #   Gif Update Function  #
    ##########################

        
    def fTopLevelLoading():
        
        global gifLabel
        global topLevel
        
        # Create new top level window
        fProgramWindow()
        print("Loading System Requirement Tool...")
        print()
        mw.withdraw()
        topLevel = Toplevel(mw,bg='black')
        topLevel.geometry("110x110")
        topLevel.overrideredirect(1)

        def center(toplevel):
            toplevel.withdraw()
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
            toplevel.deiconify()

        # Call the function that centers the window
        center(topLevel)
        topLevel.lift(mw)
        topLevel.lift(mw)
        topLevel.lift(mw)

        # Show the waiting cursor
        topLevel.focus_set()
        topLevel.config(cursor="wait")
            
        # Show the current frame of the gif
        gifLabel = Label(topLevel,highlightthickness=4,bg='#A9A9A9',relief=FLAT)
        gifLabel.pack()
        topLevel.after(0, fUpdateGif, 0)
        
    def fUpdateGif(index):

        global gifFrames
        global gifLabel
        global timesLooped
        global topLevel
        global pw
        
        # Check how many times the gif has looped
        if timesLooped == 2:
            mw.after(0, lambda:  removeWidgets(topLevel))
            mw.destroy()
            pw.deiconify()
            print("Loaded program")
            print()
            return
        
        # Show the next frame of the gif
        # Loop the gif once the 35th frame has been shown
        if index == 36:
            index = 0
            timesLooped += 1
            topLevel.attributes('-topmost', True)
        else:
            currentFrame = gifFrames[index]
            gifLabel.configure(image=currentFrame)
            index += 1
            topLevel.attributes('-topmost', True)
        mw.after(1, fUpdateGif, index)
    mw.mainloop()
__init__()
