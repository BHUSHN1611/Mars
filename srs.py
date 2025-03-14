import pickle
import pandas as pd
import requests

series_dict = pickle.load( open("series_dict.pkl",'rb'))
series = pd.DataFrame(series_dict)
series_similarity = pickle.load(open("series_similarity.pkl", "rb"))

def fetch_serieposter(serie_name):
    response = requests.get(
        "https://api.themoviedb.org/3/search/tv?api_key=621f11a3e889718c83d29d87d900be79&query={}".format(
            serie_name))
    data = response.json()
    # return data['results'][0]['poster_path']

    return "https://image.tmdb.org/t/p/w500"+data['results'][0]['poster_path']

def fetch_serie_rating(serie_name):
    response = requests.get(
        "https://api.themoviedb.org/3/search/tv?api_key=621f11a3e889718c83d29d87d900be79&query={}".format(
            serie_name))
    data = response.json()
    rating_conv = float(data["results"][0]["vote_average"])

    return rating_conv


def series_recommend(serie):

    flag = False
    for i in series['name']:
        if (serie == i):
            flag = True
            break
        else:
            flag = False

    if (flag == True):
        serie_index = series[series['name'] == serie].index[0]
        distances = series_similarity[serie_index]
        series_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        rec_series_id = []

        rec_series = []
        series_poster_path = []
        conv = []
        rec_serie_rating = []


        for i in series_list:
            rec_series_id.append(series.iloc[i[0]].name)
            # serie_id = series.iloc[i[0]].id

        if (rec_series_id):
            for i in rec_series_id:
                rec_series.append(series['name'][i])

            for i in rec_series:
                conv.append(i.replace(" ", "+"))


            for i in conv:
                series_poster_path.append(fetch_serieposter(i))
                rec_serie_rating.append(fetch_serie_rating(i))


            return rec_series,series_poster_path,rec_serie_rating
    else:
        print("series is not present in dataset or their is spelling mistake")





