from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_beatmap_info(url, driver):
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.beatmapset-header__details-text-link")))

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    # song info
    song_info_elements = soup.find_all("a", class_="beatmapset-header__details-text-link")
    if len(song_info_elements) >= 2:
        title = song_info_elements[0].text
        artist = song_info_elements[1].text
    else:
        title = ""
        artist = ""

    print(f"\nSong Info \nTitle: {title} \nArtist: {artist}")

    # map info
    mapper = soup.find("a", class_="js-usercard beatmapset-mapping__user").text
    stats_info_elements = soup.find_all("time")

    if len(stats_info_elements) >= 1:
        if stats_info_elements[0].get("class") == ["js-tooltip-time"] and stats_info_elements[0].text is not None:
            submitted = stats_info_elements[0].text
        elif stats_info_elements[0].get("class") == ["js-timeago"]:
            submitted = stats_info_elements[0].text
        else:
            submitted = ""
    else:
        submitted = ""

    if len(stats_info_elements) >= 2:
        if stats_info_elements[1].get("class") == ["js-tooltip-time"] and stats_info_elements[1].text is not None:
            ranked = stats_info_elements[1].text
        elif stats_info_elements[1].get("class") == ["js-timeago"]:
            ranked = stats_info_elements[1].text
        else:
            ranked = ""
    else:
        ranked = ""

    print(f"\nMap Info \nMapper: {mapper} \nSubmitted: {submitted} \nRanked: {ranked}")

    # stats
    duration = soup.find("div", class_="beatmap-basic-stats__entry").find("span").text
    stats_info_elements = soup.find_all("td", class_="beatmap-stats-table__value")
    if len(stats_info_elements) >= 2:
        cs = stats_info_elements[0].text
        ar = stats_info_elements[3].text
        sr = stats_info_elements[4].text
    else:
        cs = ""
        ar = ""
        sr = ""

    print(f"\nImportant Stats \nDuration: {duration} \nCS: {cs} \nAR: {ar} \nStar Rating: {sr}")

    driver.quit()


inp = input("Enter URL for the beatmap: ")

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

webdriver = webdriver.Chrome(options=options)

while True:
    if "https://osu.ppy.sh/beatmapsets/" in inp:
        get_beatmap_info(inp, webdriver)
        download = input("\nDownload beatmap? [y/n]: ").lower()
        if download == "y":
            try:
                download_button = WebDriverWait(webdriver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "button.btn-osu-big btn-osu-big--beatmapset-header js-user-link")
                    )
                )
                download_button.click()
                print("Downloading beatmap...")
            except Exception as e:
                print(f"Failed to click download button: {e}")
        break
    else:
        print("Invalid URL")
        inp = input("Enter URL for the beatmap: ")
