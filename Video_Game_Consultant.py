import streamlit as st
import openai
import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Video Game Recommender", page_icon="🎮", layout="wide")

# At the top of your app, after setting page config
st.image("banner.jpg", use_column_width=True)  # A nice gaming banner

st.title("🎮 OpenAI Video Game Recommender with Retrieval")
st.markdown("This app recommends **newer video games** based on your criteria. Select your preferences, then hit **Generate Recommendations**.")
st.info("Tip: Adjust the filters on the left to refine your game suggestions.")

# Sidebar header
st.sidebar.header("🕹️ Your Game Preferences")

# Sidebar components (selectbox, text_input, etc.)
genre = st.sidebar.selectbox(
    'Select a video game genre:',
    ['Action', 'Adventure', 'RPG', 'Strategy', 'Shooter', 'Puzzle', 'Sports', 'Racing', 'Simulation', 'Horror', 'Platformer']
)
preferences = st.sidebar.text_input(
    'Describe your preferences:',
    'I enjoy narrative-driven titles with rich characters and a strong storyline.'
)
language = st.sidebar.selectbox(
    'Select a language:',
    ['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Japanese']
)
console = st.sidebar.selectbox(
    'Select a console/platform:',
    ['Any', 'PC', 'PlayStation', 'Xbox', 'Nintendo Switch']
)
age_restriction = st.sidebar.selectbox(
    'Select an age rating restriction:',
    ['Any', 'E (Everyone)', 'E10+ (Everyone 10+)', 'T (Teen)', 'M (Mature 17+)', 'AO (Adults Only 18+)']
)
price_range = st.sidebar.text_input(
    'Enter a price range (Under $20, $20-$60, no preference):',
    'Under $40'
)

recommendations_placeholder = st.empty()

# Setup vectorstore and chains
chroma_db = Chroma(
    collection_name="games_db", 
    embedding_function=OpenAIEmbeddings(openai_api_key=openai.api_key)
)

retriever = chroma_db.as_retriever(search_kwargs={"k": 5})
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model_name="gpt-4", openai_api_key=openai.api_key),
    retriever=retriever,
    return_source_documents=True
)

if st.sidebar.button('Generate Recommendations'):
    with st.spinner("Generating recommendations..."):
        # Ensure the indented block follows the 'with' statement
        user_query = (
            f"Recommend newer {genre} video games for the {console} platform, "
            f"suitable for {age_restriction} players, within a price range of {price_range}. "
            f"Preferences: {preferences}. "
            f"Respond in {language}. "
            f"Include a brief description of why each game fits these criteria."
        )
        result = qa_chain({"question": user_query, "chat_history": []})  # Ensure this line is indented
        recommendations = result["answer"]

        # Displaying the results
        st.subheader("Your Recommendations 🎉")
        st.markdown(recommendations)


# Main Title
st.title("🎮 Video Game Recommender")

st.markdown("This app will recommend **newer video games** based on chosen criteria, using external data. Just select your desired criteria from the sidebar and hit **Generate Recommendations**!")

# Note: The sidebar components are defined above; avoid redefining them here to prevent conflicts.
