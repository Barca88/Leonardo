var mongoose = require('mongoose');
var Question = require('../models/imported_questions');


// Devolve a lista de Questions
module.exports.list = ()=>{
    return Question
        .find()
        .exec()
}

// Devolve a lista de Questions por Author
module.exports.lookupAuthor = author=>{
    return Question
        .find({author: author})
        .exec()
}

// Devolve a lista de Questions por Domínio
module.exports.lookupDomain = domain=>{
    return Question
        .find({domain: domain})
        .exec()
}

// Devolve a lista de Questions por Domínio & Autor
module.exports.lookupBoth = (author,domain) =>{
    return Question
        .find({domain: domain,author:author})
        .exec()
}

// Permite inserir uma question
module.exports.insert = question  =>{
    var newQuestion = new Question (question);
    return newQuestion.save()
}

// Permite editar a flag de uma question
module.exports.edit = (id,question) => {
    return Question.findOneAndUpdate({identifier:id},{flag:question.flag});
}

