# FloreantPOS Edição Flask

Uma recriação moderna do sistema FloreantPOS usando Python Flask com armazenamento local (CSV e JSON).

## Funcionalidades

- **Gerenciamento de Cardápio**: Adicione, edite e organize itens do menu por categorias
- **Processamento de Pedidos**: Crie e gerencie pedidos com uma interface amigável
- **Gerenciamento de Mesas**: Layout visual de mesas com indicadores de status
- **Exibição para Cozinha**: Visualização em tempo real dos pedidos para a equipe da cozinha
- **Relatórios**: Análise de vendas e funcionalidade de relatórios
- **Armazenamento Local**: Dados armazenados em arquivos CSV e JSON - sem necessidade de banco de dados
- **Autenticação de Usuários**: Controle de acesso baseado em funções (admin, garçom)

## Instalação e Configuração

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```
   python app.py
   ```
4. Abra seu navegador e acesse `http://127.0.0.1:5000`

## Credenciais de Login Padrão

- **Admin**: Usuário: `admin` Senha: `admin`
- **Garçom**: Usuário: `garcom` Senha: `garcom`

## Armazenamento de Dados

A aplicação armazena todos os dados localmente no diretório `data`:

- `data/menu/` - Categorias e itens do cardápio
- `data/pedidos/` - Pedidos ativos e completados
- `data/usuarios/` - Contas de usuário e funções
- `data/mesas/` - Layout e status das mesas

## Estrutura do Projeto

- `app.py` - Aplicação Flask principal
- `templates/` - Templates HTML para a aplicação
- `static/` - CSS, JavaScript e imagens
- `data/` - Diretório de armazenamento local para arquivos JSON e CSV

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.