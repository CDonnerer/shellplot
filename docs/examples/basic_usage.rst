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
             └┬----------------┬----------------┬-----------------┬----------------┬
              -4               -2               0                 2                4


Histogram plots
-------------------

Histogram plots can be created via the ``hist`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.random.randn(10000)
        >>> plt.hist(x, bins=10)

        counts
         2836┤                         -----
             |                        |     |-----
             |                        |     |     |
             |                        |     |     |
             |                        |     |     |
             |                        |     |     |
         2127┤                        |     |     |
             |                        |     |     |
             |                        |     |     |
             |                   -----|     |     |
             |                  |     |     |     |
             |                  |     |     |     |
         1418┤                  |     |     |     |-----
             |                  |     |     |     |     |
             |                  |     |     |     |     |
             |                  |     |     |     |     |
             |                  |     |     |     |     |
             |                  |     |     |     |     |
          709┤                  |     |     |     |     |
             |             -----|     |     |     |     |
             |            |     |     |     |     |     |-----
             |            |     |     |     |     |     |     |
             |            |     |     |     |     |     |     |
             |       -----|     |     |     |     |     |     |-----
            0┤ -----|     |     |     |     |     |     |     |     |-----
             └┬--------------┬--------------┬--------------┬--------------┬---------
              -4             -2             0              2              4



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
              └┬-------------┬-------------┬------------┬-------------┬-------------┬
               0             2             4            6             8             10


Pandas integration
-------------------

Shellplot can directly be used via `pandas`_, by setting the ``plotting.backend``
parameter::


        >>> import pandas as pd
        >>> pd.set_option("plotting.backend", "shellplot")
        >>> x = np.random.randn(10000)
        >>> my_series = pd.Series(data=x, name="my_fun_distribution")
        >>> my_series.hist(bins=10)

        counts
         2636┤                         -----
             |                        |     |-----
             |                        |     |     |
             |                        |     |     |
             |                        |     |     |
             |                        |     |     |
         1977┤                        |     |     |
             |                        |     |     |
             |                   -----|     |     |
             |                  |     |     |     |
             |                  |     |     |     |
             |                  |     |     |     |-----
         1318┤                  |     |     |     |     |
             |                  |     |     |     |     |
             |                  |     |     |     |     |
             |                  |     |     |     |     |
             |                  |     |     |     |     |
             |             -----|     |     |     |     |
          659┤            |     |     |     |     |     |
             |            |     |     |     |     |     |-----
             |            |     |     |     |     |     |     |
             |            |     |     |     |     |     |     |
             |       -----|     |     |     |     |     |     |
             |      |     |     |     |     |     |     |     |-----
            0┤ -----|     |     |     |     |     |     |     |     |-----
             └┬-----------┬-----------┬-----------┬-----------┬-----------┬---------
              -3.4        -2.0        -0.6        0.8         2.2         3.6
                                      my_fun_distribution



.. _pandas: https://pandas.pydata.org/
