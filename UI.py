from re import L
import cv2
from pip import main
import face_rec as fc
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import DISABLED, NORMAL, NO
from PIL import Image, ImageTk
from csv import writer, reader

class webcam:
    def __init__(self, directory) -> None:
        self.path = directory
        self.frame = None
        self.cap = False
        self.name = ""

        self.win = tk.Tk()
        self.win.resizable(False, False)
        self.x, self.y = self.win.winfo_screenwidth() // 2 , self.win.winfo_screenmmheight() // 2

        self.main()

    def main(self):
        for widget in self.win.winfo_children():
            widget.destroy()
        
        if self.cap:
            if self.cap.isOpened():
                self.cap.release()
                self.cap = False

        self.win.title("Attendance App")
        self.win.geometry("300x200+{}+{}".format(self.x - 150, self.y))

        self.mark = ttk.Button(self.win, text= "Mark Attendance", width= 30, command= self.make_Mark_Attendance_UI)
        self.mark.place(x= 150, y= 50, anchor= "center")

        self.add_student = ttk.Button(self.win, text= "Add Student", width= 30, command= self.make_Add_Student_UI)
        self.add_student.place(x= 150, y= 100, anchor= "center")

        self.show = ttk.Button(self.win, text= "Show Attendance", width= 30, command= self.show_attendance)
        self.show.place(x= 150, y= 150, anchor= "center")

        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.win.mainloop()
    
    def make_Mark_Attendance_UI(self):
        for widget in self.win.winfo_children():
            widget.destroy()

        self.win.title("Mark Your Attendance")
        self.win.geometry("720x580+{}+{}".format(self.x - 360, self.y))

        border = tk.LabelFrame(self.win, bg= "black")
        border.place(x= 360, y= 280, anchor= "center")
        
        self.frame_label = tk.Label(border, bg= "black")
        self.frame_label.pack()

        self.mark = ttk.Button(self.win, text= "Mark Attendance", command= self.mark_attendance)
        self.mark.place(x= 360, y= 540, anchor= "center")

        back = ttk.Button(self.win, text= "Back", command= self.main)
        back.place(x= 0, y= 0)

        self.start(0)
    
    def mark_attendance(self):
        def back():
            popup.destroy()
            self.main()

        if self.name == "Unknown":
            popup = tk.Toplevel(self.win)
            popup.geometry("350x100+{}+{}".format(self.x - 175, self.y))
            tk.Label(popup, text= "Person in the picture is not identified!!").place(x= 175, y= 20, anchor= "center")
            tk.Label(popup, text= "If this is a student, add to database using Add Student!!").place(x= 175, y= 40, anchor= "center")
            ttk.Button(popup, text= "Ok", command= back).place(x= 175, y= 80, anchor= "center")
            return
        
        if self.name == None:
            popup = tk.Toplevel(self.win)
            popup.geometry("350x100+{}+{}".format(self.x - 175, self.y))
            tk.Label(popup, text= "No person found!!").place(x= 175, y= 20, anchor= "center")
            tk.Label(popup, text= "Please sit in front of the camera").place(x= 175, y= 40, anchor= "center")
            ttk.Button(popup, text= "Ok", command= popup.destroy).place(x= 175, y= 80, anchor= "center")
            return

        now = datetime.now()
        temp = [self.name, now.strftime("%Y/%m/%d"), now.strftime("%H:%M"), 1]

        with open(self.path + "/data.csv", "a", newline= "") as f:
            write = writer(f)
            write.writerow(temp)

        popup = tk.Toplevel(self.win)
        popup.geometry("300x80+{}+{}".format(self.x - 150, self.y))
        tk.Label(popup, text= "Marked {}'s Attendance Succesfully".format(self.name)).place(x= 150, y= 20, anchor= "center")
        ttk.Button(popup, text= "Ok", command= back).place(x= 150, y= 60, anchor= "center")
    
    def show_attendance(self):
        for widget in self.win.winfo_children():
            widget.destroy()

        self.win.title("Attendance Logs")
        self.win.geometry("400x300+{}+{}".format(self.x - 200, self.y))

        columns = ("Name", "Date", "Time", "Status")
        tree = ttk.Treeview(self.win, columns= columns)
        tree.place(x= 200, y= 150, anchor= "center")

        tree.column('#0', width=0, stretch= NO)
        tree.column("Name", width= 100, anchor= "center")
        tree.column("Date", width= 100, anchor= "center")
        tree.column("Time", width= 100, anchor= "center")
        tree.column("Status", width= 50, anchor= "center")

        tree.heading('#0', text= "", anchor= "center")
        tree.heading("Name", text= "Name")
        tree.heading("Date", text= "Date")
        tree.heading("Time", text= "Time")
        tree.heading("Status", text= "Status")

        csv_file = open(self.path + "/data.csv")
        
        for row in reader(csv_file):
            tree.insert('', tk.END, values= row)
        
        csv_file.close()

        scrollbar = ttk.Scrollbar(self.win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll= scrollbar.set)
        scrollbar.grid(row= 0, column= 1, sticky= 'ns')

        back = ttk.Button(self.win, text= "Back", command= self.main)
        back.place(x= 0, y= 0)
    
    def make_Add_Student_UI(self):
        for widget in self.win.winfo_children():
            widget.destroy()
        
        self.win.title("Add New Student to the Database")
        self.win.geometry("720x640+{}+{}".format(self.x - 360, self.y))

        self.name = tk.StringVar()

        border = tk.LabelFrame(self.win, bg= "black")
        border.place(x= 360, y= 280, anchor= "center")

        self.frame_label = tk.Label(border, bg= "black")
        self.frame_label.pack()

        self.l1 = tk.Label(self.win, text= "Enter Name of the person in the image", font= ("bold", 10))
        self.l1.place(x= 360, y= 540, anchor= "center")

        self.enter_name = tk.Entry(self.win, textvariable= self.name, font= ("bold", 10))
        self.enter_name.place(x= 360, y= 570, anchor= "center")

        self.capture_B = ttk.Button(self.win, text= "Capture", command= self.save)
        self.capture_B.place(x= 360, y= 600, anchor= "center")
        self.capture_B["state"] = DISABLED

        back = ttk.Button(self.win, text= "Back", command= self.main)
        back.place(x= 0, y= 0)

        self.start(1)

    def save(self):
        self.warn = tk.Label(self.win, text= "", fg= "red")
        self.warn.place(x= 500, y= 560, anchor= "center")
        if self.name.get() == "":
            self.warn["text"] = "Enter name!!"
            return
        
        if self.warn in self.win.winfo_children():
            self.warn.destroy()
            self.win.update()
        
        mod = fc.Face(self.path + "/students/")
        img, name = mod.classify_face(self.frame.copy())
        if name != "Unknown":
            def add(popup):
                cv2.imwrite(self.path + "/students/" + self.name.get() + ".jpg", self.frame)
                popup.destroy()

                popup = tk.Toplevel(self.win)
                popup.geometry("200x100+{}+{}".format(self.x - 100, self.y))
                tk.Label(popup, text= "Added Seccesfully").place(x= 100, y= 30, anchor= "center")
                ttk.Button(popup, text= "Ok", command= popup.destroy).place(x= 100, y= 70, anchor= "center")
                
            popup = tk.Toplevel(self.win)
            popup.title("Student Exixts")
            popup.geometry("300x100+{}+{}".format(self.x - 150, self.y))

            tk.Label(popup, text= "This Student Already in The Database as " + name).place(x= 150, y= 30, anchor= "center")
            ttk.Button(popup, text= "Ok", command= popup.destroy).place(x= 100, y= 70, anchor= "center")
            ttk.Button(popup, text= "Add Student", command= lambda: add(popup)).place(x= 200, y= 70, anchor= "center")
        else:
            cv2.imwrite(self.path + "/students/" + self.name.get() + ".jpg", self.frame)
            
            popup = tk.Toplevel(self.win)
            popup.geometry("200x100+{}+{}".format(self.x - 100, self.y))
            tk.Label(popup, text= "Added {} to Database Succesfully".format(self.name.get())).place(x= 100, y= 30, anchor= "center")
            ttk.Button(popup, text= "Ok", command= popup.destroy).place(x= 100, y= 70, anchor= "center")

    def start(self, task = 0):        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while self.cap.isOpened():
            self.frame = self.cap.read()[1]
            img = self.frame.copy()

            if task == 1:
                self.capture_B["state"] = NORMAL
                locations = fc.face_recognition.face_locations(img)
                for (top, right, bottom, left) in locations:
                    cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(img))
                self.frame_label["image"] = img
            else:
                mod = fc.Face(self.path + "/students/")
                img, self.name = mod.classify_face(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(img))
                self.frame_label["image"] = img
            
            self.win.update()

    def on_closing(self):
        # Release the webcam
        if self.cap:
            if self.cap.isOpened():
                self.cap.release()
                self.cap = False
            
        # Close tkiner window
        self.win.destroy()


if __name__ == "__main__":
    path = os.getcwd() + "/main"
    cam = webcam(path)