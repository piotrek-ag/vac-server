# Simple ID generation
def generate_id(data):
    return max([0] + [item['id'] for item in data]) + 1
