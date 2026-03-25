#%%
import pandas as pd
import os
import streamlit as st

#%%
assets_path = 'assets'
@st.cache_data
def load_data():
    data={
        'angles':{},
        'moments':{},
        'powers':{},
        'grf': {}
    }
    for data_type in data.keys():
        for file in os.listdir(assets_path):
            if file.endswith('.csv') and file.startswith(f'{data_type}_'):
                shoe_name = file.replace(f'{data_type}_', '').replace('.csv', '')
                filepath= os.path.join(assets_path,file)
                try:
                    df = pd.read_csv(filepath, header=[0,1,4])
                    df = df.drop(columns=[col for col in df.columns if 'Unnamed' in str(col[0])])
                    df.columns = pd.MultiIndex.from_tuples(df.columns, names=['Stat', 'Metric', 'Axis'])
                    df.index=range(101)
                    data[data_type][shoe_name] = df
                except Exception as e:
                    st.write(f"Failed to load {file}: {e}")
    return data  

def get_series(data, data_type, shoe, joint, axis, stat='Mean'):
    df = data[data_type].get(shoe)
    if df is None:
        return None
    
    # Map data_type to the exact label used in each CSV
    label_map = {
        'angles':  'Angles',
        'moments': 'Moment',   # singular in moments CSV
        'powers':  'Power',
        'grf': 'GRF'     
    }
    metric_label = f'{joint} {label_map[data_type]}'
    
    try:
        return df[(stat, metric_label, axis)]
    except KeyError:
        return None
#%%

# %%
