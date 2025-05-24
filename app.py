from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import json
import csv
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Garante que os diretórios de dados existam
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    
# Cria subdiretórios
for subdir in ['menu', 'pedidos', 'usuarios', 'mesas']:
    subdir_path = os.path.join(data_dir, subdir)
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)

# Funções auxiliares para manipulação de dados
def load_json(filename):
    filepath = os.path.join(data_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_json(data, filename):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_csv(filename):
    filepath = os.path.join(data_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)
    return []

def save_csv(data, filename, fieldnames):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Inicializa arquivos de dados se não existirem
def init_data():
    # Cria categorias do menu
    if not os.path.exists(os.path.join(data_dir, 'menu/categorias.json')):
        categorias = [
            {"id": "1", "nome": "Entradas"},
            {"id": "2", "nome": "Pratos Principais"},
            {"id": "3", "nome": "Sobremesas"},
            {"id": "4", "nome": "Bebidas"}
        ]
        save_json(categorias, 'menu/categorias.json')
    
    # Cria itens do menu
    if not os.path.exists(os.path.join(data_dir, 'menu/itens.json')):
        itens = [
            {
                "id": "101",
                "nome": "Pão de Alho",
                "preco": 12.90,
                "categoria_id": "1",
                "descricao": "Pão italiano com manteiga de alho e ervas"
            },
            {
                "id": "201",
                "nome": "Picanha",
                "preco": 89.90,
                "categoria_id": "2",
                "descricao": "Picanha grelhada com arroz, farofa e vinagrete"
            },
            {
                "id": "301",
                "nome": "Pudim",
                "preco": 15.90,
                "categoria_id": "3",
                "descricao": "Pudim de leite condensado tradicional"
            },
            {
                "id": "401",
                "nome": "Refrigerante",
                "preco": 7.90,
                "categoria_id": "4",
                "descricao": "Refrigerantes diversos (lata)"
            }
        ]
        save_json(itens, 'menu/itens.json')
    
    # Cria usuários
    if not os.path.exists(os.path.join(data_dir, 'usuarios/usuarios.json')):
        usuarios = [
            {
                "id": "1",
                "usuario": "admin",
                "senha": generate_password_hash("admin"),
                "cargo": "admin",
                "nome": "Administrador"
            },
            {
                "id": "2",
                "usuario": "garcom",
                "senha": generate_password_hash("garcom"),
                "cargo": "garcom",
                "nome": "Garçom"
            }
        ]
        save_json(usuarios, 'usuarios/usuarios.json')
    
    # Cria mesas
    if not os.path.exists(os.path.join(data_dir, 'mesas/mesas.json')):
        mesas = [
            {"id": "1", "nome": "Mesa 1", "lugares": 4, "status": "disponivel"},
            {"id": "2", "nome": "Mesa 2", "lugares": 2, "status": "disponivel"},
            {"id": "3", "nome": "Mesa 3", "lugares": 6, "status": "disponivel"},
            {"id": "4", "nome": "Mesa 4", "lugares": 4, "status": "disponivel"}
        ]
        save_json(mesas, 'mesas/mesas.json')

# Inicializa dados
init_data()

# Rotas
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        usuarios = load_json('usuarios/usuarios.json')
        for user_id, user in usuarios.items():
            if user['usuario'] == usuario and check_password_hash(user['senha'], senha):
                session['user_id'] = user_id
                session['usuario'] = user['usuario']
                session['cargo'] = user['cargo']
                session['nome'] = user['nome']
                return redirect(url_for('index'))
        
        flash('Usuário ou senha inválidos')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    categorias = load_json('menu/categorias.json')
    itens = load_json('menu/itens.json')
    
    return render_template('menu.html', categorias=categorias, itens=itens)

@app.route('/menu/adicionar', methods=['GET', 'POST'])
def adicionar_item_menu():
    if 'user_id' not in session or session['cargo'] != 'admin':
        flash('Não autorizado')
        return redirect(url_for('menu'))
    
    categorias = load_json('menu/categorias.json')
    
    if request.method == 'POST':
        item_id = str(uuid.uuid4())[:8]
        novo_item = {
            "id": item_id,
            "nome": request.form.get('nome'),
            "preco": float(request.form.get('preco')),
            "categoria_id": request.form.get('categoria_id'),
            "descricao": request.form.get('descricao')
        }
        
        itens = load_json('menu/itens.json')
        itens[item_id] = novo_item
        save_json(itens, 'menu/itens.json')
        
        flash('Item adicionado com sucesso')
        return redirect(url_for('menu'))
    
    return render_template('menu_form.html', categorias=categorias)

@app.route('/mesas')
def mesas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    mesas_data = load_json('mesas/mesas.json')
    return render_template('mesas.html', mesas=mesas_data)

@app.route('/pedido/<mesa_id>', methods=['GET', 'POST'])
def pedido(mesa_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    mesas = load_json('mesas/mesas.json')
    mesa = mesas.get(mesa_id)
    
    if not mesa:
        flash('Mesa não encontrada')
        return redirect(url_for('mesas'))
    
    categorias = load_json('menu/categorias.json')
    itens = load_json('menu/itens.json')
    
    # Carrega pedido existente se disponível
    pedidos = load_json('pedidos/pedidos_ativos.json')
    pedido_atual = None
    for pedido_id, pedido in pedidos.items():
        if pedido['mesa_id'] == mesa_id and pedido['status'] == 'ativo':
            pedido_atual = pedido
            pedido_atual['id'] = pedido_id
            break
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        
        if acao == 'adicionar_item':
            item_id = request.form.get('item_id')
            quantidade = int(request.form.get('quantidade', 1))
            
            if not pedido_atual:
                # Cria novo pedido
                pedido_id = str(uuid.uuid4())
                pedido_atual = {
                    "id": pedido_id,
                    "mesa_id": mesa_id,
                    "garcom_id": session['user_id'],
                    "status": "ativo",
                    "itens": [],
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "total": 0
                }
                pedidos[pedido_id] = pedido_atual
            
            # Adiciona item ao pedido
            item = itens.get(item_id)
            if item:
                item_pedido = {
                    "item_id": item_id,
                    "nome": item['nome'],
                    "preco": item['preco'],
                    "quantidade": quantidade,
                    "subtotal": item['preco'] * quantidade
                }
                pedido_atual['itens'].append(item_pedido)
                
                # Atualiza total
                pedido_atual['total'] = sum(item['subtotal'] for item in pedido_atual['itens'])
                
                # Atualiza pedido no armazenamento
                pedidos[pedido_atual['id']] = pedido_atual
                save_json(pedidos, 'pedidos/pedidos_ativos.json')
                
                # Atualiza status da mesa
                mesas[mesa_id]['status'] = 'ocupada'
                save_json(mesas, 'mesas/mesas.json')
                
                flash('Item adicionado ao pedido')
            
        elif acao == 'finalizar_pedido':
            if pedido_atual:
                # Move pedido para completados
                pedidos_completados = load_json('pedidos/pedidos_completados.json')
                pedido_id = pedido_atual['id']
                pedido_atual['status'] = 'completado'
                pedido_atual['hora_finalizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pedidos_completados[pedido_id] = pedido_atual
                save_json(pedidos_completados, 'pedidos/pedidos_completados.json')
                
                # Remove dos pedidos ativos
                del pedidos[pedido_id]
                save_json(pedidos, 'pedidos/pedidos_ativos.json')
                
                # Atualiza status da mesa
                mesas[mesa_id]['status'] = 'disponivel'
                save_json(mesas, 'mesas/mesas.json')
                
                flash('Pedido finalizado')
                return redirect(url_for('mesas'))
    
    return render_template('pedido.html', mesa=mesa, categorias=categorias, itens=itens, pedido=pedido_atual)

@app.route('/relatorios')
def relatorios():
    if 'user_id' not in session or session['cargo'] != 'admin':
        flash('Não autorizado')
        return redirect(url_for('index'))
    
    # Obtém pedidos completados para relatório
    pedidos_completados = load_json('pedidos/pedidos_completados.json')
    
    # Calcula vendas totais
    vendas_totais = sum(pedido['total'] for pedido in pedidos_completados.values())
    
    # Conta pedidos por dia
    pedidos_por_dia = {}
    for pedido in pedidos_completados.values():
        data = pedido['hora_finalizacao'].split(' ')[0]
        if data not in pedidos_por_dia:
            pedidos_por_dia[data] = {'quantidade': 0, 'total': 0}
        pedidos_por_dia[data]['quantidade'] += 1
        pedidos_por_dia[data]['total'] += pedido['total']
    
    return render_template('relatorios.html', vendas_totais=vendas_totais, pedidos_por_dia=pedidos_por_dia)

@app.route('/cozinha')
def cozinha():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Obtém pedidos ativos para exibição na cozinha
    pedidos_ativos = load_json('pedidos/pedidos_ativos.json')
    mesas = load_json('mesas/mesas.json')
    
    return render_template('cozinha.html', pedidos=pedidos_ativos, mesas=mesas)

if __name__ == '__main__':
    app.run(debug=True)