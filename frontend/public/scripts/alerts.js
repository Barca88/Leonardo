import axios from 'axios'

export default {
    logPopup (popup){
        // Log it on the db
        console.log(popup)
        axios.post(`${process.env.VUE_APP_BACKEND}/importation/imported_errors?nome=${this.$store.state.user._id}`,popup)
            .then((res) => {
            console.log("errrrrrrrorrrrrrrrr")
            console.log(res.response)
            if (res.response) {
              // Request made and server responded
              console.log(res.response.data);
              console.log(res.response.status);
              console.log(res.response.headers);
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
            dialog: true,
            createdAt: new Date()
        }
        console.log("1111111111111111111111")
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
            dialog: true,
            createdAt: new Date()
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
            dialog: true,
            createdAt: new Date()
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
            dialog: true,
            createdAt: new Date()
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
            dialog: true,
            createdAt: new Date()
        }
        this.logPopup(popup)
        return popup
    }
}
