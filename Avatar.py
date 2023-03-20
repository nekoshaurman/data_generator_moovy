import pandas as pd
import random
import enum


class TypeAvatar(enum.Enum):
    driver = 0
    technician = 1
    ecologist = 2


class TestAvatar:
    def __init__(self, type_of_avatar, level):
        self.type = type_of_avatar  # Driver, Technician, Ecologist
        self.level = level  # 1 - 25

        self.versality_base = None
        self.fame_base = None
        self.mastery_base = None

        self.versality_real = None
        self.fame_real = None
        self.mastery_real = None

        self.versality = None
        self.fame = None
        self.mastery = None

        self.talents = None

    def getTypeDigit(self):
        return self.type.value

    def getTypeName(self):
        return self.type.name


def getAvatarData(file):
    excel = pd.ExcelFile(file)
    dataframe = excel.parse("data")
    Data = []
    Talents = []

    # Get characters characteristics Versality, Fame, Mastery, Range
    BasicData = [round(elem, 1) for elem in dataframe.iloc[26, 1:5]]
    # BasicData.pop()
    DriverData = [round(elem, 1) for elem in dataframe.iloc[27, 1:5]]
    TechnicianData = [round(elem, 1) for elem in dataframe.iloc[28, 1:5]]
    EcologistData = [round(elem, 1) for elem in dataframe.iloc[29, 1:5]]
    TalentsV = dataframe.iloc[32, 1:5]
    TalentsM = dataframe.iloc[33, 1:5]
    TalentsF = dataframe.iloc[34, 1:5]

    Data.append(BasicData)
    Data.append(DriverData)
    Data.append(TechnicianData)
    Data.append(EcologistData)
    Talents.append(list(map(float, TalentsV.tolist())))
    Talents.append(list(map(float, TalentsM.tolist())))
    Talents.append(list(map(float, TalentsF.tolist())))

    return Data, Talents


def upByLevel(avatar: TestAvatar, avatarData):
    ups = avatar.level
    for up in range(ups):
        avatar.versality_real = avatar.versality_real * avatarData[0][3]
        avatar.fame_real = avatar.fame_real * avatarData[0][3]
        avatar.mastery_real = avatar.mastery_real * avatarData[0][3]
    return avatar


def upByTalents(avatar: TestAvatar, talentsData):
    save_talents = []
    talents = {
        'Versality': 0,
        'Mastery': 0,
        'Fame': 0,
        'Wheelspins': 0,
        'Lottery': 0,
        'Lootbox': 0,
        'Innitial Sale': 0,
        'Maintance': 0,
        'Consumption': 0,
    }

    max_level = 3
    upgrade_points = avatar.level // 5
    avatar.versality = avatar.versality_real
    avatar.mastery = avatar.mastery_real
    avatar.fame = avatar.fame_real

    while upgrade_points > 0:
        branch = random.choice(list(talents.keys()))
        if talents[branch] < max_level:
            talents[branch] += 1
            upgrade_points -= 1

    for talent, level in talents.items():
        if level > 0:
            if talent == 'Versality':
                for x in range(level):
                    avatar.versality = avatar.versality + avatar.versality * talentsData[0][x]
                if level == 3:
                    avatar.versality = avatar.versality + avatar.versality * talentsData[0][3]

            if talent == 'Mastery':
                for x in range(level):
                    avatar.mastery = avatar.mastery + avatar.mastery * talentsData[1][x]
                if level == 3:
                    avatar.mastery = avatar.mastery + avatar.mastery * talentsData[1][3]

            if talent == 'Fame':
                for x in range(level):
                    avatar.fame = avatar.fame + avatar.fame * talentsData[2][x]
                if level == 3:
                    avatar.fame = avatar.fame + avatar.fame * talentsData[2][3]

    for talent in talents.keys():
        if talents[talent] > 0:
            save_talents.append(talent + str(talents[talent]))

    return avatar, save_talents


def transformType(avatar_type):
    if avatar_type == 0:
        return TypeAvatar.driver
    elif avatar_type == 1:
        return TypeAvatar.technician
    else:
        return TypeAvatar.ecologist


def generateAvatar(avatarList, levelList, file):
    randomList = []
    for i in range(3):
        if avatarList[i] == 1:
            randomList.append(i)

    avatarType = random.choice(randomList)
    avatarLevel = random.randint(levelList[0], levelList[1])

    avatarData, talentsData = getAvatarData(file)
    # print(avatarData)
    # print(talentsData)

    avatarType = transformType(avatarType)

    avatar = TestAvatar(avatarType, avatarLevel)
    avatar.versality_base = avatarData[0][0]
    avatar.fame_base = avatarData[0][1]
    avatar.mastery_base = avatarData[0][2]

    versality_range = avatar.versality_base * \
                      avatarData[avatar.getTypeDigit() + 1][0] * \
                      avatarData[avatar.getTypeDigit() + 1][3]

    fame_range = avatar.fame_base * \
                 avatarData[avatar.getTypeDigit() + 1][1] * \
                 avatarData[avatar.getTypeDigit() + 1][3]

    mastery_range = avatar.mastery_base * \
                    avatarData[avatar.getTypeDigit() + 1][2] * \
                    avatarData[avatar.getTypeDigit() + 1][3]

    avatar.versality_real = (avatar.versality_base * avatarData[avatar.getTypeDigit() + 1][0]) * \
                            (1 + random.uniform((-1) * versality_range, versality_range))

    avatar.fame_real = (avatar.fame_base * avatarData[avatar.getTypeDigit() + 1][1]) * \
                       (1 + random.uniform((-1) * fame_range, fame_range))

    avatar.mastery_real = (avatar.mastery_base * avatarData[avatar.getTypeDigit() + 1][2]) * \
                          (1 + random.uniform((-1) * mastery_range, mastery_range))

    avatar = upByLevel(avatar, avatarData)

    avatar, talents = upByTalents(avatar, talentsData)

    avatar.talents = talents

    # print("Type:  ", avatar.type)
    # print("Level: ", avatar.level)
    # print("=====================")

    # print("VersB: ", avatar.versality_base)
    # print("VersR: ", avatar.versality_real)
    # print("Vers:  ", avatar.versality)
    # print("=====================")

    # print("FameB: ", avatar.fame_base)
    # print("FameR: ", avatar.fame_real)
    # print("Fame:  ", avatar.fame)
    # print("=====================")

    # print("MastB: ", avatar.mastery_base)
    # print("MastR: ", avatar.mastery_real)
    # print("Mast:  ", avatar.mastery)
    # print("=====================")

    # print(talents)

    return avatar


# if __name__ == '__main__':
    # avatar_types = [1, 1, 1]
    # avatar_level = [1, 25]
    # generateAvatar(avatar_types, avatar_level, "data.xlsx")
