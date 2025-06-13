Projeto: ETL com PokeAPI 🐍🔍
📋 Descrição
Este projeto tem como objetivo demonstrar habilidades em desenvolvimento de pipelines ETL (Extração, Transformação e Carga) utilizando Python, com consumo de dados públicos da PokeAPI, modelagem e análise com pandas, e geração de relatórios estatísticos.

O projeto está totalmente modularizado, segue boas práticas de programação e está containerizado com Docker, facilitando a execução em qualquer ambiente.

🚀 Funcionalidades
Extração dos dados de 100 Pokémon via PokeAPI

Normalização e estruturação dos dados em DataFrame

Categorização dos Pokémon por experiência base

Análise estatística por tipo de Pokémon

Geração de gráfico da distribuição de tipos

Exportação de relatórios (.csv e .png)

Automatização do pipeline completo

Logging e tratamento de exceções

🧱 Estrutura do Projeto
📦PipelineETL-PokeAPI-Python
├── 📁 src
│ ├── 📁 common # Utilitários gerais
│ ├── 📁 drivers # Coletor de dados e requisições HTTP
│ ├── 📁 reports # Pasta para relatórios gerados
│ ├── 📁 stages
│ │ ├── 📁 contract # Contratos entre as camadas
│ │ ├── 📁 extract # Módulo de extração de dados
│ │ ├── 📁 transform # Módulo de transformação de dados
│ │ └── 📁 load # Módulo de geração de relatórios
│ ├── 📁 tests # Testes automatizados das camadas
│ └── 🧾 main.py # Script principal da pipeline
├── 🐳 Dockerfile # Dockerfile para ambiente containerizado
├── 📦 requirements.txt # Dependências do projeto

⚙️ Como Executar
Pré-requisitos
Docker instalado e configurado
Acesso ao PowerShell

Passos
Clone o repositório:

```bash
git clone https://github.com/PedroMarques1205/PipelineETL-PokeAPI-Python.git
```

abra o terminal ou o powershell e navegue até o diretório code:

```bash
cd code
```

Construa a imagem Docker:

```bash
docker build -t python-etl-pokeapi:1.0 .
```

Em qualquer pasta desejada (onde deseja salvar os relatórios), execute no powershell:

```bash
docker run -v ${PWD}\reports:/app/reports python-etl-pokeapi:1.0
```

⚠️ Será criada uma pasta reports com os seguintes arquivos no diretório onde foi executado o comando no powershell:

top5_pokemon.csv

media_por_tipo.csv

distribuicao_pokemon_por_tipo.png

📈 Relatórios Gerados
Top 5 Pokémon com maior experiência base

Média de ataque, defesa e HP por tipo

Gráfico de distribuição de Pokémon por tipo (barras)

🔍 Tecnologias Utilizadas
Python 3.11+

pandas

matplotlib / seaborn

requests

logging

Docker

🧪 Testes
Os testes automatizados foram implementados para garantir a qualidade das funções principais de extração, transformação e carga. Os arquivos de teste estão localizados em src/stages/tests.

📌 Observações
Todo o pipeline foi desenvolvido visando desempenho e modularidade.

O volume de dados foi tratado com caching interno e redução de chamadas desnecessárias à API.

Logs informativos são emitidos ao longo da execução para facilitar o acompanhamento do processo.

📫 Contato
Pedro Marques
Email: pedrophmo1205@gmail.com
LinkedIn: https://www.linkedin.com/in/pedro-marques-8556b4262/

