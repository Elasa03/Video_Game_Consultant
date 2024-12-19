#################################
## Video Game Recommender ##
#################################

# Importing Libraries
import streamlit as st
import openai

# Setting up OpenAI API Key securely using Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit App

st.title('🎮 Video Game Recommender')

st.write('Welcome to the Video Game Recommender! Provide your preferences below and receive tailored game suggestions.')

# Sidebar for User Inputs
st.sidebar.header("🕹️ Your Game Preferences")

# Selecting Genre
genre = st.sidebar.selectbox(
    'Select a video game genre:',
    ['Action', 'Adventure', 'RPG', 'Strategy', 'Shooter', 'Puzzle', 'Sports', 'Racing', 'Simulation', 'Horror', 'Platformer']
)

# Describing Preferences
preferences = st.sidebar.text_input(
    'Describe your preferences:',
    'I enjoy narrative-driven titles with rich characters and a strong storyline.'
)

# Selecting Language
language = st.sidebar.selectbox(
    'Select a language:',
    ['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Japanese']
)

# Selecting Platform
console = st.sidebar.selectbox(
    'Select a console/platform:',
    ['Any', 'PC', 'PlayStation', 'Xbox', 'Nintendo Switch']
)

# Selecting Age Rating
age_restriction = st.sidebar.selectbox(
    'Select an age rating restriction:',
    ['Any', 'E (Everyone)', 'E10+ (Everyone 10+)', 'T (Teen)', 'M (Mature 17+)', 'AO (Adults Only 18+)']
)

# Entering Price Range
price_range = st.sidebar.text_input(
    'Enter a price range (e.g., Under $20, $20-$60, No preference):',
    'Under $40'
)

# Placeholder for Recommendations
recommendations_placeholder = st.empty()

# Generate Recommendations Button
if st.sidebar.button('Generate Recommendations'):
    with st.spinner("Generating recommendations..."):
        try:
            # Crafting the Prompt
            user_query = (
                f"Recommend newer {genre} video games for the {console} platform, "
                f"suitable for {age_restriction} players, within a price range of {price_range}. "
                f"Preferences: {preferences}. "
                f"Respond in {language}. "
                f"Include a brief description of why each game fits these criteria."
            )
            
            # Interacting with OpenAI's API using the new ChatCompletion method
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in recommending video games."},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=500,
                temperature=0.7,
            )
            
            # Extracting recommendations from the response
            recommendations = response['choices'][0]['message']['content']
            
            # Displaying Recommendations
            st.subheader("Your Recommendations 🎉")
            st.markdown(recommendations)

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")