from selenium import webdriver
import pandas as pd

# 当测试好能够顺利爬取后，为加快爬取速度可设置无头模式，即不弹出浏览器
# 添加无头headlesss 1使用chrome headless,2使用PhantomJS
# 使用 PhantomJS 会警告高不建议使用phantomjs，建议chrome headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

# 赋值给一个浏览器对象
chrome_driver_h = r'C:\Users\zky\Anaconda3\envs\py3.6\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'
chrome_driver_g = r'C:\ProgramData\Anaconda3\envs\py3.6\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'
browser = webdriver.Chrome(
    executable_path=chrome_driver_g, chrome_options=chrome_options)

# browser = webdriver.PhantomJS()
# browser.maximize_window()  # 最大化窗口,可以选择设置

url = 'http://data.eastmoney.com/bbsj/201906/lrb.html'
browser.get(url)

# 与页面交互，可以通过id,name,xpath进行查找(使用xpath时，只会匹配到第一个元素)

# 定位表格，element是WebElement类型
element = browser.find_element_by_css_selector('#dt_1')

# 提取表格内容td,进一步定位到表格内容所在的td节点
td_content = element.find_elements_by_tag_name("td")
lst = []  # 存储为list

for td in td_content:
    lst.append(td.text.encode('utf-8').decode('gb2312','ignore'))

# print(lst)

# 将list转换为DataFrame，首先先把一个大的list分割为多行多列的子list

# 确定表格列数
col = len(element.find_elements_by_css_selector(
    '#dt_1 > tbody > tr:nth-child(1) td'))
print(col)
# 通过定位一行td的数量，可获得表格的列数，然后将list拆分对应列数的子list 把每一行都拆分出来
lst = [lst[i:i+col] for i in range(0, len(lst), col)]
print(lst)
# 打开原网页中'详细'链接可以查看更详细的数据，这里我们可以把url提取出来
lst_link = []

# 选择 id="firstname" 的所有元素,选择第一个dt_1标签下的所有a.red标签
# element,element div,p 选择所有<div>元素和所有<p>元素
# element element div p 选择所有<div>元素内部的所有<p>元素
# element>element div>p 选择父元素<div>元素的所有<p>元素
links = element.find_elements_by_css_selector('#dt_1 a.red')

for link in links:
    url = link.get_attribute('href')
    lst_link.append(url)

lst_link = pd.Series(lst_link)
# list转化为dataframe
df_table = pd.DataFrame(lst)

# 添加到url列
df_table['url'] = lst_link
# print(df_table)