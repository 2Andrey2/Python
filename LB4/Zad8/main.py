import pandas




def print_names(names):
    for i, name in enumerate(names, 1):
        print(str(i) + '.', name.split(',')[0])

data = pandas.read_csv('countries.csv', ';')
sorted_by_area = data.sort_values(by='area', ascending=False)

print('The largest countries')
print_names(sorted_by_area.head(10).name)
print('\nThe smallest countries')
print_names(reversed(list(sorted_by_area.tail(10).name)))

french_speaking = data.where(pandas.Series(['French' in str(d)
                                            for d in data.languages])
                             ).name.dropna()
print('\nFrench-speaking countries')
print_names(french_speaking)

island = data.where(data.borders.isnull()).name.dropna()
print('\nIsland countries')
print_names(island)

southern = data.where(pandas.Series([float(str(d).split(',')[0]) < 0
                                    for d in data.latlng])
                      ).name.dropna()
print('\nCountries in the Southern Hemisphere')
print_names(southern)

print('\n\nCountries by first letters')
for i, group in data.groupby([d[0] for d in data.name]):
    print(i + ': ')
    print_names(group.name)
    print()


names = pandas.Series([d.split(',')[0] for d in data.name])
names.name = 'name'
lat, lng = zip(*[d.split(',')
                 if isinstance(d, str)  # проверка на случай, если latlng = nan
                 else ['nan', 'nan']     # без неё 'nan'.split(',')
                 for d in data.latlng])  # возвращает ['nan'] и zip не работает
lat, lng = map(pandas.Series, (lat, lng))
lat.name = 'latitude'
lng.name = 'longitude'
for_export = pandas.concat([names,
                            data[['capital', 'area', 'currency']],
                            lat,
                            lng],
                           axis=1)
with pandas.ExcelWriter('exported.xls') as excel_writer:
    for_export.to_excel(excel_writer)
