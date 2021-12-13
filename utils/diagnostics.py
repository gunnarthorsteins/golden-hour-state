class DiagnosticPlots:
    """Reproduces the 4 base plots of an OLS model in R.
    
    Original code from here: https://bit.ly/3a4YGH1, with modifications
    by gt2447.
    """

    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.fig, self.ax = plt.subplots(2, 2)
        self.set_properties()

        self.model()
        self.resid_vs_fitted()
        self.qq_plot()
        self.heteroscedasticity()
        self.resid_vs_leverage()

    def model(self):
        """Creates a linear regression model"""

        self.model = sm.OLS(self.y, sm.add_constant(self.X)).fit()

        # create df from X, y for easier plot handling
        self.df = pd.concat([self.X, self.y], axis=1)

        # Getting miscallaneous properties
        self.modelted_y = self.model.fittedvalues
        self.model_residuals = self.model.resid
        self.model_norm_residuals = self.model.get_influence().resid_studentized_internal
        self.model_norm_residuals_abs_sqrt = np.sqrt(
            np.abs(self.model_norm_residuals))
        self.model_abs_resid = np.abs(self.model_residuals)
        self.model_leverage = self.model.get_influence().hat_matrix_diag
        self.model_cooks = self.model.get_influence().cooks_distance[0]

        print(self.model.summary())

    def graph(self, formula, x_range, label=None):
        """Helper function for plotting cook's distance lines"""

        x = x_range
        y = formula(x)
        plt.plot(x, y, label=label, lw=1, ls='--', color='red')

    def resid_vs_fitted(self):
        sns.residplot(self.modelted_y, self.df.columns[-1], data=self.df,
                      ax=self.ax[0, 0],
                      lowess=True,
                      scatter_kws={'alpha': 0.5},
                      line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

        # Annotations
        abs_resid = self.model_abs_resid.sort_values(ascending=False)
        abs_resid_top_3 = abs_resid[:3]
        for i in abs_resid_top_3.index:
            self.ax[0, 0].annotate(i,
                                   xy=(self.modelted_y[i],
                                       self.model_residuals[i]))

    def qq_plot(self):
        QQ = ProbPlot(self.model_norm_residuals)
        QQ.qqplot(line='45',
                  alpha=0.5,
                  color='#4C72B0',
                  lw=1,
                  ax=self.ax[0, 1])

        # Annotations
        abs_norm_resid = np.flip(np.argsort(
            np.abs(self.model_norm_residuals)), 0)
        self.abs_norm_resid_top_3 = abs_norm_resid[:3]
        for r, i in enumerate(self.abs_norm_resid_top_3):
            self.ax[0, 1].annotate(i,
                                   xy=(np.flip(QQ.theoretical_quantiles,
                                               0)[r],
                                       self.model_norm_residuals[i]))

    def heteroscedasticity(self):
        self.ax[1, 0].scatter(self.modelted_y,
                              self.model_norm_residuals_abs_sqrt,
                              alpha=0.5)
        sns.regplot(self.modelted_y,
                    self.model_norm_residuals_abs_sqrt,
                    ax=self.ax[1, 0],
                    scatter=False,
                    ci=False,
                    lowess=True,
                    line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})



        # Annotations
        abs_sq_norm_resid = np.flip(
            np.argsort(self.model_norm_residuals_abs_sqrt), 0)
        abs_sq_norm_resid_top_3 = abs_sq_norm_resid[:3]
        for i in self.abs_norm_resid_top_3:
            self.ax[1, 0].annotate(i,
                                   xy=(self.modelted_y[i],
                                       self.model_norm_residuals_abs_sqrt[i]))

    def resid_vs_leverage(self):
        self.ax[1, 1].scatter(self.model_leverage,
                              self.model_norm_residuals, alpha=0.5)
        sns.regplot(self.model_leverage, self.model_norm_residuals,
                    ax=self.ax[1, 1],
                    scatter=False,
                    ci=False,
                    lowess=True,
                    line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

        # Annotations
        leverage_top_3 = np.flip(np.argsort(self.model_cooks), 0)[:3]
        for i in leverage_top_3:
            self.ax[1, 1].annotate(i,
                                   xy=(self.model_leverage[i],
                                       self.model_norm_residuals[i]))

        p = len(self.model.params)  # number of model parameters
        self.graph(lambda x: np.sqrt((0.5 * p * (1 - x)) / x),
                   np.linspace(0.001, max(self.model_leverage), 50),
                   'Cook\'s distance')  # 0.5 line
        self.graph(lambda x: np.sqrt((1 * p * (1 - x)) / x),
                   np.linspace(0.001, max(self.model_leverage), 50))  # 1 line
        self.ax[1, 1].legend(loc='upper right')

    def set_properties(self):
        self.ax[0, 0].set_title('Residuals vs Fitted')
        self.ax[0, 0].set_xlabel('Fitted values')
        self.ax[0, 0].set_ylabel('Residuals')
        self.ax[0, 0].xaxis.tick_top()
        self.ax[0, 0].xaxis.set_label_position('top')

        self.ax[0, 1].set_title('Normal Q-Q')
        self.ax[0, 1].set_xlabel('Theoretical Quantiles')
        self.ax[0, 1].set_ylabel('Standardized Residuals')
        self.ax[0, 1].yaxis.tick_right()
        self.ax[0, 1].xaxis.tick_top()
        self.ax[0, 1].xaxis.set_label_position('top')
        self.ax[0, 1].yaxis.set_label_position('right')

        self.ax[1, 0].set_ylabel('Std. Residuals')
        self.ax[1, 0].set_title('Scale-Location')
        self.ax[1, 0].set_xlabel('Fitted values')
        self.ax[1, 0].set_ylabel('$\sqrt{|Standardized Residuals|}$')

        self.ax[1, 1].yaxis.tick_right()
        self.ax[1, 1].set_xlabel('Leverage')
        self.ax[1, 1].set_ylabel('Std. Residuals')
        self.ax[1, 1].yaxis.set_label_position('right')
        self.ax[1, 1].set_xlim(0, max(self.model_leverage)+0.01)
        self.ax[1, 1].set_ylim(-3, 5)
        self.ax[1, 1].set_title('Residuals vs Leverage')