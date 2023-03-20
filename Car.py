import enum
import random
import pandas as pd
import numpy as np


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
        return self.respect_real * self.VAT

    def getEfficiency(self):
        return self.efficiency_real * self.MAT

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
