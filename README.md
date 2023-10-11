# VAREJISTA LEROY MERLIN - ENGENHERIA DE DADOS
- A LEROY MERLIN chegou no Brasil em 1998 e desde então vem inovando o mundo de materiais de construção. Além de cimentos, tijolos, acabamentos, decorações, e eletrodomésticos, a LEROY MERLIN ainda oferece diversos serviços para você.
Fonte: Leroy Merlin (Aba 'sobre')

- OBS.: ESSE PROJETO NÃO É UMA RECOMENDAÇÃO DE COMPRA, MAS UMA INICIATIVA DE FORNECER ALGUMAS INFORMAÇÕES E DADOS ÚTEIS - E DISPONÍVEIS PELA PRÓPRIA COMPANHIA - AOS INTERESSADOS.

---------------------------------------------------------------------------------------------
# PROJETO
- Levando em conta a gama de produtos disponibilizados pela varejista, e possibilidade de mapear o mercado e evolução de preços, fiz a extração dos produtos - usando web scraping - e organizei por departamento. Através dos dados coletados, gerei um relatório formal abordando diversos informações por produto (como: nome do produto, departamento, preço, avaliações). Para conclusão desse projeto - abordando obtenção dos dados, tratamento e armazenamento deles -, foram necessárias algumas etapas, sendo elas:

---------------------------------------------------------------------------------------------
# ETAPAS

# 1) Configuração de Acessos
- Visando uma melhor organização das informações de configurações, inseri as informações necessárias, e de acessos, em um arquivo json, de nome 'data' - localizado dentro da pasta utils -, nesse arquivo há informações pertinentes a fonte extraída, o tipo do arquivo a ser gerado, parâmetros, credenciais da conta cloud AWS - usuário IAM, e informações pertinentes as planilhas desejadas, pré-selecionadas pelo usuário;

# 2) Criei um processo ETL:
- E: Extração dos dados respectivos oriundos da fonte https://www.leroymerlin.com.br/;

- T: Posterior à coleta dos dados, e visando a geração de um relatório formal relacionado aos produtos, tratei os dados e gerei um dataframe para facilitar a manipulação;

- L: Logo após os tratamentos, e tendo um dataframe preparado, carreguei os dados em um arquivo csv - nomeado com a estrutura padrão: 'Produto_[%Y%m%d].['formatodesejado']', um arquivo já tratado, limpo e em conformidade, disponível para ser utilizado como ferramenta para obtenção de insights.

# 3) Criei um processo EL:
- E: Para garantir a integridade dos dados, extraí, também, o html de cada url - pois nele fica contido os valores que estamos coletando, com a estrutura de nome: 'Html_[produto]_[index].txt'. (%B: o produto é condizente à url e o index, à paginação);

- L: Como a intenção é justamente usar como garantia de integridade, salvei ele na pasta da data de coleta, dentro do Bucket S3 configurado - informado logo após.

# 4) Configurei o Selenium
- Para extração dos dados da web, fiz uso do selenium - que é um framework portátil para testar aplicativos web, ou seja, ele permite a simulação de um usuário no sistema, a partir da configuração de um robô. Para fazer funcionar, é necessário escolher o navegador que será utilizado na automatização, saber o versionamento dele e baixar o driver selenium que suporta/é compatível, posterior a isso, codifique da maneira que melhor atender.
    - Escolher navegador e pegar o versionamento atual dele;
    - Baixar o driver condizente/compatível a ele;
    - Codificar para não engessá-lo, ou seja, caso aconteça alguma mudança no versionamento, ele mesmo se atualizar e baixar o driver correspondente.

# 5) Criei Bucket S3:
- Usei o Bucket S3 (que serve de 'armazém' para arquivos, conhecidos como objetos) para guardar os objetos gerados com segurança, organização e escalabilidade. Para inserção no S3, fiz uso do Boto3, que é um SDK (Software Development Kit) da AWS para Python, permitindo interações facilitadas com serviços AWS.

# 6) Criei DynamoDB (NoSQL):
- Fiz uso do DynamoDB (Banco Não Relacional da AWS) para guardar os dados tratados, coletados oriundos do website da varejista, justamente pela facilidade de armazenamento e escalabilidade. Por ser um recurso AWS, também, fiz uso do Boto3, que é um SDK para Python.

---------------------------------------------------------------------------------------------
# OBSERVAÇÕES:
- Passo 1: conforme mencionado, há arquivos ausentes nesse repositório - exemplo do data.json, justamente para manter integridade dos dados pessoais. Dessa forma, para obtenção do resultado esperado, criei um arquivo base (de nome data_exemplo.json, dentro da pasta utils), para vocês terem uma noção da estrutura que foi necessária para obtenção do resultado esperado. Além dele, tem o arquivo do chromedriver, que é criado a partir da compilação/rodagem do código.

- Passos 2 e 3: foram realizadas usando, prioritariamente e somente, Linguagem de Programação Python e suas principais bibliotecas, sendo algumas delas: pandas, requests, bs4, selenium.

- Passo 4: foi realizado via código mesmo, onde peguei a versão desejada, a partir de uma vistoria sobre o versionamento do meu navegador. Com a versão em mãos (ou armazenada, rs) baixo ele automaticamente e atualizo o meu chromedriver (chrome pois é o navegador que decidi utilizar) sempre que necessário. Em referências, no fim desse documento, há um conteúdo para ajudá-lo em sua codificação

- Passo 5 e 6: foram realizados manualmente, via console AWS, entretanto, é possível utilizar o boto3 para criação do Bucket/Dynamo via código, a partir da informação dos dados pertinentes ao Usuário e permissões necessárias para criação, inserções e manipulações devida. Quanto às permissões, fiz uso do recurso IAM, criando dois grupos (S3 e Dynamo) com permissões de acesso e inserção ao S3 e Dynamo. Visando melhor organização e tratamento, criei um usuário e o inseri dentro desses dois grupos. Dessa forma, depois dessas criações, consegui usar as chaves AWS para acessar/inserir os objetos/dados em serviços respectivos.

------------------------------------------------------------------------------------------------
# REFERÊNCIAS:
- Sites que podem contribuir à realização das etapas acima, e que me ajudaram para obtenção do resultado final e esperado:

- https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/creating-bucket.html
- https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/uploading-an-object-bucket.html
- https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/deleting-object-bucket.html
- https://docs.aws.amazon.com/pt_br/cost-management/latest/userguide/create-budget-report.html
- https://docs.aws.amazon.com/pt_br/sdk-for-javascript/v2/developer-guide/using-lambda-functions.html
- https://docs.aws.amazon.com/pt_br/amazondynamodb/latest/developerguide/SettingUp.DynamoWebService.html
- https://felipepimentelrosa.medium.com/usando-selenium-em-um-projeto-de-rpa-em-python-990ea496609a

------------------------------------------------------------------------------------------------
Obrigado pela interação, fico à disposição e disponível para receber dicas. Bons estudos e fica na paz!