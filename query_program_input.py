#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:42:35 2020

@author: sahyadri
"""


from astroquery.vizier import Vizier
import sys
from astroquery.vizier import Vizier
import requests
from bs4 import BeautifulSoup
from astroquery.simbad import Simbad
import numpy as np
from astropy.table import Table
from astroquery.xmatch import XMatch
from astropy.io import ascii
from astropy import units as u

print('Downloading constellation_borders.csv...')
catalogue_list = Vizier.find_catalogs("Constellation")#This loads all the catalogs by the keyword "constellation"
Vizier.ROW_LIMIT = -1
catalog = Vizier.get_catalogs("VI/49")#This selects the 2nd of three tables that were found by the key-word search. This table contains relevant data
catalog[1].write("constellation_borders.csv",format="csv",overwrite="True")#creates a csv file
print('\n')
print('Done')
print('\n')
print('Parsing through HyperLEDA...')
#will add all mags into an array
mags = []
for i in range(110):
    page = requests.get("http://leda.univ-lyon1.fr/ledacat.cgi?o=M{}".format(i+1))
    soup = BeautifulSoup(page.content,'html.parser')
    if len(soup.find_all('table',attrs={"class":"datatable"}))!=0:
        table_rel = soup.find_all('table',attrs={"class":"datatable"})[1]
        index = 0
        for rows in table_rel.find_all('tr'):
            if rows.find_all('a', attrs = {"title":"Total V-magnitude"}) != []:
                            mag_value = rows.find_all('td')[1].get_text().split()[0]
                            mags.append(mag_value)
                            index = index + 1
                            break
            if rows == table_rel.find_all('tr')[-1] and index == 0:
                mags.append('-')
                break
    else:
        mags.append('-')
        continue
print('\n')
print('Done')
print('\n')
print('Downloading Messier Catalogue...')

#the next three lines are to simplify the output table
Simbad.reset_votable_fields()
Simbad.remove_votable_fields('coordinates')
Simbad.add_votable_fields('otype(S)', 'ra(d;A;ICRS;J2000;2000)', 'dec(d;D;ICRS;J2000;2000)','distance','flux(B)','flux(V)','flux_unit(V)')#These are all the columns added to the table

result_table = Simbad.query_catalog("Messier")#This asks the SIMBAD database to list all objects from the messier catalog
result_table['V Mag (from HyperLeda/SED)'] = mags#adding v mags
result_table.write("messier_objects.csv",format="csv",overwrite="True")#creates a csv file

Simbad.reset_votable_fields()#renders the prev changes to simbad class temporary.
print('\n')
print('Done')
print('\n')
while True:
    status = input('About to download NGC catalogue. Big file - proceed? (y/n)',)
    if status=="n":
        n_run = True
    elif status == "y":
        n_run = False
        break
    else:
        print("invalid entry")
while n_run:
    print('Downloading NGC catalogue...')
    v = Vizier(columns = ['Name','Type','mag','Const','RA (deg)','Dec (deg)'])#Columns added to table
    v.ROW_LIMIT = -1
    result_table = v.get_catalogs("VII/118/ngc2000")[0]
    result_table.write("NGC.csv",format="csv",overwrite="True")
    print('\n')
    print('Done')
    print('\n')
    break

print('Tycho-2 Catalogue')
MinVmag = input('(INT ONLY) Input minimum value of Vmag (skippable)',)
while True:
    MaxVmag = int(input('(INT ONLY) Input maximum value of Vmag',))
    if type(MaxVmag)==int:
        break
    else:
        print("invalid entry")
if MinVmag!='':
    MinVmag = int(MinVmag)    
run_count = 0
run = True

while run:
    run_count = run_count +1
    if MinVmag=='':
        filter_input = "<{}".format(MaxVmag)
    else:
        filter_input = "{}..{}".format(MinVmag, MaxVmag)
    v = Vizier(columns = ['HIP','TYC','HD','_RAJ2000','DECJ2000','B-V','Vmag','Plx'], column_filters = {"Vmag":"{}".format(filter_input)})
    v.ROW_LIMIT = -1
    v.TIMEOUT = 1000
    catalog_stars = v.get_catalogs("I/239/tyc_main")[0]
    catalog_stars.write("tycho_{}.csv".format(run_count),format="csv",overwrite = "True")
    while True:
        status = input("Another run of Tycho database download? (y/n)",)
        if status == "n":
            run = False
            break
        elif status == "y":
            run = True
            break
        else:
            print("invalid answer")
print('Done')
print('\n')
while True:
    g_status = input('Gaia - Do you want to skip? (y/n)',)
    if g_status == "y":
        g_run = False
        break
    elif g_status == "n":
        g_run = True
        break
    else:
        print('invalid answer')
        
print('Gaia dr1 catalogue')

MinVmag = input('(INT ONLY) Input minimum value of Vmag (skippable)',)
while True:
    MaxVmag = int(input('(INT ONLY) Input maximum value of Vmag',))
    if type(MaxVmag)==int:
        break
    else:
        print("invalid entry")
if MinVmag!='':
    MinVmag = int(MinVmag)    

run_count = 0
while g_run:
    if MinVmag=='':
        filter_input = "<{}".format(MaxVmag)
    else:
        filter_input = "{}..{}".format(MinVmag, MaxVmag)
    run_count = run_count + 1
    v = Vizier(columns = ['HIP','TYC','_RAJ2000','DECJ2000','<Gmag>','VTmag','BTmag','Plx'], column_filters = {"Vmag":"{}".format(filter_input)})
    v.ROW_LIMIT = 50
    v.TIMEOUT = 1000
    catalog_stars = v.get_catalogs("I/337/tgasptyc")[0]
    vmag = catalog_stars['VTmag']-0.09*(catalog_stars['BTmag']-catalog_stars['VTmag'])
    catalog_stars['Vmag'] = vmag
    plx = catalog_stars['Plx']
    catalog_stars.remove_columns(['VTmag','BTmag','__Gmag_','Plx'])
    catalog_stars['Plx'] = plx
    catalog_stars.write("gaia_tgas_{}.csv".format(run_count),format="csv",overwrite = "True")
    while True:
        status = input("Another run of Gaia database download? (y/n)",)
        if status == "n":
            g_run = False
            break
        elif status == "y":
            g_run = True
            break
        else:
            print("invalid answer")
print('Done')
print('\n')
print('Downloading BSC5P...')
catalog_strs = Vizier.get_catalogs("V/50")
Vizier.ROW_LIMIT = -1
catalog_strs[0].write("BSC5P.csv",format="csv",overwrite="True")
print('\n')
print('Done')
print('\n')
print('Downloading Star Names..')
names = []
hr_no = []
const = []
ident = []
vmag = []
ra = []
dec = []


page = requests.get("https://www.iau.org/public/themes/naming_stars/")
soup_page = BeautifulSoup(page.content,'html.parser')
table = soup_page.find_all("table",attrs = {"class":"table sortable"})[0]
table_rows = table.find_all("tr")[1:]
for rows in table_rows:
    columns = rows.find_all("td")
    names.append(columns[0].get_text())
    hr_no.append(columns[1].get_text())
    ident.append(columns[2].get_text())
    const.append(columns[3].get_text())
    vmag.append(columns[6].get_text())
    ra.append(columns[7].get_text())
    dec.append(columns[8].get_text())
    

ascii.write([names,hr_no,ident,const,vmag,ra,dec],"IAU_names.csv",format="csv",names = ['Name','HR','ID','Const','Vmag','RA','Dec'],overwrite="True")
print('Done')