from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

def load(driver, game: str):
    driver.execute_script(f"window.localStorage.setItem('CookieClickerGame', '{game}');")

def get_game_code(driver):
    game = driver.execute_script("return window.localStorage.getItem('CookieClickerGame');")

    return game

def main():
    code = read_txt()
    
    driver = Chrome()
    
    driver.get("https://orteil.dashnet.org/cookieclicker/")
    
    wait = WebDriverWait(driver, 10) 

    consent_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Consent']"))
    )
    consent_button.click()
    
    language_button = wait.until(
        EC.element_to_be_clickable((By.ID, "langSelect-EN"))
    )
    language_button.click()
    
    sleep(2)
    
    if code:
        load(driver=driver, game=code)
        driver.refresh()
    else:
        code = get_game_code(driver=driver)
        
        with open("game.txt", "w") as f:
            f.write(code)
    
    cookie_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='bigCookie']"))
    )
    click_cookie(cookie=cookie_button, driver=driver)

def read_txt():
    with open("game.txt", "r") as f:
        content = f.read()
        
        if len(content) > 0:
            return content
        else:
            return None

def save(driver):
    driver.execute_script("Game.toSave=true")
    code = get_game_code(driver=driver)
    
    return code

def get_unlocked(driver):
    l = driver.find_elements(By.XPATH, "//div[@class='product unlocked enabled']")
    
    for unlocked in l:
        unlocked.click()
    
    return l

def get_locked(driver):
    l = driver.find_elements(By.XPATH, "//div[@class='product locked disabled']")
    
    for locked in l:
        print(f"Locked: {locked.id}")
    
    return l

def click_cookie(cookie, driver):
    run = True
    
    while run:
        cookie.click()
        
        code = save(driver=driver)
        
        with open("game.txt", "w") as f:
            f.write(code)
            
        get_unlocked(driver=driver)
        
        sleep(.00000000000000001)
    
if __name__ == "__main__":
    main()