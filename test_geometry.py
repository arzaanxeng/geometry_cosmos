"""
tests/test_geometry.py
----------------------
Unit tests for geometry.py.

Run:
    pytest tests/ -v
"""

import pytest
import numpy as np
from geometry import Geometry, GeometryAnalyzer, Point


class TestPoint:
    def test_basic_345_triangle(self):
        assert Point(0, 0, 3, 4).point_distance() == 5.0

    def test_same_point_is_zero(self):
        assert Point(2, 2, 2, 2).point_distance() == 0.0

    def test_horizontal(self):
        assert Point(0, 0, 5, 0).point_distance() == 5.0

    def test_vertical(self):
        assert Point(0, 0, 0, 7).point_distance() == 7.0

    def test_negative_coords(self):
        assert Point(-1, -1, 2, 3).point_distance() == pytest.approx(5.0, abs=1e-3)

    def test_float_diagonal(self):
        assert Point(0, 0, 1, 1).point_distance() == pytest.approx(np.sqrt(2), abs=1e-4)


class TestGeometry:
    def test_intersection_basic(self):
        # x+y-1=0 and x-y+1=0 → (0, 1)
        assert Geometry(1, 1, -1, 1, -1, 1).line_intersection() == (0.0, 1.0)

    def test_intersection_at_origin(self):
        # y=0 and x=0 → (0, 0)
        assert Geometry(0, 1, 0, 1, 0, 0).line_intersection() == (0.0, 0.0)

    def test_parallel_raises(self):
        with pytest.raises(ZeroDivisionError):
            Geometry(1, 1, 1, 1, 1, 3).line_intersection()

    def test_parallel_distance(self):
        # x+y+1=0 and x+y+5=0 → 4/sqrt(2)
        assert Geometry(1, 1, 1, 1, 1, 5).parallel_line_distance() == pytest.approx(4/np.sqrt(2), abs=1e-3)

    def test_coincident_distance_is_zero(self):
        assert Geometry(2, 3, 6, 2, 3, 6).parallel_line_distance() == 0.0


class TestGeometryAnalyzer:
    def test_invalid_radius_raises(self):
        with pytest.raises(ValueError):
            GeometryAnalyzer(0, 0, -1, 1, 0, -5)

    def test_zero_radius_raises(self):
        with pytest.raises(ValueError):
            GeometryAnalyzer(0, 0, 0, 1, 0, -5)

    def test_secant_vertical_line(self):
        # Circle (0,0) r=5, line x=0 → (0,5) and (0,-5)
        pts = GeometryAnalyzer(0, 0, 5, 1, 0, 0).get_intersection_points()
        assert len(pts) == 2

    def test_no_intersection(self):
        # Circle (0,0) r=1, line x=10
        assert GeometryAnalyzer(0, 0, 1, 1, 0, -10).get_intersection_points() == []

    def test_tangent_returns_one_point(self):
        # Circle (0,0) r=5, line x=5 → tangent at (5,0)
        pts = GeometryAnalyzer(0, 0, 5, 1, 0, -5).get_intersection_points()
        assert len(pts) == 1
        assert pts[0] == (5.0, 0.0)

    def test_secant_general_line_two_points(self):
        # Circle (1,1) r=5, horizontal line y=1 (0x+1y-1=0) → 2 pts with y≈1
        pts = GeometryAnalyzer(1, 1, 5, 0, 1, -1).get_intersection_points()
        assert len(pts) == 2
        for _, py in pts:
            assert py == pytest.approx(1.0, abs=0.1)

    def test_perpendicular_distance_through_centre(self):
        # Line 3x+4y+0=0 through (0,0) → distance = 0
        analyzer = GeometryAnalyzer(0, 0, 5, 3, 4, 0)
        assert analyzer._perpendicular_distance() == pytest.approx(0.0, abs=1e-6)

    def test_relationship_secant(self):
        status, _ = GeometryAnalyzer(0, 0, 5, 1, 0, 0)._relationship()
        assert "SECANT" in status

    def test_relationship_no_intersection(self):
        status, _ = GeometryAnalyzer(0, 0, 1, 1, 0, -10)._relationship()
        assert "NO INTERSECTION" in status
