import numpy as np


class KalmanFilter(object):
    def __init__(self, F=None, B=None, H=None, Q=None, R=None, P=None, x0=None):

        if F is None or H is None:
            raise ValueError("Set proper system dynamics.")

        self.n = F.shape[1]  # Steps ahead
        self.m = H.shape[1]

        self.F = F
        self.H = H
        self.B = 0 if B is None else B
        self.Q = np.eye(self.n) if Q is None else Q
        self.R = np.eye(self.n) if R is None else R
        self.P = np.eye(self.n) if P is None else P
        # self.x is the state
        self.x = np.zeros((self.n, 1)) if x0 is None else x0

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


        z = observations

        
        predictions_state = [self.x]
        predictions_obs = []
        predictions_cov = [self.P]

        for z in observations:
            z = z.reshape(self.m, 1)
            if np.isnan(z).any():# all the missing values
                
                if not predictions_state: #if predictions are empty, meaning that the first observation is empty i.e. the first va
                    z = np.array(np.full(self.m,2)).reshape(self.m,1)
                else:
                    expected_mean = np.random.normal(predictions_state[-1],predictions_cov[-1]) # sampling from the last observed step
                    z = self.H @ expected_mean #from latent to observed state

            self.update(z)
            predictions_dummy, prediction_dummy_cov = self.predict()
            predictions_obs.append(self.H @ predictions_dummy)
            predictions_state.append(predictions_dummy)
            predictions_cov.append(prediction_dummy_cov)

        return predictions_state, predictions_cov, predictions_obs

    def smooth(self, predictions_state, predictions_cov):

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

        return x_smooth, P_smooth, K  #    -> what do we do with K?
