import pandas as pd, matplotlib.pyplot as plt, seaborn as sns, matplotlib.animation as ani

#Load CPI data from Excel Sheet
cpi = pd.read_excel("C:/Users/noahs/Desktop/Python Stuff/Practice Exercises/cpi_1938_2021.xlsx", header = 9, skiprows = (0, 8), dtype = {"Year": int, "Annual" : float})
#print(f"{cpi.info()}\n{cpi.head()}\n{cpi.tail()}")

#Create list of years (1938-2021)
years = cpi.Year.tolist()

#Dict of min wage changes
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

    adjusted_min_wage = (original_min_wage / original_cpi) * latest_cpi

    #Append adjusted min wage to appropriate df
    adjusted_min_wage_df.loc[len(adjusted_min_wage_df.index)] = [year, adjusted_min_wage]

#do this for every year
for i in range(len(years)):
    calc_adjusted_min_wage(years[i])


def inflation_calculator(year, amount, year2):
    """Uses CPI amounts to calculate equivalent buying power"""

    #gather cpi amounts
    initial_cpi = cpi.loc[cpi['Year'] == year]['Annual'].values[0]
    second_cpi = cpi.loc[cpi['Year'] == year2]['Annual'].values[0]

    #inflation calculation:
    buying_power = round((amount / initial_cpi) * second_cpi, 2)

    print(f"\n${amount} in {year} has the same buying power as ${buying_power} in {year2}\n")


def graph():
    """Creates graph of minimum wage over time"""
    fig, ax = plt.subplots(figsize = (6.4, 4.6))
    plt.subplots_adjust(bottom = 0.22, top = 0.9)
    fig.set_dpi(150)

    def animation(i):
        sns.lineplot(x = min_wage.Year[:i], y = adjusted_min_wage_df.Wage[:i], color = 'red', linewidth = 2)
        sns.lineplot(x = min_wage.Year[:i], y = min_wage.Wage[:i], color = 'green')
        plt.legend(labels = ['Min. Wage Adjusted for Inflation', 'Federal Minimum Wage'], loc = 'center', bbox_to_anchor = (0.5, -0.2), ncol = 2, frameon = False, fontsize = '10')

    animated = ani.FuncAnimation(fig, animation, interval = 100, repeat_delay = 4000)

    plt.grid(axis = 'y')
    plt.suptitle("Minimum Wage over Time", fontweight = 'bold')
    plt.title('Source: U.S. DOL and BLS', fontsize = 8)
    plt.xlabel("Year", fontsize = '12')
    plt.ylabel("Dollars", fontsize = '12')

    #animation needs to be returned so it exists outside of scope
    return animated

#Menu
choice = 0
while (choice != '4'):
    print("\nPlease select one of the following options: ")
    print("1. Inflation Calculator\n2. Show Inflation over Time graph\n3. Save Inflation over Time graph\n4. Exit")
    choice = input()

    if (choice == '1'):
        #Inflation calculator option
        #print()
        user_year = input("Please enter a year from 1938-2021 (year of original dollar amount): ")
        user_amount = input("Please enter a dollar amount (enter as number, will be rounded to nearest cent): ")
        user_year2 = input("Please enter a second year from 1938-2021 (year you would like to compare to): ")
        try:
            user_year = int(user_year)
            if (user_year < 1938 or user_year > 2021):
                raise Exception("Invalid Year")
            user_amount = round(float(user_amount), 2)
            user_year2 = int(user_year2)
            if (user_year2 < 1938 or user_year > 2021):
                raise Exception("Invalid Year")

            inflation_calculator(user_year, user_amount, user_year2)

            cont = input("Continue? (y/n)\n")
            if (cont == 'y'):
                continue
            else:
                break

        except:
            print(f"\nInvalid Input\n")

    if (choice == '2'):
        #Displaying Graph
        animated = graph()
        plt.show()
    
    if (choice == '3'):
        #Saving graph
        animated = graph()
        output_name = input("Please enter a name for the output file (do not include .gif): ")
        output = f"C:/Users/noahs/Desktop/Python Stuff/Practice Exercises/{output_name}.gif"
        writer = ani.PillowWriter(fps = 7)
        try:
            animated.save(output, writer = writer)
            print('Saved Succesfully')
        except:
            print('Something went wrong, please try again')

        cont = input("Continue? (y/n)\n")
        if (cont == 'y'):
            continue
        else:
            break


print("Exiting program succesfully")