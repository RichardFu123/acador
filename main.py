# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import PySimpleGUI as sg
from acador.utils.arxiv_json_reader import get_arxiv_db

def test():
    # Use a breakpoint in the code line below to debug your script.
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Some text on Row 1')],
              [sg.Text('Enter something on Row 2'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        print('You entered ', values[0])

    window.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    conn = get_arxiv_db()
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM Documents WHERE id IS "0704.0051"').fetchall()
    data = dict(zip([c[0] for c in cur.description], res[0]))
    print(data)
    # test()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
