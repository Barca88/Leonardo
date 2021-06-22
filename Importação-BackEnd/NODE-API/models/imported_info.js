var mongoose = require('mongoose');

var infoSchema = new mongoose.Schema({
    type: {type:String,required:false},
    name: {type:String,required:false},
    number:{type: Number,required: false},
    date: {type:String,required:false},
    size:{type: Number,required: false}
})

module.exports = mongoose.model('imported_infos',infoSchema);