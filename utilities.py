def location_name(country=None, state=None):
    """return the name of the country and/or state used in the current filter"""
    locations = []
    if state:
        locations.append(state)
    if country:
        locations.append(country)
    return " - ".join(locations) if len(locations) > 0 else "everywhere"
