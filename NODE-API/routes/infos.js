var express = require('express');
var router = express.Router();
var Info = require('../controllers/imported_info');


router.get('/',(req,res)=>{
        Info.list()
            .then(dados => res.status(201).jsonp(dados))
            .catch(e => res.status(500).jsonp({error:e}))
  });


router.post('/', function(req, res){
    Info.insert(req.body)
      .then(dados => res.status(201).jsonp({dados: dados}))
      .catch(e => res.status(500).jsonp({error: e}))
  })

module.exports = router;