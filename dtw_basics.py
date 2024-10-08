import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Euclidean distance function
def euclidean_dist(x, y):
    return np.abs(x - y)

# Dynamic Time Warping function
def dtw(X, Y):
    N, M = len(X), len(Y)
    cost = np.zeros((N, M))

    # Initialize cost matrix
    cost[0, 0] = euclidean_dist(X[0], Y[0])
    for i in range(1, N):
        cost[i, 0] = cost[i-1, 0] + euclidean_dist(X[i], Y[0])
    for j in range(1, M):
        cost[0, j] = cost[0, j-1] + euclidean_dist(X[0], Y[j])

    # Populate cost matrix
    for i in range(1, N):
        for j in range(1, M):
            choices = [cost[i-1, j], cost[i, j-1], cost[i-1, j-1]]
            cost[i, j] = euclidean_dist(X[i], Y[j]) + min(choices)

    # Backtrack to find the warping path
    path = []
    i, j = N-1, M-1
    while i > 0 or j > 0:
        path.append((i, j))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            move = np.argmin([cost[i-1, j], cost[i, j-1], cost[i-1, j-1]])
            if move == 0:
                i -= 1
            elif move == 1:
                j -= 1
            else:
                i -= 1
                j -= 1
    path.append((0, 0))
    path.reverse()
    
    return cost, path

# Align the signals based on the warping path
def align_signals(X, Y, path):
    aligned_X = []
    aligned_Y = []
    for (i, j) in path:
        aligned_X.append(X[i])
        aligned_Y.append(Y[j])
    return np.array(aligned_X), np.array(aligned_Y)

# Plot the results
def plot_dtw(X, Y, cost, path, aligned_X, aligned_Y):
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))

    # Plot time series
    ax[0].plot(X, label="Time Series X", color='blue')
    ax[0].plot(Y, label="Time Series Y", color='orange')
    ax[0].legend()
    ax[0].set_title("Time Series Comparison")

    # Plot cost matrix and warping path
    ax[1].imshow(cost, origin='lower', cmap='viridis', norm=LogNorm())
    ax[1].plot([j for i, j in path], [i for i, j in path], color='red')  # warping path
    ax[1].set_title("Cost Matrix with Warping Path")
    ax[1].set_xlabel("Time Series Y")
    ax[1].set_ylabel("Time Series X")

    # Plot aligned signals
    ax[2].plot(aligned_X, label="Aligned Time Series X", color='blue')
    ax[2].plot(aligned_Y, label="Aligned Time Series Y", color='orange')
    ax[2].set_title("Aligned Signals")
    ax[2].legend()

    plt.tight_layout()
    plt.show()

# Sample time series
X = np.sin(np.linspace(0, 3 * np.pi, 50))  # Sine wave
Y = np.sin(np.linspace(0, 2 * np.pi, 40) + 0.5)  # Shifted sine wave

# Compute DTW, align signals, and visualize
cost, path = dtw(X, Y)
aligned_X, aligned_Y = align_signals(X, Y, path)
plot_dtw(X, Y, cost, path, aligned_X, aligned_Y)
