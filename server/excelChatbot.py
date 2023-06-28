from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from streamlit_chat import message
import streamlit as st
import pandas as pd
import openai
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(layout="wide",page_title="ExcelMate",page_icon="https://cdn.dribbble.com/userupload/3963238/file/original-2aac66a107bee155217987299aac9af7.png?compress=1&resize=400x300&vertical=center")

os.environ["OPENAI_API_KEY"] = "d1eff60358e649b38c6a9140ee656cef"
openai.api_type = "azure"
openai.api_base = "https://datascience.openai.azure.com/"
openai.api_version = "2022-12-01"

def pandas_agent(df,user_prompt):
    agent = create_pandas_dataframe_agent(OpenAI(engine="gpt-demo",temperature=0), df, verbose=True)
    return agent.run(user_prompt)


# st.sidebar.title("ExcelMate")
# st.sidebar.caption("Your go-to solution for all Excel queries. Get instant answers and solutions for your Excel file questions.")
excel_file = st.sidebar.file_uploader("Upload",type="csv")
# user_prompt = st.text_input("",placeholder="Ask Your Query..")

if excel_file is not None:
    df = pd.read_csv(excel_file, encoding="latin-1")
    st.sidebar.dataframe(df)

    if 'history' not in st.session_state:
        st.session_state['history'] = []


    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]
            
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me anything about " + excel_file.name + " 🤗"] 
    #container for the chat history
    response_container = st.container()
    #container for the user's text input
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
                
            user_input = st.text_input("Query:", placeholder="Talk about your csv data here (:", key='input')
            submit_button = st.form_submit_button(label='Send')
                
        if submit_button and user_input:
            output = pandas_agent(df,user_input)
            st.pyplot()
                
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="adventurer", seed=123,)
                message(st.session_state["generated"][i], key=str(i))
