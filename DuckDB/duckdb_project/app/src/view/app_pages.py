import pandas as pd
import streamlit as st
from src.auth.auth import AuthHandler
from src.model.filters.filter import Filter
from src.controller.database.quality_olap import QualityDatabaseQueryHandler

class AppPagesViews:
    def __init__(self):
        """
        app pages views
        """
        self.database_handler = QualityDatabaseQueryHandler()

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
        start_date = st.sidebar.date_input('Start Date').strftime('%Y-%m-%d') 
        end_date = st.sidebar.date_input('End Date').strftime('%Y-%m-%d') 

        # get production line and product
        production_lines = self.database_handler.get_production_line()
        production_line = st.sidebar.selectbox('Production Line', production_lines)

        products = self.database_handler.get_products()
        product = st.sidebar.selectbox('Product', products)

        # create and validate filter
        filter = Filter(start_date=start_date, end_date=end_date, production_line=production_line, product=product)
        print(filter)

        # create a small chat box so the user can interact with an LLM
        st.sidebar.subheader('Chat with LLM')
        message = st.sidebar.text_input('Message')
        if st.sidebar.button('Send'):
            # clean previous messages
            st.sidebar.text('User: ' + message)

            st.sidebar.text('LLM: Hi, how can I help you?')

        # main screen
        tab1, tab2 = st.tabs(['Internal Non-Conformities', 'External Non-Conformities'])

        # fill tab 1
        with tab1:
            
            # cards for non-conformities
            col1, col2 = st.columns(2)

            total_ncs = self.database_handler.get_total_internal_ncs(filter)

            col1.metric('Total Non-Conformities', total_ncs)
            col2.metric('Total Defects Cost', 1000)

            # time evolution chart
            st.subheader('Evolution of Defects in Time')

            # find granularity
            granularity = st.radio('Select Granularity', ['Yearly', 'Monthly', 'Daily'], horizontal=True, key='granularity')

            # plot chart
            st.line_chart([1, 2, 3, 4, 5])

            # most defective product
            st.subheader('Most Defective Product')
            st.bar_chart([1, 2, 3, 4, 5])

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

        # fill tab 2
        with tab2:
            
            # cards for non-conformities
            col1, col2, col3 = st.columns(3)
            col1.metric('Total Non-Conformities', 100)
            col2.metric('Total Defects Cost', 1000)
            col3.metric('Key Account Fraction', '50%')

            # time evolution chart
            st.subheader('Evolution of Defects in Time')

            # most defective product
            st.subheader('Most Defective Product')
            st.bar_chart([1, 2, 3, 4, 5])

            # find granularity
            granularity = st.radio('Select Granularity', ['Yearly', 'Monthly', 'Daily'], horizontal=True)

            # plot chart with two series
            st.line_chart({
                'Internal': [1, 2, 3, 4, 5],
                'External': [5, 4, 3, 2, 1]
            })

            # defects distributions
            st.subheader('Evolution of Defects in Time')

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

            # geographical distribution
            st.subheader('Geographical Analysis')

            # toggle analysis by city or state
            analysis_by = st.radio('Select Analysis', ['City', 'State'], key='geo', horizontal=True)

            # plot map
            st.bar_chart([1, 2, 3, 4, 5])




    def show_pages(self) -> None:
        """
        show pages based on session state
        """
        # if 'logged_in' not in st.session_state:
        #     st.session_state.logged_in = False

        # if not st.session_state.logged_in:
        #     self.login_page()
        # else:
        #     self.main_screen()
        self.main_screen()
