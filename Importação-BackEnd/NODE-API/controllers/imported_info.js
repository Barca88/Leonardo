var mongoose = require('mongoose');
var Info = require('../models/imported_info');


// Devolve a lista de Infos 
module.exports.list = ()=>{
    return Info 
        .find()
        .exec()
}

// Permite inserir uma info 
module.exports.insert = info  =>{
    var newInfo = new Info (info);
    return newInfo.save()
} 
