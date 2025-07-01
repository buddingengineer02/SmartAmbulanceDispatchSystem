
import pandas as pd
from geopy.distance import geodesic
from sklearn.neighbors import NearestNeighbors

# ---------- Load Data -------------------------------------------------------
DATA_PATH = "mock_data.csv"
df = pd.read_csv(DATA_PATH)

ambulances = df[df["entity_type"] == "ambulance"].reset_index(drop=True)
hospitals  = df[df["entity_type"] == "hospital"].reset_index(drop=True)

# ---------- Helper Functions -----------------------------------------------
def find_nearest_ambulance(lat, lon):
    coords = ambulances[["latitude", "longitude"]].values
    nbrs   = NearestNeighbors(n_neighbors=1, metric="haversine").fit(coords)
    # Haversine expects radians
    import numpy as np
    distances, indices = nbrs.kneighbors(np.radians([[lat, lon]]))
    idx   = indices[0][0]
    amb   = ambulances.iloc[idx]
    km    = distances[0][0] * 6_371  # radius of Earth
    return amb, round(km, 2)

def select_destination_hospital():
    available = hospitals[hospitals["beds_available"] > 0]
    if available.empty:
        return None
    # Pick the hospital with max beds (simple rule)
    return available.sort_values("beds_available", ascending=False).iloc[0]

# ---------- Main Flow -------------------------------------------------------
def main():
    try:
        lat = float(input("Enter emergency latitude : "))
        lon = float(input("Enter emergency longitude: "))
    except ValueError:
        print("❌  Invalid coordinates.")
        return

    amb, distance_km = find_nearest_ambulance(lat, lon)
    hospital         = select_destination_hospital()

    print("\n📢  DISPATCH DECISION")
    print("-" * 40)
    print(f"Nearest Ambulance : {amb['id']} ({amb['name']})")
    print(f"Distance          : {distance_km} km")
    if hospital is not None:
        print(f"Destination Hosp. : {hospital['name']} "
              f"({int(hospital['beds_available'])} beds free)")
    else:
        print("Destination Hosp. : ❗ No beds available anywhere!")

    # Mock alert (stdout)
    print("\n✅  Alert sent to driver of", amb["id"])

if __name__ == "__main__":
    main()
