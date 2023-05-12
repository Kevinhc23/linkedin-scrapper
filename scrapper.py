from selenium import webdriver
from bs4 import BeautifulSoup

# Configuración del navegador (en este caso, Chrome)
driver = webdriver.Chrome('ruta_del_controlador_de_chrome')  # Reemplaza 'ruta_del_controlador_de_chrome' por la ruta real del controlador de Chrome en tu sistema.

# Realizar una búsqueda en LinkedIn
search_keyword = 'término_de_búsqueda'  # Reemplaza 'término_de_búsqueda' con tu término de búsqueda real.
search_url = f'https://www.linkedin.com/search/results/people/?keywords={search_keyword}'
driver.get(search_url)

# Obtener el HTML de la página
page_html = driver.page_source

# Analizar el HTML con BeautifulSoup
soup = BeautifulSoup(page_html, 'html.parser')

# Encontrar los elementos relevantes en la página y extraer la información deseada
profiles = soup.find_all('a', class_='app-aware-link')
with open('emails.txt', 'w') as file:
    for profile in profiles:
        name = profile.text.strip()
        profile_url = profile['href']

        # Visitar el perfil individual para obtener más información
        driver.get(profile_url)
        profile_html = driver.page_source
        profile_soup = BeautifulSoup(profile_html, 'html.parser')

        # Extraer el correo electrónico si está disponible
        email_element = profile_soup.find('section', class_='pv-contact-info__contact-type ci-email')
        if email_element:
            email = email_element.find('a').text.strip()
            file.write(f'Nombre: {name} - Correo electrónico: {email}\n')
        else:
            file.write(f'Nombre: {name} - No se encontró el correo electrónico\n')

# Cerrar el navegador
driver.quit()
