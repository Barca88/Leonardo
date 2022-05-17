<template>
    <v-app>
        <div id="outerbox">
            <h2>Importação de Questões</h2>
            <div class="fileSelection">
                Ficheiro: <span class="selected">{{ selectedFile }}</span>
                <label for="file-upload">
                    <v-icon>mdi-paperclip</v-icon>
                </label>
                <input enctype=multipart/form-data name="questions" id="file-upload" v-on:change="handleChanged" accept=".leo,.json" type="file"/>
            </div>
            <div id="btn-group">
                <v-btn id="im-btn" color="#ebc610" v-on:click="importFile" dark>
                    <v-icon>mdi-check-box-outline</v-icon>
                </v-btn>
                <v-btn color="#22e0ca" v-on:click="clear" class="im-btn" dark>
                    <v-icon>mdi-eraser</v-icon>
                </v-btn>
                <v-btn color="#16207f" v-on:click="help" class="im-btn" dark>
                    <v-icon>mdi-help</v-icon>
                </v-btn>
            </div>
        </div>
        <GenericAlert :alertPopup="alertPopup"/>
    </v-app>
</template>

<script>
import axios from 'axios'
import GenericAlert from '../../components/Importacao/GenericAlert.vue'
import alerts from "../../../public/scripts/alerts.js"

export default {
      metaInfo:{
      title:'Leonardo-Importação de Questões'
    },
    data () {
        return {
            selectedFile: "<ficheiro .leo>",
            anySelected: false,
            alertPopup: {},
            actualFile: {}
        }
    },
    components:{
        GenericAlert
    },
    methods: {

        getUserDomains: async  function(){
            //var username=this.$store.state['user']._id;
            var domains =[]
            await axios.get(`${process.env.VUE_APP_BACKEND}/domain/getDomains`,{
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        Authorization: `Bearer: ${this.$store.state.jwt}`,
                        'Access-Control-Allow-Origin': "*"   
                    }
                })
                .then(res =>{

                    res.data.domains.forEach(e => {
                        //if(e.responsible==username)
                            domains.push(e._id);
                    });
                })
                .catch( e => {
                    console.log('Erro a obter a lista de domínios :: '+ e );
                })

                return domains;
        }
        ,
        clear: function(){
            this.selectedFile = "<ficheiro .leo>"
            this.anySelected = false
        },
        async performPOST (json, fileInfo){
            var i, count = 0,domains= await this.getUserDomains()
            for (i in json) {
                console.log(domains)
                json[i].flag = 'pending'
                // post it into the question database
                console.log(domains +'   '+ json[i].domain )
                if(domains.includes(json[i].domain)){
                    await axios.post(`${process.env.VUE_APP_BACKEND}/importation/imported_questions?nome=${this.$store.state.user._id}`,json[i],{
                        headers: {
                            'Content-Type': 'multipart/form-data',
                            Authorization: `Bearer: ${this.$store.state.jwt}`,
                            'Access-Control-Allow-Origin': "*"       
                        }}
                    )
                    .catch(function (error) {
                        console.log("error")
                        console.log(error)
                        console.log(error.response)
                        if (error.response) {
                            count += 1;
                            // Request made and server responded
                            console.log(error.response.data);
                            console.log(error.response.status);
                            console.log(error.response.headers);
                    }
                });
                }
                else {
                       count+=1;
                }
            }
            // post it into the imported files database
            await axios.post(`${process.env.VUE_APP_BACKEND}/importation/imported_info?nome=${this.$store.state.user._id}`,fileInfo,{
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`,
                    'Access-Control-Allow-Origin': "*"       
                }}
            )
            .catch(function (error) {
                console.log(error)
                if (error.response) {
                  // Request made and server responded
                  console.log(error.response.data);
                  console.log(error.response.status);
                  console.log(error.response.headers);
                }
            });
            return count
        },
        async loadJSON (text, isLeo, fileInfo){
            var count = 0, json = text, rest
            // Parse JSON if that hasn't been done yet
            if(isLeo) {
               json = JSON.parse(text)
                fileInfo['type'] = "json"
            } else fileInfo['type'] = "leo"

            // Finish the file info object
            fileInfo['number'] = json.length

            // Wait for the posts to finish so we can present the alert to the user
            count = await this.performPOST(json, fileInfo)
            rest = json.length - count
            console.log("alertttt")
            this.alertPopup = alerts.importDialog(rest, count)
        },
        loadLEO: function(text, fileInfo){
            // Transform .leo into JSON text
            axios.post(`${process.env.VUE_APP_BACKEND}/importation/text?nome=${this.$store.state.user._id}`,text,{
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`,
                    'Access-Control-Allow-Origin': "*"       
                }}
            )
            .then(response => {
                console.log(response.data);
                this.loadJSON(response.data, false, fileInfo);
            })
            .catch(function (error) {
                if (error.response) {
                    // Request made and server responded
                    console.log(error.response.data);
                    console.log(error.response.status);
                    console.log(error.response.headers);
                } else if (error.request) {
                    // The request was made but no response was received
                    console.log(error.request)
                }
            });
        },
        importFile: function(){
            if(this.anySelected) {
                (new Response(this.actualFile)).text().then(
                    x => {                 
                        // Create the file info object
                        var fileInfo = {
                            date: new Date(),
                            name: this.actualFile.name,
                            size: this.actualFile.size
                        }

                        if(this.actualFile.name.endsWith(".json")) this.loadJSON(x, true, fileInfo);
                        else if(this.actualFile.name.endsWith(".leo")) this.loadLEO(x, fileInfo);
                        else {
                            this.alertPopup = alerts.errorDialog("Extensão inválida (tem de ser .leo ou .json).")
                        }
                    }
                );
            } else {
                this.alertPopup = alerts.warningDialog("Nome de ficheiro a importar não indicado.")
            }
        },
        handleChanged: function(e){
            var files = e.target.files
            console.log(files)
            this.actualFile = files[0]
            this.selectedFile = files[0].name
            this.anySelected = true
        },
        help: function(){
        this.alertPopup = alerts.infoDialog("Escolha um ficheiro clicando no símbolo de anexo.<br> De seguida, clique no botão com um certo para importar.")
        }
    }
}
</script>

<style scoped>
#outerbox{
    width: 100%;
    height: 300px;
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px 20px;
    box-sizing: border-box;
    background-color: #e6e6e6;
}
.selected{
    border-bottom: 1px solid black;
    width: 40%;
    display: inline-block;
    margin-right: 10px;
    margin-left: 20px;
}
input[type="file"] {
    display: none;
}
.v-btn{
    margin-right: 10px;
}
h2{
    margin-bottom: 30px;
}
.fileSelection{
    margin-bottom: 80px;
}
</style>
