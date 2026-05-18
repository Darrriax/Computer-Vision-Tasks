import numpy as np
import matplotlib.pyplot as plt

# Параметри
EPOCHS = 2
ALPHA = 0.1
SYMBOLS = ["?", "!", "%", "("]

QUESTION_MARK = [0, 1, 1, 1, 1, 0,
                 1, 0, 0, 0, 0, 1,
                 0, 1, 0, 0, 1, 0,
                 0, 0, 0, 1, 0, 0,
                 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 1, 0, 0]

EXCLAMATION_MARK = [0, 0, 1, 1, 0, 0,
                    0, 0, 1, 1, 0, 0,
                    0, 0, 1, 1, 0, 0,
                    0, 0, 1, 1, 0, 0,
                    0, 0, 0, 0, 0, 0,
                    0, 0, 1, 1, 0, 0]

PERCENT_SIGN = [1, 1, 0, 0, 0, 1,
                1, 1, 0, 0, 1, 0,
                0, 0, 0, 1, 0, 0,
                0, 0, 1, 0, 0, 0,
                0, 1, 0, 0, 1, 1,
                1, 0, 0, 0, 1, 1]

LEFT_PARENTHESIS = [0, 0, 0, 1, 0, 0,
                    0, 0, 1, 0, 0, 0,
                    0, 0, 1, 0, 0, 0,
                    0, 0, 1, 0, 0, 0,
                    0, 0, 1, 0, 0, 0,
                    0, 0, 0, 1, 0, 0]

# ----------------------------------- Вхідні дані DataSet ------------------------------------
def data_x():
    # Візуалізація символів
    symbols = [QUESTION_MARK, EXCLAMATION_MARK, PERCENT_SIGN, LEFT_PARENTHESIS]
    plt.figure(figsize=(10, 2))
    for i, symbol in enumerate(symbols):
        plt.subplot(1, 4, i+1)
        plt.imshow(np.array(symbol).reshape(6, 6), cmap='viridis')
    plt.show()

    # Формування вхідних даних
    x = [np.array(symbol).reshape(1, 36) for symbol in symbols]
    return x

def data_y():
    # Формування вихідних даних
    out_dataset = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    y = np.array(out_dataset)
    return y

# ----------------------------------- Конструювання нейромережі ------------------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def f_forward(x, w1, w2):
    # Прихований прошарок
    z1 = x.dot(w1)
    a1 = sigmoid(z1)

    # Вихідний прошарок
    z2 = a1.dot(w2)
    a2 = sigmoid(z2)
    return a2

def generate_wt(x, y):
    return np.random.randn(x, y)

def loss(out, Y):
    return np.sum(np.square(out - Y)) / len(y)

def back_prop(x, y, w1, w2, alpha):
    # Прихований прошарок
    z1 = x.dot(w1)
    a1 = sigmoid(z1)

    # Вихідний прошарок
    z2 = a1.dot(w2)
    a2 = sigmoid(z2)

    # Похибка на вихідному прошарку
    d2 = a2 - y
    d1 = np.multiply(w2.dot(d2.T).T, np.multiply(a1, 1 - a1))

    # Градієнт для w1 і w2
    w1_adj = x.T.dot(d1)
    w2_adj = a1.T.dot(d2)

    # Оновлення параметрів
    w1 -= alpha * w1_adj
    w2 -= alpha * w2_adj
    return w1, w2

def train(x, Y, w1, w2, alpha, epochs):
    acc = []
    losses = []
    for epoch in range(epochs):
        epoch_losses = []
        for i in range(len(x)):
            out = f_forward(x[i], w1, w2)
            epoch_losses.append(loss(out, Y[i]))
            w1, w2 = back_prop(x[i], y[i], w1, w2, alpha)
        epoch_loss = sum(epoch_losses) / len(x)
        epoch_acc = (1 - epoch_loss) * 100
        print(f"Epoch {epoch + 1}: Accuracy = {epoch_acc:.2f}%")
        acc.append(epoch_acc)
        losses.append(epoch_loss)
    return w1, w2, acc, losses

def predict(x, w1, w2):
    output = f_forward(x, w1, w2)
    prediction = np.argmax(output)
    confidence = output[0][prediction]
    return prediction, confidence

# ----------------------------------- Основний процес ---------------------------------------
x = data_x()
y = data_y()

# Генерація початкових вагових коефіціентів
w1 = generate_wt(36, 5)
w2 = generate_wt(5, 4)

print("============== Вхідні параметри DataSet =============")
for i, xi in enumerate(x):
    print(f"x{i} \n", xi)
print("==================== Вихідна частина DataSet ====================")
for i, yi in enumerate(y):
    print(f"y{i} \n", yi)
print("===================== Навчання нейронної мережі =====================")
trained_wts = train(x, y, w1, w2, ALPHA, EPOCHS)
print("==================== Обчислені вагові коефіціенти ====================")
print("w1 \n", trained_wts[0])
print("w2 \n", trained_wts[1])

# Графічне відображення процесу навчання мережі
plt.plot(trained_wts[2])
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title('Accuracy over Epochs')
plt.show()

plt.plot(trained_wts[3])
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.title('Loss over Epochs')
plt.show()

# Ідентифікація літералів / передбачення
for i, symbol in enumerate(SYMBOLS):
    print(f'Вхідні параметри відповідають літералу "{symbol}"')
    print('Результат ідентифікації:')
    prediction, confidence = predict(x[i], trained_wts[0], trained_wts[1])
    print(f'Передбачений літерал: "{SYMBOLS[prediction]}" з впевненістю {confidence * 100:.2f}%\n')
