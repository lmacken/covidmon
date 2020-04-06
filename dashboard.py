"""
Monitor the COVID-19 status across many locations in a single dashboard.

Copyright (C) 2020  Luke Macken <luke.macken@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import math
import pandas as pd
import matplotlib.pyplot as plt

KEYWORDS = [
    ("province:Colorado", "city:Denver"),
    ("province:Massachusetts", "city:Hampden"),
    ("province:Massachusetts", "city:Suffolk"),
    ("province:California", "city:Los Angeles"),
    ("province:New York", "city:Wayne"),
    ("province:New York", "city:New York"),
    ("province:Virginia", "city:Arlington"),
    ("province:Florida", "city:Orange"),
    "country:Viet Nam",
    "country:Korea (South)",
    "country:Japan",
]
REFRESH_HOURS = 12  # Refresh the data twice a day

# Setup the window
NUM_COLS = 3
NUM_ROWS = math.ceil(len(KEYWORDS) / NUM_COLS)

# Map each axis to a number
# Then the index of the keyword in KEYWORDS is the axis key
AXMAP = {}


def get_data():
    """
    Country 	CountryCode 	Lat 	Lon 	Confirmed 	Deaths 	Recovered 	Active 	Date 	LocationID 	Province 	City 	CityCode
    Date
    2020-04-04 00:00:00+00:00 	Colombia 	CO 	4.57 	-74.30 	1406 	32 	85 	0 	2020-04-04 00:00:00+00:00 	89e1ca12-78be-407f-aa18-bfcd05f01a56 	NaN 	NaN 	NaN
    """
    print("Downloading all COVID-19 data from covid19api.com")
    df = pd.read_json("https://api.covid19api.com/all")
    df = df.query("Country != ''")  # Clean it
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index("Date").sort_index().fillna(0)
    return df


def analyze_keyword(keyword, df):
    ax = AXMAP[KEYWORDS.index(keyword)]
    ax.clear()

    if isinstance(keyword, tuple):
        keywords = list(keyword)
    else:
        keywords = [keyword]

    kw_df = None
    title = ''

    while len(keywords):
        kw = keywords.pop(0)
        qdf = df
        if kw_df is not None:
            qdf = kw_df
        if kw.startswith("country:"):
            kw = kw.split(":")[1]
            _df = qdf[qdf.Country == kw]
        elif kw.startswith("province:"):
            kw = kw.split(":")[1]
            _df = qdf[qdf.Province == kw]
        elif kw.startswith("city:"):
            kw = kw.split(":")[1]
            _df = qdf[qdf.City == kw]
        elif kw.startswith("citycode:"):
            kw = kw.split(":")[1]
            _df = qdf[qdf.CityCode == kw]
        else:
            _df = qdf[qdf.Province.str.contains(kw)]
        kw_df = _df
        title = f"{kw} {title}"
    kw_df = kw_df.sort_index()

    print(f"Found {len(kw_df)} entries for {keyword}")
    recent_data = kw_df.tail(6)
    print(recent_data.to_string())

    kw_df.Confirmed.plot(label='confirmed', legend=True, title=title, ax=ax)
    kw_df.Deaths.plot(label='deaths', legend=True, title=title, ax=ax)
    kw_df.Recovered.plot(label='recovered', legend=True, title=title, ax=ax)

    def annotate_status(df, status, color, xytext, shrink=0.05):
        latest = df.tail(1)
        x = latest.index.tolist()[0]
        y = latest[status].tolist()[0]
        ax.annotate(
            f"{latest[status].values[0]}",
            xy=(x, y),
            xycoords="data",
            xytext=xytext,
            textcoords="axes fraction",
            arrowprops=dict(facecolor=color, shrink=shrink),
            horizontalalignment="right",
            verticalalignment="top",
        )

    annotate_status(kw_df, "Confirmed", "black", xytext=(0.8, 0.95))
    annotate_status(kw_df, "Deaths", "red", xytext=(0.7, 0.7))
    annotate_status(kw_df, "Recovered", "green", xytext=(0.6, 0.4), shrink=0.1)
    print()


def main():
    fig, axes = plt.subplots(NUM_ROWS, NUM_COLS, sharex=False, sharey=False)

    # Give each axis a number
    i = 0
    for row in axes:
        try:
            for col in row:
                AXMAP[i] = col
                i += 1
        except TypeError:  # AxesSubplot is not iterable; single entry
            AXMAP[i] = row
            i += 1

    plt.show(block=False)

    while True:
        df = get_data()

        for keyword in KEYWORDS:
            analyze_keyword(keyword, df)

        fig.subplots_adjust(wspace=0.25, hspace=0.7)
        fig.canvas.draw()
        fig.canvas.flush_events()

        print(f"Sleeping for {REFRESH_HOURS} hour(s)")
        print(80 * "=")
        plt.pause(REFRESH_HOURS * 60 * 60)


if __name__ == "__main__":
    main()
