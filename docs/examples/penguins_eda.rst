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


        >>> df["body_mass_g"].hist(bins=10)

        counts
         70.0┤             _____
             |            |     |
             |            |     |
             |            |     |
             |            |     |
             |            |     |
         54.0┤            |     |
             |            |     |_____
             |            |     |     |
             |            |     |     |
             |       _____|     |     |
             |      |     |     |     |_____ _____
         38.0┤      |     |     |     |     |     |
             |      |     |     |     |     |     |
             |      |     |     |     |     |     |
             |      |     |     |     |     |     |
             |      |     |     |     |     |     |_____ _____
             |      |     |     |     |     |     |     |     |
         22.0┤      |     |     |     |     |     |     |     |
             |      |     |     |     |     |     |     |     |
             |      |     |     |     |     |     |     |     |_____
             | _____|     |     |     |     |     |     |     |     |
             ||     |     |     |     |     |     |     |     |     |
             ||     |     |     |     |     |     |     |     |     |
          6.0┤|     |     |     |     |     |     |     |     |     |_____
             ├------------┬------------┬------------┬------------┬------------┬----
             2700.0       3420.0       4140.0       4860.0       5580.0       6300.0
                                          body_mass_g


For categorical features, bar plots can be useful. We can check which penguin
species are found on which islands in the data::


        >>> df[["species", "island"]].value_counts().plot.barh()

                                |
                                |------------------------┐
                                |                        |
            ('Adelie', 'Biscoe')┤                        |
                                |                        |
                                |-----------------------------┐
                                |                             |
         ('Adelie', 'Torgersen')┤                             |
                                |                             |
                                |-------------------------------┐
                                |                               |
             ('Adelie', 'Dream')┤                               |
                                |                               |
                                |--------------------------------------┐
                                |                                      |
          ('Chinstrap', 'Dream')┤                                      |
                                |                                      |
                                |--------------------------------------------------------------------┐
                                |                                                                    |
            ('Gentoo', 'Biscoe')┤                                                                    |
                                |                                                                    |
                                |--------------------------------------------------------------------
                                ├-------------┬-------------┬------------┬-------------┬-------------┬
                                0             25            50           75            100           125


Multivariate plots
------------------------------


Let's start by looking at bill and flipper lengths vary across species::


        >>> plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])


        flipper_length_mm
         232.0┤                                         o  o   o o    o o          o
              |                                          ooo o   o        o
              |                                           o ooo
              |                                 o         oooo
              |                            o   oo o oo ooo oooo   o
              |                            o  o  o o o  o  oo  o    o
         217.0┤                             o o   oo oo  oo  o
              |                      o   ooo  oooooooooo   o
              |                                oo o  o   o
              |                      + ooooooo ooooo o oo*   *  *
              |                                o                *         *
              |                      +                 o  *  **   * *
         202.0┤         +             +    *                ** **     *
              |      +      ++++   ++  ++       *    * *  **** *
              |                  +++    ++++ +  *+         ** *****
              |     +  +++++ ++ +++++++ + +      * * *   *** * **
              |       + +   +  ++ +  ++++  +    *+***   *
              |+   + ++ ++++ +++++++++  +       ****        *
         187.0┤      + + + + ++ +++ +*   * *      *            *
              |     ++  + +++++ + +  +              *
              |           +  ++ +   ++   *                                     *
              |              +  +   +   +
              |   +         +    + +              *                                  + Adelie
              |              +                                                       * Chinstrap
         172.0┤               +                                                      o Gentoo
              ├--------------┬--------------┬-------------┬--------------┬----------
              32.0           38.0           44.0          50.0           56.0
                                          bill_length_mm


To be continued!


.. _penguins: https://github.com/allisonhorst/palmerpenguins
