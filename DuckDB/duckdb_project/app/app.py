# Description: Main app file
import streamlit as st
from src.model.filters.filter import Filter
from src.view.app_pages import AppPagesViews
from src.controller.database.quality_olap import QualityDatabaseQueryHandler

# query handler
query_handler = QualityDatabaseQueryHandler()

# define main app
def app_main() -> None:

    # create the app pages
    app_pages = AppPagesViews(query_handler=query_handler)

    # main screen
    app_pages.show_pages()

        
if __name__ == '__main__':

    # set page config
    st.set_page_config(page_title='Quality Management System', page_icon=':bar_chart:', layout='wide')
    
    # run app
    app_main()
