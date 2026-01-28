import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
from trafilatura import fetch_url, extract
from openai import OpenAI
import datetime
import os

# --- Page Config ---
st.set_page_config(
    page_title="Labor News Weekly",
    page_icon="👷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        color: #f0f0f0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff4d4d, #f9cb28);
        color: white;
        border: None;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(255, 77, 77, 0.4);
    }
    .header-text {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key to enable summarization.")
    if not api_key:
        st.warning("Please enter your OpenAI API key.")
    
    st.divider()
    st.subheader("Sources")
    sources = [
        "Google News (Labor News)",
        "NBC News (Labor News)",
        "MarketWatch (Labor News)",
        "CNBC (Labor News)",
        "Bureau of Labor Statistics",
        "Federal Reserve News"
    ]
    for s in sources:
        st.write(f"- {s}")

# --- Main Logic ---

def fetch_labor_news():
    results = []
    ddgs = DDGS()
    
    source_queries = [
        {"name": "Google News", "query": "labor news"},
        {"name": "NBC News", "query": "site:nbcnews.com labor news"},
        {"name": "MarketWatch", "query": "site:marketwatch.com labor news"},
        {"name": "CNBC", "query": "site:cnbc.com labor news"},
        {"name": "Bureau of Labor Statistics", "query": "site:bls.gov latest news"},
        {"name": "Federal Reserve", "query": "site:federalreserve.gov latest news"}
    ]
    
    with st.status("Fetching latest news...", expanded=True) as status:
        for sq in source_queries:
            st.write(f"Searching {sq['name']}...")
            try:
                search_results = list(ddgs.news(sq['query'], max_results=3))
                for res in search_results:
                    results.append({
                        "source": sq['name'],
                        "title": res['title'],
                        "link": res['url'],
                        "snippet": res['body'],
                        "date": res.get('date', 'N/A')
                    })
            except Exception as e:
                st.error(f"Error fetching from {sq['name']}: {e}")
        status.update(label="News fetched!", state="complete", expanded=False)
    
    return results

def get_summary(articles, api_key):
    if not articles:
        return "No articles found to summarize."
    
    client = OpenAI(api_key=api_key)
    
    # Combine article info for the prompt
    context = ""
    for i, art in enumerate(articles):
        context += f"Source: {art['source']}\nTitle: {art['title']}\nSnippet: {art['snippet']}\nLink: {art['link']}\n---\n"
    
    prompt = f"""
    You are an expert economic and labor analyst. 
    Below are news snippets related to labor news from various sources for the past week.
    
    Please provide a comprehensive "Weekly Labor News Summary" that:
    1. Highlights the top 3-5 most significant trends or events.
    2. Categorizes news by source type (General News, BLS, Fed).
    3. Provides a concise outlook for the coming week.
    4. Is professional, informative, and formatted with clear headings and bullet points.
    
    Articles:
    {context}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional labor market analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

# --- UI Layout ---

st.markdown('<div class="header-text">Labor News Weekly Summarizer</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🚀 Fetch & Summarize"):
        if not api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        else:
            news_data = fetch_labor_news()
            st.session_state['news_data'] = news_data
            
            with st.spinner("Generating Weekly Summary..."):
                summary = get_summary(news_data, api_key)
                st.session_state['summary'] = summary

if 'summary' in st.session_state:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Weekly Summary")
    st.markdown(st.session_state['summary'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📰 Source Articles")
    df = pd.DataFrame(st.session_state['news_data'])
    st.dataframe(
        df,
        column_config={
            "source": "Source",
            "title": "Title",
            "link": st.column_config.LinkColumn("Article Link"),
            "date": "Date",
            "snippet": None # Hide snippet in main table
        },
        use_container_width=True
    )
else:
    st.info("Click the button to fetch and summarize the latest labor news.")

# --- Footer ---
st.divider()
st.caption(f"Powered by Streamlit & OpenAI | Last checked: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
