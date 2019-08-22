from tkinter import *
import json

tk = None

def openGui():
    with open("phone_numbers.json", 'r') as f:
        phone_numbers = json.load(f)

    if len(phone_numbers) > 0:
        phone_number = phone_numbers[0]
    else:
        phone_number = "None"

    tk = Tk()
    tk.title("Auto Skrab Settings")
    tk.geometry("350x350")
    tk.resizable(0, 0)
    tk.iconbitmap('app.ico')

    inputString = StringVar()

    mainframe = Frame(tk, bg="white", width=350, height=350)
    mainframe.grid(row=1)

    title = Label(mainframe, text="Cirkle K Auto Skrab", font=("Arial", 25), bg="white")
    title.place(rely=0.125, relx=0.5, anchor=CENTER)

    number_field_text = Label(mainframe, text="Current Phone Number: " + phone_number, font=("Arial", 12), bg="white")
    number_field_text.place(rely=0.4, relx=0.5, anchor=CENTER)

    status_label = Label(mainframe, text="", font=("Arial", 12), bg="white", fg="red")
    status_label.place(rely=0.7, relx=0.5, anchor=CENTER)

    phone_number_field = Entry(mainframe, textvariable=inputString)
    phone_number_field.place(rely=0.5, relx=0.5, anchor=CENTER)

    def setNumber():
        global phone_number

        input = inputString.get()
        if len(input) != 8:
            status_label.config(text="Not a valid phone number")
            return
        if not input.isdigit():
            status_label.config(text="Not a valid phone number")
            return

        if len(phone_numbers) > 0:
            phone_numbers[0] = input
        else:
            phone_numbers.append(input)

        with open('phone_numbers.json', 'w') as g:
            json.dump(phone_numbers, g)

        phone_number = input
        inputString.set("")
        status_label.config(text="")
        number_field_text.config(text=("Current Phone Number: " + phone_number))

    set_phone_number_button = Button(mainframe, text="Set Phone Number", command=setNumber)
    set_phone_number_button.place(rely=0.6, relx=0.5, anchor=CENTER)



    tk.mainloop()
