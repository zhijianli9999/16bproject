# prediction model
# %%
import pandas as pd
import numpy as np
import pysal as ps
from pysal.lib.weights import KNN


# %%
# read dataset created by clean.py
m = pd.read_csv('./cleaned/m_agg.csv')

# %%
# prediction model (aggregated by time and coordinates)

kd = ps.lib.cg.KDTree(m[['latitude', 'longitude']])
wnn2 = ps.lib.weights.KNN(kd, 4)
# wnn2.neighbors
# %%
# no spatial lag

preds = ['wse_ch_av', 'd_gwe']
m

model1 = ps.model.spreg.OLS(m['sh_frac'].values[:, None],
                            m[preds].values, w=wnn2, spat_diag=True,
                            name_x=m[preds].columns.tolist())
print(model1.summary)


# %%
# adding spatial lag (4 nearest neighbors)
m2 = m.assign(w_wse=ps.lib.weights.lag_spatial(wnn2, m['wse_ch_av'].values),
              w_gwe=ps.lib.weights.lag_spatial(wnn2, m['d_gwe'].values))

preds = ['wse_ch_av', 'd_gwe', 'w_wse', 'w_gwe']
model2 = ps.model.spreg.OLS(m2['sh_frac'].values[:, None],
                            m2[preds].values, w=wnn2, spat_diag=True,
                            name_x=m2[preds].columns.tolist())
print(model2.summary)


# %%
# adding spatial lag (8 nearest neighbors)
kd = ps.lib.cg.KDTree(m[['latitude', 'longitude']])
wnn3 = ps.lib.weights.KNN(kd, 8)
wnn3.neighbors
m3 = m.assign(w_wse=ps.lib.weights.lag_spatial(wnn3, m['wse_ch_av'].values),
              w_gwe=ps.lib.weights.lag_spatial(wnn3, m['d_gwe'].values))
model3 = ps.model.spreg.OLS(m3['sh_frac'].values[:, None],
                            m3[preds].values, w=wnn3, spat_diag=True,
                            name_x=m2[preds].columns.tolist())
print(model3.summary)

m['m1preds'] = model1.predy
m['m2preds'] = model2.predy
m['m3preds'] = model3.predy
m.to_csv('./cleaned/m_preds.csv', index=False)


# %%
# still aggregated by coordinates, but with monthly data
m_time = pd.read_csv('./cleaned/m_time.csv')
m_time.columns
preds = ['meas', 'meas_l1', 'meas_l2']
modelt = ps.model.spreg.OLS(m_time['sh01'].values[:, None],
                            m_time[preds].values,
                            name_x=m_time[preds].columns.tolist())
print(modelt.summary)

m_time['preds'] = modelt.predy
mt_preds = m_time.groupby(['latitude', 'longitude']).mean().reset_index()
mt_preds.to_csv('./cleaned/mt_preds.csv', index=False)


# %%
# model without current measurement
preds = ['meas_l1', 'meas_l2']
modelt2 = ps.model.spreg.OLS(m_time['sh01'].values[:, None],
                             m_time[preds].values,
                             name_x=m_time[preds].columns.tolist())
print(modelt2.summary)
