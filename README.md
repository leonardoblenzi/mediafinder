# Pesquisa de Mídias

Aplicativo desktop em Python + PySide6 para localizar fotos e vídeos em múltiplas pastas locais ou compartilhadas.

## Recursos da primeira versão

- Cadastro de vários diretórios de busca
- Classificação opcional por diretório: Fotos, Vídeos, Geral ou personalizada
- Busca instantânea enquanto digita
- Busca por nome do arquivo + nomes das pastas
- Ignora diferenças de acentos, maiúsculas/minúsculas, hífens e sublinhados
- Índice local em SQLite para busca rápida
- Miniaturas de imagens
- Identificação de vídeos
- Filtros por tipo e classificação
- Abrir arquivo
- Abrir pasta do arquivo
- Copiar caminho
- Atualizar índice manualmente
- Atualização manual do índice, preservando o catálogo salvo entre aberturas

## Como rodar no PyCharm

1. Extraia a pasta do projeto.
2. No PyCharm, use **File > Open** e selecione a pasta `pesquisa_midias`.
3. Configure um interpretador Python 3.11 ou 3.12.
4. Abra o Terminal do PyCharm e rode:

```bash
pip install -r requirements.txt
```

5. Rode o arquivo:

```bash
python app.py
```

Ou clique com o botão direito em `app.py` > **Run 'app'**.

## Pastas compartilhadas

Você pode cadastrar caminhos como:

```text
\\SERVIDOR\Produtos\Fotos
\\192.168.0.10\Marketing\Videos
D:\Produtos\Fotos
```

O Windows precisa já ter permissão para acessar essas pastas.

## Banco local

O programa salva as configurações e o índice em:

```text
%APPDATA%\PesquisaMidias\media_index.db
```

## Gerar .exe depois

Quando quiser distribuir para outros computadores:

```bash
pip install pyinstaller
pyinstaller --noconfirm --windowed --name PesquisaMidias app.py
```

O executável será criado em `dist\PesquisaMidias\PesquisaMidias.exe`.

> Para a primeira versão, recomendo rodar no PyCharm até validarmos a experiência e depois gerar o .exe.
