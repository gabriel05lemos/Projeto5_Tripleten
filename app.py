import pandas as pd
import streamlit as st
from plotly import express as px

color_palette = px.colors.qualitative.Alphabet

vehicles = pd.read_csv('vehicles.csv')

vehicles['brand'] = vehicles['model'].apply(lambda x: x.split()[0])

brand_order = vehicles['brand'].value_counts().index.tolist()
type_order = vehicles['type'].value_counts().index.tolist()
condition_order = ['new', 'like new', 'excellent', 'good', 'fair', 'salvage']

ordem = {
    'Condição': ['new', 'like new', 'excellent', 'good', 'fair', 'salvage'],
    'Marca': brand_order,
    'Categoria': type_order
}

caracteristica_dic = {
    'Condição': 'condition',
    'Marca': 'brand',
    'Categoria': 'type'
}


avg_price_year = vehicles.groupby('model_year')['price'].mean().reset_index()

type_counts = vehicles.groupby(['brand', 'type']).size().reset_index(name='count')

st.header('📊 Análise de Anúncios de Carros')

st.write(
    '''
    Nessa página fornecemos visualizações ods dados de anúncios de carros à venda em uma plataforma americana. Analisamos como diferentes características dos carros (preço, ano, modelo, condição, marca) afetam umas as outras.
    '''
)

st.subheader('🚗 Como o Hodômetro Afeta o Preço do Carro?')

st.write(
    '''
    Naturalmente, quando mais Km tem um carro, mais "usado" ele é e então deveria possuir um preço menor em relação a um com menos distância. Mas será que isso se verifica de fato? E como isso é diferente para diferentes categorias (SUV, sedan, caminhonete...)? O gráfico a seguir revela essas relações. 
    '''
)

fig = px.scatter(
    vehicles[~vehicles["odometer"].isna()], 
    x="odometer", 
    y="price", 
    color="type", 
    title="Preço vs. Hodômetro",
    labels={'odometer': 'Hodômetro', 'price': 'Preço', 'type': 'Categoria'},
    category_orders={"type": type_order},
    color_discrete_sequence=color_palette
)

st.plotly_chart(fig, width='stretch')

st.subheader('🛠️ Como a Condição do Veículo Afeta os Dias em Anúncio?')

st.write(
    '''
    Será que carros mais bem cuidados são vendidos mais rapidamente? E os menos cuidados demoram mais para vender? Esse gráfico mostra a distribuição de dias para as diferentes condições de manutenção. 
    '''
)

fig = px.box(
    vehicles, 
    x="condition", 
    y="days_listed", 
    title="Days Listed by Condition",
    width=800,
    height=800,
    labels={'days_listed': 'Dias de Anúncio', 'condition': 'Condição do Veículo'},
    category_orders={"condition": condition_order}
)

st.plotly_chart(fig, width='stretch')

st.subheader('📈 Como o Ano do Carro Afeta o Preço?')

st.write(
    '''
    Será que carros mais novos custam mais e os carros mais velhos menos? E os carros de colecionador. Quando será que um carro velho se torna "vintage"? No gráfico a seguir, exploramos essa questão. Escolha um intervalo de anos e analise o preço médio dos carros nesse intervalo.
    '''
)

intervalo = st.slider(
    'Selecione um intervalo:',
    min_value=1908,
    max_value=2019,
    value=(1908, 2019) 
)

fig = px.line(
    avg_price_year[avg_price_year['model_year'].between(*intervalo)], 
    x="model_year", 
    y="price", 
    title="Preço Médio por Ano",
    labels={'price': 'Preço', 'model_year': 'Ano do Carro'}
)

st.plotly_chart(fig, width='stretch')

st.subheader('🏷️ Quais Características Afetam a Distribuição de Preços?')

st.write(
    '''
    Como que a distribuição dos preços variam conforme diferentes características? Os carros em melhor condição tem uma distribuição de preços diferente dos demais? E as SUVs? Será que exite diferença entre os preços da Chevrolet e Ford. No próximo gráfico, você poderá construir histogramas para avaliar essas diferenças. Selecione uma característica para avaliar e gere o gráfico!
    '''
)

caracteristica = st.selectbox(
    'Selecione a Característica',
    ['Condição', 'Marca', 'Categoria']
)

fig = px.histogram(
    vehicles, 
    x="price", 
    color=caracteristica_dic[caracteristica], 
    title=f"Distribuição dos Preços por {caracteristica}",
    category_orders={caracteristica_dic[caracteristica]: ordem[caracteristica]},
    labels={
        'price': 'Preço', 
        'condition': 'Condição do Veículo',
        'brand': 'Marca',
        'type': 'Categoria'
    },
    color_discrete_sequence=color_palette
)

fig.update_layout(yaxis_title='Quantidade de Anúncios')
st.plotly_chart(fig, width='stretch')

st.subheader('🏢 Quantos Carros de Cada Empresa e Categoria Foram Anunciados?')

st.write(
    '''
    Será que os americanos tem alguma preferência em relação às marcas de carro? E em relação às diferentes categorias? Nesse próximo gráfico você poderá comparar as quantidades de veículoas anunciados por marca e por categoria.
    '''
)

fig = px.bar(
    type_counts, 
    x="brand", 
    y="count", 
    color="type",
    title="Categorias de Veículos por Marca",
    labels={'brand': 'Marca', 'count': 'Quantidade de Anúncios', 'type': 'Categoria'},
    category_orders={"brand": brand_order, "type": type_order},
    color_discrete_sequence=color_palette,
    height=600
)

st.plotly_chart(fig, width='stretch')