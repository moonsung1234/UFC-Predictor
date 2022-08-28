
# UFC Match Predictor

    UFC 경기를 보면서, 선수들의 정보를 이용하여 경기 결과를 높은 확률로 예측할 수 없을까 하는 아이디어를 떠올렸다.

## Feature (example)
|hitting_accuracy|takedown_accuracy|critical_hit_blow|critical_absorption_strike|average_takedown|average_submission|critical_hit_defense|takedown_defense|average_knockdown|age|height|weight|reach|leg_reach|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|57.0|37.0|6.79|3.53|1.71|0.22|60.0|73.0|0.37|33.0|167.64|65.53|181.61|91.44|

## Model
- model structure
![model](https://user-images.githubusercontent.com/71556009/187060585-891722c1-0ffd-452e-9c12-40cafa3babd8.PNG)

- loss(train, test) graph
![graph](https://user-images.githubusercontent.com/71556009/187060925-71a84cb7-31db-47a9-be64-e05080a9fdbc.PNG)

## Predict
#### Francis Ngannou vs Alexander Volkov
> 98% vs 0.02%

#### Alexander Volkanovski vs Chan Sung Jung
> 99% vs 0.01% 

#### Israel Adesanya vs Darren Till
> 99% vs 0.01%


## More
- 본 model 은 오직 선수들의 외적 데이터를 통해 경기 결과를 예측하므로 예상하지 못하는 변수(에드워즈 헤드킥같은 상황) 는 고려하지 못한다.
- over fitting 이 어김없이 일어났지만 기존의 경기 결과와 새로운 예측에 대해서 비교적 좋게 나타난다.
- 딥러닝을 다시 공부하기 시작한 후, 2번째 offical project 이며 개인적으로 만족스럽다. ^^

<br/>