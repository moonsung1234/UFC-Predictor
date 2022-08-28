
# UFC Match Predictor

    UFC 경기를 보면서, 선수들의 정보를 이용하여 경기 결과를 높은 확률로 예측할 수 없을까 하는 아이디어를 떠올렸다.

## Feature
- example
|hitting_accuracy|takedown_accuracy|critical_hit_blow|critical_absorption_strike|average_takedown|average_submission|critical_hit_defense|takedown_defense|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|57.0|37.0|6.79|3.53|1.71|0.22|60.0|73.0|0.37|33.0|167.64|65.53|181.61|91.44|

## Model
- model structure
![model](https://user-images.githubusercontent.com/71556009/187060585-891722c1-0ffd-452e-9c12-40cafa3babd8.PNG)

- loss(train, text) graph
![graph](https://user-images.githubusercontent.com/71556009/187060925-71a84cb7-31db-47a9-be64-e05080a9fdbc.PNG)

## More
- age, height, weight etc.. 의 14개 features 를 사용했다.
- over fitting 이 어김없이 일어났지만 기존의 경기 결과와 새로운 예측에 대해서 비교적 좋게 나타난다.
- 딥러닝을 다시 공부하기 시작한 후, 2번째 offical project 이며 개인적으로 만족스럽다. ^^

<br/>