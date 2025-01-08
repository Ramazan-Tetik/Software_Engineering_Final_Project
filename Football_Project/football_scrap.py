#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import re
import traceback
from warnings import filterwarnings
import streamlit as st
filterwarnings('ignore')
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


#arayuz icin eklendi bunu kaldirman gerekebilir.
dataframe_placeholder = st.empty()
#run this cell just for the first time. Because you may lose data

keys = [
    'Country',
    'Lig',
    'home_team',
    'away_team',
    'home_score',
    'away_score',
    'season_year',
    'Date_day',
    'Date_hour',
    'first_half',
    'second_half',
    
    'home_team_goals_current_time',
    'home_team_goals_current_score',
    'home_team_goals',
    'home_team_goals_assist',
    
    'away_team_goals_current_time',
    'away_team_goals_current_score',
    'away_team_goals',
    'away_team_goals_assist',

    'home_team_yellow_card_current_time',
    'home_team_yellow_card',
    'home_team_yellow_card_why',

    'away_team_yellow_card_current_time',
    'away_team_yellow_card',
    'away_team_yellow_card_why',

    'home_team_red_card_current_time',
    'home_team_red_card',
    'home_team_red_card_why',
    
    'away_team_red_card_current_time',
    'away_team_red_card',
    'away_team_red_card_why',
    
    'home_team_substitutions_current_time',
    'home_team_substitutions',
    'home_team_substitutions_with',
    'home_team_substitution_why',
    
    'away_team_substitutions_current_time',
    'away_team_substitutions',
    'away_team_substitutions_with',
    'away_team_substitution_why',
    
    'expected_goals_xg_home' ,
    'expected_goals_xg_host' ,
    
    'Ball_Possession_Home' ,
    'Ball_Possession_Host' ,
    
    'Goal_Attempts_Home' ,
    'Goal_Attempts_Host' ,
    
    'Shots_on_Goal_Home' ,
    'Shots_on_Goal_Host' ,
    
    'Shots_off_Goal_Home' ,
    'Shots_off_Goal_Host' ,
    
    'Blocked_Shots_Home' ,
    'Blocked_Shots_Host' ,
    
    'Free_Kicks_Home' ,
    'Free_Kicks_Host' ,
    
    'Corner_Kicks_Home' ,
    'Corner_Kicks_Host' ,
    
    'Offsides_Home' ,
    'Offsides_Host' ,
    
    'Throw_ins_Home' ,
    'Throw_ins_Host' ,
    
    'Goalkeeper_Saves_Home' ,
    'Goalkeeper_Saves_Host' ,
    
    'Fouls_Home' ,
    'Fouls_Host' ,
    
    'Red_Cards_Home' ,
    'Red_Cards_Host' ,
    
    'Yellow_Cards_Home' ,
    'Yellow_Cards_Host' ,
    
    'Total_Passes_Home' ,
    'Total_Passes_Host' ,
    
    'Completed_Passes_Home' ,
    'Completed_Passes_Host' ,
    
    'Tackles_Home' ,
    'Tackles_Host' ,
    
    'Crosses_Completed_Home' ,
    'Crosses_Completed_Host' ,
    
    'Interceptions_Home' ,
    'Interceptions_Host',
    
    'Attacks_Home',
    'Attacks_Host',
    
    'Dangerous_Attacks_Home' ,
    'Dangerous_Attacks_Host',
    
    'Distance_Covered_(km)_Home',
    'Distance_Covered_(km)_Host',
    
    'Clearances_Completed_Home',
    'Clearances_Completed_Host',
    
    'Pass_Success_per_Home',
    'Pass_Success_per_Host',
    
    'referee',
    'venue',
    'capacity',
    'attendance',
    
]

df = pd.DataFrame(columns=keys)


# In[4]:


def clean_country(country):
    country = country.lower()
    replacements = {
        ' - ': '-',
        " & ": "-",
        ' ':'-',
        'ç':'c',
        'é':'e',
        'ã':'a',
        'í':'i'
    }
    for old, new in replacements.items():
        country = country.replace(old, new)
    
    return country


# In[5]:


def clean_lig(lig):
    lig = lig.lower()
    replacements = {
        ' - ': '-',
        '- ': ' - ',
        ' - ': '-',
        '. ': '-',
        ' ': '-',
        'ë': 'e',
        'ó': 'o',
        "'": '-',
        '(': '',
        ')': '',
        'é': 'e',
        '’': '-',
        '/': '-',
        'ü': 'u',
        '.': '-',
        'serie-d-winners-stage': 'serie-d-winners-stag',
        'ç': 'c',
        'ö': 'o',
        'ä': 'a',
        '---': '-',
        '--': '-',
        '-&-': '-'
    }
    for old, new in replacements.items():
        lig = lig.replace(old, new)
    
    return lig


# In[6]:


def scrap(country_link_name, leagues, years):
    print('ffonksiyona girildi')
    
    only_once= True
    #path = "/Users/muhammedaydin/Desktop/driverchrome/chromedriver"
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    print('site aciliyor')
    driver = webdriver.Chrome(service=service, options=options)
    print('the site was opened.')
    driver.implicitly_wait(3)
    ligs = leagues
    for lig in ligs:
        lig = clean_lig(lig)
        print('League name given to the link.')
        country_link_name = clean_country(country_link_name)
        print('Country name given to the link.')
        url = "https://www.flashscore.com/football/" + country_link_name +"/" + lig +"/"
        driver.get(url)
        print('url ye gidildi')
        if only_once==True:
            print('sorgu gecildi')
            cookies_rejected_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))
                )
            print('elemant bulundu') 
            cookies_rejected_button.click()
            print('cookies reddedildi')
            print('Cookies are rejected.')
            only_once =False
        time.sleep(2)
        try:
            for year in years:
                driver.implicitly_wait(3)
                select_year(driver,year)
                print('The year is selected from archive')
                more_button(driver)
                print('Click on the more button phase has passed')
                county_name = country_link_name.capitalize()
                scrape_everything(driver,county_name, lig, year)
                print('Exited scrape everything function')
                print('Going to next year...')
        except Exception as e:
            print(f"A general error has occurred: {e}")
            traceback.print_exc()


def select_year(driver,year):
    counter = 1
    archive_button = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="li5"]')))
    archive_button.click()
    archive_season_links = driver.find_elements(By.XPATH, '//div[@class="archive__season"]/a')
    print('-------------------------------------------------------------------------')
    for i in range(len(archive_season_links)):
        if year == archive_season_links[i].text.strip().split(' ')[-1]:
            counter = 0
            print(f'sene:{year}')
            archive_season_links[i].click()
            results_button = driver.find_element(By.XPATH, '//*[@id="li2"]')
            results_button.click()
            time.sleep(2)
            break

    if counter == 1:
        year = year.split('/')[-2]
        for i in range(len(archive_season_links)):
            print('test edilen sene',archive_season_links[i].text.strip().split(' ')[-1])
            print('aranan sene: ',year)
            if year == archive_season_links[i].text.strip().split(' ')[-1]:
                print(f'sene:{year}')
                archive_season_links[i].click()
                results_button = driver.find_element(By.XPATH, '//*[@id="li2"]')
                results_button.click()
                time.sleep(2)
                counter = 2
                break
    if counter == 1:
        archive_season_links[0].click()
    


# In[8]:


def more_button(driver):
    print('located location : more_button')
    for i in range(0,3):
        try:
            show_more_button = driver.find_element(By.XPATH, "//a[@class='event_more event_more--static']")
            #driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            show_more_button.click()
            time.sleep(2)
        except NoSuchElementException:
            print("There is no button in this page.")
            break
    driver.execute_script("window.scrollTo(0, 0);")


# In[9]:


def scrape_everything(driver, county_name, lig, year):
    print(f"Scraping for country: {county_name}, league: {lig}, year: {year}")
    try:
        matches = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "event__match")]'))
        )
        for match in matches:
            new_row = []
            date = match.find_element(By.CLASS_NAME, 'event__time').text
            date = date.split(' ')
            date_day = date[0].rstrip('.')
            date_hour = date[1]
            home_team = match.find_element(By.CLASS_NAME, 'event__homeParticipant').text
            away_team = match.find_element(By.CLASS_NAME, 'event__awayParticipant').text
            home_score = match.find_element(By.CLASS_NAME, 'event__score--home').text
            away_score = match.find_element(By.CLASS_NAME, 'event__score--away').text
            match.click()
            windows = driver.window_handles
            driver.switch_to.window(windows[1])

            halfs = driver.find_elements(By.CLASS_NAME, 'smv__incidentsHeader ')
            first_half_score = None
            second_half_score = None
            
            if len(halfs) > 0:
                try:
                    first_half_score = halfs[0].text.split('\n')[1]
                except IndexError:
                    first_half_score = halfs[0].text.split('\n')[0]
            else:
                first_half_score = None
            if len(halfs) > 1:
                try:
                    second_half_score = halfs[1].text.split('\n')[1]
                except IndexError:
                    second_half_score = halfs[1].text.split('\n')[0]
            else:
                second_half_score = None
            
            summary_data = scrape_summary(driver)

           

            home_goals_time  = summary_data['home_goals_time']
            home_current_score = summary_data['home_current_score']
            home_the_goal = summary_data['home_the_goal']
            home_assist = summary_data['home_assist']
            
            home_yellow_time = summary_data['home_yellow_time']
            home_yellow_who = summary_data['home_yellow_who']
            home_yellow_why = summary_data['home_yellow_why']
            
            home_red_time = summary_data['home_red_time']
            home_red_who = summary_data['home_red_who']
            home_red_why= summary_data['home_red_why']
            
            home_substitution_time = summary_data['home_substitution_time']
            home_substitution_who = summary_data['home_substitution_who']
            home_substitution_with_who = summary_data['home_substitution_with_who']
            home_substitution_why = summary_data['home_substitution_why']
            
            away_goals_time = summary_data['away_goals_time']
            away_current_score = summary_data['away_current_score']
            away_the_goal = summary_data['away_the_goal']
            away_assist = summary_data['away_assist']
            
            away_yellow_time = summary_data['away_yellow_time']
            away_yellow_who = summary_data['away_yellow_who']
            away_yellow_why = summary_data['away_yellow_why']
            
            away_red_time = summary_data['away_red_time']
            away_red_who = summary_data['away_red_who']
            away_red_why = summary_data['away_red_why']
            
            away_substitution_time = summary_data['away_substitution_time']
            away_substitution_who = summary_data['away_substitution_who']
            away_substitution_with_who = summary_data['away_substitution_with_who']
            away_substitution_why= summary_data['away_substitution_why'] 
            
            match_details = scrape_match_details(driver)
            referee = match_details['referee']
            venue = match_details['venue']
            capacity = match_details['capacity']
            attendance = match_details['attendance']

            stats = scrape_stats(driver)
            
            expected_goals_xg_home = stats['Expected_Goals_(xG)_Home']
            expected_goals_xg_host = stats['Expected_Goals_(xG)_Host']
            
            Ball_Possession_Home = stats['Ball_Possession_Home']
            Ball_Possession_Host = stats['Ball_Possession_Host']
            
            Goal_Attempts_Home = stats['Goal_Attempts_Home']
            Goal_Attempts_Host = stats['Goal_Attempts_Host']
            
            Shots_on_Goal_Home = stats['Shots_on_Goal_Home']
            Shots_on_Goal_Host = stats['Shots_on_Goal_Host']
            
            Shots_off_Goal_Home = stats['Shots_off_Goal_Home']
            Shots_off_Goal_Host = stats['Shots_off_Goal_Host']
            
            Blocked_Shots_Home = stats['Blocked_Shots_Home']
            Blocked_Shots_Host = stats['Blocked_Shots_Host']
            
            Free_Kicks_Home = stats['Free_Kicks_Home']
            Free_Kicks_Host = stats['Free_Kicks_Host']
            
            Corner_Kicks_Home = stats['Corner_Kicks_Home']
            Corner_Kicks_Host = stats['Corner_Kicks_Host']
            
            Offsides_Home = stats['Offsides_Home']
            Offsides_Host = stats['Offsides_Host']
            
            Throw_ins_Home = stats['Throw-ins_Home']
            Throw_ins_Host = stats['Throw-ins_Host']
            
            Goalkeeper_Saves_Home = stats['Goalkeeper_Saves_Home']
            Goalkeeper_Saves_Host = stats['Goalkeeper_Saves_Host']
            
            Fouls_Home = stats['Fouls_Home']
            Fouls_Host = stats['Fouls_Host']
            
            Red_Cards_Home = stats['Red_Cards_Home']
            Red_Cards_Host = stats['Red_Cards_Host']
            
            Yellow_Cards_Home = stats['Yellow_Cards_Home']
            Yellow_Cards_Host = stats['Yellow_Cards_Host']
            
            Total_Passes_Home = stats['Total_Passes_Home']
            Total_Passes_Host = stats['Total_Passes_Host']
            
            Completed_Passes_Home = stats['Completed_Passes_Home']
            Completed_Passes_Host = stats['Completed_Passes_Host']
            
            Tackles_Home = stats['Tackles_Home']
            Tackles_Host = stats['Tackles_Host']
            
            Crosses_Completed_Home = stats['Crosses_Completed_Home']
            Crosses_Completed_Host = stats['Crosses_Completed_Host']
            
            Interceptions_Home = stats['Interceptions_Home']
            Interceptions_Host = stats['Interceptions_Host']
            
            Attacks_Home = stats['Attacks_Home']
            Attacks_Host = stats['Attacks_Host']
            
            Dangerous_Attacks_Home = stats['Dangerous_Attacks_Home']
            Dangerous_Attacks_Host = stats['Dangerous_Attacks_Host']
            
            Distance_Covered_km_Home = stats['Distance_Covered_(km)_Home']
            Distance_Covered_km_Host = stats['Distance_Covered_(km)_Host']
            
            Clearances_Completed_Home = stats['Clearances_Completed_Home']
            Clearances_Completed_Host = stats['Clearances_Completed_Host']
            Pass_Success_per_Home = stats['Pass_Success_%_Home']
            Pass_Success_per_Host = stats['Pass_Success_%_Host']
            
            driver.close()

            driver.switch_to.window(windows[0])
            
            
            new_row.extend([county_name, lig.capitalize(), home_team, away_team, home_score, away_score, year, date_day,
                            date_hour,first_half_score,second_half_score,home_goals_time, home_current_score ,home_the_goal, home_assist,
                            away_goals_time ,away_current_score, away_the_goal,away_assist,home_yellow_time ,home_yellow_who,
                            home_yellow_why, away_yellow_time, away_yellow_who ,away_yellow_why,
                            home_red_time, home_red_who, home_red_why,away_red_time, away_red_who, away_red_why,
                            home_substitution_time, home_substitution_who, home_substitution_with_who, home_substitution_why,
                            away_substitution_time, away_substitution_who, away_substitution_with_who, away_substitution_why,
                            expected_goals_xg_home ,expected_goals_xg_host ,Ball_Possession_Home ,Ball_Possession_Host ,
                            Goal_Attempts_Home ,Goal_Attempts_Host ,Shots_on_Goal_Home ,Shots_on_Goal_Host ,Shots_off_Goal_Home ,
                            Shots_off_Goal_Host ,Blocked_Shots_Home ,Blocked_Shots_Host ,Free_Kicks_Home ,Free_Kicks_Host ,
                            Corner_Kicks_Home ,Corner_Kicks_Host ,Offsides_Home ,Offsides_Host ,Throw_ins_Home ,Throw_ins_Host ,
                            Goalkeeper_Saves_Home ,Goalkeeper_Saves_Host ,Fouls_Home ,Fouls_Host ,Red_Cards_Home ,Red_Cards_Host ,
                            Yellow_Cards_Home ,Yellow_Cards_Host ,Total_Passes_Home ,Total_Passes_Host ,Completed_Passes_Home ,
                            Completed_Passes_Host ,Tackles_Home ,Tackles_Host ,Crosses_Completed_Home ,Crosses_Completed_Host ,
                            Interceptions_Home ,Interceptions_Host, Attacks_Home, Attacks_Host, Dangerous_Attacks_Home, Dangerous_Attacks_Host,
                            Distance_Covered_km_Home, Distance_Covered_km_Host,Clearances_Completed_Home, Clearances_Completed_Host,
                            Pass_Success_per_Home,Pass_Success_per_Host,
                            referee,venue, capacity, attendance])
            
            dataframe_placeholder.dataframe(df) #arayuzde df yi gostermek  icin eklendi kaldirman gerekebilir.
            df.loc[len(df)] = new_row
    except TimeoutException:
        print("Timeout occurred while waiting for matches to load.")
        raise
    driver.execute_script("window.scrollTo(0, 0);")
        


# In[10]:


def handle_svg1(svg_class,summ_list, goals_time, current_score, the_goal, assist, yellow_time, yellow_who, yellow_why,
              red_time, red_who, red_with, substitution_time, substitution_who, substitution_with_who, substitution_why):
    print('located location : handle_svg1')
    summ_list = summ_list.split('\n')
    #print(summ_list)
    if svg_class == '':
        goals_time.append(summ_list[0])
        current_score.append(summ_list[1])
        the_goal.append(summ_list[2])
        
        if len(summ_list)>3:
            assist.append(summ_list[3])
        else:
            assist.append('-')
    elif svg_class == 'card-ico yellowCard-ico':
        yellow_time.append(summ_list[0])
        yellow_who.append(summ_list[1])
        yellow_why.append(summ_list[2])
        
    elif svg_class == 'card-ico redCard-ico':
        red_time.append(summ_list[0])
        red_who.append(summ_list[1])
        red_with.append(summ_list[2])
        
    elif svg_class == 'substitution ':
        substitution_time.append( summ_list[0])
        substitution_who.append(summ_list[1])
        substitution_with_who.append(summ_list[2])
        
        if len(summ_list) > 3:
            substitution_why.append(summ_list[3])
        else:
            substitution_why.append('-')
    elif svg_class == 'card-ico ':
        red_time.append(summ_list[0])
        red_who.append(summ_list[1])
        red_with.append(summ_list[2])
        
    elif svg_class == 'var ':
        pass
    elif svg_class == 'footballOwnGoal-ico':
        goals_time.append(summ_list[0])
        current_score.append(summ_list[1])
        the_goal.append(summ_list[2])
        
        if len(summ_list)>3:
            assist.append(summ_list[3])
        else:
            assist.append('-')
    elif svg_class == 'warning ':
        pass
    elif svg_class == 'arrow arrowDown-ico':
        pass
    elif svg_class == 'arrow arrowUp-ico':
        pass
    elif svg_class == 'smv__incidentIcon':
        pass
    else:
        pass


# In[11]:


def scrape_summary(driver):
    print('located location : scrape_summary')
    home_goals_time = []
    home_current_score = []
    home_the_goal = []
    home_team_goals_assist = []
    home_yellow_time = []
    home_yellow_who = []
    home_yellow_why = []
    home_red_time = []
    home_red_who = []
    home_red_why = []
    home_substitution_time = []
    home_substitution_who = []
    home_substitution_with_who = []
    home_substitution_why = []
    
    away_goals_time = []
    away_current_score = []
    away_the_goal = []
    away_team_goals_assist = []
    away_yellow_time = []
    away_yellow_who = []
    away_yellow_why = []
    away_red_time = []
    away_red_who = []
    away_red_why = []
    away_substitution_time = []
    away_substitution_who = []
    away_substitution_with_who = []
    away_substitution_why = []
    driver.implicitly_wait(2)
    try:
        summary = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'smv__participantRow')))
    
        for index, summ in enumerate(summary):
            combined_info = None
            
            svg = WebDriverWait(summ, 3).until(
                EC.presence_of_element_located((By.TAG_NAME, "svg")))
            svg_class = svg.get_attribute('class')
            if svg_class == 'arrow arrowDown-ico':
                current_time  = summ.text.split('\n')[0]
                down = summ.text.split('\n')[1]
                up = summary[index+1].text.split('\n')[1]
                combined_info = f"{current_time} {up} {down}"
                
            summ_list = summ.text
            
            if 'smv__awayParticipant' in summ.get_attribute('class'):
                if combined_info is not None:
                    away_team_substitutions.append(combined_info)
                    
                handle_svg1(svg_class, summ_list,
                       away_goals_time,away_current_score,away_the_goal,away_team_goals_assist,
                       away_yellow_time,away_yellow_who,away_yellow_why,away_red_time,
                       away_red_who,away_red_why,away_substitution_time,away_substitution_who,
                       away_substitution_with_who,away_substitution_why)

            elif 'smv__homeParticipant' in summ.get_attribute('class'):

                if combined_info is not None:
                    home_team_substitutions.append(combined_info)
                    
                handle_svg1(svg_class, summ_list,home_goals_time ,home_current_score ,
                           home_the_goal,home_team_goals_assist ,home_yellow_time ,home_yellow_who ,home_yellow_why ,home_red_time ,
                           home_red_who ,home_red_why ,home_substitution_time ,home_substitution_who ,
                           home_substitution_with_who ,home_substitution_why)    
                
                
    except:
        driver.implicitly_wait(3)
        pass
        
    return {
        'home_goals_time': home_goals_time,
        'home_current_score': home_current_score,
        'home_the_goal': home_the_goal,
        'home_assist': home_team_goals_assist,
        'home_yellow_time': home_yellow_time,
        'home_yellow_who': home_yellow_who,
        'home_yellow_why': home_yellow_why,
        'home_red_time': home_red_time,
        'home_red_who': home_red_who,
        'home_red_why': home_red_why,
        'home_substitution_time': home_substitution_time,
        'home_substitution_who': home_substitution_who,
        'home_substitution_with_who': home_substitution_with_who,
        'home_substitution_why': home_substitution_why,
        
        'away_goals_time': away_goals_time,
        'away_current_score': away_current_score,
        'away_the_goal': away_the_goal,
        'away_assist': away_team_goals_assist,
        'away_yellow_time': away_yellow_time,
        'away_yellow_who': away_yellow_who,
        'away_yellow_why': away_yellow_why,
        'away_red_time': away_red_time,
        'away_red_who': away_red_who,
        'away_red_why': away_red_why,
        'away_substitution_time': away_substitution_time,
        'away_substitution_who': away_substitution_who,
        'away_substitution_with_who': away_substitution_with_who,
        'away_substitution_why': away_substitution_why
    }
    


# In[12]:


def scrape_match_details(driver):
    print('located location : scrape_match_details')
    match_info = driver.find_elements(By.CLASS_NAME, 'wcl-content_J-1BJ')

    referee = None
    venue = None
    capacity = None
    attendance = None

    full_text = " ".join([info.text.replace("\n", " ") for info in match_info])

    if "REFEREE:" in full_text:
        referee = full_text.split("REFEREE:")[1].split("VENUE:")[0].strip()
    if "VENUE:" in full_text:
        venue = full_text.split("VENUE:")[1].split("CAPACITY:")[0].strip()
    if "CAPACITY:" in full_text:
        capacity = full_text.split("CAPACITY:")[1].split("ATTENDANCE:")[0].strip()
    if "ATTENDANCE:" in full_text:
        attendance = full_text.split("ATTENDANCE:")[1].strip()

    return {
        'referee': referee,
        'venue': venue,
        'capacity': capacity,
        'attendance': attendance
    }


# In[13]:


def scrape_stats(driver):
    print('located location : scrape_stats')
    stats_dict = {
        'Expected_Goals_(xG)_Home': None,
        'Expected_Goals_(xG)_Host': None,
        'Ball_Possession_Home': None,
        'Ball_Possession_Host': None,
        'Goal_Attempts_Home': None,
        'Goal_Attempts_Host': None,
        'Shots_on_Goal_Home': None,
        'Shots_on_Goal_Host': None,
        'Shots_off_Goal_Home': None,
        'Shots_off_Goal_Host': None,
        'Blocked_Shots_Home': None,
        'Blocked_Shots_Host': None,
        'Free_Kicks_Home': None,
        'Free_Kicks_Host': None,
        'Corner_Kicks_Home': None,
        'Corner_Kicks_Host': None,
        'Offsides_Home': None,
        'Offsides_Host': None,
        'Throw-ins_Home': None,
        'Throw-ins_Host': None,
        'Goalkeeper_Saves_Home': None,
        'Goalkeeper_Saves_Host': None,
        'Fouls_Home': None,
        'Fouls_Host': None,
        'Red_Cards_Home': None,
        'Red_Cards_Host': None,
        'Yellow_Cards_Home': None,
        'Yellow_Cards_Host': None,
        'Total_Passes_Home': None,
        'Total_Passes_Host': None,
        'Completed_Passes_Home': None,
        'Completed_Passes_Host': None,
        'Tackles_Home': None,
        'Tackles_Host': None,
        'Crosses_Completed_Home': None,
        'Crosses_Completed_Host': None,
        'Interceptions_Home': None,
        'Interceptions_Host': None,
        'Attacks_Home':None,
        'Attacks_Host':None,
        'Dangerous_Attacks_Home':None,
        'Dangerous_Attacks_Host':None,
        'Distance_Covered_(km)_Home':None,
        'Distance_Covered_(km)_Host':None,
        'Clearances_Completed_Home':None,
        'Clearances_Completed_Host':None,
        'Pass_Success_%_Home':None,
        'Pass_Success_%_Host':None}
    
    cleaned_stats = []
    driver.implicitly_wait(2)
    try:
        stats_button = driver.find_element(By.XPATH, "//button[text()='Stats']")
        stats_button.click()
        stats = driver.find_elements(By.CLASS_NAME, 'wcl-category_ITphf')
        
        for stat in stats:
            stat = stat.text
            stat_split = stat.split('\n')
            current_stat = stat_split[1].replace(' ', '_')
            current_stat_home = current_stat + '_Home'
            current_stat_host = current_stat + '_Host'
            stats_dict[current_stat_home] = stat_split[0]
            stats_dict[current_stat_host] = stat_split[2]
    
    except NoSuchElementException:
        driver.implicitly_wait(3)
        pass
    return stats_dict


# In[14]:


#scrap('France',['Coupe de France'],[f"{year}/{year + 1}" for year in range(2024, 1999, -1)])


#df.to_csv('Coupe_de_France_2000.csv',index=False)




#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)
#df.tail(1)


# In[18]:


df


# In[19]:


# In[ ]:





# In[ ]:
