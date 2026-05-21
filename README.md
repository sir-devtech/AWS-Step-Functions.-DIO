# Explorando Workflows Automatizados com AWS Step Functions

> Laboratório prático da trilha **Fundamentos de Cloud com AWS** — DIO  
> Tema: Orquestração de serviços serverless usando AWS Step Functions, Lambda e S3

---

## 📋 Sobre o Projeto

Este repositório documenta minha experiência prática com **AWS Step Functions**, cobrindo desde a criação de máquinas de estado simples até workflows que integram AWS Lambda, Amazon S3 e Amazon CloudWatch.

> Laboratório concluído com criação de máquina de estado, integração com AWS Lambda e execução com sucesso registrada.

---

## 🎯 Objetivos de Aprendizagem

- Compreender o modelo de orquestração de serviços via Step Functions
- Criar e executar máquinas de estado usando o **Amazon States Language (ASL)**
- Integrar AWS Lambda em workflows automatizados
- Processar grandes volumes de dados no S3 com o estado **Distributed Map**
- Monitorar execuções via **Amazon CloudWatch**

---

## 🧱 Conceitos Abordados

### AWS Step Functions
Serviço de orquestração serverless que permite coordenar múltiplos serviços AWS em workflows visuais. Cada passo do fluxo é chamado de **estado (state)**.

**Tipos de estados principais:**
| Estado | Descrição |
|--------|-----------|
| `Task` | Executa uma ação (ex: invocar Lambda) |
| `Choice` | Bifurcação condicional no fluxo |
| `Wait` | Pausa a execução por um período |
| `Parallel` | Executa ramificações em paralelo |
| `Map` | Itera sobre uma coleção de itens |
| `Pass` | Repassa dados sem processamento |
| `Succeed` / `Fail` | Encerra o fluxo com sucesso ou falha |

### Amazon States Language (ASL)
Linguagem baseada em JSON usada para definir as máquinas de estado. Exemplo de uma máquina mínima:

```json
{
  "Comment": "Máquina de estado simples",
  "StartAt": "MeuPrimeiroEstado",
  "States": {
    "MeuPrimeiroEstado": {
      "Type": "Pass",
      "End": true
    }
  }
}
```

### AWS Lambda Invoke (dentro do Step Functions)
Integração direta do Step Functions com funções Lambda usando o tipo de integração **Optimized**:

```json
{
  "InvocaLambda": {
    "Type": "Task",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "NomeDaFuncao:$LATEST",
      "Payload.$": "$"
    },
    "End": true
  }
}
```

### Distributed Map + S3
O estado **Distributed Map** processa arquivos CSV armazenados no S3 em larga escala, criando execuções filhas para cada item — ideal para pipelines de dados.

```json
{
  "ProcessaArquivosS3": {
    "Type": "Map",
    "ItemReader": {
      "Resource": "arn:aws:states:::s3:listObjectsV2",
      "Parameters": {
        "Bucket": "meu-bucket",
        "Prefix": "2024/"
      }
    },
    "ItemProcessor": {
      "ProcessorConfig": {
        "Mode": "DISTRIBUTED",
        "ExecutionType": "STANDARD"
      },
      "StartAt": "ProcessaCSV",
      "States": {
        "ProcessaCSV": {
          "Type": "Task",
          "Resource": "arn:aws:states:::lambda:invoke",
          "Parameters": {
            "FunctionName": "ProcessadorCSV:$LATEST",
            "Payload.$": "$"
          },
          "End": true
        }
      }
    },
    "End": true
  }
}
```

---

## 🚀 Roteiro da Prática

> Marque os itens conforme concluir no laboratório.

### Passo 1 — Criando a Primeira Máquina de Estado

- [ ] Acessar o console AWS → **Step Functions**
- [ ] Clicar em **Criar máquina de estado**
- [ ] Escolher o modo **Design** no Workflow Studio
- [ ] Criar uma máquina simples para entender o fluxo Start → State → End
- [ ] Configurar nome e permissões IAM
- [ ] Criar a máquina de estado
- [ ] Fazer uma captura de tela da máquina criada

### Passo 2 — Integrando AWS Lambda

- [ ] Criar ou selecionar uma função Lambda de teste
- [ ] No Workflow Studio, arrastar **AWS Lambda → Invoke** para o canvas
- [ ] Selecionar a função Lambda criada na própria conta AWS
- [ ] Definir o **Payload** como entrada do estado
- [ ] Salvar e executar passando um JSON de teste
- [ ] Verificar o resultado da execução
- [ ] Fazer uma captura de tela da execução com sucesso

### Passo 3 — Processamento Distribuído com S3 + Distributed Map

- [ ] Verificar o bucket S3 usado pelo laboratório
- [ ] Identificar a pasta/prefixo que contém os arquivos `.csv`
- [ ] Configurar o estado **Distributed Map** apontando para o bucket/prefixo
- [ ] Definir a função Lambda processadora como `ItemProcessor`
- [ ] Executar o workflow
- [ ] Acompanhar as execuções filhas geradas pelo Distributed Map
- [ ] Fazer capturas do bucket S3 e da execução do Step Functions

### Passo 4 — Monitoramento no CloudWatch

- [ ] Acessar **CloudWatch → Log Groups** para ver logs das execuções
- [ ] Verificar métricas de sucesso/falha no painel do Step Functions
- [ ] Consultar o histórico de eventos de cada execução
- [ ] Fazer captura dos logs ou do histórico da execução

---

## 📸 Capturas de Tela do Laboratório

| # | Descrição | Imagem |
|---|-----------|--------|
| 1 | Console AWS Step Functions | ![Console Step Functions](images/1-%20Console%20Step%20Functions.png) |
| 2 | Tela de criação da máquina de estado | ![Criar máquina](images/2-%20Criar%20maquina%20opções.png) |
| 3 | Galeria de templates (busca DynamoDB) | ![Templates DynamoDB](images/3-%20Captura%20de%20tela%202026-05-21%20154902.png) |
| 4 | Detalhe do template Distributed Map | ![Template Distributed Map](images/4-%20Captura%20de%20tela%202026-05-21%20154944.png) |
| 5 | Workflow Studio — configuração MinhaStateMachine | ![Workflow Studio](images/5-%20Captura%20de%20tela%202026-05-21%20155430.png) |
| 6 | Estado Lambda Invoke adicionado ao canvas | ![Lambda Invoke](images/6-%20Captura%20de%20tela%202026-05-21%20155801.png) |
| 7 | Confirmação de criação da máquina de estado | ![Máquina criada](images/7-%20Captura%20de%20tela%202026-05-21%20160053.png) |
| 8 | Criação da função Lambda MinhaFuncao | ![Lambda criada](images/8-%20Captura%20de%20tela%202026-05-21%20160150.png) |
| 9 | Confirmação de permissões IAM geradas | ![Permissões IAM](images/9-%20Captura%20de%20tela%202026-05-21%20162505.png) |
| 10 | Execução iniciada com êxito | ![Execução iniciada](images/10-%20Captura%20de%20tela%202026-05-21%20163022.png) |
| 11 | Histórico de eventos — ExecutionSucceeded | ![Execução com sucesso](images/11-%20Captura%20de%20tela%202026-05-21%20163040.png) |

---

## 🗂️ Estrutura do Repositório

```
AWS PROJETO 2/
├── README.md                          # Esta documentação
├── state-machines/
│   ├── maquina-simples.json           # Exemplo de máquina de estado básica
│   ├── lambda-invoke.json             # Máquina com invocação de Lambda
│   └── distributed-map-s3.json       # Workflow com Distributed Map + S3
├── lambda/
│   └── processador.py                # Exemplo de função Lambda processadora
└── images/
    └── (11 capturas de tela do laboratório)
```

---

## 💡 Insights e Aprendizados

- **Step Functions elimina código de orquestração**: lógica de retry, tratamento de erros e paralelismo ficam na definição ASL, não no código da aplicação.
- **Tipo de integração Optimized vs. SDK**: a integração Optimized para Lambda é mais eficiente (sem polling) e reduz custos.
- **Distributed Map escala automaticamente**: processa milhares de arquivos S3 em paralelo, com controle de concorrência configurável.
- **CloudWatch é essencial**: sem monitoramento, depurar falhas em workflows complexos é muito difícil.
- **ASL é declarativo**: descreve *o que* fazer, não *como* — torna workflows mais legíveis e auditáveis.

---

## ✅ Entrega

- [x] Assistidas todas as aulas do módulo na DIO
- [x] Máquina de estado criada no console AWS (MinhaStateMachine)
- [x] Função Lambda integrada (MinhaFuncao — Python 3.14)
- [x] Execução realizada com status **Com êxito** (7 eventos registrados)
- [x] Capturas de tela salvas na pasta `images/`
- [x] Repositório público publicado no GitHub

---

## 🔗 Referências

- [AWS Step Functions — Documentação Oficial](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon States Language](https://states-language.net/spec.html)
- [Distributed Map — Processamento em Larga Escala](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-asl-use-map-state-distributed.html)
- [AWS Lambda — Documentação](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [DIO — Formação Fundamentos de Cloud com AWS](https://web.dio.me)

---

*Desenvolvido como parte da trilha Fundamentos de Cloud com AWS — DIO.*
