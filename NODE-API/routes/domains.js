var express = require('express');
var router = express.Router();
var Domain = require('../controllers/domains');

router.get('/',(req,res)=>{
        Domain.list()
            .then(dados => res.status(201).jsonp(dados))
            .catch(e => res.status(500).jsonp({error:e}))
  });


router.post('/', function(req, res){
    Domain.insert(req.body)
      .then(dados => res.status(201).jsonp({dados: dados}))
      .catch(e => res.status(500).jsonp({error: e}))
  })

module.exports = router;