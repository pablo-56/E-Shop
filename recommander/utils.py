import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame
from store.models import Product

def train_similarity_model():
    # Load data
    qs = Product.objects.all()
    df = read_frame(qs, fieldnames=['id', 'product_name', 'slug'])
    
    # Combine text fields
    df['text'] = df[['product_name', 'slug']].apply(
        lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    
    # Compute TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['text'])
    
    # Compute similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix)
    
    return df, cosine_sim

def get_recommendations(product_id, df, cosine_sim, top_n=3):
    # Get the index of the product that matches the product_id
    idx = df.index[df['id'] == product_id].tolist()[0]
    
    # Get the pairwise similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the products based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the top_n most similar products (excluding itself)
    sim_scores = sim_scores[1:top_n+1]
    
    # Get the product indices
    product_indices = [i[0] for i in sim_scores]
    
    # Return the top_n most similar products
    return df.iloc[product_indices]

