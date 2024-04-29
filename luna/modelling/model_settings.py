import numpy as np

F = np.array([[1]])  # Assuming no change in state


Q = np.array(
    [[0.01]]
)  # Adjust the value as per your system dynamics and noise characteristics

R = (
    np.array(
        [
            [2, 0, 0],  # Covariance of the first observation
            [0, 2, 0],  # Covariance of the second observation
            [0, 0, 2],
        ]
    )
    * 0.02
)  # Covariance of the third observation
x0 = np.array([[0]])  # Initial state estimates

H = np.array([[2.05169581], [2.40295494], [2.0302588]])
