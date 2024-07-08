import requests
import matplotlib.pyplot as plt
url = "http://localhost:3000/filmes"

def titulo(texto, sublinhado="-"):
  print()
  print(texto)
  print(sublinhado*40)

def incluir():
  titulo("Inclusão de Filmes")

  nome    = input("Título do Filme: ")
  genero  = input("Gênero.........: ") 
  duracao = int(input("Duração........: "))
  preco   = float(input("Preço R$.......: "))

  response = requests.post(url, 
                           json={"titulo": nome, 
                                 "genero": genero, 
                                 "duracao": duracao, 
                                 "preco": preco})
  
  if response.status_code == 201:
    filme = response.json()
    print(f"Ok! Filme cadastrado com o código: {filme['id']}")
  else:
    print("Erro... Não foi possível realizar a inclusão")

def listar():
  titulo("Lista dos Filmes Cadastrados")

  print("Cód. Título do Filme..............: Gênero.....: Duração Preço R$:")
  print("==================================================================")

  response = requests.get(url)

  if response.status_code != 200:
    print("Erro... Não foi possível obter dados da API")
    return
  
  filmes = response.json()

  for filme in filmes:
    print(f"{filme['id']:4d} {filme['titulo']:30s} {filme['genero']:12s} {filme['duracao']:4d}min {filme['preco']:9.2f}")


def alterar():
  listar()  
  
  titulo("Alteração do Preço dos Filmes")

  id = int(input("Código do Filme: "))

  # obtém os dados da API (para verificar se existe e os dados)
  response = requests.get(url)  
  filmes = response.json()

  filme = [x for x in filmes if x['id'] == id]

  if len(filme) == 0:
    print("Erro... Código de Filme Inválido")
    return

  print(f"Título do Filme: {filme[0]['titulo']}")
  print(f"Gênero.........: {filme[0]['genero']}") 
  print(f"Duração........: {filme[0]['duracao']}")
  print(f"Preço R$.......: {filme[0]['preco']:9.2f}")
  print()

  novo_preco = float(input("Novo Preço R$: "))

  response = requests.put(url+"/"+str(id), 
                          json={"preco": novo_preco})
  
  if response.status_code == 200:
    filme = response.json()
    print("Ok! Preço do filme alterado com sucesso")
  else:
    print("Erro... Não foi possível realizar a alteração")

def excluir():
  listar()  
  
  titulo("Exclusão de Filmes")

  id = int(input("Código do Filme: "))

  # obtém os dados da API (para verificar se existe e os dados)
  response = requests.get(url)  
  filmes = response.json()

  filme = [x for x in filmes if x['id'] == id]

  if len(filme) == 0:
    print("Erro... Código de Filme Inválido")
    return

  print(f"Título do Filme: {filme[0]['titulo']}")
  print(f"Gênero.........: {filme[0]['genero']}") 
  print(f"Duração........: {filme[0]['duracao']}")
  print(f"Preço R$.......: {filme[0]['preco']:9.2f}")
  print()

  confirma = input("Confirma a Exclusão deste Filme(S/N)? ").upper()

  if confirma == "S":
    response = requests.delete(url+"/"+str(id))
  
    if response.status_code == 200:
      print("Ok! Filme Excluído com sucesso")
    else:
      print("Erro... Não foi possível excluir este filme")

def grafico():
  titulo("Gráfico Relacionando Gêneros dos Filmes")

  response = requests.get(url)
  filmes = response.json()

  labels = list(set([x['genero'] for x in filmes]))
  sizes = [0] * len(labels)

  for filme in filmes:
    indice = labels.index(filme['genero'])
    sizes[indice] += 1

  fig, ax = plt.subplots()
  ax.pie(sizes, labels=labels, autopct='%1.1f%%')

  plt.show()

# --------------------------------------------- Programa Principal
while True:
  titulo("Cadastro de Filmes - Uso de API")
  print("1. Inclusão de Filmes")
  print("2. Listagem de Filmes")
  print("3. Alteração de Filmes")
  print("4. Exclusão de Filmes")
  print("5. Gráfico Comparando Gêneros")
  print("6. Finalizar")
  opcao = int(input("Opção: "))
  if opcao == 1:
    incluir()
  elif opcao == 2:
    listar()
  elif opcao == 3:
    alterar()
  elif opcao == 4:
    excluir()
  elif opcao == 5:
    grafico()
  else:
    break  

