import requests
import matplotlib.pyplot as plt
url = "http://localhost:3000/curso"

def titulo(texto, sublinhado="-"):
  print()
  print(texto)
  print(sublinhado*40)


def incluir():
  titulo("Inclusão de Cursos")

  nome  = input("Nome do Curso..: ")
  tipo  = input("Tipo.........: ") 
  valor = input("Valor Total........: ")
  nomeProfessor   = input("Nome do Professor..: ")



  response = requests.post(url, json=  {"nome": nome,
                                       "tipo": tipo,
                                       "valor": valor,
                                       "nomeProfessor": nomeProfessor})
  
  if response.status_code == 201:
    curso = response.json()
    print(f"OK! Curso cadastrado com sucesso! Código: {curso['id']} ")
  else:
    print(f"Erro...! Não foi possível concluir o cadastro")






def listar():
  titulo("Listagem dos Cursos Disponíveis!")

  print("  Cód.    Nome do Curso........:    Tipo....:      Custo total R$....:     Professor.....: " )
  print("==================================================================================" )

  response = requests.get(url)

  if response.status_code != 200:
    print("Erro...! Não foi possível listar os cursos...")
    return
  

  cursos = response.json()


  for curso in cursos:
    print(f"{curso['id']:4d} {curso['nome']:30s} {curso['tipo']:12s} {curso['valor']:30s} {curso['nomeProfessor']:12s}")





def alterar():

  listar()

  titulo("Alteração de preço dos cursos")

  id = int(input("Código do Curso: "))

  response = requests.get(url)
  cursos = response.json()


  curso = [x for x in cursos if x['id'] == id ]

  if len(curso) == 0:
    print("Erro..! Código do curso inválido!")
    return
  

  print(f"Nome do Curso....: {curso [0] ['nome']}")
  print(f"Tipo.............: {curso [0] ['tipo']}")
  print(f"Valor Total R$...: {curso [0] ['valor']}")
  print(f"Professor: {curso [0] ['nomeProfessor']}")
  print()


  novo_valor = input("Novo Preço R$:    ")


  response = requests.put(url+"/"+str(id), json={"valor": novo_valor})


  if response.status_code == 200:
    curso = response.json()
    print("OK! Preço alterado com sucesso!")
  else:
    print("Erro.... Não foi possível realizar a alteração")




def excluir():

  listar()


  titulo("Exclusão de Cursos")


  id = int(input("Código do Curso: "))

  response = requests.get(url)
  cursos = response.json()

  curso = [x for x in cursos if x['id'] == id]


  if len(curso) == 0:
    print("Erro...! Código do curso inválido!")
    return
  

  print(f"Nome do Curso....: {curso [0] ['nome']}")
  print(f"Tipo.............: {curso [0] ['tipo']}")
  print(f"Valor Total R$...: {curso [0] ['valor']}")
  print(f"Professor: {curso [0] ['nomeProfessor']}")
  print()

  confirma  = input("Confirma a exclusão deste curso(S/N)? ").upper()


  if confirma == "S":
    response = requests.delete(url+"/"+str(id))


    if response.status_code == 200:
      print("Curso excluido com sucesso!")
    else:
      print("Erro... Não foi possível excluir o curso")



def grafico():

  titulo("Gráfico Relacionando os Tipos de Cursos")

  response = requests.get(url)
  cursos   = response.json()


  labels = list(set([x['tipo'] for x in cursos]))
  sizes = [0] * len(labels)

  for curso in cursos:
    indice = labels.index(curso['tipo'])
    sizes[indice] += 1

  fig, ax = plt.subplots()
  ax.pie(sizes, labels=labels, autopct='%1.1f%%')

  plt.show()


# --------------------------------------------- Programa Principal
while True:
  titulo("Cadastro de Filmes - Uso de API")
  print("1. Inclusão de Cursos")
  print("2. Listagem de Cursos")
  print("3. Alteração de Custo")
  print("4. Exclusão de Cursos")
  print("5. Gráfico Comparando Tipos de Cursos")
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
