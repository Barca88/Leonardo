var express = require('express');
var router = express.Router();
var Error = require('../controllers/errors');


router.get('/',(req,res)=>{
        Error.list()
            .then(dados => res.status(201).jsonp(dados))
            .catch(e => res.status(500).jsonp({error:e}))
  });


// Insere um erro.
router.post('/', function(req, res){
    Error.insert(req.body)
      .then(dados => res.status(201).jsonp({dados: dados}))
      .catch(e => res.status(500).jsonp({error: e}))
  })

module.exports = router;