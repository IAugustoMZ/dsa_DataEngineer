import pandas as pd
import plotly.express as px
from src.auth.auth import AuthHandler
from src.model.filters.filter import Filter
from src.controller.database.quality_olap import QualityDatabaseQueryHandler

class AppPagesViews:
    def __init__(self, query_handler: QualityDatabaseQueryHandler) -> None:
        """
        app pages views

        Parameters
        ----------
        query_handler : QualityDatabaseQueryHandler
            query handler
        """
        self.query_handler = query_handler
    
    def main_screen(self) -> None:
        """
        main screen
        """

        # sidebar
        st.sidebar.title('Quality Management System')
        st.sidebar.markdown('---')
        st.sidebar.title('Select Filters')

        # date range
        start_date = st.sidebar.date_input('Start Date').strftime('%Y-%m-%d')
        end_date = st.sidebar.date_input('End Date').strftime('%Y-%m-%d')

        # production line
        production_lines = self.query_handler.get_production_line()
        selected_production_line = st.sidebar.selectbox('Production Line', production_lines)

        # standard main screen
        st.title('Quality Management System')
        st.markdown('---')
        st.write('Please select the filters on the sidebar and click on the button below to apply the filter.')

        # fill tab 1
        if st.sidebar.button('Apply Filter'):

            # create filter
            filter = Filter(start_date=start_date, end_date=end_date, production_line=selected_production_line)

            # main screen
            tab1, tab2 = st.tabs(['Internal Non-Conformities', 'External Non-Conformities'])

            with tab1:
                
                # cards for non-conformities
                col1, col2 = st.columns(2)

                # get total non-conformities
                total_ncs = self.query_handler.get_total_internal_ncs(filter)

                # metrics with 1000 formatting
                if type(total_ncs) == int:
                    col1.metric('Total Non-Conformities', f'{total_ncs:,}')
                else:
                    col1.metric('Total Non-Conformities', total_ncs)
                
                # get total defects cost
                total_defects_cost = self.query_handler.get_total_defects_cost(filter)

                # cost with USD XX.00 and , for 1000
                if type(total_defects_cost) == int:
                    col2.metric('Total Defects Cost', f'${total_defects_cost:,}')
                else:
                    col2.metric('Total Defects Cost', total_defects_cost)

                # time evolution chart
                st.subheader('Evolution of Defects in Time')

                # plot chart

                # get the evolution of defects
                evolution = self.query_handler.get_evolution_defects(filter)

                # plot chart with date in the x-axis and total defects in the y-axis
                if len(evolution) > 0:
                    st.plotly_chart(px.line(evolution, x='date', y='total_ncs', title='Evolution of Defects in Time'), use_container_width=True)
                else:
                    st.warning('No data available for the selected filters.')

                # most defective product
                st.subheader('Most Defective Product')

                # get most defective product
                most_defective_product = self.query_handler.get_most_defective_product(filter)

                if len(most_defective_product) > 0:
                    n = most_defective_product.shape[0]
                    st.plotly_chart(px.bar(most_defective_product, y='product_name', x='total_ncs', orientation='h', title=f'Most Defective Product ({n} products)'), use_container_width=True)
                else:
                    st.warning('No data available for the selected filters.')

                # process responsibilities and motivations
                st.subheader('Defects Distributions')
                col1, col2 = st.columns(2)

                # defects distribution by process step
                defects_by_process_step = self.query_handler.get_defects_distribution_by_process_step(filter)
                if len(defects_by_process_step) > 0:
                    col1.plotly_chart(px.bar(defects_by_process_step, x='process_step_name', y='total_ncs', title='Defects Distribution by Process Step'), use_container_width=True)
                else:
                    st.warning('No data available for the selected filters.')

                # defects distribution
                defects_distribution_by_issues = self.query_handler.get_defects_distribution_by_issues(filter)
                if len(defects_distribution_by_issues) > 0:
                    col2.plotly_chart(px.bar(defects_distribution_by_issues, x='issue_name', y='total_ncs', title='Defects Distribution by Issues'), use_container_width=True)
                else:
                    st.warning('No data available for the selected filters.')

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

                # plot map
                st.bar_chart([1, 2, 3, 4, 5])

    def show_pages(self) -> None:
        """
        show pages
        """
        self.main_screen()
