
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import *
from tensorflow.keras.layers import *
from tensorflow.keras import *
import matplotlib.pyplot as plt
import numpy as np
import pickle
import json

data = None

with open("./data.json", "r") as fp :
    data = json.load(fp)

data1 = np.array(data)
data2 = np.copy(data1)

train_x1 = np.array(data1[:, 1:].tolist())
train_t1 = np.array([1, 0] * train_x1.shape[0]).reshape(train_x1.shape[0], 2)

train_x2 = np.array(data2[:, 1:].tolist())[:, ::-1]
train_t2 = np.array([0, 1] * train_x2.shape[0]).reshape(train_x2.shape[0], 2)

train_x = np.concatenate((train_x1, train_x2), axis=0)
train_t = np.concatenate((train_t1, train_t2), axis=0)

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
dense1 = Dense(100, activation="relu")(concatenated)
dense2 = Dense(10, activation="relu")(dense1)
output = Dense(2, activation="softmax")(dense2)

# model
model = Model([input1, input2], output)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

check_point = ModelCheckpoint("./model/best_model.h5", monitor="val_loss")
# early_stopping = EarlyStopping(monitor="val_loss", verbose=1, patience=20)

model.summary()

history = model.fit(
    [train_input[:, 0], train_input[:, 1]],
    train_target,
    epochs=100,
    batch_size=100,
    validation_data=([test_input[:, 0], test_input[:, 1]], test_target),
    callbacks=[check_point]  
)

with open("./scaler.pickle", "wb") as fp :
    pickle.dump(scaler_list, fp)

plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.xlabel("epoch")
plt.xlabel("loss")
plt.legend(["train", "val"])
plt.show()