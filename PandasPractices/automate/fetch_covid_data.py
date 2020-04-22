import time
import pandas as pd
import schedule

timestring = time.strftime("%Y%m%d-%H%M%S")

confirmed_covid_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
death_covid_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_covid_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"


def get_n_melt_data(data_url, case_type):
    df = pd.read_csv(data_url)
    melted_df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long']) 
    melted_df.rename(columns={"variable": "Date", "value":case_type}, inplace = True)
    return melted_df


def merge_data(confirmed_covid_df, recovered_covid_df, death_covid_df):
    new_df = confirmed_covid_df.join(recovered_covid_df["recovered"]).join(death_covid_df["death"])
    return new_df


def fetch_data():
    confirmed_covid_df = get_n_melt_data(confirmed_covid_cases_url, "confirmed")    
    recovered_covid_df = get_n_melt_data(recovered_covid_cases_url, "recovered")
    death_covid_df = get_n_melt_data(death_covid_cases_url, "death")

    print("Merging Data....")

    final_df = merge_data(confirmed_covid_df, recovered_covid_df, death_covid_df)

    print("Preview data...")
    print(final_df.tail(5))
    filename = "covid19_merged_dataset_updated_{}.csv".format(timestring)
    print("saving dataset as {}".format(filename))
    final_df.to_csv(filename)
    print("All DONE!!")


# Scheduler

schedule.every(10).seconds.do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)
