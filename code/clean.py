# %%
import pandas as pd
import numpy as np
import pysal as ps
from pysal.lib.weights import KNN

# %%
# clean shortages dataset
sh = pd.read_csv("./data/shortages.csv", usecols=['Report Date', 'LATITUDE', 'LONGITUDE'])
sh.columns = sh.columns.str.lower()
sh = sh.rename(columns={'report date': 'date'})

sh.date = pd.to_datetime(sh.date, errors='coerce', infer_datetime_format=True)
sh['y'] = sh.date.dt.to_period('Y')

sh.shape

sh.to_csv('./cleaned/sh.csv', index=False)

# %%
# clean wells dataset

wells = pd.read_csv('./data/gama_allwells.csv', encoding_errors='replace',
                    usecols=['gm_latitude', 'gm_longitude', 'gm_gis_gama_study_area'])

wells.columns = wells.columns.str.replace('gm_', '')
wells.shape
wells.to_csv('./cleaned/wells.csv', index=False)

# keep only central valley wells
wells['gis_gama_study_area'] = wells.gis_gama_study_area.astype('category')
wells = wells[wells.gis_gama_study_area.isin(['NORTHERN SACRAMENTO VALLEY', 'MIDDLE SACRAMENTO VALLEY',
                                              'SOUTHERN SACRAMENTO VALLEY', 'NORTHERN SAN JOAQUIN VALLEY', 'WESTERN SAN JOAQUIN VALLEY',
                                              'CENTRAL EASTSIDE', 'MADERA/CHOWCHILLA', 'SOUTHEAST SAN JOAQUIN VALLEY', 'KERN'])]
wells.shape

# %%
# get stations data
st = pd.read_csv('./data/stations.csv', usecols=['SITE_CODE', 'LATITUDE', 'LONGITUDE'])
st.columns = st.columns.str.lower()
st.shape

st.to_csv('./cleaned/st.csv', index=False)


# %%
# get water surface elevation changes data

ch = pd.read_csv('./data/gw_seasonal_change.csv', usecols=[
                 'SITE_CODE', 'WSE_CHANGE', 'WSE_EARLY', 'WSE_LATE', 'GSE_EARLY', 'MSMT_YEAR_EARLY', 'MSMT_YEAR_LATE'])
ch.columns = ch.columns.str.lower()
ch


def annualmean(change, early, late):
    span = late-early
    return change / span


ch['wse_ch_av'] = annualmean(ch.wse_change, ch.msmt_year_early, ch.msmt_year_late)


ch.columns
ch.shape
# 10793 stations
ch.site_code.nunique()
# get average change for each station
ch_agg = ch.groupby(['site_code']).wse_ch_av.mean().reset_index()

ch_agg

# ch_agg.to_csv('./cleaned/ch.csv', index=False)

# %%
# measurements data

me = pd.read_csv('./data/measurements.csv', usecols=[
    'SITE_CODE', 'MSMT_DATE', 'GWE'])

me.columns = me.columns.str.lower()

me.msmt_date = pd.to_datetime(me.msmt_date.str.split(' ').str[0], infer_datetime_format=True)
me = me.loc[me.msmt_date > pd.Timestamp(2013, 1, 1)]

me.columns

me = me.dropna(axis=0)
me['m'] = me.msmt_date.dt.to_period('M')
me.m.nunique()
me.shape
me.site_code.nunique()

me = me.sort_values(['site_code', 'msmt_date'])
me
# %%


me_f = me.groupby(['site_code', 'm']).mean().reset_index()
me_f.shape
me_f['month'] = me_f.m.dt.to_timestamp()
me_f.tail()

# forward fill every month

me_f.index = pd.DatetimeIndex(me_f.month)
me_f = me_f.drop(columns=['m', 'month'])
me_f
me_pad = me_f.groupby('site_code').resample('MS').pad()

me_pad = me_pad.drop(columns=['site_code']).reset_index()

me_pad.shape

me_pad[0:5]

# compute first difference
me_pad['d_gwe'] = me_pad.groupby(['site_code'])['gwe'].transform(lambda x: x.diff())


# %%
# create aggregate measurements
me_agg = me_pad.groupby('site_code').d_gwe.mean().reset_index()
me_agg

# %%
# merge st, me_agg, and ch_agg
d = st.merge(me_agg, on='site_code', how='left').merge(ch_agg, on='site_code', how='left')
d = d.dropna(how='all', subset=['d_gwe', 'wse_ch_av'])
d.shape

# d is the dataset of predictors
# d.to_csv('./cleaned/d.csv', index=False)

# %%
# aggregate by blocks


def round_to(series, nearest):
    return (round(series / nearest) * nearest)


factor = 0.05
d[['latitude', 'longitude']] = round_to(d[['latitude', 'longitude']], factor)
wells[['latitude', 'longitude']] = round_to(wells[['latitude', 'longitude']], factor)
sh[['latitude', 'longitude']] = round_to(sh[['latitude', 'longitude']], factor)

d = d.groupby(['latitude', 'longitude']).mean().reset_index().dropna(axis=0)
d
wells = wells.groupby(['latitude', 'longitude']).size().reset_index(name='wells')
wells.shape
shortages = sh.groupby(['latitude', 'longitude']).size().reset_index(name='shortages')
shortages.shape


m = d.merge(wells, on=['latitude', 'longitude'], how='inner').merge(
    shortages, on=['latitude', 'longitude'], how='left')
m = m.fillna(0)

m['sh_frac'] = m.shortages / (m.wells + m.shortages)

m.head()

m.to_csv('./cleaned/m_agg.csv', index=False)
# m is the dataset of predictors and outocomes (aggregated by coordinates)


# %%
# now, still aggregated by coordinates, but with monthly data
st.head()
# merge coordinates onto monthly measurements
me_pad


me_c = me_pad.reset_index().merge(st, on='site_code', how='inner')
me_c = me_c.sort_values(['latitude', 'longitude', 'month'])
me_c[['latitude', 'longitude']] = round_to(me_c[['latitude', 'longitude']], factor)
me_c = me_c.groupby(['latitude', 'longitude', 'month']).d_gwe.mean().reset_index(name='meas')
me_c.shape
me_c = me_c.dropna(axis=0)
me_c.head()
me_c['m'] = me_c.month.dt.to_period('M')
me_c
# %%


sh['m'] = sh.date.dt.to_period('M')

sh_count = sh.groupby(['latitude', 'longitude', 'm']).size().reset_index(name='shortages')

m_time = sh_count.merge(me_c, on=['latitude', 'longitude', 'm'], how='right').drop(columns='month')
m_time.shape
m_time.shortages = m_time.shortages.fillna(0)


m_time = m_time.merge(wells, on=['latitude', 'longitude'], how='inner')
m_time['sh_frac'] = m_time.shortages / m_time.wells
m_time['meas_l1'] = m_time.groupby(['latitude', 'longitude']).meas.shift(1)
m_time['meas_l2'] = m_time.groupby(['latitude', 'longitude']).meas.shift(2)
m_time['sh01'] = (m_time.shortages > 0).astype(int)
m_time = m_time.dropna(axis=0)
m_time

m_time.to_csv('./cleaned/m_time.csv', index=False)
