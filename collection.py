import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from streamlit_option_menu import option_menu
import os



def request(url: str, bearer: str, account: str) -> pd.DataFrame:
    headers = {"Authorization": f"Bearer {bearer}"}

    if url.endswith("Log__Trading_history"):
        params = {"filter[Account][_eq]": account, "limit": -1}
    elif url.endswith("log_balance") or url.endswith("log__drawdown_tracking") or url.endswith("log_estatistica") or url.endswith("log_trading"):
        params = {"filter[account_number][_eq]": account, "limit": -1}
    elif url.endswith("Log__Pnl"):
        params = {"filter[Account_number][_eq]": account, "limit": -1}
    elif url.endswith("coreops_accounts"):
        params = {"filter[account_number][_eq]": account, "limit": 1}
    else:
        params = {}

    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", [])
        return pd.DataFrame(data)
    except requests.HTTPError as e:
        st.error(f"Erro: {e}")
        return pd.DataFrame()


def indicador_card(titulo, valor):
    fig = go.Figure(go.Indicator(
        mode="number",
        value=valor,
        number={"font": {"size": 36}},
        title={"text": f"<b>{titulo}</b>", "font": {"size": 16}}
    ))
    fig.update_layout(
        height=160,
        margin=dict(t=20, b=10, l=10, r=10),
        template="simple_white"
    )
    return fig


def main():
    st.set_page_config(page_title="PropHub", layout="wide")

    if "env" not in st.session_state:
        st.session_state.env = "blueberry"

    st.markdown(
    """
    <style>
    /* Global adjustments for a sleek dark theme */
    body {
        background-color: #1a1a2e; /* Darker, more neutral background */
        color: #e0e0e0; /* Lighter text for contrast */
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Main Title - PropHub */
    .main-title {
        font-size: 68px; /* Slightly larger for impact */
        font-weight: 700; /* Bolder */
        color: #400705; /* White/off-white for main title */
        text-align: center;
        margin-bottom: 5px; /* Reduced space to subtitle */
        letter-spacing: 2px; /* A bit of letter spacing for elegance */
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); /* Subtle text shadow for depth */
        background: linear-gradient(90deg, #400705, #9f5d59); /* Gradient for a modern touch */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }

    /* Subtitle - Dashboard de Verificação das Coleções do Directus */
    .sub-title {
        font-size: 26px; /* Slightly larger and more prominent */
        color: #a0a0a0; /* Softer grey for subtitle */
        text-align: center;
        margin-bottom: 50px; /* More space below the subtitle */
        font-weight: 300; /* Lighter font weight for elegance */
        letter-spacing: 0.8px;
        line-height: 1.5;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); /* Very subtle shadow */
    }

    /* Info Card - (If you decide to use it later, example refined style) */
    .info-card {
        background-color: #2a2a3e; /* Darker, sophisticated background for cards */
        padding: 20px;
        border-radius: 12px; /* Softer rounded corners */
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3); /* More pronounced, soft shadow */
        margin-bottom: 20px;
        border: 1px solid #3c3c5a; /* Subtle border for definition */
    }

    /* Section Title - (If you decide to use it later, example refined style) */
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #f0f2f6; /* Matching main title color for hierarchy */
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 2px solid #3a3a4e; /* Subtle underline effect */
        padding-bottom: 5px;
        letter-spacing: 1px;
    }
    </style>
    <div class="main-title">PropHub</div>
    <div class="sub-title">Dashboard de Verificação das Coleções do Directus</div>
    """,
    unsafe_allow_html=True,
    )

    # ─── Novo CSS para o seletor ────────────────────────────────────────
    st.markdown(
    """
    <style>
    /* Container centralizado com padding e sombra suave */
    [data-testid="stRadio"] > div {
        display: flex !important;
        justify-content: center;
        gap: 20px; /* Mais espaço entre os botões */
        margin-bottom: 40px;
        padding: 12px;
        border-radius: 18px; /* Cantos mais arredondados para um visual suave */
        background: #25252b; /* Fundo mais escuro e elegante */
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); /* Sombra mais profunda */
        border: 1px solid #3a3a42; /* Borda sutil para definição */
    }

    /* Esconde o círculo padrão do rádio */
    [data-testid="stRadio"] input[type="radio"] {
        display: none;
    }

    /* Cada label vira um "botão" customizado */
    [data-testid="stRadio"] label > span {
        position: relative;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 16px 36px; /* Mais preenchimento para um toque premium */
        border-radius: 12px; /* Cantos arredondados nos botões */
        background: #303036; /* Cor de fundo padrão do botão */
        color: #c0c0c0; /* Cor de texto padrão, mais clara */
        font-size: 20px; /* Fonte ligeiramente maior */
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease; /* Transições suaves para todos os efeitos */
        border: 1px solid #45454d; /* Borda sutil para cada botão */
        letter-spacing: 0.5px; /* Espaçamento leve entre letras */
    }

    /* Bolinha custom antes do texto */
    [data-testid="stRadio"] label > span::before {
        content: "";
        width: 18px; /* Bolinha maior */
        height: 18px;
        border: 2px solid #777; /* Borda da bolinha */
        border-radius: 50%;
        background: transparent;
        transition: border-color 0.3s, background 0.3s;
        box-shadow: inset 0 0 0 2px #303036; /* Sombra interna para profundidade */
    }

    /* Hover sobre o "botão" */
    [data-testid="stRadio"] label:hover > span {
        background: #3c3c43; /* Fundo mais claro no hover */
        color: #ffffff; /* Texto branco no hover */
        transform: translateY(-3px); /* Leve levantamento */
        box-shadow: 0 5px 15px rgba(0,0,0,0.4); /* Sombra mais visível no hover */
    }

    /* Estado selecionado: fundo diferenciado + texto branco */
    [data-testid="stRadio"] label[data-selected="true"] > span {
        background: #6a057d; /* Um roxo profundo para o estado selecionado */
        color: #ffffff; /* Texto branco puro */
        border-color: #6a057d; /* Borda combinando */
        box-shadow: 0 6px 16px rgba(106, 5, 125, 0.5); /* Sombra vibrante para destaque */
        transform: translateY(-1px); /* Mantém um leve levantamento */
    }
    /* Bolinha preenchida no selecionado */
    [data-testid="stRadio"] label[data-selected="true"] > span::before {
        background: #ffffff; /* Preenchimento branco */
        border-color: #ffffff; /* Borda branca */
        box-shadow: none; /* Remove a sombra interna quando preenchida */
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    # --- Seletor de Empresa customizado ────────────────────────────────
    env_keys = ["blueberry","p4f","demo"]
    empresa = st.radio(
        "",
        env_keys,
        key="env",
        horizontal=True,
        format_func=lambda x: {
            "blueberry": "Blueberry",
            #"horizon":   "Horizon",
            "p4f":       "P4F",
            "demo":"Demo"
        }[x]
    )


    # ─── Carrega .env conforme seleção ─────────────────────────────────
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=f".env.{empresa}", override=True)

    ESTATISTICA       = os.getenv("URL_ENVIO_ESTATISTICA")
    DRAWDOWN_TRACKING = os.getenv("URL_ENVIO_DRAWDOWN_TRACKING")
    BALANCE           = os.getenv("URL_ENVIO_BALANCE")
    ORDENS            = os.getenv("URL_ENVIO_TRADING")
    TRADING_HISTORY   = os.getenv("URL_TRADING_HISTORY")
    PNL               = os.getenv("URL_LOG_PNL")
    COREOPS_ACCOUNTS  = os.getenv("URL_COREOPS_ACCOUNTS")
    BEARER            = os.getenv("BEARER_BB__PROD__")

    account = st.text_input("Digite o Account Number:", "1919349374881500200")

    if account:

        df1 = request(url=TRADING_HISTORY, bearer=BEARER, account=account)
        df2 = request(url=BALANCE, bearer=BEARER, account=account)
        df3 = request(url=PNL, bearer=BEARER, account=account)
        df4 = request(url=DRAWDOWN_TRACKING, bearer=BEARER, account=account)
        df5 = request(url=ESTATISTICA, bearer=BEARER, account=account)
        df6 = request(url=ORDENS,bearer=BEARER,account=account)
        df_info = request(url=COREOPS_ACCOUNTS, bearer=BEARER, account=account)

        if not df_info.empty:
            with st.expander("📌 Informações da Conta", expanded=True):
                info = df_info.iloc[0]
                cols = st.columns(3)
                cols[0].markdown(f"""<div class='info-card'><strong>Status:</strong> {info.get('status', '-')}</div>""",
                                 unsafe_allow_html=True)
                cols[1].markdown(f"""<div class='info-card'><strong>Tipo:</strong> {info.get('title', '-')}</div>""",
                                 unsafe_allow_html=True)
                cols[2].markdown(f"""<div class='info-card'><strong>Broker:</strong> {info.get('broker', '-')}</div>""",
                                 unsafe_allow_html=True)
                cols = st.columns(3)
                cols[0].markdown(
                    f"""<div class='info-card'><strong>Plataforma:</strong> {info.get('trading_platform', '-')}</div>""",
                    unsafe_allow_html=True)
                cols[1].markdown(
                    f"""<div class='info-card'><strong>Saldo Inicial:</strong> {info.get('initial_balance', '-')}</div>""",
                    unsafe_allow_html=True)
                cols[2].markdown(
                    f"""<div class='info-card'><strong>Saldo Atual:</strong> {info.get('current_balance', '-')}</div>""",
                    unsafe_allow_html=True)

        colecoes = {
            "Trading History": df1,
            "Balance": df2,
            "PnL": df3,
            "Drawdown Tracking": df4,
            "Estatística": df5,
            "Ordens":df6
        }

        aba = option_menu(
            menu_title=None,
            options=list(colecoes.keys()),
            icons=["bar-chart", "credit-card", "cash-coin", "exclamation-triangle", "calculator"],
            orientation="horizontal"
        )

        df = colecoes[aba]

        st.subheader(f"Coleção: {aba}")
        st.plotly_chart(indicador_card("Total de Linhas", len(df)), use_container_width=True)

        if not df.empty:
            st.dataframe(df)

            if aba == "Trading History":
                # Processar e converter dados
                df_trading = df.copy()

                # Convertendo colunas de data e numéricas
                date_cols = ['date_created', 'date_updated', 'Opentime', 'Closetime']
                for col in date_cols:
                    if col in df_trading.columns:
                        df_trading[col] = pd.to_datetime(df_trading[col], errors='coerce')

                numeric_cols = ['Openprice', 'Closeprice', 'Duration', 'Lots', 'Ticks', 'Initial_Balance']
                for col in numeric_cols:
                    if col in df_trading.columns:
                        df_trading[col] = pd.to_numeric(df_trading[col], errors='coerce')

                st.markdown("<div class='section-title'>Análise de Trading</div>", unsafe_allow_html=True)

                # 1. Distribuição de operações por ativo
                if 'Asset' in df_trading.columns:
                    st.write("### Distribuição de Operações por Ativo")
                    fig_assets = px.pie(df_trading, names='Asset', title='Distribuição por Ativo')
                    fig_assets.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_assets, use_container_width=True)

                # 2. Análise de operações por direção (Side)
                if 'Side' in df_trading.columns:
                    st.write("### Análise por Direção de Operação")
                    cols = st.columns(2)

                    # Contagem por direção
                    side_count = df_trading['Side'].value_counts().reset_index()
                    side_count.columns = ['Side', 'Count']
                    fig_side = px.bar(side_count, x='Side', y='Count',
                                      color='Side', text='Count',
                                      title='Quantidade de Operações por Direção')
                    cols[0].plotly_chart(fig_side, use_container_width=True)

                    # Análise cruzada de Asset por Side
                    if 'Asset' in df_trading.columns:
                        asset_side = pd.crosstab(df_trading['Asset'], df_trading['Side'])
                        fig_asset_side = px.bar(asset_side,
                                                title='Distribuição de Direção por Ativo',
                                                labels={'value': 'Quantidade', 'variable': 'Direção'})
                        cols[1].plotly_chart(fig_asset_side, use_container_width=True)

                # 3. Análise de preços
                if all(col in df_trading.columns for col in ['Openprice', 'Closeprice']):
                    st.write("### Análise de Preços")

                    # Calcular P&L bruto por operação
                    if 'Side' in df_trading.columns:
                        df_trading['PnL_points'] = df_trading.apply(
                            lambda x: (x['Closeprice'] - x['Openprice']) if x['Side'] == 'BUY'
                            else (x['Openprice'] - x['Closeprice']) if x['Side'] == 'SELL'
                            else 0, axis=1
                        )

                        # Gráfico de P&L por operação ao longo do tempo
                        if 'date_created' in df_trading.columns:
                            df_pnl_time = df_trading.sort_values('date_created')
                            df_pnl_time['cumulative_pnl'] = df_pnl_time['PnL_points'].cumsum()

                            fig_pnl = px.line(df_pnl_time, x='date_created', y='cumulative_pnl',
                                              title='P&L Cumulativo ao Longo do Tempo (em pontos)',
                                              labels={'cumulative_pnl': 'P&L Cumulativo', 'date_created': 'Data'})
                            st.plotly_chart(fig_pnl, use_container_width=True)

                    # Distribuição de preços de abertura e fechamento
                    cols = st.columns(2)
                    fig_open = px.histogram(df_trading, x='Openprice',
                                            title='Distribuição de Preços de Abertura',
                                            labels={'Openprice': 'Preço de Abertura', 'count': 'Frequência'})
                    cols[0].plotly_chart(fig_open, use_container_width=True)

                    fig_close = px.histogram(df_trading, x='Closeprice',
                                             title='Distribuição de Preços de Fechamento',
                                             labels={'Closeprice': 'Preço de Fechamento', 'count': 'Frequência'})
                    cols[1].plotly_chart(fig_close, use_container_width=True)

                # 4. Análise de duração das operações
                if 'Duration' in df_trading.columns:
                    st.write("### Análise de Duração das Operações")

                    # Histograma de duração
                    fig_duration = px.histogram(df_trading, x='Duration',
                                                title='Distribuição da Duração das Operações',
                                                labels={'Duration': 'Duração (s)', 'count': 'Frequência'},
                                                nbins=20)
                    st.plotly_chart(fig_duration, use_container_width=True)

                    # Duração x Resultado
                    if 'PnL_points' in df_trading.columns:
                        fig_dur_pnl = px.scatter(df_trading, x='Duration', y='PnL_points',
                                                 color='Side', title='Relação entre Duração e Resultado',
                                                 labels={'Duration': 'Duração (s)', 'PnL_points': 'Resultado (pontos)'})
                        st.plotly_chart(fig_dur_pnl, use_container_width=True)


                # 6. Análise de volume (Lots)
                if 'Lots' in df_trading.columns:
                    st.write("### Análise de Volume")

                    # Distribuição de lotes
                    fig_lots = px.histogram(df_trading, x='Lots',
                                            title='Distribuição de Tamanho das Operações',
                                            labels={'Lots': 'Lotes', 'count': 'Frequência'})
                    st.plotly_chart(fig_lots, use_container_width=True)

                    # Volume por ativo se disponível
                    if 'Asset' in df_trading.columns:
                        asset_volume = df_trading.groupby('Asset')['Lots'].sum().sort_values(
                            ascending=False).reset_index()
                        fig_asset_vol = px.bar(asset_volume, x='Asset', y='Lots',
                                               title='Volume Total por Ativo',
                                               labels={'Asset': 'Ativo', 'Lots': 'Volume Total (lotes)'})
                        st.plotly_chart(fig_asset_vol, use_container_width=True)

                # 7. Análise por tipo de operação
                if 'Type' in df_trading.columns:
                    st.write("### Análise por Tipo de Operação")

                    type_counts = df_trading['Type'].value_counts().reset_index()
                    type_counts.columns = ['Type', 'Count']

                    fig_type = px.pie(type_counts, values='Count', names='Type',
                                      title='Distribuição por Tipo de Operação')
                    fig_type.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_type, use_container_width=True)

                    # Performance por tipo se PnL calculado
                    if 'PnL_points' in df_trading.columns:
                        type_pnl = df_trading.groupby('Type')['PnL_points'].mean().reset_index()
                        fig_type_pnl = px.bar(type_pnl, x='Type', y='PnL_points',
                                              title='P&L Médio por Tipo de Operação',
                                              labels={'Type': 'Tipo', 'PnL_points': 'P&L Médio (pontos)'})
                        st.plotly_chart(fig_type_pnl, use_container_width=True)

                # 8. Análise de horários (se disponível)
                if 'Opentime' in df_trading.columns:
                    st.write("### Análise de Horários")

                    # Adicionar hora do dia
                    df_trading['hour'] = df_trading['Opentime'].dt.hour

                    # Distribuição de operações por hora
                    hour_counts = df_trading['hour'].value_counts().sort_index().reset_index()
                    hour_counts.columns = ['Hour', 'Count']

                    fig_hour = px.bar(hour_counts, x='Hour', y='Count',
                                      title='Distribuição de Operações por Hora do Dia',
                                      labels={'Hour': 'Hora', 'Count': 'Quantidade'})
                    st.plotly_chart(fig_hour, use_container_width=True)

                    # Performance por hora se PnL calculado
                    if 'PnL_points' in df_trading.columns:
                        hour_pnl = df_trading.groupby('hour')['PnL_points'].mean().reset_index()
                        fig_hour_pnl = px.line(hour_pnl, x='hour', y='PnL_points',
                                               title='P&L Médio por Hora do Dia',
                                               labels={'hour': 'Hora', 'PnL_points': 'P&L Médio (pontos)'})
                        st.plotly_chart(fig_hour_pnl, use_container_width=True)

                # 9. Análise de Ticks (se disponível)
                if 'Ticks' in df_trading.columns:
                    st.write("### Análise de Ticks")

                    # Distribuição de ticks
                    fig_ticks = px.histogram(df_trading, x='Ticks',
                                             title='Distribuição de Ticks das Operações',
                                             labels={'Ticks': 'Ticks', 'count': 'Frequência'},
                                             nbins=20)
                    st.plotly_chart(fig_ticks, use_container_width=True)

                    # Relação entre ticks e duração
                    if 'Duration' in df_trading.columns:
                        fig_ticks_dur = px.scatter(df_trading, x='Duration', y='Ticks',
                                                   title='Relação entre Duração e Ticks',
                                                   labels={'Duration': 'Duração (s)', 'Ticks': 'Ticks'})
                        st.plotly_chart(fig_ticks_dur, use_container_width=True)

                # 10. Status da conta (se disponível)
                if 'Account_status' in df_trading.columns:
                    st.write("### Análise de Status da Conta")

                    status_counts = df_trading['Account_status'].value_counts().reset_index()
                    status_counts.columns = ['Status', 'Count']

                    fig_status = px.pie(status_counts, values='Count', names='Status',
                                        title='Distribuição por Status da Conta')
                    fig_status.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_status, use_container_width=True)

            elif aba != "Estatística":
                st.write("### Gráfico de Frequências por Data (se aplicável)")
                for col in ["date_created", "created_at", "data_ref"]:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        df_freq = df[col].dt.date.value_counts().sort_index()
                        fig = px.bar(x=df_freq.index, y=df_freq.values, labels={"x": "Data", "y": "Frequência"})
                        st.plotly_chart(fig, use_container_width=True)
                        break

            if aba == "Estatística":
                st.write("### Indicadores Estatísticos")
                row = df.iloc[0].to_dict()
                cards = []
                for key, value in row.items():
                    try:
                        valor = float(value)
                        cards.append(indicador_card(key, valor))
                    except:
                        continue

                for i in range(0, len(cards), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(cards):
                            cols[j].plotly_chart(cards[i + j], use_container_width=True)

            if aba == "Drawdown Tracking":
                df_draw = df.copy()
                df_draw['date_created'] = pd.to_datetime(df_draw['date_created'], errors='coerce')
                df_draw.sort_values(by='date_created', inplace=True)
                for col in ['dd_restante', 'saldo_atual', 'saldo_flt', 'dd_max', 'perda_max', 'max_conta', 'hwm']:
                    if col in df_draw.columns:
                        df_draw[col] = pd.to_numeric(df_draw[col], errors='coerce')

                df_balance = df2.copy()
                if 'date_created' in df_balance.columns and 'balance' in df_balance.columns:
                    df_balance['date_created'] = pd.to_datetime(df_balance['date_created'], errors='coerce')
                    df_balance['balance'] = pd.to_numeric(df_balance['balance'], errors='coerce')

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=df_draw['date_created'],
                    y=df_draw['dd_max'],
                    name='DD Máximo',
                    mode='lines',
                    line=dict(width=2.5, color='#EF553B', dash='dot'),
                    line_shape='spline'
                ))

                fig.add_trace(go.Scatter(
                    x=df_draw['date_created'],
                    y=df_draw['hwm'],
                    name='HWM',
                    mode='lines',
                    line=dict(width=2.5, color='#00CC96'),
                    line_shape='spline'
                ))

                fig.add_trace(go.Scatter(
                    x=df_draw['date_created'],
                    y=df_draw['saldo_atual'],
                    name='Saldo Atual',
                    mode='lines',
                    line=dict(width=2.5, color='#636EFA'),
                    line_shape='spline'
                ))

                fig.add_trace(go.Scatter(
                    x=df_draw['date_created'],
                    y=df_draw['saldo_flt'],
                    name='Saldo Flutuante',
                    mode='lines+markers',
                    marker=dict(size=4),
                    line=dict(width=2.5, color='#AB63FA'),
                    line_shape='spline'
                ))

                fig.update_layout(
                    template='plotly_dark',
                    margin=dict(l=20, r=20, t=30, b=30),
                    hovermode='x unified',
                    legend=dict(
                        orientation='h',
                        yanchor='top',
                        y=1.1,
                        xanchor='right',
                        x=1,
                        font=dict(size=12)
                    ),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, zeroline=False)
                )

                st.plotly_chart(fig, use_container_width=True)

            if aba == "Ordens":
                st.dataframe(df6)

        else:
            st.warning("Nenhum dado encontrado para essa coleção.")


if __name__ == "__main__":
    main()