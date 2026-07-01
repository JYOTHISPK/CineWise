from src.ContentBased import (
    load_user_data,
    save_user_data
)
from src.ContextBased import recommend
import random
import streamlit as st
import os

# ---------------- PAGE ---------------- #

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* HIDE SIDEBAR */
[data-testid="stSidebar"] {
    display: none;
}

/* REMOVE SIDEBAR NAV */
[data-testid="collapsedControl"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TOP BAR ---------------- #

left_space, logo_col, profile_col = st.columns([4,8,1])

# ---------------- LOGO ---------------- #

with logo_col:

    st.markdown( "<div style='margin-top:40px'></div>", unsafe_allow_html=True )

    st.image(
        "images/others/IMG_20260621_150902.png",
        width=420
    )

# ---------------- PROFILE BUTTON ---------------- #

with profile_col:

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("👤"):

        st.switch_page("pages/profile.py")


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

/* FULL WIDTH */
.block-container {
    max-width: 100% !important;
    padding-top: 1rem;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
}

/* REMOVE COLUMN PADDING */
[data-testid="column"] {
    padding: 0rem 0.25rem !important;
}

/* IMAGES */
[data-testid="stImage"] img {
    border-radius: 12px;
}

/* MOVIE CARD */
.movie-card {

    border: 1px solid rgba(255,255,255,0.12);

    border-radius: 16px;

    padding: 18px;

    background-color: rgba(255,255,255,0.03);

    height: 240px;

    margin-bottom: 20px;

    box-shadow:
    0px 0px 10px rgba(255,255,255,0.05);
}

/* TITLE */
.movie-title {

    color: white;

    font-size: 24px;

    font-weight: 700;

    line-height: 1.3;

    height: 78px;

    overflow: hidden;
}

/* DETAILS */
.movie-details {

    color: #b8b8b8;

    font-size: 15px;

    line-height: 1.6;

    margin-top: 10px;

    height: 65px;

    overflow: hidden;
}

/* RATING */
.movie-rating {

    color: #FFD54F;

    font-size: 18px;

    font-weight: 600;

    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- INIT ---------------- #

if "banner_index" not in st.session_state:

    st.session_state.banner_index = 0

# ---------------- BANNERS ---------------- #

banner_folder = "images/poster"

banners = sorted(
    os.listdir(banner_folder)
)

current = st.session_state.banner_index

# pick 5 sequential banners

selected_banners = [

    banners[(current + i) % len(banners)]

    for i in range(5)

]

# ---------------- DISPLAY ---------------- #

cols = st.columns(5, gap="small")

for col, banner in zip(cols, selected_banners):

    with col:

        st.image(

            os.path.join(
                banner_folder,
                banner
            ),

            use_container_width=True

        )

# ---------------- SHIFT FOR NEXT RERUN ---------------- #

st.session_state.banner_index = (

    current + 1

) % len(banners)




# ---------------- LOAD MOVIES ---------------- #

movies = recommend(
)

top_movies = movies[:15]

explore_movies = movies[15:2000]

random_movies = random.sample(
    explore_movies,
    15
)

movies = (
    top_movies + random_movies
)


# ---------------- TITLE ---------------- #

st.markdown("""
<h1 style="
color:white;
margin-top:30px;
margin-bottom:35px;
margin-left:100px;
font-size:58px;
font-weight:800;
">
TOP RECOMMENDS FOR YOU
</h1>
""", unsafe_allow_html=True)

# ---------------- MOVIES ---------------- #

liked, disliked, watched = load_user_data()

for i in range(0, min(len(movies), 30), 5):

    left_space, main_area, right_space = st.columns([0.08, 1, 0.08])

    with main_area:

        cols = st.columns(5)

        batch = movies[i:i+5]

        for col, movie in zip(cols, batch):

            with col:

                movie_name = movie["name"]
                movie_id = movie["id"]

                with st.container(border=True):

                    # ---------------- TITLE ---------------- #

                    st.markdown(
                        f"""
                        <div style="
                        height:70px;
                        font-size:28px;
                        font-weight:700;
                        color:white;
                        overflow:hidden;
                        line-height:1.3;
                        ">
                        {movie_name}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ---------------- DETAILS ---------------- #

                    st.markdown(
                        f"""
                        <div style="
                        height:65px;
                        color:#b8b8b8;
                        font-size:15px;
                        line-height:1.6;
                        margin-top:10px;
                        overflow:hidden;
                        ">
                        {movie['year']} |
                        {movie['language']} <br>
                        {movie['genre']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ---------------- RATING ---------------- #

                    st.markdown(
                        f"""
                        <div style="
                        color:#FFD54F;
                        font-size:18px;
                        font-weight:600;
                        margin-top:10px;
                        margin-bottom:10px;
                        ">
                        ⭐ {movie['rating']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ---------------- STATUS ---------------- #

                    if movie_id in liked:

                        st.success("✓ Liked")

                    elif movie_id in disliked:

                        st.error("✕ Disliked")

                    elif movie_id in watched:

                        st.info("👁 Watched")

                    # ---------------- BUTTONS ---------------- #

                    c1, c2, c3 = st.columns(3)

                    # ---------------- LIKE BUTTON ---------------- #

                    with c1:

                        if st.button(
                            "👍 ",
                            key=f"like_{movie_id}"
                        ):

                            # REMOVE FROM DISLIKED
                            if movie_id in disliked:

                                disliked.remove(movie_id)

                            # ADD TO LIKED
                            if movie_id not in liked:

                                liked.append(movie_id)

                            # ADD TO WATCHED
                            if movie_id not in watched:

                                watched.append(movie_id)

                            save_user_data(liked,disliked,watched)
                            st.rerun()

                    # ---------------- DISLIKE BUTTON ---------------- #

                    with c2:

                        if st.button(
                            "👎 ",
                            key=f"dislike_{movie_id}"
                        ):

                            # REMOVE FROM LIKED
                            if movie_id in liked:

                                liked.remove(movie_id)

                            # ADD TO DISLIKED
                            if movie_id not in disliked:

                                disliked.append(movie_id)

                            # ADD TO WATCHED
                            if movie_id not in watched:

                                watched.append(movie_id)

                            save_user_data(liked,disliked,watched)
                            st.rerun()

                    # ---------------- WATCH BUTTON ---------------- #

                    with c3:

                        if st.button(
                            "👁 ",
                            key=f"watch_{movie_id}"
                        ):

                            # ADD TO WATCHED
                            if movie_id not in watched:

                                watched.append(movie_id)
                            
                            save_user_data(liked,disliked,watched)
                            st.rerun()

# ---------------- WATERMARK ---------------- #

st.markdown("""

<div style="
text-align:center;
margin-top:60px;
margin-bottom:20px;
color:rgba(255,255,255,0.35);
font-size:14px;
letter-spacing:1px;
font-weight:500;
">

Made by Jyothis P K

</div>

""", unsafe_allow_html=True)
