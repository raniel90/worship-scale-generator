import random
import datetime
import pandas as pd

musicians = {
  'baterista': ['Deco', 'Raniel', 'Roosevelt', 'Mago', 'Ary', 'Gustavo'],
  'baixista': ['Nona', 'Douglas', 'Edson', 'Eraldo', 'Jonathas'], 
  'guitarrista': ['Eraldo', 'Fernando', 'Afonso'],
  'violonista': ['Zeik', 'Joel', 'Flávio', 'Fagner', 'Paty'],
  'tecladista': ['Flávio', 'Giba', 'Fábio'],
  'percussionista': ['Natal']
}

indexes = {}

for musician_type in musicians:
  indexes[musician_type] = 0

def get_first_sunday():
  d = datetime.date.today()

  while d.weekday() != 6:
    d += datetime.timedelta(1)
  
  return d


def get_next_index(items, indexes):
  new_items = items

  if len(items) == indexes + 1:
      indexes = 0
  else:
    indexes += 1
  
  return indexes


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

    for musician_type in musicians:
      if df_last[musician_type] == item[musician_type]:
        indexes[musician_type] = get_next_index(musicians[musician_type], indexes[musician_type])
        item[musician_type] = musicians[musician_type][indexes[musician_type]]


    for instrument in item:
      if instrument != 'Data':
        musician = item[instrument]

        if musician not in duplicated_musicians:
          duplicated_musicians[musician] = []  

        duplicated_musicians[musician].append(instrument)

    
    for musician in duplicated_musicians:
      if len(duplicated_musicians[musician]) > 1:
        instrument_duplicated = duplicated_musicians[musician][0]
        indexes[musician_type] = get_next_index(musicians[musician_type], indexes[musician_type])
        item[musician_type] = musicians[musician_type][indexes[musician_type]]


  return item


def get_gigs():
  gigs = {}
  global indexes
  date = get_first_sunday()
  reference_year = date.year

  df = pd.DataFrame({})

  while date.year == reference_year:
    formatted_date = f"{date.day}/{date.month}/{date.year}"

    item = {
      'Data': formatted_date
    }

    for musician_type in musicians:
      item[musician_type] = musicians[musician_type][indexes[musician_type]]

    item = remove_duplicates(df, item)
    df = df.append(item, ignore_index=True)

    shuffle_musicians()

    for musician_type in musicians:
      indexes[musician_type] = get_next_index(musicians[musician_type], indexes[musician_type])

    date += datetime.timedelta(7)

  return df
    

df = get_gigs()
print(df)
df.to_excel("Escala de músicos.xlsx")