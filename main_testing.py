import pandas as pd

phone_df = pd.read_csv("phone_data.csv", index_col = 0)

start_date = input("Enter start Date: ")
end_date = input("Enter end date: ") 

date_select = pd.DataFrame(phone_df.loc[start_date:end_date])
print(date_select)

user_selected_stat = input('Please choose a column from the above stats: ')
stat_series = pd.Series(date_select[user_selected_stat])

print()
print("You chose:", user_selected_stat, "which is shown below with the corresponding dates")

print(stat_series)


