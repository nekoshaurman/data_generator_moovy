# import PySimpleGUI as sg
# import pandas as pd
from PySimpleGUI import  WIN_CLOSED
from pandas import DataFrame
from Car import generateCar
from Avatar import generateAvatar
from OutputClass import OutputClass
from GUI import create_window


def checkDigits(values_window):
    """
    Проверка, что введены числа
    """
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
        if event == WIN_CLOSED or event == 'Exit':
            break

        # Подсказка по нажатию кнопки
        if 'HELP' in event:
            info()

        # Начало генерации по кнопке
        if 'GENERATE' in event:
            # Проверка, что введены числа
            if checkDigits(values):
                print("ERROR: something wrong in percents or levels!")

            # Введен ли файл с данными
            elif values["SPREADDATA"] == '':
                print("ERROR: no data of spread")

            # Введено ли количество которое нужно сгенерировать
            elif not values["CARCOUNT"].isdigit():
                print("ERROR: count error")

            # Основной алгоритм
            else:
                output_list = []
                for i in range(int(values["CARCOUNT"])):
                    #car_type = transformType(values["TYPE"])
                    #car_rare = transformRare(values["RARE"])
                    ut_spread = int(values["UTSPREAD"])
                    uc_spread = int(values["UCSPREAD"])
                    ur_spread = int(values["URSPREAD"])
                    ue_spread = int(values["UESPREAD"])
                    dt_spread = int(values["UTSPREAD"])
                    dc_spread = int(values["UCSPREAD"])
                    dr_spread = int(values["URSPREAD"])
                    de_spread = int(values["UESPREAD"])
                    data_file = values["SPREADDATA"]

                    # Генерация аватара
                    avatar_types = [int(values['CHECKDRIVER']), int(values['CHECKTECH']), int(values['CHECKECOLOG'])]
                    avatar_level = [int(values['MINLEVEL']), int(values['MAXLEVEL'])]
                    Avatar = generateAvatar(avatarList=avatar_types,
                                            levelList=avatar_level,
                                            file=data_file)

                    # Генерация машины
                    car_types = [int(values['TYPEA']), int(values['TYPEB']), int(values['TYPEC']), int(values['TYPED'])]
                    car_rarities = [int(values['CLASSIC']), int(values['RARE']), int(values['EPIC']),
                                    int(values['LEGENDARY']), int(values['INSANE']), ]
                    Car = generateCar(types_of_car=car_types,
                                      rarities_of_car=car_rarities,
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

                    # Создаем класс для вывода в файл
                    Output = OutputClass(car=Car, avatar=Avatar)
                    output_list.append(Output)

                    print(i + 1, ". Type Car:   ", Car.getTypeName())
                    print(i + 1, ". Rarity:     ", Car.getRarityName())
                    print(i + 1, ". Type Avatar:", Avatar.type)
                    print(i + 1, ". Level:      ", Avatar.level)
                    print(i + 1, ". Talents:    ", Avatar.talents)
                    print("======================================")

                out_data = DataFrame([vars(output) for output in output_list])

                try:
                    out_data.to_excel(values['OUTPUTDATA']+'.xlsx', index=False, header=True)
                    print("SUCCESS: Data saved")
                except PermissionError:
                    print("======================================")
                    print("ERROR: May be you don't close your output file before generating")
                    info()
