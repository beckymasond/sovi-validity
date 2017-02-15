import pandas as pd
from scipy.stats import spearmanr 

######################
##Compute spearman correlation
######################

local_path = '/Users/becky/'
path = local_path + 'documents/sovi-validity/data/output/'

#state geofips codes
state_id = ['g51', 'g48', 'g36', 'g06', 'g13', 'g16', 'g17', 'g29', 'g46', 'g23g33g25']
rank = pd.read_csv(path + 'County_in_State_Rank.csv')
state = pd.read_csv(path + 'State_Sovi_Score.csv')

# create column names for dataframe based on state ids
# columns for r values
corr = [s + '_r' for s in state_id]
# columns for p values
pval = [x + '_p' for x in state_id]
cols = corr + pval
# create dataframe to store results
state_results = pd.DataFrame(index = ['Region', 'US'], columns=cols)

for ID in state_id:
    print ID
    st = state[state['state_id'] == ID]
    select = rank[rank['Geo_FIPS'].isin(st['Geo_FIPS'])]
    st_reg = spearmanr(select['state_sovi_rank'], select['fema_region_sovi_rank'])
    st_US = spearmanr(select['state_sovi_rank'], select['us_sovi_rank'])
    state_results[ID+'_r']['Region'] = st_reg[0]
    state_results[ID+'_p']['Region'] = st_reg[1]
    state_results[ID+'_r']['US'] = st_US[0]
    state_results[ID+'_p']['US'] = st_US[1]
    '''
    print "State: Region"
    print spearmanr(select['state_sovi_rank'], select['fema_region_sovi_rank'])
    print "State: US"
    print spearmanr(select['state_sovi_rank'], select['us_sovi_rank'])
    print "\n"
    '''
state_results.to_csv(path + 'spearman_state.csv')

US_Sovi_Score = pd.read_csv(path + 'US_Sovi_Score.csv', index_col='Geo_FIPS')
FEMA_Region_Sovi_Score = pd.read_csv(path + 'FEMA_Region_Sovi_Score.csv', index_col='Geo_FIPS')
county_in_region_rank = pd.DataFrame(index=FEMA_Region_Sovi_Score.index,
                                    columns=['fema_region_sovi_rank', 'us_sovi_rank'])

regionList = ['FEMA_1','FEMA_2','FEMA_3','FEMA_4','FEMA_5','FEMA_6','FEMA_7','FEMA_8','FEMA_9','FEMA_10']

for region in regionList:
    x = FEMA_Region_Sovi_Score[FEMA_Region_Sovi_Score['fema_region'] == region]
    # get all counties in region and rank for us
    rg_cty_scores = US_Sovi_Score[US_Sovi_Score.index.isin(x.index)]
    county_in_region_rank.loc[rg_cty_scores.index, 'us_sovi_rank'] = abs(rg_cty_scores.sovi).rank(method='average', ascending=False)
    # get all counties in state and rank for fema region
    county_in_region_rank.loc[rg_cty_scores.index, 'fema_region_sovi_rank'] = abs(x.sovi).rank(method='average', ascending=False)

county_in_region_rank.to_csv(path + 'County_in_Region_Rank.csv')

corrReg = [s + '_r' for s in regionList]
# columns for p values
pvalReg = [x + '_p' for x in regionList]
colsReg = corrReg + pvalReg
# create dataframe to store results
region_results = pd.DataFrame(index = ['US'], columns=colsReg)

for ID in regionList:
    print ID
    rg = FEMA_Region_Sovi_Score[FEMA_Region_Sovi_Score['fema_region'] == ID]
    rank = pd.read_csv(path + 'County_in_Region_Rank.csv')
    select = rank[rank['Geo_FIPS'].isin(rg.index)]
    reg_us = spearmanr(select['fema_region_sovi_rank'], select['us_sovi_rank'])
    region_results[ID+'_r'] = reg_us[0]
    region_results[ID+'_p'] = reg_us[1]
region_results.to_csv(path + 'spearman_region.csv')
    
    