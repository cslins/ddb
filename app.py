from flask import Flask, redirect, url_for, render_template, request


app = Flask(__name__)


tabela_departamento = {'nome_dep':['departamento 1', 'departamento 2', 'departamento 3'], 'num_dep':[1,2,3]}


tabela_funcionario = {'nome_func':['fulano silva', 'fulano goncalves', 'fulano matos', 'fulano oliveira', 'fulano lima', 'fulano martins', 'fulano lins'],
                      'num_dep':[1,2,2,1,1,3,1], 'cpf':['0000', '0001', '0002', '0003', '0004', '0005', '0006']}
    

databases_tabelas = {'db1':{'Funcionario':{'nome_func':['fulano silva', 'fulano goncalves'],
                      'num_dep':[1,2], 'cpf':['0000', '0001']},
                            
                            'Departamento':{'nome_dep':['departamento 1'], 'num_dep':[1]}},
                     
                     
                     'db2':{'Funcionario':{'nome_func':['fulano oliveira', 'fulano lima', 'fulano martins'],
                      'num_dep':[1,1], 'cpf':['0003', '0004']},
                            
                            'Departamento':{'nome_dep':['departamento 2'], 'num_dep':[2]}}}


@app.route('/')
def hello():
    
    all_headers_departamento = list(tabela_departamento.keys())
    all_rows_departamento = list(zip(*tabela_departamento.values()))
    
    all_headers_funcionario = list(tabela_funcionario.keys())
    all_rows_funcionario = list(zip(*tabela_funcionario.values()))
    
    
    dbs = process_dbs(databases_tabelas)
    
    
    dbs_tables = dbs[1]
    dbs = dbs[0]
    


    return render_template('index.html', headers_departamento = all_headers_departamento,
                           rows_departamento = all_rows_departamento, headers_funcionario = all_headers_funcionario,
                           rows_funcionario = all_rows_funcionario, dbs = dbs, dbs_tables = dbs_tables)




@app.route('/insert_info', methods=["GET", "POST"])
def insert_info():
    
    
    
    
    comandos_sql = request.form.get('sqlcommands')
    
    print(comandos_sql)
    
    return redirect('/')


def process_dbs(db_dicts):
    
    dbs = []
    dbs_tables = []
    
    for db in db_dicts:
        
        dbs.append(db)
        
        all_headers_departamento = list(db_dicts[db]['Departamento'].keys())
        all_rows_departamento = list(zip(*db_dicts[db]['Departamento'].values()))
        
        
        all_headers_funcionario = list(db_dicts[db]['Funcionario'].keys())
        all_rows_funcionario = list(zip(*db_dicts[db]['Funcionario'].values()))
        
        dbs_tables.append([all_headers_departamento, all_rows_departamento, all_headers_funcionario, all_rows_funcionario])


    return [dbs,dbs_tables]
    
    
    
    
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)