## Crawler

### Estructures de dades

* **Data Base**: La nostra base de dades és un diccionari amb dues claus, pàgines i paraules. Aquestes claus et permeten indexar  en subdiccionaris, que contenen informació sobre les relacions paraula-pàgina i pàgina-caràcterístiques. 

  ``` python
  db = {
      'pages':{
          'url':{
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

* **Graf dirigit**: El graf dirigit 

