import pytest
from fpl.scraper import FixtureScraper, PlayerScraper, GenInfoScraper
from requests.exceptions import ConnectionError


@pytest.fixture(scope="session")
def gis():
    return GenInfoScraper()


@pytest.fixture(scope="session")
def gis_response(gis):
    return gis.get_response(gis.url)


@pytest.fixture(scope="session")
def fs():
    return FixtureScraper()


@pytest.fixture(scope="session")
def fs_response(fs):
    return fs.get_response(fs.url)


@pytest.fixture(scope="session")
def ps():
    return PlayerScraper(id=1)


## GENERAL INFO SCRAPER
def test_get_response_succeeds(gis):
    assert type(gis.get_response(gis.url)) is dict


def test_get_response_fails(gis):
    with pytest.raises((AssertionError, ConnectionError)):
        gis.get_response("https://www.invalid_url1231243132asdas.com")


def test_get_response_invalid_endpoint(gis):
    with pytest.raises((AssertionError)):
        gis.get_response(gis.url + "/invalid_url")


def test_get_team_map(gis, gis_response):
    team_map = gis.get_team_map(gis_response)
    assert list(team_map.keys()) == list(range(1, 21))
    assert team_map[1]["name"] == "Arsenal"


def test_get_gw_deadlines(gis, gis_response):
    # TODO: Will fail for the next season
    gw_deadlines = gis.get_gw_deadlines(gis_response)
    assert list(gw_deadlines.keys()) == list(range(1, 39))
    assert gw_deadlines[1] == "2024-08-16T17:30:00Z"


def test_get_element_name_map(gis, gis_response):
    element_name_map = gis.get_element_name_map(gis_response)
    # print(element_name_map)
    assert element_name_map[1]["first_name"] == "Fábio"


def test_general_scrape(gis):
    data = gis.scrape()
    assert isinstance(data, dict)
    assert "team_map" in data.keys()
    assert "gw_deadlines" in data.keys()
    assert "element_map" in data.keys()


def test_parse_fixtures(fs, fs_response):
    fixtures = fs.parse_fixtures(fs_response)
    assert isinstance(fixtures, list)
    assert len(fixtures) > 0
    assert isinstance(fixtures[0], dict)
    assert "event" in fixtures[0].keys()
    assert "team_h" in fixtures[0].keys()
    assert "team_a" in fixtures[0].keys()


def test_fixture_scrape(fs):
    data = fs.scrape()
    # assert isinstance(data[0], dict)
    assert "fixtures" in data.keys()
    assert len(data["fixtures"]) == 380


def test_get_fixture_response_succeeds(fs):
    assert type(fs.get_response(fs.url)) is list


def test_get_fixture_response_fails(fs):
    with pytest.raises((AssertionError, ConnectionError)):
        fs.get_response("https://www.invalid_url1231243132asdas.com")


def test_get_fixture_response_invalid_endpoint(fs):
    with pytest.raises((AssertionError)):
        fs.get_response(fs.url + "/invalid_url")


## PLAYER SCRAPER
def test_get_player_response_succeeds(ps):
    assert type(ps.get_response(ps.url)) is dict


def test_get_player_response_fails(ps):
    with pytest.raises((AssertionError, ConnectionError)):
        ps.get_response("https://www.invalid_url1231243132asdas.com")


def test_get_player_response_invalid_endpoint(ps):
    with pytest.raises((AssertionError)):
        ps.get_response(ps.url + "/invalid_url")


def test_scrape_player(ps):
    data = ps.scrape()
    assert isinstance(data, dict)
    assert data[f"player_stats_{ps.id}"][0]["element"] == ps.id
