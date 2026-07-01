from src.ContentBased import (
    load_user_data,
    save_user_data,
    df
)
from src.mapping import region_map
import streamlit as st
import json

liked, disliked, watched = load_user_data()

# ---------------- PAGE ---------------- #

st.set_page_config(
    page_title="Profile",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

/* APP */
.stApp {
    background-color: black;
}

/* HEADER */
header {
    background-color: black !important;
}

[data-testid="stHeader"] {
    background-color: black;
}

/* TEXT */
h1,h2,h3,h4,h5,h6,p,span,label {
    color: white !important;
}

/* CARD */
.profile-card {

    border: 1px solid rgba(255,255,255,0.12);

    border-radius: 16px;

    padding: 20px;

    background-color: rgba(255,255,255,0.03);

    min-height: 500px;

    box-shadow:
    0px 0px 10px rgba(255,255,255,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD USER DATA ---------------- #

with open(
    "data/user_data.json",
    "r"
) as f:

    data = json.load(f)

region = data.get("region", "kerala")

age = data.get("age", 20)

# ---------------- TITLE ---------------- #

st.markdown("""
<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-top:20px;
margin-bottom:40px;
padding-left:80px;
padding-right:300px;
">

<h1 style="
color:white;
font-size:58px;
font-weight:800;
margin:0;
">
YOUR PROFILE
</h1>

<img src="https://cdn-icons-png.flaticon.com/512/149/149071.png"
style="
width:240px;
height:240px;
border-radius:50%;
border:2px solid rgba(255,255,255,0.2);
object-fit:cover;
">

</div>
""", unsafe_allow_html=True)

nav1, nav2 = st.columns([10,1])

with nav2:

    if st.button("🏠"):

        st.switch_page("app.py")

st.markdown("""
<style>

[data-testid="stSidebar"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MAIN AREA ---------------- #

left_space, main_area, right_space = st.columns([0.08, 1, 0.08])

with main_area:

    # ---------------- SETTINGS ---------------- #

    st.subheader("User Preferences")

    c1, c2 = st.columns(2)

    # REGION

    with c1:

        selected_region = st.selectbox(
            "Select Region",
            options=list(region_map.keys()),
            index=list(region_map.keys()).index(region)
        )

    # AGE

    with c2:

        selected_age = st.slider(
            "Select Age",
            10,
            80,
            age
        )

    # SAVE PROFILE

    if st.button("Save Profile"):

        data["region"] = selected_region

        data["age"] = selected_age

        with open(
            "data/user_data.json",
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        st.success("Profile Updated")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- LISTS ---------------- #

    l1, l2, l3 = st.columns(3)

    # ---------------- LIKED ---------------- #

    with l1:

        with st.container(height=500, border=True):

            st.subheader("👍 Liked Movies")

            for movie_id in liked:

                movie_name = df.loc[
                    movie_id,
                    "Movie Name"
                ]

                st.write(movie_name)

            if st.button(
                "Clear Likes",
                key="clear_likes"
            ):

                liked.clear()

                save_user_data(liked,disliked,watched)

                st.rerun()

    # ---------------- DISLIKED ---------------- #

    with l2:

        with st.container(height=500, border=True):

            st.subheader("👎 Disliked Movies")

            for movie_id in disliked:

                movie_name = df.loc[
                    movie_id,
                    "Movie Name"
                ]

                st.write(movie_name)

            if st.button(
                "Clear Disliked",
                key="clear_disliked"
            ):

                disliked.clear()

                save_user_data(liked,disliked,watched)

                st.rerun()

    # ---------------- WATCHED ---------------- #

    with l3:

        with st.container(height=500, border=True):

            st.subheader("👁 Watched Movies")

            for movie_id in watched:

                movie_name = df.loc[
                    movie_id,
                    "Movie Name"
                ]

                st.write(movie_name)

            if st.button(
                "Clear Watched",
                key="clear_watched"
            ):

                watched.clear()

                save_user_data(liked,disliked,watched)

                st.rerun()

