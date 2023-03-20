import PySimpleGUI as sg
import pandas as pd
from Car import generateCar, transformRare, transformType
from Avatar import generateAvatar
from OutputClass import OutputClass


def create_window():
    layout_car = [[
        sg.Frame(title='Car', layout=[
            [
                sg.Text("Percents Up", size=(11, 1)),
                sg.Text("T:"), sg.InputText(key='UTSPREAD', size=(4, 1)),
                sg.Text("C:"), sg.InputText(key='UCSPREAD', size=(4, 1)),
                sg.Text("R:"), sg.InputText(key='URSPREAD', size=(4, 1)),
                sg.Text("E:"), sg.InputText(key='UESPREAD', size=(4, 1)),
            ],
            [
                sg.Text("Percents Down", size=(11, 1)),
                sg.Text("T:"), sg.InputText(key='DTSPREAD', size=(4, 1)),
                sg.Text("C:"), sg.InputText(key='DCSPREAD', size=(4, 1)),
                sg.Text("R:"), sg.InputText(key='DRSPREAD', size=(4, 1)),
                sg.Text("E:"), sg.InputText(key='DESPREAD', size=(4, 1)),
            ],
            [
                sg.Text("Real Respect Percent:", size=(18, 1)), sg.InputText(key='R_PERCENT',
                                                                             size=(4, 1), default_text="25"),
            ],
            [
                sg.Text("Real Efficiency Percent:", size=(18, 1)), sg.InputText(key='E_PERCENT',
                                                                                size=(4, 1), default_text="25"),
            ],
        ])
    ]]

    layout_avatar = [[
        sg.Frame(title='Avatar', layout=[
            [
                # sg.Text("Driver:", size=(4, 1)),
                sg.Checkbox(text='Driver', key='CHECKDRIVER'),
            ],
            [
                # sg.Text("Technician:", size=(4, 1)),
                sg.Checkbox(text='Technician', key='CHECKTECH'),
            ],
            [
                # sg.Text("Ecologist:", size=(4, 1)),
                sg.Checkbox(text='Ecologist', key='CHECKECOLOG'),
            ],
            [
                sg.Text("Min Level:", size=(7, 1)), sg.InputText(key='MINLEVEL', size=(4, 1), default_text='1'),
                sg.Text("Max Level:", size=(7, 1)), sg.InputText(key='MAXLEVEL', size=(4, 1), default_text='25'),
            ],
        ])
    ]]

    layout_down = [[
        sg.Frame(title='', layout=[
            [
                sg.Text("Type:", size=(5, 1)),
                sg.Combo(["Type A", "Type B", "Type C", "Type D"],
                         key='TYPE', size=(10, 1), default_value="Type A"),
                sg.Text("Base Data:", size=(8, 1)), sg.InputText(key='SPREADDATA', size=(30, 1)),
                sg.FileBrowse(target='SPREADDATA', file_types=(('Excel Files', '*.xlsx'),)),
            ],
            [
                sg.Text("Rare:", size=(5, 1)),
                sg.Combo(["Classic", "Rare", "Epic", "Legendary", "Insane"],
                         key='RARE', size=(10, 1), default_value="Classic"),
                sg.Text("Output file:", size=(8, 1)),
                sg.InputText(key='OUTPUTDATA', size=(30, 1), default_text='output'),
            ],
            [
                sg.Text("Count:", size=(5, 1)), sg.InputText(key='CARCOUNT', size=(12, 1)),
            ],
            [
                sg.Button("Generate", key='GENERATE'),
                sg.Button("Help", key='HELP'),
            ],
            [
                sg.Multiline(autoscroll=True, auto_refresh=True,
                             reroute_stdout=True, size=(90, 25),
                             font="Courier",
                             default_text="Info:\n"
                                          "1. DO NOT START GENERATION WHEN YOUR OUTPUT FILE IS OPEN\n"
                                          "2. INPUT AND OUTPUT FILES MUST BE .XLSX FORMAT\n"
                                          "3. T - TANK, C - CONSUMPTION, R - RESPECT, E - EFFICIENCY\n"
                                          "4. Percents Up shows how much higher the value can be\n"
                                          "5. Percents Down shows how much lower the value can be\n"),
            ],
        ])
    ]]
    layout = [
        [
            sg.Column(layout_car), sg.Column(layout_avatar),
        ],
        [
            layout_down,
        ],
    ]
    window_out = sg.Window('Car Generate', layout)
    return window_out


def checkPercents(values_window):
    if not (values_window["UTSPREAD"].isdigit() and
            values_window["UCSPREAD"].isdigit() and
            values_window["URSPREAD"].isdigit() and
            values_window["UESPREAD"].isdigit() and
            values_window["DTSPREAD"].isdigit() and
            values_window["DCSPREAD"].isdigit() and
            values_window["DRSPREAD"].isdigit() and
            values_window["MINLEVEL"].isdigit() and
            values_window["MAXLEVEL"].isdigit()):
        return True
    else:
        return False


def info():
    print("================================================================================")
    print("    Info:")
    print("    1. DO NOT START GENERATION WHEN YOUR OUTPUT FILE IS OPEN")
    print("    2. INPUT AND OUTPUT FILES MUST BE .XLSX FORMAT")
    print("    3. T - TANK, C - CONSUMPTION, R - RESPECT, E - EFFICIENCY")
    print("    4. Percents Up shows how much higher the value can be")
    print("    5. Percents Down shows how much lower the value can be")
    print("================================================================================")


if __name__ == '__main__':

    window = create_window()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if 'HELP' in event:
            info()

        if 'GENERATE' in event:
            if checkPercents(values):
                print("ERROR: something wrong in percents or levels!")

            elif values["SPREADDATA"] == '':
                print("ERROR: no data of spread")

            elif not values["CARCOUNT"].isdigit():
                print("ERROR: count error")

            else:
                output_list = []
                for i in range(int(values["CARCOUNT"])):

                    car_type = transformType(values["TYPE"])
                    car_rare = transformRare(values["RARE"])
                    ut_spread = int(values["UTSPREAD"])
                    uc_spread = int(values["UCSPREAD"])
                    ur_spread = int(values["URSPREAD"])
                    ue_spread = int(values["UESPREAD"])
                    dt_spread = int(values["UTSPREAD"])
                    dc_spread = int(values["UCSPREAD"])
                    dr_spread = int(values["URSPREAD"])
                    de_spread = int(values["UESPREAD"])
                    data_file = values["SPREADDATA"]

                    avatar_types = [int(values['CHECKDRIVER']), int(values['CHECKTECH']), int(values['CHECKECOLOG'])]
                    avatar_level = [int(values['MINLEVEL']), int(values['MAXLEVEL'])]
                    Avatar = generateAvatar(avatarList=avatar_types,
                                            levelList=avatar_level,
                                            file=data_file)

                    Car = generateCar(type_of_car=car_type, rarity_of_car=car_rare,
                                      UTspread=ut_spread, UCspread=uc_spread, URspread=ur_spread, UEspread=ue_spread,
                                      DTspread=dt_spread, DCspread=dc_spread, DRspread=dr_spread, DEspread=de_spread,
                                      file=data_file)

                    Car.max_distance = Car.getMaxDistance()

                    Car.R_percent = int(values["R_PERCENT"])
                    Car.respect_real = Car.getRealRespect()

                    Car.E_percent = int(values["E_PERCENT"])
                    Car.efficiency_real = Car.getRealEfficiency()

                    Car.VAT = Avatar.versality
                    Car.MAT = Avatar.mastery

                    Car.respect = Car.getRespect()
                    Car.efficiency = Car.getEfficiency()

                    Car.earning_base = Car.getBaseEarning()
                    Car.earning_real = Car.getRealEarning()

                    Car.occupation = Car.getOccupation()

                    Output = OutputClass(car=Car, avatar=Avatar)
                    output_list.append(Output)

                    print(i + 1, ". Type Car:   ", Car.getTypeName())
                    print(i + 1, ". Rarity:     ", Car.getRarityName())
                    print(i + 1, ". Type Avatar:", Avatar.type)
                    print(i + 1, ". Level:      ", Avatar.level)
                    print(i + 1, ". Talents:    ", Avatar.talents)
                    print("======================================")

                out_data = pd.DataFrame([vars(output) for output in output_list])

                try:
                    out_data.to_excel(values['OUTPUTDATA']+'.xlsx', index=False, header=True)
                    print("SUCCESS: Data saved")
                except PermissionError:
                    print("ERROR: May be you don't close your output file before generating")
                    info()
