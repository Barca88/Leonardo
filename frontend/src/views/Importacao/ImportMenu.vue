<template>
    <v-app>
        <div id="outerbox">
            <appHeader :ajuda='ajuda'></appHeader>
            <navDraw></navDraw>
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
import Header from '../../components/header.vue'
import NavDraw from '../../components/navDraw.vue'
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
            teachersCheck: false,
            alertPopup: {},
            actualFile: {},
            questionId: [],
            domain: [],
            domainsForm: [],
            teacher: [],
            responsible: [],
            subdomain: []
        }
    },
    components:{
        GenericAlert,
        'appHeader': Header,
        'navDraw':NavDraw
    },

    created: function () {
    axios.get(`${process.env.VUE_APP_BACKEND}/users/import?nome=${this.$store.state.user._id}&import=questoes`, {
            headers: {
                Authorization: `Bearer: ${this.$store.state.jwt}`
            }
        })
    },

    methods: {

        clear: function(){
            this.selectedFile = "<ficheiro .leo>"
            this.anySelected = false
        },

        async createDomain (json){
            console.log(json)
            let obj = [{
                subdomain: json.subdomain,
                sub_description: json.subdomain_Description
            }]
            if((json.access_type === "publico" || json.access_type === "privado") && json.scholarity && json.domain_description &&
              json.domain && json.notes && json.subdomain && json.subdomain_Description){
                console.log("Criar")
                let formData = new FormData()
                formData.append('_id', json.domain)
                formData.append('description', json.domain_description)
                formData.append('scholarity', json.scholarity)
                formData.append('responsible', this.$store.state.user._id)
                formData.append('notes', json.notes)
                formData.append('access_type', json.access_type)
                formData.append('body', JSON.stringify(obj))
                formData.append('default_user_level', "")
                formData.append('high_performance_factor', "")
                formData.append('low_performance_factor', "")
                formData.append('high_skill_factor', "")
                formData.append('low_skill_factor', "")
                formData.append('min_questions_number', "")
                formData.append('backlog_factor', "")
                formData.append('question_factor', "")
                formData.append('inserted_by', json.inserted_by)
                json.inserted_at = new Date().toLocaleString()
                formData.append('inserted_at', json.inserted_at)


                await axios.post(`${process.env.VUE_APP_BACKEND}/domain/insert?nome=${this.$store.state.user._id}&importation=imp`, formData,{
                    headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization:`Bearer: ${this.$store.state.jwt}`,
                        'Access-Control-Allow-Origin': "*"     
                    }
                    })
                        .then(function(response){
                        console.log(response)
                        },(error) =>{
                            console.log(error);
                    }); 
            }
        },

        async editDomain(json){
            console.log(json)
            let obj = {
                subdomain: json.subdomain,
                sub_description: json.subdomain_Description
            } //adicionar aos que já existem
            console.log(this.domain)
            this.domain.forEach(e => {
                if(e._id === json.domain){
                    e.body.push(obj)
                    obj = e.body
                }
            })
            console.log(this.domain)
            if(json.subdomain && json.subdomain_Description){
                console.log("Editar")
                let formData = new FormData()
                formData.append('_id', this.domain[0]._id)
                formData.append('description', this.domain[0].description)
                formData.append('scholarity', this.domain[0].scholarity)
                formData.append('responsible', this.$store.state.user._id)
                formData.append('notes', this.domain[0].notes)
                formData.append('access_type', this.domain[0].access_type)
                formData.append('body', JSON.stringify(obj))
                formData.append('default_user_level', this.domain[0].default_user_level)
                formData.append('high_performance_factor', this.domain[0].high_performance_factor)
                formData.append('low_performance_factor', this.domain[0].low_performance_factor)
                formData.append('high_skill_factor', this.domain[0].high_skill_factor)
                formData.append('low_skill_factor', this.domain[0].low_skill_factor)
                formData.append('min_questions_number', this.domain[0].min_questions_number)
                formData.append('backlog_factor', this.domain[0].backlog_factor)
                formData.append('question_factor', this.domain[0].question_factor)
                formData.append('inserted_by', this.domain[0].inserted_by)
                formData.append('inserted_at', this.domain[0].inserted_at)

                await axios.post(`${process.env.VUE_APP_BACKEND}/domain/editar?nome=${this.$store.state.user._id}&importation=imp`, formData,{
                    headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization:`Bearer: ${this.$store.state.jwt}`,
                        'Access-Control-Allow-Origin': "*"     
                    }
                    })
                        .then(function(response){
                        console.log(response)
                        },(error) =>{
                            console.log(error);
                    }); 
            }
        },

        async updateData(json){
            //alterar logs
            var user = this.$store.state.user._id
            console.log("UPDATE!!!")
            await axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions?nome=${this.$store.state.user._id}`,{},{
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`,
                    'Access-Control-Allow-Origin': "*"       
                }}
                ).then((res) => {
                    console.log(res)
                    res.data.questions.forEach(e => {
                        this.questionId.push(e._id)
                    });
                    this.domain = res.data.domains.filter(function(e){
                        return e._id === json[0].domain
                    });
                    this.teacher = res.data.users.filter(function(e){
                        return e.name === json[0].author && e.university === json[0].institution
                    });
                    this.responsible = res.data.users.filter(function(e){
                        return e._id === user
                    });
                    this.domainsForm = res.data.domains
                })
                .catch( e => {
                    console.log('Erro a obter a lista de importação de questões :: '+ e );
                })
        },
        
        async validImportation(json){
            console.log("Validar Dominio")
            
            await this.updateData(json)

            console.log(json)
            console.log(this.domain)
            console.log(this.responsible)
            if(this.domain.length == 0 && this.responsible.length != 0){
                console.log("Criar Dominio")
                console.log("1")
                await this.createDomain(json[0])
                console.log("2")
                await this.updateData(json)
                console.log("3")

            }
            console.log("4")
            console.log(json)
            console.log(this.domain)
            if(this.domain.length != 0){
                console.log("tem dominio")
                this.domain[0].body.forEach(b => {
                    if (b.subdomain === json[0].subdomain){
                        this.subdomain.push(b)
                    }
                });
                /*var responsible
                this.domain.forEach(e => {
                    if(e._id === json[0].domain){
                        responsible = e.responsible
                        e.body.forEach(b => {
                            if (b.subdomain === json[0].subdomain){
                                this.subdomain.push(b)
                            }
                        });
                    }
                })*/
                console.log(this.responsible)
                if(this.responsible.length != 0){
                    console.log("tem responsável")
                    console.log(this.subdomain)
                    if(this.subdomain.length == 0){
                        console.log("não tem subdominio")
                        await this.editDomain(json[0]) //está a substituir!!!!
                        await this.updateData(json)
                        /*this.domain.forEach(e => {
                            if(e._id === json[0].domain){
                                responsible = e.responsible._id
                                e.body.forEach(b => {
                                    if (b._id === json[0].subdomain){
                                        this.subdomain.push(b)
                                    }
                                });
                            }
                        })*/
                        //fazer outro get para atualizar~
                        this.domain[0].body.forEach(b => {
                            if (b.subdomain === json[0].subdomain){
                                this.subdomain.push(b)
                            }
                        });
                    }
                    console.log(this.subdomain)
                    console.log(this.teacher)
                    if(this.subdomain.length != 0 && this.teacher.length != 0){
                        return 1
                    }
                }
            }
            return 0
        },

        async performPOST (json, fileInfo){
            const confirm = await this.validImportation(json)
            var i
            var correct = 0, failed = 0   
            console.log(confirm)
            if(confirm){
                console.log("Dominio Correto")
                for (i in json) {
                    json[i].flag = 'pending'
                    json[i].imported = true
                    if (json[i].language == 'pt' || json[i].language == 'PT')
                        json[i].language = 'Portuguese'
                    if (json[i].language == 'fr' || json[i].language == 'FR')
                        json[i].language = 'French'
                    if (json[i].language == 'en' || json[i].language == 'EN')
                        json[i].language = 'English'
                    if (json[i].language == 'es' || json[i].language == 'ES')
                        json[i].language = 'Spanish'
                    console.log(json[i].domain)
                    console.log(json[i].author)
                    console.log(json[i]._id)
                    let inserted_at = new Date().toLocaleString()
                    json[i]["inserted_at"] = inserted_at
                    json[i]["inserted_by"] = this.$store.state.user._id
                    
                    if(!this.questionId.includes(json[i]._id)){
                        await axios.post(`${process.env.VUE_APP_BACKEND}/importation/imported_questions?nome=${this.$store.state.user._id}`,json[i],{
                            headers: {
                                'Content-Type': 'multipart/form-data',
                                Authorization: `Bearer: ${this.$store.state.jwt}`,
                                'Access-Control-Allow-Origin': "*"       
                            }}
                        )
                        .then((res) => {
                            console.log(res)
                            correct += 1
                        })
                        .catch(function (error) {
                            console.log("error")
                            console.log(error)
                            console.log(error.response)
                            if (error.response) {
                                failed += 1;
                                // Request made and server responded
                                console.log(error.response.data);
                                console.log(error.response.status);
                                console.log(error.response.headers);
                        }
                    });
                    }
                    else {
                        failed+=1;
                    }
                }
            }
            // post it into the imported files database
            await axios.post(`${process.env.VUE_APP_BACKEND}/importation/imported_info?nome=${this.$store.state.user._id}&count=${failed}`,fileInfo,{
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
            return correct
        },

        async loadJSON (text, isLeo, fileInfo){
            console.log(isLeo)
            console.log(text)
            var json = text
            var failed = 0, correct = 0
            // Parse JSON if that hasn't been done yet
            if(isLeo) {
               json = JSON.parse(text)
                fileInfo['type'] = "json"
            } else fileInfo['type'] = "leo"

            // Finish the file info object
            fileInfo['number'] = json.length

            // Wait for the posts to finish so we can present the alert to the user
            console.log("leo3")
            correct = await this.performPOST(json, fileInfo)
            failed = json.length - correct
            console.log("alertttt")
            this.alertPopup = alerts.importDialog(correct, failed, this.$store.state.user._id)
        },
        loadLEO: function(text, fileInfo){
            console.log("leo1")
            console.log(text)
            // Transform .leo into JSON text
            axios.post(`${process.env.VUE_APP_BACKEND}/importation/text?nome=${this.$store.state.user._id}`,text,{
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`,
                    'Access-Control-Allow-Origin': "*"       
                }}
            )
            .then(response => {
                console.log("leo2")
                console.log(response);
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
                        console.log("File: ")
                        console.log(x)
                        console.log(fileInfo)
                        if(this.actualFile.name.endsWith(".json")) this.loadJSON(x, true, fileInfo);
                        else if(this.actualFile.name.endsWith(".leo")) this.loadLEO(x, fileInfo);
                        else {
                            this.alertPopup = alerts.errorDialog("Extensão inválida (tem de ser .leo ou .json).",this.$store.state.user._id)
                        }
                    }
                );
            } else {
                this.alertPopup = alerts.warningDialog("Nome de ficheiro a importar não indicado.",this.$store.state.user._id)
            }
        },
        handleChanged: function(e){
            console.log(e)
            var files = e.target.files
            console.log(files)
            this.actualFile = files[0]
            this.selectedFile = files[0].name
            this.anySelected = true
        },
        help: function(){
        this.alertPopup = alerts.infoDialog("Escolha um ficheiro clicando no símbolo de anexo.<br> De seguida, clique no botão com um certo para importar.",this.$store.state.user._id)
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
