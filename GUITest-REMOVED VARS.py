
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

# Import  for  information # 
import PLUGIN_wmi

##########################
#    Initialisation      #
##########################

def __init__():

    global 
    global 
    global 
    global 
    global 
    global 
    global 
    global 
    global 

    global 
    global 

    global 
    global 
    global 
    global 
    
    ### Database configuration ###
    
    print("Configuring database...")
     = PLUGIN_pypyodbc
     = "Database\\.accdb"
    if os..exists():
        print("Already Created database\n")
    else:
        try:
            .win_create_mdb("Database\\.accdb")
            print("Created Database")
            print("Configuring Tables...")
             = .win_connect_mdb("Database\\.accdb")
             = .cursor()
            .execute('CREATE TABLE Credentials (ID INTEGER PRIMARY KEY, Usernames CHAR(32), Hash CHAR(64),  INTEGER, Admin INTEGER);').commit()
            print("Created Table\n")
        except:
            raise
    
    # Initialize variables
     = ""
     = ""
     = ""
     = ["",""]
    [0] = ""
    [1] = ""
    
    # Create the Master Window ()
     = tk.Tk()
    .geometry('440x250')
    .iconbitmap('Images\\favicon.ico')
    .title("Social Club Login")
    .resizable(0,0)
     = 0

    # Center the login window
    def centerWindow():
        .update_idletasks()
         = .winfo_screenwidth()
         = .winfo_screenheight()
         = tuple(int(_) for _ in .geometry().split('+')[0].split(''))
         = /2 - [0]/2
         = /2 - [1]/2
        .geometry("%dx%d+%d+%d" % ( + (, )))

    # Call the function that centers the window
    centerWindow()

    # Configure the general aesthetics of the login window 
    .configure(bg='black')

    # Import the social club logo
     = PhotoImage(master=,file='Images\\social_clublogo.ppm')
    .image = 
     = Label(master=,image=,bd=0)
    .place(=155,=20)

    # Create the  entry and check to see when the user has clicked on the entry box
     = StringVar()
     = Entry(master=, bd=0,textvariable=, width=30,fg='#A9A9A9',font=('Helvetica',10))
    .place(=120,=90)
    .insert(0,"")

    # Define the function to see if the  box has been clicked on and - if it equals "" - clear it. If the  box is empty, fill it with ""
    def isUsernameFocused():
        if .get() == "":
            .delete(0,END)
            .config(fg='black')

        if .get() == "":
            .insert(0,"")
            .config(fg='#A9A9A9',show="")

    # Create the  entry and check to see when the user has clicked on the entry box
     = StringVar()
     = Entry(master=, bd=0, width=30,fg='#A9A9A9',font=('Helvetica',10),textvariable=)
    .place(=120,=110)
    .insert(0,"")

    # Define the function to see if the  box has been clicked on and - if it equals "" - clear it. If the  box is empty, fill it with ""
    def isPassFocused():
        if .get() == "":
            .delete(0,END)
            .config(fg='black',show="*")
                    
        if .get() == "":
            .insert(0,"")
            .config(fg='#A9A9A9')

    # Bind the primary mouse button and ENTER to the entry boxes to call a function when they're clicked on
    .bind("<Button-1>",lambda : isUsernameFocused())
    .bind("<Button-1>",lambda : isPassFocused())
    .bind("<Return>",lambda : fCheckPass())

    # Change the  to asterisks if the user uses TAB to highlight the entry widget
    def on_typingPass(*args):
        .config(fg='black',show="*")
    .trace_variable("",on_typingPass)
    
    def on_typingUser(*args):
        .config(fg='black')
    .trace_variable("",on_typingUser)


##########################
#    Widget Remover      #
##########################

        
    def removeWidgets(widget):

        widget.destroy()


##########################
#   Verification #
##########################


     = 0
    def fCheckPass():

        global 
        global 
        global 
        global 
        
        # Create the function that throws the errors if the entered info is incorrect
        def fIncorrectPassword():

            global 
            global 
            global 

            if  == 5:
                
                def resetLogin():
                    
                    global 
                    
                    .config(state=NORMAL)
                     = 0
                    removeWidgets()
                    removeWidgets()
                    print("Lock out ended\n")

                print("\nMaximum attempts reached.")
                .config(state=DISABLED)
                 = Label(master=,text="Maximum attempts reached! Please wait 10 seconds...",font=('Helvetica',8),fg='red',bg='black')
                .place(=100,=205)
                .after(10000,resetLogin)
            else:
                 += 1
                if  > 1:
                    print("Incorrect ")
                else:
                    print("Incorrect ")
                     = Label(master=,text="Incorrect  or ",font=('Helvetica',8),fg='red',bg='black')
                    .place(=140,=185)

        # Check to see if the  box is empty to prevent errors being raised
         = .get()
        if  == "" or  == "":
            print(" box is empty")
            return

        # HASH the  the user entered and compare it
         = SHA512_Hash.fGetHash()
        
        # Check if the  is correct
         = .win_connect_mdb("Database\\.accdb")
         = .cursor()
        
         = .get()
        if  == "" or  == "":
            print(" box empty")
            return
            
        .execute("SELECT Usernames, Hash FROM Credentials WHERE Usernames = ?;",[,])
        
        while True:
             = .fetchone()
            if  != None:
                 = [0].replace(" ","")
                if  == :
                    if :
                         = [1]
                         = .replace(" ","")
                         = [0]
                        break
                    else:
                        print("Incorrect ")
                         = None
                        break
                else:
                    continue
            else:
                print("Error!")
                 = None
                break
        print("Successfully converted entered  to hash")

        if  < 5:
            if  == :
                 = Label(master=,text="Correct Credentials - Logging in...",font=('Helvetica',8),fg='#A9A9A9',bg='black')
                .place(=140,=185)
                print("Correct ")
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

    # Create the login button for the user to press after they've entered their 
     = tk.Button(master=,bd=0,text="SIGN IN",font=('Helvetica',10), bg='black',fg='white',activebackground='black',activeforeground='white', relief=FLAT, command=fCheckPass)
    .place(=140,=150)


##########################
#  Database Registration #
##########################


    def databaseRegister(,,security):

        # Connect to db
         = .win_connect_mdb("Database\\.accdb")
         = .cursor()

        # Convert the  given to hash
         = SHA512_Hash.fGetHash()

        # Get the next available ID
        .execute("SELECT ID FROM Credentials;")
         = 0
        
        while True:
             = .fetchone()
            if :
                 = [0]
            else:
                 =  + 1
                print("Next available ID:",)
                break
        
        # Check if the  is already in use
        .execute("SELECT Usernames FROM Credentials;")
         = []
        
        while True:
             = .fetchone()
            if :
                 = [0]
                 = .replace(" ","")
                .append()
            else:
                break

        if  in :
            print(" already taken!")
             = Label(master=,text=" already taken!",font=('Helvetica',8),fg='red',bg='black')
            .place(=205,=350)

        else:
            .execute('INSERT INTO Credentials (ID, Usernames, Hash, , Admin) values (?,?,?,?,0);',[,,,security]).commit()
            .close()
        
            removeWidgets()
            fCheckPass()

             = Label(master=,text="Account creation successful!",font=('Helvetica',8),fg='green',bg='black')
            .place(=145,=210)


##########################
#    Sign Up Window      #
##########################


    ## Register the details the user entered ##
    def fRegistration():

        global 
        global 
        global 

        # Create an error label for each error

         = Label(master=,text="You must create a !",font=('Helvetica',8),fg='red',bg='black')
         = Label(master=,text="You must create a !",font=('Helvetica',8),fg='red',bg='black')
         = Label(master=,text="Your security  must be 4 !",font=('Helvetica',8),fg='red',bg='black')
        
        # Make sure the entry boxes are not empty

         = .get()
         = .get()
         = .get()

        if  == "" or  == "":
            print("Please enter a stronger !")
            .delete(0,END)
            return
        if  == "":
            print("")
            .place(=190,=350)
            return
        elif  == "":
            print("errorUserPass")
            .place(=190,=350)
            return
        elif len() <4:
            print("")
            .place(=190,=350)
            return
        else:
            databaseRegister(,,)

    # Create the window and widgets on it
    def fSignUp():

        global 
        global 
        global 
        global 
        global 

         = (master=,height=500,width=550,bg='black')
        .resizable(0,0)
        .iconbitmap('Images\\favicon.ico')
        .title("Social Club Account Creation")
        
         = PhotoImage(file='Images\social_clublogo.ppm')
        .image = 
        
         = Label(master=,image=,bd=0)
        .place(=215,=20)

        # Create the CREATE ACCOUNT title
         = Label(master=,text="CREATE ACCOUNT:",font=('Helvetica',11,'underline','bold'),fg='white',bg='black')
        .place(=130,=105)
        
        # Create the entry boxes
         = Entry(master=,width=30)
         = Entry(master=,width=30,show="*")
         = StringVar()
         = Entry(master=,width=10,textvariable=)

        .place(=215,=165)
        .place(=215,=195)
        .place(=215,=238)

         = Label(master=,text=":",font=('Helvetica',9),fg='white',bg='black')
         = Label(master=,text=":",font=('Helvetica',9),fg='white',bg='black')
         = Label(master=,text="SECURITY\n :*",font=('Helvetica',9),fg='white',bg='black')

        .place(=132,=165)
        .place(=130,=195)
        .place(=135,=225)

         = Button(master=,bd=0,image=,text="JOIN NOW",font=('Helvetica',9,'bold'),bg='black',activebackground='black',relief=FLAT,compound=CENTER,command=fRegistration)
        .place(=230,=300)

         = Label(master=,text='''*Your 4-Digit security  will be used if you forget your  and need to recover your account.
    It should remain a secret and should be something you'll easily remember that is secure at the same time.
    Try avoid using commonly used combinations of numbers such as '1234' or '1111', etc...''',font=('Helvetica',7),fg='#A9A9A9',bg='black')
        .place(=45,=400)

        .bind("<Return>",lambda : fRegistration())
        .bind("<Return>",lambda : fRegistration())
        .bind("<Return>",lambda : fRegistration())
        
        # Check the length of the security information entered
        # Check to see if the security  contains numbers
        def on_typing(*args):
             = ["0","1","2","3","4","5","6","7","8","9","0"]
             = .get()
             = ""

            # Tells the function to only process one number at a time
            if len() == 0:
                 = [0:0]
            elif len() == 1:
                 = [0:1]
            elif len() == 2:
                 = [1:2]
            elif len() == 3:
                 = [2:3]
            elif len() == 4:
                 = [3:4]
            else:
                .set([:4])

            # First number is always empty. Create an exception for it
            if  == "":
                return
            if  not in :    
                .set([:len()-1])
        .trace_variable("",on_typing)

    # Check if CREATE ACCOUNT window is open
    def fCreateAccountChecks():

        global 
        
        print("Checking...")
        try:
             = .winfo_exists()
            if  == 1:
                print("Create account already open")
                return
            else:
                print("Returned 0 - Continuing...")
                fSignUp()
        except:
            print("Continuing...")
            fSignUp()

    # Create the 'JOIN SOCIAL CLUB' button
     = PhotoImage(master=,file='Images\\.ppm')
    .image = 

     = Button(master=,bd=0,image=,text="JOIN NOW",font=('Helvetica',9,'bold'),bg='black',activebackground='black',relief=FLAT,compound=CENTER,command=fCreateAccountChecks)
    .place(=220,=140)

    # Import the loading gif
     = [PhotoImage(file='Images\Loading_icon.gif',format = 'gif - %i' %(i)) for i in range(0,36)]


##########################
#   Sign Out Function    #
##########################


    def fSignOUT():

        global 
        global 
        
         = "Database\\f_status"
        os..join(, '*')
         = open(,"r+")
         = .read()
        .close()

        if  == "1":
            print("Can't sign out now")
            return
        else:
            print("Signing out...")
            removeWidgets()
            try:
                removeWidgets()
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
     = [False]
     = [False]
     = [False]
     = [False]

    # Setup an external file to be imported into different scripts and functions. Prevents 'cyclical dependency' 
     = "Database\\f_status"
    os..join(, '*')

     = open(,"")
    .write('0')
    .close()

    # Create the main program window which will give the user the ability to interact with the program
    def fProgramWindow():

        global 
        global 
        global 
        global 
        global 
        global 
        global 
        global 
        global 
        global 
        
        # Make the Program Window ()
         = tk.Tk()
        .geometry('1200x700')
        ("Rockstar Games - Requirements")
        .iconbitmap('Images\\favicon.ico')
        .attributes('-topmost', True)
        .attributes('-topmost', False)
        .resizable(0,0)
        .withdraw()

        # Center the login window
        def centerWindow():
            .update_idletasks()
             = .winfo_screenwidth()
             = .winfo_screenheight()
             = tuple(int(_) for _ in .geometry().split('+')[0].split(''))
             = /2 - [0]/2
             = /2 - [1]/2
            .geometry("%dx%d+%d+%d" % ( + (, )))
        centerWindow()
        
        # Create the tabs in the window/notebook
         = ttk.Notebook()
        
         = ttk.Frame(,width=0)
         = ttk.Frame(,width=0)
         = ttk.Frame(,width=0)
         = ttk.Frame(,width=0)

        .add(,state='hidden',text='System Information')
        .add(,state='hidden',text='Games List')
        .add(,state='hidden',text='About')
        .add(,state='hidden',text='Other')

        # Create the  for the background picture
         = (master=,width=1200,height=700,highlightthickness=0)
        .pack(expand=YES, fill=BOTH)

        # Place the background on the 
         = PhotoImage(master=, file='Images\\rockstar-background.ppm')
        .create_image(0,0,image=,anchor=NW)

        # Draws the tab bar
        .pack(fill='both', expand='yes')

        # Apply labels/information to notebook tabs
         = Label(, text="System Information")
         = Label(, text="Games List")
         = Label(, text="About")
         = Label(, text="Other")

        .pack
        .pack()
        .pack()
        .pack()
        .pack()

        # Create a semi-transparent overlay when loading  tests

        def overlayFunction():

            global 
            
             = tk.Tk()
            overlayLabel = Label(,text="Loading...",bg='black',font=('Helvetica',30),fg='#A9A9A9')
            .geometry('+250+250')
            .overrideredirect(True)
            .lift()
            .attributes('-alpha', 0.5)
            overlayLabel.pack()

            # Center the overlay window
            def centerWindow():
                .update_idletasks()
                 = .winfo_screenwidth()
                 = .winfo_screenheight()
                 = tuple(int(_) for _ in .geometry().split('+')[0].split(''))
                 = /2 - [0]/2
                 = 10
                .geometry("%dx%d+%d+%d" % ( + (,)))

            # Python needs to call the function twice so that it is actually centered?
            # Need to call return before mainloop to stop Python from hanging/freezing
            # Mainloop needs to be used so that the window is transparent
                
            centerWindow()
            centerWindow()
            return
            .mainloop()


        ##########################
        #    Retrieve    #
        ##########################

        
        # Create the function which gets the user's information
        def retrieveHardware(,,,,,,,):

             = PLUGIN_wmi

            # Retrieve computer information,  information and processor information
             = .()
             = .Win32_ComputerSystem()[0]
             = .Win32_Processor()[0]
             = .Win32_LogicalDisk()[0]

            # Convert the free space to GB
             = int(.)
             = (/1073741824)
             = math.ceil()

            #  is always Integrated Graphics (e.g Intel HD Graphics)
            # 2 is always Dedicated Graphics (e.g NVIDIA GTX 1080)
            # Try get the dedicated  - if an error is raised, use the integrated  
             = .Win32_VideoController()[0]
            2 = .Win32_VideoController()[1]
            
            if "Driver" in .Name or "Graphics" in .Name:
                Final = 2
            if "Driver" in 2.Name or "Graphics" in 2.Name:
                Final = 
            else:
                Final = 2

            # Use OS information to get  as a float - round it up to the nearest one
             = .Win32_OperatingSystem()[0]
             = float(.TotalVisibleMemorySize) / 1048576  # KB to GB
             = math.ceil()

            # Print the information gathered from the user's system replacing unecessary words
             = .Name.replace(" ","")
             = .replace("(TM)","")
             = .replace("(R)","")
            
             = Final.Name.replace("(TM)","")
             = .replace("NVIDIA ","")
             = .replace("AMD ","")
             = .replace("(R)","")

            print()
            print(":",)
            print(":",)
            print(":",str()+"GB")
            print(":",str()+"GB")
            print()

            # Open the database of  and get the rank of the user's 
             = open("Resources\passmarkTableCPU.txt","r+")
             = .read()
            
             = .replace("[","")
             = .replace("]","")
             = .replace("'","")
             = .replace(", ",",")
             = .split(",")
            
             = .()
             = [+1]

            # Repeat for graphics card
             = open("Resources\passmarkTableGPU.txt","r+")
             = .read()
            
             = .replace("[","")
             = .replace("]","")
             = .replace("'","")
             = .replace(", ",",")
             = .split(",")
            
             = .()
             = [+1]

            # Return the real names and ranks of each piece of 
             = 
             = 
             = 
             = 

             = .Name
             = Final.Name
             = 
             = 

            return ,,,,,,,
        
        
        ##########################
        #    Create NAV Bar      #
        ##########################
        

        # Import the image to be used when a tab has been selected
         = PhotoImage(master=,file='Images\\NAV-BarSelected.ppm')

        # Import the image to be used in the NAV Bar
         = PhotoImage(master=,file='Images\\NAV-Bar.PPM')

        # Apply my information to the bottom left of the program
         = Label(master=,image=,width=600,height=30,bd=0,anchor=SW)
         = Label(master=,image=,width=600,height=30,bd=0,anchor=SW)
         = Label(master=,text="© SCOTT CRAWLEY\n POST 16 CS",fg='#A9A9A9',bg='black',bd=0,font=('Helvetica',6,'bold'))
        
        .place(=0,=674)
        .place(=600,=674)
        .place(=10,=676)

        # Add the currently signed in user to the bottom right
         = 
         = .upper()
         = .replace(" ","")
         = Label(master=,text="Logged in as:",font=('Helvetica',7,'bold'),fg='#A9A9A9',bg='black')

        # Create a context menu (right-click menu)
        def popupMenu():
            .post(.x_root, .y_root)
        
         = Menubutton(master=,text=,font=('Helvetica',7,'bold','underline'),bg='black',fg='white',relief=FLAT,bd=0,activebackground='#e5e5e5')
         = Menu(,tearoff=0,bg='black',fg='#A9A9A9',activeforeground='white',activebackground='black',relief=SUNKEN)
        .add_command(label="SIGN OUT",font=('Helvetica',9,'bold'),command=fSignOUT)

        # Bind both left-click and right-click to the menu
        # Make sure the context menu only appears when clicking the button
        .bind("<Button-3>", popupMenu)
        .bind("<Button-1>", popupMenu)
        
        .place(=1100,=679)
        .place(=1035,=679)


        ##########################
        #      TAB CREATION      #
        ##########################
        
        
        def resetCanvas(,boolVar,scrollbar,frame):

            # Resets the  on given tab
            removeWidgets()
            removeWidgets(scrollbar)
            removeWidgets(frame)
            boolVar[0] = False
            return boolVar
        
        def fNAVSys():

            ### SYSTEM INFORMATION TAB ###
            
            global 
            global 
            global 
            global 
            global 
            
            fResetNAVSelection()
            ("R* Requirement Tool - System Information")
            .config(fg='white',image=)
            .select()

            if [0] == False:
                print(">Created ")
                [0] = True

                 = Frame(master=,width=600,height=620)
                .pack(side=BOTTOM)
                 = Scrollbar(master=)
                 = (master=,width=600,height=620,bg='white')
                 = Frame(master=,width=620,height=820,bg='white')

                .pack(side=BOTTOM)
                .create_window((0,0),window=,anchor=NW)

                print("System",str())
                print()
                
                ##################### ADD TO THE TAB  BELOW HERE #####################
                
                 = PhotoImage(master=,file='Images\\rectangleBackground.ppm')
                .image = 

                # Processor Information
                 = Label(master=,text="PROCESSOR ():",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=,pady=10)
                .place(=0,=0)

                 = Label(master=,text="YOUR :",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=39)
                 = Label(master=,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=96)
                
                #  Information
                 = Label(master=,text="MEMORY ():",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=,pady=10)
                .place(=0,=145)

                 = Label(master=,text="YOUR :",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=184)
                 = Label(master=,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=241)
                
                # Graphics Card Information
                 = Label(master=,text="GRAPHICS CARD ():",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=,pady=10)
                .place(=0,=290)

                 = Label(master=,text="YOUR :",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=329)
                 = Label(master=,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=386)

                # Hard Drive Space Available
                 = Label(master=,text="HARD DRIVE ():",font=('Helvetica',9,'bold'),fg='#888',bg='#e5e5e5',width=320,anchor=,pady=10)
                .place(=0,=435)

                 = Label(master=,text="YOUR :",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=474)
                 = Label(master=,text="REQUIRED:",font=('Helvetica',7,'bold'),fg='#A9A9A9')
                .place(=0,=531)

            else:
                print("already created window: SYS")
                print()
                return

        def _gameInit_(,,,,,,,,,,,,,,,):

            global 
            global 

             = PhotoImage(master=,file="Images\\cross.ppm")
            .image = 
             = PhotoImage(master=,file="Images\\tick.ppm")
            .image = 

            if  < :
                 = Label(,image=,bd=0)
                .place(=500,=70)
            else:
                 = Label(,image=,bd=0)
                .place(=500,=70)

            if  < :
                 = Label(,image=,bd=0)
                .place(=500,=360)
            else:
                 = Label(,image=,bd=0)
                .place(=500,=360)

            if  > :
                 = Label(,image=,bd=0)
                .place(=500,=210)
            else:
                 = Label(,image=,bd=0)
                .place(=500,=210)

            if  > :
                 = Label(,image=,bd=0)
                .place(=500,=505)
            else:
                 = Label(,image=,bd=0)
                .place(=500,=505)

            .place(=0,=110)
            .place(=0,=400)
            .place(=0,=258)
            .place(=0,=548)

             = Label(master=,text=,font=('Helvetica',10))
             = Label(master=,text=,font=('Helvetica',10))
             = Label(master=,text=str()+"GB ",font=('Helvetica',10))
             = Label(master=,text=str()+"GB Free Space",font=('Helvetica',10))

            .place(=0,=53)
            .place(=0,=343)
            .place(=0,=198)
            .place(=0,=488)

            removeWidgets()


        ##########################
        #   Game Requirements    #
        ##########################


        def fViceCity():

            global 

            print("Vice City chosen")
            print("Getting  information...")
            overlayFunction()

            # Assign the user's  information to some labels
    
             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Pentium III @ 800 MHz (1 ) or AMD Athlon @ 800 MHz (1 )",font=('Helvetica',10))
             = Label(master=,text="32MB NVIDIA GeForce2 MX",font=('Helvetica',10))
             = Label(master=,text="128 MB ",font=('Helvetica',10))
             = Label(master=,text="1GB Free Space",font=('Helvetica',10))

             = 2474
             = 1566
             = 0.128
             = 1

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)
            
        def fMidnightClub():

            global 

            print("Midnight Club chosen")
            print("Getting  information...")
            overlayFunction()
            
             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()
            
             = Label(master=,text="Intel Pentium III @ 800 MHz (1 ) or AMD Athlon @ 800 MHz (1 )",font=('Helvetica',10))
             = Label(master=,text="32MB NVIDIA GeForce2 MX",font=('Helvetica',10))
             = Label(master=,text="128 MB ",font=('Helvetica',10))
             = Label(master=,text="1.5GB Free Space",font=('Helvetica',10))

             = 2474
             = 1566
             = 0.128
             = 1.5

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fMaxPayne2():

            global 

            print("Max Payne 2 chosen")
            print("Getting  information...")
            overlayFunction()
            
             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Celeron @ 1.2 GHz (1 ) or 1.2 GHz AMD Duron (1 )",font=('Helvetica',10))
             = Label(master=,text="64MB NVIDIA GeForce2 MX",font=('Helvetica',10))
             = Label(master=,text="256 MB ",font=('Helvetica',10))
             = Label(master=,text="1.5GB Free Space",font=('Helvetica',10))

             = 2612
             = 1566
             = 0.256
             = 1.5

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fSanAndreas():

            global 
            
            print("San Andreas chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()
            
             = Label(master=,text="Intel Pentium III @ 1.0 GHz (1 ) or AMD Athlon @ 800 MHz (1 )",font=('Helvetica',10))
             = Label(master=,text="64MB NVIDIA GeForce3",font=('Helvetica',10))
             = Label(master=,text="256 MB ",font=('Helvetica',10))
             = Label(master=,text="3.6GB Free Space",font=('Helvetica',10))

             = 2474
             = 1566
             = 0.256
             = 3.6

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)
            
        def fLibertyCityStories():

            global 
            
            print("Grand Theft Auto: Liberty City Stories chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Pentium III @ 1.0 GHz (1 ) or AMD Athlon @ 800 MHz (1 )",font=('Helvetica',10))
             = Label(master=,text="64MB NVIDIA GeForce3",font=('Helvetica',10))
             = Label(master=,text="256 MB ",font=('Helvetica',10))
             = Label(master=,text="2GB Free Space",font=('Helvetica',10))

             = 2612
             = 1566
             = 0.256
             = 2

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)
            
        def fBully():

            global 

            print("Bully chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Pentium 4 @ 3.0 GHz (1 ) or AMD Athlon 3000 (1 )",font=('Helvetica',10))
             = Label(master=,text="256MB NVIDIA GeForce 7300",font=('Helvetica',10))
             = Label(master=,text="1 GB ",font=('Helvetica',10))
             = Label(master=,text="4.7GB Free Space",font=('Helvetica',10))

             = 2572
             = 1276
             = 1
             = 4.7

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fManhunt():

            global 

            print("Manhunt 2 chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Pentium 4 @ 1.7 GHz (1 ) or AMD Athlon 3000 (1 )",font=('Helvetica',10))
             = Label(master=,text="128MB NVIDIA 6200GT",font=('Helvetica',10))
             = Label(master=,text="512 MB ",font=('Helvetica',10))
             = Label(master=,text="4GB Free Space",font=('Helvetica',10))

             = 2572
             = 1336
             = 0.512
             = 4

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fGTA4():

            global 

            print("Grand Theft Auto IV chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Core 2 Duo @ 1.8 GHz (2 CPUs) or AMD Athlon X2 64 2.4GHz (2 CPUs)",font=('Helvetica',10))
             = Label(master=,text="256MB NVIDIA 7900",font=('Helvetica',10))
             = Label(master=,text="1 GB ",font=('Helvetica',10))
             = Label(master=,text="16GB Free Space",font=('Helvetica',10))

             = 2333
             = 990
             = 1
             = 16

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fGTA4v2():

            global 

            print("Grand Theft Auto: EFLC chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Core 2 Duo @ 1.8 GHz (2 CPUs) or AMD Athlon X2 64 2.4GHz (2 CPUs)",font=('Helvetica',10))
             = Label(master=,text="256MB NVIDIA 7900",font=('Helvetica',10))
             = Label(master=,text="1 GB ",font=('Helvetica',10))
             = Label(master=,text="16GB Free Space",font=('Helvetica',10))

             = 2333
             = 990
             = 1
             = 16

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fNoire():

            global 
            
            print("L.A. Noire chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Core 2 Duo @ 2.2 GHz (2 CPUs) or AMD Dual Core 2.4 GHz (2 CPUs)",font=('Helvetica',10))
             = Label(master=,text="512MB NVIDIA 8600",font=('Helvetica',10))
             = Label(master=,text="2 GB ",font=('Helvetica',10))
             = Label(master=,text="16GB Free Space",font=('Helvetica',10))

             = 1995
             = 963
             = 2
             = 16

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fMaxPayne3():

            global 

            print("Max Payne 3 chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Dual Core @ 2.4 GHz (2 CPUs) AMD Dual Core 2.4 GHz (2 CPUs)",font=('Helvetica',10))
             = Label(master=,text="512MB NVIDIA 8600 GT",font=('Helvetica',10))
             = Label(master=,text="2 GB ",font=('Helvetica',10))
             = Label(master=,text="35GB Free Space",font=('Helvetica',10))

             = 1755
             = 999
             = 2
             = 35

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fGTA5():

            global 

            print("Grand Theft Auto V chosen")
            print("Getting  information...")
            overlayFunction()

             = " "
             = " "
             = " "
             = " "
             = 0
             = 0
             = 0
             = 0

             = retrieveHardware(,,,,,,,)
             = list()

             = [0]
             = [1]
             = [2]
             = [3]

            fNAVSys()

             = Label(master=,text="Intel Core 2 Quad Q6600 @ 2.4 GHz or AMD Phenom 9850 Quad-Core @ 2.5GHz",font=('Helvetica',10))
             = Label(master=,text="1GB NVIDIA 9800 GT",font=('Helvetica',10))
             = Label(master=,text="4 GB ",font=('Helvetica',10))
             = Label(master=,text="72GB Free Space",font=('Helvetica',10))

             = 1100
             = 628
             = 4
             = 72

             = int([4])
             = int([5])
             = int([6])
             = int([7])

            _gameInit_(,,,,,,,,,,,,,,,)

        def fNAVGames():

            ### GAMES SELECTION TAB ### 

            global 
            global 
            global 
            global 
            global 
            global 
            
            fResetNAVSelection()
            ("R* Requirement Tool - Games List")
            .config(fg='white',image=)
            .select()

            if [0] == False:
                print(">Created ")
                [0] = True

                # Create the Frame and  for the scrollbar
                 = Frame(master=,width=600,height=620)
                .pack(side=BOTTOM)
                 = Scrollbar(master=)
                 = (master=,width=600,height=620,yscrollcommand=.set,highlightthickness=0,bg='white')
                .config(scrollregion=[0,0,600,1050])
                 = Frame(master=,width=600,height=1000,bg='white')
                .config(command=.yview,width=10)
                .pack(side=RIGHT,fill=)
                
                .pack(side=BOTTOM)
                .create_window((0,0),window=,anchor=NW)

                # Creating the function which allows us to use the mousewheel to control the scrollbar
                 = 0

                def mouseWheel():
                    global 
                    if [0] == True:
                        def delta():
                            if .num == 5 or .delta < 0:
                                #print(.delta)
                                return 1
                            return -1
                         += delta()
                        .yview_scroll(delta(),UNITS)

                .bind("<MouseWheel>",mouseWheel)
                print("Games",str())
                print()

                ##################### ADD TO THE TAB  BELOW HERE #####################

                # Add the button for Grand Theft Auto: Vice City (2002)
                 = PhotoImage(master=,file="Images\\VC_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fViceCity)
                .place(=30,=20)

                # Add the button for Midnight Club II (2003)
                 = PhotoImage(master=,file="Images\\Midnight_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fMidnightClub)
                .place(=230,=20)

                # Add the button for Max Payne 2 (2003)
                 = PhotoImage(master=,file="Images\\Max2_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fMaxPayne2)
                .place(=430,=20)

                # Add the button for Grand Theft Auto: San Andreas (2004)
                 = PhotoImage(master=,file="Images\\SA_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fSanAndreas)
                .place(=30,=270)

                # Add the button for Grand Theft Auto: Liberty City Stories (2005)
                 = PhotoImage(master=,file="Images\\LCS_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fLibertyCityStories)
                .place(=230,=270)

                # Add the button for Bully (2006)
                 = PhotoImage(master=,file="Images\\Bully_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fBully)
                .place(=430,=270)

                # Add the button for Manhunt 2 (2007)
                 = PhotoImage(master=,file="Images\\Manhunt_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fManhunt)
                .place(=30,=520)

                # Add the button for Grand Theft Auto IV (2008)
                 = PhotoImage(master=,file="Images\\GTA4_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fGTA4)
                .place(=230,=520)

                # Add the button for Grand Theft Auto: EFLC (2009)
                 = PhotoImage(master=,file="Images\\GTAEFLC_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fGTA4v2)
                .place(=430,=520)

                # Add the button for L.A. Noire (2011)
                 = PhotoImage(master=,file="Images\\L.A_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fNoire)
                .place(=30,=770)

                # Add the button for Max Payne 3 (2012)
                 = PhotoImage(master=,file="Images\\Max3_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fMaxPayne3)
                .place(=230,=770)

                # Add the button for Grand Theft Auto V (2013)
                 = PhotoImage(master=,file="Images\\GTAV_Cover.ppm")
                .image = 

                 = Button(master=,image=,width=150,height=200,relief=GROOVE,command=fGTA5)
                .place(=430,=770)
                
            else:
                print("already created window: GAMES")
                print()
                return

        def fNAVAbout():

            ### ABOUT TAB ###

            global 
            global 
            global 
            global 
            
            fResetNAVSelection()
            ("R* Requirement Tool - About Page")
            .config(fg='white',image=)
            .select()

            if [0] == False:
                print(">Created ")
                [0] = True

                 = Frame(master=,width=600,height=620)
                .pack(side=BOTTOM)
                 = Scrollbar(master=)
                .pack(side=RIGHT,fill=)
                 = (master=,bg='white',width=600,height=620,yscrollcommand = .set)
                .pack(side=BOTTOM)
                .config(command=.yview,width=5)

                print("About",str())
                print()

                ##################### ADD TO THE TAB  BELOW HERE #####################

                ### Guide ###
                 = Label(master=,text="Guide/Tutorial",font=("Helvetica",15),width=320,anchor=,pady=20,bg='#3d3d3d',fg='#a9a9a9')
                .place(=0,=7)

                 = Label(master=,text='''On the [SYSTEM INFORMATION] tab there are four categories containing information that determines
whether or not your system will be able to run your chosen game. Both your  and
FREE SPACE need to be greater than the required amounts but, as for your PROCESSOR and
GRAPHICS CARD, the program will calculate everything for you using Online resources.''',font=("Helvetica",10),anchor=,justify=LEFT,width=320)

                 = Label(master=,text='''----------------------------------------------------------------------------------------------------------------------------------------------------------------------
1 - Begin by going to the [GAMES LIST] tab and choosing a game.\n
2 - Wait for the program to finish gathering your system information.\n
3 - Once completed, you will be taken to the [SYSTEM INFORMATION] tab automatically.\n
4 - From here you will see either a TICK or CROSS next to each category\n
5 - A full set of ticks indicate you can run the game. Any less and it's very unlikely you'll be able to.''',font=("Helvetica",9),anchor=,justify=LEFT,width=320)
                .place(=0,=74)
                .place(=0,=141)

                ### Info ###
                 = Label(master=,text="Information",font=("Helvetica",15),width=320,anchor=,pady=20,bg='#3d3d3d',fg='#a9a9a9')
                .place(=0,=300)

                 = Label(master=,text=''' rankings taken from:
's - https://www.cpubenchmark.net/CPU_mega_page.html
's - https://www.videocardbenchmark.net/GPU_mega_page.html
\nData Storage:
Microsoft Access 2010
\nExternal Python Plugins:
- Pypyodbc: Database connection tool
-  and pyWin32:  information
- HTML Fetcher: Written by me
-  Hasher: Written by me
\nImages/Assets created by me. Rockstar logo's and game covers taken from Google.''',font=("Helvetica",10),anchor=,justify=LEFT,width=320)
                .place(=0,=367)
            else:
                print("already created window: ABOUT")
                print()
                return

        def fNAVOther():

            ### OTHER TAB ###

            global 
            global 
            global 
            global 
            global 
            global 
            
            fResetNAVSelection()
            ("R* Requirement Tool - Other")
            .config(fg='white',image=)
            .select()

            if [0] == False:
                print(">Created ")
                [0] = True

                 = Frame(master=,width=600,height=620)
                .pack(side=BOTTOM)
                 = Scrollbar(master=)
                .pack(side=RIGHT,fill=)
                 = (master=,bg='white',width=600,height=620,yscrollcommand=.set)
                .pack(side=BOTTOM)
                .config(command=.yview,width=5)

                print("Other",str())
                print()

                def fProgressBarWindow():

                    global 
                    global 
                    global 
                        
                     = "Database\\f_status"
                    os..join(, '*')
                     = open(,"r+")
                     = .read()
                    .close()
                    
                    if  == "0":
                         = "Database\\f_status"
                        os..join(, '*')
                         = open(,"")
                        .write("1")
                        .close()
                        fetch_HTML.fFetchHTML()
                    elif  == "1":
                        print("Already running")
                    else:
                        print("Error in file f_status")
                        print()
                    .update()

                def managePerms():

                    global 
                    
                     = tk.Tk()
                    .geometry("350x150")
                    .config(bg='black')
                    .title("User Permissions")
                    .iconbitmap('Images\\favicon.ico')
                    .attributes('-topmost', True)
                    .attributes('-topmost', False)
                    .resizable(0,0)

                     = .win_connect_mdb("Database\\.accdb")
                     = .cursor()      
                    .execute("SELECT Usernames FROM Credentials;")

                     = []
                    while True:
                         = .fetchone()
                        if  != None:
                            if :
                                 = [0]
                                 = .replace("(","")
                                 = .replace("[","")
                                 = .replace("'","")
                                 = .replace(")","")
                                 = .replace("]","")
                                .append()
                                continue
                            else:
                                break
                        else:
                            break
                    
                     = tk.StringVar()
                     = ttk.Combobox(,textvariable=,width=25,height=50)
                    .bind('<<ComboboxSelected>>')
                    ['values'] = ()
                    .set('--Select User--')
                    .place(=110,=20)
                    .withdraw()
                    .deiconify()

                    def fmakeAdmin():
                         = .get()
                        .execute("SELECT Usernames, Admin FROM Credentials;")

                        while True:
                             = .fetchone()
                            if  != None:
                                if [0] == :
                                     = [1]
                            else:
                                break
                        if  != "--Select User--":
                            try:
                                if  == 1:
                                    print("User already Admin")
                                elif  == None:
                                    print("Not a correct ")
                                else:
                                    # Have to use StrComp to prevent updating same usernames with differemt capitalisation 
                                    print("Added user to admin")
                                    .execute("UPDATE Credentials SET Admin = 1 WHERE StrComp([Usernames],(?),0) = 0;",[]).commit()
                            except:
                                print("Not a correct !")
                        else:
                            print("That is not a user!")

                    def fremoveAdmin():
                         = .get()
                        .execute("SELECT Usernames, Admin FROM Credentials;")

                        while True:
                             = .fetchone()
                            if  != None:
                                if [0] == :
                                     = [1]
                            else:
                                break
                        if  != "--Select User--":
                            try:
                                if  == 0:
                                    print("User not an Admin")
                                elif  == None:
                                    print("Not a correct ")
                                else:
                                    # Have to use StrComp to prevent updating same usernames with differemt capitalisation 
                                    print("Removed user from Admin")
                                    .execute("UPDATE Credentials SET Admin = 0 WHERE StrComp([Usernames],(?),0) = 0;",[]).commit()
                            except:
                                print("Not a correct ")
                        else:
                            print("That is not a user!")

                     = Label(,text="USER:",font=("Helvetica",10),bg='black',fg='white')
                    .place(=60,=20)
                     = Button(,text="Make Admin",font=("Helvetica",10),bg='black',fg='white',relief=FLAT,bd=0,command=fmakeAdmin)
                    .place(=80,=80)
                     = Button(,text="Remove Admin",font=("Helvetica",10),bg='black',fg='white',relief=FLAT,bd=0,command=fremoveAdmin)
                    .place(=180,=80)

                def checkPermsWindow():
                    global 
                    print("Checking...")
                    try:
                         = .winfo_exists()
                        if  == 1:
                            print("Perms Manager already open")
                            return
                        else:
                            print("Returned 0 - Continuing...")
                            managePerms()
                    except:
                        print("Continuing...")
                        managePerms()

                def removeTempFiles():
                    try:
                        shutil.rmtree("__pycache__")
                        os.remove("Resources\\passmarkCPU.html")
                        os.remove("Resources\\passmarkGPU.html")
                        print("Temporary files removed")
                    except:
                        print("Temporary files removed")

                def removeDatabaseFunc():
                    global 
                    try:
                        .config(state=DISABLED)
                        os.remove("Database\\.accdb")
                        print("Reset database")
                    except:
                        print("Files do not exist")

                def ():
                    global 
                    try:
                        .destroy()
                    except:
                        print()
                    .destroy()

                def resetPassword():

                    global 
                    global 
                    global 
                    
                     = tk.Tk()
                    .config(bg='black')
                    .geometry("350x150")
                    .title("Reset ")
                    .iconbitmap('Images\\favicon.ico')
                    .attributes('-topmost', True)
                    .attributes('-topmost', False)
                    .resizable(0,0)

                    def changePassword():
                         = .get()
                         = .win_connect_mdb("Database\\.accdb")
                         = .cursor()   

                        if  != "" or "":
                             = SHA512_Hash.fGetHash()
                            .execute("UPDATE Credentials SET Hash = (?) WHERE StrComp([Usernames],(?),0) = 0;",[,]).commit()
                            
                            print("Updated ")
                             = Label(,text="Updated ",bg='black',fg='green',font=("Helvetica",10))
                            .place(=100,=125)
                            return
                        else:
                            print("Not an acceptable ")
                            return

                    def checkCode():
                         = int(.get())
                         = .win_connect_mdb("Database\\.accdb")
                         = .cursor()      
                        .execute("SELECT Usernames, , Hash FROM Credentials;")

                        while True:
                             = .fetchone()
                            if  != None:
                                if [0] == :
                                    if [1] == :
                                        print("Correct security ")
                                        .config(state=NORMAL)
                                        .config(state=NORMAL)
                                        .config(state=DISABLED)
                                else:
                                    continue
                            else:
                                break
                            
                     = StringVar()
                     = Entry(,textvariable=)
                    .place(=150,=20)

                     = Button(,text="Submit ",bg='black',fg='white',bd=0,command=checkCode)
                    .place(=75,=100)

                     = Entry(,state=DISABLED,disabledbackground='#a9a9a9')
                    .place(=150,=60)
                     = Button(,state=DISABLED,text="Submit ",bg='black',fg='white',bd=0,command=changePassword)
                    .place(=175,=100)

                     = Label(,text="Security :",font=("Helvetica",10),bg='black',fg='white')
                     = Label(,text="New :",font=("Helvetica",10),bg='black',fg='white')
                    .place(=50,=20)
                    .place(=50,=60)

                    def on_typing(*args):
                         = ["0","1","2","3","4","5","6","7","8","9","0"]
                         = .get()
                         = ""

                        # Tells the function to only process one number at a time
                        if len() == 0:
                             = [0:0]
                        elif len() == 1:
                             = [0:1]
                        elif len() == 2:
                             = [1:2]
                        elif len() == 3:
                             = [2:3]
                        elif len() == 4:
                             = [3:4]
                        else:
                            .set([:4])

                        # First number is always empty. Create an exception for it
                        if  == "":
                            return

                        if  not in :    
                            .set([:len()-1])
                            #print("Entered string",)
                    .trace_variable("",on_typing)

                # Check if CHANGE PASS window is open
                def checkPassWindow():
                    global 
                    print("Checking...")
                    try:
                         = .winfo_exists()
                        if  == 1:
                            print("Change  already open")
                            return
                        else:
                            print("Returned 0 - Continuing...")
                            resetPassword()
                    except:
                        print("Continuing...")
                        resetPassword()
                
                ##################### ADD TO THE TAB  BELOW HERE #####################

                 = Button(master=,text="Update Essential Databases",font=("Helvetica",15),width=320,anchor=,pady=20,command=fProgressBarWindow,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                .place(=0,=7)

                 = Button(master=,text="Sign Out",font=("Helvetica",15),width=320,anchor=,pady=20,command=fSignOUT,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                .place(=0,=87)

                 = Button(master=,text="Remove Temporary Files",font=("Helvetica",15),width=320,anchor=,pady=20,command=removeTempFiles,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                .place(=0,=167)

                 = Button(master=,text="User Permissions",font=("Helvetica",15),width=320,anchor=,pady=20,command=checkPermsWindow,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                .place(=0,=247)

                 = Button(master=,text="Reset Database",font=("Helvetica",15),width=320,anchor=,pady=20,command=removeDatabaseFunc,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                .place(=0,=327)

                 = Button(master=,text="Change ",font=("Helvetica",15),width=320,anchor=,pady=20,command=checkPassWindow,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                .place(=0,=407)

                 = Button(master=,text="Exit Program",font=("Helvetica",15),width=320,anchor=,pady=20,command=,bg='#3d3d3d',fg='#a9a9a9',relief=FLAT,activebackground='#3d3d3d',activeforeground='white')
                .place(=0,=487)

                 = Button(master=,text="",width=320,anchor=,pady=20,bg='black',relief=FLAT,state=DISABLED,activebackground='#3d3d3d')
                .place(=0,=567)

                .config(state=DISABLED)
                .config(state=DISABLED)

                # Enable the admin actions for certain users

                 = .win_connect_mdb("Database\\.accdb")
                 = .cursor()      
                .execute("SELECT Usernames, Admin FROM Credentials;")

                while True:
                     = .fetchone()
                    if  != None:
                        if [0] == :
                             = [1]
                    else:
                        break
                    
                if  == 1:
                    .config(state=NORMAL)
                    .config(state=NORMAL)
                else:
                     = Label(master=,text="Admin Only",font=("Helvetica",10),fg='red',bg='#3d3d3d')
                    .place(=470,=355)
                     = Label(master=,text="Admin Only",font=("Helvetica",10),fg='red',bg='#3d3d3d')
                    .place(=470,=275)
            else:
                print("already created window: OTHER")
                print()


        ##########################
        #   Reset Tabs Function  #
        ##########################
        
        
        def fResetNAVSelection():
            
            # Resets the tab selection and closes any opened 

            global 
            global 
            global 
            global 

            global 
            global 
            global 
            global 

            global 
            global 
            global 
            global  
            
            if [0] == True:
                ='system'
                print("Resetting ...")
                print("-Deleted -",)
                print()
                resetCanvas(,,,)

            if [0] == True:
                ='games'
                print("Resetting ...")
                print("-Deleted -",)
                print()
                resetCanvas(,,,)

            if [0] == True:
                ='about'
                print("Resetting ...")
                print("-Deleted -",)
                print()
                resetCanvas(,,,)
            
            if [0] == True:
                ='other'
                print("Resetting ...")
                print("-Deleted -",)
                print()
                resetCanvas(,,,)
            
            .config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=)
            .config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=)
            .config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=)
            .config(fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),image=)
            
        # Creating the buttons in the NAV bar
         = tk.Button(master=,compound=LEFT,command=fNAVSys,bg='#A9A9A9')
         = tk.Button(master=,compound=LEFT,command=fNAVGames,bg='#A9A9A9')
         = tk.Button(master=,compound=LEFT,command=fNAVAbout,bg='#A9A9A9')
         = tk.Button(master=,compound=LEFT,command=fNAVOther,bg='#A9A9A9')
        
        # Configure the buttons to show the image and adjust the design of it to be professional
        .config(image=,relief=FLAT,text='SYSTEM\n INFORMATION',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')
        .config(image=,relief=FLAT,text='GAMES LIST',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')
        .config(image=,relief=FLAT,text='ABOUT',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')
        .config(image=,relief=FLAT,text='OTHER',fg='#A9A9A9',font=('Helvetica Neue',12,'bold'),compound=tk.CENTER,bd=0,activeforeground='white',activebackground='black')

        .image = 
        .image = 
        .image = 
        .image = 
        
        # Packing the buttons in a NAV bar
        .place(=290,=0,height=80,width=200)
        .place(=480,=0,height=80,width=200)
        .place(=670,=0,height=80,width=200)
        .place(=860,=0,height=80,width=200)

        # Select the first tab once the NAV bar is setup
        .select()
        fNAVSys()

        # Add the banner to the top left and right corners in order to extend the NAV bar for aesthetic reasons
         = Label(master=,image=,compound=CENTER)
        .image = 
        .place(=0,=0,height=80,width=290)

         = Label(master=,image=,compound=CENTER)
        .image = 
        .place(=1060,=0,height=80,width=140)
        
        # Create the Social Club logo and put it into the top left corner 
         = PhotoImage(master=,file='Images\\social_clublogo.ppm')
        .image = 

        # Make the label which will place the social club logo
         = Label(master=,image=,bd=0)
        .place(=20,=15)

        
    ##########################
    #   Gif Update Function  #
    ##########################

        
    def fTopLevelLoading():
        
        global 
        global 
        
        # Create new top level window
        fProgramWindow()
        print("Loading System Requirement Tool...")
        print()
        .withdraw()
         = (,bg='black')
        .geometry("110x110")
        .overrideredirect(1)

        def center():
            .withdraw()
            .update_idletasks()
             = .winfo_screenwidth()
             = .winfo_screenheight()
             = tuple(int(_) for _ in .geometry().split('+')[0].split(''))
             = /2 - [0]/2
             = /2 - [1]/2
            .geometry("%dx%d+%d+%d" % ( + (, )))
            .deiconify()

        # Call the function that centers the window
        center()
        .lift()
        .lift()
        .lift()

        # Show the waiting cursor
        .focus_set()
        .config(cursor="wait")
            
        # Show the current frame of the gif
         = Label(,highlightthickness=4,bg='#A9A9A9',relief=FLAT)
        .pack()
        .after(0, fUpdateGif, 0)
        
    def fUpdateGif():

        global 
        global 
        global 
        global 
        global 
        
        # Check how many times the gif has looped
        if  == 2:
            .after(0, lambda:  removeWidgets())
            .destroy()
            .deiconify()
            print("Loaded program")
            print()
            return
        
        # Show the next frame of the gif
        # Loop the gif once the 35th frame has been shown
        if  == 36:
             = 0
             += 1
            .attributes('-topmost', True)
        else:
             = []
            .configure(image=)
             += 1
            .attributes('-topmost', True)
        .after(1, fUpdateGif, )
    .mainloop()
__init__()
