# Description: Main app file
from src.view.app_pages import AppPagesViews

# define main app
def app_main() -> None:

    # initialize auth handler
    app = AppPagesViews()
    app.show_pages()

    return 

if __name__ == '__main__':
    
    # run app
    app_main()