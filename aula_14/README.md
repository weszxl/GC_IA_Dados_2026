#   API de suco

API REST desenvolvida em **Python** utilizando **Flask** e **Flasgger**, integrada à API externa **Fruityvice**.

## Estrutura do Projeto

```text
aula_14/
├── .venv/                
├── .gitignore            
├── requirements.txt      
├── README.md             
└── src/
    └── api.py           
```

---

### 1. Criação do Ambiente Virtual (venv)

#### No Windows:

```bash
python -m venv .venv

.\.venv\Scripts\Activate.ps1

```

#### No Linux / macOS:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

### 2. Instalação das Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Execução da API

```bash
cd src
python api.py
```

---

## Documentação Swagger

- **URL do Swagger UI:** [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---

## Endpoints da API

**GET** /frutas/<nome> - Consulta informações nutricionais de uma fruta na API Fruityvice. 
**POST** /sucos - Cadastra um novo suco calculando o total de calorias e açúcar das frutas. 
**GET** /sucos - Lista todos os sucos cadastrados em memória. 
**PUT** /sucos/<id> - Atualiza informações de um suco existente