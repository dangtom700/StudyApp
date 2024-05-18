from sklearn.cluster import AgglomerativeClustering

# Sample keywords
keywords = ["car", "automobile", "vehicle", "truck", "bike", "motorcycle"]

# Convert keywords to TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(keywords)

# Perform agglomerative clustering
agg_cluster = AgglomerativeClustering(n_clusters=2)
agg_cluster.fit(X.toarray())

# Print clusters
clusters = {}
for i, label in enumerate(agg_cluster.labels_):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(keywords[i])

print("Clusters:")
for cluster in clusters.values():
    print(cluster)
