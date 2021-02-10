.. _basic_usage:

===========
Basic usage
===========

Scatter plot
-------------------

Scatter plots can be created via the ``plot`` function::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-4, 4, 0.05)
        >>> y = np.cos(x)
        >>> plt.plot(x, y)

          1.0┤                                 +++++
             |                               ++     ++
             |                              ++       ++
             |                            ++           ++
             |                            +             +
             |                           +               +
          0.5┤                          +                 +
             |                         ++                 ++
             |                        ++                   +
             |                        +                     +
             |                       ++                     ++
             |                      ++                       ++
             |                      +                         +
          0.0┤                     +                           +
             |                     +                           +
             |                    +                             +
             |                   +                               +
             |                  ++                               ++
             |                 ++                                 +
             |                 +                                   +
         -0.5┤                ++                                   ++
             |+              ++                                     ++
             |++            ++                                       ++            ++
             | ++          ++                                         ++          ++
             |  ++        ++                                           ++        ++
             |   +++    ++                                               ++    ++
         -1.0┤     ++++++                                                 ++++++
             └┬-----------------┬----------------┬----------------┬-----------------┬
              -4                -2               0                2                 4


Figure API
-------------------

Similar to `matplotlib`_, shellplot has an "object-orientated" interface for
making plots, which works by creating and modifying a figure state. This is
useful for more complex plots, such as plotting multiple arrays::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-4, 4, 0.5)
        >>> fig = plt.figure()
        >>> fig.plot(x, np.cos(x), label="cos(x)")
        >>> fig.plot(x, np.sin(x), label="sin(x)", marker=None, line=True)
        >>> fig.set_xlim((-4, 2))
        >>> fig.set_xlabel("x axis")
        >>> fig.set_xlabel("y axis")
        >>> fig.show()

          y axis
          1.0┤                                               +               ·····
             |                                                            ···     ··
             |                                         +          +     ··
             |·                                                        ·
             | ·                                                     ··
             |  ·                                                   ·
          0.5┤   ··                              +                 ·    +
             |     ·                                              ·
             |      ·                                            ·
             |       ·                                          ·
             |        ·
             |                                                 ·
             |         ·                   +                  ·               +
          0.0┤          ·                                    ·
             |           ·                                  ·
             |            ·                                ·
             |             ·                              ·
             |              ·                            ·
             |               ·       +                  ·                           +
             |                ·                        ·
         -0.5┤                 ·                      ·
             |+                 ·                    ·
             |                   ·                 ··
             |                  + ··              ·
             |                      ·           ··
             |      +                ···     ···                                     + cos(x)
         -1.0┤            +             ·····                                        · sin(x)
             └┬-------------┬-------------┬-------------┬-------------┬-------------┬
              -4.0          -2.8          -1.6          -0.4          0.8           2.0
                                              x axis


Histogram
-------------------

Histogram plots can be created via the ``hist`` function. Below, we attach a
Histogram to an exiting figure::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.random.randn(10_000)
        >>> fig = plt.figure()
        >>> plt.hist(x, bins=8, fig=fig)
        >>> fig.show()

         3492┤                         -------
             |                        |       |
             |                        |       |
             |                        |       |
             |                        |       |
             |                        |       |-------
             |                        |       |       |
         2619┤                        |       |       |
             |                        |       |       |
             |                        |       |       |
             |                        |       |       |
             |                 -------|       |       |
             |                |       |       |       |
         1746┤                |       |       |       |
             |                |       |       |       |
             |                |       |       |       |
             |                |       |       |       |
             |                |       |       |       |
             |                |       |       |       |-------
             |                |       |       |       |       |
          873┤                |       |       |       |       |
             |                |       |       |       |       |
             |         -------|       |       |       |       |
             |        |       |       |       |       |       |
             |        |       |       |       |       |       |
             |        |       |       |       |       |       |-------
            0┤ -------|       |       |       |       |       |       |-------
             └┬---------------┬---------------┬---------------┬---------------┬------
              -4              -2              0               2               4



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


Global options
-------------------

Global options for shellplot can be viewed and set via ``get_option`` and
``set_option``. For example, this allows to override the standard figure size::


        >>> import shellplot as plt
        >>> plt.set_option("figsize", (70, 30))
        >>> plt.get_option("figsize")

        (70, 30)


.. _pandas: https://pandas.pydata.org/
.. _matplotlib: https://matplotlib.org/contents.html#
