<template>
  <v-form v-model="valid" ref="form" >
    <v-container>
      <v-row> 
        <v-col cols="12" md="4">
          <v-text-field v-if="editing" v-model="formData._id" 
            :rules="[...rules.required,...rules.length30]" 
            :counter="30" label="Identificador" 
            :input="onChange()" readonly/>
            
            <v-text-field v-else v-model="formData._id" 
            :rules="[...rules.required,...rules.length30,...rules.repeatedID]" 
            :counter="30" label="Identificador" 
            :input="onChange()"/>
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
          <v-text-field v-model="formData.domain"
            :rules="[...rules.required,...rules.length100]" 
            :counter="100" 
            label="Domínio"
            :input="onChange()"
          />
        </v-col>

        <v-col cols="12" md="4">
          <v-text-field v-model="formData.subdomain" :rules="[...rules.required,...rules.length100]" :counter="100" label="Subdomínio"/>
        </v-col>

        <v-col cols="12" md="4">
          <v-text-field v-model="formData.subsubdomain" :rules="[...rules.required,...rules.length100]" :counter="100" label="Subsubdomínio"/>
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
          <v-text-field v-model="formData.author" :rules="[...rules.required,...rules.length75]" :counter="75" label="Autor"/>
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
          <v-select v-model="formData.type_" :rules="rules.required" :items="tipos" label="Tipo de Questão" dense/>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select v-model="formData.repetitions" :rules="rules.required" :items="repeticoes" label="Repetições" dense/>
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
      formData:{
          _id: '',
          id: '',
          study_cycle: '',
          scholarity: '',
          domain: '',
          subdomain: '',
          subsubdomain: '',
          header: '',
          difficulty_level: '',
          author: '',
          display_mode: '',
          answering_time: '',
          type: '',
          precedence: [],
          repetitions: ''
        },
      rules: {
          required: [(v) => !!v || "Field is required"],
          repeatedID: [v => this.checkID(v) || "ID already exists"],
          length30: [v => (v && v.length <= 30) || "Field must be less or equal than 30 characters"],
          length75: [v => (v && v.length <= 75) || "Field must be less or equal than 75 characters"],
          length100: [v => (v && v.length <= 100) || "Field must be less or equal than 100 characters"],
      },
      tempos: ['30', '45', '60'],
      tipos: ['1', '2', '3'],
      repeticoes: ['0','1', '2', '3'],
      idQuestoes: []
    }  
  },
  created() {
    axios.get(`${process.env.VUE_APP_BACKEND}/question`)
      .then((response)=>{
        response.data.forEach((obj) =>{
          this.idQuestoes.push(obj._id)
        });
      },(error) =>{
          console.log(error);
    });

    if(this.$route.params.data!=null){
      this.editing = true
      let data = this.$route.params.data
          this.formData._id = data._id
          this.formData._id = data._id
          this.formData.study_cycle = data.study_cycle
          this.formData.scholarity = data.scholarity
          this.formData.domain = data.domain
          this.formData.subdomain = data.subdomain
          this.formData.subsubdomain = data.subsubdomain
          this.formData.header = data.header
          this.formData.difficulty_level = data.difficulty_level
          this.formData.author = data.author
          this.formData.display_mode = data.display_mode
          this.formData.repetitions = data.repetitions
          this.formData.answering_time = data.answering_time
          this.formData.type_ = data.type_
          this.formData.precedence = data.precedence            
    }
  },

  mounted(){
    this.$root.$on('import', data => {
            axios.get(`${process.env.VUE_APP_BACKEND}/question/`+ data)
              .then((response)=>{
                this.formData._id = response.data._id
                this.formData._id = response.data._id
                this.formData.study_cycle = response.data.study_cycle
                this.formData.scholarity = response.data.scholarity
                this.formData.domain = response.data.domain
                this.formData.subdomain = response.data.subdomain
                this.formData.subsubdomain = response.data.subsubdomain
                this.formData.difficulty_level = response.data.difficulty_level
                this.formData.author = response.data.author
                this.formData.display_mode = response.data.display_mode,
                this.formData.answering_time = response.data.answering_time
                this.formData.type_ = response.data.type_
                this.formData.precedence = response.data.precedence
                this.formData.repetitions = response.data.repetitions
                this.formData.header = response.data.header
                this.editing = true
              },(error) =>{
                  console.log(error);
              });
    })
  },

  methods: {

    checkID(item){
      return !this.idQuestoes.find(x => x === item)
    },

    reset () {
      this.$refs.form.reset()
    },

    validate() {
      return this.$refs.form.validate()
    },
    
    onChange(){
      this.sendObject.sendId = this.formData._id
      this.sendObject.sendDomain = this.formData.domain
      this.sendObject.sendHeader = this.formData.header
      this.$root.$emit('change',this.sendObject)
    },
  },
  watch: {
      formData: {
          handler: function() {
            this.$emit('newdataCaracterizacao', [this.formData._id,this.formData.study_cycle,this.formData.scholarity,this.formData.domain,
            this.formData.subdomain,this.formData.subsubdomain,this.formData.header,this.formData.difficulty_level,this.formData.author,
            this.formData.display_mode,this.formData.answering_time,this.formData.type_,this.formData.precedence,this.formData.repetitions,this.editing,this.formData._id]);
        },
          deep: true
      },
    }   
}
</script>
