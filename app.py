import streamlit as st
import requests
import json

# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(
    page_title="Previsão de Receita de Marketing",
    page_icon="📊",
    layout="centered"
)

# ============ TÍTULO E DESCRIÇÃO ============
st.markdown("""
# 📈 **Previsão de Receita de Marketing**
Preveja a **receita esperada** com base no valor investido em anúncios 💰  
Modelo de Machine Learning treinado e implantado no **Azure Machine Learning** 🚀
""")

# ============ INPUT ============
gasto = st.number_input(
    "💵 Informe o valor de **Gasto em Anúncios**:",
    min_value=0.0,
    step=100.0,
    help="Digite o valor investido em campanhas de marketing para estimar a receita prevista."
)

# ============ BOTÃO DE AÇÃO ============
if st.button("🔮 Prever Receita"):
    endpoint = "https://marketing-endpoint-045be.brazilsouth.inference.ml.azure.com/score"
    key = "AZURE_ML_KEY", "SUA_CHAVE_AQUI_SEM_SUBIR"
    data = {
        "input_data": {
            "columns": ["Gasto Anuncios"],
            "data": [[gasto]]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    # ============ REQUISIÇÃO ============
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    # ============ EXIBIÇÃO DO RESULTADO ============
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, str):
            result = json.loads(result)
        valor_previsto = result["result"][0]

        st.success(f"💡 **Receita prevista:** R$ {valor_previsto:,.2f}")
        st.metric(label="Retorno sobre investimento estimado", value=f"{valor_previsto / (gasto or 1):.2f}x")

        st.balloons()

    else:
        st.error(f"❌ Erro {response.status_code}: {response.text}")

# ============ RODAPÉ ============
st.markdown("""
---
👩‍💻 Desenvolvido por **Dayane Teodoro**  
💼 Projeto de **Machine Learning no Azure** com deploy em **endpoint gerenciado**  
🔗 [LinkedIn](https://www.linkedin.com/in/dayaneteodoro) | [GitHub](https://github.com/DayaneTeodoro)
""")

