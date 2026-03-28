"""
main.py
-------
Interactive CLI for Geometry Cosmos.

Run:
    python main.py
"""

from geometry import Geometry, GeometryAnalyzer, Point

DIVIDER = "=" * 42


def prompt_float(label: str) -> float:
    while True:
        try:
            return float(input(f"  {label}: "))
        except ValueError:
            print("  [!] Invalid input — please enter a number.")


def handle_lines() -> None:
    print("\nLine 1  (a1·x + b1·y + c1 = 0)")
    a1 = prompt_float("a1"); b1 = prompt_float("b1"); c1 = prompt_float("c1")
    print("\nLine 2  (a2·x + b2·y + c2 = 0)")
    a2 = prompt_float("a2"); b2 = prompt_float("b2"); c2 = prompt_float("c2")

    geo = Geometry(a1, b1, c1, a2, b2, c2)
    if a1*b2 == a2*b1:
        if a1*c2 == a2*c1:
            print("\n  Lines are COINCIDENT (identical).")
        else:
            print(f"\n  Lines are PARALLEL.  Distance = {geo.parallel_line_distance()}")
            geo.plot(save_path="lines_parallel.png")
    else:
        print(f"\n  Intersection point: {geo.line_intersection()}")
        geo.plot(save_path="lines_intersecting.png")


def handle_points() -> None:
    print("\nPoint 1"); x1 = prompt_float("x1"); y1 = prompt_float("y1")
    print("\nPoint 2"); x2 = prompt_float("x2"); y2 = prompt_float("y2")
    print(f"\n  Distance between points: {Point(x1, y1, x2, y2).point_distance()}")


def handle_circle_line() -> None:
    print("\nCircle  ((x − a)² + (y − b)² = r²)")
    a1 = prompt_float("Centre x  (a)"); b1 = prompt_float("Centre y  (b)")
    while True:
        r = prompt_float("Radius    (r)")
        if r > 0: break
        print("  [!] Radius must be positive.")
    print("\nLine  (a·x + b·y + c = 0)")
    a2 = prompt_float("a"); b2 = prompt_float("b"); c2 = prompt_float("c")
    GeometryAnalyzer(a1, b1, r, a2, b2, c2).analyze_geometry()


MENU = """
  1 — Line–line  (intersection / parallel distance)
  2 — Point–point  (Euclidean distance)
  3 — Circle–line  (tangent / secant / none)
  0 — Quit
"""

HANDLERS = {1: handle_lines, 2: handle_points, 3: handle_circle_line}


def main() -> None:
    print(DIVIDER)
    print("        Welcome to Geometry Cosmos")
    print(DIVIDER)
    print("  All lines use the form:  ax + by + c = 0")

    while True:
        print(MENU)
        try:
            choice = int(input("  Your choice: "))
        except ValueError:
            print("  [!] Please enter a number."); continue

        if choice == 0:
            print("\n  Goodbye!\n"); break

        handler = HANDLERS.get(choice)
        if handler is None:
            print("  [!] Invalid option — choose 0, 1, 2, or 3."); continue

        try:
            handler()
        except Exception as exc:
            print(f"\n  [!] Error: {exc}")

        if input("\n  Continue? (y / n): ").strip().lower() != "y":
            print("\n  Goodbye!\n"); break


if __name__ == "__main__":
    main()
