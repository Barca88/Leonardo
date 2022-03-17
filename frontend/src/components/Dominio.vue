<template>
  <v-form v-model="valid" ref="form">
    <v-container>
      <v-row>
        <v-col cols="6">
          <v-text-field v-if="editing" v-model="formData.id" 
            :rules="[...rules.required,...rules.length30]" 
            :counter="30" label="Identificador" 
            :input="onChange()" readonly/>
            
            <v-text-field v-else v-model="formData.id" 
            :rules="[...rules.required,...rules.length30,...rules.repeatedID]" 
            :counter="30" label="Identificador" 
            :input="onChange()"/>
        </v-col>

        
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <v-textarea
                    v-model="formData.description"
                    label="Descricao"
                    counter
                    outlined
                    auto-grow
                    background-color="#f2f2fc"
                    color="#2A3F54"
                    rows="3"
                    :rules="rules.required"
                    placeholder="Insira uma Descrição"
                    :input="onChange()"
          ></v-textarea>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <v-text-field v-model="formData.scholarity" :rules="[...rules.required,...rules.length75]" :counter="75" label="Escolaridade"/>
        </v-col>
        <v-col cols="6">
          <v-text-field v-model="formData.responsible" :rules="[...rules.required,...rules.length75]" :counter="75" label="Responsável"/>
        </v-col>
      </v-row>

      <v-row class="mt-5">
        <v-col cols="12" md="12">
          <v-textarea
                    v-model="formData.notes"
                    label="Notas"
                    counter
                    outlined
                    auto-grow
                    background-color="#f2f2fc"
                    color="#2A3F54"
                    rows="3"
                    :rules="rules.required"
                    placeholder="Introduza algumas notas sobre o Domínio"
          ></v-textarea>
        </v-col>
      </v-row>

      <v-row>
        <v-col sm="3" md="3" lg="2" xl="2" class="mt-4">
          <p class="grey--text text--darken-1">Tipo de Acesso:</p>
        </v-col>
        <v-radio-group v-model="formData.access_type" row mandatory>
          <v-col xm="1" sm="5" md="5" lg="5" xl="5">
            <v-radio label="Público" value="publico"/>
          </v-col>
          <v-col xm="1" sm="4" md="4" lg="4" xl="5"> 
            <v-radio label="Privado" value="privado"/>
          </v-col>
        </v-radio-group>
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
        sendDescription: '',
      },
      valid: false,
      formData:{
          _id: '',
          id: '',
          description: '',
          scholarity: '',
          responsible: '',
          notes: '',
          access_type: '',
      },
      idDomains: [],

      rules: {
          required: [(v) => !!v || "Field is required"],
          repeatedID: [v => this.checkID(v) || "ID already exists"],
          length30: [v => (v && v.length <= 30) || "Field must be less or equal than 30 characters"],
          length75: [v => (v && v.length <= 75) || "Field must be less or equal than 75 characters"],
          length100: [v => (v && v.length <= 100) || "Field must be less or equal than 100 characters"],
      },
    }  
  },

  created() {
    axios.get(`http://localhost:8001/domain`)
      .then((response)=>{
        response.data.forEach((obj) =>{
          this.idDomains.push(obj.id)
        });
      },(error) =>{
          console.log(error);
    });

    if(this.$route.params.data!=null){
      this.editing = true
      let data = this.$route.params.data
          this.formData._id = data._id
          this.formData.id = data.id
          this.formData.description = data.description
          this.formData.scholarity = data.scholarity
          this.formData.responsible = data.responsible
          this.formData.notes = data.notes
          this.formData.access_type = data.access_type       
    }
  },

  mounted(){
    this.$root.$on('import', data => {
            axios.get(`http://localhost:8001/domain/`+ data)
              .then((response)=>{
                this.formData._id = response.data._id
                this.formData.id = response.data.id,
                this.formData.description = response.data.description,
                this.formData.scholarity = response.data.scholarity,
                this.formData.responsible = response.data.responsible
                this.formData.notes = response.data.notes
                this.formData.access_type = response.data.access_type 
                this.editing = true
              },(error) =>{
                  console.log(error);
              });
    })
  },

  methods: {

    checkID(item){
      return !this.idDomains.find(x => x === item)
    },

    reset () {
      this.$refs.form.reset()
    },

    validate() {
      return this.$refs.form.validate()
    },

    onChange(){
      this.sendObject.sendId = this.formData.id
      this.sendObject.sendDescription = this.formData.description
      this.$root.$emit('change',this.sendObject)
    }
  },
  watch: {
      formData: {
          handler: function() {
            this.$emit('newdataDominio', [this.formData.id,this.formData.description,this.formData.scholarity,
            this.formData.responsible,this.formData.notes,this.formData.access_type,this.editing,this.formData._id]);         
        },
          deep: true
      }
    }   
}
</script>