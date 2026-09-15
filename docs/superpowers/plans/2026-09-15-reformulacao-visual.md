# Reformulação Visual do Pesquisa de Mídias Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir o visual inconsistente por uma interface clara, profissional, com filtros laterais e resultados em grade, sem alterar a busca ou a indexação.

**Architecture:** A aparência será centralizada em um módulo de tema. `MainWindow` passará a compor o cabeçalho, filtros e uma grade rolável; `ResultCard` exibirá as ações em um menu e se adaptará à largura da grade. Banco, workers e indexador não serão alterados.

**Tech Stack:** Python 3, PySide6, SQLite existente, unittest.

---

## Estrutura de arquivos

- Criar `mediafinder/theme.py`: paleta, folha de estilos e aplicação do tema.
- Modificar `mediafinder/main_window.py`: novo layout, estados vazios e grade adaptável.
- Modificar `mediafinder/result_card.py`: cartão em grade e menu de ações.
- Modificar `mediafinder/settings_dialog.py`: nomes de objetos e hierarquia de ações compatíveis com o tema.
- Criar `tests/test_theme.py`: verificação dos seletores e tokens críticos do tema.
- Criar `tests/test_result_card.py`: verificação dos metadados e ações do cartão.

### Task 1: Tema centralizado

**Files:**
- Create: `mediafinder/theme.py`
- Test: `tests/test_theme.py`

- [ ] Escrever testes que confirmem que a folha define texto escuro em superfícies claras e estilos para cartões, botões, filtros e tabelas.
- [ ] Executar `python -m unittest tests.test_theme -v` e confirmar falha por módulo inexistente.
- [ ] Implementar `APP_STYLE` e `apply_theme(widget)` em `mediafinder/theme.py`, com seletores explícitos para `QWidget`, `QLabel`, `QLineEdit`, `QComboBox`, `QPushButton`, `QFrame#resultCard`, `QTableWidget` e `QMenu`.
- [ ] Executar `python -m unittest tests.test_theme -v` e confirmar aprovação.

### Task 2: Cartão de resultado em grade

**Files:**
- Modify: `mediafinder/result_card.py`
- Test: `tests/test_result_card.py`

- [ ] Escrever teste que construa um cartão a partir de um registro e confirme nome, metadados e menu de ações.
- [ ] Executar `python -m unittest tests.test_result_card -v` e confirmar falha antes da nova API.
- [ ] Implementar cartão vertical compacto com miniatura, rótulos de tipo/classificação/origem e menu contendo Abrir, Abrir pasta e Copiar caminho.
- [ ] Executar `python -m unittest tests.test_result_card -v` e confirmar aprovação.

### Task 3: Janela principal e estados vazios

**Files:**
- Modify: `mediafinder/main_window.py`

- [ ] Substituir a lista vertical por uma área rolável que recalcula colunas conforme a largura da janela.
- [ ] Adicionar cabeçalho, campo de busca destacado, painel lateral de filtros/status e widgets de estado vazio.
- [ ] Preservar conexões de busca, filtros, atualização e indexação; chamar a atualização da grade após cada pesquisa e redimensionamento.
- [ ] Executar `python -m unittest discover -v` e confirmar aprovação.

### Task 4: Diálogos e verificação visual

**Files:**
- Modify: `mediafinder/settings_dialog.py`
- Modify: `app.py`

- [ ] Aplicar o tema aos diálogos e atribuir papéis a botões principais/secundários e à tabela.
- [ ] Executar `python -m unittest discover -v` e confirmar aprovação.
- [ ] Executar `python app.py`, abrir Configurações e conferir: contraste, filtros, estado sem diretórios e ausência de textos claros sobre fundo claro.
