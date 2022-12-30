import tkinter as tk

root = tk.Tk()

fl = False
def Hello(event):
    global fl
    fl = True
    print("Yet another hello world")

def Hello1(event):
    global fl
    while True:
        print('==')
        if fl:
            print(fl)
            fl = False


btn = tk.Button(root,
             text="Click me",
             width=30,height=5,
             bg="white",fg="black")
btn.bind("<Button-1>", Hello)
btn2 = tk.Button(root,
                text="Click me",
                width=30, height=5,
                bg="white", fg="black")
btn2.bind("<Button-1>", Hello1)
btn.pack()
btn2.pack()
root.mainloop()
