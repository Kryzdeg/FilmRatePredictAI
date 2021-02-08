from requests_html import HTMLSession
import re
session = HTMLSession()


def get_movie_info(link):
    r = session.get(link)
    film = dict()


    rate = r.html.find(".filmRating__rateValue", first=True)
    count_rate = r.html.find(".filmRating__count", first=True)
    film["rate"] = rate.text
    film["count_rate"] = count_rate.text.replace("\nocen", "").replace(" ", "")
    info = r.html.find(".filmPosterSection__info")[0].find(".filmInfo__info")
    film["director"] = info[0].text.replace(" ", "_")
    film["genre"] = info[2].text.replace(" / ", "_")
    film["production"] = info[3].text.replace(" / ", "_")
    infos = r.html.find(".FilmOtherInfoSection")[0].find(".filmOtherInfoSection__group")[0].find(".filmInfo__group")
    for info in infos:
        for header in info.find(".filmInfo__header"):
            if header.text == "budżet":
                film["budget"] = info.find(".filmInfo__info")[1].text.replace("$", "").replace(" ", "")
            elif header.text == "data produkcji":
                film["date"] = info.find(".filmInfo__info", first=True).text



    print(film)
    return film


def filmweb_scrap():
    films = []
    file_train = open("train.txt", "w+")
    base_page = "https://www.filmweb.pl/films/search"
    current_page = ""
    # while True:
    for i in range(10):
        r = session.get(base_page + current_page)
        print(r.html)
        for l in r.html.find(".filmPreview__titleDetails"):
            for h in l.absolute_links:
                film = get_movie_info(h)
                films.append(film)
                file_train.write(f"{film['rate']} | count_rate:{film['count_rate']} director_{film['director']} genre_{film['genre']} production_{film['production']} budget:{film['budget']} {film['date']}")

        try:
            current_page = r.html.find(".pagination__item--next", first=True).links.pop()
        except Exception as e:
            break

    file_train.close()
    print(films, "\n", len(films))
    # print(links, "\n", len(links))


filmweb_scrap()
# get_movie_info("https://www.filmweb.pl/film/Mroczny+Rycerz-2008-236351")
