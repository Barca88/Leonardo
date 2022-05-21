import axios from 'axios'

export default {
    logPopup : async function (popup, user){
        // Log it on the db
        await axios.post(`${process.env.VUE_APP_BACKEND}/importation/imported_errors?nome=${user}`,popup)
            .then((res) => {
            if (res.response) {
              // Request made and server responded
              console.log(res.response.data);
              console.log(res.response.status);
              console.log(res.response.headers);
            }
        });
    },
    // Alert functions also log errors in the errors database
    importDialog:function(correct, failed, user){
        // Create the popup
        var popup = {
            header: "Informação",
            message: "Ficheiro importado.</br>" + correct + " novas questões inseridas no sistema.</br>" + failed + " questões recusadas.",
            confirmB: false,
            type: "info",
            dialog: true,
            createdAt: new Date()
        }
        this.logPopup(popup,user)
        return popup
    },
    infoDialog:function(text,user){
        // Create the popup
        var popup = {
            header: "Informação",
            message: text,
            confirmB: false,
            type: "info",
            dialog: true,
            createdAt: new Date()
        }
        this.logPopup(popup,user)
        return popup
    },
    errorDialog:function(text,user){
        // Create the popup
        var popup = {
            header: "Erro",
            message: text,
            confirmB: false,
            type: "del",
            dialog: true,
            createdAt: new Date()
        }
        this.logPopup(popup,user)
        return popup
    },
    warningDialog: function(text,user){
        // Create the popup
        var popup = {
            header: "Aviso",
            message: text,
            confirmB: false,
            type: "warn",
            dialog: true,
            createdAt: new Date()
        }
        this.logPopup(popup,user)
        return popup
    },
    confirmDialog: function(text,user){
        // Create the popup
        var popup = {
            header: "Confirmação",
            message: text,
            confirmB: true,
            type: "confirm",
            dialog: true,
            createdAt: new Date()
        }
        console.log(popup)
        this.logPopup(popup,user)
        return popup
    }
}
