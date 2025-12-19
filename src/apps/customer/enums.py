from enum import Enum


class CustomerGenderEnums(str, Enum):
    FEMALE = 'female'
    MALE = 'male'


class CountryIsoEnums(str, Enum):
    BELARUS = 'BY'
    RUSSIA = 'RU'
