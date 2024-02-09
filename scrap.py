import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

stading_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
years = list(range(2024, 2018, -1))
all_matches = []

for year in years:
    data = requests.get(stading_url)
    time.sleep(3.1)
    soup = BeautifulSoup(data.text)
    season = soup.select("#meta")[0]
    season = season.find("h1")
    match = re.search(r"\b\d{4}-\d{4}\b", season.text)
    if match:
        season = match.group()
    data = requests.get(stading_url)
    time.sleep(3.1)  # 20 req per 1 min, 1/3 req per sec, 3 sec per 1 req, 3.1 for sure
    soup = BeautifulSoup(data.text)
    standing_table = soup.select("table.stats_table")[0]

    links = standing_table.find_all("a")
    links = [l.get("href") for l in links]
    links = [l for l in links if "/squads/" in l]

    previous_season = soup.select("a.prev")[0].get("href")
    stading_url = f"https://fbref.com{previous_season}"

    team_urls = [f"https://fbref.com{l}" for l in links]
    for team_url in team_urls:
        data = requests.get(team_url)
        time.sleep(3.1)
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", "")
        print(team_name)

        matches = pd.read_html(data.text, match="Scores & Fixtures")
        soup = BeautifulSoup(data.text)
        links_for_specific_stats = soup.find_all("a")
        links_for_specific_stats = [l.get("href") for l in links_for_specific_stats]

        links_for_shooting = [
            l for l in links_for_specific_stats if l and "all_comps/shooting/" in l
        ]
        req_for_shooting = requests.get(f"https://fbref.com{links_for_shooting[0]}")
        time.sleep(3.1)
        try:
            data_for_shooting = pd.read_html(req_for_shooting.text, match="Shooting")[0]
            data_for_shooting.columns = data_for_shooting.columns.droplevel()
            data_for_shooting.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_shooting.columns = [
                "shooting_" + col if col != "Date" else col for col in data_for_shooting.columns
            ]
            team_data = matches[0].merge(
                data_for_shooting,
                on="Date"
            )
        except ValueError:
            pass

        links_for_goalkeeping = [
            l for l in links_for_specific_stats if l and "all_comps/keeper/" in l
        ]
        req_for_goalkeeping = requests.get(
            f"https://fbref.com{links_for_goalkeeping[0]}"
        )
        time.sleep(3.1)
        try:
            data_for_goalkeeping = pd.read_html(
                req_for_goalkeeping.text, match="Goalkeeping "
            )[0]
            data_for_goalkeeping.columns = data_for_goalkeeping.columns.droplevel()
            data_for_goalkeeping_rem_col = data_for_goalkeeping.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_goalkeeping_rem_col.columns = [
                "keeper_" + col if col != "Date" else col
                for col in data_for_goalkeeping_rem_col.columns
            ]
            team_data = team_data.merge(
                data_for_goalkeeping_rem_col,
                on="Date",
            )
        except ValueError:
            pass

        links_for_passing = [
            l for l in links_for_specific_stats if l and "all_comps/passing/" in l
        ]
        req_for_passing = requests.get(f"https://fbref.com{links_for_passing[0]}")
        time.sleep(3.1)
        try:
            data_for_passing = pd.read_html(req_for_passing.text, match="Passing")[0]
            data_for_passing.columns = data_for_passing.columns.droplevel()
            data_for_passing = data_for_passing.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_passing.columns = [
                "passing_" + col if col != "Date" else col
                for col in data_for_passing.columns
            ]
            team_data = team_data.merge(
                data_for_passing,
                on="Date",
            )
        except ValueError:
            pass

        links_for_passing_types = [
            l for l in links_for_specific_stats if l and "all_comps/passing_types/" in l
        ]
        req_for_passing_types = requests.get(
            f"https://fbref.com{links_for_passing_types[0]}"
        )
        time.sleep(3.1)
        try:
            data_for_passing_types = pd.read_html(
                req_for_passing_types.text, match="Pass Types"
            )[0]
            data_for_passing_types.columns = data_for_passing_types.columns.droplevel()
            data_for_passing_types = data_for_passing_types.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_passing_types.columns = [
                "passing_types_" + col if col != "Date" else col
                for col in data_for_passing_types.columns
            ]
            team_data = team_data.merge(
                data_for_passing_types,
                on="Date",
            )
        except ValueError:
            pass

        links_for_gca = [
            l for l in links_for_specific_stats if l and "all_comps/gca/" in l
        ]
        req_for_gca = requests.get(f"https://fbref.com{links_for_gca[0]}")
        time.sleep(3.1)
        try:
            data_for_gca = pd.read_html(
                req_for_gca.text, match="Goal and Shot Creation"
            )[0]
            data_for_gca.columns = data_for_gca.columns.droplevel()
            data_for_gca = data_for_gca.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_gca.columns = [
                "gca_" + col if col != "Date" else col for col in data_for_gca.columns
            ]
            team_data = team_data.merge(
                data_for_gca,
                on="Date",
            )
        except ValueError:
            pass

        links_for_defense = [
            l for l in links_for_specific_stats if l and "all_comps/defense/" in l
        ]
        req_for_defense = requests.get(f"https://fbref.com{links_for_defense[0]}")
        time.sleep(3.1)
        try:
            data_for_defense = pd.read_html(
                req_for_defense.text, match="Defensive Actions"
            )[0]
            data_for_defense.columns = data_for_defense.columns.droplevel()
            data_for_defense = data_for_defense.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_defense.columns = [
                "defense_" + col if col != "Date" else col
                for col in data_for_defense.columns
            ]
            team_data = team_data.merge(
                data_for_defense,
                on="Date",
            )
        except ValueError:
            pass

        links_for_possession = [
            l for l in links_for_specific_stats if l and "all_comps/possession/" in l
        ]
        req_for_possession = requests.get(f"https://fbref.com{links_for_possession[0]}")
        time.sleep(3.1)
        try:
            data_for_possession = pd.read_html(
                req_for_possession.text, match="Possession "
            )[0]
            data_for_possession.columns = data_for_possession.columns.droplevel()
            data_for_possession = data_for_possession.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_possession.columns = [
                "possession_" + col if col != "Date" else col
                for col in data_for_possession.columns
            ]
            team_data = team_data.merge(
                data_for_possession,
                on="Date",
            )
        except ValueError:
            pass

        links_for_misc = [
            l for l in links_for_specific_stats if l and "all_comps/misc/" in l
        ]
        req_for_misc = requests.get(f"https://fbref.com{links_for_misc[0]}")
        time.sleep(3.1)
        try:
            data_for_misc = pd.read_html(
                req_for_misc.text, match="Miscellaneous Stats"
            )[0]
            data_for_misc.columns = data_for_misc.columns.droplevel()
            data_for_misc = data_for_misc.drop(
                columns=[
                    "Time",
                    "Comp",
                    "Round",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Match Report",
                ]
            )
            data_for_misc.columns = [
                "misc_" + col if col != "Date" else col for col in data_for_misc.columns
            ]
            team_data = team_data.merge(
                data_for_misc,
                on="Date",
            )
        except ValueError:
            pass

        team_data = team_data[team_data["Comp"] == "Premier League"]

        team_data["Season"] = season
        team_data["Team"] = team_name
        all_matches.append(team_data)

    matches_df = pd.concat(all_matches)
    matches_df.columns = [c.lower() for c in matches_df.columns]
    matches_df.to_csv("matches.csv")
