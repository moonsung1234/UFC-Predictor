
from bs4 import BeautifulSoup
import requests
import json

class Searcher :
    def __get_tool(self, url) :
        res = requests.get(url)

        if res.status_code == 200 :
            soup = BeautifulSoup(res.text, "html.parser")

            return soup

        else :
            return None

    def __find_player(self, player_list, player_piece_name) :
        for i, player_name in enumerate(player_list) :
            if player_piece_name in player_name :
                return i

        return None 
    
    def __init__(self) :
        self.url = "https://kr.ufc.com"
        self.rank_url = self.url + "/rankings"

        self.players_name = []
        self.players_href = []
        
        soup = self.__get_tool(self.rank_url)
        contents = soup.select(".view-grouping-content")

        for content in contents :
            players = content.select(".views-row a")

            self.players_name += list(map(lambda x : x.get_text().strip(), players))
            self.players_href += list(map(lambda x : self.url + x["href"], players))

    def get_info(self, player_name) :
        index = self.__find_player(self.players_name, player_name)

        if index != None :
            href = self.players_href[index]

            soup = self.__get_tool(href)

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
                "leg_reach" : 0
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

                return info_dic

            except :
                return None

    def get_info_list(self, player_name) :
        info_dic = self.get_info(player_name)
        values = list(info_dic.values())

        return values