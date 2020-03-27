"""
Monitor the COVID-19 status across many locations in a single dashboard.

SPDX-License-Identifier: AGPL-3.0-or-later
"""
import math
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

KEYWORDS = [
    "Denver",
    "Massachusetts, Hampden",
    "Los Angeles",
    "country:Vietnam",
    "exact:Florida",
    "Washington, D.C.",
    "New York City",
    "Portland, OR",
    "country:Italy",
]
REFRESH_HOURS = 24  # Refresh the data once a day

# Setup the window
NUM_COLS = 3
NUM_ROWS = math.ceil(len(KEYWORDS) / NUM_COLS)

# Map each axis to a number
# Then the index of the keyword in KEYWORDS is the axis key
AXMAP = {}


def get_data():
    print("Downloading all COVID-19 data from covid19api.com")
    df = pd.read_json("https://api.covid19api.com/all")
    df = df.query("Country != ''")  # Clean it
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index("Date").sort_index()
    return df


def analyze_keyword(keyword, df, recent_idx):
    ax = AXMAP[KEYWORDS.index(keyword)]
    ax.clear()
    if keyword.startswith("country:"):
        kw = keyword.split(":")[1]
        kw_df = df[df.Country == kw]
        keyword = kw
    else:
        if keyword.startswith("exact:"):
            kw = keyword.split(":")[1]
            keyword = kw
            kw_df = df[df.Province == keyword]
        else:
            kw_df = df[df.Province.str.contains(keyword)]

    print(f"Found {len(kw_df)} entries for {keyword}")
    recent_data = kw_df[recent_idx:]
    print(recent_data.to_string())

    kw_df.groupby("Status").Cases.plot(legend=True, title=f"{keyword}", ax=ax)

    def annotate_status(kw_df, status, color, xytext, shrink=0.05):
        latest = kw_df[kw_df.Status == status].tail(1)
        x = latest.index.tolist()[0]
        y = latest.Cases.tolist()[0]
        ax.annotate(
            f"{latest.Cases.values[0]}",
            xy=(x, y),
            xycoords="data",
            xytext=xytext,
            textcoords="axes fraction",
            arrowprops=dict(facecolor=color, shrink=shrink),
            horizontalalignment="right",
            verticalalignment="top",
        )

    annotate_status(kw_df, "confirmed", "black", xytext=(0.8, 0.95))
    annotate_status(kw_df, "deaths", "red", xytext=(0.7, 0.7))
    annotate_status(kw_df, "recovered", "green", xytext=(0.6, 0.4), shrink=0.1)
    print()


def main():
    fig, axes = plt.subplots(NUM_ROWS, NUM_COLS, sharex=False, sharey=False)

    # Give each axis a number
    i = 0
    for row in axes:
        for col in row:
            AXMAP[i] = col
            i += 1

    plt.show(block=False)

    while True:
        recent_idx = pd.Timestamp(
            datetime.utcnow().date() - timedelta(days=2), tz="utc"
        )

        df = get_data()

        for keyword in KEYWORDS:
            analyze_keyword(keyword, df, recent_idx)

        fig.subplots_adjust(wspace=0.1, hspace=0.5)
        fig.canvas.draw()
        fig.canvas.flush_events()

        print(f"Sleeping for {REFRESH_HOURS} hour(s)")
        print(80 * "=")
        plt.pause(REFRESH_HOURS * 60 * 60)


if __name__ == "__main__":
    main()
