import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Calculadora Patrimonial")

# Configuración de estilo de gráficos
sns.set_theme(style="darkgrid", palette="pastel") 

# Lista de ETFs
ETFs_Data = [
    {"nombre": "AZ QQQ NASDAQ 100", "simbolo": "QQQ"},
    {"nombre": "AZ SPDR S&P 500 ETF TRUST", "simbolo": "SPY"},
    {"nombre": "AZ SPDR DJIA TRUST", "simbolo": "DIA"},
    {"nombre": "AZ VANGUARD EMERGING MARKET ETF", "simbolo": "VWO"},
    {"nombre": "AZ FINANCIAL SELECT SECTOR SPDR", "simbolo": "XLF"},
    {"nombre": "AZ HEALTH CARE SELECT SECTOR", "simbolo": "XLV"},
    {"nombre": "AZ DJ US HOME CONSTRUCT", "simbolo": "ITB"},
    {"nombre": "AZ SILVER TRUST", "simbolo": "SLV"},
    {"nombre": "AZ MSCI TAIWAN INDEX FD", "simbolo": "EWT"},
    {"nombre": "AZ MSCI UNITED KINGDOM", "simbolo": "EWU"},
    {"nombre": "AZ MSCI SOUTH KOREA IND", "simbolo": "EWY"},
    {"nombre": "AZ MSCI EMU", "simbolo": "EZU"},
    {"nombre": "AZ MSCI JAPAN INDEX FD", "simbolo": "EWJ"},
    {"nombre": "AZ MSCI CANADA", "simbolo": "EWC"},
    {"nombre": "AZ MSCI GERMANY INDEX", "simbolo": "EWG"},
    {"nombre": "AZ MSCI AUSTRALIA INDEX", "simbolo": "EWA"},
    {"nombre": "AZ BARCLAYS AGGREGATE", "simbolo": "AGG"}
]

# Formulario de usuario
st.sidebar.header("Información del Usuario")
nombre = st.sidebar.text_input("Nombre")
edad = st.sidebar.number_input("Edad", min_value=1, step=1)
num_afiliacion = st.sidebar.text_input("Número de Afiliación")

# Verificación de datos de usuario
if nombre and edad and num_afiliacion:
    st.sidebar.success("Información completa. Puedes proceder con los cálculos.")
else:
    st.sidebar.warning("Por favor, completa toda la información antes de continuar.")

# Selección de ETFs (se habilita solo si se completaron los datos)
if nombre and edad and num_afiliacion:
    st.sidebar.header("Selecciona los ETFs")
    etf_nombres = [etf["nombre"] for etf in ETFs_Data]
    selected_etfs = st.sidebar.multiselect("Elige los ETFs:", etf_nombres)

    # Selección del período de análisis
    st.sidebar.header("Selecciona el periodo de tiempo")
    periodo = st.sidebar.selectbox("Periodo:", ["1mo", "3mo", "6mo", "1y", "5y", "10y"])

    # Entrada de monto de inversión
    st.sidebar.header("Monto de Inversión")
    monto_inicial = st.sidebar.number_input("Ingresa el monto a invertir:", min_value=0.0, step=100.0)

    if selected_etfs:
        # Obtener símbolos de los ETFs seleccionados
        etf_simbolos = [etf["simbolo"] for etf in ETFs_Data if etf["nombre"] in selected_etfs]

        # Descargar datos de precios ajustados
        data = yf.download(etf_simbolos, period=periodo)
        precios_cierre = data["Adj Close"]
        st.write("Precios de Cierre Ajustados:")
        st.line_chart(precios_cierre)

        # Calcular rendimiento porcentual
        rendimientos = precios_cierre.pct_change().dropna()
        st.write("Rendimientos Diarios de los ETFs:")
        st.line_chart(rendimientos)

        # Rendimiento promedio y visualización con gráfico de barras
        rendimiento_promedio = rendimientos.mean() * 100
        st.write("Rendimiento Promedio de los ETFs Seleccionados (%)")

        # Gráfico de barras estilizado
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        sns.barplot(x=rendimiento_promedio.index, y=rendimiento_promedio.values, ax=ax, palette="pastel")
        ax.set_title("Rendimiento Promedio (%)", fontsize=16, color="white")
        ax.set_xlabel("ETF", fontsize=14, color="white")
        ax.set_ylabel("Rendimiento (%)", fontsize=14, color="white")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f%%", padding=3, fontsize=10, color="white")
        sns.despine(left=True, bottom=True)
        st.pyplot(fig)

        # Rendimiento acumulado y rendimiento en términos monetarios
        if monto_inicial > 0:
            rendimiento_acumulado = (rendimientos + 1).prod() - 1
            st.write("Rendimientos Acumulados (%) en el Periodo Seleccionado")
            
            # Crear DataFrame para mostrar rendimientos acumulados
            df_rendimiento_acumulado = pd.DataFrame({
                "ETF": rendimiento_acumulado.index,
                "Rendimiento Acumulado (%)": rendimiento_acumulado.values * 100
            })

            # Mejorar la visualización de la tabla con formato condicional
            styled_df = df_rendimiento_acumulado.style.format({"Rendimiento Acumulado (%)": "{:.2f}%"}) \
                .set_properties(**{'text-align': 'center', 'color': 'white', 'background-color': '#0E1117'}) \
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#2B2B2B'), ('color', 'white'), ('font-weight', 'bold'), ('text-align', 'center')]},
                    {'selector': 'td', 'props': [('border', '1px solid #555'), ('text-align', 'center')]}
                ])

            # Mostrar la tabla estilizada
            st.dataframe(styled_df, height=200)

            # Calcular y mostrar el rendimiento basado en el monto inicial
            rendimiento_monetario = rendimiento_acumulado * monto_inicial
            st.write(f"Rendimiento en base a una inversión de {monto_inicial} en el período:")

            # Gráfico de barras para el rendimiento monetario
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            fig2.patch.set_facecolor('#0E1117')
            ax2.set_facecolor('#0E1117')
            sns.barplot(x=rendimiento_monetario.index, y=rendimiento_monetario.values, ax=ax2, palette="pastel")
            ax2.set_title(f"Rendimiento Monetario Basado en una Inversión de {monto_inicial}", fontsize=16, color="white")
            ax2.set_xlabel("ETF", fontsize=14, color="white")
            ax2.set_ylabel("Rendimiento en $", fontsize=14, color="white")
            ax2.tick_params(axis='x', colors='white')
            ax2.tick_params(axis='y', colors='white')
            for container in ax2.containers:
                ax2.bar_label(container, fmt="$%.2f", padding=3, fontsize=10, color="white")
            sns.despine(left=True, bottom=True)
            st.pyplot(fig2)
else:
    st.write("Completa tu información en la barra lateral para activar los cálculos.")




