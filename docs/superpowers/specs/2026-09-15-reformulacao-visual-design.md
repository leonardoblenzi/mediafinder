# Reformulação visual do Pesquisa de Mídias

## Objetivo

Transformar a interface atual em um aplicativo desktop claro, profissional e consistente, mantendo intactas a indexação local, a pesquisa instantânea, os filtros e as ações sobre arquivos.

## Escopo

- Aplicar um tema claro único à janela principal e aos diálogos.
- Reorganizar a janela em cabeçalho, painel lateral de filtros e resultados em grade responsiva.
- Exibir resultados em cartões com miniatura maior, metadados e ações reunidas em menu.
- Criar estados vazios para nenhuma pesquisa, nenhum resultado e nenhum diretório cadastrado.
- Melhorar hierarquia visual, foco de teclado e contraste dos controles.

## Fora do escopo

- Alterar o esquema SQLite, a indexação ou os diretórios cadastrados.
- Alterar como arquivos são abertos, pastas são abertas ou caminhos são copiados.
- Adicionar reconhecimento de conteúdo, tags manuais ou suporte a novos tipos de mídia.

## Interface principal

O cabeçalho terá o título do aplicativo e ações globais: `Atualizar índice` como ação principal e `Configurações` como ação secundária. A busca ocupará uma faixa ampla abaixo do cabeçalho, com ícone, texto de apoio e contador de resultados.

Um painel lateral fixo concentrará os filtros de tipo e classificação, além do status do índice. A área de conteúdo mostrará cartões em duas ou mais colunas, conforme a largura disponível. Cada cartão terá miniatura, nome, tipo, classificação, diretório de origem e um botão de menu para abrir o arquivo, abrir a pasta ou copiar o caminho.

O tema usará fundo cinza-azulado muito claro, superfícies brancas, texto grafite, bordas discretas e azul somente para ações primárias, foco e seleção. Nenhum texto dependerá de cores herdadas do sistema.

## Estados e erros

- Sem diretórios: exibir orientação e atalho para Configurações.
- Sem consulta: exibir orientação para iniciar a pesquisa ou atualizar o índice.
- Sem resultados: informar que não houve correspondências e manter os filtros visíveis.
- Indexação: apresentar progresso no painel lateral e impedir uma segunda indexação simultânea.
- Erros de acesso e operações de arquivo: preservar as mensagens claras já existentes.

## Arquitetura

- Um módulo de tema centraliza a folha de estilos e os tokens de cor.
- A janela principal monta cabeçalho, busca, filtros e uma grade de resultados.
- O cartão de resultado é responsável apenas pela apresentação de um arquivo e por suas ações.
- Diálogos de diretórios recebem o mesmo tema sem mudar suas regras de validação.
- A camada de banco de dados, o indexador e os workers permanecem inalterados.

## Verificação

- Executar o aplicativo sem diretórios e confirmar o estado inicial legível.
- Cadastrar diretórios e confirmar que a indexação continua funcional.
- Pesquisar, alternar filtros e verificar a atualização da grade e do contador.
- Validar as ações Abrir, Abrir pasta e Copiar caminho em um cartão.
- Conferir legibilidade do tema claro nas janelas principal, configurações e diretório.
