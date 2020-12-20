.. _basic_usage:

===========
Basic usage
===========

Scatter plots
-------------------

Scatter plots can be created via the ``plot`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-4, 4, 0.01)
        >>> y = np.cos(x)
        >>> plt.plot(x, y)

          1.0┤                                ++++++
             |                              +++    +++
             |                             ++        ++
             |                            ++          ++
             |                           ++            ++
             |                          ++              ++
          0.5┤                         ++                ++
             |                        ++                  ++
             |                        +                    +
             |                       +                      +
             |                      ++                      ++
             |                     ++                        ++
          0.0┤                     +                          +
             |                    ++                          ++
             |                   ++                            ++
             |                  ++                              ++
             |                  +                                +
             |                 ++                                ++
         -0.5┤                ++                                  ++
             |               ++                                    ++
             |++            ++                                      ++            ++
             | ++          ++                                        ++          ++
             |  ++        ++                                          ++        ++
             |   +++    +++                                            +++    +++
         -1.0┤     ++++++                                                ++++++
             ├----------------┬----------------┬-----------------┬----------------┬
             -4.0             -2.0             0.0               2.0              4.0


Histogram plots
-------------------

Histogram plots can be created via the ``hist`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.random.randn(5000)
        >>> plt.hist(x, bins=10)

        counts
         1435.0┤                         _____
               |                        |     |_____
               |                        |     |     |
               |                        |     |     |
               |                        |     |     |
               |                        |     |     |
         1077.0┤                        |     |     |
               |                        |     |     |
               |                        |     |     |
               |                        |     |     |
               |                   _____|     |     |
               |                  |     |     |     |
          719.0┤                  |     |     |     |_____
               |                  |     |     |     |     |
               |                  |     |     |     |     |
               |                  |     |     |     |     |
               |                  |     |     |     |     |
               |                  |     |     |     |     |
          361.0┤                  |     |     |     |     |
               |             _____|     |     |     |     |
               |            |     |     |     |     |     |_____
               |            |     |     |     |     |     |     |
               |            |     |     |     |     |     |     |
               |       _____|     |     |     |     |     |     |_____
            3.0┤ _____|     |     |     |     |     |     |     |     |_____
               ├---------------┬---------------┬----------------┬---------------┬----
               -4.0            -2.0            0.0              2.0             4.0



Bar plots
-------------------

Bar plots can be created via the ``bar`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.logspace(0, 1, 3)
        >>> plt.barh(x, labels=np.array(["bar_1", "bar_b", "bar_3"]))

              |---------------------------------------------------------------------┐
              |                                                                     |
              |                                                                     |
              |                                                                     |
         bar_3┤                                                                     |
              |                                                                     |
              |                                                                     |
              |                                                                     |
              |---------------------------------------------------------------------
              |                      |
              |                      |
              |                      |
         bar_b┤                      |
              |                      |
              |                      |
              |                      |
              |----------------------
              |       |
              |       |
              |       |
         bar_1┤       |
              |       |
              |       |
              |       |
              |-------
              ├-------------┬-------------┬------------┬-------------┬-------------┬
              0             2             4            6             8             10


Pandas integration
-------------------

Shellplot can directly be used via `pandas`_, by setting the ``plotting.backend``
parameter::


        >>> import pandas as pd
        >>> pd.set_option("plotting.backend", "shellplot")
        >>> x = np.random.randn(1000)
        >>> my_series = pd.Series(data=x, name="my_fun_distribution")
        >>> my_series.hist(bins=10)

        counts
         233.0┤                         _____
              |                        |     |
              |                        |     |_____
              |                        |     |     |
              |                        |     |     |
              |                        |     |     |
         176.0┤                        |     |     |
              |                        |     |     |_____
              |                   _____|     |     |     |
              |                  |     |     |     |     |
              |                  |     |     |     |     |
              |                  |     |     |     |     |
         119.0┤                  |     |     |     |     |
              |                  |     |     |     |     |
              |                  |     |     |     |     |
              |                  |     |     |     |     |_____
              |                  |     |     |     |     |     |
              |             _____|     |     |     |     |     |
          62.0┤            |     |     |     |     |     |     |
              |            |     |     |     |     |     |     |
              |            |     |     |     |     |     |     |
              |            |     |     |     |     |     |     |
              |       _____|     |     |     |     |     |     |_____
              |      |     |     |     |     |     |     |     |     |
           5.0┤ _____|     |     |     |     |     |     |     |     |_____
              ├------------┬-----------┬------------┬-----------┬------------┬------
              -3.1         -1.9        -0.7         0.5         1.7          2.9
                                       my_fun_distribution



.. _pandas: https://pandas.pydata.org/
