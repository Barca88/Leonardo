import axios from 'axios'

export default {
    logPopup (popup){
        // Log it on the db
        axios.post('http://localhost:1337/errors', popup)
        .catch(function (error) {
            if (error.response) {
              // Request made and server responded
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
        });
    },
    // Alert functions also log errors in the errors database
    importDialog:function(correct, failed){
        // Create the popup
        var popup = {
            header: "Informação",
            message: "Ficheiro importado.</br>" + correct + " novas questões inseridas no sistema.</br>" + failed + " questões recusadas.",
            confirmB: false,
            type: "info",
            dialog: true
        }
        this.logPopup(popup)
        return popup
    },
    infoDialog:function(text){
        // Create the popup
        var popup = {
            header: "Informação",
            message: text,
            confirmB: false,
            type: "info",
            dialog: true
        }
        this.logPopup(popup)
        return popup
    },
    errorDialog:function(text){
        // Create the popup
        var popup = {
            header: "Erro",
            message: text,
            confirmB: false,
            type: "del",
            dialog: true
        }
        this.logPopup(popup)
        return popup
    },
    warningDialog: function(text){
        // Create the popup
        var popup = {
            header: "Aviso",
            message: text,
            confirmB: false,
            type: "warn",
            dialog: true
        }
        this.logPopup(popup)
        return popup
    },
    confirmDialog: function(text){
        // Create the popup
        var popup = {
            header: "Confirmação",
            message: text,
            confirmB: true,
            type: "confirm",
            dialog: true
        }
        this.logPopup(popup)
        return popup
    }
}
