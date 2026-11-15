import os
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

# App Title & Description
st.title("✍️ AI Content Assistant")
st.markdown("Generate platform-optimized posts, captions, and hashtags instantly using **Groq**.")

# Retrieve API Key (Supports local .env/environment variables and Streamlit Cloud Secrets)
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

# Sidebar for API Key and Configuration
with st.sidebar:
    st.header("🔑 Configuration")
    if not api_key:
        api_key = st.text_input("Enter Groq API Key:", type="password")
        st.markdown("[Get a free Groq API Key](https://console.groq.com/)")
    else:
        st.success("API Key loaded successfully!")
    
    st.divider()
    st.markdown("### About")
    st.info("Powered by Groq's blazing-fast LLMs (Llama 3) and Streamlit.")

# Main Form Inputs
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Select Content Type",
            ["Social Media Post", "Blog Intro / Summary", "Ad Copy", "Newsletter Blurb", "Thread / Carousel"]
        )
        platform = st.selectbox(
            "Select Platform",
            ["LinkedIn", "X (Twitter)", "Instagram", "Facebook", "General"]
        )
    
    with col2:
        tone = st.selectbox(
            "Tone of Voice",
            ["Professional", "Casual & Friendly", "Authoritative", "Humorous", "Inspirational", "Educational"]
        )
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Tech founders, Marketers, Beginners"
        )

    topic = st.text_area(
        "Topic / Key Message",
        placeholder="What is this post about? Include key points or call-to-action..."
    )
    
    submit_button = st.form_submit_button("🚀 Generate Content", use_container_width=True)

# Generation Logic
if submit_button:
    if not api_key:
        st.error("⚠️ Please provide a valid Groq API Key in the sidebar or Streamlit Secrets.")
    elif not topic.strip():
        st.warning("⚠️ Please enter a topic or key message.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert copywriter and social media manager. Create a high-performing {content_type} optimized for {platform}.
            
            - **Topic/Key Message:** {topic}
            - **Target Audience:** {target_audience if target_audience else 'General Audience'}
            - **Tone:** {tone}
            
            Requirements:
            1. Create an engaging hook/headline.
            2. Write a clear, valuable body caption structured for readability (use line breaks and emojis where appropriate for the platform).
            3. Include a strong Call-to-Action (CTA).
            4. Provide 5-8 relevant, high-reaching hashtags at the end.
            
            Format the output clearly with Markdown headings.
            """
            
            with st.spinner("✨ Generating your content with Groq..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional content creator who writes viral, high-engagement copy."
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=1024,
                )
                
                generated_content = chat_completion.choices[0].message.content
                
            st.success("✅ Content Generated Successfully!")
            st.markdown("---")
            st.markdown(generated_content)
            
            # Copy friendly text area output
            st.text_area("Raw Output (Easy to Copy):", value=generated_content, height=200)

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")