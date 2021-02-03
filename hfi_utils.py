# /media/neeraj/Yugal/Coding/jupyternotebooks/0. Personal Projects/Fraser

import numpy as np
import pandas as pd
from tabula import read_pdf
import pickle
import fitz
import random
#Helper Functions

def get_data(page_no):
    try :
        assert page_no >= 0
        assert page_no <=420
        
        print("Getting data for page no. : ", page_no , "\n")
        
        df= read_pdf('hfi2020.pdf',pages=str(page_no))
        df=df[0]
        df.rename( columns={'Unnamed: 0':'Indicator'}, inplace=True )
        df=df.dropna()
        
        def strip(text):
            try:
                return text.replace(" ", "")

            except AttributeError:
                return text
            
        for ind, column in enumerate(df.columns):
            if ind>0:
                df[column]=df[column].apply(lambda x : strip(x))
                
        df=df.reset_index()
        df=df.drop('index',axis=1)
        print("Data for pageno ", page_no, " successfully imported.\n","--"*40,"\n")
        return df
    
    except AssertionError:
        print(f"{page_no} looks Like an Invalid Page number")
        
        
def clean_transpose(dictionary):

    country_names=list(dictionary.keys())
    updated_datadict = {}
    for i in country_names:

        indicator_name = list(dictionary[i].transpose().iloc[0])
        transposed_df = dictionary[i].replace('-', np.nan).transpose().iloc[1:]
        transposed_df.columns = indicator_name
        transposed_df = transposed_df.transform(lambda x: pd.to_numeric(x))
        transposed_df = transposed_df.transform(lambda x : x.fillna(x.mean()))
        updated_datadict[i]=transposed_df
        
    return updated_datadict
    
    
def store_data(datadict, filename = 'HFI_Countries.pickle'):
    import pickle

    # Store data (serialize)
    with open(filename, 'wb') as handle:
        pickle.dump(datadict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Load data (deserialize)
    with open(filename, 'rb') as handle:
        unserialized_data = pickle.load(handle)

    return print("--"*18 + "Done" + "--"*18)

def get_country_names():
    # For Testing Purposes
    country_names = np.array(['INDIA','CHINA','PAKISTAN','NEPAL',

     'BANGLADESH',
     'BHUTAN',
     'UNITED KINGDOM',
     'UNITED STATES', 'AUSTRALIA',
     'ALGERIA',
     'ANGOLA',
     'ARGENTINA',
     'ARMENIA',
     'ALBANIA',
     'AUSTRIA',
     'AZERBAIJAN',
     'BAHAMAS, THE',
     'BAHRAIN',
     'BARBADOS',
     'BELARUS',
     'BELGIUM',
     'BELIZE',
     'BENIN',
     'BOLIVIA',
     'BOSNIA AND HERZEGOVINA',
     'BOTSWANA',
     'BRAZIL',
     'BRUNEI DARUSSALAM',
     'BULGARIA',
     'BURKINA FASO',
     'BURUNDI',
     'CABO VERDE',
     'CAMBODIA',
     'CAMEROON',
     'CANADA',
     'CENTRAL AFRICAN REPUBLIC',
     'CHAD',
     'CHILE',
     'COLOMBIA',
     'CONGO, DEM. REP.',
     'CONGO, REP. OF',
     'COSTA RICA',
     'CÔTE D’IVOIRE',
     'CROATIA',
     'CYPRUS',
     'CZECH REPUBLIC',
     'DENMARK',
     'DOMINICAN REPUBLIC',
     'ECUADOR',
     'EGYPT, ARAB REP.',
     'EL SALVADOR',
     'ESTONIA',
     'ESWATINI',
     'ETHIOPIA',
     'FIJI',
     'FINLAND',
     'FRANCE',
     'GABON',
     'GAMBIA, THE',
     'GEORGIA',
     'GERMANY',
     'GHANA',
     'GREECE',
     'GUATEMALA',
     'GUINEA',
     'GUINEA-BISSAU',
     'GUYANA',
     'HAITI',
     'HONDURAS',
     'HONG KONG SAR, CHINA',
     'HUNGARY',
     'ICELAND',
     'INDONESIA',
     'IRAN, ISLAMIC REP.',
     'IRAQ',
     'IRELAND',
     'ISRAEL',
     'ITALY',
     'JAMAICA',
     'JAPAN',
     'JORDAN',
     'KAZAKHSTAN',
     'KENYA',
     'KOREA, REP. OF',
     'KUWAIT',
     'KYRGYZ REPUBLIC',
     'LAO PDR',
     'LATVIA',
     'LEBANON',
     'LESOTHO',
     'LIBERIA',
     'LIBYA',
     'LITHUANIA',
     'LUXEMBOURG',
     'MADAGASCAR',
     'MALAWI',
     'MALAYSIA',
     'MALI',
     'MALTA',
     'MAURITANIA',
     'MAURITIUS',
     'MEXICO',
     'MOLDOVA',
     'MONGOLIA',
     'MONTENEGRO',
     'MOROCCO',
     'MOZAMBIQUE',
     'MYANMAR',
     'NAMIBIA',
     'NETHERLANDS',
     'NEW ZEALAND',
     'NICARAGUA',
     'NIGER',
     'NIGERIA',
     'NORTH MACEDONIA',
     'NORWAY',
     'OMAN',
     'PANAMA',
     'PAPUA NEW GUINEA',
     'PARAGUAY',
     'PERU',
     'PHILIPPINES',
     'POLAND',
     'PORTUGAL',
     'QATAR',
     'ROMANIA',
     'RUSSIAN FEDERATION',
     'RWANDA',
     'SAUDI ARABIA',
     'SENEGAL',
     'SERBIA',
     'SEYCHELLES',
     'SIERRA LEONE',
     'SINGAPORE',
     'SLOVAK REPUBLIC',
     'SLOVENIA',
     'SOUTH AFRICA',
     'SPAIN',
     'SRI LANKA',
     'SUDAN',
     'SURINAME',
     'SWEDEN',
     'SWITZERLAND',
     'SYRIAN ARAB REPUBLIC',
     'TAIWAN',
     'TAJIKISTAN',
     'TANZANIA',
     'THAILAND',
     'TIMOR-LESTE',
     'TOGO',
     'TRINIDAD AND TOBAGO',
     'TUNISIA',
     'TURKEY',
     'UGANDA',
     'UKRAINE',
     'UNITED ARAB EMIRATES',
     'URUGUAY',
     'VENEZUELA, RB',
     'VIETNAM',
     'YEMEN, REP. OF',
     'ZAMBIA',
     'ZIMBABWE'])

    return country_names
