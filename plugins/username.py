from osintbuddy.elements import TextInput
import osintbuddy as ob

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Username(ob.Plugin):
    label = "Username"
    color = "#BF288D"
    node = [
        TextInput(label="Username", icon="user-search"),
    ]
    icon = "user-search"
    author = ["the OSINTBuddy team", "Artemii"]
    description = "Reveal social profiles"

    @ob.transform(label='To profile', icon='user')
    async def transform_to_profile(self, node, use):
        with use.get_driver() as driver:
            driver.get('https://whatsmyname.app/')
            driver.find_element(By.XPATH, "//*[@id='targetUsername']").send_keys(node.username)
            driver.find_element(By.XPATH, "//*[@id='main']/div/div/div[3]/div[2]/div/div[2]/button").click()
            WebDriverWait(driver, 90).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[@id='txtall']"), "579")
            )
            records = driver.find_elements(By.XPATH, "//*[@id='collectiontable']/tbody/tr")
            data = []
            SocialProfilePlugin = await ob.Registry.get_plugin('username_profile')
            for elm in records:
                tds = elm.find_elements(by=By.TAG_NAME, value='td')
                blueprint = SocialProfilePlugin.blueprint(
                    category=tds[2].text,
                    site=tds[0].text,
                    link=tds[3].text,
                    username=tds[1].text
                )
                data.append(blueprint)
            return data
