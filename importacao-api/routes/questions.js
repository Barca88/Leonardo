var express = require('express');
var router = express.Router();
var Question = require('../controllers/imported_questions');


router.get('/',(req,res)=>{
        Question.list()
            .then(dados => res.status(201).jsonp(dados))
            .catch(e => res.status(500).jsonp({error:e}))
  });


// Consultar uma categoria por domínio.
router.get('/statsByDomain/:id', function(req, res) {
Question.lookupDomain(req.params.id)
    .then(dados => res.status(200).jsonp(dados))
    .catch(e => res.status(500).jsonp({error: e}))
});


// Consultar uma categoria por autor.
router.get('/statsByAuthor/:id', function(req, res) {
  Question.lookupAuthor(req.params.id)
      .then(dados => res.status(200).jsonp(dados))
      .catch(e => res.status(500).jsonp({error: e}))
  });


// Consultar uma categoria por domínio.
router.get('/statsByBoth/:author/:domain', function(req, res) {
  Question.lookupBoth(req.params.author,req.params.domain)
      .then(dados => res.status(200).jsonp(dados))
      .catch(e => res.status(500).jsonp({error: e}))
  });


router.put('/:id', function(req, res) {
  Question.edit(req.params.id,req.body)
      .then(dados => res.status(200).jsonp(dados))
      .catch(e => res.status(500).jsonp({error: e}))
  });

router.post('/', function(req, res){
    Question.insert(req.body)
      .then(dados => res.status(201).jsonp({dados: dados}))
      .catch(e => res.status(500).jsonp({error: e}))
  })


module.exports = router;