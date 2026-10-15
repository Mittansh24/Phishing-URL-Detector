import re

def extract_features(url):
    features = []

    # Basic features
    features.append(len(url))
    features.append(1 if url.startswith("https") else 0)
    features.append(1 if "@" in url else 0)
    features.append(1 if re.match(r'http[s]?://\d+\.\d+\.\d+\.\d+', url) else 0)
    features.append(url.count("-"))

    # Fill remaining features to match model (30 total)
    while len(features) < 30:
        features.append(0)

    return features