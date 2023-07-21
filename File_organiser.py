#Project2- file Organiser
import os
import shutil
from tkinter import *
from threading import *
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog

# Modification can be performed here.
# You can add more extensions to this dictionary
Extensions = {
   'Documents': ('.pdf', '.doc', '.xls', 'txt', '.csv', '.zip', '.xml', '.zip', '.docx', '.DOCX', '.odt', '.docx'), 'Pictures' : ('.jpg', '.jpeg', '.png', '.JPG'),
   'Videos': ('.mp4', '.mkv', '.3gp', '.flv', '.mpeg'), 'Music': ('.mp3', '.wav', '.m4a', '.webm'),
   'Programs': ('.py', '.cpp', '.c', '.sh', '.js', '.php', '.html'),
    'Zip Folder' : ('.zip'),
   'Apps': ('.exe', '.apk'),
 }
class File_Organizer:
    def __init__(self,root):
        # Setting the Tkinter main windows
        self.window = root
        self.window.geometry("720x500")
        self.window.title('File Organizer')
        self.window.resizable(width=False, height=False)
        self.window.configure(bg='purple')

        # self.Selected_Dir = ''
        # self.Browsed = False
        # # Frame 1: For the Logo
        # self.frame_1 = Frame(self.window, bg='gray90', width=280, height=70)
        # self.frame_1.pack()
        # self.frame_1.place(x=20, y=20)

        # Calling the function to display the logo
        self.Display_Logo()

        # Exit Button
        Exit_Btn = Button(self.window, text="Exit", font=("Kokila", 10, 'bold'), bg="dodger blue", fg="white", width=5, command=self.Exit_Window)
        Exit_Btn.place(x=600, y=60)

        # Frame 2: For the Main Page Widgets
        self.frame_2 = Frame(self.window, bg="white", width=720, height=480)
        self.frame_2.place(x=0, y=110)

        # Calling the function to display main page
        # widgets
        self.Main_Page()

    # This function displays the File Organizer Logo
    def Display_Logo(self):
         Label(text="File Organiser", font="Ariel 20 bold").pack()
    # This function displays all the widgets in the 'self.frame_2'
    # related to File Organizing Operation
    def Main_Page(self):
        # Heading Label
        Heading_Label = Label(self.frame_2, text="Please Select the Folder", font=("Kokila", 20, 'bold'), bg='white')
        Heading_Label.place(x=160, y=20)

        # Button for selecting the directory(where
        # the desired files are presented)
        Folder_Button = Button(self.frame_2, text="Select Folder", font=("Kokila", 10, 'bold'), bg="blue", width=10, command=self.Select_Directory)
        Folder_Button.place(x=130, y=80)

        # The directory path selected from the Tkinter file dialog 
        # that opens by the 'Folder_Button' is displayed here.
        self.Folder_Entry = Entry(self.frame_2, font=("Helvetica", 12), width=32)
        self.Folder_Entry.place(x=256, y=85)
        Status = Label(self.frame_2, text="Status: ", font=("Kokila", 12, 'bold'), bg='white')
        Status.place(x=180, y=130)

        # Status Label:
        self.Status_Label = Label(self.frame_2, text="Not Started Yet", font=("Kokila", 12), bg="white", fg="dark green")
        self.Status_Label.place(x=256, y=130)

        Start_Button = Button(self.frame_2, text="Start", font=("Kokila", 13, 'bold'), bg="pink", fg="black", width=8, command=self.Organizer)
        Start_Button.place(x=280, y=180)

    # let users select the directory where the files are presented
    def Select_Directory(self):
        self.Selected_Dir = filedialog.askdirectory(title = "Select a location")
        # Insert the folder path to the Entry Box
        self.Folder_Entry.insert(0, self.Selected_Dir)

        # Converting the type of 'self.Selected_Dir' variable
        # to String for avoiding any error while checking
        # the path is exists or not
        self.Selected_Dir = str(self.Selected_Dir)

        # Checks if the folder path is exists or not
        if os.path.exists(self.Selected_Dir):
            self.Browsed = True

    # Creating a different thread to run the 'self.Organizer' function
    def Threading(self):
        # Killing a thread through "daemon=True" isn't a good idea
        self.x = Thread(target=self.Organizer, daemon=True)
        self.x.start()
    
    # The Organizer function 
    def Organizer(self):
        # If no directory is chosen
        if not self.Browsed:
            messagebox.showwarning('No folders are choosen', \
            'Please Select a Folder First')
            return
        try:
            # Showing the current status of the operation
            self.Status_Label.config(text='Processing...')

            self.Current_Path = self.Selected_Dir
 
            if os.path.exists(self.Current_Path):
                self.Folder_List1 = []
                self.Folder_List2 = []
                self.Flag = False
 
                for folder, extensions in Extensions.items():
                    self.folder_name = folder
                    self.folder_path = os.path.join(self.Current_Path, self.folder_name)

                    os.chdir(self.Current_Path)
 
                    # If the folder is already present in that directory
                    if os.path.exists(self.folder_name):
                        self.Folder_List1.append(self.folder_name)
                    else:
                        self.Folder_List2.append(self.folder_name)
                        os.mkdir(self.folder_path)

                    for item in self.File_Finder(self.Current_Path, extensions):
                        self.Old_File_Path = os.path.join(self.Current_Path,item)
                        self.New_File_Path = os.path.join(self.folder_path,item)

                        shutil.move(self.Old_File_Path, self.New_File_Path)

                        self.Flag = True
            else:
                messagebox.showerror('Error!', 'Please Enter a Valid Path!')

            if self.Flag:
                self.Status_Label.config(text='Complete!')
                messagebox.showinfo('Done!', 'Complete!')
                self.Clear()
            if not self.Flag:
                self.Status_Label.config(text='Complete!')
                messagebox.showinfo('Done!', 'Folders have been created\nNo Files were there to move')
                self.Clear()
        # If any error occurs
        except Exception as es:
            messagebox.showerror("Error!", f"Error due to {str(es)}")

    def File_Finder(self, folder_path, file_extensions):
        self.files = []
        for file in os.listdir(folder_path):
            for extension in file_extensions:
                if file.endswith(extension):
                    self.files.append(file)
        return self.files

    def Clear(self):
        self.Status_Label.config(text='Not Started Yet')
        self.Folder_Entry.delete(0, END)
        self.Selected_Dir = ''
    # This function closes the main window
    def Exit_Window(self):
        self.window.destroy()

# The main function
if __name__ == "__main__":
    root = Tk()
    # Creating a 'File_Renamer' class object
    obj = File_Organizer(root)
    root.mainloop()