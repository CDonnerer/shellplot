import numpy as np

import shellplot as plt

# x = np.arange(-4, 4, 0.01)
# y = np.cos(x)
# plt.plot(x, y)

x = [np.random.randn(100) for i in range(3)]
plt.boxplot(x)

# x = np.logspace(0, 1, 3)
# plt.barh(x, labels=np.array(["bar_1", "bar_b", "bar_3"]))
