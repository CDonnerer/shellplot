EDA: Penguins
=================

Getting setup
--------------

For a more realistic example of shellplot in a data science usecase, we will
walk through an exploratory data analysis (EDA) of the `penguins`_ data.

We first import pandas and shellplot and set the pandas plotting backend::


        >>> import pandas as pd
        >>> import shellplot as plt
        >>> pd.set_option("plotting.backend", "shellplot")


For convenience, the penguins dataset can be directly loaded from ``shellplot``::


        >>> df = plt.load_dataset("penguins")
        >>> df.sample(5)

          species  island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
           Gentoo  Biscoe            47.5           15.0              218.0       4950.0  FEMALE
           Adelie   Dream            38.9           18.8              190.0       3600.0  FEMALE
           Gentoo  Biscoe            47.2           15.5              215.0       4975.0  FEMALE
           Gentoo  Biscoe            46.4           15.6              221.0       5000.0    MALE
           Adelie  Biscoe            36.4           17.1              184.0       2850.0  FEMALE



Exploring features
------------------------------

Histograms offer a nice way to explore numeric features. For example, we can
plot the distribution of penguin body masses::


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


For categorical features, bar plots can be useful. We can check which penguin
species are contained in the data::


        >>> df["species"].value_counts().plot.barh()

                  |
                  |----------------------------------┐
                  |                                  |
                  |                                  |
                  |                                  |
         Chinstrap┤                                  |
                  |                                  |
                  |                                  |
                  |                                  |
                  |---------------------------------------------------------------┐
                  |                                                               |
                  |                                                               |
                  |                                                               |
            Gentoo┤                                                               |
                  |                                                               |
                  |                                                               |
                  |                                                               |
                  |-----------------------------------------------------------------------------┐
                  |                                                                             |
                  |                                                                             |
                  |                                                                             |
            Adelie┤                                                                             |
                  |                                                                             |
                  |                                                                             |
                  |                                                                             |
                  |-----------------------------------------------------------------------------
                  ├---------------┬--------------┬---------------┬---------------┬--------------┬-
                  0               31             62              93              124            155


We can also check how these species are distributed on the differen islands::


        >>> df[["species", "island"]].value_counts().plot.barh()

                        |---------------------------┐
                        |                           |
                        |                           |
    ('Adelie', 'Biscoe')┤                           |
                        |                           |
                        |--------------------------------┐
                        |                                |
 ('Adelie', 'Torgersen')┤                                |
                        |                                |
                        |                                |
                        |-----------------------------------┐
                        |                                   |
                        |                                   |
     ('Adelie', 'Dream')┤                                   |
                        |                                   |
                        |------------------------------------------┐
                        |                                          |
  ('Chinstrap', 'Dream')┤                                          |
                        |                                          |
                        |                                          |
                        |-----------------------------------------------------------------------------┐
                        |                                                                             |
                        |                                                                             |
    ('Gentoo', 'Biscoe')┤                                                                             |
                        |                                                                             |
                        |-----------------------------------------------------------------------------
                        ├---------------┬--------------┬---------------┬--------------┬---------------┬-
                        0               25             50              75             100             125




Multivariate plots
------------------------------


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



to be continued...


.. _penguins: https://github.com/allisonhorst/palmerpenguins
