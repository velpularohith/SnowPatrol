from datetime import datetime, timedelta
# from snowflake.snowpark import Session
import snowflake.connector
import snowflake
import plotly.graph_objects as go
from app_data_model import SnowpatrolDataModel
import json 
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
# from streamlit_toggle import st_toggle_switch
from streamlit_option_menu import option_menu
from PIL import Image
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#from sqlalchemy import URL
import pandas as pd
import json
from snowflake.snowpark.session import Session
import snowflake.snowpark.functions as F
import snowflake.snowpark.types as T
from dotenv import find_dotenv
from pathlib import Path
import sys
import Revocations
import Export_Data
from streamlit_extras.switch_page_button import switch_page
import base64

# project_home = Path(find_dotenv()).parent
# sys.path.append(str(project_home))

# def build_snowpark_session(kwargs) -> Session:
#     try:
#         res=Session.builder.configs({
#         "account": kwargs["account"],
#         "user": kwargs["username"],
#         "password": kwargs["password"],
#         "warehouse": kwargs.get("warehouse", ""),
#         "database": kwargs.get("database", ""),
#         "schema": kwargs.get("schema", ""),
#         "role": kwargs.get("role", "")
#             }).create() 
#     except:
#         st.error(":warning: Incorrect login credentials")
#         res = None
#     return res

# def connect_to_snowflake(**kwargs):
#     if 'SNOWPARK_SESSION' not in st.session_state:
#         if (kwargs["account"].strip() != "") & (kwargs["username"].strip() != "") & (kwargs["password"].strip() is not None):
#             SNOWPARK_SESSION=build_snowpark_session(kwargs)
#             st.session_state['SNOWPARK_SESSION']=SNOWPARK_SESSION
#             st.info(f":+1: Connected to {SNOWPARK_SESSION.get_current_account()} as your default role - {SNOWPARK_SESSION.get_current_role()}")
#         else:
#             st.error(":warning: Missing fields")

# @st.cache_data
# def get_available_roles_for_user():
#     return st.session_state['sdm'].get_available_roles()

# @st.cache_data
# def get_available_databases(role):
#     return st.session_state['sdm'].get_available_databases(role)

# @st.cache_data
# def get_available_schemas(role, db):
#     return st.session_state['sdm'].get_available_schemas(role, db)

# @st.cache_data
# def get_available_warehouses(role):
#     return st.session_state['sdm'].get_available_warehouses(role)



# # Create a session state object to store app state
# if 'page' not in st.session_state:
#     st.session_state.page = 'login'

# # Set the page layout to be wide (call this only once, at the beginning)
# st.set_page_config(layout="wide")

# # Define the image you want to display
# image = "Image.png"
# with open(project_home / 'config/creds.json', 'r') as creds_file:
#     creds = json.load(creds_file)


    
# def init_session():
#     #Create a layout with two columns for the top 70% and bottom 30% of the page
#     col1, col2 = st.columns((3, 1))

#     # Add the image to the first column (top 70%)
#     with col1:
#         # Adjust the image width to fit correctly (you can adjust the width value)
#         st.image(image,  width=1000, output_format="PNG"  ,channels="BGR") 
#         st.markdown('<style>div.block-container{padding-bottom :0px; padding-right :0px; padding-top :0px;padding-left :50px; }</style>',unsafe_allow_html=True) # Set background color to transparent
       
        

#     # Add your logo to the second column (top 30%)
#     with col2:
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         logo = "SnowPatrol.png"  # Replace with the path to your logo
#         st.image(logo)
#         st.markdown('<style>div.block-container{margin-right :70px; margin-top: 50px;  }</style>',unsafe_allow_html=True) 


#         # Add login credentials below the logo
#         account = st.text_input("Snowflake Account Identifier**")
#         username = st.text_input("Username*")
#         password = st.text_input("Password*", type="password")
#             # Create a custom HTML button with rounded edges and "Connect" text
#         button_html = f"""
#         <button style="width: 100%; height: 35px; margin-top:20px; background: linear-gradient(to right, #a02a41 0%,    #1D4077 100%); color: white; border-radius: 15px;">Connect</button>
#         """
#         if st.markdown(button_html, unsafe_allow_html=True):
#             try:
#                 # Establish a connection to Snowflake using creds
#                 snowflake_conn = snowflake.connector.connect(
#                     user=username,
#                     password=password,
#                     account=account,
#                     warehouse=creds['warehouse'],
#                     database=creds['database'],
#                     schema=creds['schema']
#                 )

#                 # If the connection is successful, set a flag to indicate the connection status
#                 connection_successful = True
#             except Exception as e:
#                 # If the connection fails, display an error message
#                 connection_successful = False

#         # Based on the connection status, you can transition to the next page or display different content
#         if connection_successful:
#             connect_to_snowflake(account=account , username=username , password=password)
#             session_sdm = SnowpatrolDataModel(st.session_state['SNOWPARK_SESSION'])
#             st.session_state['sdm']=session_sdm # Placeholder for your next page logic
#             switch_page("Overview")
        

#         # Use custom CSS to change the color of the "Powered by Anblicks" text to sky blue
#         st.markdown(
#             """
#             <div style="text-align: center; margin-top: 10px;">
#                 <p style="font-size: 14px; color: #87CEEB;">Powered by Anblicks</p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#         # Next Message or Action
        
#         # You can add your desired actions or messages for the next step here

# if __name__ == '__main__':
#     if 'SNOWPARK_SESSION' not in st.session_state:
#         init_session()
    
    
project_home = Path(find_dotenv()).parent
sys.path.append(str(project_home))

def build_snowpark_session(kwargs) -> Session:
    try:
        res=Session.builder.configs({
        "account": kwargs["account"],
        "user": kwargs["username"],
        "password": kwargs["password"],
        "warehouse": kwargs.get("warehouse", ""),
        "database": kwargs.get("database", ""),
        "schema": kwargs.get("schema", ""),
        "role": kwargs.get("role", "")
            }).create() 
    except:
        st.error(":warning: Incorrect login credentials")
        res = None
    return res

def connect_to_snowflake(**kwargs):
    if 'SNOWPARK_SESSION' not in st.session_state:
        if (kwargs["account"].strip() != "") & (kwargs["username"].strip() != "") & (kwargs["password"].strip() is not None):
            SNOWPARK_SESSION=build_snowpark_session(kwargs)
            st.session_state['SNOWPARK_SESSION']=SNOWPARK_SESSION
            st.info(f":+1: Connected to {SNOWPARK_SESSION.get_current_account()} as your default role - {SNOWPARK_SESSION.get_current_role()}")
        else:
            st.error(":warning: Missing fields")

@st.cache_data
def get_available_roles_for_user():
    return st.session_state['sdm'].get_available_roles()

@st.cache_data
def get_available_databases(role):
    return st.session_state['sdm'].get_available_databases(role)

@st.cache_data
def get_available_schemas(role, db):
    return st.session_state['sdm'].get_available_schemas(role, db)

@st.cache_data
def get_available_warehouses(role):
    return st.session_state['sdm'].get_available_warehouses(role)



# Create a session state object to store app state
# if 'page' not in st.session_state:
#     st.session_state.page = 'login'

# Set the page layout to be wide (call this only once, at the beginning)
# st.set_page_config(layout="wide")

# Define the image you want to display
with open(project_home / 'config/creds.json', 'r') as creds_file:
    creds = json.load(creds_file)



    
from datetime import datetime, timedelta
from snowflake.snowpark import Session
import snowflake.connector
import plotly.graph_objects as go
import json 
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_toggle import st_toggle_switch
from streamlit_option_menu import option_menu
from PIL import Image
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import URL
import pandas as pd
import base64 
import snowflake.connector

_memory_cache = {}

def get_img_as_base64(file):

    if file in _memory_cache:

        return _memory_cache[file]

 

    with open(file, "rb") as f:

        data = f.read()

    encoded_data = base64.b64encode(data).decode()

    _memory_cache[file] = encoded_data

 

    return encoded_data

 
# Getting the base64 encoding of the image

image = get_img_as_base64(r"C:\Users\rohith.velpula\Downloads\login-image.png")

 
# Setting the background image using inline CSS

page_bg_img = f"""

<style>

.main {{

    background-color: white;

    background-image: linear-gradient(rgba(255,255,255,0), rgba(255,255,255,0)), url("data:image/png;base64,{image}");
    /*filter: brightness(1);  Adjust the value as needed */


    background-size: 70% 100%;  /* This makes the image cover 50% of the view */

    background-repeat: no-repeat;

}}

</style>

"""

# Applying the background image to the Streamlit app

st.markdown(page_bg_img, unsafe_allow_html=True)


    
def init_session():
    #Create a layout with two columns for the top 70% and bottom 30% of the page
    col1,col2 = st.columns((3,1))

    # Add the image to the first column (top 70%)
    with col1:
        # Adjust the image width to fit correctly (you can adjust the width value)
        # st.image(image,  width=1000, output_format="PNG"  ,channels="BGR") 
        # st.markdown('<style>div.block-container{padding-bottom :0px; padding-right :0px; padding-top :0px;padding-left :50px; }</style>',unsafe_allow_html=True) # Set background color to transparent
        st.write("")

    # Add your logo to the second column (top 30%)
    with col2:
        # st.write("")
        # st.write("")
        # st.write("")
        # st.write("")
        # st.write("")
        logo = "SnowPatrol.png"  # Replace with the path to your logo
        st.image(logo)
        st.markdown('<style>div.block-container{margin-left :100px; margin-top: 40px;  }</style>',unsafe_allow_html=True) 


        # Add login credentials below the logo
        account = st.text_input("Snowflake Account Identifier**")
        username = st.text_input("Username*")
        password = st.text_input("Password*", type="password")
            # Create a custom HTML button with rounded edges and "Connect" text
        button_html = f"""
        <button style="width: 100%; height: 35px; margin-top:20px; background: linear-gradient(to right, #a02a41 0%,    #1D4077 100%); color: white; border-radius: 15px;">Connect</button>
        """
        if st.markdown(button_html, unsafe_allow_html=True):
            try:
                # Establish a connection to Snowflake using creds
                snowflake_conn = snowflake.connector.connect(
                    user=username,
                    password=password,
                    account=account,
                    warehouse=creds['warehouse'],
                    database=creds['database'],
                    schema=creds['schema']
                )

                # If the connection is successful, set a flag to indicate the connection status
                connection_successful = True
            except Exception as e:
                # If the connection fails, display an error message
                connection_successful = False

        # Based on the connection status, you can transition to the next page or display different content
        if connection_successful:
            connect_to_snowflake(account=account , username=username , password=password)
            session_sdm = SnowpatrolDataModel(st.session_state['SNOWPARK_SESSION'])
            st.session_state['sdm']=session_sdm # Placeholder for your next page logic
            switch_page("Overview")
        

        # Use custom CSS to change the color of the "Powered by Anblicks" text to sky blue
        st.markdown(
            """
            <div style="text-align: center; margin-top: 10px;">
                <p style="font-size: 14px; color: #87CEEB;">Powered by Anblicks</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Next Message or Action
        
        # You can add your desired actions or messages for the next step here

if __name__ == '__main__':
    if 'SNOWPARK_SESSION' not in st.session_state:
        init_session()
    
    
