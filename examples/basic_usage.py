import numpy as np

import shellplot as plt

x = np.arange(-4, 4, 0.01)
y = np.cos(x)

plt.plot(x, y)

x = np.random.randn(1000)
plt.hist(x, bins=12)
