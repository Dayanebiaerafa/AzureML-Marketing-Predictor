# AzureML Marketing Predictor

📊 Previsão de receita de campanhas de marketing com Machine Learning e Azure Machine Learning

<p align="center">
  <img src="img/site-stremlit.png" alt="App em Streamlit do AzureML Marketing Predictor" width="850"/>
</p>

Projeto de estudo que segue o tutorial oficial da Microsoft ([Azure Machine Learning in a Day](https://learn.microsoft.com/pt-br/azure/machine-learning/tutorial-azure-ml-in-a-day?view=azureml-api-2)), adaptado para prever a receita de campanhas de marketing a partir do valor gasto em anúncios. O modelo foi treinado e publicado no Azure Machine Learning, e um app em Streamlit permite testá-lo.

**Stack:** Python 3.10 · Pandas · scikit-learn · MLflow · Azure Machine Learning · Streamlit
**Período:** out. de 2025

---

## Como funciona

1. **Treino:** um script em Python (Pandas e scikit-learn) treina um modelo de Regressão Linear (técnica que prevê um número a partir de outro) em um cluster de computação do Azure ML.
2. **Registro:** o modelo é salvo e versionado no workspace com o MLflow (ferramenta que registra métricas e versões do modelo), com o nome `modelo_regressao_marketing`.
3. **Publicação:** o modelo é publicado em um endpoint online (uma API REST) no Azure ML e testado com uma requisição de exemplo.
4. **Uso:** o app em Streamlit recebe o gasto em anúncios, envia ao endpoint e mostra a previsão de receita.

## Demonstração

![Detalhes do endpoint](img/detalhes2-endpoint.png)
![Como consumir o endpoint](img/consumir-endpoint.png)
![Teste do endpoint](img/test-endpoint.png)
![Monitoramento do endpoint](img/monitoramento-endpoint.png)

## O app em Streamlit

```python
st.title("📈 Previsão de Receita de Marketing")
gasto = st.number_input("💰 Informe o valor de 'Gasto em Anúncios':", min_value=0.0)
```

Quando o usuário informa o valor, o app envia uma requisição ao endpoint do Azure ML e mostra a previsão (veja a imagem no topo).

## O que foi feito no Azure

1. **Grupo de recursos:** reúne todos os serviços do projeto e facilita apagar tudo no fim, para evitar custos.
2. **Workspace do Azure ML:** ambiente central onde ficam experimentos, modelos e endpoints.
3. **Cluster de computação** `Standard_DS11_v2`: usado só durante o treino.
4. **Script de treino:** carrega e prepara os dados, treina a Regressão Linear e registra o modelo com o MLflow.
5. **Ambiente e job:** as dependências foram definidas em um arquivo `conda.yaml` e o job de treino foi enviado ao cluster; o Azure ML guardou métricas, logs e artefatos.
6. **Endpoint online gerenciado** e **deployment** `blue`, criado com o arquivo `deployment_fixed.yml` (ambiente `azureml:sklearn-env-py310:1`, script de inferência `score.py`, instância `Standard_E8ds_v4`).
7. **Teste:** requisição de exemplo (`sample-request.json`) para conferir que o endpoint devolve a previsão.
8. **Limpeza:** os recursos podem ser removidos de uma vez pelo grupo de recursos.

<details>
<summary>Permissões, provedores de recursos e documentação da Microsoft</summary>

### Permissões necessárias

Para repetir o projeto, a conta precisa de papéis na assinatura do Azure, como:

- `Owner` ou `Contributor` no grupo de recursos
- `AzureML Data Scientist` para as operações de machine learning
- `AzureML Compute Operator` para criar e gerenciar clusters
- Permissão `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*/actions` para criar endpoints

Para ver suas permissões atuais:

```bash
az role assignment list --all --output table
```

Ou, só as do workspace:

```bash
az role assignment list \
  --scope "/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>" \
  --output table
```

### Provedores de recursos (Resource Providers)

Provedores são serviços internos do Azure que habilitam recursos específicos. Sem os essenciais registrados na assinatura, o treino, o registro do modelo e o deploy podem falhar.

**Essenciais:**

| Provedor | Para que serve |
|---|---|
| `Microsoft.MachineLearningServices` | Azure Machine Learning (workspaces, modelos e endpoints) |
| `Microsoft.Storage` | Armazena dados, artefatos e logs |
| `Microsoft.ContainerRegistry` | Guarda as imagens Docker dos ambientes |
| `Microsoft.Compute` | Clusters e instâncias de computação |
| `Microsoft.KeyVault` | Guarda chaves e segredos |
| `Microsoft.Network` | Rede entre os serviços |

**Recomendados (opcionais):**

| Provedor | Para que serve |
|---|---|
| `Microsoft.Insights` | Application Insights: logs, métricas e erros do endpoint |
| `Microsoft.OperationalInsights` | Log Analytics: coleta logs e métricas em um só lugar |
| `Microsoft.Authorization` | Controle de acesso (RBAC): papéis e permissões |
| `Microsoft.ManagedIdentity` | Identidades gerenciadas: autenticação entre serviços sem expor chaves |
| `Microsoft.Advisor` | Recomendações de custo e desempenho |

Para ver todos os provedores, ou só os registrados:

```bash
az provider list --output table
az provider list --query "[?registrationState=='Registered'].namespace" --output table
```

### Documentação usada, por etapa

1. Grupo de recursos: [Gerenciar grupos de recursos](https://learn.microsoft.com/pt-br/azure/azure-resource-manager/management/manage-resource-groups-portal)
2. Workspace: [Criar e gerenciar workspaces](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-manage-workspace?view=azureml-api-2)
3. Computação: [Instâncias e clusters de computação](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-create-attach-compute-studio?view=azureml-api-2)
4. Script de treino: [Treinar modelos com scripts](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-train-model?view=azureml-api-2)
5. Ambiente e job: [Executar trabalhos de treinamento](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-train-model-cli?view=azureml-api-2) e [Monitorar trabalhos](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-monitor-jobs?view=azureml-api-2)
6. Endpoint online: [Criar e gerenciar endpoints online](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-deploy-online-endpoints?view=azureml-api-2)
7. Deployment: [Implantar modelos em endpoints online](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-deploy-managed-online-endpoints?view=azureml-api-2)
8. Teste: [Testar endpoints](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-invoke-endpoint?view=azureml-api-2)
9. Limpeza: [Excluir grupos de recursos e workspaces](https://learn.microsoft.com/pt-br/azure/machine-learning/how-to-manage-workspace?view=azureml-api-2)

</details>

## Como rodar o app

O app precisa da URL e da chave do **seu próprio** endpoint no Azure ML (a conta e os recursos do Azure são pagos). **Nunca coloque a chave no código nem envie ao GitHub.**

```bash
pip install streamlit requests
streamlit run app.py
```

## Tecnologias

| Categoria | Ferramenta |
|---|---|
| Linguagem | Python 3.10 |
| Machine Learning | scikit-learn, Pandas, MLflow |
| Nuvem | Azure Machine Learning |
| Interface | Streamlit |
| API | REST (requests, JSON) |
| Versionamento | Git e GitHub |

## Aprendizados

- Organizar um projeto no Azure ML: grupo de recursos, workspace, computação, permissões e provedores de recursos.
- Registrar e versionar um modelo com o MLflow.
- Publicar um modelo como endpoint e consumi-lo por API a partir de um app.
- Cuidar de custos e permissões ao usar a nuvem.

## Limitações e próximos passos

- É um projeto de estudo, com um modelo simples: o foco foi o ciclo de Machine Learning na nuvem.
- Repetir o projeto exige uma assinatura própria do Azure.

- [ ] Testar mais variáveis de entrada além do gasto em anúncios
- [ ] Adicionar testes automatizados para o app

## Contato

- **LinkedIn:** [Dayane Teodoro](https://www.linkedin.com/in/dayaneteodoro/)
- **GitHub:** [Dayanebiaerafa](https://github.com/Dayanebiaerafa)
- **E-mail:** dayaneteodorob@outlook.com

⭐ Dica: se este projeto te inspirou, deixe uma estrela no repositório para apoiar o trabalho!

