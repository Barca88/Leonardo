var mongoose = require('mongoose');

var domainSchema = new mongoose.Schema({
    id: {type:String,required:true,unique:true},
    responsible: {type:String,required:true}
})

module.exports = mongoose.model('domains',domainSchema);
