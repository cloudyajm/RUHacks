# pylint: disable=no-member
########################################################FLASK#####################################################

import pandas
import folium
import base64
from google.cloud.vision import types
from google.cloud import vision
import backend
from tkinter import *
import os
import io
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)


def guipop():

    def get_selected_row(event):
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])

    def view_command():
        list1.delete(0, END)
        for row in backend.view():
            list1.insert(END, row)

    def search_command():
        list1.delete(0, END)
        for row in backend.search(patient_text.get(), address_text.get(), prescription_text.get(), date_text.get()):
            list1.insert(END, row)

    def add_command():
        backend.insert(patient_text.get(), address_text.get(),
                       prescription_text.get(), date_text.get())
        list1.delete(0, END)
        list1.insert(END, (patient_text.get(), address_text.get(),
                           prescription_text.get(), date_text.get()))

    def delete_command():
        backend.delete(selected_tuple[0])

    def update_command():
        backend.update(selected_tuple[0], patient_text.get(
        ), address_text.get(), prescription_text.get(), date_text.get())

    window = Tk()

    window.wm_title("Prescription Database")

    l1 = Label(window, text="Patient")
    l1.grid(row=0, column=0)

    l2 = Label(window, text="Address")
    l2.grid(row=0, column=2)

    l3 = Label(window, text="Prescription")
    l3.grid(row=1, column=0)

    l4 = Label(window, text="Date")
    l4.grid(row=1, column=2)

    patient_text = StringVar()
    e1 = Entry(window, textvariable=patient_text)
    e1.grid(row=0, column=1)

    address_text = StringVar()
    e2 = Entry(window, textvariable=address_text)
    e2.grid(row=0, column=3)

    prescription_text = StringVar()
    e3 = Entry(window, textvariable=prescription_text)
    e3.grid(row=1, column=1)

    date_text = StringVar()
    e4 = Entry(window, textvariable=date_text)
    e4.grid(row=1, column=3)

    list1 = Listbox(window, height=6, width=35)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    sb1 = Scrollbar(window)
    sb1.grid(row=2, column=2, rowspan=6)

    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)

    list1.bind('<<ListboxSelect>>', get_selected_row)

    b1 = Button(window, text="View all", width=12, command=view_command)
    b1.grid(row=2, column=3)

    b2 = Button(window, text="Search entry", width=12, command=search_command)
    b2.grid(row=3, column=3)

    b3 = Button(window, text="Add entry", width=12, command=add_command)
    b3.grid(row=4, column=3)

    b4 = Button(window, text="Update selected",
                width=12, command=update_command)
    b4.grid(row=5, column=3)

    b5 = Button(window, text="Delete selected",
                width=12, command=delete_command)
    b5.grid(row=6, column=3)

    b6 = Button(window, text="Close", width=12, command=window.destroy)
    b6.grid(row=7, column=3)

    window.mainloop()


def detect_document(path):
    string = ""
    date1 = ""
    worddate = ""
    apple = ""
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))
                    if word_text == apple:
                        word_text = ""
                    if word_text == "R" or word_text == "B":
                        word_text = ""
                    if "/" in word_text:
                        date1 = word_text
                        word_text = ""
                    if word_text == "Date":
                        worddate = word_text
                        word_text = ""
                    string += word_text + " "
                    apple = word_text
                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    string += worddate + " " + date1
    return (string)


def getData(x):
    string = x
    string = string.upper()
    print(string)
    array = string.split()
    array.append("END")
    print(string)

    def getItem(start, end):

        i = 0
        j = 0
        item = ""
        while i < len(array):
            if array[i] == start:
                item = array[i+1]
                break
            i += 1

        j = i+2
        while j < len(array):
            if array[j] == "PATIENT" or array[j] == "ADDRESS" or array[j] == "PRESCRIPTION" or array[j] == "SIGNATURE" or array[j] == "DATE" or array[j] == "END":
                break
            item += " "
            item += array[j]
            j += 1
        return item

    patient = getItem("PATIENT", "ADDRESS")  # Patient
    address = getItem("ADDRESS", "PRESCRIPTION")  # Address
    prescription = getItem("PRESCRIPTION", "SIGNATURE")  # Prescription
    signature = getItem("SIGNATURE", "DATE")  # Signature
    date = getItem("DATE", "END")  # Date
    print("---------------------------------------------------------------")

    print(patient)
    print(address)
    print(prescription)
    # print(signature)
    print(date)
    backend.insert(patient, address, prescription, date)
    print("---------------------------------------------------------------")


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file2():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        getData(detect_document(f.filename))
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)

# Imports the Google Cloud client library

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath(
    '/Users/hassanalawie/MyCode/try2/andrewprescrip.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

path = 'andrewprescrip.jpg'


# # ########################################################GUI CODE###############################################################


guipop()
