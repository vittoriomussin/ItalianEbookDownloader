# ItalianEbookDownloader
Supported Sites: (https://ebookspy.com/, )

## Settings
- download_default_directory: path of the download directory
- user_data_dir: path of Chrome User Profile (Do not use the same profile you are using right now as chrome can only open one profile in the browser at a time!)
- executable_path: path of your chromedriver.exe

## ebookspy.com - ebookspy_links.txt File
The lines of the file have this structure:
Title;book_page;book_language;book_date;book_category

Catherine des grands chemins by Juliette Benzoni;/catherine-des-grands-chemins-by-juliette-benzoni_62246f04d77d5e6deb287590/;fra;2011-10-11;Azione e avventura

You can query this file to get the books you want (for now there is only the option for querying the year)

## Dealing with recaptchav3
- Avoid unique UserAgent-screen instances
```
options.add_argument("window-size=1280,800")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"})
```
- Remove Navigator.Webdriver Flag
```
options.add_argument("--disable-blink-features")
options.add_argument('--disable-blink-features=AutomationControlled')
```
- Exclude the collection of enable-automation switches
```
options.add_experimental_option("excludeSwitches", ["enable-automation"])
```
- Turn-off useAutomationExtension
```
options.add_experimental_option('useAutomationExtension', False)
```
- Change the property value of the navigator for webdriver to undefined
```
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
```
- Make a realistic page flow
```
# visiting google.com
time.sleep(random.randint(1, 3) + random.random())
# visiting the website's home
time.sleep(random.randint(1, 3) + random.random())
# visiting the page of the ebook
time.sleep(random.randint(1, 3) + random.random())
```
## Disclaimer: Exception Handling
I'm not very good in handling exception so i added a simple try and except in the main() to avoid the program to crash

## Upcoming Features
- better exception handling
- handle no wi-fi situation
