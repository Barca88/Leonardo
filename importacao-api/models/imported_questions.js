var mongoose = require('mongoose');

var questionSchema = new mongoose.Schema({
    identifier: { type:String,required:true,unique:true},
    languague: {type:String,required:false},
    study_cycle:{type: String,required: false},
    scholarity: {type:String,required:false},
    domain:{type: String,required: false},
    subdomain:{type: String,required: false},
    subsubdomain:{type: String,required: false},
    difficulty_level:{type: String,required: false},
    author:{type: String,required: false},
    display_mode:{type: String,required: false},
    type:{type: String,required: false},
    answering_time:{type: Number,required: false},
    repetitions:{type: Number,required: false},
    header:{type: String,required: false},
    body:{type: JSON,required: false},
    explanation:{type: String,required: false},
    imagens:{type: String,required: false},
    videos:{type: String,required: false},
    source:{type: String,required: false},
    nodes:{type: String,required: false},
    status:{type: String,required: false},
    inserted_by:{type: String,required: false},
    inserted_at:{type: Date,required: false},
    validated_by:{type: String,required: false},
    validated_at:{type: String,required: false},
    precedence:{type: JSON,required: false},
    flag:{type: String,enum:['aproved','rejected','pending'],required: true},
    inserted_at:{type: String,required: false},
    inserted_by:{type: String,required: false},
    validated_at:{type: String,required: false},
    validated_by:{type: String,required: false},
})

module.exports = mongoose.model('imported_questions',questionSchema);


