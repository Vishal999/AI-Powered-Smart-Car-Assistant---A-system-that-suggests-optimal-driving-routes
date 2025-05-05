import streamlit as st
from sample_data import get_product_data
from recommender import create_similarity_matrix, recommend_products
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration and styling
st.set_page_config(
    page_title="Product Recommender",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stSelectbox {
        margin: 1rem 0;
    }
    .recommendation-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    .similarity-score {
        color: #1f77b4;
        font-size: 0.9rem;
    }
    .product-category {
        color: #666;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

def load_data():
    """Load and prepare data with error handling"""
    try:
        df = get_product_data()
        df['id'] = df['id'].astype(str)
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        st.error("Failed to load product data. Please try refreshing the page.")
        return None

def create_similarity_matrix_with_handling(df):
    """Create similarity matrix with error handling"""
    try:
        return create_similarity_matrix(df)
    except Exception as e:
        logger.error(f"Error creating similarity matrix: {str(e)}")
        st.error("Failed to process product similarities. Please try again later.")
        return None, None

def main():
    st.title("🛒 AI-Based Product Recommender")
    
    # Add description in a container
    with st.container():
        st.markdown("""
        Get personalized product recommendations powered by AI! 
        Our system analyzes product descriptions to find items that match your interests.
        """)
    
    # Load data with error handling
    df = load_data()
    if df is None:
        return

    # Create similarity matrix with error handling
    cosine_sim, id_to_index = create_similarity_matrix_with_handling(df)
    if None in (cosine_sim, id_to_index):
        return

    # Sidebar for filters
    with st.sidebar:
        st.subheader("📊 Filter Options")
        # Add category filter
        categories = ["All"] + sorted(df['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category:", categories)
        
        # Filter products based on category
        filtered_df = df if selected_category == "All" else df[df['category'] == selected_category]
        
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🔍 Select a Product")
        selected_name = st.selectbox(
            "Choose a product:",
            filtered_df['name'].tolist(),
            key="product_selector"
        )
        
        # Show selected product details
        if selected_name:
            product_details = df[df['name'] == selected_name].iloc[0]
            st.markdown("### Selected Product Details")
            st.markdown(f"**Category:** {product_details['category']}")
            st.markdown(f"**Description:** _{product_details['description']}_")

    with col2:
        if selected_name:
            try:
                selected_id = df[df['name'] == selected_name]['id'].values[0]
                recommendations = recommend_products(str(selected_id), df, cosine_sim, id_to_index)
                
                st.subheader("🎯 Top Recommendations")
                
                # Display recommendations in a grid
                for i, rec in enumerate(recommendations, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>{i}. {rec['name']}</h4>
                            <p class="product-category">{rec['category']}</p>
                            <p>{rec['description']}</p>
                            <p class="similarity-score">Similarity Score: {rec['similarity_score']:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                logger.error(f"Error generating recommendations: {str(e)}")
                st.error("Failed to generate recommendations. Please try a different product.")

if __name__ == "__main__":
    main()
