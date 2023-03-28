import enum
from random import choice, uniform
import pandas as pd
import numpy as np


class TypeCar(enum.Enum):
    """
    enum типа авто
    """
    typeA = 0
    typeB = 1
    typeC = 2
    typeD = 3


class RarityCar(enum.Enum):
    """
    enum редкости авто
    """
    classic = 0
    rare = 1
    epic = 2
    legendary = 3
    insane = 4


class TestCar:
    """
    Класс авто
    """
    def __init__(self, type_of_car: TypeCar, rarity_of_car: RarityCar,
                 tank: float, consumption: float, respect: float, efficiency: float,
                 price: float):

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
        """
        Возвращает тип авто в виде enum числа
        """
        return self.type.value

    def getTypeName(self):
        """
        Возвращает тип авто в виде enum имени
        """
        return self.type.name

    def getRarityDigit(self):
        """
        Возвращает редкость авто в виде enum числа
        """
        return self.rarity.value

    def getRarityName(self):
        """
        Возвращает редкость авто в виде enum имени
        """
        return self.rarity.name

    def getMaxDistance(self):
        """
        Возвращает максимальную дистанцию (tank * 10 / consumption)
        """
        return self.tank_base * 10 / self.consumption_base

    def getRealRespect(self):
        """
        Возвращает respect уменьшая его на R_percent
        """
        return self.respect_base * (1 - self.R_percent / 100)

    def getRealEfficiency(self):
        """
        Возвращает efficiency уменьшая его на E_percent
        """
        return self.efficiency_base * (1 - self.E_percent / 100)

    def getRespect(self):
        """
        Возвращает respect с учетом versality
        """
        return self.respect_real * self.VAT

    def getEfficiency(self):
        """
        Возвращает efficiency с учетом mastery
        """
        return self.efficiency_real * self.MAT

    def getBaseEarning(self):
        """
        Возвращает базовый заработок (MD * Respect / 100 / 2)
        """
        return self.max_distance * self.respect / 100 / 2

    def getRealEarning(self):
        """
        Вовзвращает заработок (earning_base * efficiency)
        """
        return self.earning_base * self.efficiency

    def getOccupation(self):
        """
        Возвращает окупаемость (price / earning_real)
        """
        return self.price / self.earning_real


def generateCar(types_of_car: list, rarities_of_car: list,
                UTspread: int, UCspread: int, URspread: int, UEspread: int,
                DTspread: int, DCspread: int, DRspread: int, DEspread: int,
                file: str):
    """
    Генерирует параметры машины с помощью табличных параметров и возвращает объект типа TestCar
    """

    randomType = []
    randomRare = []

    for temp in range(4):
        if types_of_car[temp] == 1:
            randomType.append(temp)

    for temp in range(5):
        if rarities_of_car[temp] == 1:
            randomRare.append(temp)

    type_of_car = choice(randomType)
    type_of_car = transformType(type_of_car)

    rarity_of_car = choice(randomRare)
    rarity_of_car = transformRare(rarity_of_car)

    TankData, ConsumptionData, RespectData, EfficiencyData, PricesData = getData(file)

    Tank = round(uniform(
        (TankData[type_of_car.value][rarity_of_car.value] * (1 - DTspread / 100)),
        (TankData[type_of_car.value][rarity_of_car.value] * (1 + UTspread / 100))), 2)

    Consumption = round(uniform(
        (ConsumptionData[type_of_car.value][rarity_of_car.value] * (1 - DCspread / 100)),
        (ConsumptionData[type_of_car.value][rarity_of_car.value] * (1 + UCspread / 100))), 2)

    Respect = round(uniform(
        (RespectData[type_of_car.value][rarity_of_car.value] * (1 - DRspread / 100)),
        (RespectData[type_of_car.value][rarity_of_car.value] * (1 + URspread / 100))), 2)

    Efficiency = round(uniform(
        (EfficiencyData[type_of_car.value][rarity_of_car.value] * (1 - DEspread / 100)),
        (EfficiencyData[type_of_car.value][rarity_of_car.value] * (1 + UEspread / 100))), 4)

    Price = round(PricesData[type_of_car.value][rarity_of_car.value], 0)

    car = TestCar(type_of_car, rarity_of_car, Tank, Consumption, Respect, Efficiency, Price)

    return car


def getData(file: str):
    """
    Возвращает данные для генерации характеристик
    """
    excel = pd.ExcelFile(file)
    dataframe = excel.parse("data")  # название листа в файле .xlsx

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


def transformType(car_type_in: int):
    """
    Полученное число трансформирует в enum TypeCar объект и возвращает его
    """
    if car_type_in == 0:
        car_type_out = TypeCar.typeA
    elif car_type_in == 1:
        car_type_out = TypeCar.typeB
    elif car_type_in == 2:
        car_type_out = TypeCar.typeC
    else:
        car_type_out = TypeCar.typeD

    return car_type_out


def transformRare(rare: int):
    """
    Полученное число трансформирует в enum RarityCar объект и возвращает его
    """
    if rare == 0:
        car_rarity = RarityCar.classic
    elif rare == 1:
        car_rarity = RarityCar.rare
    elif rare == 2:
        car_rarity = RarityCar.epic
    elif rare == 3:
        car_rarity = RarityCar.legendary
    else:
        car_rarity = RarityCar.insane

    return car_rarity
