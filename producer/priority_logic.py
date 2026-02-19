def determine_priority(alert):
    if alert['weapons_count'] > 0 or alert['distance_from_fence_m'] <= 50 or alert['people_count'] >= 8 or alert['vehicle_type'] == 'truck':
        return 'URGENT'
    if (alert['people_count'] >= 4 and alert['distance_from_fence_m'] <= 150) or (alert['people_count'] >= 3 and alert['vehicle_type'] == 'jeep'):
        return 'URGENT'
    return 'NORMAL'
