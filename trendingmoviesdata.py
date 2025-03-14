# import requests
import streamlit as st
import cssload

# for testing purpose
# st.set_page_config(layout="wide")
# st.title(" ☄️ MARS")

# this is used for data extracting
# def gen_pos_lnk(movie_id):
#     responses = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=621f11a3e889718c83d29d87d900be79&language=en-US'.format(movie_id))
#
#     data = responses.json()
#
#     return "https://image.tmdb.org/t/p/w500" + data['poster_path']
#
# responses = requests.get("https://api.themoviedb.org/3/trending/movie/day?api_key=621f11a3e889718c83d29d87d900be79&language=en-US")
# data = responses.json()
# sd_pos_url =[]
# sd_title = []
# sd_rating = []
# print("type-resp",type(responses))
# print("type-data",type(data))
# for i in range(0,20):
#     sd_pos_url.append(gen_pos_lnk(data['results'][i]['id']))
#     sd_title.append(data['results'][i]['title'])
#     sd_rating.append(data['results'][i]['vote_average'])
# print("url -",sd_pos_url)
# print("title -",sd_title)
# print("rating -",sd_rating)
def copyoftrending():
    cssload.load_css()

    url_pos = ['https://image.tmdb.org/t/p/w500/cgXk2tNYhJZLXdBDO5DidAVzQ82.jpg', 'https://image.tmdb.org/t/p/w500/oCoTgC3UyWGfyQ9thE10ulWR7bn.jpg', 'https://image.tmdb.org/t/p/w500/imKSymKBK7o73sajciEmndJoVkR.jpg', 'https://image.tmdb.org/t/p/w500/lrCcovGRcuv8Z1v3ae1ZH5Ird05.jpg', 'https://image.tmdb.org/t/p/w500/vP7Yd6couiAaw9jgMd5cjMRj3hQ.jpg', 'https://image.tmdb.org/t/p/w500/m5x8D0bZ3eKqIVWZ5y7TnZ2oTVg.jpg', 'https://image.tmdb.org/t/p/w500/4kLK3cl4MbrjVFDQXb9PT11ZaV4.jpg', 'https://image.tmdb.org/t/p/w500/llWl3GtNoXosbvYboelmoT459NM.jpg', 'https://image.tmdb.org/t/p/w500/xDGbZ0JJ3mYaGKy4Nzd9Kph6M9L.jpg', 'https://image.tmdb.org/t/p/w500/evdF1vmLzuzH8EFblqAXBXWRGSi.jpg', 'https://image.tmdb.org/t/p/w500/qNLMPY3KLrYgTX2QZ5iEwwOqyRz.jpg', 'https://image.tmdb.org/t/p/w500/fQ9hzto0cUuxjfzqNAiAnNJo8O7.jpg', 'https://image.tmdb.org/t/p/w500/yaTFjMNh8D78dDHrglivOTv5YOx.jpg', 'https://image.tmdb.org/t/p/w500/7seqaCaaXDNUHOx4DqwpoOH8pPa.jpg', 'https://image.tmdb.org/t/p/w500/7iMBZzVZtG0oBug4TfqDb9ZxAOa.jpg', 'https://image.tmdb.org/t/p/w500/AnDwpI8dY8iqJVUwVS5UotYAbB1.jpg', 'https://image.tmdb.org/t/p/w500/lI2uFlSEkwXKljqiry7coaJ6wIS.jpg', 'https://image.tmdb.org/t/p/w500/pzIddUEMWhWzfvLI3TwxUG2wGoi.jpg', 'https://image.tmdb.org/t/p/w500/6izwz7rsy95ARzTR3poZ8H6c5pp.jpg', 'https://image.tmdb.org/t/p/w500/s7XYieuZg9kMe07i9VI4bfGN4Pw.jpg']
    title = ['Anora', 'Companion', 'Flow', 'Mickey 17', 'The Brutalist', 'Conclave', 'Heart Eyes', 'A Complete Unknown', 'Wicked', 'The Substance', "I'm Still Here", 'Demon City', 'A Real Pain', 'Emilia Pérez', 'The Gorge', 'Squad 36', 'Counterattack', 'Captain America: Brave New World', 'Dune: Part Two', 'No Other Land']
    rating = [7.1, 7.07, 8.3, 7.6, 7.1, 7.1, 6.2, 7.2, 6.9, 7.1, 8.0, 6.571, 6.777, 6.846, 7.79, 6.7, 8.486, 6.179, 8.1, 8.1]

    st.header("Trending Movies copy",divider=True)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f""" <div class='movie-card'>
                        <img src="{url_pos[0]}" style="width:100%; border-radius:4px;">
                        <div class='movie-title'>{title[0]}</div>
                        <div class='movie-info'>
                            Rating: {round(rating[0],1)}/10
                        </div>
                    </div>""",unsafe_allow_html=True )
    with col2:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[1]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[1]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[1],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[2]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[2]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[2],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[3]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[3]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[3],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[4]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[4]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[4],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f""" <div class='movie-card'>
                        <img src="{url_pos[5]}" style="width:100%; border-radius:4px;">
                        <div class='movie-title'>{title[5]}</div>
                        <div class='movie-info'>
                            Rating: {round(rating[5],1)}/10
                        </div>
                    </div>""",unsafe_allow_html=True)
    with col2:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[6]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[6]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[6],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[7]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[7]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[7],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[8]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[8]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[8],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[9]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[9]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[9],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f""" <div class='movie-card'>
                        <img src="{url_pos[10]}" style="width:100%; border-radius:4px;">
                        <div class='movie-title'>{title[10]}</div>
                        <div class='movie-info'>
                            Rating: {round(rating[10],1)}/10
                        </div>
                    </div>""",unsafe_allow_html=True)
    with col2:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[11]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[11]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[11],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[12]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title12>{title[12]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[12],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[13]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[13]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[13],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[14]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[14]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[14],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f""" <div class='movie-card'>
                        <img src="{url_pos[11]}" style="width:100%; border-radius:4px;">
                        <div class='movie-title'>{title[11]}</div>
                        <div class='movie-info'>
                            Rating: {round(rating[11],1)}/10
                        </div>
                    </div>""",unsafe_allow_html=True)
    with col2:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[16]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[16]}</div>
                                <div class='movie-info'6
                                    Rating: {round(rating[16],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[17]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title12>{title[17]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[17],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[18]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[18]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[18],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f""" <div class='movie-card'>
                                <img src="{url_pos[19]}" style="width:100%; border-radius:4px;">
                                <div class='movie-title'>{title[19]}</div>
                                <div class='movie-info'>
                                    Rating: {round(rating[19],1)}/10
                                </div>
                            </div>""", unsafe_allow_html=True)


