import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol

import plotly.express as px

import requests
import xml.dom.minidom as minidom
import datetime as dt
import pandas as pd

from app import app
from navbar import Navbar

import json
from dateutil.relativedelta import *

nav = Navbar()


def site_data(site1, site2):
    metric = 'WTEQ'

    http = 'https://www.nrcs.usda.gov/Internet/WCIS/sitedata/MONTHLY/$METRIC$/$TRIPLET$.json'

    http = http.replace('$METRIC$', metric)

    # site 1

    http = http.replace('$TRIPLET$', site1)

    response = requests.get(http)

    todo = json.loads(response.text)

    todo_list = todo['values']
    beginDate = todo["beginDate"]
    endDate = todo["endDate"]

    beginDate = dt.datetime.strptime(beginDate, '%Y-%m-%d %H:%M:%S')
    endDate = dt.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')

    dates = pd.date_range(beginDate, endDate, freq='MS')

    date_list = []
    for i in dates:
        date_list.append(i.to_pydatetime())

    data1 = {site1: {Key1: None for Key1 in date_list}}

    month_iterator = beginDate

    count = len(todo_list)
    for i in range(count):
        value = todo_list[i]
        data1[site1][month_iterator] = value
        month_iterator = month_iterator + relativedelta(months=+1)

    # site 2

    http = http.replace(site1, '$TRIPLET$')

    http = http.replace('$TRIPLET$', site2)

    response = requests.get(http)

    todo = json.loads(response.text)

    todo_list = todo['values']
    beginDate = todo["beginDate"]
    endDate = todo["endDate"]

    beginDate = dt.datetime.strptime(beginDate, '%Y-%m-%d %H:%M:%S')
    endDate = dt.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')

    dates = pd.date_range(beginDate, endDate, freq='MS')

    date_list = []
    for i in dates:
        date_list.append(i.to_pydatetime())

    data2 = {site2: {Key1: None for Key1 in date_list}}

    month_iterator = beginDate

    count = len(todo_list)
    for i in range(count):
        value = todo_list[i]
        data2[site2][month_iterator] = value
        month_iterator = month_iterator + relativedelta(months=+1)

    # create dataframes and join

    df1 = pd.DataFrame.from_dict(data1, dtype='float')
    df2 = pd.DataFrame.from_dict(data2, dtype='float')

    df = df1.join(df2)
    df = df.dropna()

    df.index = pd.to_datetime(df.index, format='%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%Y')
    df = df.reset_index()
    df.rename(columns={'index': 'DATE'}, inplace=True)

    return df


all_SNOTEL_old = [
    {'label': 'Badger Pass', 'value': '307_MT_SNTL'},
    {'label': 'Bald Mtn.', 'value': '309_WY_SNTL'},
    {'label': 'Banfield Mountain', 'value': '311_MT_SNTL'},
    {'label': 'Barker Lakes', 'value': '313_MT_SNTL'},
    {'label': 'Basin Creek', 'value': '315_MT_SNTL'},
    {'label': 'Beagle Springs', 'value': '318_MT_SNTL'},
    {'label': 'Bear Trap Meadow', 'value': '325_WY_SNTL'},
    {'label': 'Beartooth Lake', 'value': '326_WY_SNTL'},
    {'label': 'Beaver Creek', 'value': '328_MT_SNTL'},
    {'label': 'Bisson Creek', 'value': '346_MT_SNTL'},
    {'label': 'Black Bear', 'value': '347_MT_SNTL'},
    {'label': 'Black Pine', 'value': '349_MT_SNTL'},
    {'label': 'Blackwater', 'value': '350_WY_SNTL'},
    {'label': 'Blind Park', 'value': '354:SD:SNTL'},
    {'label': 'Bloody Dick', 'value': '355:MT:SNTL'},
    {'label': 'Bone Springs Div', 'value': '358:WY:SNTL'},
    {'label': 'Boulder Mountain', 'value': '360:MT:SNTL'},
    {'label': 'Box Canyon', 'value': '363:MT:SNTL'},
    {'label': 'Brackett Creek', 'value': '365:MT:SNTL'},
    {'label': 'Burgess Junction', 'value': '377:WY:SNTL'},
    {'label': 'Burroughs Creek', 'value': '379:WY:SNTL'},
    {'label': 'Calvert Creek', 'value': '381:MT:SNTL'},
    {'label': 'Canyon', 'value': '384:WY:SNTL'},
    {'label': 'Carrot Basin', 'value': '385:MT:SNTL'},
    {'label': 'Cloud Peak Reservoir', 'value': '402:WY:SNTL'},
    {'label': 'Clover Meadow', 'value': '403:MT:SNTL'},
    {'label': 'Cold Springs', 'value': '405:WY:SNTL'},
    {'label': 'Cole Creek', 'value': '407:MT:SNTL'},
    {'label': 'Combination', 'value': '410:MT:SNTL'},
    {'label': 'Copper Bottom', 'value': '413:MT:SNTL'},
    {'label': 'Copper Camp', 'value': '414:MT:SNTL'},
    {'label': 'Crystal Lake', 'value': '427:MT:SNTL'},
    {'label': 'Daly Creek', 'value': '433:MT:SNTL'},
    {'label': 'Darkhorse Lake', 'value': '436:MT:SNTL'},
    {'label': 'Deadman Creek', 'value': '437:MT:SNTL'},
    {'label': 'Divide', 'value': '448:MT:SNTL'},
    {'label': 'Dome Lake', 'value': '451:WY:SNTL'},
    {'label': 'Dupuyer Creek', 'value': '458:MT:SNTL'},
    {'label': 'Emery Creek', 'value': '469:MT:SNTL'},
    {'label': 'Evening Star', 'value': '472:WY:SNTL'},
    {'label': 'Fisher Creek', 'value': '480:MT:SNTL'},
    {'label': 'Flattop Mtn.', 'value': '482:MT:SNTL'},
    {'label': 'Frohner Meadow', 'value': '487:MT:SNTL'},
    {'label': 'Grave Creek', 'value': '500:MT:SNTL'},
    {'label': 'Grave Springs', 'value': '501:WY:SNTL'},
    {'label': 'Hand Creek', 'value': '510:MT:SNTL'},
    {'label': 'Hansen Sawmill', 'value': '512:WY:SNTL'},
    {'label': 'Hawkins Lake', 'value': '516:MT:SNTL'},
    {'label': 'Hobbs Park', 'value': '525:WY:SNTL'},
    {'label': 'Hoodoo Basin', 'value': '530:MT:SNTL'},
    {'label': 'Kirwin', 'value': '560:WY:SNTL'},
    {'label': 'Kraft Creek', 'value': '562:MT:SNTL'},
    {'label': 'Lakeview Ridge', 'value': '568:MT:SNTL'},
    {'label': 'Lemhi Ridge', 'value': '576:MT:SNTL'},
    {'label': 'Lick Creek', 'value': '578:MT:SNTL'},
    {'label': 'Little Warm', 'value': '585:WY:SNTL'},
    {'label': 'Lone Mountain', 'value': '590:MT:SNTL'},
    {'label': 'Lower Twin', 'value': '603:MT:SNTL'},
    {'label': 'Lubrecht Flume', 'value': '604:MT:SNTL'},
    {'label': 'Madison Plateau', 'value': '609:MT:SNTL'},
    {'label': 'Many Glacier', 'value': '613:MT:SNTL'},
    {'label': 'Marquette', 'value': '616:WY:SNTL'},
    {'label': 'Middle Powder', 'value': '625:WY:SNTL'},
    {'label': 'Monument Peak', 'value': '635:MT:SNTL'},
    {'label': 'Moss Peak', 'value': '646:MT:SNTL'},
    {'label': 'Mount Lockhart', 'value': '649:MT:SNTL'},
    {'label': 'Mule Creek', 'value': '656:MT:SNTL'},
    {'label': 'N Fk Elk Creek', 'value': '657:MT:SNTL'},
    {'label': 'Nez Perce Camp', 'value': '662:MT:SNTL'},
    {'label': 'Noisy Basin', 'value': '664:MT:SNTL'},
    {'label': 'North Fork Jocko', 'value': '667:MT:SNTL'},
    {'label': 'Northeast Entrance', 'value': '670:MT:SNTL'},
    {'label': 'Owl Creek', 'value': '676:WY:SNTL'},
    {'label': 'Parker Peak', 'value': '683:WY:SNTL'},
    {'label': 'Pickfoot Creek', 'value': '690:MT:SNTL'},
    {'label': 'Pike Creek', 'value': '693:MT:SNTL'},
    {'label': 'Placer Basin', 'value': '696:MT:SNTL'},
    {'label': 'Porcupine', 'value': '700:MT:SNTL'},
    {'label': 'Powder River Pass', 'value': '703:WY:SNTL'},
    {'label': 'Rocker Peak', 'value': '722:MT:SNTL'},
    {'label': 'S Fork Shields', 'value': '725:MT:SNTL'},
    {'label': 'Saddle Mtn.', 'value': '727:MT:SNTL'},
    {'label': 'Shell Creek', 'value': '751:WY:SNTL'},
    {'label': 'Short Creek', 'value': '753:MT:SNTL'},
    {'label': 'Shower Falls', 'value': '754:MT:SNTL'},
    {'label': 'Skalkaho Summit', 'value': '760:MT:SNTL'},
    {'label': 'South Pass', 'value': '775:WY:SNTL'},
    {'label': 'Spur Park', 'value': '781:MT:SNTL'},
    {'label': 'Sleeping Woman', 'value': '783:MT:SNTL'},
    {'label': 'St. Lawrence Alt', 'value': '786:WY:SNTL'},
    {'label': 'Stahl Peak', 'value': '787:MT:SNTL'},
    {'label': 'Sucker Creek', 'value': '798:WY:SNTL'},
    {'label': 'Sylvan Lake', 'value': '806:WY:SNTL'},
    {'label': 'Sylvan Road', 'value': '807:WY:SNTL'},
    {'label': 'Tepee Creek', 'value': '813:MT:SNTL'},
    {'label': 'Tie Creek', 'value': '818:WY:SNTL'},
    {'label': 'Timber Creek', 'value': '819:WY:SNTL'},
    {'label': 'Togwotee Pass', 'value': '822:WY:SNTL'},
    {'label': 'Townsend Creek', 'value': '826:WY:SNTL'},
    {'label': 'Twelvemile Creek', 'value': '835:MT:SNTL'},
    {'label': 'Twin Lakes', 'value': '836:MT:SNTL'},
    {'label': 'Waldron', 'value': '847:MT:SNTL'},
    {'label': 'Warm Springs', 'value': '850:MT:SNTL'},
    {'label': 'Whiskey Creek', 'value': '858:MT:SNTL'},
    {'label': 'White Mill', 'value': '862:MT:SNTL'},
    {'label': 'Wolverine', 'value': '875:WY:SNTL'},
    {'label': 'Wood Creek', 'value': '876:MT:SNTL'},
    {'label': 'Younts Peak', 'value': '878:WY:SNTL'},
    {'label': 'Tizer Basin', 'value': '893:MT:SNTL'},
    {'label': 'Stuart Mountain', 'value': '901:MT:SNTL'},
    {'label': 'Nevada Ridge', 'value': '903:MT:SNTL'},
    {'label': 'Albro Lake', 'value': '916:MT:SNTL'},
    {'label': 'Rocky Boy', 'value': '917:MT:SNTL'},
    {'label': 'Garver Creek', 'value': '918:MT:SNTL'},
    {'label': 'Daisy Peak', 'value': '919:MT:SNTL'},
    {'label': 'North Rapid Creek', 'value': '920:SD:SNTL'},
    {'label': 'Deer Park', 'value': '923:WY:SNTL'},
    {'label': 'West Yellowstone', 'value': '924:MT:SNTL'},
    {'label': 'Sacajawea', 'value': '929:MT:SNTL'},
    {'label': 'Peterson Meadows', 'value': '930:MT:SNTL'},
    {'label': 'Big Goose', 'value': '931:WY:SNTL'},
    {'label': 'Poorman Creek', 'value': '932:MT:SNTL'},
    {'label': 'Burnt Mtn', 'value': '981:MT:SNTL'},
    {'label': 'Cole Canyon', 'value': '982:WY:SNTL'},
    {'label': 'Onion Park', 'value': '1008:MT:SNTL'},
    {'label': 'Stringer Creek', 'value': '1009:MT:SNTL'},
    {'label': 'East Boulder Mine', 'value': '1105:MT:SNTL'},
    {'label': 'Elk Peak', 'value': '1106:MT:SNTL'},
    {'label': 'Castle Creek', 'value': '1130:WY:SNTL'},
    {'label': 'Little Goose', 'value': '1131:WY:SNTL'},
    {'label': 'Soldier Park', 'value': '1132:WY:SNTL'},
    {'label': 'Blacktail Mtn', 'value': '1144:MT:SNTL'},
    {'label': 'JL Meadow', 'value': '1287:MT:SNTL'},
]

all_SNOTEL = [
    {'label': 'Above Gilmore SNOW', 'value': '13E19_ID_SNOW'},
    {'label': 'Above Roland SNOW', 'value': '15B07_ID_SNOW'},
    {'label': 'Albany SNOW', 'value': '06H11_WY_SNOW'},
    {'label': 'Albro Lake SNTL', 'value': '916_MT_SNTL'},
    {'label': 'Allen Ranch SNOW', 'value': '11G35_ID_SNOW'},
    {'label': 'Arch Falls SNOW', 'value': '10D14_MT_SNOW'},
    {'label': 'Ashley Divide SNOW', 'value': '14A19_MT_SNOW'},
    {'label': 'Aster Creek SNOW', 'value': '10E08_WY_SNOW'},
    {'label': 'Atlanta Summit SNTL', 'value': '306_ID_SNTL'},
    {'label': 'Bad Bear SNOW', 'value': '15F02_ID_SNOW'},
    {'label': 'Badger Gulch SNOW', 'value': '14G03_ID_SNOW'},
    {'label': 'Badger Pass SNTL', 'value': '307_MT_SNTL'},
    {'label': 'Bald Mtn. SNTL', 'value': '309_WY_SNTL'},
    {'label': 'Banfield Mountain SNTL', 'value': '311_MT_SNTL'},
    {'label': 'Banner Summit SNTL', 'value': '312_ID_SNTL'},
    {'label': 'Baree Creek SNOW', 'value': '15B11_MT_SNOW'},
    {'label': 'Baree Midway SNOW', 'value': '15B16_MT_SNOW'},
    {'label': 'Baree Trail SNOW', 'value': '15B15_MT_SNOW'},
    {'label': 'Barker Lakes SNTL', 'value': '313_MT_SNTL'},
    {'label': 'Base Camp SNTL', 'value': '314_WY_SNTL'},
    {'label': 'Base Camp SNOW', 'value': '10F02_WY_SNOW'},
    {'label': 'Basin Creek SNTL', 'value': '315_MT_SNTL'},
    {'label': 'Basin Creek SNOW', 'value': '12D09_MT_SNOW'},
    {'label': 'Bassoo Peak SNOW', 'value': '14B03_MT_SNOW'},
    {'label': 'Battle Creek AM SNOW', 'value': '16G09_ID_SNOW'},
    {'label': 'Battle Mountain SNTL', 'value': '317_WY_SNTL'},
    {'label': 'Beagle Springs SNTL', 'value': '318_MT_SNTL'},
    {'label': 'Bear Basin SNTL', 'value': '319_ID_SNTL'},
    {'label': 'Bear Canyon SNTL', 'value': '320_ID_SNTL'},
    {'label': 'Bear Lodge Divide SNOW', 'value': '04E02_WY_SNOW'},
    {'label': 'Bear Mountain SNTL', 'value': '323_ID_SNTL'},
    {'label': 'Bear Saddle SNTL', 'value': '324_ID_SNTL'},
    {'label': 'Bear Trap Meadow SNTL', 'value': '325_WY_SNTL'},
    {'label': 'Beartooth Lake SNTL', 'value': '326_WY_SNTL'},
    {'label': 'Beaver Creek SNTL', 'value': '328_MT_SNTL'},
    {'label': 'Benton Meadow SNOW', 'value': '16A02_ID_SNOW'},
    {'label': 'Benton Spring SNOW', 'value': '16A03_ID_SNOW'},
    {'label': 'Big Creek Summit SNTL', 'value': '338_ID_SNTL'},
    {'label': 'Big Goose SNTL', 'value': '931_WY_SNTL'},
    {'label': 'Big Park SNOW', 'value': '10G11_WY_SNOW'},
    {'label': 'Big Sandy Opening SNTL', 'value': '342_WY_SNTL'},
    {'label': 'Big Snowy SNOW', 'value': '09C05_MT_SNOW'},
    {'label': 'Big Springs SNOW', 'value': '11E09_ID_SNOW'},
    {'label': 'Bisson Creek SNTL', 'value': '346_MT_SNTL'},
    {'label': 'Black Bear SNTL', 'value': '347_MT_SNTL'},
    {'label': 'Black Mountain SNOW', 'value': '12C19_MT_SNOW'},
    {'label': 'Black Pine SNTL', 'value': '349_MT_SNTL'},
    {'label': 'Blackhall Mtn SNTL', 'value': '1119_WY_SNTL'},
    {'label': 'Blacktail SNOW', 'value': '14B04_MT_SNOW'},
    {'label': 'Blacktail Mtn SNTL', 'value': '1144_MT_SNTL'},
    {'label': 'Blackwater SNTL', 'value': '350_WY_SNTL'},
    {'label': 'Blind Bull Sum SNTL', 'value': '353_WY_SNTL'},
    {'label': 'Blind Park SNTL', 'value': '354_SD_SNTL'},
    {'label': 'Bloody Dick SNTL', 'value': '355_MT_SNTL'},
    {'label': 'Blue Ridge SNOW', 'value': '11F17_ID_SNOW'},
    {'label': 'Blue Ridge SNOW', 'value': '08G02_WY_SNOW'},
    {'label': 'Bogus Basin SNTL', 'value': '978_ID_SNTL'},
    {'label': 'Bogus Basin SNOW', 'value': '16F02_ID_SNOW'},
    {'label': 'Bogus Basin Road SNOW', 'value': '16F04_ID_SNOW'},
    {'label': 'Bone SNOW', 'value': '11F08_ID_SNOW'},
    {'label': 'Bone Springs Div SNTL', 'value': '358_WY_SNTL'},
    {'label': 'Bostetter R.S. SNTL', 'value': '359_ID_SNTL'},
    {'label': 'Bots Sots SNOW', 'value': '09D14_MT_SNOW'},
    {'label': 'Boulder Mountain SNTL', 'value': '360_MT_SNTL'},
    {'label': 'Box Canyon SNTL', 'value': '363_MT_SNTL'},
    {'label': 'Boxelder Creek SNOW', 'value': '09A08_MT_SNOW'},
    {'label': 'Boy Scout Camp SNOW', 'value': '13G02_ID_SNOW'},
    {'label': 'Brackett Creek SNTL', 'value': '365_MT_SNTL'},
    {'label': 'Branham Lakes SNOW', 'value': '11D14_MT_SNOW'},
    {'label': 'Bristow Creek SNOW', 'value': '15A10_MT_SNOW'},
    {'label': 'Brooklyn Lake SNTL', 'value': '367_WY_SNTL'},
    {'label': 'Brundage Reservoir SNTL', 'value': '370_ID_SNTL'},
    {'label': 'Bruno Creek SNOW', 'value': '14E08_ID_SNOW'},
    {'label': 'Brush Creek Timber SNOW', 'value': '14A13_MT_SNOW'},
    {'label': 'Bull Basin AM SNOW', 'value': '16G10_ID_SNOW'},
    {'label': 'Bull Mountain SNOW', 'value': '12D08_MT_SNOW'},
    {'label': 'Burgess Junction SNTL', 'value': '377_WY_SNTL'},
    {'label': 'Burnt Mtn SNTL', 'value': '981_MT_SNTL'},
    {'label': 'Burroughs Creek SNTL', 'value': '379_WY_SNTL'},
    {'label': 'Cabin Creek SNOW', 'value': '12B06_MT_SNOW'},
    {'label': 'Calvert Creek SNTL', 'value': '381_MT_SNTL'},
    {'label': 'Camas Creek Divide SNTL', 'value': '382_ID_SNTL'},
    {'label': 'Camp Creek SNOW', 'value': '12E03_ID_SNOW'},
    {'label': 'Camp Senia SNOW', 'value': '09D01_MT_SNOW'},
    {'label': 'Canyon SNTL', 'value': '384_WY_SNTL'},
    {'label': 'Carrot Basin SNTL', 'value': '385_MT_SNTL'},
    {'label': 'Casper Mtn. SNTL', 'value': '389_WY_SNTL'},
    {'label': 'Castle Creek SNOW', 'value': '09F20_WY_SNOW'},
    {'label': 'Castle Creek SNTL', 'value': '1130_WY_SNTL'},
    {'label': 'Ccc Camp SNOW', 'value': '10G07_WY_SNOW'},
    {'label': 'Chessman Reservoir SNOW', 'value': '12C05_MT_SNOW'},
    {'label': 'Chicago Ridge SNOW', 'value': '15B22_MT_SNOW'},
    {'label': 'Chicken Creek SNOW', 'value': '14A15_MT_SNOW'},
    {'label': 'Chimney Creek SNOW', 'value': '15F15_ID_SNOW'},
    {'label': 'Chocolate Gulch SNTL', 'value': '895_ID_SNTL'},
    {'label': 'Cinnabar Park SNTL', 'value': '1046_WY_SNTL'},
    {'label': 'Cloud Peak Reservoir SNTL', 'value': '402_WY_SNTL'},
    {'label': 'Clover Meadow SNTL', 'value': '403_MT_SNTL'},
    {'label': 'Cold Springs SNTL', 'value': '405_WY_SNTL'},
    {'label': 'Cole Canyon SNTL', 'value': '982_WY_SNTL'},
    {'label': 'Cole Creek SNTL', 'value': '407_MT_SNTL'},
    {'label': 'Colley Creek SNOW', 'value': '10D30_MT_SNOW'},
    {'label': 'Combination SNTL', 'value': '410_MT_SNTL'},
    {'label': 'Cool Creek SNTL', 'value': '411_ID_SNTL'},
    {'label': 'Copes Camp SNOW', 'value': '13E17_ID_SNOW'},
    {'label': 'Copper Basin SNOW', 'value': '13F02_ID_SNOW'},
    {'label': 'Copper Bottom SNTL', 'value': '413_MT_SNTL'},
    {'label': 'Copper Camp SNTL', 'value': '414_MT_SNTL'},
    {'label': 'Copper Mountain SNOW', 'value': '12C09_MT_SNOW'},
    {'label': 'Cottonwood Creek SNOW', 'value': '12C17_MT_SNOW'},
    {'label': 'Cottonwood Creek SNTL', 'value': '419_WY_SNTL'},
    {'label': 'Couch Summit SNTL', 'value': '1306_ID_SNTL'},
    {'label': 'Couch Summit #2 SNOW', 'value': '14F18_ID_SNOW'},
    {'label': 'Cougar Point SNOW', 'value': '14D06_ID_SNOW'},
    {'label': 'Coyote Hill SNOW', 'value': '13B10_MT_SNOW'},
    {'label': 'Cozy Cove SNTL', 'value': '423_ID_SNTL'},
    {'label': 'Crab Creek SNTL', 'value': '424_ID_SNTL'},
    {'label': 'Crater Meadows SNTL', 'value': '425_ID_SNTL'},
    {'label': 'Crevice Mountain SNOW', 'value': '10D05_MT_SNOW'},
    {'label': 'Crooked Fork SNOW', 'value': '14C11_ID_SNOW'},
    {'label': 'Crow Creek SNTL', 'value': '1045_WY_SNTL'},
    {'label': 'Crystal Lake SNTL', 'value': '427_MT_SNTL'},
    {'label': 'Daisy Peak SNTL', 'value': '919_MT_SNTL'},
    {'label': 'Daly Creek SNTL', 'value': '433_MT_SNTL'},
    {'label': 'Daniels Creek SNOW', 'value': '12G12_ID_SNOW'},
    {'label': 'Darby Canyon SNOW', 'value': '10F21_WY_SNOW'},
    {'label': 'Darkhorse Lake SNTL', 'value': '436_MT_SNTL'},
    {'label': 'Deadman Creek SNTL', 'value': '437_MT_SNTL'},
    {'label': 'Deadman Gulch SNOW', 'value': '16F01_ID_SNOW'},
    {'label': 'Deadwood Summit SNTL', 'value': '439_ID_SNTL'},
    {'label': 'Deep Lake SNOW', 'value': '06H17_WY_SNOW'},
    {'label': 'Deer Park SNTL', 'value': '923_WY_SNTL'},
    {'label': 'Democrat Creek SNOW', 'value': '16F13_ID_SNOW'},
    {'label': 'Desert Mountain SNOW', 'value': '13A02_MT_SNOW'},
    {'label': 'Discovery Basin SNOW', 'value': '13C42_MT_SNOW'},
    {'label': 'Ditch Creek SNOW', 'value': '03F04_SD_SNOW'},
    {'label': 'Divide SNTL', 'value': '448_MT_SNTL'},
    {'label': 'Divide Peak SNTL', 'value': '449_WY_SNTL'},
    {'label': 'Dix Hill SNOW', 'value': '12C15_MT_SNOW'},
    {'label': 'Dobson Creek SNOW', 'value': '16F12_ID_SNOW'},
    {'label': 'Dodson Pass SNOW', 'value': '16E15_ID_SNOW'},
    {'label': 'Dollarhide Summit SNTL', 'value': '450_ID_SNTL'},
    {'label': 'Dome Lake SNTL', 'value': '451_WY_SNTL'},
    {'label': 'Dry Basin SNOW', 'value': '11G14_ID_SNOW'},
    {'label': 'Dry Fork SNOW', 'value': '13F20_ID_SNOW'},
    {'label': 'Dunoir SNOW', 'value': '09F06_WY_SNOW'},
    {'label': 'Dupuyer Creek SNTL', 'value': '458_MT_SNTL'},
    {'label': 'Eagle Creek SNOW', 'value': '10C13_MT_SNOW'},
    {'label': 'East Boulder Mine SNTL', 'value': '1105_MT_SNTL'},
    {'label': 'East Creek SNOW', 'value': '11G34_ID_SNOW'},
    {'label': 'East Fork R.S. SNOW', 'value': '13D01_MT_SNOW'},
    {'label': 'East Rim Divide SNTL', 'value': '460_WY_SNTL'},
    {'label': 'El Dorado Mine SNOW', 'value': '13C09_MT_SNOW'},
    {'label': 'Elbo Ranch SNOW', 'value': '10F28_WY_SNOW'},
    {'label': 'Elk Butte SNTL', 'value': '466_ID_SNTL'},
    {'label': 'Elk Horn Springs SNOW', 'value': '13D15_MT_SNOW'},
    {'label': 'Elk Peak SNOW', 'value': '10C07_MT_SNOW'},
    {'label': 'Elk Peak SNTL', 'value': '1106_MT_SNTL'},
    {'label': 'Elkhart Park G.S. SNTL', 'value': '468_WY_SNTL'},
    {'label': 'Emery Creek SNTL', 'value': '469_MT_SNTL'},
    {'label': 'Emigrant Summit SNTL', 'value': '471_ID_SNTL'},
    {'label': 'Emigration Canyon SNOW', 'value': '11G07_ID_SNOW'},
    {'label': 'Evening Star SNTL', 'value': '472_WY_SNTL'},
    {'label': 'Fall Creek SNOW', 'value': '11F19_ID_SNOW'},
    {'label': 'Fatty Creek SNOW', 'value': '13B04_MT_SNOW'},
    {'label': 'Fish Ck SNTL', 'value': '1305_ID_SNTL'},
    {'label': 'Fish Creek SNOW', 'value': '12D10_MT_SNOW'},
    {'label': 'Fish Lake Airstrip SNOW', 'value': '15C02_ID_SNOW'},
    {'label': 'Fisher Creek SNTL', 'value': '480_MT_SNTL'},
    {'label': 'Flattop Mtn. SNTL', 'value': '482_MT_SNTL'},
    {'label': 'Fleecer Ridge SNOW', 'value': '12D07_MT_SNOW'},
    {'label': 'Foolhen SNOW', 'value': '13D21_MT_SNOW'},
    {'label': 'Forest Lake SNOW', 'value': '10C14_MT_SNOW'},
    {'label': 'Four Mile SNOW', 'value': '11D12_MT_SNOW'},
    {'label': 'Four Mile Meadow SNOW', 'value': '10F06_WY_SNOW'},
    {'label': 'Fourth Of July Summit SNOW', 'value': '16B03_ID_SNOW'},
    {'label': 'Fox Park #2 SNOW', 'value': '06H24_WY_SNOW'},
    {'label': 'Foxpark SNOW', 'value': '06H12_WY_SNOW'},
    {'label': 'Franklin Basin SNTL', 'value': '484_ID_SNTL'},
    {'label': 'Freight Creek SNOW', 'value': '12A01_MT_SNOW'},
    {'label': 'Frohner Meadow SNTL', 'value': '487_MT_SNTL'},
    {'label': 'Galena SNTL', 'value': '489_ID_SNTL'},
    {'label': 'Galena Summit SNTL', 'value': '490_ID_SNTL'},
    {'label': 'Garfield R.S. SNTL', 'value': '492_ID_SNTL'},
    {'label': 'Garver Creek SNTL', 'value': '918_MT_SNTL'},
    {'label': 'Geyser Creek SNOW', 'value': '09F07_WY_SNOW'},
    {'label': 'Giveout SNTL', 'value': '493_ID_SNTL'},
    {'label': 'Glade Creek SNOW', 'value': '10E13_WY_SNOW'},
    {'label': 'Government Saddle SNOW', 'value': '15B23_MT_SNOW'},
    {'label': 'Graham Guard Sta. SNTL', 'value': '496_ID_SNTL'},
    {'label': 'Grand Targhee SNTL', 'value': '1082_WY_SNTL'},
    {'label': 'Granite Creek SNTL', 'value': '497_WY_SNTL'},
    {'label': 'Grannier Meadows SNOW', 'value': '08G04_WY_SNOW'},
    {'label': 'Grasshopper SNOW', 'value': '10C02_MT_SNOW'},
    {'label': 'Grassy Lake SNTL', 'value': '499_WY_SNTL'},
    {'label': 'Grassy Lake SNOW', 'value': '10E15_WY_SNOW'},
    {'label': 'Grave Creek SNTL', 'value': '500_MT_SNTL'},
    {'label': 'Grave Springs SNTL', 'value': '501_WY_SNTL'},
    {'label': 'Griffin Creek Divide SNOW', 'value': '14A09_MT_SNOW'},
    {'label': 'Gros Ventre Summit SNTL', 'value': '506_WY_SNTL'},
    {'label': 'Grover Park Divide SNOW', 'value': '10G03_WY_SNOW'},
    {'label': 'Gunsight Pass SNTL', 'value': '944_WY_SNTL'},
    {'label': 'Hahn Homestead SNOW', 'value': '13E29_ID_SNOW'},
    {'label': 'Hairpin Turn SNOW', 'value': '06H02_WY_SNOW'},
    {'label': 'Hams Fork SNTL', 'value': '509_WY_SNTL'},
    {'label': 'Hand Creek SNTL', 'value': '510_MT_SNTL'},
    {'label': 'Hansen Sawmill SNTL', 'value': '512_WY_SNTL'},
    {'label': 'Haskins Creek SNOW', 'value': '07H01_WY_SNOW'},
    {'label': 'Hawkins Lake SNTL', 'value': '516_MT_SNTL'},
    {'label': 'Haymaker SNOW', 'value': '10C11_MT_SNOW'},
    {'label': 'Hebgen Dam SNOW', 'value': '11E05_MT_SNOW'},
    {'label': 'Hell Roaring Divide SNOW', 'value': '14A03_MT_SNOW'},
    {'label': 'Hemlock Butte SNTL', 'value': '520_ID_SNTL'},
    {'label': 'Herrig Junction SNOW', 'value': '14A16_MT_SNOW'},
    {'label': 'Hidden Lake SNTL', 'value': '988_ID_SNTL'},
    {'label': 'Highwood Divide SNOW', 'value': '10B02_MT_SNOW'},
    {'label': 'Highwood Station SNOW', 'value': '10B01_MT_SNOW'},
    {'label': 'Hilts Creek SNTL', 'value': '524_ID_SNTL'},
    {'label': 'Hoback GS SNOW', 'value': '10F30_WY_SNOW'},
    {'label': 'Hobbs Park SNTL', 'value': '525_WY_SNTL'},
    {'label': 'Holbrook SNOW', 'value': '13B13_MT_SNOW'},
    {'label': 'Hoodoo Basin SNTL', 'value': '530_MT_SNTL'},
    {'label': 'Howell Canyon SNTL', 'value': '534_ID_SNTL'},
    {'label': 'Huckleberry Divide SNOW', 'value': '10E14_WY_SNOW'},
    {'label': 'Humboldt Gulch SNTL', 'value': '535_ID_SNTL'},
    {'label': 'Hyndman SNTL', 'value': '537_ID_SNTL'},
    {'label': 'Iceberg Lake No 3 SNOW', 'value': '13A03_MT_SNOW'},
    {'label': 'Indian Creek SNTL', 'value': '544_WY_SNTL'},
    {'label': 'Intergaard SNOW', 'value': '13C04_MT_SNOW'},
    {'label': 'Iron Mine Creek SNOW', 'value': '13F10_ID_SNOW'},
    {'label': 'Irving Creek SNOW', 'value': '12E04_ID_SNOW'},
    {'label': 'Island Park SNTL', 'value': '546_ID_SNTL'},
    {'label': 'Jackpine Creek SNOW', 'value': '10F26_WY_SNOW'},
    {'label': 'Jackson Peak SNTL', 'value': '550_ID_SNTL'},
    {'label': 'Jahnke Lake Trail SNOW', 'value': '13D27_MT_SNOW'},
    {'label': 'Jakes Canyon SNOW', 'value': '13E28_ID_SNOW'},
    {'label': 'JL Meadow SNTL', 'value': '1287_MT_SNTL'},
    {'label': 'John Evans Canyon SNOW', 'value': '12G22_ID_SNOW'},
    {'label': 'Johnson Creek SNOW', 'value': '11G36_ID_SNOW'},
    {'label': 'Johnson Park SNOW', 'value': '10C12_MT_SNOW'},
    {'label': 'Josephine Lower No 9 SNOW', 'value': '13A14_MT_SNOW'},
    {'label': 'Kelley R.S. SNTL', 'value': '554_WY_SNTL'},
    {'label': 'Kellogg Peak SNOW', 'value': '16B05_ID_SNOW'},
    {'label': 'Kendall R.S. SNTL', 'value': '555_WY_SNTL'},
    {'label': 'Ketchum R S SNOW', 'value': '14F21_ID_SNOW'},
    {'label': 'Kilgore SNOW', 'value': '11E12_ID_SNOW'},
    {'label': 'Kings Hill SNOW', 'value': '10C01_MT_SNOW'},
    {'label': 'Kirwin SNTL', 'value': '560_WY_SNTL'},
    {'label': 'Kishenehn SNOW', 'value': '14A06_MT_SNOW'},
    {'label': 'Kraft Creek SNTL', 'value': '562_MT_SNTL'},
    {'label': 'Lake Camp SNOW', 'value': '10E04_WY_SNOW'},
    {'label': 'Lake Fork SNOW', 'value': '15E01_ID_SNOW'},
    {'label': 'Lakeview Canyon SNOW', 'value': '11E04_MT_SNOW'},
    {'label': 'Lakeview Ridge SNTL', 'value': '568_MT_SNTL'},
    {'label': 'Langford Flat Creek SNOW', 'value': '14G08_ID_SNOW'},
    {'label': 'Laprele Creek SNTL', 'value': '571_WY_SNTL'},
    {'label': 'Larsen Creek SNOW', 'value': '09G06_WY_SNOW'},
    {'label': 'Larsen Creek SNTL', 'value': '1134_WY_SNTL'},
    {'label': 'Latham Springs SNOW', 'value': '11E16_ID_SNOW'},
    {'label': 'Lava Creek SNOW', 'value': '11F15_ID_SNOW'},
    {'label': 'Lemhi Ridge SNTL', 'value': '576_MT_SNTL'},
    {'label': 'Lewis Lake Divide SNTL', 'value': '577_WY_SNTL'},
    {'label': 'Lewis Lake Divide SNOW', 'value': '10E09_WY_SNOW'},
    {'label': 'Libby Lodge SNOW', 'value': '06H03_WY_SNOW'},
    {'label': 'Lick Creek SNTL', 'value': '578_MT_SNTL'},
    {'label': 'Little Bear Run SNOW', 'value': '04F01_WY_SNOW'},
    {'label': 'Little Camas Flat SNOW', 'value': '15F12_ID_SNOW'},
    {'label': 'Little Goose SNTL', 'value': '1131_WY_SNTL'},
    {'label': 'Little Park SNOW', 'value': '11D10_MT_SNOW'},
    {'label': 'Little Snake River SNTL', 'value': '1047_WY_SNTL'},
    {'label': 'Little Warm SNTL', 'value': '585_WY_SNTL'},
    {'label': 'Logan Creek SNOW', 'value': '14A05_MT_SNOW'},
    {'label': 'Logger Springs SNOW', 'value': '13G03_ID_SNOW'},
    {'label': 'Lolo Pass SNTL', 'value': '588_ID_SNTL'},
    {'label': 'Lone Mountain SNTL', 'value': '590_MT_SNTL'},
    {'label': 'Long Valley SNTL', 'value': '1016_ID_SNTL'},
    {'label': 'Lookout SNTL', 'value': '594_ID_SNTL'},
    {'label': 'Loomis Park SNTL', 'value': '597_WY_SNTL'},
    {'label': 'Lost Lake SNTL', 'value': '600_ID_SNTL'},
    {'label': 'Lost-Wood Divide SNTL', 'value': '601_ID_SNTL'},
    {'label': 'Lower Pebble SNOW', 'value': '12G06_ID_SNOW'},
    {'label': 'Lower Sands Creek #2 SNOW', 'value': '16B13_ID_SNOW'},
    {'label': 'Lower Twin SNTL', 'value': '603_MT_SNTL'},
    {'label': 'Lubrecht Flume SNTL', 'value': '604_MT_SNTL'},
    {'label': 'Lubrecht Forest No 3 SNOW', 'value': '13C21_MT_SNOW'},
    {'label': 'Lubrecht Forest No 4 SNOW', 'value': '13C22_MT_SNOW'},
    {'label': 'Lubrecht Forest No 6 SNOW', 'value': '13C08_MT_SNOW'},
    {'label': 'Lubrecht Hydroplot SNOW', 'value': '13C37_MT_SNOW'},
    {'label': 'Lucky Dog SNOW', 'value': '11E14_ID_SNOW'},
    {'label': 'Lupine Creek SNOW', 'value': '10E01_WY_SNOW'},
    {'label': 'Madison Plateau SNTL', 'value': '609_MT_SNTL'},
    {'label': 'Magic Mountain SNTL', 'value': '610_ID_SNTL'},
    {'label': 'Mallo SNOW', 'value': '04E05_WY_SNOW'},
    {'label': 'Many Glacier SNTL', 'value': '613_MT_SNTL'},
    {'label': 'Marias Pass SNOW', 'value': '13A05_MT_SNOW'},
    {'label': 'Marquette SNTL', 'value': '616_WY_SNTL'},
    {'label': 'McCall U Of I Campus SNOW', 'value': '16E20_ID_SNOW'},
    {'label': 'McRenolds Reservoir SNOW', 'value': '11F12_ID_SNOW'},
    {'label': 'Meadow Lake SNTL', 'value': '620_ID_SNTL'},
    {'label': 'Med Bow SNTL', 'value': '1196_WY_SNTL'},
    {'label': 'Medicine Lodge Lakes SNOW', 'value': '07E24_WY_SNOW'},
    {'label': 'Mesa Ditch SNOW', 'value': '16E19_ID_SNOW'},
    {'label': 'Mica Creek SNTL', 'value': '623_ID_SNTL'},
    {'label': 'Middle Fork SNOW', 'value': '08G06_WY_SNOW'},
    {'label': 'Middle Mill Creek SNOW', 'value': '11D15_MT_SNOW'},
    {'label': 'Middle Powder SNTL', 'value': '625_WY_SNTL'},
    {'label': 'Mill Creek SNOW', 'value': '10D19_MT_SNOW'},
    {'label': 'Mill Creek Summit SNTL', 'value': '627_ID_SNTL'},
    {'label': 'Mineral Creek SNOW', 'value': '13A16_MT_SNOW'},
    {'label': 'Monument Peak SNTL', 'value': '635_MT_SNTL'},
    {'label': 'Moonshine SNTL', 'value': '636_ID_SNTL'},
    {'label': 'Moose Creek SNTL', 'value': '638_ID_SNTL'},
    {'label': 'Moran SNOW', 'value': '10F04_WY_SNOW'},
    {'label': 'Mores Creek Summit SNTL', 'value': '637_ID_SNTL'},
    {'label': 'Mores Creek Summit SNOW', 'value': '15F01_ID_SNOW'},
    {'label': 'Morgan Creek SNTL', 'value': '639_ID_SNTL'},
    {'label': 'Morse Creek Sawmill SNOW', 'value': '13E26_ID_SNOW'},
    {'label': 'Moscow Mountain SNTL', 'value': '989_ID_SNTL'},
    {'label': 'Mosquito Ridge SNTL', 'value': '645_ID_SNTL'},
    {'label': 'Moss Lake SNOW', 'value': '06H16_WY_SNOW'},
    {'label': 'Moss Lake #2 SNOW', 'value': '06H26_WY_SNOW'},
    {'label': 'Moss Peak SNTL', 'value': '646_MT_SNTL'},
    {'label': 'Moulton Reservoir SNOW', 'value': '12C20_MT_SNOW'},
    {'label': 'Mount Allen No 7 SNOW', 'value': '13A07_MT_SNOW'},
    {'label': 'Mount Baldy SNOW', 'value': '14F09_ID_SNOW'},
    {'label': 'Mount Lockhart SNTL', 'value': '649_MT_SNTL'},
    {'label': 'Mount Tom SNOW', 'value': '04E04_WY_SNOW'},
    {'label': 'Mountain Meadows SNTL', 'value': '650_ID_SNTL'},
    {'label': 'Mud Creek SNOW', 'value': '11F14_ID_SNOW'},
    {'label': 'Mud Flat SNTL', 'value': '654_ID_SNTL'},
    {'label': 'Mud Spring SNOW', 'value': '14F20_ID_SNOW'},
    {'label': 'Mudd Lake SNOW', 'value': '13D25_MT_SNOW'},
    {'label': 'Muldoon SNOW', 'value': '13F05_ID_SNOW'},
    {'label': 'Mule Creek SNTL', 'value': '656_MT_SNTL'},
    {'label': 'Myrtle Creek SNTL', 'value': '1053_ID_SNTL'},
    {'label': 'N Fk Elk Creek SNTL', 'value': '657_MT_SNTL'},
    {'label': 'Nevada Ridge SNTL', 'value': '903_MT_SNTL'},
    {'label': 'New Fork Lake SNTL', 'value': '661_WY_SNTL'},
    {'label': 'New World SNOW', 'value': '10D01_MT_SNOW'},
    {'label': 'Nez Perce Camp SNTL', 'value': '662_MT_SNTL'},
    {'label': 'Nez Perce Creek SNOW', 'value': '12C10_MT_SNOW'},
    {'label': 'Nez Perce Pass SNOW', 'value': '14D01_MT_SNOW'},
    {'label': 'Noisy Basin SNTL', 'value': '664_MT_SNTL'},
    {'label': 'Norris Basin SNOW', 'value': '10E19_WY_SNOW'},
    {'label': 'North Barrett Creek SNOW', 'value': '06H05_WY_SNOW'},
    {'label': 'North Crane Creek SNOW', 'value': '16E17_ID_SNOW'},
    {'label': 'North Fork Jocko SNOW', 'value': '13B07_MT_SNOW'},
    {'label': 'North Fork Jocko SNTL', 'value': '667_MT_SNTL'},
    {'label': 'North French Creek SNTL', 'value': '668_WY_SNTL'},
    {'label': 'North Rapid Creek SNTL', 'value': '920_SD_SNTL'},
    {'label': 'North Tongue SNOW', 'value': '07E15_WY_SNOW'},
    {'label': 'Northeast Entrance SNTL', 'value': '670_MT_SNTL'},
    {'label': 'Old Battle SNTL', 'value': '673_WY_SNTL'},
    {'label': 'Old Faithful SNOW', 'value': '10E18_WY_SNOW'},
    {'label': 'Onion Gulch SNOW', 'value': '07E27_WY_SNOW'},
    {'label': 'Onion Park SNTL', 'value': '1008_MT_SNTL'},
    {'label': 'Ophir Park SNOW', 'value': '12C16_MT_SNOW'},
    {'label': 'Owl Creek SNTL', 'value': '676_WY_SNTL'},
    {'label': 'Oxford Spring SNTL', 'value': '677_ID_SNTL'},
    {'label': 'Packsaddle Spring SNOW', 'value': '11F18_ID_SNOW'},
    {'label': 'Parker Peak SNTL', 'value': '683_WY_SNTL'},
    {'label': 'Pebble Creek SNOW', 'value': '12G02_ID_SNOW'},
    {'label': 'Pebble Creek SNTL', 'value': '1299_ID_SNTL'},
    {'label': 'Perreau Meadows SNOW', 'value': '14D05_ID_SNOW'},
    {'label': 'Peterson Meadows SNTL', 'value': '930_MT_SNTL'},
    {'label': 'Phillips Bench SNTL', 'value': '689_WY_SNTL'},
    {'label': 'Pickfoot Creek SNTL', 'value': '690_MT_SNTL'},
    {'label': 'Piegan Pass No 6 SNOW', 'value': '13A06_MT_SNOW'},
    {'label': 'Pierce R.S. SNTL', 'value': '1142_ID_SNTL'},
    {'label': 'Pike Creek SNTL', 'value': '693_MT_SNTL'},
    {'label': 'Pine Creek Pass SNTL', 'value': '695_ID_SNTL'},
    {'label': 'Pipestone Pass SNOW', 'value': '12D01_MT_SNOW'},
    {'label': 'Placer Basin SNTL', 'value': '696_MT_SNTL'},
    {'label': 'Placer Creek SNOW', 'value': '16E02_ID_SNOW'},
    {'label': 'Pocket Creek SNOW', 'value': '09G11_WY_SNOW'},
    {'label': 'Pocket Creek SNTL', 'value': '1133_WY_SNTL'},
    {'label': 'Pole Mountain SNOW', 'value': '05H01_WY_SNOW'},
    {'label': 'Poorman Creek SNTL', 'value': '932_MT_SNTL'},
    {'label': 'Porcupine SNTL', 'value': '700_MT_SNTL'},
    {'label': 'Potomageton Park SNOW', 'value': '11E21_MT_SNOW'},
    {'label': 'Powder River Pass SNTL', 'value': '703_WY_SNTL'},
    {'label': 'Prairie SNTL', 'value': '704_ID_SNTL'},
    {'label': 'Ptarmigan No 8 SNOW', 'value': '13A08_MT_SNOW'},
    {'label': 'Purgatory Gulch SNOW', 'value': '06H18_WY_SNOW'},
    {'label': 'Ragged Mountain SNTL', 'value': '1081_ID_SNTL'},
    {'label': 'Ranger Creek SNOW', 'value': '07E04_WY_SNOW'},
    {'label': 'Rattlesnake Spring SNOW', 'value': '15F19_ID_SNOW'},
    {'label': 'Red Canyon AM SNOW', 'value': '16G11_ID_SNOW'},
    {'label': 'Red Mountain SNOW', 'value': '15A01_MT_SNOW'},
    {'label': 'Reno Hill SNTL', 'value': '716_WY_SNTL'},
    {'label': 'Reuter Canyon SNOW', 'value': '04E03_WY_SNOW'},
    {'label': 'Revais SNOW', 'value': '14B06_MT_SNOW'},
    {'label': 'Reynolds Creek SNTL', 'value': '2029_ID_SNTL'},
    {'label': 'Reynolds Mountain SNOW', 'value': '16F08_ID_SNOW'},
    {'label': 'Reynolds West Fork #1 SNOW', 'value': '16F10_ID_SNOW'},
    {'label': 'Reynolds West Fork #2 SNOW', 'value': '16F09_ID_SNOW'},
    {'label': 'Reynolds-Dobson Divide SNOW', 'value': '16F11_ID_SNOW'},
    {'label': 'Rock Creek Mdws SNOW', 'value': '15B24_MT_SNOW'},
    {'label': 'Rock Creek Meadow SNOW', 'value': '11D21_MT_SNOW'},
    {'label': 'Rocker Peak SNTL', 'value': '722_MT_SNTL'},
    {'label': 'Rocky Boy SNTL', 'value': '917_MT_SNTL'},
    {'label': 'Rocky Boy SNOW', 'value': '09A01_MT_SNOW'},
    {'label': 'Roland Summit SNOW', 'value': '15B05_ID_SNOW'},
    {'label': 'Rowdy Creek SNOW', 'value': '10G21_WY_SNOW'},
    {'label': 'Ryan Park SNOW', 'value': '06H06_WY_SNOW'},
    {'label': 'S Fork Shields SNTL', 'value': '725_MT_SNTL'},
    {'label': 'Sacajawea SNTL', 'value': '929_MT_SNTL'},
    {'label': 'Saddle Mtn. SNTL', 'value': '727_MT_SNTL'},
    {'label': 'Sage Creek Basin SNTL', 'value': '1015_WY_SNTL'},
    {'label': 'Salt River Summit SNTL', 'value': '730_WY_SNTL'},
    {'label': 'Sand Lake SNTL', 'value': '731_WY_SNTL'},
    {'label': 'Sandpoint Exp Stn SNOW', 'value': '16A11_ID_SNOW'},
    {'label': 'Sandstone RS SNTL', 'value': '732_WY_SNTL'},
    {'label': 'Savage Pass SNTL', 'value': '735_ID_SNTL'},
    {'label': 'Sawmill Divide SNOW', 'value': '07E38_WY_SNOW'},
    {'label': 'Schwartz Lake SNTL', 'value': '915_ID_SNTL'},
    {'label': 'Schweitzer Basin SNTL', 'value': '738_ID_SNTL'},
    {'label': 'Secesh Summit SNTL', 'value': '740_ID_SNTL'},
    {'label': 'Sedgwick Peak SNTL', 'value': '741_ID_SNTL'},
    {'label': 'Shanghi Summit SNTL', 'value': '747_ID_SNTL'},
    {'label': 'Sheep Mtn. SNTL', 'value': '749_ID_SNTL'},
    {'label': 'Shell Creek SNTL', 'value': '751_WY_SNTL'},
    {'label': 'Sheridan R.S. (New) SNOW', 'value': '09F15_WY_SNOW'},
    {'label': 'Sherwin SNTL', 'value': '752_ID_SNTL'},
    {'label': 'Shirts Creek SNOW', 'value': '16E16_ID_SNOW'},
    {'label': 'Short Creek SNTL', 'value': '753_MT_SNTL'},
    {'label': 'Shower Falls SNTL', 'value': '754_MT_SNTL'},
    {'label': 'Skalkaho Summit SNTL', 'value': '760_MT_SNTL'},
    {'label': 'Skitwish Ridge SNOW', 'value': '16B11_ID_SNOW'},
    {'label': 'Slag-A-Melt Lake SNOW', 'value': '13D24_MT_SNOW'},
    {'label': 'Slagamelt Lakes SNTL', 'value': '1286_MT_SNTL'},
    {'label': 'Sleeping Woman SNTL', 'value': '783_MT_SNTL'},
    {'label': 'Slide Rock Mountain SNOW', 'value': '13C02_MT_SNOW'},
    {'label': 'Slug Creek Divide SNTL', 'value': '761_ID_SNTL'},
    {'label': 'Smiley Mountain SNTL', 'value': '926_ID_SNTL'},
    {'label': 'Smuggler Mine SNOW', 'value': '12D05_MT_SNOW'},
    {'label': 'Snake River Station SNTL', 'value': '764_WY_SNTL'},
    {'label': 'Snake River Station SNOW', 'value': '10E12_WY_SNOW'},
    {'label': 'Snider Basin SNTL', 'value': '765_WY_SNTL'},
    {'label': 'Snow King Mountain SNOW', 'value': '10F20_WY_SNOW'},
    {'label': 'Soldier Park SNOW', 'value': '07E05_WY_SNOW'},
    {'label': 'Soldier Park SNTL', 'value': '1132_WY_SNTL'},
    {'label': 'Soldier R.S. SNTL', 'value': '769_ID_SNTL'},
    {'label': 'Somsen Ranch SNTL', 'value': '770_ID_SNTL'},
    {'label': 'Sour Dough SNOW', 'value': '06E01_WY_SNOW'},
    {'label': 'South Brush Creek SNTL', 'value': '772_WY_SNTL'},
    {'label': 'South Mtn. SNTL', 'value': '774_ID_SNTL'},
    {'label': 'South Pass SNTL', 'value': '775_WY_SNTL'},
    {'label': 'Spotted Bear Mountain SNOW', 'value': '13B02_MT_SNOW'},
    {'label': 'Spring Creek Divide SNTL', 'value': '779_WY_SNTL'},
    {'label': 'Spring Mountain Canyon SNOW', 'value': '13E30_ID_SNOW'},
    {'label': 'Spur Park SNTL', 'value': '781_MT_SNTL'},
    {'label': 'Squaw Flat SNTL', 'value': '782_ID_SNTL'},
    {'label': 'Squaw Meadow SNOW', 'value': '15D02_ID_SNOW'},
    {'label': 'St. Lawrence Alt SNTL', 'value': '786_WY_SNTL'},
    {'label': 'Stahl Peak SNTL', 'value': '787_MT_SNTL'},
    {'label': 'State Line SNOW', 'value': '11F01_ID_SNOW'},
    {'label': 'Stemple Pass SNOW', 'value': '12C01_MT_SNOW'},
    {'label': 'Stickney Mill SNTL', 'value': '792_ID_SNTL'},
    {'label': 'Storm Lake SNOW', 'value': '13C07_MT_SNOW'},
    {'label': 'Strawberry Creek SNOW', 'value': '11G09_ID_SNOW'},
    {'label': 'Stringer Creek SNTL', 'value': '1009_MT_SNTL'},
    {'label': 'Stryker Basin SNOW', 'value': '14A17_MT_SNOW'},
    {'label': 'Stuart Mountain SNTL', 'value': '901_MT_SNTL'},
    {'label': 'Sublett SNOW', 'value': '12G08_ID_SNOW'},
    {'label': 'Succor Creek AM SNOW', 'value': '16F06_ID_SNOW'},
    {'label': 'Sucker Creek SNTL', 'value': '798_WY_SNTL'},
    {'label': 'Sunset SNTL', 'value': '803_ID_SNTL'},
    {'label': 'Swede Peak SNTL', 'value': '805_ID_SNTL'},
    {'label': 'Sylvan Lake SNTL', 'value': '806_WY_SNTL'},
    {'label': 'Sylvan Road SNTL', 'value': '807_WY_SNTL'},
    {'label': 'T-Cross Ranch SNOW', 'value': '09F03_WY_SNOW'},
    {'label': 'Taylor Road SNOW', 'value': '09A07_MT_SNOW'},
    {'label': 'Telfer Ranch SNOW', 'value': '13F06_ID_SNOW'},
    {'label': 'Ten Mile Lower SNOW', 'value': '12C02_MT_SNOW'},
    {'label': 'Ten Mile Middle SNOW', 'value': '12C03_MT_SNOW'},
    {'label': 'Tepee Creek SNTL', 'value': '813_MT_SNTL'},
    {'label': 'Teton Pass W.s. SNOW', 'value': '10F24_WY_SNOW'},
    {'label': 'Thorson Cabin #2 SNOW', 'value': '17E06_ID_SNOW'},
    {'label': 'Thumb Divide SNOW', 'value': '10E07_WY_SNOW'},
    {'label': 'Thumb Divide SNTL', 'value': '816_WY_SNTL'},
    {'label': 'Tie Creek SNTL', 'value': '818_WY_SNTL'},
    {'label': 'Timber Creek SNTL', 'value': '819_WY_SNTL'},
    {'label': 'Timberline Creek SNOW', 'value': '09D04_MT_SNOW'},
    {'label': 'Tizer Basin SNTL', 'value': '893_MT_SNTL'},
    {'label': 'Togwotee Pass SNOW', 'value': '10F09_WY_SNOW'},
    {'label': 'Togwotee Pass SNTL', 'value': '822_WY_SNTL'},
    {'label': 'Tollgate SNOW', 'value': '15F20_ID_SNOW'},
    {'label': 'Townsend Creek SNTL', 'value': '826_WY_SNTL'},
    {'label': 'Trinity Mtn. SNTL', 'value': '830_ID_SNTL'},
    {'label': 'Trinkus Lake SNOW', 'value': '13B01_MT_SNOW'},
    {'label': 'Triple Peak SNTL', 'value': '831_WY_SNTL'},
    {'label': 'Tripod Summit SNOW', 'value': '16E03_ID_SNOW'},
    {'label': 'Truman Creek SNOW', 'value': '14A18_MT_SNOW'},
    {'label': 'Turpin Meadows SNOW', 'value': '10F05_WY_SNOW'},
    {'label': 'Twelvemile Creek SNTL', 'value': '835_MT_SNTL'},
    {'label': 'Twenty-One Mile SNOW', 'value': '11E06_MT_SNOW'},
    {'label': 'Twin Lakes SNTL', 'value': '836_MT_SNTL'},
    {'label': 'Twin Spirit Divide SNOW', 'value': '16B12_ID_SNOW'},
    {'label': 'Two Ocean Plateau SNTL', 'value': '837_WY_SNTL'},
    {'label': 'Tyrell R.S. SNOW', 'value': '07E35_WY_SNOW'},
    {'label': 'Upper Elkhorn SNOW', 'value': '12G10_ID_SNOW'},
    {'label': 'Upper Holland Lake SNOW', 'value': '13B05_MT_SNOW'},
    {'label': 'Upper Home Canyon SNOW', 'value': '11G26_ID_SNOW'},
    {'label': 'Upper Spearfish SNOW', 'value': '03E01_SD_SNOW'},
    {'label': 'Valley View SNOW', 'value': '11E08_ID_SNOW'},
    {'label': 'Van Wyck SNTL', 'value': '979_ID_SNTL'},
    {'label': 'Vaught Ranch AM SNOW', 'value': '16G12_ID_SNOW'},
    {'label': 'Vienna Mine SNTL', 'value': '845_ID_SNTL'},
    {'label': 'Waldron SNTL', 'value': '847_MT_SNTL'},
    {'label': 'Warm Springs SNTL', 'value': '850_MT_SNTL'},
    {'label': 'Weasel Divide SNOW', 'value': '14A07_MT_SNOW'},
    {'label': 'Webb Creek #2 SNOW', 'value': '16C21_ID_SNOW'},
    {'label': 'Webber Creek SNOW', 'value': '12E05_ID_SNOW'},
    {'label': 'Webber Springs SNTL', 'value': '852_WY_SNTL'},
    {'label': 'West Branch SNTL', 'value': '855_ID_SNTL'},
    {'label': 'West Yellowstone SNTL', 'value': '924_MT_SNTL'},
    {'label': 'West Yellowstone SNOW', 'value': '11E07_MT_SNOW'},
    {'label': 'Whiskey Creek SNTL', 'value': '858_MT_SNTL'},
    {'label': 'Whiskey Park SNTL', 'value': '859_WY_SNTL'},
    {'label': 'White Elephant SNTL', 'value': '860_ID_SNTL'},
    {'label': 'White Mill SNTL', 'value': '862_MT_SNTL'},
    {'label': 'Wildhorse Divide SNTL', 'value': '867_ID_SNTL'},
    {'label': 'Willow Creek SNTL', 'value': '868_WY_SNTL'},
    {'label': 'Willow Flat SNOW', 'value': '11G04_ID_SNOW'},
    {'label': 'Wilson Creek SNTL', 'value': '871_ID_SNTL'},
    {'label': 'Windy Peak SNTL', 'value': '872_WY_SNTL'},
    {'label': 'Wolverine SNTL', 'value': '875_WY_SNTL'},
    {'label': 'Wood Creek SNTL', 'value': '876_MT_SNTL'},
    {'label': 'Wood Rock G.S. SNOW', 'value': '07E13_WY_SNOW'},
    {'label': 'Worm Creek SNOW', 'value': '11G28_ID_SNOW'},
    {'label': 'Wrong Creek SNOW', 'value': '12B04_MT_SNOW'},
    {'label': 'Wrong Ridge SNOW', 'value': '12B03_MT_SNOW'},
    {'label': 'Younts Peak SNTL', 'value': '878_WY_SNTL'},
]

body = dbc.Container([
    dbc.Row(dbc.Col([
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            }),
        html.H1('Site Correlator (SWE Only)',
                style={
                    "color": "black",
                    "text-align": "center",
                    "font-weight": "bold",
                }),
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            })],
    )),

    dbc.Row([
        dbc.Col([
            html.H2('Site 1'),
            dcc.Dropdown(id='triplet1', options=all_SNOTEL, value='07E05_WY_SNOW'),
        ]),
        dbc.Col([
            html.H2('Site 2'),
            dcc.Dropdown(id='triplet2', options=all_SNOTEL, value='1132_WY_SNTL'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H6('Note: Type in site name or scroll through list. Site lists include all SNOTEL and Snow Courses in '
                    'MT, WY, SD, and ID. Also, refresh web browser if having issues selecting new sites.'),
        ]),
    ]),

    dbc.Row(dbc.Col(
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            }
        )
    )),

    dbc.Row(dbc.Col([
        html.H3('Scatter Plot'),
        html.H6('Note: The trendline is calculated using Ordinary Least Squares (OLS) trendline function.'),
        html.Div(
            dcc.Graph(id='scatter-plot')),
    ])),

    dbc.Row(dbc.Col(
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            }
        )
    )),

    dbc.Row(dbc.Col([
        html.H3('Line Plot'),
        html.Div(
            dcc.Graph(id='line-plot')),
    ])),

    dbc.Row(dbc.Col(
        html.Hr(
            style={
                "border": "none",
                "border-top": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "text-align": "center",
                "height": "5px",
            }
        )
    )),

    dbc.Row(dbc.Col([
        html.H3('Data Table'),
        html.Div(id='site_data_table'),
    ])),
], fluid=True)


def site_correlator():
    layout = html.Div([
        nav,
        body
    ])
    return layout


@app.callback(Output('scatter-plot', 'figure'),
              [Input('triplet1', 'value'),
               Input('triplet2', 'value')
               ])
def update_scatter(id1, id2):
    if id1 and id2 and id1 != id2:
        df = site_data(id1, id2)
        fig = px.scatter(data_frame=df, x=id1, y=id2, trendline="ols", marginal_x="box", marginal_y="box")
        return fig
    else:
        return None


@app.callback(Output('line-plot', 'figure'),
              [Input('triplet1', 'value'),
               Input('triplet2', 'value')
               ])
def update_scatter(id1, id2):
    if id1 and id2 and id1 != id2:
        df = site_data(id1, id2)
        fig = px.line(data_frame=df, x='DATE', y=[id1, id2], labels={'x': 'WTEQ (inches)'})
        return fig
    else:
        return None


@app.callback(Output('site_data_table', 'children'),
              [Input('triplet1', 'value'),
               Input('triplet2', 'value')
               ])
def daily_table(triplet1, triplet2):
    if triplet1 and triplet2 and triplet1 != triplet2:
        df = site_data(triplet1, triplet2)
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_cell={
                'textAlign': 'center',
                'height': 'auto',
                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                'whiteSpace': 'normal'
            },
            merge_duplicate_headers=True,
            fixed_rows={'headers': True},
            sort_action='native',
            style_data={'border': '2px solid black'},
            style_header={'border': '2px solid black'},
            style_table={'overflowX': 'auto'},
        )
    else:
        return None
