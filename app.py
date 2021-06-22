import random
import datetime
import pandas as pd

musicians = {
    'Baterista': ['Roosevelt', 'Deco', 'Raniel', 'Gustavo'],
    'Baixista': ['Douglas', 'Nona', 'Edson', 'Jonatas'],
    'Guitarrista': ['Fernando', 'Guga', 'Afonso'],
    'Violonista': ['Joel', 'Zeik', 'Belle', 'Fagner'],
    'Tecladista': ['Flávio', 'Giba', 'Fábio'],
    'Percussionista': ['Natal'],
    'Vocal 1': ['Kátia', 'Flavinha', 'Julinha', 'Paty'],
    'Vocal 2': ['Betânia', 'Helen', 'Cinthia', 'Belle'],
    'Vocal 3': ['Sandra', 'Dani', 'Helena'],
    'Vocal 4': ['Vinícius', 'Kaio', 'Zeik'],
    'Líder': ['Flávio', 'Jonatas', 'Vinícius', 'Zeik']
}

indexes = {}

for musician_type in musicians:
    indexes[musician_type] = 0


def get_youth_musicians(date):
    data = {
        'Baterista': 'Juventude',
        'Baixista': 'Juventude',
        'Guitarrista': 'Juventude',
        'Violonista': 'Juventude',
        'Tecladista': 'Juventude',
        'Percussionista': 'Juventude',
        'Vocal 1': 'Juventude',
        'Vocal 2': 'Juventude',
        'Vocal 3': 'Juventude',
        'Vocal 4': 'Juventude',
        'Líder': 'Juventude'
    }

    data['Data'] = date

    return data


def get_first_sunday():
    d = datetime.date.today()

    while d.weekday() != 6:
        d += datetime.timedelta(1)

    return d


def get_next_index(items, indexes):
    if len(items) == indexes + 1:
        indexes = 0
    else:
        indexes += 1

    return indexes


def get_sundays_fifth_week():
    dates = {}
    dates_five_weeks = {}
    today = datetime.date.today()
    d = datetime.datetime.strptime(f"{today.year}-01-01", '%Y-%m-%d')

    while d.year == today.year:
        if d.weekday() == 6:

            if d.month not in dates:
                dates[d.month] = []

            dates[d.month].append(f"{d.day}/{d.month}/{d.year}")

        d += datetime.timedelta(1)

    for date in dates:
        if len(dates[date]) == 5:
            last_index = len(dates[date]) - 1
            sunday_five_week = dates[date][last_index]

            dates_five_weeks[sunday_five_week] = True

    return dates_five_weeks


def remove_duplicates(df, item):
    global indexes
    df_last = None
    last_idx = len(df.index) - 1

    if (last_idx != -1):
        df_last = df.loc[last_idx]

        for df_attr in df_last:
            for attr in item:

                while df_attr == item[attr] and len(musicians[attr]) > 1:
                    indexes[attr] = get_next_index(
                        musicians[attr], indexes[attr])
                    item[attr] = musicians[attr][indexes[attr]]

        # Jonatas Rules
        while item['Líder'] == 'Jonatas' and item['Baixista'] == 'Jonatas':
            indexes['Líder'] = get_next_index(
                musicians['Líder'], indexes['Líder'])
            item['Líder'] = musicians['Líder'][indexes['Líder']]

        # Zeik Rules
        if item['Líder'] == 'Zeik':
            item['Violonista'] = 'Zeik'

        while item['Líder'] == 'Zeik' and item['Vocal 4'] == 'Zeik':
            indexes['Vocal 4'] = get_next_index(
                musicians['Vocal 4'], indexes['Vocal 4'])
            item['Vocal 4'] = musicians['Vocal 4'][indexes['Vocal 4']]

        # Flávio Rules
        if item['Líder'] == 'Flávio':
            item['Tecladista'] = 'Flávio'

        # Fabio Rules
        if item['Tecladista'] == 'Fábio':
            item['Vocal 2'] = 'Belle'

        while item['Tecladista'] != 'Fábio' and item['Vocal 2'] == 'Belle':
            indexes['Vocal 2'] = get_next_index(
                musicians['Vocal 2'], indexes['Vocal 2'])
            item['Vocal 2'] = musicians['Vocal 2'][indexes['Vocal 2']]

        while item['Tecladista'] != 'Fábio' and item['Violonista'] == 'Belle':
            indexes['Violonista'] = get_next_index(
                musicians['Violonista'], indexes['Violonista'])
            item['Violonista'] = musicians['Violonista'][indexes['Violonista']]

        while item['Líder'] == 'Vinícius' and item['Vocal 4'] == 'Vinícius':
            indexes['Vocal 4'] = get_next_index(
                musicians['Vocal 4'], indexes['Vocal 4'])
            item['Vocal 4'] = musicians['Vocal 4'][indexes['Vocal 4']]

    return item


def get_gigs():
    global indexes
    date = get_first_sunday()
    reference_year = date.year
    sunday_five_week = get_sundays_fifth_week()

    df = pd.DataFrame({})

    while date.year == reference_year:
        formatted_date = f"{date.day}/{date.month}/{date.year}"

        item = {
            'Data': formatted_date
        }

        for musician_type in musicians:
            item[musician_type] = musicians[musician_type][indexes[musician_type]]

        item = remove_duplicates(df, item)

        if item['Data'] in sunday_five_week:
            item = get_youth_musicians(item['Data'])

        df = df.append(item, ignore_index=True)

        for musician_type in musicians:
            indexes[musician_type] = get_next_index(
                musicians[musician_type], indexes[musician_type])

        date += datetime.timedelta(7)

    return df


df = get_gigs()
today = datetime.date.today()

df.insert(0, 'DataTemp', df['Data'])
df = df.drop(columns=['Data']).copy()
df = df.rename(columns={'DataTemp': 'Data'}).copy()

# df.to_csv(f"Escala de músicos {today.year}.csv", index=False)
df.to_excel(f"Escala de músicos {today.year}.xls", index=False)
