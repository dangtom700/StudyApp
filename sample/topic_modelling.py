from sklearn.decomposition import LatentDirichletAllocation

# Sample keywords
keywords = ["car", "automobile", "vehicle", "truck", "bike", "motorcycle"]

# Convert keywords to TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(keywords)

# Apply Latent Dirichlet Allocation (LDA)
lda = LatentDirichletAllocation(n_components=2, random_state=42)
lda.fit(X)

# Print topics and associated keywords
print("Topics and Associated Keywords:")
for topic_idx, topic in enumerate(lda.components_):
    print(f"Topic {topic_idx}:")
    top_keywords_idx = topic.argsort()[:-5:-1]  # Get top 5 keywords for each topic
    top_keywords = [vectorizer.get_feature_names()[i] for i in top_keywords_idx]
    print(top_keywords)
