class Log_Detection:
    def __init__(self):
        import tkinter as tk
        from tkinter import messagebox as messagebox
        from tkinter import filedialog as filedialog
        import os as OS
        import cv2 as cv
        import numpy as np
        import time as time
        self.tk = tk
        self.messagebox = messagebox
        self.filedialog = filedialog
        self.OS = OS
        self.cv = cv
        self.np = np
        self.time = time

    def No_wood_found(self, window):
        # background image
        bg_img = self.tk.PhotoImage(file="Backgrounds/unsatisfactin_bg.png")
        bg_img_label = self.tk.Label(master=window, image=bg_img)
        bg_img_label.image = bg_img
        bg_img_label.place(x=0, y=0, relwidth=1, relheight=1)

        text_label = self.tk.Label(master=window, font=("times", 40), text="No wood Found", bg="black", fg="Yellow")
        text_label.place(x=200, y=60)
        Home_button = self.tk.Button(master=window, text="Home", width=10, font=("times", 20), fg="black", bg="Yellow",
                                activebackground="cyan", command=lambda: self.repeat_window(window))
        Quit_button = self.tk.Button(master=window, text="Exit", width=10, font=("times", 20), fg="black", bg="red",
                                activebackground="magenta", command=quit)
        Home_button.place(x=100, y=350)
        Quit_button.place(x=500, y=350)

    def Wood_Found_Window(self, window, tot_vol):
        # background image
        bg_img = self.tk.PhotoImage(file="Backgrounds/active_bg.png")
        bg_img_label = self.tk.Label(master=window, image=bg_img)
        bg_img_label.image = bg_img
        bg_img_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Main image to display

        Home_button = self.tk.Button(master=window, text="Home", width=10, font=("times", 20), fg="black", bg="yellow",
                                activebackground="cyan", command=lambda:self.repeat_window(window))
        Quit_button = self.tk.Button(master=window, text="Exit", width=10, font=("times", 20), fg="black", bg="red",
                                activebackground="magenta", command=quit)

        text_label = self.tk.Label(master=window, font=("times", 20),
                              text=str(tot_vol) + "cc Volume of Wood has been Found\n"
                                                  " Check the output image and text file\n"
                                                  "named output.png image abd Logs.txt", justify="left", bg="black",
                              fg="yellow", height = 3)
        text_label.place(x=110, y=100)
        Home_button.place(x=150, y=350)
        Quit_button.place(x=450, y=350)

    def Generate_Text_File(self, Identified_objs, length, cnt, flag=0):
        """

        :return:All text in the file containing info about volumes and total volume as a tuple
        """
        Areas = {}
        Volumes = {}
        FILE = open("Logs.txt", mode='w')
        FILE.seek(0)
        if not flag:
            i = 1
            for ele in Identified_objs:
                Areas[i] = 3.14 * ele[2] ** 2
                i += 1
            i = 1
            for ele in Identified_objs:
                Volumes[i] = 3.14 * (ele[2] ** 2) * length
                i += 1

            # writing to file and screen text
            FILE.write("Found " + str(cnt) + " Logs" + '\n')
            FILE.write("AREAS\n")
            for key, value in Areas.items():
                if key < 10:
                    FILE.write("Wood-0" + str(key) + "  Area" + "  " + str(value) + '\n')
                else:
                    FILE.write("Wood-" + str(key) + "  Area" + "  " + str(value) + '\n')
            FILE.write("VOLUMES\n")
            for key, value in Volumes.items():
                if key < 10:
                    FILE.write("Wood-0" + str(key) + "  Volume" + " " + str(value) + '\n')
                else:
                    FILE.write("Wood-" + str(key) + "  Volume" + "  " + str(value) + '\n')
            FILE.write("Total Volume Accurate :" + str(sum(Volumes.values())) + "\n")
            FILE.write("Total Volume Approx :" + str(round(sum(Volumes.values()))))
            FILE.close()
            return round(sum(Volumes.values()))
        else:
            # FILE.write("")
            FILE.close()
            return round(sum(Volumes.values()))

    def Image_processing_Method2(self, window, path, length):
        #print("Hey I am Medium pass processing the Image")
        img = self.cv.imread(path, self.cv.IMREAD_UNCHANGED)
        img_original = img.copy()

        hsv = self.cv.cvtColor(img_original, self.cv.COLOR_BGR2HSV)

        lower_color = self.np.array([0, 0, 100])
        upper_color = self.np.array([30, 200, 255])
        mask = self.cv.inRange(hsv, lower_color, upper_color, self.cv.COLOR_BGR2HSV)
        brown_objects = self.cv.bitwise_and(img, img, mask=mask)

        brown_gray = self.cv.cvtColor(brown_objects, self.cv.COLOR_BGR2GRAY)
        img_blur = self.cv.GaussianBlur(brown_gray, (21, 21), self.cv.BORDER_DEFAULT)

        #for showing the real processing in the background 
        """
        self.cv.imshow("hello", hsv)
        self.cv.imshow("brown_gray", brown_gray)
        self.cv.imshow("blur", brown_objects)
        self.cv.imshow("mask", mask)
        """

        circles = self.cv.HoughCircles(img_blur, self.cv.HOUGH_GRADIENT, 0.9, 120, param1=50, param2=39, minRadius=1,
                                       maxRadius=180)

        if circles is not None:
            circles_to_round = self.np.uint16(self.np.around(circles))
            objects = circles_to_round.tolist()[0]
            wood = []
            for obj in objects:
                center = (obj[0], obj[1])
                wood.append(obj)
                #drawing circle and the center
                self.cv.circle(img_original, (obj[0], obj[1]), 2, (0, 255, 255), 3)
                self.cv.circle(img_original, (obj[0], obj[1]), obj[2], (0, 255, 255), 3)
            count = circles_to_round.shape[1]
            if len(wood) == 0:
                self.No_wood_found(window)
            else:
                self.cv.imwrite("output.png", img_original)
                vol = self.Generate_Text_File(wood, length, count)
                self.Wood_Found_Window(window, vol)
        else:
            self.Generate_Text_File(None, length, 0, 1)
            self.No_wood_found(window)


    def Image_processing_Method1(self, window, path, length):
        #print("Hey I am Low pass processing the Image")
        img = self.cv.imread(path, self.cv.IMREAD_UNCHANGED)
        height = img.shape[0]
        width = img.shape[1]
        img_original = img.copy()
        img_gray = self.cv.cvtColor(img, self.cv.COLOR_BGR2GRAY)
        img_blur = self.cv.GaussianBlur(img_gray, (21, 21), self.cv.BORDER_DEFAULT)
        #self.cv.imshow("wer", img_blur)

        circles = self.cv.HoughCircles(img_blur, self.cv.HOUGH_GRADIENT, 0.9, 120, param1=50, param2=39, minRadius=1,
                                   maxRadius=180)

        if circles is not None:
            circles_to_round = self.np.uint16(self.np.around(circles))
            objects = circles_to_round.tolist()[0]
            wood = []
            for obj in objects:
                center = (obj[0], obj[1])
                wood.append(obj)
                self.cv.circle(img_original, (obj[0], obj[1]), 2, (0, 255, 255), 3)
                self.cv.circle(img_original, (obj[0], obj[1]), obj[2], (0, 255, 255), 3)
            count = circles_to_round.shape[1]

            if len(wood) == 0:
                self.No_wood_found(window)
            else:
                self.cv.imwrite("output.png", img_original)
                vol = self.Generate_Text_File(wood, length, count)
                self.Wood_Found_Window(window, vol)
        else:
            self.Generate_Text_File(None, length, 0, 1)
            self.No_wood_found(window)

    def Accuracy_window(self, window, path, length):
        current_image = self.tk.PhotoImage(file="Backgrounds/active_bg.png")
        bg_img_label = self.tk.Label(master=window, image=current_image)
        bg_img_label.image = current_image

        #bg_color_label = self.tk.Label(master=window, text="", height=15, width=57, bg="silver")


        Ip2_button = self.tk.Button(master=window, text="Processing 2", width=20, font=("times", 20), fg="black", bg="Blue",
                                  activebackground="cyan", command=lambda:self.Image_processing_Method2(window, path, length))
        Ip1_button = self.tk.Button(master=window, text="Processing 1", width=20, font=("times", 20), fg="black",
                               bg="Orange",
                               activebackground="cyan", command=lambda: self.Image_processing_Method1(window, path, length))
        Back_button = self.tk.Button(master=window, text="Home", width=10, font=("times", 20), fg="black", bg="Yellow",
                                activebackground="cyan", command=lambda: self.repeat_window(window))
        Quit_button = self.tk.Button(master=window, text="Exit", width=10, font=("times", 20), fg="black", bg="red",
                                activebackground="magenta", command=quit)
        bg_img_label.place(x=0, y=0, relwidth=1, relheight=1)
        #bg_color_label.place(x=180, y=108)
        Ip2_button.place(x=230, y=150)
        Ip1_button.place(x=230, y=250)
        Back_button.place(x=155, y=360)
        Quit_button.place(x=455, y=360)

    # Checks the path
    def check_path(self, window, path, length):
        if self.OS.path.exists(path):
            if (path.find(".") == -1):
                self.messagebox.showinfo("No Image Found", "Provide an image")
            else:
                right_dot = path.rfind(".") + 1
                if path[right_dot:] == "png" or path[right_dot:] == "jpg" or path[right_dot:] == "jpeg":
                    self.Accuracy_window(window, path, length)
                else:
                    self.messagebox.showinfo("Image Format Error",
                                           "Unsupported File type Supported Formats are jpg, jpeg, png")

    def get_file(self, window, length):
            filename = self.filedialog.askopenfile()
            if filename is not None:self.check_path(window, filename.name, length)
            else:self.messagebox.showinfo("Check image", "Oops select an image")

    def check_length(self, window, length):
        try:
            length = int(length)
            assert length > 0
            self.get_file(window, length)
        except:
            print("so sad")
            self.messagebox.showinfo("Check Length", "Oops Check length")
            self.repeat_window(window)



    def repeat_window(self, window):
        current_image = self.tk.PhotoImage(file="Backgrounds/active_bg.png")
        bg_img_label = self.tk.Label(master=window, image=current_image)
        bg_img_label.image = current_image
        bg_img_label.place(x=0, y=0, relwidth=1, relheight=1)

        caution_image = self.tk.PhotoImage(file = "Images/Caution-icon.png")
        caution_image_label = self.tk.Label(master = window, image = caution_image)
        suppported = self.tk.Label(master = window, text = "Supported formats are jpg, jpeg, png \n"
                                                           "we recommend image of minimum size 1200 x 800", font=("times", 15),
                                   fg="RED", bg="black", height= 2)
        input_len_label = self.tk.Label(master=window, text = "Enter the log length", font = ("times", 25),
                                        fg = "yellow", bg = "black", height = 1)
        Len = self.tk.StringVar()
        entry = self.tk.Entry(master = window,textvariable = Len,width = 10, fg = "black", bg = "white")

        caution_image_label.place(x = 148, y = 300)
        caution_image_label.image = caution_image
        suppported.place(x = 150 + 50, y = 300 )
        input_len_label.place(x = 200, y = 300 - 150)
        entry.place(x = 290+ 175, y = 310 - 150)

        choose_file = self.tk.Button(window, font=("times", 20), text="Open Image", width=10, fg="Silver", bg="Black",
                           activebackground="silver", command=lambda: self.check_length(window, Len.get()),
                           highlightcolor="black")

        choose_file.place(x=290, y=330 - 110)

    # Main_ window
    def Main_Window(self):
        window = self.tk.Tk()
        window.title("Forest_Wood_Detection")
        canvas = self.tk.Canvas(window, bg="black", height=499, width=750)
        background_image = self.tk.PhotoImage(file="Backgrounds/active_bg.png")
        canvas.image = background_image
        canvas.create_image(0, 0, anchor=self.tk.NE, image=background_image)
        canvas.pack()
        self.repeat_window(window)
        window.mainloop()

if __name__ == "__main__":
    detect_wood = Log_Detection()
    detect_wood.Main_Window()
