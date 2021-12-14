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

    return df


all_sites = [
    {'label': 'Above Gilmore SNOW (13E19)', 'value': '13E19_ID_SNOW'},
    {'label': 'Above Roland SNOW (15B07)', 'value': '15B07_ID_SNOW'},
    {'label': 'Albany SNOW (06H11)', 'value': '06H11_WY_SNOW'},
    {'label': 'Albro Lake SNTL (916)', 'value': '916_MT_SNTL'},
    {'label': 'Allen Ranch SNOW (11G35)', 'value': '11G35_ID_SNOW'},
    {'label': 'Arch Falls SNOW (10D14)', 'value': '10D14_MT_SNOW'},
    {'label': 'Ashley Divide SNOW (14A19)', 'value': '14A19_MT_SNOW'},
    {'label': 'Aster Creek SNOW (10E08)', 'value': '10E08_WY_SNOW'},
    {'label': 'Atlanta Summit SNTL (306)', 'value': '306_ID_SNTL'},
    {'label': 'Bad Bear SNOW (15F02)', 'value': '15F02_ID_SNOW'},
    {'label': 'Badger Gulch SNOW (14G03)', 'value': '14G03_ID_SNOW'},
    {'label': 'Badger Pass SNTL (307)', 'value': '307_MT_SNTL'},
    {'label': 'Bald Mtn. SNTL (309)', 'value': '309_WY_SNTL'},
    {'label': 'Banfield Mountain SNTL (311)', 'value': '311_MT_SNTL'},
    {'label': 'Banner Summit SNTL (312)', 'value': '312_ID_SNTL'},
    {'label': 'Baree Creek SNOW (15B11)', 'value': '15B11_MT_SNOW'},
    {'label': 'Baree Midway SNOW (15B16)', 'value': '15B16_MT_SNOW'},
    {'label': 'Baree Trail SNOW (15B15)', 'value': '15B15_MT_SNOW'},
    {'label': 'Barker Lakes SNTL (313)', 'value': '313_MT_SNTL'},
    {'label': 'Base Camp SNTL (314)', 'value': '314_WY_SNTL'},
    {'label': 'Base Camp SNOW (10F02)', 'value': '10F02_WY_SNOW'},
    {'label': 'Basin Creek SNTL (315)', 'value': '315_MT_SNTL'},
    {'label': 'Basin Creek SNOW (12D09)', 'value': '12D09_MT_SNOW'},
    {'label': 'Bassoo Peak SNOW (14B03)', 'value': '14B03_MT_SNOW'},
    {'label': 'Battle Creek AM SNOW (16G09)', 'value': '16G09_ID_SNOW'},
    {'label': 'Battle Mountain SNTL (317)', 'value': '317_WY_SNTL'},
    {'label': 'Beagle Springs SNTL (318)', 'value': '318_MT_SNTL'},
    {'label': 'Bear Basin SNTL (319)', 'value': '319_ID_SNTL'},
    {'label': 'Bear Canyon SNTL (320)', 'value': '320_ID_SNTL'},
    {'label': 'Bear Lodge Divide SNOW (04E02)', 'value': '04E02_WY_SNOW'},
    {'label': 'Bear Mountain SNTL (323)', 'value': '323_ID_SNTL'},
    {'label': 'Bear Saddle SNTL (324)', 'value': '324_ID_SNTL'},
    {'label': 'Bear Trap Meadow SNTL (325)', 'value': '325_WY_SNTL'},
    {'label': 'Beartooth Lake SNTL (326)', 'value': '326_WY_SNTL'},
    {'label': 'Beaver Creek SNTL (328)', 'value': '328_MT_SNTL'},
    {'label': 'Benton Meadow SNOW (16A02)', 'value': '16A02_ID_SNOW'},
    {'label': 'Benton Spring SNOW (16A03)', 'value': '16A03_ID_SNOW'},
    {'label': 'Big Creek Summit SNTL (338)', 'value': '338_ID_SNTL'},
    {'label': 'Big Goose SNTL (931)', 'value': '931_WY_SNTL'},
    {'label': 'Big Park SNOW (10G11)', 'value': '10G11_WY_SNOW'},
    {'label': 'Big Sandy Opening SNTL (342)', 'value': '342_WY_SNTL'},
    {'label': 'Big Snowy SNOW (09C05)', 'value': '09C05_MT_SNOW'},
    {'label': 'Big Springs SNOW (11E09)', 'value': '11E09_ID_SNOW'},
    {'label': 'Bisson Creek SNTL (346)', 'value': '346_MT_SNTL'},
    {'label': 'Black Bear SNTL (347)', 'value': '347_MT_SNTL'},
    {'label': 'Black Mountain SNOW (12C19)', 'value': '12C19_MT_SNOW'},
    {'label': 'Black Pine SNTL (349)', 'value': '349_MT_SNTL'},
    {'label': 'Blackhall Mtn SNTL (1119)', 'value': '1119_WY_SNTL'},
    {'label': 'Blacktail SNOW (14B04)', 'value': '14B04_MT_SNOW'},
    {'label': 'Blacktail Mtn SNTL (1144)', 'value': '1144_MT_SNTL'},
    {'label': 'Blackwater SNTL (350)', 'value': '350_WY_SNTL'},
    {'label': 'Blind Bull Sum SNTL (353)', 'value': '353_WY_SNTL'},
    {'label': 'Blind Park SNTL (354)', 'value': '354_SD_SNTL'},
    {'label': 'Bloody Dick SNTL (355)', 'value': '355_MT_SNTL'},
    {'label': 'Blue Ridge SNOW (11F17)', 'value': '11F17_ID_SNOW'},
    {'label': 'Blue Ridge SNOW (08G02)', 'value': '08G02_WY_SNOW'},
    {'label': 'Bogus Basin SNTL (978)', 'value': '978_ID_SNTL'},
    {'label': 'Bogus Basin SNOW (16F02)', 'value': '16F02_ID_SNOW'},
    {'label': 'Bogus Basin Road SNOW (16F04)', 'value': '16F04_ID_SNOW'},
    {'label': 'Bone SNOW (11F08)', 'value': '11F08_ID_SNOW'},
    {'label': 'Bone Springs Div SNTL (358)', 'value': '358_WY_SNTL'},
    {'label': 'Bostetter R.S. SNTL (359)', 'value': '359_ID_SNTL'},
    {'label': 'Bots Sots SNOW (09D14)', 'value': '09D14_MT_SNOW'},
    {'label': 'Boulder Mountain SNTL (360)', 'value': '360_MT_SNTL'},
    {'label': 'Box Canyon SNTL (363)', 'value': '363_MT_SNTL'},
    {'label': 'Boxelder Creek SNOW (09A08)', 'value': '09A08_MT_SNOW'},
    {'label': 'Boy Scout Camp SNOW (13G02)', 'value': '13G02_ID_SNOW'},
    {'label': 'Brackett Creek SNTL (365)', 'value': '365_MT_SNTL'},
    {'label': 'Branham Lakes SNOW (11D14)', 'value': '11D14_MT_SNOW'},
    {'label': 'Bristow Creek SNOW (15A10)', 'value': '15A10_MT_SNOW'},
    {'label': 'Brooklyn Lake SNTL (367)', 'value': '367_WY_SNTL'},
    {'label': 'Brundage Reservoir SNTL (370)', 'value': '370_ID_SNTL'},
    {'label': 'Bruno Creek SNOW (14E08)', 'value': '14E08_ID_SNOW'},
    {'label': 'Brush Creek Timber SNOW (14A13)', 'value': '14A13_MT_SNOW'},
    {'label': 'Bull Basin AM SNOW (16G10)', 'value': '16G10_ID_SNOW'},
    {'label': 'Bull Mountain SNOW (12D08)', 'value': '12D08_MT_SNOW'},
    {'label': 'Burgess Junction SNTL (377)', 'value': '377_WY_SNTL'},
    {'label': 'Burnt Mtn SNTL (981)', 'value': '981_MT_SNTL'},
    {'label': 'Burroughs Creek SNTL (379)', 'value': '379_WY_SNTL'},
    {'label': 'Cabin Creek SNOW (12B06)', 'value': '12B06_MT_SNOW'},
    {'label': 'Calvert Creek SNTL (381)', 'value': '381_MT_SNTL'},
    {'label': 'Camas Creek Divide SNTL (382)', 'value': '382_ID_SNTL'},
    {'label': 'Camp Creek SNOW (12E03)', 'value': '12E03_ID_SNOW'},
    {'label': 'Camp Senia SNOW (09D01)', 'value': '09D01_MT_SNOW'},
    {'label': 'Canyon SNTL (384)', 'value': '384_WY_SNTL'},
    {'label': 'Carrot Basin SNTL (385)', 'value': '385_MT_SNTL'},
    {'label': 'Casper Mtn. SNTL (389)', 'value': '389_WY_SNTL'},
    {'label': 'Castle Creek SNOW (09F20)', 'value': '09F20_WY_SNOW'},
    {'label': 'Castle Creek SNTL (1130)', 'value': '1130_WY_SNTL'},
    {'label': 'Ccc Camp SNOW (10G07)', 'value': '10G07_WY_SNOW'},
    {'label': 'Chessman Reservoir SNOW (12C05)', 'value': '12C05_MT_SNOW'},
    {'label': 'Chicago Ridge SNOW (15B22)', 'value': '15B22_MT_SNOW'},
    {'label': 'Chicken Creek SNOW (14A15)', 'value': '14A15_MT_SNOW'},
    {'label': 'Chimney Creek SNOW (15F15)', 'value': '15F15_ID_SNOW'},
    {'label': 'Chocolate Gulch SNTL (895)', 'value': '895_ID_SNTL'},
    {'label': 'Cinnabar Park SNTL (1046)', 'value': '1046_WY_SNTL'},
    {'label': 'Cloud Peak Reservoir SNTL (402)', 'value': '402_WY_SNTL'},
    {'label': 'Clover Meadow SNTL (403)', 'value': '403_MT_SNTL'},
    {'label': 'Cold Springs SNTL (405)', 'value': '405_WY_SNTL'},
    {'label': 'Cole Canyon SNTL (982)', 'value': '982_WY_SNTL'},
    {'label': 'Cole Creek SNTL (407)', 'value': '407_MT_SNTL'},
    {'label': 'Colley Creek SNOW (10D30)', 'value': '10D30_MT_SNOW'},
    {'label': 'Combination SNTL (410)', 'value': '410_MT_SNTL'},
    {'label': 'Cool Creek SNTL (411)', 'value': '411_ID_SNTL'},
    {'label': 'Copes Camp SNOW (13E17)', 'value': '13E17_ID_SNOW'},
    {'label': 'Copper Basin SNOW (13F02)', 'value': '13F02_ID_SNOW'},
    {'label': 'Copper Bottom SNTL (413)', 'value': '413_MT_SNTL'},
    {'label': 'Copper Camp SNTL (414)', 'value': '414_MT_SNTL'},
    {'label': 'Copper Mountain SNOW (12C09)', 'value': '12C09_MT_SNOW'},
    {'label': 'Cottonwood Creek SNOW (12C17)', 'value': '12C17_MT_SNOW'},
    {'label': 'Cottonwood Creek SNTL (419)', 'value': '419_WY_SNTL'},
    {'label': 'Couch Summit SNTL (1306)', 'value': '1306_ID_SNTL'},
    {'label': 'Couch Summit #2 SNOW (14F18)', 'value': '14F18_ID_SNOW'},
    {'label': 'Cougar Point SNOW (14D06)', 'value': '14D06_ID_SNOW'},
    {'label': 'Coyote Hill SNOW (13B10)', 'value': '13B10_MT_SNOW'},
    {'label': 'Cozy Cove SNTL (423)', 'value': '423_ID_SNTL'},
    {'label': 'Crab Creek SNTL (424)', 'value': '424_ID_SNTL'},
    {'label': 'Crater Meadows SNTL (425)', 'value': '425_ID_SNTL'},
    {'label': 'Crevice Mountain SNOW (10D05)', 'value': '10D05_MT_SNOW'},
    {'label': 'Crooked Fork SNOW (14C11)', 'value': '14C11_ID_SNOW'},
    {'label': 'Crow Creek SNTL (1045)', 'value': '1045_WY_SNTL'},
    {'label': 'Crystal Lake SNTL (427)', 'value': '427_MT_SNTL'},
    {'label': 'Daisy Peak SNTL (919)', 'value': '919_MT_SNTL'},
    {'label': 'Daly Creek SNTL (433)', 'value': '433_MT_SNTL'},
    {'label': 'Daniels Creek SNOW (12G12)', 'value': '12G12_ID_SNOW'},
    {'label': 'Darby Canyon SNOW (10F21)', 'value': '10F21_WY_SNOW'},
    {'label': 'Darkhorse Lake SNTL (436)', 'value': '436_MT_SNTL'},
    {'label': 'Deadman Creek SNTL (437)', 'value': '437_MT_SNTL'},
    {'label': 'Deadman Gulch SNOW (16F01)', 'value': '16F01_ID_SNOW'},
    {'label': 'Deadwood Summit SNTL (439)', 'value': '439_ID_SNTL'},
    {'label': 'Deep Lake SNOW (06H17)', 'value': '06H17_WY_SNOW'},
    {'label': 'Deer Park SNTL (923)', 'value': '923_WY_SNTL'},
    {'label': 'Democrat Creek SNOW (16F13)', 'value': '16F13_ID_SNOW'},
    {'label': 'Desert Mountain SNOW (13A02)', 'value': '13A02_MT_SNOW'},
    {'label': 'Discovery Basin SNOW (13C42)', 'value': '13C42_MT_SNOW'},
    {'label': 'Ditch Creek SNOW (03F04)', 'value': '03F04_SD_SNOW'},
    {'label': 'Divide SNTL (448)', 'value': '448_MT_SNTL'},
    {'label': 'Divide Peak SNTL (449)', 'value': '449_WY_SNTL'},
    {'label': 'Dix Hill SNOW (12C15)', 'value': '12C15_MT_SNOW'},
    {'label': 'Dobson Creek SNOW (16F12)', 'value': '16F12_ID_SNOW'},
    {'label': 'Dodson Pass SNOW (16E15)', 'value': '16E15_ID_SNOW'},
    {'label': 'Dollarhide Summit SNTL (450)', 'value': '450_ID_SNTL'},
    {'label': 'Dome Lake SNTL (451)', 'value': '451_WY_SNTL'},
    {'label': 'Dry Basin SNOW (11G14)', 'value': '11G14_ID_SNOW'},
    {'label': 'Dry Fork SNOW (13F20)', 'value': '13F20_ID_SNOW'},
    {'label': 'Dunoir SNOW (09F06)', 'value': '09F06_WY_SNOW'},
    {'label': 'Dupuyer Creek SNTL (458)', 'value': '458_MT_SNTL'},
    {'label': 'Eagle Creek SNOW (10C13)', 'value': '10C13_MT_SNOW'},
    {'label': 'East Boulder Mine SNTL (1105)', 'value': '1105_MT_SNTL'},
    {'label': 'East Creek SNOW (11G34)', 'value': '11G34_ID_SNOW'},
    {'label': 'East Fork R.S. SNOW (13D01)', 'value': '13D01_MT_SNOW'},
    {'label': 'East Rim Divide SNTL (460)', 'value': '460_WY_SNTL'},
    {'label': 'El Dorado Mine SNOW (13C09)', 'value': '13C09_MT_SNOW'},
    {'label': 'Elbo Ranch SNOW (10F28)', 'value': '10F28_WY_SNOW'},
    {'label': 'Elk Butte SNTL (466)', 'value': '466_ID_SNTL'},
    {'label': 'Elk Horn Springs SNOW (13D15)', 'value': '13D15_MT_SNOW'},
    {'label': 'Elk Peak SNOW (10C07)', 'value': '10C07_MT_SNOW'},
    {'label': 'Elk Peak SNTL (1106)', 'value': '1106_MT_SNTL'},
    {'label': 'Elkhart Park G.S. SNTL (468)', 'value': '468_WY_SNTL'},
    {'label': 'Emery Creek SNTL (469)', 'value': '469_MT_SNTL'},
    {'label': 'Emigrant Summit SNTL (471)', 'value': '471_ID_SNTL'},
    {'label': 'Emigration Canyon SNOW (11G07)', 'value': '11G07_ID_SNOW'},
    {'label': 'Evening Star SNTL (472)', 'value': '472_WY_SNTL'},
    {'label': 'Fall Creek SNOW (11F19)', 'value': '11F19_ID_SNOW'},
    {'label': 'Fatty Creek SNOW (13B04)', 'value': '13B04_MT_SNOW'},
    {'label': 'Fish Ck SNTL (1305)', 'value': '1305_ID_SNTL'},
    {'label': 'Fish Creek SNOW (12D10)', 'value': '12D10_MT_SNOW'},
    {'label': 'Fish Lake Airstrip SNOW (15C02)', 'value': '15C02_ID_SNOW'},
    {'label': 'Fisher Creek SNTL (480)', 'value': '480_MT_SNTL'},
    {'label': 'Flattop Mtn. SNTL (482)', 'value': '482_MT_SNTL'},
    {'label': 'Fleecer Ridge SNOW (12D07)', 'value': '12D07_MT_SNOW'},
    {'label': 'Foolhen SNOW (13D21)', 'value': '13D21_MT_SNOW'},
    {'label': 'Forest Lake SNOW (10C14)', 'value': '10C14_MT_SNOW'},
    {'label': 'Four Mile SNOW (11D12)', 'value': '11D12_MT_SNOW'},
    {'label': 'Four Mile Meadow SNOW (10F06)', 'value': '10F06_WY_SNOW'},
    {'label': 'Fourth Of July Summit SNOW (16B03)', 'value': '16B03_ID_SNOW'},
    {'label': 'Fox Park #2 SNOW (06H24)', 'value': '06H24_WY_SNOW'},
    {'label': 'Foxpark SNOW (06H12)', 'value': '06H12_WY_SNOW'},
    {'label': 'Franklin Basin SNTL (484)', 'value': '484_ID_SNTL'},
    {'label': 'Freight Creek SNOW (12A01)', 'value': '12A01_MT_SNOW'},
    {'label': 'Frohner Meadow SNTL (487)', 'value': '487_MT_SNTL'},
    {'label': 'Galena SNTL (489)', 'value': '489_ID_SNTL'},
    {'label': 'Galena Summit SNTL (490)', 'value': '490_ID_SNTL'},
    {'label': 'Garfield R.S. SNTL (492)', 'value': '492_ID_SNTL'},
    {'label': 'Garver Creek SNTL (918)', 'value': '918_MT_SNTL'},
    {'label': 'Geyser Creek SNOW (09F07)', 'value': '09F07_WY_SNOW'},
    {'label': 'Giveout SNTL (493)', 'value': '493_ID_SNTL'},
    {'label': 'Glade Creek SNOW (10E13)', 'value': '10E13_WY_SNOW'},
    {'label': 'Government Saddle SNOW (15B23)', 'value': '15B23_MT_SNOW'},
    {'label': 'Graham Guard Sta. SNTL (496)', 'value': '496_ID_SNTL'},
    {'label': 'Grand Targhee SNTL (1082)', 'value': '1082_WY_SNTL'},
    {'label': 'Granite Creek SNTL (497)', 'value': '497_WY_SNTL'},
    {'label': 'Grannier Meadows SNOW (08G04)', 'value': '08G04_WY_SNOW'},
    {'label': 'Grasshopper SNOW (10C02)', 'value': '10C02_MT_SNOW'},
    {'label': 'Grassy Lake SNTL (499)', 'value': '499_WY_SNTL'},
    {'label': 'Grassy Lake SNOW (10E15)', 'value': '10E15_WY_SNOW'},
    {'label': 'Grave Creek SNTL (500)', 'value': '500_MT_SNTL'},
    {'label': 'Grave Springs SNTL (501)', 'value': '501_WY_SNTL'},
    {'label': 'Griffin Creek Divide SNOW (14A09)', 'value': '14A09_MT_SNOW'},
    {'label': 'Gros Ventre Summit SNTL (506)', 'value': '506_WY_SNTL'},
    {'label': 'Grover Park Divide SNOW (10G03)', 'value': '10G03_WY_SNOW'},
    {'label': 'Gunsight Pass SNTL (944)', 'value': '944_WY_SNTL'},
    {'label': 'Hahn Homestead SNOW (13E29)', 'value': '13E29_ID_SNOW'},
    {'label': 'Hairpin Turn SNOW (06H02)', 'value': '06H02_WY_SNOW'},
    {'label': 'Hams Fork SNTL (509)', 'value': '509_WY_SNTL'},
    {'label': 'Hand Creek SNTL (510)', 'value': '510_MT_SNTL'},
    {'label': 'Hansen Sawmill SNTL (512)', 'value': '512_WY_SNTL'},
    {'label': 'Haskins Creek SNOW (07H01)', 'value': '07H01_WY_SNOW'},
    {'label': 'Hawkins Lake SNTL (516)', 'value': '516_MT_SNTL'},
    {'label': 'Haymaker SNOW (10C11)', 'value': '10C11_MT_SNOW'},
    {'label': 'Hebgen Dam SNOW (11E05)', 'value': '11E05_MT_SNOW'},
    {'label': 'Hell Roaring Divide SNOW (14A03)', 'value': '14A03_MT_SNOW'},
    {'label': 'Hemlock Butte SNTL (520)', 'value': '520_ID_SNTL'},
    {'label': 'Herrig Junction SNOW (14A16)', 'value': '14A16_MT_SNOW'},
    {'label': 'Hidden Lake SNTL (988)', 'value': '988_ID_SNTL'},
    {'label': 'Highwood Divide SNOW (10B02)', 'value': '10B02_MT_SNOW'},
    {'label': 'Highwood Station SNOW (10B01)', 'value': '10B01_MT_SNOW'},
    {'label': 'Hilts Creek SNTL (524)', 'value': '524_ID_SNTL'},
    {'label': 'Hoback GS SNOW (10F30)', 'value': '10F30_WY_SNOW'},
    {'label': 'Hobbs Park SNTL (525)', 'value': '525_WY_SNTL'},
    {'label': 'Holbrook SNOW (13B13)', 'value': '13B13_MT_SNOW'},
    {'label': 'Hoodoo Basin SNTL (530)', 'value': '530_MT_SNTL'},
    {'label': 'Howell Canyon SNTL (534)', 'value': '534_ID_SNTL'},
    {'label': 'Huckleberry Divide SNOW (10E14)', 'value': '10E14_WY_SNOW'},
    {'label': 'Humboldt Gulch SNTL (535)', 'value': '535_ID_SNTL'},
    {'label': 'Hyndman SNTL (537)', 'value': '537_ID_SNTL'},
    {'label': 'Iceberg Lake No 3 SNOW (13A03)', 'value': '13A03_MT_SNOW'},
    {'label': 'Indian Creek SNTL (544)', 'value': '544_WY_SNTL'},
    {'label': 'Intergaard SNOW (13C04)', 'value': '13C04_MT_SNOW'},
    {'label': 'Iron Mine Creek SNOW (13F10)', 'value': '13F10_ID_SNOW'},
    {'label': 'Irving Creek SNOW (12E04)', 'value': '12E04_ID_SNOW'},
    {'label': 'Island Park SNTL (546)', 'value': '546_ID_SNTL'},
    {'label': 'Jackpine Creek SNOW (10F26)', 'value': '10F26_WY_SNOW'},
    {'label': 'Jackson Peak SNTL (550)', 'value': '550_ID_SNTL'},
    {'label': 'Jahnke Lake Trail SNOW (13D27)', 'value': '13D27_MT_SNOW'},
    {'label': 'Jakes Canyon SNOW (13E28)', 'value': '13E28_ID_SNOW'},
    {'label': 'JL Meadow SNTL (1287)', 'value': '1287_MT_SNTL'},
    {'label': 'John Evans Canyon SNOW (12G22)', 'value': '12G22_ID_SNOW'},
    {'label': 'Johnson Creek SNOW (11G36)', 'value': '11G36_ID_SNOW'},
    {'label': 'Johnson Park SNOW (10C12)', 'value': '10C12_MT_SNOW'},
    {'label': 'Josephine Lower No 9 SNOW (13A14)', 'value': '13A14_MT_SNOW'},
    {'label': 'Kelley R.S. SNTL (554)', 'value': '554_WY_SNTL'},
    {'label': 'Kellogg Peak SNOW (16B05)', 'value': '16B05_ID_SNOW'},
    {'label': 'Kendall R.S. SNTL (555)', 'value': '555_WY_SNTL'},
    {'label': 'Ketchum R S SNOW (14F21)', 'value': '14F21_ID_SNOW'},
    {'label': 'Kilgore SNOW (11E12)', 'value': '11E12_ID_SNOW'},
    {'label': 'Kings Hill SNOW (10C01)', 'value': '10C01_MT_SNOW'},
    {'label': 'Kirwin SNTL (560)', 'value': '560_WY_SNTL'},
    {'label': 'Kishenehn SNOW (14A06)', 'value': '14A06_MT_SNOW'},
    {'label': 'Kraft Creek SNTL (562)', 'value': '562_MT_SNTL'},
    {'label': 'Lake Camp SNOW (10E04)', 'value': '10E04_WY_SNOW'},
    {'label': 'Lake Fork SNOW (15E01)', 'value': '15E01_ID_SNOW'},
    {'label': 'Lakeview Canyon SNOW (11E04)', 'value': '11E04_MT_SNOW'},
    {'label': 'Lakeview Ridge SNTL (568)', 'value': '568_MT_SNTL'},
    {'label': 'Langford Flat Creek SNOW (14G08)', 'value': '14G08_ID_SNOW'},
    {'label': 'Laprele Creek SNTL (571)', 'value': '571_WY_SNTL'},
    {'label': 'Larsen Creek SNOW (09G06)', 'value': '09G06_WY_SNOW'},
    {'label': 'Larsen Creek SNTL (1134)', 'value': '1134_WY_SNTL'},
    {'label': 'Latham Springs SNOW (11E16)', 'value': '11E16_ID_SNOW'},
    {'label': 'Lava Creek SNOW (11F15)', 'value': '11F15_ID_SNOW'},
    {'label': 'Lemhi Ridge SNTL (576)', 'value': '576_MT_SNTL'},
    {'label': 'Lewis Lake Divide SNTL (577)', 'value': '577_WY_SNTL'},
    {'label': 'Lewis Lake Divide SNOW (10E09)', 'value': '10E09_WY_SNOW'},
    {'label': 'Libby Lodge SNOW (06H03)', 'value': '06H03_WY_SNOW'},
    {'label': 'Lick Creek SNTL (578)', 'value': '578_MT_SNTL'},
    {'label': 'Little Bear Run SNOW (04F01)', 'value': '04F01_WY_SNOW'},
    {'label': 'Little Camas Flat SNOW (15F12)', 'value': '15F12_ID_SNOW'},
    {'label': 'Little Goose SNTL (1131)', 'value': '1131_WY_SNTL'},
    {'label': 'Little Park SNOW (11D10)', 'value': '11D10_MT_SNOW'},
    {'label': 'Little Snake River SNTL (1047)', 'value': '1047_WY_SNTL'},
    {'label': 'Little Warm SNTL (585)', 'value': '585_WY_SNTL'},
    {'label': 'Logan Creek SNOW (14A05)', 'value': '14A05_MT_SNOW'},
    {'label': 'Logger Springs SNOW (13G03)', 'value': '13G03_ID_SNOW'},
    {'label': 'Lolo Pass SNTL (588)', 'value': '588_ID_SNTL'},
    {'label': 'Lone Mountain SNTL (590)', 'value': '590_MT_SNTL'},
    {'label': 'Long Valley SNTL (1016)', 'value': '1016_ID_SNTL'},
    {'label': 'Lookout SNTL (594)', 'value': '594_ID_SNTL'},
    {'label': 'Loomis Park SNTL (597)', 'value': '597_WY_SNTL'},
    {'label': 'Lost Lake SNTL (600)', 'value': '600_ID_SNTL'},
    {'label': 'Lost-Wood Divide SNTL (601)', 'value': '601_ID_SNTL'},
    {'label': 'Lower Pebble SNOW (12G06)', 'value': '12G06_ID_SNOW'},
    {'label': 'Lower Sands Creek #2 SNOW (16B13)', 'value': '16B13_ID_SNOW'},
    {'label': 'Lower Twin SNTL (603)', 'value': '603_MT_SNTL'},
    {'label': 'Lubrecht Flume SNTL (604)', 'value': '604_MT_SNTL'},
    {'label': 'Lubrecht Forest No 3 SNOW (13C21)', 'value': '13C21_MT_SNOW'},
    {'label': 'Lubrecht Forest No 4 SNOW (13C22)', 'value': '13C22_MT_SNOW'},
    {'label': 'Lubrecht Forest No 6 SNOW (13C08)', 'value': '13C08_MT_SNOW'},
    {'label': 'Lubrecht Hydroplot SNOW (13C37)', 'value': '13C37_MT_SNOW'},
    {'label': 'Lucky Dog SNOW (11E14)', 'value': '11E14_ID_SNOW'},
    {'label': 'Lupine Creek SNOW (10E01)', 'value': '10E01_WY_SNOW'},
    {'label': 'Madison Plateau SNTL (609)', 'value': '609_MT_SNTL'},
    {'label': 'Magic Mountain SNTL (610)', 'value': '610_ID_SNTL'},
    {'label': 'Mallo SNOW (04E05)', 'value': '04E05_WY_SNOW'},
    {'label': 'Many Glacier SNTL (613)', 'value': '613_MT_SNTL'},
    {'label': 'Marias Pass SNOW (13A05)', 'value': '13A05_MT_SNOW'},
    {'label': 'Marquette SNTL (616)', 'value': '616_WY_SNTL'},
    {'label': 'McCall U Of I Campus SNOW (16E20)', 'value': '16E20_ID_SNOW'},
    {'label': 'McRenolds Reservoir SNOW (11F12)', 'value': '11F12_ID_SNOW'},
    {'label': 'Meadow Lake SNTL (620)', 'value': '620_ID_SNTL'},
    {'label': 'Med Bow SNTL (1196)', 'value': '1196_WY_SNTL'},
    {'label': 'Medicine Lodge Lakes SNOW (07E24)', 'value': '07E24_WY_SNOW'},
    {'label': 'Mesa Ditch SNOW (16E19)', 'value': '16E19_ID_SNOW'},
    {'label': 'Mica Creek SNTL (623)', 'value': '623_ID_SNTL'},
    {'label': 'Middle Fork SNOW (08G06)', 'value': '08G06_WY_SNOW'},
    {'label': 'Middle Mill Creek SNOW (11D15)', 'value': '11D15_MT_SNOW'},
    {'label': 'Middle Powder SNTL (625)', 'value': '625_WY_SNTL'},
    {'label': 'Mill Creek SNOW (10D19)', 'value': '10D19_MT_SNOW'},
    {'label': 'Mill Creek Summit SNTL (627)', 'value': '627_ID_SNTL'},
    {'label': 'Mineral Creek SNOW (13A16)', 'value': '13A16_MT_SNOW'},
    {'label': 'Monument Peak SNTL (635)', 'value': '635_MT_SNTL'},
    {'label': 'Moonshine SNTL (636)', 'value': '636_ID_SNTL'},
    {'label': 'Moose Creek SNTL (638)', 'value': '638_ID_SNTL'},
    {'label': 'Moran SNOW (10F04)', 'value': '10F04_WY_SNOW'},
    {'label': 'Mores Creek Summit SNTL (637)', 'value': '637_ID_SNTL'},
    {'label': 'Mores Creek Summit SNOW (15F01)', 'value': '15F01_ID_SNOW'},
    {'label': 'Morgan Creek SNTL (639)', 'value': '639_ID_SNTL'},
    {'label': 'Morse Creek Sawmill SNOW (13E26)', 'value': '13E26_ID_SNOW'},
    {'label': 'Moscow Mountain SNTL (989)', 'value': '989_ID_SNTL'},
    {'label': 'Mosquito Ridge SNTL (645)', 'value': '645_ID_SNTL'},
    {'label': 'Moss Lake SNOW (06H16)', 'value': '06H16_WY_SNOW'},
    {'label': 'Moss Lake #2 SNOW (06H26)', 'value': '06H26_WY_SNOW'},
    {'label': 'Moss Peak SNTL (646)', 'value': '646_MT_SNTL'},
    {'label': 'Moulton Reservoir SNOW (12C20)', 'value': '12C20_MT_SNOW'},
    {'label': 'Mount Allen No 7 SNOW (13A07)', 'value': '13A07_MT_SNOW'},
    {'label': 'Mount Baldy SNOW (14F09)', 'value': '14F09_ID_SNOW'},
    {'label': 'Mount Lockhart SNTL (649)', 'value': '649_MT_SNTL'},
    {'label': 'Mount Tom SNOW (04E04)', 'value': '04E04_WY_SNOW'},
    {'label': 'Mountain Meadows SNTL (650)', 'value': '650_ID_SNTL'},
    {'label': 'Mud Creek SNOW (11F14)', 'value': '11F14_ID_SNOW'},
    {'label': 'Mud Flat SNTL (654)', 'value': '654_ID_SNTL'},
    {'label': 'Mud Spring SNOW (14F20)', 'value': '14F20_ID_SNOW'},
    {'label': 'Mudd Lake SNOW (13D25)', 'value': '13D25_MT_SNOW'},
    {'label': 'Muldoon SNOW (13F05)', 'value': '13F05_ID_SNOW'},
    {'label': 'Mule Creek SNTL (656)', 'value': '656_MT_SNTL'},
    {'label': 'Myrtle Creek SNTL (1053)', 'value': '1053_ID_SNTL'},
    {'label': 'N Fk Elk Creek SNTL (657)', 'value': '657_MT_SNTL'},
    {'label': 'Nevada Ridge SNTL (903)', 'value': '903_MT_SNTL'},
    {'label': 'New Fork Lake SNTL (661)', 'value': '661_WY_SNTL'},
    {'label': 'New World SNOW (10D01)', 'value': '10D01_MT_SNOW'},
    {'label': 'Nez Perce Camp SNTL (662)', 'value': '662_MT_SNTL'},
    {'label': 'Nez Perce Creek SNOW (12C10)', 'value': '12C10_MT_SNOW'},
    {'label': 'Nez Perce Pass SNOW (14D01)', 'value': '14D01_MT_SNOW'},
    {'label': 'Noisy Basin SNTL (664)', 'value': '664_MT_SNTL'},
    {'label': 'Norris Basin SNOW (10E19)', 'value': '10E19_WY_SNOW'},
    {'label': 'North Barrett Creek SNOW (06H05)', 'value': '06H05_WY_SNOW'},
    {'label': 'North Crane Creek SNOW (16E17)', 'value': '16E17_ID_SNOW'},
    {'label': 'North Fork Jocko SNOW (13B07)', 'value': '13B07_MT_SNOW'},
    {'label': 'North Fork Jocko SNTL (667)', 'value': '667_MT_SNTL'},
    {'label': 'North French Creek SNTL (668)', 'value': '668_WY_SNTL'},
    {'label': 'North Rapid Creek SNTL (920)', 'value': '920_SD_SNTL'},
    {'label': 'North Tongue SNOW (07E15)', 'value': '07E15_WY_SNOW'},
    {'label': 'Northeast Entrance SNTL (670)', 'value': '670_MT_SNTL'},
    {'label': 'Old Battle SNTL (673)', 'value': '673_WY_SNTL'},
    {'label': 'Old Faithful SNOW (10E18)', 'value': '10E18_WY_SNOW'},
    {'label': 'Onion Gulch SNOW (07E27)', 'value': '07E27_WY_SNOW'},
    {'label': 'Onion Park SNTL (1008)', 'value': '1008_MT_SNTL'},
    {'label': 'Ophir Park SNOW (12C16)', 'value': '12C16_MT_SNOW'},
    {'label': 'Owl Creek SNTL (676)', 'value': '676_WY_SNTL'},
    {'label': 'Oxford Spring SNTL (677)', 'value': '677_ID_SNTL'},
    {'label': 'Packsaddle Spring SNOW (11F18)', 'value': '11F18_ID_SNOW'},
    {'label': 'Parker Peak SNTL (683)', 'value': '683_WY_SNTL'},
    {'label': 'Pebble Creek SNOW (12G02)', 'value': '12G02_ID_SNOW'},
    {'label': 'Pebble Creek SNTL (1299)', 'value': '1299_ID_SNTL'},
    {'label': 'Perreau Meadows SNOW (14D05)', 'value': '14D05_ID_SNOW'},
    {'label': 'Peterson Meadows SNTL (930)', 'value': '930_MT_SNTL'},
    {'label': 'Phillips Bench SNTL (689)', 'value': '689_WY_SNTL'},
    {'label': 'Pickfoot Creek SNTL (690)', 'value': '690_MT_SNTL'},
    {'label': 'Piegan Pass No 6 SNOW (13A06)', 'value': '13A06_MT_SNOW'},
    {'label': 'Pierce R.S. SNTL (1142)', 'value': '1142_ID_SNTL'},
    {'label': 'Pike Creek SNTL (693)', 'value': '693_MT_SNTL'},
    {'label': 'Pine Creek Pass SNTL (695)', 'value': '695_ID_SNTL'},
    {'label': 'Pipestone Pass SNOW (12D01)', 'value': '12D01_MT_SNOW'},
    {'label': 'Placer Basin SNTL (696)', 'value': '696_MT_SNTL'},
    {'label': 'Placer Creek SNOW (16E02)', 'value': '16E02_ID_SNOW'},
    {'label': 'Pocket Creek SNOW (09G11)', 'value': '09G11_WY_SNOW'},
    {'label': 'Pocket Creek SNTL (1133)', 'value': '1133_WY_SNTL'},
    {'label': 'Pole Mountain SNOW (05H01)', 'value': '05H01_WY_SNOW'},
    {'label': 'Poorman Creek SNTL (932)', 'value': '932_MT_SNTL'},
    {'label': 'Porcupine SNTL (700)', 'value': '700_MT_SNTL'},
    {'label': 'Potomageton Park SNOW (11E21)', 'value': '11E21_MT_SNOW'},
    {'label': 'Powder River Pass SNTL (703)', 'value': '703_WY_SNTL'},
    {'label': 'Prairie SNTL (704)', 'value': '704_ID_SNTL'},
    {'label': 'Ptarmigan No 8 SNOW (13A08)', 'value': '13A08_MT_SNOW'},
    {'label': 'Purgatory Gulch SNOW (06H18)', 'value': '06H18_WY_SNOW'},
    {'label': 'Ragged Mountain SNTL (1081)', 'value': '1081_ID_SNTL'},
    {'label': 'Ranger Creek SNOW (07E04)', 'value': '07E04_WY_SNOW'},
    {'label': 'Rattlesnake Spring SNOW (15F19)', 'value': '15F19_ID_SNOW'},
    {'label': 'Red Canyon AM SNOW (16G11)', 'value': '16G11_ID_SNOW'},
    {'label': 'Red Mountain SNOW (15A01)', 'value': '15A01_MT_SNOW'},
    {'label': 'Reno Hill SNTL (716)', 'value': '716_WY_SNTL'},
    {'label': 'Reuter Canyon SNOW (04E03)', 'value': '04E03_WY_SNOW'},
    {'label': 'Revais SNOW (14B06)', 'value': '14B06_MT_SNOW'},
    {'label': 'Reynolds Creek SNTL (2029)', 'value': '2029_ID_SNTL'},
    {'label': 'Reynolds Mountain SNOW (16F08)', 'value': '16F08_ID_SNOW'},
    {'label': 'Reynolds West Fork #1 SNOW (16F10)', 'value': '16F10_ID_SNOW'},
    {'label': 'Reynolds West Fork #2 SNOW (16F09)', 'value': '16F09_ID_SNOW'},
    {'label': 'Reynolds-Dobson Divide SNOW (16F11)', 'value': '16F11_ID_SNOW'},
    {'label': 'Rock Creek Mdws SNOW (15B24)', 'value': '15B24_MT_SNOW'},
    {'label': 'Rock Creek Meadow SNOW (11D21)', 'value': '11D21_MT_SNOW'},
    {'label': 'Rocker Peak SNTL (722)', 'value': '722_MT_SNTL'},
    {'label': 'Rocky Boy SNTL (917)', 'value': '917_MT_SNTL'},
    {'label': 'Rocky Boy SNOW (09A01)', 'value': '09A01_MT_SNOW'},
    {'label': 'Roland Summit SNOW (15B05)', 'value': '15B05_ID_SNOW'},
    {'label': 'Rowdy Creek SNOW (10G21)', 'value': '10G21_WY_SNOW'},
    {'label': 'Ryan Park SNOW (06H06)', 'value': '06H06_WY_SNOW'},
    {'label': 'S Fork Shields SNTL (725)', 'value': '725_MT_SNTL'},
    {'label': 'Sacajawea SNTL (929)', 'value': '929_MT_SNTL'},
    {'label': 'Saddle Mtn. SNTL (727)', 'value': '727_MT_SNTL'},
    {'label': 'Sage Creek Basin SNTL (1015)', 'value': '1015_WY_SNTL'},
    {'label': 'Salt River Summit SNTL (730)', 'value': '730_WY_SNTL'},
    {'label': 'Sand Lake SNTL (731)', 'value': '731_WY_SNTL'},
    {'label': 'Sandpoint Exp Stn SNOW (16A11)', 'value': '16A11_ID_SNOW'},
    {'label': 'Sandstone RS SNTL (732)', 'value': '732_WY_SNTL'},
    {'label': 'Savage Pass SNTL (735)', 'value': '735_ID_SNTL'},
    {'label': 'Sawmill Divide SNOW (07E38)', 'value': '07E38_WY_SNOW'},
    {'label': 'Schwartz Lake SNTL (915)', 'value': '915_ID_SNTL'},
    {'label': 'Schweitzer Basin SNTL (738)', 'value': '738_ID_SNTL'},
    {'label': 'Secesh Summit SNTL (740)', 'value': '740_ID_SNTL'},
    {'label': 'Sedgwick Peak SNTL (741)', 'value': '741_ID_SNTL'},
    {'label': 'Shanghi Summit SNTL (747)', 'value': '747_ID_SNTL'},
    {'label': 'Sheep Mtn. SNTL (749)', 'value': '749_ID_SNTL'},
    {'label': 'Shell Creek SNTL (751)', 'value': '751_WY_SNTL'},
    {'label': 'Sheridan R.S. (New) SNOW (09F15)', 'value': '09F15_WY_SNOW'},
    {'label': 'Sherwin SNTL (752)', 'value': '752_ID_SNTL'},
    {'label': 'Shirts Creek SNOW (16E16)', 'value': '16E16_ID_SNOW'},
    {'label': 'Short Creek SNTL (753)', 'value': '753_MT_SNTL'},
    {'label': 'Shower Falls SNTL (754)', 'value': '754_MT_SNTL'},
    {'label': 'Skalkaho Summit SNTL (760)', 'value': '760_MT_SNTL'},
    {'label': 'Skitwish Ridge SNOW (16B11)', 'value': '16B11_ID_SNOW'},
    {'label': 'Slag-A-Melt Lake SNOW (13D24)', 'value': '13D24_MT_SNOW'},
    {'label': 'Slagamelt Lakes SNTL (1286)', 'value': '1286_MT_SNTL'},
    {'label': 'Sleeping Woman SNTL (783)', 'value': '783_MT_SNTL'},
    {'label': 'Slide Rock Mountain SNOW (13C02)', 'value': '13C02_MT_SNOW'},
    {'label': 'Slug Creek Divide SNTL (761)', 'value': '761_ID_SNTL'},
    {'label': 'Smiley Mountain SNTL (926)', 'value': '926_ID_SNTL'},
    {'label': 'Smuggler Mine SNOW (12D05)', 'value': '12D05_MT_SNOW'},
    {'label': 'Snake River Station SNTL (764)', 'value': '764_WY_SNTL'},
    {'label': 'Snake River Station SNOW (10E12)', 'value': '10E12_WY_SNOW'},
    {'label': 'Snider Basin SNTL (765)', 'value': '765_WY_SNTL'},
    {'label': 'Snow King Mountain SNOW (10F20)', 'value': '10F20_WY_SNOW'},
    {'label': 'Soldier Park SNOW (07E05)', 'value': '07E05_WY_SNOW'},
    {'label': 'Soldier Park SNTL (1132)', 'value': '1132_WY_SNTL'},
    {'label': 'Soldier R.S. SNTL (769)', 'value': '769_ID_SNTL'},
    {'label': 'Somsen Ranch SNTL (770)', 'value': '770_ID_SNTL'},
    {'label': 'Sour Dough SNOW (06E01)', 'value': '06E01_WY_SNOW'},
    {'label': 'South Brush Creek SNTL (772)', 'value': '772_WY_SNTL'},
    {'label': 'South Mtn. SNTL (774)', 'value': '774_ID_SNTL'},
    {'label': 'South Pass SNTL (775)', 'value': '775_WY_SNTL'},
    {'label': 'Spotted Bear Mountain SNOW (13B02)', 'value': '13B02_MT_SNOW'},
    {'label': 'Spring Creek Divide SNTL (779)', 'value': '779_WY_SNTL'},
    {'label': 'Spring Mountain Canyon SNOW (13E30)', 'value': '13E30_ID_SNOW'},
    {'label': 'Spur Park SNTL (781)', 'value': '781_MT_SNTL'},
    {'label': 'Squaw Flat SNTL (782)', 'value': '782_ID_SNTL'},
    {'label': 'Squaw Meadow SNOW (15D02)', 'value': '15D02_ID_SNOW'},
    {'label': 'St. Lawrence Alt SNTL (786)', 'value': '786_WY_SNTL'},
    {'label': 'Stahl Peak SNTL (787)', 'value': '787_MT_SNTL'},
    {'label': 'State Line SNOW (11F01)', 'value': '11F01_ID_SNOW'},
    {'label': 'Stemple Pass SNOW (12C01)', 'value': '12C01_MT_SNOW'},
    {'label': 'Stickney Mill SNTL (792)', 'value': '792_ID_SNTL'},
    {'label': 'Storm Lake SNOW (13C07)', 'value': '13C07_MT_SNOW'},
    {'label': 'Strawberry Creek SNOW (11G09)', 'value': '11G09_ID_SNOW'},
    {'label': 'Stringer Creek SNTL (1009)', 'value': '1009_MT_SNTL'},
    {'label': 'Stryker Basin SNOW (14A17)', 'value': '14A17_MT_SNOW'},
    {'label': 'Stuart Mountain SNTL (901)', 'value': '901_MT_SNTL'},
    {'label': 'Sublett SNOW (12G08)', 'value': '12G08_ID_SNOW'},
    {'label': 'Succor Creek AM SNOW (16F06)', 'value': '16F06_ID_SNOW'},
    {'label': 'Sucker Creek SNTL (798)', 'value': '798_WY_SNTL'},
    {'label': 'Sunset SNTL (803)', 'value': '803_ID_SNTL'},
    {'label': 'Swede Peak SNTL (805)', 'value': '805_ID_SNTL'},
    {'label': 'Sylvan Lake SNTL (806)', 'value': '806_WY_SNTL'},
    {'label': 'Sylvan Road SNTL (807)', 'value': '807_WY_SNTL'},
    {'label': 'T-Cross Ranch SNOW (09F03)', 'value': '09F03_WY_SNOW'},
    {'label': 'Taylor Road SNOW (09A07)', 'value': '09A07_MT_SNOW'},
    {'label': 'Telfer Ranch SNOW (13F06)', 'value': '13F06_ID_SNOW'},
    {'label': 'Ten Mile Lower SNOW (12C02)', 'value': '12C02_MT_SNOW'},
    {'label': 'Ten Mile Middle SNOW (12C03)', 'value': '12C03_MT_SNOW'},
    {'label': 'Tepee Creek SNTL (813)', 'value': '813_MT_SNTL'},
    {'label': 'Teton Pass W.s. SNOW (10F24)', 'value': '10F24_WY_SNOW'},
    {'label': 'Thorson Cabin #2 SNOW (17E06)', 'value': '17E06_ID_SNOW'},
    {'label': 'Thumb Divide SNOW (10E07)', 'value': '10E07_WY_SNOW'},
    {'label': 'Thumb Divide SNTL (816)', 'value': '816_WY_SNTL'},
    {'label': 'Tie Creek SNTL (818)', 'value': '818_WY_SNTL'},
    {'label': 'Timber Creek SNTL (819)', 'value': '819_WY_SNTL'},
    {'label': 'Timberline Creek SNOW (09D04)', 'value': '09D04_MT_SNOW'},
    {'label': 'Tizer Basin SNTL (893)', 'value': '893_MT_SNTL'},
    {'label': 'Togwotee Pass SNOW (10F09)', 'value': '10F09_WY_SNOW'},
    {'label': 'Togwotee Pass SNTL (822)', 'value': '822_WY_SNTL'},
    {'label': 'Tollgate SNOW (15F20)', 'value': '15F20_ID_SNOW'},
    {'label': 'Townsend Creek SNTL (826)', 'value': '826_WY_SNTL'},
    {'label': 'Trinity Mtn. SNTL (830)', 'value': '830_ID_SNTL'},
    {'label': 'Trinkus Lake SNOW (13B01)', 'value': '13B01_MT_SNOW'},
    {'label': 'Triple Peak SNTL (831)', 'value': '831_WY_SNTL'},
    {'label': 'Tripod Summit SNOW (16E03)', 'value': '16E03_ID_SNOW'},
    {'label': 'Truman Creek SNOW (14A18)', 'value': '14A18_MT_SNOW'},
    {'label': 'Turpin Meadows SNOW (10F05)', 'value': '10F05_WY_SNOW'},
    {'label': 'Twelvemile Creek SNTL (835)', 'value': '835_MT_SNTL'},
    {'label': 'Twenty-One Mile SNOW (11E06)', 'value': '11E06_MT_SNOW'},
    {'label': 'Twin Lakes SNTL (836)', 'value': '836_MT_SNTL'},
    {'label': 'Twin Spirit Divide SNOW (16B12)', 'value': '16B12_ID_SNOW'},
    {'label': 'Two Ocean Plateau SNTL (837)', 'value': '837_WY_SNTL'},
    {'label': 'Tyrell R.S. SNOW (07E35)', 'value': '07E35_WY_SNOW'},
    {'label': 'Upper Elkhorn SNOW (12G10)', 'value': '12G10_ID_SNOW'},
    {'label': 'Upper Holland Lake SNOW (13B05)', 'value': '13B05_MT_SNOW'},
    {'label': 'Upper Home Canyon SNOW (11G26)', 'value': '11G26_ID_SNOW'},
    {'label': 'Upper Spearfish SNOW (03E01)', 'value': '03E01_SD_SNOW'},
    {'label': 'Valley View SNOW (11E08)', 'value': '11E08_ID_SNOW'},
    {'label': 'Van Wyck SNTL (979)', 'value': '979_ID_SNTL'},
    {'label': 'Vaught Ranch AM SNOW (16G12)', 'value': '16G12_ID_SNOW'},
    {'label': 'Vienna Mine SNTL (845)', 'value': '845_ID_SNTL'},
    {'label': 'Waldron SNTL (847)', 'value': '847_MT_SNTL'},
    {'label': 'Warm Springs SNTL (850)', 'value': '850_MT_SNTL'},
    {'label': 'Weasel Divide SNOW (14A07)', 'value': '14A07_MT_SNOW'},
    {'label': 'Webb Creek #2 SNOW (16C21)', 'value': '16C21_ID_SNOW'},
    {'label': 'Webber Creek SNOW (12E05)', 'value': '12E05_ID_SNOW'},
    {'label': 'Webber Springs SNTL (852)', 'value': '852_WY_SNTL'},
    {'label': 'West Branch SNTL (855)', 'value': '855_ID_SNTL'},
    {'label': 'West Yellowstone SNTL (924)', 'value': '924_MT_SNTL'},
    {'label': 'West Yellowstone SNOW (11E07)', 'value': '11E07_MT_SNOW'},
    {'label': 'Whiskey Creek SNTL (858)', 'value': '858_MT_SNTL'},
    {'label': 'Whiskey Park SNTL (859)', 'value': '859_WY_SNTL'},
    {'label': 'White Elephant SNTL (860)', 'value': '860_ID_SNTL'},
    {'label': 'White Mill SNTL (862)', 'value': '862_MT_SNTL'},
    {'label': 'Wildhorse Divide SNTL (867)', 'value': '867_ID_SNTL'},
    {'label': 'Willow Creek SNTL (868)', 'value': '868_WY_SNTL'},
    {'label': 'Willow Flat SNOW (11G04)', 'value': '11G04_ID_SNOW'},
    {'label': 'Wilson Creek SNTL (871)', 'value': '871_ID_SNTL'},
    {'label': 'Windy Peak SNTL (872)', 'value': '872_WY_SNTL'},
    {'label': 'Wolverine SNTL (875)', 'value': '875_WY_SNTL'},
    {'label': 'Wood Creek SNTL (876)', 'value': '876_MT_SNTL'},
    {'label': 'Wood Rock G.S. SNOW (07E13)', 'value': '07E13_WY_SNOW'},
    {'label': 'Worm Creek SNOW (11G28)', 'value': '11G28_ID_SNOW'},
    {'label': 'Wrong Creek SNOW (12B04)', 'value': '12B04_MT_SNOW'},
    {'label': 'Wrong Ridge SNOW (12B03)', 'value': '12B03_MT_SNOW'},
    {'label': 'Younts Peak SNTL (878)', 'value': '878_WY_SNTL'},
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
            dcc.Dropdown(id='triplet1', options=all_sites, value='07E05_WY_SNOW'),
        ]),
        dbc.Col([
            html.H2('Site 2'),
            dcc.Dropdown(id='triplet2', options=all_sites, value='1132_WY_SNTL'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H6('Note: Type in site name or scroll through list. Site lists include all SNOTEL and Snow Courses in '
                    'MT, WY, SD, and ID. Refresh web browser if having issues selecting new sites.'),
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
        html.H3('Filtered Scatter Plot'),
        html.H6('Note: The trendline is calculated using Ordinary Least Squares (OLS) trendline function.'),
        html.Br(),
        html.H5('Select Months to Include'),
        html.Div(
            dcc.Checklist(
                id='list-months',
                options=[
                    {'label': 'January 1st |', 'value': 1},
                    {'label': 'February 1st |', 'value': 2},
                    {'label': 'March 1st |', 'value': 3},
                    {'label': 'April 1st |', 'value': 4},
                    {'label': 'May 1st |', 'value': 5},
                    {'label': 'June 1st |', 'value': 6},
                ],
                value=[1, 2, 3, 4, 5, 6],
            )
        ),
        html.Div(
            dcc.Graph(id='filtered-scatter-plot')),
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
        df.index = pd.to_datetime(df.index, format='%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%Y')
        df = df.reset_index()
        df.rename(columns={'index': 'DATE'}, inplace=True)
        fig = px.scatter(data_frame=df, x=id1, y=id2, trendline="ols", marginal_x="box", marginal_y="box")

        model = px.get_trendline_results(fig)
        results = model.iloc[0]["px_fit_results"]
        nobs = results.nobs
        alpha = results.params[0]
        beta = results.params[1]
        p_beta = results.pvalues[1]
        r_squared = results.rsquared

        line1 = 'y = ' + str(round(alpha, 4)) + ' + ' + str(round(beta, 4))+'x'
        line2 = 'p-value = ' + '{:.5f}'.format(p_beta)
        line3 = 'R^2 = ' + str(round(r_squared, 3))
        line4 = 'n = ' + str(int(nobs))
        summary = line1 + '<br>' + line2 + '<br>' + line3 + '<br>' + line4

        fig.add_annotation(
            xref="x",
            yref="paper",
            x=df[id1].max(),
            y='0',
            text=summary,
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
            ),
            align="right",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            borderwidth=2,
            borderpad=4,
            bgcolor="rgba(100,100,100, 0.6)",
            opacity=0.8
        )
        return fig
    else:
        return None


@app.callback(Output('filtered-scatter-plot', 'figure'),
              [Input('triplet1', 'value'),
               Input('triplet2', 'value'),
               Input('list-months', 'value')
               ])
def update_scatter_filtered(id1, id2, months):
    if id1 and id2 and id1 != id2:
        df = site_data(id1, id2)
        df = df.reset_index()
        df.rename(columns={'index': 'DATE'}, inplace=True)
        df1 = df.loc[df['DATE'].dt.month.isin(months)]
        fig = px.scatter(data_frame=df1, x=id1, y=id2, trendline="ols", marginal_x="box", marginal_y="box")

        model = px.get_trendline_results(fig)
        results = model.iloc[0]["px_fit_results"]
        nobs = results.nobs
        alpha = results.params[0]
        beta = results.params[1]
        p_beta = results.pvalues[1]
        r_squared = results.rsquared

        line1 = 'y = ' + str(round(alpha, 4)) + ' + ' + str(round(beta, 4))+'x'
        line2 = 'p-value = ' + '{:.5f}'.format(p_beta)
        line3 = 'R^2 = ' + str(round(r_squared, 3))
        line4 = 'n = ' + str(int(nobs))
        summary = line1 + '<br>' + line2 + '<br>' + line3 + '<br>' + line4

        fig.add_annotation(
            xref="x",
            yref="paper",
            x=df[id1].max(),
            y='0',
            text=summary,
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
            ),
            align="right",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            borderwidth=2,
            borderpad=4,
            bgcolor="rgba(100,100,100, 0.6)",
            opacity=0.8
        )
        return fig
    else:
        return None


@app.callback(Output('line-plot', 'figure'),
              [Input('triplet1', 'value'),
               Input('triplet2', 'value')
               ])
def update_lineplot(id1, id2):
    if id1 and id2 and id1 != id2:
        df = site_data(id1, id2)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%Y')
        df = df.reset_index()
        df.rename(columns={'index': 'DATE'}, inplace=True)
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
        df.index = pd.to_datetime(df.index, format='%Y-%m-%dT%H:%M:%S').strftime('%m-%d-%Y')
        df = df.reset_index()
        df.rename(columns={'index': 'DATE'}, inplace=True)
        df['Difference'] = (df[triplet1] - df[triplet2]).round(1)
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
