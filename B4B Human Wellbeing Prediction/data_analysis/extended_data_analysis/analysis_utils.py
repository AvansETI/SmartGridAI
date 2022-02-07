import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

def calculate_crosstab_and_chi(df,col1,col2, lambda_="log-likelihood", normalize=True, chi_p_array=None):
    crosstab = pd.crosstab(df[col1],df[col2], normalize=normalize)
    c, p, dof, expected = chi2_contingency(crosstab, lambda_=lambda_)
    column_identifier =f"{col1}->{col2}"
    if chi_p_array != None:
        chi_p_array[column_identifier] = p
    return {column_identifier: p}, crosstab

def analysis_chi_heatmap(df,cols, target, chi_p_array=None, cmap="YlGnBu", columns=2):
    fig = plt.figure(figsize=(30,30))
    rows = round(len(cols)/columns)
    axis_array = []

    for i in range(0,rows):
        for row in range(0,columns):
            axis_array.append(plt.subplot2grid((rows,columns), (i,row)))

    for index in range(len(cols)):
        res, crosstab = calculate_crosstab_and_chi(df,target,cols[index],chi_p_array=chi_p_array)
        sns.heatmap(crosstab, annot=True, cmap=cmap,ax=axis_array[index])
        
def analysis_scatter(df, cols, huetarget, target_column, colors=["#FF0000", "#7FFF00"], columns=2):
    fig = plt.figure(figsize=(25,35))
    sns.set_palette(sns.color_palette(colors))

    rows = round(len(cols)/columns)
    axis_array = []
    target_column = target_column

    for i in range(0,rows):
        for row in range(0,columns):
            axis_array.append(plt.subplot2grid((rows,columns), (i,row)))

    for index in range(len(cols)):
        sns.scatterplot(x=cols[index], y=target_column, data=df,ax=axis_array[index], hue=huetarget)