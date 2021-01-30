.. _basic_usage:

===========
Basic usage
===========

Scatter plot
-------------------

Scatter plots can be created via the ``plot`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-4, 4, 0.01)
        >>> y = np.cos(x)
        >>> plt.plot(x, y)

          1.0┤                                     ++++++
             |                                   +++     ++
             |                                  ++         ++
             |                                 ++           ++
             |                                ++             ++
             |                               ++               ++
          0.6┤                              ++                 ++
             |                              +                   +
             |                             +                    ++
             |                            ++                     ++
             |                           ++                       ++
             |                           +                         +
          0.2┤                          ++                         ++
             |                         ++                           ++
             |                         +                             +
             |                        ++                             ++
             |                       ++                               ++
             |                       +                                 +
         -0.2┤                      ++                                 ++
             |                     ++                                   ++
             |                     +                                     +
             |                    +                                      ++
             |                   ++                                       ++
             |                  ++                                         ++
         -0.6┤                 ++                                           +
             |++               +                                             +               ++
             | ++             +                                              ++             ++
             |  ++          ++                                                ++           ++
             |   ++        ++                                                   ++        ++
             |    +++    +++                                                     +++    +++
         -1.0┤      ++++++                                                         ++++++
             └┬-------------------┬-------------------┬-------------------┬-------------------┬
              -4                  -2                  0                   2                   4


It is possible to modify the appearance of the plot by passing keyword args,
using a similar syntax to `matplotlib`_. E.g. we could modify the above call to
``plot`` like so::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-4, 4, 0.01)
        >>> y = np.cos(x)
        >>> plt_str = plt.plot(
                x, y,
                figsize=(40, 21),
                xlim=(0, 3),
                ylim=(-1, 1),
                xlabel="x",
                ylabel="cos(x)",
                return_type="str",
            )
        >>> print(plt_str)

          cos(x)
          1.0┤+++++
             |    ++++
             |       +++
             |         +++
             |           +++
          0.5┤             ++
             |              +++
             |                ++
             |                 ++
             |                   ++
          0.0┤                    ++
             |                     ++
             |                      +++
             |                        ++
             |                         ++
         -0.5┤                           ++
             |                            +++
             |                              ++
             |                               ++++
             |                                  ++++
         -1.0┤                                     +++
             └┬------------┬------------┬------------┬
              0            1            2            3
                                  x

Please refer to :ref:`api_reference` for the full list of possible options.


Multiple series
-------------------

Multiple series can be plotted by providing 2d arrays to the plot function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-3, 6, 0.01)
        >>> y1 = np.cos(x)
        >>> y2 = np.sin(x)
        >>> x, y = np.vstack((x, x)), np.vstack((y1, y2))
        >>> plt.plot(x, y, line=True, label=("cos", "sin"), figsize=(70, 25))

          1.0┤                      ·+·        ·*··*
             |                    ·+   +·     *     ·
             |                  +·       ·+  ·       *                           +
             |                              *         ·                        ··
             |                 ·           ·           *                      +
             |                +           * +           ·
          0.5┤               ·           ·   ·           ·                   ·
             |                          ·                 *                 +
             |              +          *      +            ·
             |             ·                                               ·
             |            ·           ·        ·            *
             |           +                      +                         +
          0.0┤                       *           ·           ·           ·
             |          ·
             |*                     ·             ·           *         ·
             |         +                           +           ·       +
             | ·      ·            *                ·           ·     ·
             |  *                 ·                              *
         -0.5┤   ·   +           ·                   +            ·  +
             |    ·             *                                                *
             |     *·          ·                      ·            *·          ··
             |     +·         *                        +           +·         *
             |   ··  *       ·                          ··        ·  *       ·
             |  +     ·    ·*                             +     ·+    ·     *       + cos
         -1.0┤+·       *·*·                                ·+·+·       *··*·        * sin
             └┬--------------┬---------------┬--------------┬--------------┬--------
              -3             -1              1              3              5



Histogram
-------------------

Histogram plots can be created via the ``hist`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.random.randn(10000)
        >>> plt.hist(x, bins=8)

          counts
         3220┤                                         ---------
             |                                        |         |
             |                               ---------|         |
             |                              |         |         |
             |                              |         |         |
             |                              |         |         |
         2576┤                              |         |         |
             |                              |         |         |
             |                              |         |         |
             |                              |         |         |
             |                              |         |         |
             |                              |         |         |
         1932┤                              |         |         |
             |                              |         |         |
             |                              |         |         |
             |                              |         |         |---------
             |                              |         |         |         |
             |                     ---------|         |         |         |
         1288┤                    |         |         |         |         |
             |                    |         |         |         |         |
             |                    |         |         |         |         |
             |                    |         |         |         |         |
             |                    |         |         |         |         |
             |                    |         |         |         |         |
          644┤                    |         |         |         |         |
             |                    |         |         |         |         |
             |                    |         |         |         |         |---------
             |           ---------|         |         |         |         |         |
             |          |         |         |         |         |         |         |
             |          |         |         |         |         |         |         |---------
            0┤ ---------|         |         |         |         |         |         |         |
             └┬-------------------┬-------------------┬-------------------┬-------------------┬
              -4                  -2                  0                   2                   4



Bar plot
-------------------

Bar plots can be created via the ``bar`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.logspace(0, 1, 3)
        >>> plt.barh(x, labels=np.array(["bar_1", "bar_b", "bar_3"]), figsize=(61, 19))

          |------------------------------------------------------------
          |                                                            |
          |                                                            |
     bar_3┤                                                            |
          |                                                            |
          |                                                            |
          |------------------------------------------------------------
          |                   |
          |                   |
     bar_b┤                   |
          |                   |
          |                   |
          |-------------------
          |      |
          |      |
     bar_1┤      |
          |      |
          |      |
          |------
          └┬-----------┬-----------┬-----------┬-----------┬-----------┬
           0.0         2.0         4.0         6.0         8.0         10.0



Box plot
-------------------

Box plots can be created via the ``boxplot`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = [np.random.randn(100) for i in range(3)]
        >>> plt.boxplot(x, labels=np.array(["dist_1", "dist_2", "dist_3"]))

               |
               |
               |                  ----------------
               |  |              |      |         |                   |
         dist_3┤  |--------------|      |         |-------------------|
               |  |              |      |         |                   |
               |                  ----------------
               |
               |
               |
               |                    ---------------
               ||                  |      |        |                     |
         dist_2┤|------------------|      |        |---------------------|
               ||                  |      |        |                     |
               |                    ---------------
               |
               |
               |
               |                     ------------
               |   |                |     |      |                                  |
         dist_1┤   |----------------|     |      |----------------------------------|
               |   |                |     |      |                                  |
               |                     ------------
               |
               |
               └┬-------------┬-------------┬-------------┬-------------┬-------------
                -2.2          -1.0          0.2           1.4           2.6


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
.. _matplotlib: https://matplotlib.org/contents.html#
