.. _examples:

========
Examples
========

Basic usage
-------------

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


EDA: Penguins
-------------------

For a more realistic example of shellplot in a data science usecase, we will
walk through an exploratory data analysis (EDA) of the `penguins`_ data.

For convenience, this dataset can be directly loaded from ``shellplot``::


        >>> import pandas as pd
        >>> import shellplot as plt
        >>> pd.set_option("plotting.backend", "shellplot")
        >>> df = plt.load_dataset("penguins")
        >>> df.sample(5)

          species  island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
           Gentoo  Biscoe            47.5           15.0              218.0       4950.0  FEMALE
           Adelie   Dream            38.9           18.8              190.0       3600.0  FEMALE
           Gentoo  Biscoe            47.2           15.5              215.0       4975.0  FEMALE
           Gentoo  Biscoe            46.4           15.6              221.0       5000.0    MALE
           Adelie  Biscoe            36.4           17.1              184.0       2850.0  FEMALE


Let's start by looking at bill and flipper lengths vary across species::


        >>> plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])

          flipper_length_mm
              |
           237┤
              |
              |                                        o  o   oo    o o         o
              |                                         ooo o  o        o
              |                                          ooooo
           223┤                                o oooo ooo  oo   o
              |                            o o ooo oo  oo oo o    o
              |                           oo  oo ooooo  oo o
              |                      o   o o  ooooo o  oo o
           209┤                        oo oo + oooo o oo*   *  *
              |                      +   o oo  o       o       *        *
              |                       +                o *  **   **
              |          +          + +++  *             * *** *    *
              |        +     ++++    + +++++   * +  * *   ** * **
           195┤          +++  + +++ +++++++  +  ** * *  * * * *
              |       + ++  +++ +++++++++  +   ** **   * *  **
              |  +  +  ++++++ ++++++ ++ +       ****      *
              |      + ++++++ ++ ++ +*   * *     * *          *
              |       +    + ++    + ++
           181┤            + +++++  +   +*                                   *
              |    +         +    + +            *
              |               +                                                      + Adelie
              |               +                                                      * Chinstrap
           167┤                                                                      o Gentoo
              ├------------┬-------------┬-------------┬-------------┬-------------┬
              31           37            43            49            55            61
                                          bill_length_mm


Next, we want to understand the distribution of body masses::


        >>> df["body_mass_g"].hist(bins=12)

          counts
           59┤
             |           ____
             |          |    |____
             |          |    |    |
             |          |    |    |
           48┤          |    |    |
             |          |    |    |
             |          |    |    |____
             |          |    |    |    |
             |          |    |    |    |
           37┤          |    |    |    |____
             |          |    |    |    |    |____
             |          |    |    |    |    |    |
             |          |    |    |    |    |    |
             |          |    |    |    |    |    |
           26┤      ____|    |    |    |    |    |____
             |     |    |    |    |    |    |    |    |     ____
             |     |    |    |    |    |    |    |    |    |    |
             |     |    |    |    |    |    |    |    |____|    |
             |     |    |    |    |    |    |    |    |    |    |
           15┤     |    |    |    |    |    |    |    |    |    |____
             |     |    |    |    |    |    |    |    |    |    |    |
             | ____|    |    |    |    |    |    |    |    |    |    |
             ||    |    |    |    |    |    |    |    |    |    |    |
            4┤|    |    |    |    |    |    |    |    |    |    |    |____
             ├-----------┬------------┬------------┬------------┬-----------┬------
             2619        3393         4167         4941         5715        6489
                                          body_mass_g

to be continued...


.. _penguins: https://github.com/allisonhorst/palmerpenguins
