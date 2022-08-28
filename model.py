
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import *
from tensorflow.keras.layers import *
from tensorflow.keras import *
import matplotlib.pyplot as plt
import numpy as np
import json

data = None

with open("./data.json", "r") as fp :
    data = json.load(fp)

data = np.array(data)

train_x = np.array(data[:, 1:].tolist())
train_x[:int(train_x.shape[0] / 2)] = train_x[:int(train_x.shape[0] / 2), ::-1]

train_t = np.array([1, 0] * train_x.shape[0]).reshape(train_x.shape[0], 2)
train_t[:int(train_t.shape[0] / 2)] = train_t[:int(train_t.shape[0] / 2), ::-1]

scaler_list = []

for i in range(train_x.shape[-1]) :
    scaler = StandardScaler()
    train_x[:, :, i] = scaler.fit_transform(train_x[:, :, i])

    scaler_list.append(scaler)

train_input, test_input, train_target, test_target = train_test_split(train_x, train_t, test_size=0.2, random_state=2022)

print(train_input.shape, train_target.shape)
print(train_input[0], train_target[0])

# player1 input
input1 = Input(shape=(14,))
dense11 = Dense(100, activation="relu")(input1)
dense12 = Dense(10, activation="relu")(dense11)

# player2 input
input2 = Input(shape=(14,))
dense21 = Dense(100, activation="relu")(input2)
dense22 = Dense(10, activation="relu")(dense21)

# concatenate
concatenated = concatenate([dense11, dense22])

# output
dense = Dense(10, activation="relu")(concatenated)
output = Dense(2, activation="softmax")(dense)

# model
model = Model([input1, input2], output)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

check_point = ModelCheckpoint("./best_model.h5")

model.summary()

history = model.fit(
    [train_input[:, 0], train_input[:, 1]],
    train_target,
    epochs=100,
    batch_size=100,
    validation_data=([test_input[:, 0], test_input[:, 1]], test_target),
    callbacks=[check_point]  
)

plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.xlabel("epoch")
plt.xlabel("loss")
plt.legend(["train", "val"])
plt.show()