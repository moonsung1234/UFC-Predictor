
from bs4 import BeautifulSoup
import numpy as np
import requests
import json
import os

if os.path.isfile("./data.json") :
    data = None
    
    with open("./data.json", "r") as fp :
        data = json.load(fp)

    print(len(data))

    exit(0)

def get_tool(url) :
    res = requests.get(url)

    if res.status_code == 200 :
        soup = BeautifulSoup(res.text, "html.parser")

        return soup

    else :
        return None

def find_player(player_list, player_piece_name) :
    for i, player_name in enumerate(player_list) :
        if player_piece_name in player_name :
            return i

    return None 

url = "https://kr.ufc.com"
rank_url = url + "/rankings"

soup = get_tool(rank_url)

contents = soup.select(".view-grouping-content")

players_name = []
players_href = []

for content in contents :
    players = content.select(".views-row a")

    players_name += list(map(lambda x : x.get_text().strip(), players))
    players_href += list(map(lambda x : url + x["href"], players))

corrected_players_name = []
info_list = []

for i, href in enumerate(players_href) :
    soup = get_tool(href)

    info_dic = {
        "hitting_accuracy" : 0,
        "takedown_accuracy" : 0,
        "critical_hit_blow" : 0,
        "critical_absorption_strike" : 0,
        "average_takedown" : 0,
        "average_submission" : 0,
        "critical_hit_defense" : 0,
        "takedown_defense" : 0,
        "average_knockdown" : 0,
        "age" : 0,
        "height" : 0,
        "weight" : 0,
        "reach" : 0,
        "leg_reach" : 0,
        "history" : 0
    }

    try :
        features1 = soup.select(".e-chart-circle__percent")
        features2 = soup.select(".c-stat-compare__group")
        features3 = soup.select(".c-bio__field")

        value1, value2 = list(map(lambda x : x.get_text().strip().replace("%", ""), features1))

        info_dic["hitting_accuracy"] = float(value1)
        info_dic["takedown_accuracy"] = float(value2)

        for feature in features2 :
            label = feature.select_one(".c-stat-compare__label").get_text().strip()
            value = feature.select_one(".c-stat-compare__number").get_text().strip()

            if label == "증요 명중 타격" :
                info_dic["critical_hit_blow"] = float(value)

            elif label == "중요 흡수 타격" :
                info_dic["critical_absorption_strike"] = float(value)

            elif label == "평균 테이크다운" :
                info_dic["average_takedown"] = float(value)

            elif label == "평균 서브미션" :
                info_dic["average_submission"] = float(value)

            elif label == "중요 타격 방어" :
                info_dic["critical_hit_defense"] = float(value.replace("%", ""))
            
            elif label == "테이크다운 방어" :
                info_dic["takedown_defense"] = float(value.replace("%", ""))

            elif label == "평균 녹다운" :
                info_dic["average_knockdown"] = float(value)

        for feature in features3 :
            label = feature.select_one(".c-bio__label").get_text().strip()
            value = feature.select_one(".c-bio__text").get_text().strip()

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
            winning_type = result.select(".c-card-event--athlete-results__result-text")[-1].get_text().strip().lower()

            if winning_type == "" or winning_type == None :
                winning_type = "Draw"

            if red_win == "승리" :
                subject.insert(0, winning_type)
                history_list.append(subject)

            else :
                subject.append(winning_type)
                history_list.append(subject[::-1])

        info_dic["history"] = history_list

        corrected_players_name.append(players_name[i])
        info_list.append(info_dic)

        print(info_dic)

    except :
        continue

data = []

for info in info_list :
    history_list = info["history"]

    for history in history_list :
        winning_type, player1, player2 = history
        player1, player2 = find_player(corrected_players_name, player1), find_player(corrected_players_name, player2)

        if player1 != None and player2 != None :
            data.append([
                winning_type,
                list(info_list[player1].values())[:-1],
                list(info_list[player2].values())[:-1]
            ])

print(len(data))

with open("./data.json", "w") as fp :
    json.dump(data, fp)