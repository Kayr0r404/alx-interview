#!/usr/bin/python3


from collections import deque

def canUnlockAll(boxes):
    if not boxes or len(boxes) == 0:
        return False
    
    n = len(boxes)
    visited = [False] * n
    visited[0] = True  # Mark the first box (index 0) as visited
    queue = deque([0])  # Start BFS traversal from the first box
    
    while queue:
        current_box = queue.popleft()
        keys = boxes[current_box]
        
        for key in keys:
            if 0 <= key < n and not visited[key]:
                visited[key] = True
                queue.append(key)
    
    # Check if all boxes have been visited
    return all(visited)
