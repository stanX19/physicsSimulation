import math


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def closest_point_to(self, x, y):
        # variables
        x3, y3 = x, y

        # Calculate the vector components of the line segment
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        # Calculate the squared length of the line segment
        line_length_squared = dx ** 2 + dy ** 2

        # Avoid division by zero if the line segment has no length
        if line_length_squared == 0:
            return math.sqrt((x3 - self.x1) ** 2 + (y3 - self.y1) ** 2)

        # Calculate the parametric value (t) for the point on the line closest to the given point
        t = max(0, min(1, ((x3 - self.x1) * dx + (y3 - self.y1) * dy) / line_length_squared))

        # Calculate the closest point on the line
        closest_x = self.x1 + t * dx
        closest_y = self.y1 + t * dy

        return closest_x, closest_y

    def shortest_distance_from(self, x, y):
        closest_x, closest_y = self.closest_point_to(x, y)
        distance = math.hypot(x - closest_x, y - closest_y)
        return distance

    def check_line_intersection(self, x3, y3, x4, y4):
        # Calculate the denominator for the intersection calculation
        denominator = (self.x1 - self.x2) * (y3 - y4) - (self.y1 - self.y2) * (x3 - x4)

        # Check if the lines are parallel or coincident
        if denominator == 0:
            return None

        # Calculate the numerator values for the intersection calculation
        numerator_1 = (self.x1 * self.y2 - self.y1 * self.x2) * (x3 - x4) - (self.x1 - self.x2) * (x3 * y4 - y3 * x4)
        numerator_2 = (self.x1 * self.y2 - self.y1 * self.x2) * (y3 - y4) - (self.y1 - self.y2) * (x3 * y4 - y3 * x4)

        # Calculate the intersection coordinate
        intersection_x = numerator_1 / denominator
        intersection_y = numerator_2 / denominator

        # Line segments range
        x1_min, x1_max = min(self.x1, self.x2), max(self.x1, self.x2)
        y1_min, y1_max = min(self.y1, self.y2), max(self.y1, self.y2)
        x2_min, x2_max = min(x3, x4), max(x3, x4)
        y2_min, y2_max = min(y3, y4), max(y3, y4)

        # Check if the intersection point is within the line segments
        if (x1_min <= intersection_x <= x1_max and
                y1_min <= intersection_y <= y1_max and
                x2_min <= intersection_x <= x2_max and
                y2_min <= intersection_y <= y2_max):
            return intersection_x, intersection_y

        return None


if __name__ == '__main__':
    l1 = Line(19, 13, -2000, 1000)
    print(l1.check_line_intersection(20, 19, 1000, -5000))
