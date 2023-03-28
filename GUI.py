from PySimpleGUI import Frame, Window, \
                        Text, InputText, Checkbox, Combo, FileBrowse, Button, Multiline, Column
import sys
from os import path


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


def create_window():
    """
    Возвращает готовое окно и хранит layout
    """
    layout_car = [[
        Frame(title='Car', layout=[
            [
                Text("Percents Up", size=(11, 1)),
                Text("T:"), InputText(key='UTSPREAD', size=(4, 1)),
                Text("C:"), InputText(key='UCSPREAD', size=(4, 1)),
                Text("R:"), InputText(key='URSPREAD', size=(4, 1)),
                Text("E:"), InputText(key='UESPREAD', size=(4, 1)),
            ],
            [
                Text("Percents Down", size=(11, 1)),
                Text("T:"), InputText(key='DTSPREAD', size=(4, 1)),
                Text("C:"), InputText(key='DCSPREAD', size=(4, 1)),
                Text("R:"), InputText(key='DRSPREAD', size=(4, 1)),
                Text("E:"), InputText(key='DESPREAD', size=(4, 1)),
            ],
            [
                Text("Real Respect Percent:", size=(18, 1)), InputText(key='R_PERCENT',
                                                                       size=(4, 1), default_text="25"),
            ],
            [
                Text("Real Efficiency Percent:", size=(18, 1)), InputText(key='E_PERCENT',
                                                                          size=(4, 1), default_text="25"),
            ],
        ])
    ]]

    layout_avatar = [[
        Frame(title='Avatar', layout=[
            [
                # Text("Driver:", size=(4, 1)),
                Checkbox(text='Driver', key='CHECKDRIVER'),
            ],
            [
                # Text("Technician:", size=(4, 1)),
                Checkbox(text='Technician', key='CHECKTECH'),
            ],
            [
                # Text("Ecologist:", size=(4, 1)),
                Checkbox(text='Ecologist', key='CHECKECOLOG'),
            ],
            [
                Text("Min Level:", size=(7, 1)), InputText(key='MINLEVEL', size=(4, 1), default_text='1'),
                Text("Max Level:", size=(7, 1)), InputText(key='MAXLEVEL', size=(4, 1), default_text='25'),
            ],
        ])
    ]]

    layout_type = [[
        Frame(title='Type', layout=[
            [
                #Text("Type"),
                Checkbox(text='Type A', key='TYPEA'),
                Checkbox(text='Type B', key='TYPEB'),
                Checkbox(text='Type C', key='TYPEC'),
                Checkbox(text='Type D', key='TYPED'),
            ],
        ])
    ]]

    layout_rarity = [[
        Frame(title='Rarity', layout=[
            [
                #Text("Rarity:"),
                Checkbox(text='Classic', key='CLASSIC'),
                Checkbox(text='Rare', key='RARE'),
                Checkbox(text='Epic', key='EPIC'),
                Checkbox(text='Legendary', key='LEGENDARY'),
                Checkbox(text='Insane', key='INSANE'),
            ],
        ])
    ]]

    layout_data = [[
        Frame(title='', layout=[
            [
                Text("Base Data:", size=(8, 1)), InputText(key='SPREADDATA', size=(30, 1)),
                FileBrowse(target='SPREADDATA', file_types=(('Excel Files', '*.xlsx'),)),
            ],
            [
                Text("Output file:", size=(8, 1)),
                InputText(key='OUTPUTDATA', size=(30, 1), default_text='output'),
            ],
        ])
    ]]

    layout = [
        [
            Column(layout_car), Column(layout_avatar),
        ],
        [
            Column(layout_type, ),
        ],
        [
            Column(layout_rarity),
        ],
        [
            Column(layout_data),
        ],
        [
            Text("Count:", size=(5, 1)), InputText(key='CARCOUNT', size=(12, 1)),
        ],
        [
            Button("Generate", key='GENERATE'),
            Button("Help", key='HELP'),
        ],
        [
            Multiline(autoscroll=True, auto_refresh=True,
                      reroute_stdout=True, size=(90, 25),
                      font="Courier",
                      default_text="Info:\n"
                                   "1. DO NOT START GENERATION WHEN YOUR OUTPUT FILE IS OPEN\n"
                                   "2. INPUT AND OUTPUT FILES MUST BE .XLSX FORMAT\n"
                                   "3. T - TANK, C - CONSUMPTION, R - RESPECT, E - EFFICIENCY\n"
                                   "4. Percents Up shows how much higher the value can be\n"
                                   "5. Percents Down shows how much lower the value can be\n"),
        ],
    ]

    #window_out = Window(title='Car Generate', layout=layout, icon=resource_path('icon.ico'))
    window_out = Window(title='Car Generate', layout=layout, icon=resource_path('icon.ico'))

    return window_out
