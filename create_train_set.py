import csv, json
import regex as re

langs = {}
countries = {}
reg = r"'name': \"((\s?\p{posix_alnum}*[,&\.\(\)/-]?\s?)+)''?((\s?\p{posix_alnum}*[\?',&\.\(\)/-]?\s?)+)'?'?\""
reg2 = r"'name': '((\s?\p{posix_alnum}*[,\.&/-]?\s?)+)\"((\s?\p{posix_alnum}*[\.&/-]?\s?)+)\"?((\s?\p{posix_alnum}*[,\.&/-]?\s?)+)'"


with open("movies_metadata.csv", "r") as film_db:
    reader = csv.DictReader(film_db)
    with open("train_set.txt", "w+") as train_file:
        for i, row in enumerate(reader):

            if not row['original_language'] in langs.keys():
                langs[row['original_language']] = len(langs) + 1

            countries_list = [country['iso_3166_1'] for country in json.loads(re.sub(reg, '\'name\': "\g<1>\g<3>"', row['production_countries']).replace("'", '"'))]

            for country in countries_list:
                if not country in countries.keys():
                    countries[country] = len(countries) + 1
            
            try:
                companies = json.loads(row['production_companies'].replace("'", '"'))
                # print(companies)
            except Exception as e:
                companies_str = re.sub(reg, '\'name\': "\g<1>\g<3>"', row['production_companies'])
                companies_str = re.sub(reg, '\'name\': "\g<1>\g<3>"', companies_str)
                companies_str = re.sub(reg2, '\'name\': \'\g<1>\g<3>\'', companies_str)
                companies = json.loads(companies_str.replace("'", '"').replace("\\xa0", ""))

            line = f"""{row['vote_average']} | adult:{1 if row['vote_average'] == "True" else 0}
budget:{float(row['budget'])}
genres:{sum([int(genre['id']) for genre in json.loads(row['genres'].replace("'", '"'))])}
original_language:{langs[row['original_language']]}
popularity:{float(row['popularity'])}
production_companies:{sum([company['id'] for company in companies])}
production_countries:{sum([countries[country] for country in countries_list])}
release_date:{row['release_date'][:4]}
revenue:{row['revenue']}
runtime:{row['runtime']}
vote_count:{row['vote_count']}"""

            train_file.write(line.replace("\n", " ") + "\n")
