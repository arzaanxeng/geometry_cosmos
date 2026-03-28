"""
geometry.py
-----------
Core classes for 2D geometry calculations:
  - Point             : distance between two points
  - Geometry          : line-line intersection and parallel-line distance
  - GeometryAnalyzer  : circle-line relationship and intersection
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class Point:
    x1: float
    y1: float
    x2: float
    y2: float

    def point_distance(self) -> float:
        distance = float(np.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2))
        return round(distance, 4)


class Geometry:
    def __init__(self, a1, b1, c1, a2, b2, c2):
        self.a1, self.b1, self.c1 = a1, b1, c1
        self.a2, self.b2, self.c2 = a2, b2, c2

    def line_intersection(self):
        denom = self.a2*self.b1 - self.a1*self.b2
        if denom == 0:
            raise ZeroDivisionError("Lines are parallel.")
        x = (self.b2*self.c1 - self.b1*self.c2) / denom
        y = (self.a1*self.c2 - self.a2*self.c1) / (self.b1*self.a2 - self.a1*self.b2)
        return round(x, 4), round(y, 4)

    def parallel_line_distance(self):
        return round(float(np.abs(self.c1-self.c2)/np.sqrt(self.a1**2+self.b1**2)), 4)

    def plot(self, save_path="lines.png"):
        x = np.linspace(-10, 10, 400)
        y1 = (-self.a1*x - self.c1)/self.b1
        y2 = (-self.a2*x - self.c2)/self.b2
        fig, ax = plt.subplots()
        ax.plot(x, y1, label="Line 1", color="red")
        ax.plot(x, y2, label="Line 2", color="goldenrod", linestyle=":")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend()
        fig.tight_layout()
        fig.savefig(save_path)
        plt.show()
        plt.close(fig)


class GeometryAnalyzer:
    def __init__(self, a1, b1, r, a2, b2, c2):
        if r <= 0:
            raise ValueError(f"Radius must be positive, got {r}.")
        self.a1, self.b1, self.r = a1, b1, r
        self.a2, self.b2, self.c2 = a2, b2, c2

    def _perpendicular_distance(self):
        return float(
            np.abs(self.a2*self.a1 + self.b2*self.b1 + self.c2)
            / np.sqrt(self.a2**2 + self.b2**2)
        )

    def _relationship(self):
        dist = self._perpendicular_distance()
        if np.isclose(dist, self.r, atol=1e-5):
            return "TANGENT (1 point)", "orange"
        if dist < self.r:
            return "SECANT (2 points)", "green"
        return "NO INTERSECTION", "red"

    def get_intersection_points(self):
        if self.b2 == 0:
            x_fixed = -self.c2 / self.a2
            dist_sq = (x_fixed - self.a1)**2
            if dist_sq > self.r**2:
                return []
            y_offset = float(np.sqrt(self.r**2 - dist_sq))
            if np.isclose(y_offset, 0, atol=1e-9):
                return [(round(x_fixed, 2), round(float(self.b1), 2))]
            return [
                (round(x_fixed, 2), round(float(self.b1 + y_offset), 2)),
                (round(x_fixed, 2), round(float(self.b1 - y_offset), 2)),
            ]

        slope = -self.a2 / self.b2
        intercept = -self.c2 / self.b2
        A = 1 + slope**2
        B = 2*(slope*(intercept - self.b1) - self.a1)
        C = self.a1**2 + (intercept - self.b1)**2 - self.r**2

        discriminant = B**2 - 4*A*C
        if discriminant < 0:
            return []

        sqrt_d = float(np.sqrt(discriminant))
        x1 = (-B + sqrt_d) / (2*A)
        x2 = (-B - sqrt_d) / (2*A)

        if np.isclose(x1, x2, atol=1e-9):
            x1 = float(x1)
            return [(round(x1, 2), round(float(slope*x1 + intercept), 2))]

        return [
            (round(float(x), 2), round(float(slope*x + intercept), 2))
            for x in (x1, x2)
        ]

    def analyze_geometry(self, save_path=None):
        status, color = self._relationship()
        intersections = self.get_intersection_points()

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.add_patch(plt.Circle((self.a1, self.b1), self.r, color="blue", fill=False, lw=2))

        margin = self.r + 3
        x_range = np.linspace(self.a1 - margin, self.a1 + margin, 400)
        if self.b2 != 0:
            ax.plot(x_range, (-self.a2*x_range - self.c2)/self.b2, color=color, label=status)
        else:
            ax.axvline(-self.c2/self.a2, color=color, label=status)

        for px, py in intersections:
            ax.plot(px, py, "ro", markersize=10, markeredgecolor="black", zorder=5)
            ax.annotate(f"({px}, {py})", (px, py), xytext=(6, 6), textcoords="offset points", fontsize=9)

        ax.set_aspect("equal")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend()
        ax.set_title(f"Geometry Report: {status}")

        fname = save_path or f"geometry_{status.split()[0].lower()}.png"
        fig.savefig(fname, dpi=150)
        plt.show()
        plt.close(fig)

        print(f"\nAnalysis complete — {status}")
        print(f"Intersection point(s): {intersections if intersections else 'none'}")
