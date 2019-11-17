from selenium import webdriver
import time

chrome_driver = r'C:\Users\zky\Anaconda3\envs\py3.6\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver)

time.sleep(5)
print('-'*30, end = '\nFinish!\n')