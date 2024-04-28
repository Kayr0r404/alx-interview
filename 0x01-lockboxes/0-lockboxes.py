def canUnlockAll(boxes):
    keys = set(())
    for box in boxes:
        for key in box:
            keys.add(key)
    for key in keys:
        pass
    return keys


boxes = [[1, 4], [2], [0, 4, 1], [3], [], [4, 1], [5, 6]]
print(canUnlockAll(boxes))
