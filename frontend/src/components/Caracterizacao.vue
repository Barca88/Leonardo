<template>
  <v-form v-model="valid" ref="form" >
    <v-container>
      <v-row> 
        <v-col cols="12" md="4">
          <v-text-field v-if="editing" v-model="formData._id" 
            :rules="[...rules.required,...rules.length30]" 
            :counter="30" label="Identificador" 
             readonly/>
            
            <v-text-field v-else v-model="formData._id" 
            :rules="[...rules.required,...rules.length30,...rules.repeatedID]" 
            :counter="30" label="Identificador" 
            />
        </v-col>

        <v-col cols="12" md="4" >
          <v-text-field v-model="formData.study_cycle" :rules="[...rules.required,...rules.length100]" :counter="100" label="Ciclo de Estudos"/>
        </v-col>

        <v-col cols="12" md="4">
          <v-text-field v-model="formData.scholarity" :rules="[...rules.required,...rules.length75]" :counter="75" label="Escolaridade"/>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="4">
          <v-select v-model="formData.domain"
            :rules="[...rules.required,...rules.length100]" 
            label="Domínio"
            :items="this.idDomain"
          />
        </v-col>

        <v-col cols="12" md="4">
          <v-select v-model="formData.subdomain" :rules="[...rules.required,...rules.length100]" :items="this.idSubDomain" label="Subdomínio"/>
        </v-col>
      </v-row>

      <v-row class="mt-5">
        <v-col cols="12" md="12">
          <v-textarea
                    v-model="formData.header"
                    label="Pergunta"
                    counter
                    outlined
                    auto-grow
                    background-color="#f2f2fc"
                    color="#2A3F54"
                    :rules="rules.required"
                    placeholder="Insira a Pergunta"
                    :input="onChange()"
          ></v-textarea>
        </v-col>
      </v-row>
        

      <v-row>
        <v-col cols="12" xl="2" lg="3" md="3" sm="3">
          <p class="grey--text text--darken-1 mt-4">Nível de Dificuldade:</p>
        </v-col>
        <v-radio-group v-model="formData.difficulty_level" row mandatory >
          <v-col cols="12" md="2" sm="2" xm="1">
            <v-radio label="1" value="1"/>
          </v-col>
          <v-col cols="12" md="2" sm="2" xm="1">
            <v-radio label="2" value="2"/>
          </v-col>
          <v-col cols="12" md="2" sm="2" xm="1">
            <v-radio label="3" value="3"/>
          </v-col>
          <v-col cols="12" md="2" sm="2" xm="1">
            <v-radio label="4" value="4"/>
          </v-col>
          <v-col cols="12" md="2" sm="2" xm="1">
            <v-radio label="5" value="5"/>
          </v-col>
        </v-radio-group>
      </v-row>
      
      <v-row>
        <v-col xs="12">
          <v-select v-model="formData.author" :items="this.idUsers" label="Autor"/>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="2" class="mt-4">
          <p class="grey--text text--darken-1">Modo de Visualização:</p>
        </v-col>
        <v-radio-group v-model="formData.display_mode" row mandatory>
          <v-col cols="12" md="4" sm="4" xm="1">
            <v-radio label="G" value="G"/>
          </v-col>
          <v-col cols="12" md="4" sm="4" xm="1">
            <v-radio label="I" value="I"/>
          </v-col>
        </v-radio-group>
      </v-row>

      <v-row>
        <v-col cols="12" sm="4">
          <v-select v-model="formData.answering_time" clear :rules="rules.required" :items="tempos" label="Tempo de Resposta" dense/>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select v-model="formData.type" :rules="rules.required" :items="tipos" label="Tipo de Questão" dense/>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select v-model="formData.repetitions" :items="repeticoes" label="Repetições" dense/>
        </v-col>
      </v-row>
        
      <v-row>
        <v-col cols="8" >
          <v-autocomplete v-model="formData.precedencias" :items="items" dense label="Precedências" multiple/>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>


<script>
import axios from 'axios';
export default {
  data() {    
    return{
      editing: false,
      randomdata: '',
      sendObject:{
        sendId:'',
        sendDomain: '',
        sendHeader: '',
      },
      valid: false,
      idUsers: [],
      formData:{
          _id: '',
          id: '',
          study_cycle: '',
          scholarity: '',
          domain: '',
          subdomain: '',
          header: '',
          difficulty_level: '',
          author: '',
          display_mode: '',
          answering_time: '',
          type: '',
          precedence: [],
          repetitions: '',
          inf: ''
        },
      rules: {
          required: [(v) => !!v || "Field is required"],
          repeatedID: [v => this.checkID(v) || "ID already exists"],
          length30: [v => (v && v.length <= 30) || "Field must be less or equal than 30 characters"],
          length75: [v => (v && v.length <= 75) || "Field must be less or equal than 75 characters"],
          length100: [v => (v && v.length <= 100) || "Field must be less or equal than 100 characters"],
      },
      tempos: ['30', '45', '60','120','180'],
      tipos: ['Conceito','Terminologia','Definição','Exercício','Prova','Outro'],
      repeticoes: ['0','1', '2', '3'],
      idQuestoes: [],
      idSubDomain: [],
      Domain: [],
      idDomain: []
    }  
  },
  async created() {
    await axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions`,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          }
        })
      .then((response)=>{
        response.data.questions.forEach((obj) =>{
          this.idQuestoes.push(obj._id)
        });
        response.data.users.forEach((obj) =>{
          this.idUsers.push(obj._id)
        });
        response.data.domains.forEach((obj) =>{
          this.Domain.push(obj)
          this.idDomain.push(obj._id)
          console.log(this.Domain)
        });
      },(error) =>{
          this.x = error
    });
    if(this.$route.params.data!=null){
      this.editing = true
      let data = this.$route.params.data
      console.log(data)
      let inf = this.$route.params.inf
          this.formData.inf = inf  
          this.formData._id = data._id
          this.formData.study_cycle = data.study_cycle
          this.formData.scholarity = data.scholarity
          this.formData.domain = data.domain._id
          this.formData.subdomain = data.domain.body._id
          this.formData.header = data.header
          this.formData.difficulty_level = data.difficulty_level
          this.formData.author = data.author._id
          this.formData.display_mode = data.display_mode
          this.formData.repetitions = data.repetitions
          this.formData.answering_time = data.answering_time
          this.formData.type = data.type
          this.formData.precedence = data.precedence         
    }else{
        this.formData.inf = "/questions"
    }
  },

  mounted(){
    this.$root.$on('import', data => {
      
            axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions/`+ data)
              .then((response)=>{
                this.formData._id = response.data.question._id
                this.formData.study_cycle = response.data.question.study_cycle
                this.formData.scholarity = response.data.question.scholarity
                this.formData.domain = response.data.question.domain._id
                this.formData.subdomain = response.data.question.domain.body._id
                this.formData.difficulty_level = response.data.question.difficulty_level
                this.formData.author = response.data.question.author._id
                this.formData.display_mode = response.data.question.display_mode,
                this.formData.answering_time = response.data.question.answering_time
                this.formData.type = response.data.question.type
                this.formData.precedence = response.data.question.precedence
                this.formData.repetitions = response.data.question.repetitions
                this.formData.header = response.data.question.header
                this.editing = true
              },(error) =>{
                  this.x=error
              });
    })
    this.$root.$on('reset', data => {
    if(data == false){
      this.formData._id = ""
    }
    this.formData.study_cycle = ""
    this.formData.scholarity = ""
    this.formData.domain = ""
    this.formData.subdomain = ""
    this.formData.difficulty_level = ""
    this.formData.author = ""
    this.formData.display_mode = ""
    this.formData.answering_time = ""
    this.formData.type = ""
    this.formData.precedence = ""
    this.formData.repetitions = ""
    this.formData.header = ""
    })
  },
  
  beforeDestroy(){
    this.$root.$off('import')
    this.$root.$off('reset')
    this.$root.$off('change')
  },

  methods: {

    checkID(item){
      return !this.idQuestoes.find(x => x === item)
    },

    validate() {
      return this.$refs.form.validate()
    },
    
    onDomain(){
      if(this.sendObject.sendDomain != this.formData.domain){
        this.idSubDomain = []
        if(this.formData.domain){
          this.Domain.forEach((obj) =>{
            if(obj._id == this.formData.domain){
              obj.body.forEach((sub) =>{
                this.idSubDomain.push(sub._id)
              });
            }
          });
        }
      }
    },

    onChange(){
      this.sendObject.sendId = this.formData._id
      this.onDomain()
      this.sendObject.sendDomain = this.formData.domain
      this.sendObject.sendHeader = this.formData.header
      if(this.sendObject.sendHeader != "" || this.sendObject.sendDomain != "" || this.sendObject.sendHeader != ""){
        this.$root.$emit('change',this.sendObject)
      }
    },
  },
  watch: {
      formData: {
          handler: function() {
            this.$emit('newdataCaracterizacao', [this.formData._id,this.formData.study_cycle,this.formData.scholarity,this.formData.domain,
            this.formData.subdomain,this.formData.header,this.formData.difficulty_level,this.formData.author,
            this.formData.display_mode,this.formData.answering_time,this.formData.type,this.formData.precedence,this.formData.repetitions,this.editing,this.formData.inf, this.idQuestoes]);
        },
          deep: true
      },
    }   
}
</script>
