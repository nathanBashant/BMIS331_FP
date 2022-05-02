import pandas as pd

phone_df = pd.read_csv("phone_data.csv", index_col = 0)
days_week_df = pd.read_csv("days_of_week.csv", index_col=0)

start_date = input("Enter start Date: ")
end_date = input("Enter end date: ") 

date_select = pd.DataFrame(phone_df.loc[start_date:end_date])
print(date_select)

user_selected_stat = input('Please choose a column from the above stats: ')
stat_series = pd.Series(date_select[user_selected_stat])

sum = stat_series.sum()
mean = stat_series.mean()
std = stat_series.std()
median = stat_series.median()
min = stat_series.min()
max = stat_series.max()

print()
print("You chose:", user_selected_stat, "which is shown below with the corresponding dates")

print(stat_series)

stats_dict = {'Stats':['Sum', 'Mean','Std Deviation','Median','Min','Max'], 'Number': [sum, mean, std, median, min, max]}
stats_dict_df = pd.DataFrame(stats_dict)

stats_dict_df.to_csv("output_phone_data.csv", header = False, index = False, float_format = "%.2f")

merged_df = phone_df.merge(days_week_df, on=["Date"], how = 'outer')
merged_df.to_csv("data_merged_df.csv")

grouped_by_day = merged_df.groupby("Day of Week", sort = False)


mean_user_ser = pd.Series(dtype=float)

for group_name, date_select in grouped_by_day:
    group_mean_pop = date_select[user_selected_stat].mean()
    mean_user_ser[group_name] = group_mean_pop
mean_user_ser.name = "Mean per day of the week:", user_selected_stat

print()
print("And here is the average number of", user_selected_stat, "for each day of the week")
print()
print(mean_user_ser)
