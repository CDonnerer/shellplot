.. _basic_usage:

===========
Basic usage
===========

Scatter/ line plot
-------------------

Scatter/ line plots can be created via the ``plot`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-4, 4, 0.01)
        >>> y = np.cos(x)
        >>> plt.plot(x, y)


          1.0┤                                     ++++++
             |                                   +++    +++
             |                                 ++          ++
             |                                ++            ++
             |                               ++              ++
          0.6┤                              ++                ++
             |                             ++                  ++
             |                            ++                    ++
             |                           ++                      ++
             |                          ++                        ++
          0.2┤                         ++                          ++
             |                        ++                            ++
             |                        +                              +
             |                       ++                              ++
         -0.2┤                      ++                                ++
             |                     ++                                  ++
             |                    ++                                    ++
             |                   ++                                      ++
             |                  ++                                        ++
         -0.6┤                 ++                                          ++
             |++              ++                                            ++              ++
             | ++            ++                                              ++            ++
             |  ++          ++                                                ++          ++
             |    +++    +++                                                    +++    +++
         -1.0┤      ++++++                                                        ++++++
             ├-------------------┬-------------------┬------------------┬-------------------┬
             -4.0                -2.0                0.0                2.0                 4.0


Histogram plots
-------------------

Histogram plots can be accessed via the ``hist`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.random.randn(1000)
        >>> plt.hist(x, bins=8)

        counts
         316.0┤                            ________
              |                           |        |
              |                           |        |
              |                           |        |
              |                           |        |
         254.0┤                           |        |________
              |                           |        |        |
              |                           |        |        |
              |                           |        |        |
              |                           |        |        |
         192.0┤                   ________|        |        |
              |                  |        |        |        |
              |                  |        |        |        |
              |                  |        |        |        |
         130.0┤                  |        |        |        |
              |                  |        |        |        |________
              |                  |        |        |        |        |
              |                  |        |        |        |        |
              |                  |        |        |        |        |
          68.0┤          ________|        |        |        |        |
              |         |        |        |        |        |        |
              |         |        |        |        |        |        |________
              |         |        |        |        |        |        |        |
              | ________|        |        |        |        |        |        |
           6.0┤|        |        |        |        |        |        |        |________
              ├----------------┬---------------┬----------------┬---------------┬-------------
              -3.0             -1.7            -0.4             0.9             2.2



Bar plots
-------------------

Bar plots can be accessed via the ``bar`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.logspace(0, 1, 3)
        >>> plt.barh(x, labels=np.array(["bar_1", "bar_b", "bar_3"]))

              |-------------------------------------------------------------------------------┐
              |                                                                               |
              |                                                                               |
              |                                                                               |
         bar_3┤                                                                               |
              |                                                                               |
              |                                                                               |
              |                                                                               |
              |-------------------------------------------------------------------------------
              |                         |
              |                         |
              |                         |
         bar_b┤                         |
              |                         |
              |                         |
              |                         |
              |-------------------------
              |        |
              |        |
              |        |
         bar_1┤        |
              |        |
              |        |
              |        |
              |--------
              ├---------------┬---------------┬--------------┬---------------┬---------------┬
              0               2               4              6               8               10


Pandas integration
-------------------

Shellplot can directly be used via pandas, by setting the ``plotting.backend``
parameter::


        >>> import pandas as pd
        >>> pd.set_option("plotting.backend", "shellplot")
        >>> x = np.random.randn(1000)
        >>> my_series = pd.Series(data=x, name="my_fun_distribution")
        >>> my_series.hist(bins=10)

        counts
         286┤
            |                          ____
            |                     ____|    |
            |                    |    |    |
         215┤                    |    |    |____
            |                    |    |    |    |
            |                    |    |    |    |
            |                    |    |    |    |
         144┤                ____|    |    |    |
            |               |    |    |    |    |____
            |               |    |    |    |    |    |
            |               |    |    |    |    |    |
          73┤               |    |    |    |    |    |
            |           ____|    |    |    |    |    |____
            | ____ ____|    |    |    |    |    |    |    |____
            ├-------------┬-------------┬--------------┬-------------┬--
            -4.0          -2.0          0.0            2.0           4.0
                                my_fun_distribution
