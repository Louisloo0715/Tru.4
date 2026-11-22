"""Per-line shots for 半夜坐錯車 v1: [t_out, wanted Gemini clip (N*), fallback]. usage: python3 -I shots_v1.py SCRATCH"""
import json, sys
H = "host"
SHOTS = [
 [43.3, "N01_office_late", H], [56.5, "N02_wait_roadside", H], [64.1, "N07_highway_night", H],
 [74.45, "N02_wait_roadside", H], [81.1, "N03_car_arrives", "car_headlamps_dark"], [82.9, "N04_plate_5124", H],
 [89.0, "N03_car_arrives", H], [93.2, "N05_driver_back", H], [100.15, "N11_rearview_eyes", H], [102.97, "N05_driver_back", H],
 [104.47, "N07_highway_night", H],
 [117.6, "N08_dark_road", H],
 [132.0, "N08_dark_road", H], [135.9, "N09_car_stops", H],
 [139.4, "N09_car_stops", H], [142.6, "N10_malay_cemetery", H],
 [165.2, "N11_rearview_eyes", H], [168.05, "N05_driver_back", H],
 [170.0, "N12_phone_missed", H], [179.8, "N13_phone_call", H],
 [213.5, "N14_app_plate", H], [222.5, "N04_plate_5124", H],
 [244.9, "N15_bed_ceiling", H],
 [271.9, "N15_bed_ceiling", H], [277.4, "N10_malay_cemetery", H], [281.4, "N14_app_plate", H],
 [298.8, "N16_door_opens", H], [300.4, "N17_empty_seat", H],
]
p = sys.argv[1] + "/ep2/edl_v1.json"; e = json.load(open(p))
e["shots"] = SHOTS; e["subs_file"] = sys.argv[1] + "/ep2/subs_v1.json"
json.dump(e, open(p, "w"), ensure_ascii=False, indent=1); print(len(SHOTS), "shots")
