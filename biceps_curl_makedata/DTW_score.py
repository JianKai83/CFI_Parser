import pandas as pd
from tslearn.metrics import dtw


def main():

    #載入資料集
    df_elbow_good = pd.read_csv('Biceps_Curl_elbow_good.csv')
    df_body_good = pd.read_csv('Biceps_Curl_body_good.csv')
    df_elbow_bad = pd.read_csv('Biceps_Curl_elbow_bad.csv')
    df_body_bad = pd.read_csv('Biceps_Curl_elbow_bad.csv')

    #選取模板，每個sample都跟他比對
    templat_elbow = [x for x in df_elbow_good.iloc[2] if pd.isnull(x) == False]
    templat_body = [x for x in df_body_good.iloc[2] if pd.isnull(x) == False]

    good_example = []
    for i in range(len(df_elbow_good)):
        newlist_elbow_good = [x for x in df_elbow_good.iloc[i] if pd.isnull(x) == False]
        newlist_body_good = [x for x in df_body_good.iloc[i] if pd.isnull(x) == False]
        elbow_dtw_score = dtw(newlist_elbow_good, templat_elbow)
        body_dtw_score = dtw(newlist_body_good, templat_body)
        good_example.append([elbow_dtw_score,body_dtw_score,'good'])

    # print(good_example)
    df_good_dtw = pd.DataFrame(good_example)
    df_good_dtw.to_csv('Biceps_Curl_good_dtw.csv', index=False)

    bad_example = []
    for i in range(len(df_elbow_bad)):
        newlist_elbow_bad = [x for x in df_elbow_bad.iloc[i] if pd.isnull(x) == False]
        newlist_body_bad = [x for x in df_body_bad.iloc[i] if pd.isnull(x) == False]
        elbow_dtw_score = dtw(newlist_elbow_bad, templat_elbow)
        body_dtw_score = dtw(newlist_body_bad, templat_body)
        bad_example.append([elbow_dtw_score,body_dtw_score,'bad'])

    # print(bad_example)
    df_bad_dtw = pd.DataFrame(bad_example)
    df_bad_dtw.to_csv('Biceps_Curl_bad_dtw.csv', index=False)


if __name__ == '__main__':
    main()