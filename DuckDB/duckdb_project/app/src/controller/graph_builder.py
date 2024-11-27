import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class GraphBuilder:
    def __init__(self):
        """
        class to build graphs
        """

    def build_line_chart(self, df: pd.DataFrame, x: str, y: str, x_title: str, y_title: str) -> go.Figure:
        """
        builds a line chart

        Args:
        -----
        df (pd.DataFrame):
            dataframe
        x (str):
            x axis column name
        y (str):
            y axis column name
        x_title (str):
            x axis title
        y_title (str):
            y axis title

        Returns:
        --------
        go.Figure:
            line chart
        """
        # ensure the dataframe is ordered by the x axis
        df = df.sort_values(by=x)

        # if data is empty, return an empty figure
        if df.empty:
            return go.Figure()

        fig = px.line(df, x=x, y=y)

        # put the x axis name and the y axis name
        fig.update_xaxes(title_text=x_title)
        fig.update_yaxes(title_text=y_title)

        # put the markers
        fig.update_traces(mode='markers+lines')

        # put data labels
        fig.update_traces(textposition='top center')

        return fig
    
    def build_bar_chart(self, df: pd.DataFrame, x: str, y: str, x_title: str, y_title: str) -> go.Figure:
        """
        builds a bar chart

        Args:
        -----
        df (pd.DataFrame):
            dataframe
        x (str):
            x axis column name
        y (str):
            y axis column name
        x_title (str):
            x axis title
        y_title (str):
            y axis title

        Returns:
        --------
        go.Figure:
            bar chart
        """
        # if data is empty, return an empty figure
        if df.empty:
            return go.Figure()

        fig = px.bar(df, x=x, y=y)

        # put the x axis name and the y axis name
        fig.update_xaxes(title_text=x_title)
        fig.update_yaxes(title_text=y_title)

        return fig
    
    def build_h_bar_chart(self, df: pd.DataFrame, x: str, y: str, x_title: str, y_title: str) -> go.Figure:
        """
        builds a horizontal bar chart

        Args:
        -----
        df (pd.DataFrame):
            dataframe
        x (str):
            x axis column name
        y (str):
            y axis column name
        x_title (str):
            x axis title
        y_title (str):
            y axis title

        Returns:
        --------
        go.Figure:
            horizontal bar chart
        """
        # if data is empty, return an empty figure
        if df.empty:
            return go.Figure()

        fig = px.bar(df, x=y, y=x, orientation='h')

        # put the x axis name and the y axis name
        fig.update_xaxes(title_text=x_title)
        fig.update_yaxes(title_text=y_title)

        return fig
    
    def build_pie_chart(self, df: pd.DataFrame, names: str, values: str) -> go.Figure:
        """
        builds a pie chart

        Args:
        -----
        df (pd.DataFrame):
            dataframe
        names (str):
            names column name
        values (str):
            values column name

        Returns:
        --------
        go.Figure:
            pie chart
        """
        # if data is empty, return an empty figure
        if df.empty:
            return go.Figure()

        fig = px.pie(df, names=names, values=values)

        # add percentage
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # remove legend
        fig.update_layout(showlegend=False)

        return fig