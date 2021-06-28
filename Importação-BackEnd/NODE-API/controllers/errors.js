var mongoose = require('mongoose');
var Error = require('../models/imported_errors');


// Devolve a lista de Errors 
module.exports.list = ()=>{
    return Error 
        .find()
        .exec()
}

// Permite inserir um erro 
module.exports.insert = erro  =>{
    var newErro = new Error (erro);
    return newErro.save()
} 
