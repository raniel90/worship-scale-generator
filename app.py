import random
import datetime
import pandas as pd

musicians = {
  'Baterista': ['Roosevelt', 'Deco', 'Raniel', 'Ary'],
  'Baixista': ['Nona', 'Douglas', 'Edson', 'Jonatas'], 
  'Guitarrista': ['Fernando', 'Eraldo', 'Afonso'],
  'Violonista': ['Joel', 'Zeik', 'Belle', 'Fagner'],
  'Tecladista': ['Flávio', 'Giba', 'Fábio'],
  'Percussionista': ['Natal'],
  'Vocal Soprano': ['Kátia', 'Flavinha', 'Julinha', 'Paty', 'Geninha', 'Sandra'],
  'Vocal Contralto': ['Betânia', 'Helen', 'Cinthia', 'Belle', 'Dani'],
  'Líder': ['Jonatas','Vinícius', 'Zeik', 'Flávio'],
  'Vocal Homem': ['Vinícius', 'Kaio', 'Zeik']
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
    'Vocal Soprano': 'Juventude',
    'Vocal Contralto': 'Juventude',
    'Vocal Homem': 'Juventude',
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
      last_index = len(dates[date]) -1
      sunday_five_week = dates[date][last_index]

      dates_five_weeks[sunday_five_week] = True
  
  return dates_five_weeks

def shuffle_musicians():
  for key in indexes:
    if indexes[key] == len(musicians[key]) -1:
      random.shuffle(musicians[key])

def remove_duplicates(df, item):
  global indexes
  df_last = None
  duplicated_musicians = {}
  last_idx = len(df.index) -1

  if (last_idx != -1):
    df_last = df.loc[last_idx]

    for df_attr in df_last:
      for attr in item:

        while df_attr == item[attr] and len(musicians[attr]) > 1:
          indexes[attr] = get_next_index(musicians[attr], indexes[attr])
          item[attr] = musicians[attr][indexes[attr]]

    for instrument in item:
      if instrument != 'Data':
        musician = item[instrument]

        if musician not in duplicated_musicians:
          duplicated_musicians[musician] = []

        duplicated_musicians[musician].append(instrument)

    
    for musician in duplicated_musicians:
      if len(duplicated_musicians[musician]) > 1:
        instrument_duplicated = duplicated_musicians[musician][0]
        old_index = indexes[instrument_duplicated]

        while old_index == indexes[instrument_duplicated]:
          indexes[instrument_duplicated] = get_next_index(musicians[instrument_duplicated], indexes[instrument_duplicated])
          item[instrument_duplicated] = musicians[instrument_duplicated][indexes[instrument_duplicated]]
    
    #Zeik Rules
    if item['Líder'] == 'Zeik':
      item['Violonista'] = 'Zeik'
    
    #Flávio Rules
    if item['Líder'] == 'Flávio':
      item['Tecladista'] = 'Flávio'
    
    #Jonatas Rules
    while item['Líder'] == 'Jonatas' and item['Baixista'] == 'Jonatas':
      indexes['Baixista'] = get_next_index(musicians['Baixista'], indexes['Baixista'])
      item['Baixista'] = musicians['Baixista'][indexes['Baixista']]

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

    shuffle_musicians()

    for musician_type in musicians:
      indexes[musician_type] = get_next_index(musicians[musician_type], indexes[musician_type])

    date += datetime.timedelta(7)

  return df
    

df = get_gigs()
df.to_csv("Escala de músicos.csv")