import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set the background of the page to black
st.markdown("""
    <style>
    body {
        color: #fff;
        background-color: #000;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the CSV file
df = pd.read_csv('D:/stream1000.csv')

# Normalize ratings and classifications
df['valoracion'] = df['valoracion'].str.lower().str.replace('<', '').str.replace('>', '').str.strip()
df['clasificacion'] = df['clasificacion'].str.replace('<', '').str.replace('>', '').str.strip()

# Style settings for Markdown
titulo_principal = "color: white; font-size: 32px; font-family: Arial, sans-serif; text-decoration: underline;"
subtitulo = "color: white; font-size: 28px; font-family: Arial, sans-serif;"
etiquetas = "color: white; font-size: 18px; font-family: Arial, sans-serif;"

# Title and subtitle in Markdown with custom styles
st.markdown(f"""
    <h1 style='text-align: center; {titulo_principal}'>
    RESEÑA DE REVIEWS TRIPADVISOR
    </h1>
    <h2 style='text-align: center; {subtitulo}'>
    Parque de diversiones XCARET
    </h2>
""", unsafe_allow_html=True)

# Configure columns for layout
col1, col2 = st.columns(2)

# Function to calculate ratings percentages
def calcular_valoraciones(df):
    valoraciones = df['valoracion'].str.split(',', expand=True).stack().str.strip().value_counts()
    valoraciones = valoraciones.groupby(valoraciones.index).sum()  # Group by name
    return valoraciones / valoraciones.sum() * 100

# Calculate overall ratings percentages
valoraciones_porcentajes = calcular_valoraciones(df)

# Pie chart in column 1 for general distribution of ratings
with col1:
    st.markdown(f"<h3 style='{etiquetas}'>Distribución general de valoraciones</h3>", unsafe_allow_html=True)
    fig1, ax1 = plt.subplots()
    ax1.pie(valoraciones_porcentajes, labels=valoraciones_porcentajes.index, autopct='%1.1f%%', startangle=90,
            colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax1.axis('equal')  # Ensure it's a circle
    st.pyplot(fig1)

# Dropdown menu and bar chart in column 2
with col2:
    st.markdown(f"<h3 style='{etiquetas}'>Distribución de valoraciones por item</h3>", unsafe_allow_html=True)
    clasificaciones = ['general', 'naturaleza/atracciones', 'show', 'no clasificable', 'trato personal', 'buffet',
                       'precio', 'animales', 'transporte a hoteles', 'No disponible']
    seleccion_clasificacion = st.selectbox("Seleccione una clasificación:", clasificaciones)
    df_clasificacion = df[df['clasificacion'].str.contains(seleccion_clasificacion, na=False)]
    valoraciones_clasificacion = calcular_valoraciones(df_clasificacion)

    # Explicitly setting the figure size
    fig2, ax2 = plt.subplots(figsize=(10, 6))  # You can adjust the size as needed
    bars = ax2.bar(valoraciones_clasificacion.index, valoraciones_clasificacion, color=['#FF0000', '#FFFF00', '#008000' ])

    # Explicitly setting labels, titles, and tick parameters
    ax2.set_xlabel('Tipo de Valoración', color='white', fontsize=12)
    ax2.set_ylabel('Porcentaje (%)', color='white', fontsize=12)
    ax2.set_title('Distribución de Valoraciones por Clasificación', color='white', fontsize=14)
    ax2.tick_params(axis='x', colors='white', rotation=45)
    ax2.tick_params(axis='y', colors='white')

    # Adding bar labels
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}%', ha='center', va='bottom', color='white')

    st.pyplot(fig2)