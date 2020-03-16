Alínea 1: Gerar pares (N1,N2)*

Inicialmente, carregamos o conteúdo do ficheiro para a variável texto.

De seguida, usamos a função frases, de modo a colocar no início de cada uma um caracter, neste caso o '@', para ser possível tratar
depois cada frase individualmente.

Para identificar as entidades, foi usada a mesma estratégia circundando as palavras maiúsculas (entidades possíveis) no decorrer do 
texto por chavetas.

Por fim, na função getPairs, dividimos o texto pelas frases, efetuando um split no caracter '@', guardando-as numa lista.
Percorremos esta lista, usando em cada frase o findall para recolher todas as entidades presentes na frase, colocando as entidades 
encontradas noutra lista. Se o tamanho desta for superior a 1, ou seja, se a frase conter mais que 1 possível entidade, utilizamos a 
biblioteca itertools para obter todas as combinações/pares possíveis entre as entidades.

Alínea 2: Estratégias para reduzir a quantidade de pares

Nesta alínea efetuamos 2 estratégias para remover o "ruído" dos pares, de modo a tentar obter os pares que efetivamente são
compostos por pessoas/entidades.

A primeira baseou-se em pré-definir uma lista de termos (uma espécie de black-list), guardada na variável terms, que correspondem ou 
a conectores de discurso, ou verbos, ou a artigos, entre outros. Posteriormente, após a visualização dos resultados para o livro do 
Harry Potter, foram adicionados outras palavras que são específicas ao livro em questão. Efetuando posteriormente a filtragem, 
guardando apenas os pares que não continham aqueles termos.
Também foram retirados os pares que eram compostos pela mesma pessoa, como por exemplo, do tipo ('Harry','Harry').

A segunda estratégia baseou-se em eliminar todos os pares com um número de ocorrências menor que 5.
Assim, na função groupAndRemove, criamos um dicionário pairOccur, que guarda para cada par o número de ocorrências do mesmo.
Percorremos os pares obtidos da estratégia anterior e para cada um deles verificamos se já estão presentes no dicionário, efetuando
o update do valor, incrementando o número de ocorrências, caso tal seja verdade. Confirmamos também se o par oposto já está guardado,
de modo a que os pares do tipo ('Ron','Harry') e ('Harry','Ron') sejam contabilizados como o mesmo par. Caso não esteja presente no
dicionário, é adicionado com 1 ocorrência.
Por fim, eliminamos os elementos com uma frequência inferior a 5.

Alínea 3: Interpretador

Para esta alínea era pedido que fosse implementado um interpretador cujo objetivo é apresentar as K relações com maior número de ocorrências 
de uma dada personagem, ou seja, o utilizador escolhe a personagem e o número de relações com maior número de ocorrências no livro.

Assim, foi definida uma função designada por interpretador que recebe como argumento um dicionário, neste caso em específico o dicionário 
resultante da função groupAndRemove que contém apenas os pares relevantes e número de ocorrências dos mesmos. São criadas 2 variáveis, 
designadas por char e top que guardam a personagem e o número de relações com maior número de ocorrências, respetivamente, passadas como input
pelo utilizador. 

É criada uma lista auxiliar inicialmente vazia que vai guardar apenas as relações em que aparecem a personagem escolhida. Depois essa lista 
é ordenada decrescentemente pelo número de ocorrências das relações e o output será apenas as (top) relações com maior número de ocorrências 
e o número de ocorrências das mesmas. Caso a personagem escolhida não pertenca à lista, é devolvida uma mensagem (No relevant relationships found...)

Alínea 4: Grafo de relações

Para o desenho do grafo foram usadas as bibliotecas networkx, matplotlib e seaborn (necessárias instalar para conseguir usar a interface)

 $ python3 -mpip install matplotlib
 $ pip install networkx
 $ pip install seaborn

Este permite apresentar o grafo com todas as relações existentes ou apenas as relações de uma dada personagem (escolhida pelo utilizador).
Foi criada uma função designada criaGrafo que recebe como argumento um dicionário com os pares e o número de ocorrências de cada um. É criada
uma lista vazia que posteriormente vai guardar apenas os pares (keys) do dicionário.

São criadas 2 variáveis, resposta e nome, que vão guardar como resultado o input dado pelo utilizador (yes|no e o nome da personagem, 
respetivamente). Caso a resposta seja "yes" são apresentados todos os nodos e ligações entre estes (é percorrida a lista com os pares e para 
cada par caso não exista são criados os nodos e a ligação entre estes). Caso resposta seja "no" é pedido o nome da personagem de quem se 
pretende ver as relações.

Assim é percorrida a lista com os pares e criados os nodos e ligações apenas nas quais aparece a personagem escolhida.
Esta biblioteca permite criar os nodos (caso não existam) e as ligações simultaneamente com o método add_edge().
Na apresentação do grafo inteiro escolhemos por não definir um threshold, porque achamos que as relações apresentadas eram todas importantes 
já que ocorrem um número considerável de vezes.
Para melhor visualização dos nodos, na interface, é possível clicar na lupa e ampliar selecionando a área pretendida, tendo assim uma melhor 
percepção, no caso em que aparecem muitos nodos juntos. 


