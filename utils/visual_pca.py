class CaliPCA(PCA):
    """Performs PCA on data and plots the analysis,
    inheriting from its superclass PCA (sklearn)
    """

    def __init__(self, n_components=None):
        """Initializing the superclass with number of components
        'None' (default) means that the number of components isn't fixed
        """

        super().__init__(n_components=n_components)
        self.fig, self.ax1 = plt.subplots()
        self.ax2 = self.ax1.twinx()
        plot_size(7, 5, 80)

    def standardize(self, df):
        """Standardizes the data (mean=0, variance=1)
        a necessary step for PCA
        """

        scaled = sklearn.preprocessing.scale(df)
        self.fit(scaled)
        self.var = self.explained_variance_
        self.var_cumsum = np.cumsum(self.explained_variance_ratio_) * 100
        self.x = list(range(1, len(self.var_cumsum) + 1))

    def leftplot(self, c=colors['blue'], z=2):
        """Plots the cumulative sum"""
        y = self.var_cumsum
        self.ax1.plot(self.x, y, c=c, zorder=z)
        self.ax1.scatter(self.x, y, c=c, edgecolors='k', zorder=z+1)

    def rightplot(self, c=colors['orange'], z=2):
        """Plots the variance"""
        y = self.var
        self.ax2.plot(self.x, y, c=c, zorder=z)
        self.ax2.scatter(self.x, y, c=c, edgecolors='k', zorder=z+1)

    def props(self):
        """Sets plot properties"""

        self.ax1.set_title('PCA Analysis')
        self.ax1.set_xticks(np.arange(0, len(self.var_cumsum)+1, 1))
        self.ax1.set_xlabel('PCA Dim')
        self.ax1.grid()

        self.ax1.set_ylabel('Cumulative Sum [%]', c=colors['Blue'])
        # Horizontal line to show 90% mark
        self.ax1.axhline(y=90, c=colors['blue'],
                         linestyle='--', linewidth=3, zorder=1)
        self.ax1.set_ylim((0, 100))
        self.ax1.set_yticks(np.arange(0, 110, 10))

        self.ax2.set_ylabel('Variance []', c=colors['orange'])
        # Horizontal line to show where variance crosses 1
        # Usually we don't use the components less than 1
        self.ax2.axhline(y=1, c=colors['orange'],
                         linestyle='--', linewidth=3, zorder=1)
        self.ax2.set_ylim((0, 10))
        self.ax2.set_yticks(np.arange(0, 11, 1))