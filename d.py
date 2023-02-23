import pandas as pd
import numpy as np
import sys,os
sys.path.append(os.path.expanduser("~")+"/ivpy/src")
from ivpy import *
from ivpy.cluster import cluster
import warnings
warnings.filterwarnings('ignore')

#------------------------------------------------------------------------------

df = pd.read_csv('/Users/damoncrockett/Desktop/ab/lola_and_genome_prebanquet.csv')
all_lola = len(df[df.crow==True])

rcols = ['t','gi','c','r']

#------------------------------------------------------------------------------

# This function gets the distance value between the cluster centroid and a single valid (fully non-null) genome row

def get_dist(target,df,i,rcols):
    return np.linalg.norm(target-np.array(df[rcols].loc[i]))

# This function gets all the centroid-genome distances

def get_dist_list(df,rcols,target):
    dists = pd.Series([get_dist(target,df,i,rcols) for i in df.index[df.grow==True]],index=df.index[df.grow==True])
    dists = dists.sort_values()

    return dists

def check_table_pair(i,j):
    u = set(i).union(set(j))
    if len(u) < len(i)+len(j):
        return True
    else:
        return False

def check_table(table):
    for member in table:
        others = [m for m in table if m!=member]
        tm = mm.tablemates.loc[member]
        if all([o in tm for o in others]):
            pass
        else:
            return False
                
    return True 

def is_tabling_allowable(df,clustercol):
    tablenums = df[clustercol].value_counts().index
    tablenums = [item for item in tablenums if item!=-1]
    for tablenum in tablenums:
        table = df.index[df[clustercol]==tablenum]
        if check_table(table):
            pass
        else:
            return False
    return True

def guestlist(mm,guestcol,clustercol,c):
    cidxs = mm.index[mm[clustercol]==c]
    glists = list(mm[guestcol].loc[cidxs])
    glist = [item for sublist in glists for item in sublist]
    gset = set(glist)
    collapse = len(glist) - len(gset)
    
    return gset,collapse

#------------------------------------------------------------------------------

ds = []
shares = []
collapse_pcts = []
catches = []

for d in [round(item,4) for item in np.linspace(0.015,0.1,100)]:
    glists = []
    for i in df.index[df.crow==True]:
        target = np.array(df[rcols].loc[i])
        distlist = get_dist_list(df,rcols,target)
        distlist = distlist[distlist < d]
        glists.append(distlist)

    membermap = list(df.index[df.crow==True])
    guestlists = [list(item.index) for item in glists]

    mm = pd.DataFrame({"guestlist":guestlists},index=membermap)

    mm['k'] = [len(l) for l in mm.guestlist]
    mm = mm[mm.k > 0]

    tablemates = []
    for i in mm.index:
        gli = mm.guestlist.loc[i]
        imates = []
        for j in mm.index:
            if i!=j:
                glj = mm.guestlist.loc[j]
                if check_table_pair(gli,glj):
                    imates.append(j)
        tablemates.append(imates)
    mm['tablemates'] = tablemates  

    mm['n'] = [len(item) for item in mm.tablemates]
    mm = mm[mm.n > 0]

    eps = 0.164
    df['cluster'] = cluster(df[rcols].loc[mm.index],method='dbscan',eps=eps,min_samples=2)
    while is_tabling_allowable(df,'cluster') == False:
        eps -= 0.0001
        df['cluster'] = cluster(df[rcols].loc[mm.index],method='dbscan',eps=eps,min_samples=2)

    mm['cluster'] = df.cluster # same indices!

    tablenums = mm.cluster.value_counts().index
    gsets_collapse = [guestlist(mm,'guestlist','cluster',t) for t in tablenums if t > -1]
    gsets = [item[0] for item in gsets_collapse]
    collapses = [item[1] for item in gsets_collapse]
    collapse = sum(collapses)
    totalguests = sum([len(item) for item in mm.guestlist])
    collapse_pct = collapse / totalguests
    allguests = sum([len(gset) for gset in gsets])
    unique_guests = len(set.union(*gsets))
    share_pct = (allguests - unique_guests) / allguests

    ds.append(d)
    shares.append(share_pct)
    collapse_pcts.append(collapse_pct)

    catch_pct = len(mm)/all_lola
    catches.append(catch_pct)

    print(d,share_pct,collapse_pct,catch_pct)

pd.DataFrame({"d":ds,"share":shares,"collapse":collapse_pcts,"catch":catches}).to_csv('d.csv',index=False)