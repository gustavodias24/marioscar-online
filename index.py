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


        if objetoRaw.get('usuarioModel'):
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
                        valorTotal = float(str(item.get('valor')).replace(",", ".")) * int(item.get('quantidade'))
                        itensString += ("Valor Total: R$ " + str(valorTotal) + "\n" + "\n‎\n" )

                servicossString = ""
                if objetoRaw.get('servicos'):
                    for servico in objetoRaw.get('servicos'):
                        servicossString += ("Nome: " + servico.get('nomeProduto') + "\n")
                        servicossString += ("Quantidade: " + str(servico.get('quantidade')) + "\n")
                        servicossString += ("Valor Uni: " + str(servico.get('valor')) + "\n")
                        valorTotal = float(str(servico.get('valor')).replace(",", ".")) * int(servico.get('quantidade'))
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
                        Alarme: {"Sim" if objetoRaw.get('alarme') else "Não"}\n
                        Bateria: {"Sim" if objetoRaw.get('Bateria') else "Não"}\n
                        Buzina: {"Sim" if objetoRaw.get('buzina') else "Não"}\n
                        Chave de Roda: {"Sim" if objetoRaw.get('chaveRoda') else "Não"}\n
                        Extintor: {"Sim" if objetoRaw.get('extintor') else "Não"}\n
                        Som: {"Sim" if objetoRaw.get('som') else "Não"}\n
                        Tapete: {"Sim" if objetoRaw.get('tapete') else "Não"}\n
                        Trava: {"Sim" if objetoRaw.get('trava') else "Não"}\n
                        Triângulo: {"Sim" if objetoRaw.get('triangulo') else "Não"}\n
                        Vidro: {"Sim" if objetoRaw.get('vidro') else "Não"}\n
                        Macaco: {"Sim" if objetoRaw.get('macaco') else "Não"}\n
                        Obs:  {objetoRaw.get('obs')}\n
                        \n‎\n‎\n 
                        Fotos: \n‎\n{fotosString} \n
                        \n‎\n‎\n 
                       """)
                    #     Aguardando Orçamento: {objetoRaw.get('aguardandoOrcamentoHoraData')}\n
                    #     Aguardando Autorização: {objetoRaw.get('aguardandoAutorizacaoHoraData')}\n
                    #     Serviço Autorizado: {objetoRaw.get('servicoAutorizadoHoraData')}\n
                    #     Serviço em Execução: {objetoRaw.get('servicoEmExecucaoHoraData')}\n
                    #     Serviço Concluído: {objetoRaw.get('servicoConcluidoHoraData')}\n
                    #     Saiu para Entrega: {objetoRaw.get('saiuParaEntregaHoraData')}\n
                    #     Entregue: {objetoRaw.get('entregueHoraData')}\n
                    #
                    # """)

    resultado_json = {
        "cpf": cpf_cnpj,
        "os": listaDeOs,
    }

    return render_template('resultado.html', resultado=resultado_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
