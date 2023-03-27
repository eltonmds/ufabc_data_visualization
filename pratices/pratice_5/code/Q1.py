from bokeh.io.output import output_file

try:
    import yfinance as yf
except ModuleNotFoundError:
    get_ipython().system('pip install yfinance')

import pandas as pd, numpy as np, yfinance as yf  
from datetime import date, timedelta
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, RangeTool, VBar
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
output_notebook()  # Indicando que a saída Bokeh é para o COLAB

# Microsoft - MSFT
# ORACLE - ORCL
# Diferença percentual do preço de abertura e fechamento diário de ambos os ativos nos últimos 2 meses e volume de negociações por dia

# Seta a data de hoje (fim)
hoje = date.today()
data_ate = hoje.strftime("%Y-%m-%d")
# Seta a data de 2 meses atras (começo)
daux = date.today() - timedelta(days=60)
data_de = daux.strftime("%Y-%m-%d")

# Acessa o YAHOO FINANCE e capturas as cotações DIÁRIAS da Microsoft.
data_MS = yf.download('MSFT', start=data_de,  end=data_ate, progress=False)
data_MS = data_MS.reset_index(['Date'])  
faixaDatas = np.array(data_MS['Date'].dt.date, dtype=np.datetime64)

# Acessa o YAHOO FINANCE e capturas as cotações DIÁRIAS da Oracle.
data_OC = yf.download('ORCL', start=data_de,  end=data_ate, progress=False)
data_OC = data_OC.reset_index(['Date'])  
faixaDatas = np.array(data_OC['Date'].dt.date, dtype=np.datetime64)

# calcula a diferença percentual 
data_MS["percentual_dif"] = (data_MS['Close'] - data_MS['Open']) / data_MS['Open'] * 100
data_OC["percentual_dif"] = (data_OC['Close'] - data_OC['Open']) / data_OC['Open'] * 100

source_MS = ColumnDataSource(data = dict(datas = faixaDatas, valor = data_MS['percentual_dif']))
source_OC = ColumnDataSource(data = dict(datas = faixaDatas, valor = data_OC['percentual_dif']))

bar_ms_volume = ColumnDataSource(dict(datas = faixaDatas, valor = data_MS['Volume'] / 1000000))
bar_oc_volume = ColumnDataSource(dict(datas = faixaDatas, valor = data_MS['Volume'] / 1000000))

# Grafico de linhas principal
p = figure(height=500, width=1300, tools="xpan", toolbar_location=None, title = "Diferença Percentual Abertura x Fechamento Microsoft e Oracle",
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(faixaDatas[0], faixaDatas[len(faixaDatas)-1]))

# Adiciona cada linha a ser plotada
p.line('datas', 'valor', source=source_MS, legend_label = "Microsoft", line_color='green')
p.line('datas', 'valor', source=source_OC, legend_label = "Oracle", line_color='red')

p.yaxis.axis_label = 'Percentual'

# Configura BOX de seleção para detalhar porções 
select = figure(title="Para mais detalhes, ajuste o box de seleção",
                height=100, width=1300, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "gray"
range_tool.overlay.fill_alpha = 0.4

select.line('datas', 'valor', source=source_MS, line_color = 'green')
select.line('datas', 'valor', source=source_OC, line_color = 'red')
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool


# Gráfico de barras do volume da Microsoft
bar_ms = figure(title = "Volume Microsoft",height=300, width=1300, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(faixaDatas[0], faixaDatas[len(faixaDatas)-1]))

bar_ms.yaxis.axis_label = "Volume (Milhões)"
bar_ms.vbar(x = 'datas', top = 'valor', source = bar_ms_volume, color = 'green', width=timedelta(days=0.5))
bar_ms.add_tools(range_tool)
bar_ms.toolbar.active_multi = range_tool

# Gráfico de barra do volume da oracle
bar_oc = figure(title = 'Volume Oracle',height=300, width=1300, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(faixaDatas[0], faixaDatas[len(faixaDatas)-1]))

bar_oc.yaxis.axis_label = "Volume (Milhões)"
bar_oc.vbar(x = 'datas', top = 'valor', source = bar_oc_volume, color = 'red', width=timedelta(days=0.5))
bar_oc.add_tools(range_tool) # funcionalidade do range no grafico de barras da oracle
bar_oc.toolbar.active_multi = range_tool

# Apresenta VIS + Box
show(column(p, select, bar_ms, bar_oc))
output_file('Dashboard.html')
