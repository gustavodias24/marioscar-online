from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/consultar', methods=['POST'])
def consultar():
    cpf_cnpj = request.form['cpf_cnpj']

    resp = requests.get('https://mario-s-car-default-rtdb.firebaseio.com/os.json').json()

    ids_os = [i for i in resp]

    listaDeOs = []
    for id_os in ids_os:
        objetoRaw = resp.get(id_os)

        documento = objetoRaw.get('usuarioModel').get('documento')

        if documento == cpf_cnpj:

            fotosString = ""
            if objetoRaw.get('fotos'):
                for foto in objetoRaw.get('fotos'):
                    fotosString += (foto + "\n")

            itensString = ""
            if objetoRaw.get('itens'):
                for item in objetoRaw.get('itens'):
                    itensString += ("Produto: " + item.get('nomeProduto') + "\n")
                    itensString += ("Quantidade: " + str(item.get('quantidade')) + "\n")
                    itensString += ("Valor Uni: " + str(item.get('valor')) + "\n")
                    valorTotal = float(item.get('valor').replace(",", ".")) * int(item.get('quantidade'))
                    itensString += ("Valor Total: R$ " + str(valorTotal) + "\n" + "\n‎\n" )

            servicossString = ""
            if objetoRaw.get('servicos'):
                for servico in objetoRaw.get('servicos'):
                    servicossString += ("Nome: " + servico.get('nomeProduto') + "\n")
                    servicossString += ("Quantidade: " + str(servico.get('quantidade')) + "\n")
                    servicossString += ("Valor Uni: " + str(servico.get('valor')) + "\n")
                    valorTotal = float(servico.get('valor').replace(",", ".")) * int(servico.get('quantidade'))
                    servicossString += ("Valor Total: R$ " + str(valorTotal) + "\n" + "\n‎\n")


            listaDeOs.append(
                f"""
                    Número da OS: {objetoRaw.get('numeroOs')}\n
                    Data: {objetoRaw.get('data')}\n
                    Descrição: {objetoRaw.get('descricao')}\n
                    \n‎\n‎\n 
                    Peças: \n‎\n {itensString}\n
                    \n‎\n‎\n 
                    Serviços: \n‎\n{servicossString} \n
                    \n‎\n‎\n 
                    Cabeçote: {"Sim" if objetoRaw.get('cabecote') else "Não"}\n
                    Mancais do Cabeçote: {"Sim" if objetoRaw.get('mancaisCabecote') else "Não"}\n
                    Comando: {"Sim" if objetoRaw.get('comando') else "Não"}\n
                    Gaiola: {"Sim" if objetoRaw.get('gaiola') else "Não"}\n
                    Vela: {"Sim" if objetoRaw.get('vela') else "Não"}\n
                    Bloco: {"Sim" if objetoRaw.get('bloco') else "Não"}\n
                    Mancais do Bloco: {"Sim" if objetoRaw.get('mancaisBloco') else "Não"}\n
                    Virabrequim: {"Sim" if objetoRaw.get('virabrequim') else "Não"}\n
                    Biela: {"Sim" if objetoRaw.get('biela') else "Não"}\n
                    Motor Montado: {"Sim" if objetoRaw.get('motorMontado') else "Não"}\n
                    Obs:  {objetoRaw.get('obs')}\n
                    \n‎\n‎\n 
                    Fotos: \n‎\n{fotosString} \n
                    \n‎\n‎\n 
                   
                    Aguardando Orçamento: {objetoRaw.get('aguardandoOrcamentoHoraData')}\n
                    Aguardando Autorização: {objetoRaw.get('aguardandoAutorizacaoHoraData')}\n
                    Serviço Autorizado: {objetoRaw.get('servicoAutorizadoHoraData')}\n
                    Serviço em Execução: {objetoRaw.get('servicoEmExecucaoHoraData')}\n
                    Serviço Concluído: {objetoRaw.get('servicoConcluidoHoraData')}\n
                    Saiu para Entrega: {objetoRaw.get('saiuParaEntregaHoraData')}\n
                    Entregue: {objetoRaw.get('entregueHoraData')}\n
                    
                """)

    resultado_json = {
        "cpf": cpf_cnpj,
        "os": listaDeOs,
    }

    return render_template('resultado.html', resultado=resultado_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
