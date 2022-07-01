import streamlit as st

#INITIALIZE SESSION STATE

"""
This page is very important. The variable light regulates the pages process. When it is set to red, it does not allow the user to move on.
This is useful because you can put conditions on the "color" of the light. 
When the user is authenticated, for example, the light turns green and the next button works. The same for levels in the game.
Warning is set generally, but for each error you can modify the text to be more precise. That's why you will see this variable in different pages.

Next_page is used to navigate around the app. Retry is used to reload the page of the game for each level, if the level is not completed correctly.

In retry, the variable num represents the different screens in the game for each level. To maintain the state of the variables, in streamlit it is efficient to navigate the pages. 
Thus we created subpages within each page of the different levels, represented by a class(see game.py) and regulated by num.
The num variable is updated differently by page because different subpages are created for each level but they are all linked by the same variables. Therefore, both num and data are linked together. 
This makes this part quite counterintuitive, but it is the only solution to Streamlit's features. 
"""

if "light" not in st.session_state:
    st.session_state.light= "red"
if "warning" not in st.session_state:
    st.session_state.warning= "Undefined Error"

if 'num' not in st.session_state:
    st.session_state.num = 1
######################################################################

def next_page():
    if st.session_state.light=="green":
        st.session_state.page += 1
    elif st.session_state.light=="red":
        st.warning(st.session_state.warning)



def retry():
    if st.session_state.page == 1:
        st.session_state.num = 1
    elif st.session_state.page == 2:
        st.session_state.num = 5
    else:
        st.session_state.num = 10

## Num non si restarta perchcè altrimenti tornava sullo stess livello