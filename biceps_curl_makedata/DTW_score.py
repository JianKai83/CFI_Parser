import pandas as pd
from tslearn.metrics import dtw


def main():

    df_good = pd.read_csv('Biceps_Curl_good.csv')
    df_bad = pd.read_csv('Biceps_Curl_bad.csv')

    templat = [x for x in df_good.iloc[2] if pd.isnull(x) == False]

    good_example = []
    for i in range(len(df_good)):
        newlist_good = [x for x in df_good.iloc[i] if pd.isnull(x) == False]
        dtw_score = dtw(newlist_good, templat)
        good_example.append([dtw_score,'good'])

    # print(good_example)
    df_good_dtw = pd.DataFrame(good_example)
    df_good_dtw.to_csv('Biceps_Curl_good_dtw.csv', index=False)

    bad_example = []
    for i in range(len(df_bad)):
        newlist_bad = [x for x in df_bad.iloc[i] if pd.isnull(x) == False]
        dtw_score = dtw(newlist_bad, templat)
        bad_example.append([dtw_score,'bad'])

    # print(bad_example)
    df_bad_dtw = pd.DataFrame(bad_example)
    df_bad_dtw.to_csv('Biceps_Curl_bad_dtw.csv', index=False)


if __name__ == '__main__':
    main()