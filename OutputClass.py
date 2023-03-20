from Car import TestCar
from Avatar import TestAvatar


class OutputClass:
    def __init__(self, car: TestCar, avatar: TestAvatar):
        self.type_of_car = car.type.name
        self.rare_of_car = car.rarity.name
        self.price_of_car = car.price

        self.tank = car.tank_base
        self.consumption = car.consumption_base
        self.respect_base = car.respect_base
        self.efficiency_base = car.efficiency_base

        self.md = car.max_distance
        self.R_percent = car.R_percent
        self.E_percent = car.E_percent
        self.respect_real = car.respect_real
        self.efficiency_real = car.efficiency_real

        self.respect = car.respect
        self.efficiency = car.efficiency

        self.earning_base = car.earning_base
        self.earning_real = car.earning_real
        self.occupation = car.occupation

        self.sep = None

        self.type_of_avatar = avatar.type.name
        self.level_of_avatar = avatar.level

        self.VAT_base = avatar.versality_base
        self.FAM_base = avatar.fame_base
        self.MAT_base = avatar.mastery_base

        self.VAT_real = avatar.versality_real
        self.FAM_real = avatar.fame_real
        self.MAT_real = avatar.mastery_real

        self.VAT = avatar.versality
        self.FAM = avatar.fame
        self.MAT = avatar.mastery

        self.talents = avatar.talents
