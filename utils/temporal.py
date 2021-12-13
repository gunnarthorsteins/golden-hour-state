class Temporal:
    """For plotting summary plots"""

    def __init__(self):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows=3)
        plot_size(8, 12, 80)

    def set_properties(self):
        """We manually change the axes for every subfigure"""

        ax1_array = np.linspace(0, 23, 24)
        ax1_labels = [np.array2string(i)[:-1] for i in ax1_array]
        self.ax1.set_xticks(range(24))
        self.ax1.set_xticklabels(ax1_labels)

        ax2_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Agu', 'Sep', 'Oct', 'Nov', 'Dec']
        self.ax2.set_xticks(range(12))
        self.ax2.set_xticklabels(ax2_labels)

        ax3_array = np.linspace(1998, 2019, 22)
        ax3_labels = [np.array2string(i) for i in ax3_array]
        ax3_labels = ["'" + i[2:4] for i in ax3_labels]
        self.ax3.set_xticks(range(22))
        self.ax3.set_xticklabels(ax3_labels)

    def plot(self, df, c):
        """Creating summary plots"""
        period = ['hour', 'month', 'year']
        for i, ax in enumerate(self.fig.axes):
            sns.pointplot(data=df,
                          x=period[i],
                          y='dni',
                          ax=ax,
                          color=c,
                          ci=None)
        self.set_properties()