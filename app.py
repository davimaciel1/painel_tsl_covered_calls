import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Painel de Covered Calls - TSLY", layout="centered")
st.title("📈 Painel de Covered Calls - TSLY")

# Entrada do usuário
acoes_tsl = st.number_input("Quantidade de ações TSLY que você possui:", min_value=100, step=100, value=2320)
preco_acao = st.number_input("Preço atual da TSLY:", value=8.28)
strike_call = st.number_input("Strike da Call vendida:", value=9.00)
premio_call = st.number_input("Prêmio atual por ação da Call:", value=0.10)
dividendo_mensal = st.number_input("Dividendo mensal por ação:", value=0.56)
dias_para_vencimento = st.slider("Dias até o vencimento da opção:", min_value=1, max_value=30, value=5)
aporte_mensal = st.number_input("Aporte adicional mensal (opcional):", value=0.0)

# Cálculos básicos
lotes = acoes_tsl // 100
renda_opcao = lotes * premio_call * 100
renda_dividendo = acoes_tsl * dividendo_mensal
renda_total = renda_opcao + renda_dividendo

# Reinvestimento automático
acoes_novas = int((renda_total + aporte_mensal) // preco_acao)
acoes_finais = acoes_tsl + acoes_novas

# Exibição
st.markdown("---")
st.subheader("🔍 Simulação de Renda")
st.metric("Renda com opções (para {} dias)".format(dias_para_vencimento), f"US$ {renda_opcao:,.2f}")
st.metric("Renda com dividendos mensais", f"US$ {renda_dividendo:,.2f}")
st.metric("Total estimado de renda mensal", f"US$ {renda_total:,.2f}")

# Projeção anualizada simples
renda_anual = renda_total * 12
st.markdown("---")
st.subheader("📅 Projeção Anualizada")
st.metric("Renda total por ano", f"US$ {renda_anual:,.2f}")

# Reinvestimento
st.markdown("---")
st.subheader("🔁 Reinvestimento Automático")
st.metric("Ações novas que podem ser compradas", f"{acoes_novas} ações")
st.metric("Nova posição total (ações)", f"{acoes_finais}")

# Simulação de crescimento mês a mês
st.markdown("---")
st.subheader("📈 Crescimento da Posição e Renda em 12 Meses")
meses = list(range(1, 13))
posicoes = []
rendas = []

acoes = acoes_tsl
for mes in meses:
    lotes_mes = acoes // 100
    renda_opcao_mes = lotes_mes * premio_call * 100
    renda_div_mes = acoes * dividendo_mensal
    renda_total_mes = renda_opcao_mes + renda_div_mes + aporte_mensal
    novas_acoes = int(renda_total_mes // preco_acao)
    acoes += novas_acoes
    posicoes.append(acoes)
    rendas.append(renda_total_mes)

# Exibir gráfico
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
fig.tight_layout(pad=5.0)

ax1.plot(meses, posicoes, marker='o', color='blue')
ax1.set_title('Evolução da Posição TSLY com Reinvestimento')
ax1.set_xlabel('Mês')
ax1.set_ylabel('Quantidade de Ações')
ax1.grid(True)

ax2.plot(meses, rendas, marker='s', color='green')
ax2.set_title('Evolução da Renda Mensal Total (Opções + Dividendos + Aportes)')
ax2.set_xlabel('Mês')
ax2.set_ylabel('Renda Mensal (US$)')
ax2.grid(True)

st.pyplot(fig)

# Observações
st.markdown("""
### 📌 Observações:
- O painel considera que a call vendida expira OTM (fora do dinheiro) e você não é exercido.
- Se TSLY subir acima do strike, pode ser necessário rolar a call para o próximo vencimento.
- Os valores são estimativas e variam com o mercado real.
- O reinvestimento assume recompra no preço atual da TSLY sem fracionamento.
- Aportes mensais são somados à renda para simular recompra adicional de ações.
""")
