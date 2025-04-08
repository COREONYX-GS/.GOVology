import os
import random
import json
import pandas as pd

import math

def grid_dimensions(count, aspect_ratio=(16, 9), buffer=1.0):
    """
    Calculate grid dimensions (max_x, max_y) for a given number of items.

    Args:
        count (int): Total number of items.
        aspect_ratio (tuple): Desired aspect ratio as (width, height).
        buffer (float): Buffer factor to increase the count (default is 1.0 for no extra buffer).

    Returns:
        tuple: (max_x, max_y) dimensions of the grid.
    """
    # Adjust count for buffer if needed
    adjusted_count = count * buffer
    # Calculate the ratio as width/height (e.g., 16/9)
    ratio = aspect_ratio[0] / aspect_ratio[1]
    
    # Calculate grid dimensions using the derived formula
    max_x = math.ceil(math.sqrt(adjusted_count * ratio))
    max_y = math.ceil(math.sqrt(adjusted_count / ratio))
    
    return max_x, max_y

def generate_data(FILE_IN):
    data = []
    df = pd.read_csv(FILE_IN)
    count, _ = df.shape
    max_x, max_y = grid_dimensions(count, aspect_ratio=(16, 9), buffer=1.2)
    cur_x, cur_y = 0, 0

    df = df.sort_values(by="Agency")
    for _, row in df.iterrows():
        domain = row.get("Domain name", "").strip().replace(".gov", "").lower()
        if domain:  # Generate random coordinates in some bounding range
            x = cur_x
            y = cur_y

            # You can store any additional fields you like;
            # for now, we'll just keep domain, x, y
            data.append({
                "domain": domain,
                "agency": row.get("Agency", "").strip(),
                "org": row.get("Organization name", "").strip(),
                "x": x,
                "y": y
            })

            print(f"{domain} -> x: {x}, y: {y} (max_x: {max_x}, max_y: {max_y})")

            cur_y += 1
            if cur_y >= max_y:
                cur_y = 0
                cur_x += 1

            if cur_x > max_x:
                print("Warning: Exceeded grid dimensions!")

    return data

def save_data(data, json_filename = "gov-elements.json"):
    with open(json_filename, 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=4)
    
if __name__ == "__main__":
    DATA_FILE_IN = os.getenv("DATA_FILE_IN", "data/federal-domains.csv")
    DATA_FILE_OUT = os.getenv("DATA_FILE_OUT", "data/gov-elements.json")

    data = generate_data(DATA_FILE_IN)
    save_data(data, DATA_FILE_OUT)

    print(f"Data saved with {len(data)} entries.")


