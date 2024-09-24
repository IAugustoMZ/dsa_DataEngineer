import pandas as pd
import streamlit as st
from src.auth.auth import AuthHandler

class AppPagesViews:
    def __init__(self):
        """
        app pages views
        """
        pass

    def login_page(self) -> None:
        """
        login page
        """
        st.title('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            auth_handler = AuthHandler()
            if auth_handler.login(username, password):
                st.success('Login successful')
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error('Invalid username or password')
    
    def main_screen(self) -> None:
        """
        main screen
        """
        # side bar report options
        st.sidebar.title('Navigation')
        start_date = st.sidebar.date_input('Start Date')
        end_date = st.sidebar.date_input('End Date')
        production_line = st.sidebar.selectbox('Production Line', ['Line 1', 'Line 2', 'Line 3'])

        # main screen
        tab1, tab2 = st.tabs(['Internal Non-Conformities', 'External Non-Conformities'])

        # fill tab 1
        with tab1:
            
            # cards for non-conformities
            col1, col2, col3 = st.columns(3)
            col1.metric('Total Non-Conformities', 100)
            col2.metric('Product with Most Defects', 'Product A')
            col3.metric('Total Defects Cost', 1000)

            # time evolution chart
            st.subheader('Evolution of Defects in Time')

            # find granularity
            granularity = st.radio('Select Granularity', ['Yearly', 'Monthly', 'Daily'])

            # plot chart
            st.line_chart([1, 2, 3, 4, 5])

            # process responsibilities and motivations
            st.subheader('Defects Distributions')
            col1, col2 = st.columns(2)
            col1.bar_chart([1, 2, 3, 4, 5])

            # defects distribution
            col2.bar_chart([1, 2, 3, 4, 5])

            # distribution of reasons
            st.subheader('Distribution of Defects Motivations')
            col1, col2 = st.columns(2)
            reasons_8ms = {
                'Man': 10, 'Machine': 15, 'Material': 20, 'Method': 5,
                'Measurement': 10, 'Mother Nature': 8, 'Management': 12, 'Maintenance': 7
            }
            col1.bar_chart(pd.Series(reasons_8ms))

            recurring_problems = {
                'Yes': 20, 'No': 5
            }
            col2.bar_chart(pd.Series(recurring_problems))


    def show_pages(self) -> None:
        """
        show pages based on session state
        """
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            self.login_page()
        else:
            self.main_screen()
