"""
game.py

This module defines the Game class, which is used to parse and represent a game from the API response.
The Game class includes attributes for game details such as teams, date, and odds, and provides methods
to access and manipulate this data.

Classes:
    Game: A class to parse and represent a game from the API response.

Dependencies:
    - pandas: For data manipulation and analysis.
    - numpy: For numerical operations.
    - datetime: For handling date and time operations.

Usage:
    Create an instance of the Game class with a game dictionary from the API response to access game details.
"""

import pandas as pd
import numpy as np
import datetime as dt

pd.options.mode.chained_assignment = None  # default='warn'


class Game:
    """
    Parses a game from the API response.

    Attributes:
        game_dict (dict): The dictionary containing game data from the API.
        bookmakers (list): A list of bookmakers for the game.
        raw_odds (pd.DataFrame): A DataFrame containing raw odds data.
        adjusted_odds (pd.DataFrame): A DataFrame containing adjusted odds data.
        aggregated_odds (dict): A dictionary for aggregated odds (currently not implemented).
        home_team (str): The home team for the game.
        away_team (str): The away team for the game.
        date (datetime.date): The date of the game.
        game_date (datetime): The datetime object representing the game date.
    """

    def __init__(self, game_dict: dict):
        """
        Initializes the Game object with the provided game dictionary.

        Args:
            game_dict (dict): The dictionary containing game data from the API.
        """
        self.game_dict = game_dict
        self.bookmakers = []
        self.raw_odds = pd.DataFrame()
        self.adjusted_odds = pd.DataFrame()
        self.aggregated_odds = {}  # TODO
        self.home_team = ""
        self.away_team = ""
        self.date = dt.date
        self.game_date = None

    def __str__(self):
        """
        Returns a string representation of the Game object.

        Returns:
            str: A string representing the Game object.
        """
        return f"Game object: {self.home_team} v {self.away_team} on {self.game_date}"

    @property
    def home_team(self):
        """
        Gets the home team for the game.

        Returns:
            str: The home team.
        """
        if not self._home_team:
            self._home_team = self.game_dict["home_team"]
        return self._home_team

    @home_team.setter
    def home_team(self, val):
        """
        Sets the home team for the game.

        Args:
            val (str): The home team.
        """
        self._home_team = val

    @property
    def away_team(self):
        """
        Gets the away team for the game.

        Returns:
            str: The away team.
        """
        if not self._away_team:
            self._away_team = self.game_dict["away_team"]
        return self._away_team

    @away_team.setter
    def away_team(self, val):
        """
        Sets the away team for the game.

        Args:
            val (str): The away team.
        """
        self._away_team = val

    @property
    def bookmakers(self):
        """
        Gets the list of bookmakers for the game.

        Returns:
            list: The list of bookmakers.
        """
        if self._bookmakers == []:
            self._bookmakers = self.game_dict["bookmakers"]
        return self._bookmakers

    @bookmakers.setter
    def bookmakers(self, val):
        """
        Sets the list of bookmakers for the game.

        Args:
            val (list): The list of bookmakers.
        """
        self._bookmakers = val

    @property
    def game_date(self):
        """
        Gets the game date.

        Returns:
            datetime: The game date.
        """
        if self._game_date is None:
            self._game_date = dt.datetime.strptime(
                self.game_dict["commence_time"], "%Y-%m-%dT%H:%M:%SZ"
            ).date()
        return self._game_date

    @game_date.setter
    def game_date(self, val):
        """
        Sets the game date.

        Args:
            val (datetime): The game date.
        """
        self._game_date = val

    @property
    def raw_odds(self):
        """
        Retrieves the raw odds data for the game.

        If the raw odds data is empty, it formats the data for each bookmaker
        and creates a DataFrame from the formatted data.

        Returns:
            pandas.DataFrame: The raw odds data for the game.
        """
        if self._raw_odds.empty:
            formatted_bookies = [
                self._format_one_bookies_data(bookie, self.home_team, self.away_team)
                for bookie in self.bookmakers
            ]
            self._raw_odds = pd.DataFrame.from_dict(formatted_bookies)
        return self._raw_odds

    @raw_odds.setter
    def raw_odds(self, val):
        """
        Sets the raw odds data for the game.

        Args:
            val (pandas.DataFrame): The raw odds data.
        """
        self._raw_odds = val

    @property
    def adjusted_odds(self):
        """
        Retrieves the adjusted odds data for the game.

        If the adjusted odds data is empty, it adjusts the raw odds data for margin
        and creates a DataFrame from the adjusted data.

        Returns:
            pandas.DataFrame: The adjusted odds data for the game.
        """
        if self._adjusted_odds.empty:
            self._adjusted_odds = self.raw_odds.apply(
                lambda row: self._adjust_raw_game_odds_for_margin(row), axis=1
            )
        return self._adjusted_odds

    @adjusted_odds.setter
    def adjusted_odds(self, val):
        """
        Sets the adjusted odds data for the game.

        Args:
            val (pandas.DataFrame): The adjusted odds data.
        """
        self._adjusted_odds = val

    @staticmethod
    def _get_odds_for_one_bookie(odds_list, home_team, away_team):
        """
        Retrieves the odds for a single bookmaker.

        Args:
            odds_list (list): The list of odds for the bookmaker.
            home_team (str): The home team.
            away_team (str): The away team.

        Returns:
            dict: The odds for the bookmaker.
        """
        home_odds = [1 / d["price"] for d in odds_list if d["name"] == home_team][0]
        away_odds = [1 / d["price"] for d in odds_list if d["name"] == away_team][0]
        draw_odds = [1 / d["price"] for d in odds_list if d["name"] == "Draw"][0]
        return {"home_odds": home_odds, "away_odds": away_odds, "draw_odds": draw_odds}

    def _format_one_bookies_data(self, bookie, home_team, away_team):
        """
        Formats the data for a single bookmaker.

        Args:
            bookie (dict): The bookmaker data.
            home_team (str): The home team.
            away_team (str): The away team.

        Returns:
            dict: The formatted data for the bookmaker.
        """
        name = bookie["key"]
        update = bookie["last_update"]
        odds_list = bookie["markets"][0]["outcomes"]
        odds_dict = self._get_odds_for_one_bookie(odds_list, home_team, away_team)

        out = {
            "home_team": home_team,
            "away_team": away_team,
            "bookmaker": name,
            "updated_at": update,
        }
        out.update(odds_dict)
        return out

    @staticmethod
    def _adjust_raw_game_odds_for_margin(raw_odds: pd.Series) -> pd.Series:
        """
        Adjusts the raw game odds for margin.

        Args:
            raw_odds (pandas.Series): The raw game odds.

        Returns:
            pandas.Series: The adjusted game odds.
        """
        total_odds = (
            raw_odds["home_odds"] + raw_odds["away_odds"] + raw_odds["draw_odds"]
        )

        raw_odds["home_odds"] = raw_odds["home_odds"] / total_odds
        raw_odds["away_odds"] = raw_odds["away_odds"] / total_odds
        raw_odds["draw_odds"] = raw_odds["draw_odds"] / total_odds
        return raw_odds

    @property
    def aggregated_odds(self):
        """
        Retrieves the aggregated odds for the game.

        If the aggregated odds data is empty, it calculates the mean of adjusted odds
        for home, away, and draw, and returns a dictionary with the aggregated odds.

        Returns:
            dict: The aggregated odds for the game.
        """
        if self._aggregated_odds == {}:
            home_odds = np.mean(self.adjusted_odds["home_odds"])
            away_odds = np.mean(self.adjusted_odds["away_odds"])
            draw_odds = np.mean(self.adjusted_odds["draw_odds"])
            self._aggregated_odds = {
                "home_odds": home_odds,
                "away_odds": away_odds,
                "draw_odds": draw_odds,
            }
        return self._aggregated_odds

    @aggregated_odds.setter
    def aggregated_odds(self, val):
        """
        Sets the aggregated odds for the game.

        Args:
            val (dict): The aggregated odds.
        """
        self._aggregated_odds = val

    def to_dict(self):
        """
        Converts the Game object to a dictionary.

        Returns:
            dict: The Game object as a dictionary.
        """
        dict_ = {"home_team": self.home_team, "away_team": self.away_team}
        dict_.update(self.aggregated_odds)
        return dict_
