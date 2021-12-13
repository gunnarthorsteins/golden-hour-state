class DistCalc():
    """Class created for reproducibility and multiple calls to dataframe"""

    def __init__(self):
        N = len(locs)
        self.df = pd.DataFrame(np.zeros((N, N))) 

    def calc_dist(self, coordsA, coordsB):
        """For convenience if
        also using horizontal & vertical distances
        """

        dist = geopy.distance.geodesic((coordsA),
                                       (coordsB))
        self.df.iloc[i, j] = round(dist.kilometers)
        self.df.rename(columns={i: keyA},
                       index={j: keyB},
                       inplace=True)
    
dist_L2 = DistCalc()
dist_vert = DistCalc()
dist_hori = DistCalc()
for i, (keyA, valA) in enumerate(locs.items()):
    for j, (keyB, valB) in enumerate(locs.items()):
        # [::-1] b/c 'geodesic' reads lat/lon but ours is lon/lat
        dist_L2.calc_dist(valA[::-1],  valB[::-1])
        dist_vert.calc_dist((valA[1], 0), (valB[1], 0))
        # Strictly speaking, dist between longitude lines is a function
        # of latitude, but we approximate lat as 37
        dist_hori.calc_dist((37, valA[0]), (37, valB[0]))


class DistCorr():
    """Creates a distance correlation plot + regression"""

    def __init__(self, df, ax, L, const_color=True):
        self.df = df
        self.xy = np.zeros((N*(N-1), 2))  # -1 b/c we omit the diagonals
        self.k = 0
        self.const_color = const_color

        self.ax = ax
        self.ax.set_xlim([0, 1200])
        self.ax.set_ylim([0, 1])
        self.ax.grid(zorder=1)
        self.ax.set_ylabel('Correlation')
        self.ax.set_xlabel(f'{L} distance [km]')

    def corr_dist(self, i, j):
        """Calculates the distance correlation"""

        c = colors['BLUE'] if self.const_color else self.c_col(i, j)

        self.xy[self.k, :] = [self.df.iloc[i,j], df_corr.iloc[i,j]]
        self.ax.scatter(self.df.iloc[i,j], df_corr.iloc[i,j],
                       facecolors='none', edgecolors=c, zorder=3)
        self.k += 1
    
    def c_col(self, i, j):
        """Determines scatter point color based on proximity to sea"""

        c = colors['BLUE']
        if any(self.df.columns[i] == sea for sea in seaside):
            if any(self.df.index[j] == sea for sea in seaside):
                c = 'r'
            else:
                c = 'g'
        elif any(self.df.columns[j] == sea for sea in seaside):
            if any(self.df.index[i] == sea for sea in seaside):
                c = 'r'
            else:
                c = 'g'        
        else:
            pass

        return c

    def lin_regr(self):
        """Executes linear regression"""

        x = self.xy[:, 0]
        y = self.xy[:, 1]
        p = np.polyfit(x, y, deg=1)
        x_r = np.linspace(min(x), max(x))
        y_r = np.polyval(p, x_r)
        self.ax.plot(x_r, y_r, c=colors['BLUE'], zorder=2)
    
    def get_xy(self):
        """Creates a dataframe for model diagnostics"""

        self.xy = self.xy[self.xy[:, 0].argsort()]  # Sort by the first column (ascending)
        self.xy = pd.DataFrame(self.xy, columns=['distance', 'correlation'])
        return self.xy