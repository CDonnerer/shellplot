.. _basic_usage:

===========
Basic usage
===========


Shellplot aims to reproduce matplotlib's plotting API::


        >>> import numpy as np
        >>> import shellplot as plt
        >>> x = np.arange(-3, 3, 0.05)
        >>> y = np.cos(x) ** 2
        >>> plt.plot(x, y)

          1.0┤                             +
             |+                          +++++                          +
             | +                        +     +                        +
             |  +                      +       +                      +
         0.75┤   +                    +         +                    +
             |    +                  ++         ++                  +
             |    +                  +           +                  +
             |     +                +             +                +
          0.5┤      +              +               +              +
             |      +              +               +              +
             |       +            +                 +            +
             |        +          +                   +          +
         0.25┤        ++        ++                   ++        ++
             |         ++       +                     +       ++
             |          ++    ++                       ++    ++
          0.0┤           ++++++                         ++++++
             ├------------------┬-------------------┬-------------------┬
             -3                 -1                  1                   3


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
