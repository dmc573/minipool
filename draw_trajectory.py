def draw_trajectory(direction, speed, ball_center, trajectory_indicators):
    interval = [speed/5.*math.cos(direction), speed/5.*math.sin(direction)]
    centers = []
    for i in range(1,6):
        centers.append(add_vectors(ball_center, scalar_product(i, interval)))
    for i in range(len(trajectory_indicators)):
        canvas.delete(trajectory_indictors[i])
        trajectory_indicators.pop(i)