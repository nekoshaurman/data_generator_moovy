import enum
import random
import numpy as np
import PySimpleGUI as sg
import pandas as pd


class TypeCar(enum.Enum):
    typeA = 0
    typeB = 1
    typeC = 2
    typeD = 3


class RarityCar(enum.Enum):
    classic = 0
    rare = 1
    epic = 2
    legendary = 3
    insane = 4


class TestCar:
    def __init__(self, type_of_car, rarity_of_car, tank, consumption, respect, efficiency, price):
        self.type = type_of_car
        self.rarity = rarity_of_car
        self.tank_base = tank
        self.consumption_base = consumption
        self.respect_base = respect
        self.efficiency_base = efficiency
        self.price = price

        self.max_distance = None
        self.R_percent = None
        self.E_percent = None
        self.respect_real = None
        self.efficiency_real = None

        self.VAT = None
        self.MAT = None

        self.respect = None
        self.efficiency = None

        self.earning_base = None
        self.earning_real = None
        self.occupation = None

    def getTypeDigit(self):
        return self.type.value

    def getTypeName(self):
        return self.type.name

    def getRarityDigit(self):
        return self.rarity.value

    def getRarityName(self):
        return self.rarity.name

    def getMaxDistance(self):
        return self.tank_base * 10 / self.consumption_base

    def getRealRespect(self):
        return self.respect_base - (self.respect_base * self.R_percent / 100)

    def getRealEfficiency(self):
        return self.efficiency_base - (self.efficiency_base * self.E_percent / 100)

    def getRespect(self):
        return self.respect_real * self.VAT / 100

    def getEfficiency(self):
        return self.efficiency_real * self.MAT / 100

    def getBaseEarning(self):
        return self.max_distance * self.respect / 100 / 2

    def getRealEarning(self):
        return self.earning_base * self.efficiency

    def getOccupation(self):
        return self.price / self.earning_base


def generateCar(type_of_car, rarity_of_car,
                UTspread, UCspread, URspread, UEspread,
                DTspread, DCspread, DRspread, DEspread,
                file):

    TankData, ConsumptionData, RespectData, EfficiencyData, PricesData = getData(file)

    Tank = round(random.uniform(
        (TankData[type_of_car.value][rarity_of_car.value] * (1 - DTspread / 100)),
        (TankData[type_of_car.value][rarity_of_car.value] * (1 + UTspread / 100))), 2)

    Consumption = round(random.uniform(
        (ConsumptionData[type_of_car.value][rarity_of_car.value] * (1 - DCspread / 100)),
        (ConsumptionData[type_of_car.value][rarity_of_car.value] * (1 + UCspread / 100))), 2)

    Respect = round(random.uniform(
        (RespectData[type_of_car.value][rarity_of_car.value] * (1 - DRspread / 100)),
        (RespectData[type_of_car.value][rarity_of_car.value] * (1 + URspread / 100))), 2)

    Efficiency = round(random.uniform(
        (EfficiencyData[type_of_car.value][rarity_of_car.value] * (1 - DEspread / 100)),
        (EfficiencyData[type_of_car.value][rarity_of_car.value] * (1 + UEspread / 100))), 4)

    Price = round(PricesData[type_of_car.value][rarity_of_car.value], 0)

    car = TestCar(type_of_car, rarity_of_car, Tank, Consumption, Respect, Efficiency, Price)

    return car


def create_window():
    layout = [
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
            sg.Text("VAT:", size=(4, 1)), sg.InputText(key='VAT', size=(4, 1)),
        ],
        [
            sg.Text("MAT:", size=(4, 1)), sg.InputText(key='MAT', size=(4, 1)),
        ],
        [
            sg.Text("Real Respect Percent:", size=(18, 1)), sg.InputText(key='R_PERCENT',
                                                                         size=(4, 1), default_text="25"),
        ],
        [
            sg.Text("Real Efficiency Percent:", size=(18, 1)), sg.InputText(key='E_PERCENT',
                                                                            size=(4, 1), default_text="25"),
        ],
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
            sg.InputText(key='OUTPUTDATA', size=(30, 1), default_text='output.xlsx'),
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
                         reroute_stdout=True, size=(80, 30),
                         font="Courier",
                         default_text="Info:\n"
                                      "1. DO NOT START GENERATION WHEN YOUR OUTPUT FILE IS OPEN\n"
                                      "2. INPUT AND OUTPUT FILES MUST BE .XLSX FORMAT\n"
                                      "3. T - TANK, C - CONSUMPTION, R - RESPECT, E - EFFICIENCY\n"
                                      "4. Percents Up shows how much higher the value can be\n"
                                      "5. Percents Down shows how much lower the value can be\n"
                                      "6. VAT - versality(avatar characteristics)\n"
                                      "7. MAT - mastery (avatar characteristics)\n"),
        ],
        ]
    window_out = sg.Window('Car Generate', layout)
    return window_out


def transformType(car_type_in):
    if car_type_in == "Type A":
        car_type_out = TypeCar.typeA
    elif car_type_in == "Type B":
        car_type_out = TypeCar.typeB
    elif car_type_in == "Type C":
        car_type_out = TypeCar.typeC
    else:
        car_type_out = TypeCar.typeD

    return car_type_out


def transformRare(rare):
    if rare == "Classic":
        car_rarity = RarityCar.classic
    elif rare == "Rare":
        car_rarity = RarityCar.rare
    elif rare == "Epic":
        car_rarity = RarityCar.epic
    elif rare == "Legendary":
        car_rarity = RarityCar.legendary
    else:
        car_rarity = RarityCar.insane

    return car_rarity


def checkPercents(values_window):
    if not (values_window["UTSPREAD"].isdigit() and
            values_window["UCSPREAD"].isdigit() and
            values_window["URSPREAD"].isdigit() and
            values_window["UESPREAD"].isdigit() and
            values_window["DTSPREAD"].isdigit() and
            values_window["DCSPREAD"].isdigit() and
            values_window["DRSPREAD"].isdigit() and
            values_window["DESPREAD"].isdigit()):
        return True
    else:
        return False


def getData(file):
    excel = pd.ExcelFile(file)
    dataframe = excel.parse("data")

    TankData = []
    ConsumptionData = []
    RespectData = []
    EfficiencyData = []
    PricesData = []

    for string in range(4):
        TankData.append([round(elem, 2) for elem in dataframe.iloc[string]])
        ConsumptionData.append([round(elem, 2) for elem in dataframe.iloc[string+5]])
        RespectData.append([round(elem, 2) for elem in dataframe.iloc[string+10]])
        EfficiencyData.append([round(elem, 4) for elem in dataframe.iloc[string+15]])
        PricesData.append([round(elem, 0) for elem in dataframe.iloc[string + 20]])

    TankData = np.array(TankData)
    ConsumptionData = np.array(ConsumptionData)
    RespectData = np.array(RespectData)
    EfficiencyData = np.array(EfficiencyData)
    PricesData = np.array(PricesData)
    return TankData, ConsumptionData, RespectData, EfficiencyData, PricesData


def info():
    print("================================================================================")
    print("    Info:")
    print("    1. DO NOT START GENERATION WHEN YOUR OUTPUT FILE IS OPEN")
    print("    2. INPUT AND OUTPUT FILES MUST BE .XLSX FORMAT")
    print("    3. T - TANK, C - CONSUMPTION, R - RESPECT, E - EFFICIENCY")
    print("    4. Percents Up shows how much higher the value can be")
    print("    5. Percents Down shows how much lower the value can be")
    print("    6. VAT - versality (avatar characteristics)")
    print("    7. MAT - mastery (avatar characteristics)")
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
                print("ERROR: something wrong in percents!")

            elif values["SPREADDATA"] == '':
                print("ERROR: no data of spread")

            elif not values["CARCOUNT"].isdigit():
                print("ERROR: count error")

            else:
                car_list = []
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

                    Car = generateCar(car_type, car_rare, ut_spread, uc_spread, ur_spread, ue_spread,
                                      dt_spread, dc_spread, dr_spread, de_spread, data_file)

                    Car.max_distance = Car.getMaxDistance()

                    Car.R_percent = int(values["R_PERCENT"])
                    Car.respect_real = Car.getRealRespect()

                    Car.E_percent = int(values["E_PERCENT"])
                    Car.efficiency_real = Car.getRealEfficiency()

                    Car.VAT = int(values["VAT"])
                    Car.MAT = int(values["MAT"])

                    Car.respect = Car.getRespect()
                    Car.efficiency = Car.getEfficiency()

                    Car.earning_base = Car.getBaseEarning()
                    Car.earning_real = Car.getRealEarning()

                    Car.occupation = Car.getOccupation()

                    car_list.append(Car)

                    print(i+1, ". Type:        ", Car.getTypeName())
                    print(i+1, ". Rarity:      ", Car.getRarityName())
                    print(i+1, ". Tank:        ", Car.tank_base)
                    print(i+1, ". Consumption: ", Car.consumption_base)
                    print(i+1, ". Respect:     ", Car.respect_base)
                    print(i+1, ". Efficiency:  ", Car.efficiency_base)
                    print("======================================")
                out_data = pd.DataFrame([vars(car) for car in car_list])

                try:
                    out_data.to_excel(values['OUTPUTDATA'], index=False, header=True)
                    print("SUCCESS: Data saved")
                except PermissionError:
                    print("ERROR: May be you don't close your output file before generating")
                    info()
