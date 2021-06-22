var mongoose = require('mongoose');
var Domain = require('../models/domains');

// Devolve a lista de Domain 
module.exports.list = ()=> {
    return Domain 
        .find()
        .exec()
}

// Permite inserir um Domain 
module.exports.insert = domain  =>{
    var newDomain = new Domain (domain);
    return newDomain.save()
} 
