from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

print('Загрузка...')
options = Options()
options.add_argument('-headless')
driver_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'  # путь к geckodriver.exe
driver = webdriver.Firefox(executable_path=driver_path, options=options)
print('загрузка закончена')

# Запуск бесконечного цикла для поиска фильмов
while True:
    print('Открываем IMDB...')
    driver.get('https://www.imdb.com/')
    search_box = driver.find_element(By.ID, 'suggestion-search')
    print('Ищите фильм')
    movie_name = input('Введите название фильма:\n')
    search_box.send_keys(movie_name)
    search_box.submit()
    print('Запрос отправлен, ищем...')
    time.sleep(2)
    search_results = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

    print('Вот что мы нашлось:')
    found_movies = []
    for result in search_results:
        title = result.find_element(By.CLASS_NAME, 'ipc-metadata-list-summary-item__t')
        info = result.find_element(By.CLASS_NAME, 'ipc-metadata-list-summary-item__tl').find_elements(By.TAG_NAME, 'li')
        info = ' '.join(list(map(lambda x: x.text, info)))
        found_movies.append(result)
        print(f'{len(found_movies)}. {title.text} ({info})')

    movie_choice = int(input('Введите номер фильма или 0 для нового запроса:\n'))
    if movie_choice != 0:
        break

print('Парсим информацию о фильме...')
found_movies[movie_choice - 1].find_element(By.TAG_NAME, 'a').click()

movie_title = driver.find_element(By.TAG_NAME, 'h1').text
original_title = driver.find_element(By.XPATH,
        '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div').text
movie_info = driver.find_elements(By.XPATH,
        '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li')
movie_info = list(map(lambda x: x.text, movie_info))
if len(movie_info) > 3:
    movie_info = movie_info[1] + ' ' + movie_info[0]
else:
    movie_info = movie_info[0]
movie_rating = driver.find_element(By.XPATH,
        '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/'
        'a/span/div/div[2]/div[1]/span[1]').text

movie_cast = driver.find_element(By.CLASS_NAME, 'title-cast__grid').find_elements(By.TAG_NAME, 'a')
actor_names = list(map(lambda x: x.text, filter(lambda x: x.get_attribute('data-testid') == 'title-cast-item__actor', movie_cast)))
actor_roles = list(map(lambda x: x.text, filter(lambda x: x.get_attribute('data-testid') == 'cast-item-characters-link', movie_cast)))
actors = zip(actor_names, actor_roles)

print(f'{movie_title} ({movie_info})\n{original_title}\nРейтинг IMDB: {movie_rating}/10')
print('В ролях:')
print('Актёр'.ljust(39), 'Роль')
for actor in actors:
    print(actor[0].ljust(39), actor[1])

driver.close()



















