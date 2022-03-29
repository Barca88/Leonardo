<template>
    <v-container>
        <v-form v-model="valid" ref="form">
            <v-card elevation="3" class="mb-5">
                <h2 class="titulo mb-4 ml-3">Questão {{this.idQuestao}}</h2>
                <p class="field ml-5">Domínio: <span class="fieldtext">{{this.domain}}</span></p>
                <p class="field ml-5">Pergunta: <span class="fieldtext">{{this.header}}</span></p>
                <v-divider></v-divider>
            </v-card>
            <v-row>          
                <v-col cols="8">  
                    <h3 style="color:#2A3F54;padding-bottom:15px;">Escolha os ficheiros de imagem (png/jpg):</h3>
                    <v-file-input
                        show-size
                        counter
                        chips
                        multiple
                        label="Introduzir Imagens"
                    ></v-file-input>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="8">  
                    <h3 style="color:#2A3F54;padding-bottom:15px;">Escolha os ficheiros de video:</h3>
                    <v-file-input
                        show-size
                        counter
                        chips
                        multiple
                        label="Introduzir Videos"
                    ></v-file-input>
                </v-col>
            </v-row>
            
            <v-row class="mt-5">
                <v-col cols="12" md="12">
                    <v-textarea
                        v-model="formData.explanation"
                        label="Explicação"
                        counter
                        outlined
                        auto-grow
                        background-color="#f2f2fc"
                        color="#2A3F54"
                        :rules="rules.required"
                        rows="3"
                        placeholder="Introduza uma explicação sobre a questão"
                    ></v-textarea>
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
                        :rules="rules.required"
                        rows="3"
                        placeholder="Introduza algumas notas sobre a questão"
                    ></v-textarea>
                </v-col>
            </v-row>

            <v-row class="mt-5">
                <v-col cols="12" md="12">
                    <v-textarea
                        v-model="formData.source"
                        label="Fontes"
                        counter
                        outlined
                        auto-grow
                        background-color="#f2f2fc"
                        color="#2A3F54"
                        :rules="rules.required"
                        rows="3"
                        placeholder="Introduza algumas fontes de informação sobre a questão"
                    ></v-textarea>
                </v-col>
            </v-row>

            <v-row>
                <v-col cols="12" sm="6">
                    <v-select v-model="formData.status" clear :rules="rules.required" :items="status" label="Status" dense/>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-select v-model="formData.language" :rules="rules.required" :items="language" label="Language" dense/>
                </v-col>
            </v-row>
        </v-form>
    </v-container>
</template>

<script>
import axios from 'axios';
export default ({
    data(){
        return{
            idQuestao: '',
            domain: '',
            header: '',
            formData:{
                explanation: '',
                notes: '',
                source: '',
                status: '',
                language: ''
            },
            rules: {
                required: [(v) => !!v || "Field is required"],
            },
            status: ['E'],
            language: ['Portuguese', 'English', 'Spanish', 'French'],
        }
    },
    created() {
      if(this.$route.params.data!=null){
        console.log("Edição de questão")
        console.log(this.$route.params.data)
        let data = this.$route.params.data
            this.formData.explanation = data.explanation
            this.formData.notes = data.notes
            this.formData.source = data.source
            this.formData.status = data.status
            this.formData.language = data.language   
      }
    },
    mounted() {
      this.$root.$on('change', data => {
            this.idQuestao = data.sendId
            this.domain = data.sendDomain
            this.header = data.sendHeader
      })
      this.$root.$on('import', data => {
            axios.get(`${process.env.VUE_APP_BACKEND}/question/getDomains/`+ data)
              .then((response)=>{
                this.formData.explanation = response.data.explanation
                this.formData.notes = response.data.notes
                this.formData.source = response.data.source
                this.formData.status = response.data.status
                this.formData.language = response.data.language
              },(error) =>{
                  console.log(error);
              });
      })
    },
    methods: {
      reset () {
        this.$refs.form.reset()
      },
      validate() {
        return this.$refs.form.validate()
      }
    },
    watch: {
        formData: {
            handler: function() {
              this.$emit('newdataSuporte', [this.formData.explanation,this.formData.notes,
              this.formData.source,this.formData.status,this.formData.language]);            
          },
            deep: true
        }
      }     
})
</script>

<style scoped>
  h2.titulo{
    color:#2A3F54;
  }
  p.field{
    color:#2A3F54;
  }
  span.fieldtext{
    color:black;
  }
</style>
