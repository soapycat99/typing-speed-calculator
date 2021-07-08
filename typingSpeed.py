import time
from tkinter import W, E
import tkinter as tk
from words import words
import random
WIDTH = 900
HEIGHT = 400
temp = 60
pointer = 0


class Typing:

    def __init__(self, master):
        self.master = master
        self.master.grid_rowconfigure(0,weight =1)
        self.master.grid_rowconfigure(1,weight =2)
        self.master.grid_rowconfigure(2,weight =1)
        self.master.grid_columnconfigure(1,weight =1)

        self.text = tk.Label(self.master,text = 'Typing Speed Calculator', font = ('Arial', 30))
        self.text.pack()
        self.canvas = tk.Canvas(self.master, width = WIDTH, height= HEIGHT/4, bg = 'light yellow')

        #variable
        self.correct = 0
        self.incorrect = 0
        self.onKey = 0
        self.offKey = 0
        # text list
        self.list1 = self.randomText()
        self.list2 = self.randomText()

        # canvas text
        self.text1, self.text2 = self.createText() #list of canvas text


        # typing area
        self.typingArea = tk.Canvas(self.master, bg='light blue', width=WIDTH, height=10)
        self.typingArea.grid_rowconfigure(0, weight=1)
        self.typingArea.grid_columnconfigure(0, weight=4)
        self.typingArea.grid_columnconfigure(1, weight=1)
        self.typingArea.grid_columnconfigure(2, weight=1)

        # typing label
        self.typingEntry = self.typeArea()
        self.typingEntry.grid(row=0,column=0, pady =10, padx = 10)

        # timer
        self.timer = tk.StringVar()
        self.timer.set('1:00')
        self.timerLabel = self.runTimer()

        # pack
        self.canvas.pack()
        self.typingArea.pack()

        #binding
        self.typingEntry.bind("<space>", self.submit)

    # def createTimer(self):
    #     global temp
    #
    #     timerLabel = tk.Label(self.typingArea, height=2, width=5,
    #                           bg='light gray', textvariable=self.timer, font=('Arial', 20, 'bold'), fg='white')
    #     timerLabel.grid(row=0, column=1, padx=10, sticky='w')
    #     return timerLabel

    def runTimer(self):
        global temp

        timerLabel = tk.Label(self.typingArea, height=2, width=5,
                              bg='light gray', textvariable= self.timer, font=('Arial', 20, 'bold'), fg='white')
        timerLabel.grid(row=0, column=1, padx=10, sticky='w')

        #timer

        if temp>50:
            temp -= 1
            timerString = temp
            self.timer.set('0:{:02d}'.format(timerString))
            timerLabel.after(1000, self.runTimer)
        else:
            self.typingEntry.config(state = tk.DISABLED)
            print('Correct: ' + str(self.correct))
            print('Incorrect: ' + str(self.incorrect))
            self.resultWindow()

        return timerLabel

    def resultWindow(self):
        SUBWIDTH = 400
        new_window = tk.Toplevel()
        new_window.title('Result')
        subcanvas = tk.Canvas(new_window, bg= '#f2f0e9', width = SUBWIDTH)
        result = int(self.onKey/5)

        tk.Label(subcanvas, text = str(result) + ' WPM', bg= '#f2f0e9',
                 fg= 'green', font= ('Arial', 56, 'bold')).pack(pady= (10,0), padx = 100, anchor = tk.S)
        tk.Label(subcanvas, text= '(words per minute)', bg= '#f2f0e9',
                 fg = '#cccac2', font=('Arial', 15, 'bold')).pack(pady=(0,4), padx= 100, anchor = tk.N)
        subcanvas.pack()

        #box 1
        can1 = tk.Canvas(new_window, width = SUBWIDTH,height = 40)
        can1.pack(anchor=tk.N, expand = tk.YES, fill = tk.BOTH)
        tk.Label(can1, text = 'Keystrokes', font = ('Arial', 20)).pack(pady= 5, padx= 20, side= 'left')
        tk.Label(can1, text = str(self.onKey + self.offKey),
                 font = ('Arial', 20)).pack(padx= 20, pady= 5, side= 'right')

        # can1.create_line(0, 0, WIDTH, 0)
        subtext= can1.create_text(305,17, text= '(       |       )')
        bounds = can1.bbox(subtext)
        x1 = bounds[0] + 18
        x2 = bounds[2] - 18
        can1.create_text(x1, 18, text= self.onKey, fill= 'green')
        can1.create_text(x2, 18, text=self.offKey, fill='red')

        #box 2
        can2 = tk.Canvas(new_window, width = SUBWIDTH,height = 40, bg= '#f2f0e9')
        can2.pack(anchor=tk.N, expand = tk.YES, fill = tk.BOTH)
        tk.Label(can2, text = 'Accuracy', font = ('Arial', 20), bg= '#f2f0e9').pack(pady= 5, padx= 20, side= 'left')
        accuracy = round(self.onKey / float((self.onKey + self.offKey)) * 100,2)
        tk.Label(can2, text=str(accuracy) + '%',
                 font=('Arial', 20, 'bold'), bg= '#f2f0e9').pack(padx=20, pady=5, side='right')

        #box 3
        can3 = tk.Canvas(new_window, width = SUBWIDTH,height = 40)
        can3.pack(anchor=tk.N, expand = tk.YES, fill = tk.BOTH)
        tk.Label(can3, text = 'Correct words', font = ('Arial', 20)).pack(pady= 5, padx= 20, side= 'left')
        tk.Label(can3, text=str(self.correct), fg = 'green',
                 font=('Arial', 20)).pack(padx=20, pady=5, side='right')

        #box 4
        can4 = tk.Canvas(new_window, width=SUBWIDTH, height=40, bg= '#f2f0e9')
        can4.pack(anchor=tk.N, expand=tk.YES, fill=tk.BOTH)
        tk.Label(can4, text='Wrong words', font=('Arial', 20), bg= '#f2f0e9').pack(pady=5, padx=20, side='left')
        tk.Label(can4, text=str(self.incorrect), bg= '#f2f0e9', fg= 'red',
                 font=('Arial', 20)).pack(padx=20, pady=5, side='right')

    def typeArea(self):

        typingEntry = tk.Entry(self.typingArea, font =("Ink Free", 30), highlightthickness = 2)
        return typingEntry

    def submit(self, event):
        global pointer
        color = ' '

        result = self.typingEntry.get().strip()

        if result == self.list1[0]:
            self.correct +=1
            self.onKey += len(self.list1[0])
            color = 'green'
        else:
            self.incorrect += 1
            self.offKey += len(self.list1[0])
            color = 'red'


        print('keystroke: ' + str(self.onKey+self.offKey))
        #change color word typed
        self.changeColor(pointer, color)
        self.list1.pop(0)
        print(self.list1)
        self.typingEntry.delete(0,tk.END)
        pointer +=1

        if pointer > 8:
            pointer = 0
            self.flipText()
            self.text1, self.text2 = self.flipPosition()


    def flipPosition(self):
        for i in range(len(self.text1)):
            self.canvas.delete(self.text1[i])
        for i in range(len(self.text2)):
            self.canvas.delete(self.text2[i])

        #copy text2 to text1
        coord_x1 = 30
        coord_y1 = 37
        text1 = []
        for i in range(len(self.list1)):
            if i == 0:
                tempText = self.canvas.create_text(coord_x1, coord_y1,
                                                   text=self.list1[i], font=('Arial', 25), anchor = W)
            else:
                bounds = self.canvas.bbox(text1[i - 1])
                #test
                print(self.canvas.coords(text1[i-1]))
                print(text1[i-1])
                print(type(bounds))
                print(bounds)
                #stop
                x = bounds[2] + 10
                tempText = self.canvas.create_text(x, coord_y1,
                                                   text=self.list1[i], font=('Arial', 25), anchor= W)
            text1.append(tempText)
            print('print temp text'+str(tempText))
        text2 = []
        coord_x2 = 30
        coord_y2 = self.canvas.bbox(text1[0])[3] + 20

        text2 = []
        for i in range(len(self.list2)):
            if i == 0:
                tempText = self.canvas.create_text(coord_x2, coord_y2,
                                                   text=self.list2[i], font=('Arial', 25), anchor=W)
            else:
                bounds = self.canvas.bbox(text2[i - 1])
                x = bounds[2] + 10
                # var = self.canvas.itemcget(text2[i - 1], 'text')
                tempText = self.canvas.create_text(x, coord_y2,
                                                   text=self.list2[i], font=('Arial', 25), anchor=W)
            text2.append(tempText)

        return text1, text2

    def flipText(self):
        for i in range(len(self.list2)):
            self.list1.append(self.list2[i])

        tempList = self.randomText()

        for i in range(len(self.list2)):
            self.list2.pop(0)
            self.list2.append(tempList[i])


    def changeColor(self, pointer, color):
        self.canvas.itemconfig(self.text1[pointer], fill= color )

    def randomText(self):
        # text1 = ""
        # text2 = ''
        randomList = []
        for i in range(9):
            randomList.append(random.choice(words))

        print(randomList)

        return randomList

    def createText(self):
        coord_x1 = 30
        coord_y1 = 37

        text1 = []
        for i in range(len(self.list1)):
            if i == 0:
                tempText = self.canvas.create_text(coord_x1, coord_y1,
                                                   text=self.list1[i], font=('Arial', 25), anchor = W)
            else:
                bounds = self.canvas.bbox(text1[i - 1])
                #test
                print(self.canvas.coords(text1[i-1]))
                print(text1[i-1])
                print(type(bounds))
                print(bounds)
                #stop
                x = bounds[2] + 10
                # var = self.canvas.itemcget(text1[i - 1], 'text')
                tempText = self.canvas.create_text(x, coord_y1,
                                                   text=self.list1[i], font=('Arial', 25), anchor= W)
            text1.append(tempText)

        coord_x2 = 30
        coord_y2 = self.canvas.bbox(text1[0])[3] + 20
        text2 = []

        for i in range(len(self.list2)):
            if i == 0:
                tempText = self.canvas.create_text(coord_x2, coord_y2,
                                                   text=self.list2[i], font=('Arial', 25), anchor= W)
            else:
                bounds = self.canvas.bbox(text2[i - 1])
                x = bounds[2] + 10
                # var = self.canvas.itemcget(text2[i - 1], 'text')
                tempText = self.canvas.create_text(x, coord_y2,
                                                   text=self.list2[i], font=('Arial', 25), anchor=W)
            text2.append(tempText)
        # print(text1)
        # print(text2)

        return text1, text2

    def driver(self):
        pass



def main():
    root = tk.Tk()
    root.title('Typing Speed')
    window_height = root.winfo_height()
    window_width = root.winfo_width()
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    x = int(screen_width/2 - window_width/2)
    y = int(screen_height/2 - window_height/2)
    root.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')
    app = Typing(root)
    app.driver()
    root.mainloop()

if __name__ == '__main__':
    main()
