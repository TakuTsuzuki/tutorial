#!/usr/bin/python
#-*- coding:utf-8 -*-

import numpy as np
import pandas as pd
#from StringIO import StringIO
from io import StringIO
from RPE_data import FGRi_conc_txt,init_design_txt


X_names = [
    "mode",
    "trypsin_time",
    "FGRi_conc",
    "precon_days",
    "suspend_speed",
    "KSR_days",
    "3factor_days"
]
X_bounds = [
    (0., 1.),
    (0., 30.),
    (0., 510.), # drop 0, considering log-transform
    (1., 6.),
    (10., 100.),
    (1., 19.),
    (3., 19.)
]

def get_space(normalize=False, logscale=[]):
    space= {
        "mode": np.array([0,1], dtype=np.float),
        "trypsin_time": np.linspace(0, 30, 100),
        "FGRi_conc": np.array([float(c) for c in FGRi_conc_txt.split("\n")], dtype=np.float),
        #"FGRi_conc": (1.,510.),
        "precon_days": np.arange(1,6+1, dtype=np.float),
        "suspend_speed": np.arange(10, 100+1, dtype=np.float),
        "KSR_days": np.arange(1,19+1, dtype=np.float),
        "3factor_days": np.arange(3, 19+1, dtype=np.float)
    }
    
    if normalize:
        # normalize to [0,10]
        for i,k in enumerate(X_names):
            d = X_bounds[i][1] - X_bounds[i][0]
            if d > 0:
                space[k] = (space[k] - X_bounds[i][0]) / d
    
    return space

def get_domain(normalize=False, logscale=[]):
    space = get_space(normalize, logscale)
    
    return [
        {"name":"mode", "type":"categorical", "domain":space["mode"]},
        {"name":"trypsin_time", "type":"discrete", "domain":space["trypsin_time"]},
        {"name":"FGRi_conc", "type":"discrete", "domain":space["FGRi_conc"]},
        #{"name":"FGRi_conc", "type":"continuous", "domain":space["FGRi_conc"]},
        {"name":"precon_days", "type":"discrete", "domain":space["precon_days"]},
        {"name":"suspend_speed", "type":"discrete", "domain":space["suspend_speed"]},
        {"name":"KSR_days", "type":"discrete", "domain":space["KSR_days"]},
        {"name":"3factor_days", "type":"discrete", "domain":space["3factor_days"]}
    ]



def get_batch_context(normalize=False):
    # fixed parameters
    batch_context = []
    for i_plate in range(8):
        for i_well in range(6):
            batch_context.append({"trypsin_time": 8. + 3*i_well})
            if normalize:
                batch_context[-1]["trypsin_time"] /= X_bounds[1][1]
            #batch_context.append({"well_no": 6-i_well})
            #if normalize:
            #    batch_context[-1]["well_no"] -= 1.
            #    batch_context[-1]["well_no"] /= 5.

            #if i_plate <= 3: #1~4 : single
            #    batch_context[-1]["mode"] = 0
            #else: # 5~8 : double
            #    batch_context[-1]["mode"] = 1
    
    return batch_context
        
def get_init_design(normalize=False, logscale=[]):
    init_design_df = pd.read_csv(StringIO(init_design_txt), sep="\t")
    
    init_design_arr = np.array([
        init_design_df["細胞剥離方法"].as_matrix(),
        init_design_df["trypsin_time"].as_matrix(),
        init_design_df["FGRi濃度"].as_matrix(),
        init_design_df["preconditioning_period"].as_matrix(),
        init_design_df["suspend速度"].as_matrix(),
        init_design_df["KSR期間"].as_matrix(),
        init_design_df["3因子期間"].as_matrix()
    ], dtype=np.float).T

    for k in logscale:
        i = X_names.index(k)
        init_design_arr[:,i] = np.log10(init_design_arr[:,i])
    init_design_arr[np.isinf(init_design_arr)] = 0 # replace log(0)=-inf to log(1)=0

    if normalize:
        # normalize to [0,1]
        for i,k in enumerate(X_names):
            d = X_bounds[i][1] - X_bounds[i][0]
            if d > 0:
                init_design_arr[:,i] = (init_design_arr[:,i] - X_bounds[i][0]) / d
    
    return init_design_arr

def rescale(X):
    one = np.ones(X.shape)
    init = np.ones(X.shape)
    for i,k in enumerate(X_names):
        d = X_bounds[i][1] - X_bounds[i][0]
        #print(d)
        one[:,i] = d
        init[:,i] = X_bounds[i][0]
    rescaledX = np.round(np.array(one*X + init),0)
    return rescaledX

def RPE_true(x, minimize=True, normalize=False, logscale=[]):
    x = np.array(x, dtype=np.float)
    if len(x.shape) == 1:
        x = x.reshape(1,7)
        
    if normalize: # denormalize
        for i,k in enumerate(X_names):
            d = X_bounds[i][1] - X_bounds[i][0]
            if d > 0:
                x[:,i] = x[:,i] * d + X_bounds[i][0]

    for k in logscale:
        i = X_names.index(k)
        x[:,i] = np.power(10, x[:,i])
    
    mode = x[:,0]
    trypsine = x[:,1]
    FGRi_conc = x[:,2]
    precon_days = x[:,3]
    suspend_speed = x[:,4]
    KSR_days = x[:,5]
    factor3_days = x[:,6]
    
    y = 1
    y *= np.exp(-1*((trypsine-15)**2)/50)
    #y *= 1+ 2 / (1 + ((well_no-3.5)/1.5)**6)
    if mode == 0: #single
        y *= 1.
    elif mode == 1: #double
        y *= 1.2
        
    y *=  1 / (1 + np.exp(-(precon_days-3.99)*2)) + 0.01
    
    y *= 1 / (1 + ((FGRi_conc-250)/100)**4)

    y *= np.exp(-(np.log10(suspend_speed)-1)**2 / 0.4)
    
    if KSR_days < 8:
        y *= KSR_days/16+0.5
    else:
        y *= 1.

    y *= 1.5 / (1 + np.exp(-(factor3_days-7)*0.9))
    
    if y.shape[0] == 1:
        y = y[0]
    
    if minimize:
        return -y*1.1
    else:
        return y*1.1
    
def RPE_multiplicative_noisy(x, SN=9., **kwargs):
    return RPE_true(x, **kwargs) * np.random.lognormal(mean=0, sigma=1/SN)

