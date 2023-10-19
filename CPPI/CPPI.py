import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

def cppi(returns,riskfree_rate,multiplier,floor,start=100):
    
    floor_value=start*floor
    steps=len(returns.index)
    m=multiplier
    
    if type(returns)==pd.DataFrame:
        safe=pd.DataFrame().reindex_like(returns)
        safe[:]=riskfree_rate
        value_chart=pd.DataFrame().reindex_like(returns)
    
    if type(returns)==pd.Series:
        safe=pd.Series().reindex_like(returns)
        safe[:]=riskfree_rate
        value_chart=pd.Series().reindex_like(returns)
   
    value=start
    for n in range(steps):
        
        cushion=(value-floor_value)/value

        risky_weight=m*cushion
        risky_weight=np.minimum(1,risky_weight)
        #if risky_weight<0:    cannot be used as risky weight as a series sent to all different industries
        risky_weight=np.maximum(0,risky_weight)
        risky_alloc=value*risky_weight
        safe_alloc=value*(1-risky_weight)
        value=risky_alloc*np.exp(returns.iloc[n])+ safe_alloc*np.exp(safe.iloc[n])
        value_chart.iloc[n]=value
    
    value_chart.plot(legend=False)
    plt.xlim(left=0)
    plt.xlabel('time')
    plt.ylabel('wealth index')
    plt.axhline(y=floor_value) 
    plt.show()
    