"""
    Plot graph from dataset
"""
import pandas as pd
import pygal

def excel_to_dataframe(filename):
    """
        ::: excel to Dataframe Function :::
    Parameter
        filename = read excel file and return to dataframe
    """
    dataframe = pd.read_excel(filename)
    return dataframe


def plotgraph(dataframe, name, chart_title, graph_type, x_axis_title, y_axis_title):
    """
        ::: Plotgrap Function :::
            plot graph from dataframe to *.svg file
        Parameter
            data = dataframe in format
                 ------------------------------------------------------
                | data_index |     2550    |     ....    |     2559    |
                |------------|-------------|-------------|-------------|
                |  some_text | <int,float> |     ....    | <int,float> |
                |    ....    |    ....     |     ....    |    ....     |
                |  some_text | <int,float> |     ....    | <int,float> |
                 ------------------------------------------------------
            name = name of export svg ex. europe.svg
            chart_title = title of that chart
            graph_type = type of plot include line, bar, pie
    """
    year_list = dataframe.loc[0].index.values[1:].tolist()
    col_item = dataframe[dataframe.columns[0]]
    custom_style = pygal.style.Style(
        background='transparent',
        plot_background='#FFFFFF',
    )
    chart_show_legend = len(col_item) > 1
    # checking type of graph
    if graph_type == "line":
        chart = pygal.Line(show_legend=chart_show_legend,
                           x_title=x_axis_title, y_title=y_axis_title, style=custom_style)
    elif graph_type == "bar":
        chart = pygal.Bar(show_legend=chart_show_legend, legend_at_bottom=True, x_title=x_axis_title,
                          y_title=y_axis_title, style=custom_style)
    elif graph_type == "pie":
        chart == pygal.Pie()
    #Set Chart Title
    chart.title = chart_title
    #Set X axis
    chart.x_labels = year_list
    for i in range(len(dataframe)):
        chart.add(str(col_item[i]).strip() , dataframe.loc[i][1:].astype(float))
    chart.render_to_file("chart/"+name+".svg")

def main():
    """
        main function
    """

    """ Plotgraph of continents """
    files = ["dataset/continents/"+filename.strip("\n\r") for filename in open("dataset/continents/file.txt")]
    list_continent = ['Africa', 'America', 'East asia', 'Europe', 'Middle east', 'Oceania', 'South asia']
    y_title='จำนวนนักท่องเที่ยว(คน)'
    x_title='ปีพ.ศ.'
    start_year, end_year = 2550, 2560
    list_year = [i for i in range(start_year, end_year)]
    continent_values = {}
    for continent in range(len(files)):
        dataframe = excel_to_dataframe(files[continent])
        name = list_continent[continent]
        title = 'สถิตินักท่องเที่ยวจาก '+ list_continent[continent]+ " เดินทางเข้าประเทศไทยในปี พ.ศ. 2550 - 2559."
        continent_values[list_continent[continent]] = dataframe.sum().tolist()[1:]
        plotgraph(dataframe, name, title, "line", x_title, y_title)

    """ Plotgraph of tourist each continents per year"""
    data = pd.DataFrame(continent_values, index = list_year)
    tourist_each_continent = data.transpose().reset_index()
    plotgraph(tourist_each_continent, "tourist_each_continent", "สถิตินักท่องเที่ยวแต่ละทวีปที่เดินทางเข้าประเทศไทยในปี พ.ศ. 2550 – 2559", "line", x_title, y_title)

    """ Plotgraph of all tourist per years """
    tourist_per_year = data.transpose().sum().reset_index().set_index('index').transpose()
    tourist_per_year.index = ['จำนวนนักท่องเที่ยว']
    tourist_per_year = tourist_per_year.reset_index()
    plotgraph(tourist_per_year, "tourist_per_year", "สถิตินักท่องเที่ยวชาวต่างชาติที่เดินทางเข้าประเทศไทยในปี พ.ศ. 2550 – 2559", "line", x_title, y_title)

    """ Plotgraph tourist info """
    files = [filename.strip("\n\r") for filename in open("dataset/tourist_info/file.txt")]
    title_list = ['สถิตินักท่องเที่ยวจำแนกตามช่วงอายุของเดินทางเข้าประเทศไทยในปี 2550-2559', \
                  'สถิตินักท่องเที่ยวจำแนกตามเพศที่เดินทางเข้าประเทศไทยในปี 2550-2559', \
                  'สถิตินักท่องเที่ยวจำแนกตามจำนวนครั้งการเดินทางเข้าประเทศไทยในปี 2550-2559', \
                  'สถิตินักท่องเที่ยวจำแนกตามประเภทของการเดินทางในปี 2550-2559', \
                  'สถิติรายได้จากการท่องเที่ยวเฉลี่ยต่อคนในหนึ่งวันในปี 2550-2559', \
                  'สถิติรายได้จากการท่องเที่ยวในแต่ละปีตั้งแต่ 2550-2559']
    for i in range(len(files)):
        file_name = files[i]
        dataframe = excel_to_dataframe("dataset/tourist_info/"+file_name)
        name = file_name[:file_name.find(".")]
        y_title='จำนวนนักท่องเที่ยว(คน)'
        x_title='ปีพ.ศ.'
        if i == 4:
            y_title='จำนวนเงิน(บาท)'
        if i == 5:
            y_title='จำนวนเงิน(ล้านบาท)'
        plotgraph(dataframe, name, title_list[i], "bar", x_title, y_title)
main()
