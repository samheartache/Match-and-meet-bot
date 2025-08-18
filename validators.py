def sex_validate(data: str | None):
    return data in ('Мужской', 'Женский')


def search_desire_validate(data: str | None):
    return data in ('Девушек', 'Парней', 'Не важно')


def searched_by_validate(data: str | None):
    return data in ('Девушкам', 'Парням', 'Не важно')


def name_validate(data: str | None):
    if data:
        return len(data) <= 20
    return False


def age_validate(data: str | None):
    if data:
        if data.isdigit():
            return 10 <= int(data) <= 100
        return False
    return False


def city_validate(data: str | None):
    if data:
        return len(data) <= 25 and data.isalpha()
    return False


def description_validate(data: str | None):
    if data:
        return len(data) <= 500
    return False


def photo_validate(data):
    return data

