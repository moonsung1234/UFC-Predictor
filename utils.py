
from bs4 import BeautifulSoup
import requests

def get_tool(url) :
    res = requests.get(url)

    if res.status_code == 200 :
        soup = BeautifulSoup(res.text, "html.parser")

        return soup

    else :
        return None

def find_player(player_list, player_piece_name) :
    for player_name in player_list :
        if player_piece_name in player_name :
            return player_name

    return None

url = "https://kr.ufc.com"
rank_url = url + "/rankings"

soup = get_tool(rank_url)

contents = soup.select(".view-grouping-content")

players_name = []
players_href = []

for content in contents :
    players = content.select(".views-row a")

    players_name += list(map(lambda x : x.get_text(), players))
    players_href += list(map(lambda x : url + x["href"], players))

print(players_name)

info_list = []

for href in players_href :
    soup = get_tool(href)

    info_dic = {
        "age" : None,
        "height" : None,
        "weight" : None,
        "reach" : None,
        "leg_reach" : None,
        "histories" : None
    }

    features = soup.select(".c-bio__field")

    for feature in features :
        label = feature.select_one(".c-bio__label").get_text()
        value = feature.select_one(".c-bio__text").get_text()

        if label == "나이" :
            info_dic["age"] = float(value)

        elif label == "높이" :
            info_dic["height"] = float(value)

        elif label == "무게" :
            info_dic["weight"] = float(value)

        elif label == "리치" :
            info_dic["reach"] = float(value)

        elif label == "다리 리치" :
            info_dic["leg_reach"] = float(value)

    history = soup.select("div[class='l-container']")[-1]
    results = history.select(".l-listing__item")

    history_list = []

    for result in results :
        subject = result.select_one(".c-card-event--athlete-results__headline").get_text().split(" vs ")
        red_win = result.select_one(".c-card-event--athlete-results__red-image").get_text().strip()
        
        if red_win == "승리" :
            history_list.append(subject)

        else :
            history_list.append(subject[::-1])

        # sub1_player = find_player(players_name, subject[0])
        # sub2_player = find_player(players_name, subject[1])

        # print("{} : {}, {} : {}".format(
        #     subject[0],
        #     "y" if sub1_player != None else "n",
        #     subject[1],
        #     "y" if sub2_player != None else "n"
        # ))

    info_dic["histories"] = history_list

    info_list.append(info_dic)

    print(info_dic)

print(info_list)
