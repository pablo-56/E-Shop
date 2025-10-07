from django.shortcuts import render, get_object_or_404
from store.models import Product
from .utils import train_similarity_model, get_recommendations

df, cosine_sim = train_similarity_model()

def recommend_products(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recommended_df = get_recommendations(product_id, df, cosine_sim)
    
    recommended_products = Product.objects.filter(id__in=recommended_df['id'].tolist())
    
    
    product_count = recommended_products.count()  # 👈 count the results
    
    return render(request, 'recommender/recommendations.html', {
        'product': product,
        'recommended_products': recommended_products,
        'product_count': product_count,
    })
# You can call train_similarity_model() periodically or via a management command to update the model    