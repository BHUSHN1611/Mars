import gdown
file_id = "1yjUTJJf3IZUxAuFdkwZi3l3GN44CDXOP"

url = f'https://drive.google.com/uc?id={file_id}'
output = 'movie_dict.pkl'
gdown.download(url, output, quiet=False)


