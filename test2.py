import numpy as np

def find_k_nearest_neighbors(IDEAL, ALL_ARRAYS, k):
    # Step 1: Calculate the distances
    distances = np.linalg.norm(ALL_ARRAYS - IDEAL, axis=1)
    
    # Step 2: Find the indices of the k smallest distances
    k_indices = np.argpartition(distances, k)[:k]
    
    # Step 3: Sort the k smallest distances
    k_sorted_indices = k_indices[np.argsort(distances[k_indices])]
    
    # Step 4: Retrieve the k nearest neighbors
    K_MATCHES = ALL_ARRAYS[k_sorted_indices]
    
    return K_MATCHES

# Example usage
IDEAL = np.array([1, 2, 3])
ALL_ARRAYS = np.array([[1, 2, 3], [1, 1, 2], [4, 5, 6], [7, 8, 9], [2, 3, 4], [5, 6, 7]])
k = 3

K_MATCHES = find_k_nearest_neighbors(IDEAL, ALL_ARRAYS, k)
print("K nearest neighbors:\n", K_MATCHES)
