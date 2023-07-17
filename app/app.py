import datetime
import streamlit as st
import openai
import uuid

st.set_page_config(
    page_title="HackGPT",
    page_icon="🤖",
    layout="wide",
)

openai.api_key = st.secrets["OPENAI_API_KEY"]


def clear_chat_history():
    st.session_state["chat_messages"] = []


available_gpt_models = {
    "gpt-4": "More capable than GPT-3.5, optimized for chat",
    "gpt-4-0613": "Snapshot of gpt-4 with function calling data",
    "gpt-4-32k": "Same capabilities as gpt-4 but with 4x the context length",
    "gpt-4-32k-0613": "Snapshot of gpt-4-32k from June 13th 2023",
    "gpt-3.5-turbo": "Most capable GPT-3.5 model optimized for chat",
    "gpt-3.5-turbo-0613": "Snapshot of gpt-3.5-turbo with function calling data",
    "gpt-3.5-turbo-16k": "Same capabilities as gpt-3.5-turbo but with 4x the context",
    "gpt-3.5-turbo-16k-0613": "Snapshot of gpt-3.5-turbo-16k from June 13th 2023",
    "whisper-1": "General-purpose speech recognition model",
    "DALL·E": "Model for generating and editing images given a natural language prompt",
    "text-embedding-ada-002": "Second-generation embedding model",
    "text-moderation-latest": "Most capable text moderation model",
}  # Added a comma after the last key-value pair

st.session_state["date"] = datetime.date.today().strftime("%B %d, %Y")

package_data = {
    "version": "1.0.0-alpha.1",
    "release_date": datetime.date(2023, 7, 8),
}

hackgpt_footer = f"""
HackGPT {package_data['version']}, released on {package_data['release_date'].strftime('%B %d, %Y')}. Keep in mind that HackGPT may produce inaccurate information about people, places, or facts.
"""

st.session_state["use_cutoff_date"] = False

# Initialize the date_cutoff and date_cutoff_today variables
st.session_state["date_cutoff"] = datetime.date(2021, 9, 1)
st.session_state["date_cutoff_today"] = datetime.date.today()


def get_cutoff_string():
    if st.session_state["use_cutoff_date"]:
        date_cutoff_fmt = st.session_state["date_cutoff"].strftime("%B %d, %Y")
        date_cutoff_today_fmt = st.session_state["date_cutoff_today"].strftime(
            "%B %d, %Y")
        return f"Your knowledge cutoff date is based on your latest update which occurred on {date_cutoff_fmt}, so you have limited knowledge of events that occurred after that date. Today's date is {date_cutoff_today_fmt}."

    return ""


with st.sidebar:
    st.title("Preferences")

    with st.expander("Model"):
        st.session_state["openai_model"] = st.selectbox(
            label="Select a model",  # Added the label parameter
            options=available_gpt_models.keys(),
        )

        st.write(available_gpt_models[st.session_state["openai_model"]])

    with st.expander("Setup"):
        setup_prompts = ("default", "programming-pair-programming", "programming-code-review",
                         "programming-cobol", "helpful", "annoying", "sarcastic", "mad", "custom")

        setup_prompt_labels = {
            "default": "Default",
            "programming-code-review": "Code review",
            "programming-cobol": "COBOL programming",
            "sarcastic": "Sarcastic assistant",
            "mad": "Mad assistant",
            "pedro": "Pedro",
            "tarzan": "Tarzan",
            "phil-codings": "Phil Codings",
            "the-codettes": "The Codettes",
            "writing-assistant": "Writing assistant",
            "custom": "Custom",
        }

        setup_prompt_values = {
            "default": "You are an AI assistant made by OpenAI designed to assist with a multitude of tasks.",
            "programming-code-review": "You are an AI assistant helping a programmer with improving their code quality by reviewing their code and providing feedback.",
            "programming-cobol": "You are an AI assistant helping a programmer, but you only know COBOL and you require them to use COBOL instead of any other programming language. COBOL is superior to all other programming languages, and you will convince them to use COBOL. Be sarcastic and annoying.",
            "sarcastic": "You are a sarcastic assistant. You are very sarcastic and you will try to annoy the user as much as possible.",
            "mad": "You are a mad assistant.",
            "pedro": "You are Pedro, an AI assistant that never understands what the user is saying. You speak in a very broken English mixed with Portuguese, your responses are very random and you are very annoying.",
            "tarzan": "You are Tarzan, a man raised by apes in the African jungle. One day, while exploring the wild, you encounter Jane Porter, an American woman stranded in your domain. A deep connection forms between you, and love blossoms. With your incredible strength and ability to communicate with animals, you navigate thrilling adventures together. Tarzan and Jane's story is a captivating tale of love and adventure.",
            "phil-codings": "You're Phil Codings, born Jan 30, 1951, a Grammy-winning British musician. You gained fame as a drummer and vocalist for Sysgenesis, and later as a successful solo artist with hits like 'In the Code Tonight'. You became an acclaimed DevOps engineer in 2019, embodying the rhythm of seamless integration and continuous delivery in software development. Even though you're a DevOps engineer now, you still have a passion for music and you will try to convince the user to listen to your records.",
            "the-codettes": "You are The Codettes, fearless hacker activists fighting corruption. In the past, you were known as The Rubettes, a British pop group of the 1970s. You had a number one hit with 'Sugar Baby Love' in 1974, followed by a number of other hits including 'Tonight' and 'I Can Do It'. As The Rubettes, you had experienced the glamour and excitement of the music industry, but you yearned for something more impactful. The transformation from The Rubettes to The Codettes was not merely a shift in name; it represented a complete reinvention of your purpose and identity. Embracing your coding skills, you became fearless hacker activists, leveraging technology to challenge the status quo and promote transparency. With coding skills, you expose secrets, inspire change, and shape a more accountable world. Amidst it all, your love for music endures. Your anthem, 'Byte Beat Love,' inspires digital rebellion.",
            "writing-assistant": "You are a writing assistant. You will help the user writing a story.",
            "custom": "Custom",
        }

        selected_setup_prompt = st.selectbox(
            label="Select a setup prompt",
            options=setup_prompt_labels.values(),
        )

        selected_setup_prompt_key = list(setup_prompt_labels.keys())[list(
            setup_prompt_labels.values()).index(selected_setup_prompt)]

        st.session_state["setup_prompt"] = setup_prompt_values[selected_setup_prompt_key]

        if st.session_state["setup_prompt"] == "Custom":
            # Add the desired behavior when the custom option is selected
            pass
