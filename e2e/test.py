from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time

chrome = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    desired_capabilities=DesiredCapabilities.CHROME,
)
# firefox = webdriver.Remote(
#    command_executor="http://localhost:4444/wd/hub",
#    desired_capabilities=DesiredCapabilities.FIREFOX,
# )
try:
    SPOTIFY_EMAIL = os.environ["SPOTIFY_EMAIL"]
    SPOTIFY_PASSW = os.environ["SPOTIFY_PASSW"]

    print("Check that seleniun is working")
    chrome.get("https://www.google.com")
    assert chrome.title == "Google"

    print("Check that troubleshooting link works")
    troubleshooting_link = '//*[@id="responsive-navbar-nav"]/div/a[3]'
    chrome.find_element_by_xpath(troubleshooting_link).click()
    link_back_home = "/html/body/div/div[2]/a[1]"
    chrome.find_element_by_xpath(link_back_home).click()

    print("Submit a bad room code")
    chrome.get("http://nginx")
    label_for_form_room_code_input = '//*[@id="root"]/div/div[2]/form/div/label'
    room_code_input = '//*[@id="root"]/div/div[2]/form/div/input[1]'
    room_code_submit = '//*[@id="root"]/div/div[2]/form/div/input[2]'
    chrome.find_element_by_xpath(room_code_input).send_keys("0000")
    chrome.find_element_by_xpath(room_code_submit).click()
    chrome.find_element_by_xpath(label_for_form_room_code_input)

    print("Authenticate with Spotify")
    host_or_cohost_link = '//*[@id="responsive-navbar-nav"]/div/a[1]'
    authenticate_with_spotify_button = '//*[@id="root"]/div/div[2]/div/div/p/a'
    chrome.find_element_by_xpath(host_or_cohost_link).click()
    chrome.find_element_by_xpath(authenticate_with_spotify_button).click()

    email_or_username_input = '//*[@id="login-username"]'
    password_input = '//*[@id="login-password"]'
    spotify_login_submit = "/html/body/div[1]/div[2]/div/form/div[3]/div[2]/button"
    chrome.find_element_by_xpath(email_or_username_input).send_keys(SPOTIFY_EMAIL)
    chrome.find_element_by_xpath(password_input).send_keys(SPOTIFY_PASSW)
    chrome.find_element_by_xpath(spotify_login_submit).click()

    time.sleep(1)

    assert chrome.current_url == "http://nginx/rooms/"

    print("Add a room")
    add_room_button = '//*[@id="root"]/div/div[2]/div/div/button[1]'
    cell_elements = "//div[@role = 'cell']"
    chrome.find_element_by_xpath(add_room_button).click()
    time.sleep(1)
    room_code = chrome.find_elements_by_xpath(cell_elements)[0].text
    print(f"Room code: {room_code}")
    assert len(room_code) == 4

    print("Follow a room")
    follow_room_button = '//*[@id="root"]/div/div[2]/div/div/button[2]'
    chrome.find_element_by_xpath(follow_room_button).click()
    room_code_modal_input = '//*[@id="formRoomCode"]'
    chrome.find_element_by_xpath(room_code_modal_input).send_keys(
        "0000"
    )  # fake room, nbd
    room_code_modal_submit_button = "/html/body/div[3]/div/div/div[2]/form/button"
    chrome.find_element_by_xpath(room_code_modal_submit_button).click()

    print("Follow Queue Songs Link")
    queue_songs_link = '//*[@id="responsive-navbar-nav"]/div/a[1]'
    chrome.find_element_by_xpath(queue_songs_link).click()

    print("Enter the room")
    room_code_input = '//*[@id="root"]/div/div[2]/form/div/input[1]'
    room_code_submit = '//*[@id="root"]/div/div[2]/form/div/input[2]'
    chrome.find_element_by_xpath(room_code_input).send_keys(room_code)
    chrome.find_element_by_xpath(room_code_submit).click()

    print("Queue songs")
    search_songs_input = '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/input[1]'
    chrome.find_element_by_xpath(search_songs_input).send_keys("bruc")

    time.sleep(1)

    first_suggestion = '//*[@id="song-search-typeahead-item-0"]/div'
    chrome.find_element_by_xpath(first_suggestion).click()

    submit_selected_song_button = '//*[@id="qsong"]'
    chrome.find_element_by_xpath(submit_selected_song_button).click()

    chrome.find_element_by_xpath(search_songs_input)

    print("Leave Room")
    leave_room_link = '//*[@id="responsive-navbar-nav"]/div/a[2]'
    chrome.find_element_by_xpath(leave_room_link).click()
    label_for_form_room_code_input = '//*[@id="root"]/div/div[2]/form/div/label'
    chrome.find_element_by_xpath(label_for_form_room_code_input)


except Exception as e:
    raise e
finally:
    chrome.save_screenshot("debug.png")
    chrome.quit()

