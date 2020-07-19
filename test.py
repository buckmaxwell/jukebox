from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

chrome = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    desired_capabilities=DesiredCapabilities.CHROME,
)
# firefox = webdriver.Remote(
#    command_executor="http://localhost:4444/wd/hub",
#    desired_capabilities=DesiredCapabilities.FIREFOX,
# )

chrome.get("https://www.google.com")
print(chrome.title)

# firefox.get("https://www.google.com")
# print(firefox.title)

chrome.quit()
# firefox.quit()

