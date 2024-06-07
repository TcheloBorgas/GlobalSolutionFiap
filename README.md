# Título do Projeto: Modelo Integrado para Previsão de Correntes e Otimização de Navegação

## Visão Geral
Este projeto visa otimizar a navegação e a previsão de correntes oceânicas utilizando aprendizado de máquina e análise de dados. O projeto é estruturado em três componentes principais:

- `Previsao_correntes.ipynb`: Um caderno Jupyter que inclui a análise de dados e os modelos de aprendizado de máquina usados para prever correntes oceânicas.
- `app.py`: Uma API Flask que fornece endpoints para interagir com os modelos e recuperar previsões.
- `app_streamlit.py`: Uma aplicação Streamlit que oferece uma interface amigável para interação em tempo real com os modelos preditivos.

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip
- Jupyter Notebook ou JupyterLab

### Configuração do Ambiente
1. Clone o repositório:
   ```bash
   git clone <https://github.com/TcheloBorgas/GlobalSolutionFiap.git>
   cd <GlobalSolutionFiap>

Instale os pacotes Python necessários:

```
pip install -r requirements.txt
```


## Executando o Projeto
Executando o Jupyter Notebook
Para explorar a análise de dados e o processo de treinamento do modelo:

```
jupyter notebook Previsao_correntes.ipynb
```

## Executando a API Flask
Para iniciar a API Flask que serve as previsões do modelo:

```
python app.py
```

## Executando a Aplicação Streamlit
Para interagir com os modelos por meio de uma interface visual:

```
streamlit run app_streamlit.py
```

