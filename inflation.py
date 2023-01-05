import pandas as pd, matplotlib.pyplot as plt, seaborn as sns, matplotlib.animation as ani

#Load CPI data from Excel Sheet (CPI is used to calculate inflation)
cpi = pd.read_excel(".../cpi_1938_2021.xlsx", header = 9, skiprows = (0, 8), dtype = {"Year": int, "Annual" : float}) #path to file hidden
#print(f"{cpi.info()}\n{cpi.head()}\n{cpi.tail()}")

#Create list of years (1938-2021)
years = cpi.Year.tolist()

#Dict of min wage changes, data from D.O.L.
min_wage_change = {'Year' : [1938, 1939, 1945, 1950, 1956, 1961, 1963, 1967, 1968, 1974, 1975, 1976, 1978, 1979, 1980, 1981, 1990, 1991, 1996, 1997, 2007, 2008, 2009],
            'Wage' : [0.25, 0.3, 0.4, 0.75, 1, 1.15, 1.25, 1.4, 1.6, 2, 2.1, 2.3, 2.65, 2.9, 3.1, 3.35, 3.8, 4.25, 4.75, 5.15, 5.85, 6.55, 7.25]}

#Create df similar to above dict, except this includes every year (1938-2022)
min_wage = pd.DataFrame({'Year' : [], 'Wage' : []})

i = 0
for y in years:
    if y in min_wage_change['Year']:
        i += 1
    #append min. wage and year to df
    min_wage.loc[len(min_wage.index)] = [y, min_wage_change['Wage'][i-1]]

adjusted_min_wage_df = pd.DataFrame({'Year': [], 'Wage' : []})

def calc_adjusted_min_wage(year):
    """Calculate minimum wage adjusted for inflation"""
    original_cpi = cpi.loc[cpi['Year'] == year]['Annual'].values[0]
    latest_cpi = cpi.loc[cpi['Year'] == 2021]['Annual'].values[0]
    original_min_wage = min_wage.loc[min_wage['Year'] == year]['Wage'].values[0]

    #CPI is the most commonly used metric for calculating inflation, which is done by using the below formula:
    adjusted_min_wage = (original_min_wage / original_cpi) * latest_cpi

    #Append data
    adjusted_min_wage_df.loc[len(adjusted_min_wage_df.index)] = [year, adjusted_min_wage]

#do this for every year
for i in range(len(years)):
    calc_adjusted_min_wage(years[i])

#now for the graph:
fig, ax = plt.subplots(figsize = (6.4, 4.8))
plt.subplots_adjust(bottom = 0.22, top = 0.9)
fig.set_dpi(150)

plt.grid(axis = 'y')
plt.suptitle("Minimum Wage over Time", fontweight = 'bold')
plt.title('Source: U.S. DOL and BLS', fontsize = 8)
plt.xlabel("Year", fontsize = '12')
plt.ylabel("Dollars", fontsize = '12')

#Making it animated:
def animation(i):
    sns.lineplot(x = min_wage.Year[:i], y = adjusted_min_wage_df.Wage[:i], color = 'red', linewidth = 2)
    sns.lineplot(x = min_wage.Year[:i], y = min_wage.Wage[:i], color = 'green')
    plt.legend(labels = ['Min. Wage Adjusted for Inflation', 'Federal Minimum Wage'], loc = 'center', bbox_to_anchor = (0.5, -0.2), ncol = 2, frameon = False)

animated = ani.FuncAnimation(fig, animation, repeat_delay = 4000)

output = r".../min_wage_ani.gif" #path hidden
writergif = ani.PillowWriter(fps = 7)
animated.save(output, writer = writergif)

