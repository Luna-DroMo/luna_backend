import numpy as np
import pandas as pd


class KalmanFilterConfig:
    F = np.array([[1]])  # State transition matrix
    Q = np.array([[0.01]])  # Process noise covariance matrix
    R = (
        np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]]) * 0.02
    )  # Measurement noise covariance matrix
    x0 = np.array([[0]])  # Initial state estimate
    H = np.array([[2.05169581], [2.40295494], [2.0302588]])  # Observation matrix


class KalmanFilter(KalmanFilterConfig):
    def __init__(self, F=None, B=None, H=None, Q=None, R=None, P=None, x0=None):

        if F is None or H is None:
            raise ValueError("Set proper system dynamics.")

        self.n = F.shape[1]
        self.m = H.shape[1]

        self.F = F
        self.H = H
        self.B = 0 if B is None else B
        self.Q = np.eye(self.n) if Q is None else Q
        self.R = np.eye(self.n) if R is None else R
        self.P = np.eye(self.n) if P is None else P
        self.x = np.zeros((self.n, 1)) if x0 is None else x0
        self.predictions = np.array([])

    def predict(self, u=0):
        self.x = self.F @ self.x + self.B + u
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x, self.P

    def update(self, z):
        y = z - self.H @ self.x
        S = self.R + self.H @ self.P @ self.H.T
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        I = np.eye(self.n)
        self.P = (I - K @ self.H) @ self.P @ (I - K @ self.H).T + K @ self.R @ K.T

    def forward(self, observations):
        # Runs the forward algorithm based on observations
        self.predictions_state = []
        self.predictions_obs = []
        self.predictions_cov = []

        for z in observations.T:
            if np.isnan(z).any():
                if (
                    not self.predictions_state
                ):  # If the first observation is missing, use an arbitrary value
                    z = np.array([[2], [2], [2]])
            else:
                expected_mean = np.random.normal(
                    self.predictions_state[-1], self.predictions_cov[-1]
                )  # sampling from the last observed step
                z = self.H @ expected_mean  # from latent to observed state

            z = z.reshape(3, 1)
            self.predictions_obs.append(self.H @ self.predict()[0])
            self.predictions_state.append(self.predict()[0])
            self.predictions_cov.append(self.predict()[1])
            self.update(z)

        return self.predictions_state, self.predictions_cov, self.predictions_obs

    def rts_smoother(self, predictions_state, predictions_cov):
        predictions_state = np.array(predictions_state)
        predictions_cov = np.array(predictions_cov)
        n, dim_x, _ = predictions_state.shape
        # RTS smoother gain
        K = np.zeros((n, dim_x, dim_x))
        x_smooth = np.zeros((n, dim_x, 1))
        P_smooth = np.zeros((n, dim_x, dim_x))

        x_smooth[-1] = predictions_state[-1]
        P_smooth[-1] = predictions_cov[-1]

        for k in range(n - 2, -1, -1):
            P_pred = np.dot(np.dot(self.F, predictions_cov[k]), self.F.T) + self.Q

            K[k] = np.dot(np.dot(predictions_cov[k], self.F.T), np.linalg.inv(P_pred))
            x_smooth[k] = predictions_state[k] + np.dot(
                K[k], x_smooth[k + 1] - np.dot(self.F, predictions_state[k])
            )
            P_smooth[k] = predictions_cov[k] + np.dot(
                np.dot(K[k], P_smooth[k + 1] - P_pred), K[k].T
            )

        return x_smooth, P_smooth, K
