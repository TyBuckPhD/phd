import osimport numpy as npimport matplotlib.pyplot as pltfrom matplotlib.patches import FancyArrowPatchclass FlowPlotter:    """    Class for generating flow field analysis plots using a multi-panel figure.    This class creates a figure with 8 subplots arranged in a 4x2 grid. Each subplot is configured    to display different aspects of flow dynamics, including:      - Stable and unstable flow fields,      - Vorticity (first derivative of the flow field),      - Curvature (second derivative of the flow field), and      - Fjørtoft's instability criterion.    The class sets up a consistent plotting framework with annotated axes, custom arrow indicators,    and predefined labels for clarity. The flow fields are generated using mathematical functions,    and additional markers and arrows indicate key flow properties.    Attributes:      fig (Figure): The matplotlib figure object.      axes (ndarray): Flattened array of matplotlib Axes objects for the subplots.      labels (list of str): List of subplot labels (e.g., ['(a)', '(b)', ..., '(h)']).      y_labels (list of str): List of y-axis labels for the subplots.      markersize (int): Size of the marker symbols used in the plots.    Methods:      create_plot_framework:          Sets up the plot framework by configuring axis limits, adding directional arrows, axis labels,          and subplot annotations.      plot_flow_inflection_stable:          Generates data for a stable flow field based on an inflection profile.      plot_flow_inflection_unstable:          Generates data for an unstable flow field based on an inflection profile.      add_flow_arrows:          Adds arrows to a given axis at integer x-values to indicate the flow direction.      plot_vorticity:          Computes and plots vorticity (first derivative of the flow velocity) on the specified axis.      plot_curvature:          Computes and plots curvature (second derivative of the flow velocity) on the specified axis.      plot_fjortoft_criterion:          Plots the Fjørtoft instability criterion based on the flow velocity and its curvature.      plot_all:          Generates all subplots by calling the appropriate methods for each flow field analysis and          displays or saves the final figure.    """    def __init__(self):        self.fig, self.axes = plt.subplots(            4, 2, figsize=(6, 10), constrained_layout=True        )        self.axes = self.axes.ravel()  # Flatten axes for easier iteration        self.labels = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)"]        self.y_labels = [            r"$\bar{v}$",            r"$\bar{v}$",            r"$\omega_z$",            r"$\omega_z$",            "R",            "R",            "F",            "F",        ]        self.create_plot_framework()        self.markersize = 8    def create_plot_framework(self):        """Sets up the plot framework with axis labels and limits."""        for idx, ax in enumerate(self.axes):            if idx < 2:                ax.set_xlim(0, 10)                ax.set_ylim(0, 10)                ax.annotate(                    "",                    xy=(1.05, 0),                    xycoords="axes fraction",                    xytext=(-0.05, 0),                    arrowprops=dict(arrowstyle="->", lw=1.5),                )                ax.annotate(                    "",                    xy=(0, 1.05),                    xycoords="axes fraction",                    xytext=(0, -0.05),                    arrowprops=dict(arrowstyle="->", lw=1.5),                )                ax.text(                    0.95,                    -0.1,                    "x",                    transform=ax.transAxes,                    fontsize=14,                    ha="center",                )                ax.text(                    -0.07,                    0.50,                    self.y_labels[idx],                    transform=ax.transAxes,                    fontsize=14,                    ha="center",                    va="center",                )            else:                ax.set_xlim(-5, 5)                ax.set_ylim(-5, 5)                ax.annotate(                    "",                    xy=(1.05, 0.5),                    xycoords="axes fraction",                    xytext=(-0.05, 0.5),                    arrowprops=dict(arrowstyle="->", lw=1.5),                )                ax.annotate(                    "",                    xy=(0.5, 1.05),                    xycoords="axes fraction",                    xytext=(0.5, -0.05),                    arrowprops=dict(arrowstyle="->", lw=1.5),                )                ax.text(                    0.95,                    0.4,                    "x",                    transform=ax.transAxes,                    fontsize=14,                    ha="center",                )                ax.text(                    0.60,                    0.96,                    self.y_labels[idx],                    transform=ax.transAxes,                    fontsize=14,                    ha="center",                    va="center",                )            ax.set_aspect("equal")            ax.set_xticks([])            ax.set_yticks([])            ax.spines["top"].set_visible(False)            ax.spines["right"].set_visible(False)            ax.spines["left"].set_visible(False)            ax.spines["bottom"].set_visible(False)            ax.text(                -0.23,                0.9,                self.labels[idx],                transform=ax.transAxes,                fontsize=16,                fontweight="bold",            )    def plot_flow_inflection_stable(self):        """Generates data for the stable flow field."""        x_values = np.linspace(1, 9, 200)        v_values = 5 + (            np.tan((x_values - 5) / 2.8) / 1.5        )  # Stable flow field        return x_values, v_values    def plot_flow_inflection_unstable(self):        """Generates data for the unstable flow field."""        x_values = np.linspace(1, 9, 200)        v_values = 5 + 3.2 * np.arctan(            1.5 * (x_values - 5)        )  # Unstable flow field        return x_values, v_values    def add_flow_arrows(self, ax, x_points, v_values, scale=0.9):        """Adds arrows at integer x-values pointing up to scaled-down v-values to represent flow direction."""        for i in range(2, 9):            v_at_i = v_values[np.abs(x_points - i).argmin()] * scale            arrow = FancyArrowPatch(                (i, 0),                (i, v_at_i),                color="black",                lw=1.2,                arrowstyle="-|>",                mutation_scale=10,            )            ax.add_patch(arrow)    def plot_vorticity(self, ax, x, v):        """Plots vorticity as the first derivative of v with respect to x."""        dv_dx = np.gradient(v, x) * 0.9        ax.plot(x - 5, dv_dx, color="black", lw=2)        ax.plot(            0, dv_dx[len(dv_dx) // 2], "ko", markersize=self.markersize        )  # Use self.markersize    def plot_curvature(self, ax, x, v):        """Plots curvature as the second derivative of v with respect to x."""        dv_dx = np.gradient(v, x)        d2v_dx2 = np.gradient(dv_dx, x)        ax.plot(x - 5, d2v_dx2, color="black", lw=2)        ax.plot(0, 0, "ko", markersize=self.markersize)  # Use self.markersize        return d2v_dx2    def plot_fjortoft_criterion(self, ax, x, v, d2v_dx2):        """Plots the Fjørtoft instability criterion."""        inflection_velocity = v[            len(v) // 2        ]  # Velocity at the inflection point        fjortoft = d2v_dx2 * (v - inflection_velocity) * 0.5        ax.plot(x - 5, fjortoft, color="black", lw=2)        ax.plot(0, 0, "ko", markersize=self.markersize)  # Use self.markersize    def plot_all(self):        """Plots all subplots with the respective flow fields, vorticity, curvature, and Fjørtoft criterion."""        # Plot flow fields        x_stable, v_stable = self.plot_flow_inflection_stable()        x_unstable, v_unstable = self.plot_flow_inflection_unstable()        # Stable flow in (a)        self.axes[0].plot(x_stable, v_stable, color="black", lw=2)        self.axes[0].plot(5, 5, "ko", markersize=self.markersize)        self.add_flow_arrows(self.axes[0], x_stable, v_stable)        # Unstable flow in (b)        self.axes[1].plot(x_unstable, v_unstable, color="black", lw=2)        self.axes[1].plot(5, 5, "ko", markersize=self.markersize)        self.add_flow_arrows(self.axes[1], x_unstable, v_unstable)        # Vorticity plots (c) and (d)        self.plot_vorticity(self.axes[2], x_stable, v_stable)        self.plot_vorticity(self.axes[3], x_unstable, v_unstable)        # Curvature plots (e) and (f)        d2v_dx2_stable = self.plot_curvature(self.axes[4], x_stable, v_stable)        d2v_dx2_unstable = self.plot_curvature(            self.axes[5], x_unstable, v_unstable        )        # Fjørtoft's criterion plots (g) and (h)        self.plot_fjortoft_criterion(            self.axes[6], x_stable, v_stable, d2v_dx2_stable        )        self.plot_fjortoft_criterion(            self.axes[7], x_unstable, v_unstable, d2v_dx2_unstable        )        # Display or save figure        script_dir = os.path.dirname(os.path.abspath(__file__))        fig_filename = os.path.join(script_dir, "../figures/figure_04.png")        plt.savefig(            fig_filename, dpi=200, bbox_inches="tight", pad_inches=0.05        )        plt.show()# Run the FlowPlotter classif __name__ == "__main__":    plotter = FlowPlotter()    plotter.plot_all()