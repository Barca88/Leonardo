var mongoose = require('mongoose');

var errorSchema = new mongoose.Schema({
    header: {type:String,required:true},
    message: {type:String,required:true},
    type: {type:String,required: true},
    confirmB: {type:Boolean,required:false},
    createdAt: {type:Date,required:false}
})

module.exports = mongoose.model('errors',errorSchema);
