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

  ```
  
  ```

  

* **Cua**: Per poder implementar l'algorisme BFS necessitem una cua on anar guardant les url sota la política LIFO.









## Instal·lar dependències

