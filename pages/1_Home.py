import streamlit as st
import pandas as pd
from pathlib import Path
from st_pages import Page, add_page_title, hide_pages


st.set_page_config(
    page_title="Streamlit",
#    page_icon="",
)

#from nav import add_navigation

#add_navigation()

#st.title("Main Page")



#st.markdown(
#    """
#<style>
#   [data-testid="collapsedControl"] {
#        display: none
#    }
#</style>
#""",
#    unsafe_allow_html=True,
#)

# ----------------------------------------------------------------------------- #
# Menampilkan halaman utama aplikasi

"""
#  Home

**Halaman Utama**

"""
#Pengelompokan k-means adalah metode kuantisasi vektor, 
#yang awalnya berasal dari pemrosesan sinyal, 
#yang bertujuan untuk membagi n pengamatan ke dalam k klaster di mana setiap pengamatan termasuk dalam klaster dengan nilai rata-rata terdekat, 
#yang berfungsi sebagai prototipe.


st.info(
    """
    Gunakan side bar untuk mengganti halaman.
    """
)
