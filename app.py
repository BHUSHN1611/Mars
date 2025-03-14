import streamlit as st  # front-end framework
import pickle  # use for serialization - use to convert data structure into pkl form
import pandas as pd
import requests  # use for api request
from openai import OpenAI
import re
# internal modules
import cssload
from srs import series_recommend
from trendingmoviesdata import copyoftrending
# for reducing top extra space
st.set_page_config(layout="wide")
st.title("☄️ MARS")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.9rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
cssload.load_css()

# main file conversion to pkl for movies
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# main file conversion to pkl for series
series_dict = pickle.load( open("series_dict.pkl",'rb'))
series = pd.DataFrame(series_dict)
series_similarity = pickle.load(open("series_similarity.pkl", "rb"))

# It makes the poster href link and other can also be retried
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=621f11a3e889718c83d29d87d900be79&language=en-US'.format(
            movie_id))
    data = response.json()


    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def fetch_movie_rating(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=621f11a3e889718c83d29d87d900be79&language=en-US'.format(
            movie_id))
    r_data = response.json()
    return r_data['vote_average']

# main function bhai of movie recommendation
def recommend(movie):
    flag = False
    for i in movies['title']:
        if (movie == i):
            flag = True
            break
        else:
            flag = False

    if flag == True:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        rec_movies = []
        rec_movies_poster = []
        rec_movies_rating = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            rec_movies.append(movies.iloc[i[0]].title)
            # poster fetching and rating
            rec_movies_poster.append(fetch_poster(movie_id))
            rec_movies_rating.append(fetch_movie_rating(movie_id))


        if (rec_movies):
            return rec_movies, rec_movies_poster , rec_movies_rating

    else:
        st.write("Movie is not present in dataset or their is spelling mistake")

# gui continues

def set_page(page_name):
    st.session_state.page = page_name

# Create horizontal navbar with buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Trending", type="primary", use_container_width=True):
        set_page("Trending")
with col2:
    if st.button("Movies", type="primary", use_container_width=True):
        set_page("Movies")
with col3:
    if st.button("Series", type="primary", use_container_width=True):
        set_page("Series")
with col4:
    if st.button("Ai recommendation", type="primary", use_container_width=True):
        set_page("Ai recommendation")
#
promptf = ""
def prompt_gen(content_choice,content_name):
    global promptf
    if content_choice == "movies":
        promptf = f"Recommend five movies that are highly similar to {content_name} based on genres, themes, storytelling style, and core narrative elements. Provide the output strictly in the following format as a plain string: movies = [ Movie1, Movie2, Movie3, Movie4, Movie5 ] with no extra text, explanations, or formatting."
    elif content_choice == "series":
        promptf = f"Recommend five series that are highly similar to {content_name} based on genres, themes, storytelling style, and core narrative elements. Provide the output strictly in the following format as a plain string: movies = [ Movie1, Movie2, Movie3, Movie4, Movie5 ] with no extra text, explanations, or formatting."
    else:
        promptf = "Invalid choice! Please enter 'movies' or 'series'."
    return promptf
def rtr_rs():
    promptff = promptf
    return promptff

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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",
# ) isko ander bhj diya hai
def ai_rec():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    prompt = rtr_rs()
    # API request
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        extra_body={},
        model="deepseek/deepseek-r1:free",
        messages=[{"role": "user", "content": prompt}],
    )

    # Print response
    airecommeded_movieseries_str = "".join(completion.choices[0].message.content)


    # Extract text inside brackets
    match = re.search(r"\[(.*?)\]", airecommeded_movieseries_str)
    movies_list = []

    if match:
        movies_string = match.group(1)  # Get content inside brackets
        movies_list = [movie.strip() for movie in movies_string.split(",")]  # Split into a list

    aiconv = []
    for i in movies_list:
        aiconv.append(i.replace(" ", "+"))

    ai_posurl = []
    ai_rating = []
    titles = []

    for i in aiconv:
        ai_posurl.append(fetch_ai_movie_series_poster(i))
        ai_rating.append(fetch_ai_movie_serie_rating(i))
        titles.append(fetch_ai_movie_serie_title(i))

    return ai_posurl,ai_rating,titles

def fetch_ai_movie_series_poster(aimname):
    response = requests.get(
        "https://api.themoviedb.org/3/search/tv?api_key=621f11a3e889718c83d29d87d900be79&query={}".format(aimname))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['results'][0]['poster_path']
def fetch_ai_movie_serie_rating(ainame):
    response = requests.get(
        "https://api.themoviedb.org/3/search/tv?api_key=621f11a3e889718c83d29d87d900be79&query={}".format(ainame))
    data = response.json()
    ai_rating_conv = float(data["results"][0]["vote_average"])
    return ai_rating_conv
def fetch_ai_movie_serie_title(ainame):
    response = requests.get(
        "https://api.themoviedb.org/3/search/tv?api_key=621f11a3e889718c83d29d87d900be79&query={}".format(ainame))
    data = response.json()
    ai_title = data["results"][0]["original_name"]
    return ai_title

# Get popular movies for initial display.
def display_popular_movies():
    try:

        popular_movies_response = requests.get("https://api.themoviedb.org/3/trending/movie/day?api_key=621f11a3e889718c83d29d87d900be79&language=en-US")
        # popular_movies_response="https://api.themoviedb.org/3/trending/movie/week?api_key=621f11a3e889718c83d29d87d900be79"
        popular_movies_response_data = popular_movies_response.json()
        st.header("Trending Movies",divider = 'red') # title
        trending_movie_poster = []
        trending_movies_title = []
        trending_movies_rating = []

        for i in range(0,20):
            trending_movie_poster.append(fetch_poster(popular_movies_response_data["results"][i]["id"])) ## for id going to get the poster url
            trending_movies_title.append(popular_movies_response_data["results"][i]["title"])# for title
            trending_movies_rating.append(popular_movies_response_data["results"][i]["vote_average"]) # for rating


        # def display_frame_popular_movies(poster_link):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f""" <div class='movie-card'>
                        <img src="{trending_movie_poster[0]}" style="width:100%; border-radius:4px;">
                        <div class='movie-title'>{trending_movies_title[0]}</div>
                        <div class='movie-info'>
                            Rating: {round(trending_movies_rating[0],1)}/10
                        </div>
                    </div>""",unsafe_allow_html=True )
        with col2:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[1]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[1]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[1],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[2]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[2]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[2],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[3]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[3]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[3],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col5:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[4]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[4]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[4],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
           st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[5]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[5]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[5],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[6]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[6]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[6],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[7]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[7]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[7],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[8]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[8]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[8],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col5:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[9]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[9]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[9],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[10]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[10]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[10],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[11]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[11]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[11],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[12]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[12]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[12],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[13]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[13]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[13],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col5:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[14]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[14]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[14],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)

        col1, col2, col3, col4 , col5 = st.columns(5)
        with col1:
           st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[15]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[15]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[15],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[16]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[16]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[16],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[17]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[17]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[17],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[18]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[18]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[18],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
        with col5:
            st.markdown(f""" <div class='movie-card'>
                                <img src="{trending_movie_poster[19]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{trending_movies_title[19]}</div>
                                <div class='movie-info'>
                                    Rating: {round(trending_movies_rating[19],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    except:
        copyoftrending()


if "page" not in st.session_state:
    st.session_state.page = display_popular_movies()

# Display content based on selected page

if st.session_state.page == "Movies":
    st.title(f"{st.session_state.page} Page")
    selected_movie = st.selectbox(
        'Select the movies',
        movies['title'].values,
        index=None,
        placeholder='Search movie '
    )
    if st.button('Show Recommendation'):
        if (selected_movie):
            recommended_movie_names, recommended_movie_posters,recommended_movie_rating = recommend(selected_movie)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.markdown(f""" <div class='movie-card'>
                                            <img src="{recommended_movie_posters[0]}" style="width:100%; border-radius:4px;">
                                            <div class='movie-title'>{recommended_movie_names[0]}</div>
                                            <div class='movie-info'>
                                                Rating: {round(recommended_movie_rating[0],1)}/10
                                            </div>
                                        </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f""" <div class='movie-card'>
                                                            <img src="{recommended_movie_posters[1]}" style="width:100%; border-radius:4px;">
                                                            <div class='movie-title'>{recommended_movie_names[1]}</div>
                                                            <div class='movie-info'>
                                                                Rating: {round(recommended_movie_rating[1], 1)}/10
                                                            </div>
                                                        </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f""" <div class='movie-card'>
                                                            <img src="{recommended_movie_posters[2]}" style="width:100%; border-radius:4px;">
                                                            <div class='movie-title'>{recommended_movie_names[2]}</div>
                                                            <div class='movie-info'>
                                                                Rating: {round(recommended_movie_rating[2], 1)}/10
                                                            </div>
                                                        </div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f""" <div class='movie-card'>
                                                            <img src="{recommended_movie_posters[3]}" style="width:100%; border-radius:4px;">
                                                            <div class='movie-title'>{recommended_movie_names[3]}</div>
                                                            <div class='movie-info'>
                                                                Rating: {round(recommended_movie_rating[3], 1)}/10
                                                            </div>
                                                        </div>""", unsafe_allow_html=True)
            with col5:
                st.markdown(f""" <div class='movie-card'>
                                                            <img src="{recommended_movie_posters[4]}" style="width:100%; border-radius:4px;">
                                                            <div class='movie-title'>{recommended_movie_names[4]}</div>
                                                            <div class='movie-info'>
                                                                Rating: {round(recommended_movie_rating[4], 1)}/10
                                                            </div>
                                                        </div>""", unsafe_allow_html=True)
        else:
            st.text('No movies selected ')

elif st.session_state.page == "Series":
    st.title(f"{st.session_state.page} Page")
    selected_serie = st.selectbox(
        'select a series',
        series['name'].values,
        index=None,
        placeholder='Search a serie'
    )
    if st.button("Show Recommendation"):
        try:
            if (selected_serie):
                recommend_series_name,series_posterpath,series_rating  = series_recommend(selected_serie)
                col1,col2,col3,col4,col5  = st.columns(5)
                with col1:
                    st.markdown(f""" <div class='movie-card'>
                                                <img src="{series_posterpath[0]}" style="width:100%; border-radius:4px;">
                                                <div class='movie-title'>{recommend_series_name[0]}</div>
                                                <div class='movie-info'>
                                                    Rating: {round(series_rating[0], 1)}/10
                                                </div>
                                            </div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown(f""" <div class='movie-card'>
                                                                <img src="{series_posterpath[1]}" style="width:100%; border-radius:4px;">
                                                                <div class='movie-title'>{recommend_series_name[1]}</div>
                                                                <div class='movie-info'>
                                                                    Rating: {round(series_rating[1], 1)}/10
                                                                </div>
                                                            </div>""", unsafe_allow_html=True)
                with col3:
                    st.markdown(f""" <div class='movie-card'>
                                                                <img src="{series_posterpath[2]}" style="width:100%; border-radius:4px;">
                                                                <div class='movie-title'>{recommend_series_name[2]}</div>
                                                                <div class='movie-info'>
                                                                    Rating: {round(series_rating[2], 1)}/10
                                                                </div>
                                                            </div>""", unsafe_allow_html=True)
                with col4:
                    st.markdown(f""" <div class='movie-card'>
                                                                <img src="{series_posterpath[3]}" style="width:100%; border-radius:4px;">
                                                                <div class='movie-title'>{recommend_series_name[3]}</div>
                                                                <div class='movie-info'>
                                                                    Rating: {round(series_rating[3], 1)}/10
                                                                </div>
                                                            </div>""", unsafe_allow_html=True)
                with col5:
                    st.markdown(f""" <div class='movie-card'>
                                                                <img src="{series_posterpath[4]}" style="width:100%; border-radius:4px;">
                                                                <div class='movie-title'>{recommend_series_name[4]}</div>
                                                                <div class='movie-info'>
                                                                    Rating: {round(series_rating[4], 1)}/10
                                                                </div>
                                                            </div>""", unsafe_allow_html=True)
            else:
                st.text('No series selected')
        except:
            st.text("Index series index is out of bounds for similarity array.")

elif st.session_state.page == "Ai recommendation":
    st.title(f"{st.session_state.page} Page")
    ai_selcted_content_type = st.selectbox("Select the content type ,Movie or serie",
                                      ("movies","series"),index=None,placeholder='Select a serie/movie')
    ai_selctedai_selcted_content = st.text_input(label="Search a serie/movie", placeholder='Search a serie/movie')

    if st.button("Search"):
        # try:

        prompt_gen(ai_selcted_content_type,ai_selctedai_selcted_content)
        st.text("Loading.....")
        ai_rec_poster_link,ai_rec_rating,ai_rec_title = ai_rec()
        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.markdown(f""" <div class='movie-card'>
                           <img src="{ai_rec_poster_link[0]}" style="width:100%; border-radius:4px;">
                           <div class='movie-title'>{ai_rec_title[0]}</div>
                           <div class='movie-info'>
                               Rating: {round(ai_rec_rating[0], 1)}/10
                           </div>
                       </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f""" <div class='movie-card'>
                              <img src="{ai_rec_poster_link[1]}" style="width:100%; border-radius:4px;">
                              <div class='movie-title'>{ai_rec_title[1]}</div>
                              <div class='movie-info'>
                                  Rating: {round(ai_rec_rating[1], 1)}/10
                              </div>
                          </div>""", unsafe_allow_html=True)

        with col3:
            st.markdown(f""" <div class='movie-card'>
                              <img src="{ai_rec_poster_link[2]}" style="width:100%; border-radius:4px;">
                              <div class='movie-title'>{ai_rec_title[2]}</div>
                              <div class='movie-info'>
                                  Rating: {round(ai_rec_rating[2], 1)}/10
                              </div>
                          </div>""", unsafe_allow_html=True)

        with col4:
            st.markdown(f""" <div class='movie-card'>
                              <img src="{ai_rec_poster_link[3]}" style="width:100%; border-radius:4px;">
                              <div class='movie-title'>{ai_rec_title[3]}</div>
                              <div class='movie-info'>
                                  Rating: {round(ai_rec_rating[3], 1)}/10
                              </div>
                          </div>""", unsafe_allow_html=True)

        with col5:
            st.markdown(f""" <div class='movie-card'>
                              <img src="{ai_rec_poster_link[4]}" style="width:100%; border-radius:4px;">
                              <div class='movie-title'>{ai_rec_title[4]}</div>
                              <div class='movie-info'>
                                  Rating: {round(ai_rec_rating[4], 1)}/10
                              </div>
                          </div>""", unsafe_allow_html=True)
        # except:
        #     st.text("Error occured , please try 5 minutes")

elif st.session_state.page == "Trending":
    st.session_state.page = display_popular_movies()




# '''
# ---------------------------------------------------------------------------------------------|
#  things to do ,                                                                              |
#  1.Add trailer to link or playable trailer , when are they are recommended  on hover or focus|
# 2. where the user can watch it recommended content {ott platform names}                      |
# 3. use many dataset for better recommendation.                                               |
# 4. make ui better .                                                                          |
# 5. add account management for user.                                                          |
# ---------------------------------------------------------------------------------------------|
# '''

