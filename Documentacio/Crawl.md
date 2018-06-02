## Crawler

### Estructures de dades

* **Data Base**: La nostra base de dades és un diccionari amb dues claus, pàgines i paraules. Aquestes claus et permeten indexar  en subdiccionaris, que contenen informació sobre les relacions paraula-pàgina i pàgina-caràcterístiques. 

  ``` python
  db = {
      'pages':{
          'url':{
              'url':
              'title':
          	'description': 
          	'score': 
          }
      }
      'words':{
          'word':set(url)
      }
  }
  ```

* **Graf dirigit**: El graf dirigit és una xarxa de relacions, on el fill d'un node és una url que es troba en la web del node pare. S'utilitza la llibreria networkx per implementar un graf dirigit.

  ```python
  from networkx import DiGraph
  G = DiGraph()
  G.add_node(1)
  G.add_node(2)
  G.add_node(3)
  G.add_edge(1,2)
  G.add_edge(3,2)
  print(G.edges())
  >>> [(1,2),(3,2)]
  print(G.nodes())
  >>> [1,2,3]
  ```

  

* **Cua**: Per poder implementar l'algorisme BFS necessitem una cua on anar guardant les url sota la política LIFO. En el nostre cas implementem una cua on cada entrada és una llista de dos elements,(link, distància a explorar). S'utilitza la llibreria deque per implementar la cua, atès a l'eficiència de la seva implementació.

  ``` python
  from collections import deque
  queue = deque()
  #els elements s'afegeixen a l'esquerre per tenir la representacio d'una cua
  queue.appendleft(1)
  queue.appendleft(2)
  queue.appendleft(3)
  queue.pop() #elimina de la cua l'element més a la dreta i el retorna
  >>> 1
  print(queue)
  >>> 2 3
  ```



### Algorisme

El crawler està basat en l'algorisme Breadth First Search (**BFS** ) . Aquest algorisme permet poder anar recorrent layer per layer, i així en cas de trobar una pàgina ja visitada no tenim la necessitat d'explorar-la.

* El curs del nostre algorisme és el següent:
  1.  Afegir la pàgina pare, juntament amb la distància a explorar, en la cua i inicialitzar un set buit.
  2. Executar el **BFS** fins que no hi hagi elements a la cua, és a dir, fins que no haguem de visitar cap altre link més.
  3. 





## Instal·lar dependències

