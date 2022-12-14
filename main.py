
from tensorflow import keras
from player import Searcher
import numpy as np
import pickle

# load model
model = keras.models.load_model("./model/best_model.h5")
scaler_list = []

with open("./model/scaler.pickle", "rb") as fp :
    scaler_list = pickle.load(fp)

searcher = Searcher()

predict_input = np.array([
    [
        searcher.get_info_list("Francis Ngannou"),
        searcher.get_info_list("Alexander Volkov")
    ],
    [
        searcher.get_info_list("Alexander Volkanovski"),
        searcher.get_info_list("Chan Sung Jung")
    ],
    [
        searcher.get_info_list("Israel Adesanya"),
        searcher.get_info_list("Darren Till")
    ]
])

# transform
for i in range(predict_input.shape[-1]) :
    scaler = scaler_list[i]
    predict_input[:, :, i] = scaler.transform(predict_input[:, :, i])

predict1 = model.predict([predict_input[:, 0], predict_input[:, 1]])
predict2 = model.predict([predict_input[:, 1], predict_input[:, 0]])

print(predict1, predict2)