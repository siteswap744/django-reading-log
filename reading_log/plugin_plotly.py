import plotly.graph_objects as go
#from .seaborn_colorpalette import sns_deep
from .seaborn_colorpalette import sns_muted


class GraphGenerator:
    pie_line_color = "#000"
    plot_bgcolor = "rgb(255, 255, 255)"
    paper_bgcolor = "rgb(255, 255, 255)"
    #month_bar_color = "indianred"
    month_bar_color = "#5c94cc"
    font_color = "dimgray"
    #color_palette = sns_deep()
    color_palette = sns_muted()
    payment_color = "tomato"
    income_color = "forestgreen"

    #def month_pie(self, labels, values):
    #    colors = self.color_palette[0: len(labels)]

    #    fig = go.Figure()
    #    fig.add_trace(go.Pie(labels=labels,
    #                         values=values))

    #    fig.update_traces(hoverinfo="label+percent",
    #                      textinfo="value",
    #                      textfont_size=14,
    #                      marker=dict(line=dict(color=self.pie_line_color,
    #                                            width=0),
    #                                  colors=colors))

    #    fig.update_layout(
    #        margin=dict(
    #            autoexpand=True,
    #            l=20,
    #            r=0,
    #            b=0,
    #            t=30, ),
    #        height=300,
    #    )

    #    return fig.to_html(include_plotlyjs=False)

    #def month_daily_bar(self, x_list, y_list):
    #    fig = go.Figure()
    #    fig.add_trace(go.Bar(
    #        x=x_list,
    #        y=y_list,
    #        marker_color=self.month_bar_color,
    #    ))

    #    fig.update_layout(
    #        paper_bgcolor=self.paper_bgcolor,
    #        plot_bgcolor=self.plot_bgcolor,
    #        font=dict(size=14,
    #                  color=self.font_color),
    #        margin=dict(
    #            autoexpand=True,
    #            l=0,
    #            r=0,
    #            b=20,
    #            t=10, ),
    #        yaxis=dict(
    #            showgrid=False,
    #            linewidth=1,
    #            rangemode="tozero"))
    #    fig.update_yaxes(automargin=True)

    #    return fig.to_html(include_plotlyjs=False)

    def transition_plot(self,
                        #x_payment_list=None,
                        #y_payment_list=None,
                        x_books_list=None,
                        y_books_list=None):
        fig = go.Figure()

        # 支出はラインプロット
        #if x_payment_list and y_payment_list:
        #    fig.add_trace(go.Scatter(
        #        x=x_payment_list,
        #        y=y_payment_list,
        #        mode="lines",
        #        name="payment",
        #        opacity=0.5,
        #        line=dict(color=self.payment_color,
        #                  width=5, )
        #    ))

        # 冊数の推移はバープロット
        if x_books_list and y_books_list:
            fig.add_trace(go.Bar(
                x=x_books_list,
                y=y_books_list,
                name="books",
                #marker_color=self.income_color,
                opacity=0.8,
            ))

        fig.update_layout(
            xaxis_title="月",
            yaxis_title="読了ページ数",
            #paper_bgcolor=self.paper_bgcolor,
            #plot_bgcolor=self.plot_bgcolor,
            font=dict(size=14, color=self.font_color),
            margin=dict(
                autoexpand=True,
                l=0,
                r=0,
                b=20,
                t=30, ),
            yaxis=dict(
                #showgrid=False,
                linewidth=1,
                rangemode="tozero"
            ))

        #fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=True, fixedrange=True)
        fig.update_yaxes(automargin=True)
        #fig.update_xaxes(gridcolor="gray", griddash="dot")
        #fig.update_yaxes(gridcolor="gray", griddash="dash")
        return fig.to_html(include_plotlyjs=False)
