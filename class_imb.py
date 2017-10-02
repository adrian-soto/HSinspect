# Functions to deal with class imbalance

import pandas as pd
import numpy as np
import random

def downsample(df, key):
    '''
    Downsample imbalanced dataframe for a column with 
    binary (0,1) values by randomly discarding rows 
    of the majority class
    
    INPUT
      - df:  pandas.DataFrame
      - key: key of the column of interest
    OUTPUT
      - downsampled_df: 
    '''
    
    # Check that targets are only {0,1} -- ToDo
    
    # Grab row indices of two classes
    i0 = df.index[df[key]==0]
    i1 = df.index[df[key]==1]
    
    N0 = i0.size
    N1 = i1.size
    
    
    if (N0 < N1):
        downsampled_df = pd.concat((df.loc[i0], df.loc[random.sample(i1, N0)]), axis=0)
        
    elif(N1 < N0):
        downsampled_df = pd.concat((df.loc[random.sample(i0, N1)], df.loc[i1]), axis=0)
    
    return downsampled_df



def balance_data(x,t):
    # Balance data.
    #   x: np.array containing features
    #   t: np.array containing targets
    
    
    # If DataFrame or Series, convert to np.array
    if (isinstance(x, pd.DataFrame) or isinstance(x, pd.Series)):
        x = x.values
        
    if (isinstance(t, pd.DataFrame) or isinstance(t, pd.Series)):
        t = t.values
    
    
    # Check that dimensions agree
    if (np.shape(x)[0] != np.shape(t)[0]):
        print ("ERROR! Lengths of x and t do not agree. Exiting ... ")
        exit()
    
    # Find indices
    iHD=np.array(np.where(t == 0))
    iLD=np.array(np.where(t == +1))
    
    # Count HD and LD
    NHD=np.size(iHD)
    NLD=np.size(iLD)
    
    
    # Create balanced set
    if(NLD <= NHD):
        # Take all LD points and NLD random HD points
        Nhalf=NLD
        ibal=np.zeros(2*Nhalf, dtype=np.int)
        
        ibal[:Nhalf]=iLD[0,:]
        np.random.shuffle(iHD)
        
        ibal[Nhalf:]=iHD[0,:Nhalf]
        
    elif(NLD > NHD):
        # Take all HD points and NHD random LD points
        Nhalf=NHD
        ibal=np.zeros(2*Nhalf, dtype=np.int)
        
        ibal[:Nhalf]=iHD[0,:]
        np.random.shuffle(iLD)
        
        ibal[Nhalf:]=iLD[0,:Nhalf]
        
    
    # Shuffle points so that HD and LD are mixed
    np.random.shuffle(ibal)
    

    # Return shuffled balanced data 
    return x[ibal,:], t[ibal]   
 
    
    