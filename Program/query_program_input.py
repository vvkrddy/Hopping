#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:42:35 2020

@author: sahyadri
"""


from astroquery.vizier import Vizier
import requests
from bs4 import BeautifulSoup
from astroquery.simbad import Simbad
import numpy as np
from astropy.table import Table, vstack
from astropy.io import ascii
from astropy import units as u
from astropy.coordinates import SkyCoord, get_constellation
import pandas as pd 
#import kaggle
from astroquery.gaia import Gaia
import glob, os

print('Downloading constellation_borders.csv...')
catalogue_list = Vizier.find_catalogs("Constellation")#This loads all the catalogs by the keyword "constellation"
Vizier.ROW_LIMIT = -1
catalog = Vizier.get_catalogs("VI/49")[1]#This selects the 2nd of three tables that were found by the key-word search. This table contains relevant data
catalog.remove_columns(['cst','type'])
coords = SkyCoord(catalog['RAJ2000'],catalog['DEJ2000'],unit="deg")
const = coords.get_constellation()
catalog.add_column(const,name="Constellation", index = 2)
catalog.write("constellation_borders.csv",format="csv",overwrite="True")
print('\n')
print('Done')
print('\n')
print('Downloading Messier Catalogue...')

#the next three lines are to simplify the output table
Simbad.reset_votable_fields()
Simbad.remove_votable_fields('coordinates')
Simbad.add_votable_fields('otype(3)', 'ra(d;A;ICRS;J2000;2000)', 'dec(d;D;ICRS;J2000;2000)','flux(B)','flux(V)')#These are all the columns added to the table

result_table = Simbad.query_catalog("Messier")#This asks the SIMBAD database to list all objects from the messier catalog
result_table['FLUX_V'].name = 'V'
result_table['OTYPE_3']=[x.decode('utf8') for x in result_table['OTYPE_3']]
result_table['MAIN_ID']=[x.decode('utf8') for x in result_table['MAIN_ID']]
result_table['RA_d_A_ICRS_J2000_2000'].name = "RAJ2000"
result_table['DEC_d_D_ICRS_J2000_2000'].name = "DEJ2000"
result_table['B-V'] = result_table['FLUX_B'] - result_table['V']
result_table.remove_column('FLUX_B')

coords = SkyCoord(result_table['RAJ2000'],result_table['DEJ2000'],unit="deg")
const = coords.get_constellation()
const_abr = coords.get_constellation(short_name = "True")
result_table.add_column(const,name="Constellation", index = 2)

otype = result_table['OTYPE_3']
internal_id = [otype[i]+'_'+const_abr[i]+'_'+str(i+1) for i in range(len(const))]
result_table.add_column(internal_id, name = "Internal ID Number", index = 0)

result_table.write("messier_objects.csv",format="csv",overwrite="True")#creates a csv file

Simbad.reset_votable_fields()#renders the prev changes to simbad class temporary.
print('\n')
print('Done')
print('\n')
print('Downloading NGC catalogue...')

#CHANGE GET_CONSTELLATION EQUINOX FROM B1875 TO 2000
v = Vizier(columns = ['Name','Type','mag','RA (deg)','Dec (deg)'])#Columns added to table
v.ROW_LIMIT = -1
result_table = v.get_catalogs("VII/118/ngc2000")[0]

result_table['Name'] = ['IC '+x[1:] if x[0]=='I' else 'NGC '+x for x in result_table['Name']]
result_table['Type'] = ['Gal' if x=='Gx' else 'OpC' if x=='OC' else 'GlC' if x=='Gb' else 'PN' if x=='Pl' else 'Str' if x=='*' or x=='D*' or x=='***' else '-' if x == '' or x=='-' or x=='?' else x for x in result_table['Type']]

coords = SkyCoord(result_table['_RAJ2000'],result_table['_DEJ2000'],unit="deg")
const = coords.get_constellation()
const_abr = coords.get_constellation(short_name = "True")
result_table.add_column(const,name="Constellation", index = 2)

otype = result_table['Type']
internal_id = [otype[i]+'_'+const_abr[i]+'_'+str(i+1) if otype[i]!='-' else 'notype'+'_'+const_abr[i]+'_'+str(i+1) for i in range(len(const))]
result_table.add_column(internal_id, name = "Internal ID Number", index = 0)
result_table.write("NGC.csv",format="csv",overwrite="True")

#cross catalogue for NGC
v = Vizier(columns = ['Object','Name'])
v.ROW_LIMIT = -1
v.TIMEOUT = 1000
cross_catalog = v.get_catalogs('VII/118/names')[0]
cross_catalog['Name'] =  ['IC '+x.split()[1] if len(x.split())==2 and x.split()[0]=="I" else 'IC'+x.split()[0][1:] if len(x.split())==1 and x.split()[0]=="I" else 'NGC '+x for x in cross_catalog['Name']]
cross_catalog.write("DsCrossCatalog.csv",format='csv',overwrite="True")

ccat = pd.read_csv('DsCrossCatalog.csv')
ccat = pd.DataFrame(ccat)
ccat = ccat.loc[~ccat.Name.duplicated(keep='first')]
ntable= pd.read_csv('NGC.csv')
ntable = pd.DataFrame(ntable)
ntable.insert(2,"Common Name",np.zeros(len(ntable['_RAJ2000'])))
ntable['Common Name'] = ntable.Name.map(ccat.set_index('Name').Object,na_action="ignore")
ntable.to_csv('NGC.csv')
ntable = Table.read('NGC.csv')
ntable.remove_columns(['col0'])
ntable.write('NGC.csv',format='csv',overwrite="True")

print('\n')
print('Done')
print('\n')

#Download the star name file
#kaggle.api.authenticate()
#kaggle.api.dataset_download_files('ecotner/named-stars/IAU-CSN.csv', path='/home/sahyadri/Desktop/Star-Hopping', unzip=True)

#CROSS CATALOG
v = Vizier(columns = ['HD','TYC','HIP','Vmag','Fl','Bayer','Cst'])
v.ROW_LIMIT = -1
v.TIMEOUT = 1000
cross_catalog = v.get_catalogs('IV/27A/catalog')[0]
bayer_const = [x['Bayer']+' '+x['Cst'] for x in cross_catalog]
cross_catalog.remove_columns("Bayer")
cross_catalog['BayerConst'] = bayer_const
cross_catalog.write("CrossCatalog.csv",format='csv',overwrite="True")

print('Tycho-2 Catalogue')

run_count = 0
run = True
last_id = 0
while run:
    
    MinVmag = input('(INT ONLY) Input minimum value of Vmag (skippable) ',)
    MaxVmag = int(input('(INT ONLY) Input maximum value of Vmag ',))

    if type(MaxVmag)!=int:
        print("invalid entry")
        continue
    if MinVmag!='':
        MinVmag = int(MinVmag) 
    
    run_count = run_count +1
    if MinVmag=='':
        filter_input = "<{}".format(MaxVmag)
    else:
        filter_input = "{}..{}".format(MinVmag, MaxVmag)
    
    v = Vizier(columns = ['HIP','TYC','HD','_RAJ2000','DECJ2000','+Vmag','B-V'], column_filters = {"Vmag":"{}".format(filter_input)})
    v.ROW_LIMIT = 1000000000
    v.TIMEOUT = 1000
    catalog_stars = v.get_catalogs("I/239/tyc_main")[0]
    catalog_stars['Vmag'].name = "V"
    
    coords = SkyCoord(catalog_stars['_RAJ2000'],catalog_stars['_DEJ2000'],unit="deg")
    const = coords.get_constellation()
    const_abr = coords.get_constellation(short_name = "True")
    
    catalog_stars.add_column(const,name="Constellation", index = 0)
    
    internal_id = ["Str_"+const_abr[i]+"_"+f"{i+last_id+1:08d}" for i in range(len(catalog_stars['_RAJ2000']))]
    catalog_stars.add_column(internal_id, name="Internal ID Number", index = 0)
    
    catalog_stars.write("tycho_{}.csv".format(run_count),format="csv",overwrite = "True")
    last_id = last_id + len(catalog_stars['_RAJ2000'])

    #Adding common names to the stars
    names_table = pd.read_csv('IAU-CSN.csv')
    names_table = pd.DataFrame(names_table)
    ttable = pd.read_csv('tycho_{}.csv'.format(run_count))
    ttable = pd.DataFrame(ttable)
    names_table["HIP"] = [x if x!='-' else 0 for x in names_table["HIP"]]
    ttable.insert(1,"Name",np.zeros(len(ttable['TYC'])))
    names_table["HIP"] = pd.to_numeric(names_table['HIP'],errors='coerce')
    ttable['Name'] = ttable.HIP.map(names_table.set_index('HIP').Name)
    ttable.to_csv('tycho_{}.csv'.format(run_count))
    

    #The cross cataloguing part
    ccat = pd.read_csv('CrossCatalog.csv')
    ccat = pd.DataFrame(ccat)
    ccat["HIP"].fillna("0", inplace = True)
    ttable = pd.read_csv('tycho_{}.csv'.format(run_count))
    ttable = pd.DataFrame(ttable) 
    ccat = ccat.loc[~ccat.HIP.duplicated(keep='first')]
    ttable.insert(4,"Bayer",np.zeros(len(ttable['_RAJ2000'])))    
    ttable['Bayer'] = ttable.HIP.map(ccat.set_index('HIP').BayerConst,na_action="ignore")    
    ttable.to_csv('tycho_{}.csv'.format(run_count))    
    ttable = Table.read('tycho_{}.csv'.format(run_count))
    ttable.remove_columns(['col0','Unnamed: 0'])
    ttable.write('tycho_{}.csv'.format(run_count),format='csv',overwrite="True")
      
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
            
name_list = []
for file in glob.glob("tycho_*.csv"):
    name_list.append(file)
name_list.sort()
t = pd.concat([pd.read_csv(i) for i in name_list])
t.to_csv('tycho.csv')
            
#print('Done')
#print('\n')
#g_status = input('Gaia - Do you want to skip? (y/n)',)
#while True:
#    if g_status == "y":
#        g_run = False
#        break
#    elif g_status == "n":
#        g_run = True
#        break
#    else:
#        print('invalid answer')
           

#run_count = 0
#while g_run:
#    print('Gaia dr1 catalogue')

#   MinVmag = input('(INT ONLY) Input minimum value of Vmag (skippable)',)
#    MaxVmag = int(input('(INT ONLY) Input maximum value of Vmag',))
#    if type(MaxVmag)==int:
#        break
#    else:
#       print("invalid entry")
#        continue
#    if MinVmag!='':
#        MinVmag = int(MinVmag) 
#
#    if MinVmag=='':
#        filter_input = "<{}".format(MaxVmag)
#    else:
#        filter_input = "between {} and {}".format(MinVmag, MaxVmag)
#    run_count = run_count + 1
#
#    Gaia.ROW_LIMIT = -1
#    
#    job = Gaia.launch_job_async("select ra,dec,phot_g_mean_mag from gaiadr1.gaia_source where (phot_g_mean_mag {}) order by phot_g_mean_mag".format(filter_input))
#    r = job.get_results()
#    r.write('gaia.csv',format='csv',overwrite="True")
#    while True:
#        status = input("Another run of Gaia database download? (y/n)",)
#        if status == "n":
#           g_run = False
#            break
#        elif status == "y":
#            g_run = True
#            break
#        else:
#            print("invalid answer")
print('Done')