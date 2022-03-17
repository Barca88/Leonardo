<template>
    <v-container>
        <v-form v-model="valid" ref="form">
            <v-card elevation="3">
                <h2 class="titulo mb-4 ml-3">Domínio {{this.idDominio}}</h2>
                <p class="field ml-5">Descrição: <span class="fieldtext">{{this.description}}</span></p>
                <v-divider></v-divider>
            </v-card>
            <v-row>          
                <v-col cols="6">  
                    <v-select v-model="formData.default_user_level" class="mt-5" clear dense 
                        :rules="rules.required" :items="min_number" label="Nível de Dificuldade"/>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="6">  
                     <v-text-field class="mt-4" v-model="formData.high_performance_factor" 
                     :counter="3" label="Factor de Desempenho A"/>
                </v-col>
                <v-col cols="6">  
                    <v-text-field class="mt-4" v-model="formData.low_performance_factor" 
                     :counter="3" label="Factor de Desempenho B"/>
                </v-col>
            </v-row>

             <v-row>
                <v-col cols="6">  
                     <v-text-field class="mt-4" v-model="formData.high_skill_factor" 
                     :counter="3" label="Factor de Perícia A"/>
                </v-col>
                <v-col cols="6">  
                    <v-text-field class="mt-4" v-model="formData.low_skill_factor" 
                     :counter="3" label="Factor de Perícia B"/>
                </v-col>
            </v-row>

            <v-row>
                <v-col cols="6">
                    <v-select v-model="formData.min_questions_number" clear dense 
                    :rules="rules.required" :items="min_number" label="Número mínimo de Questões"/>
                </v-col>
                <v-col cols="6">
                    <v-select v-model="formData.question_factor" clear dense 
                    :rules="rules.required" :items="quest_factor" label="Factor de Questões"/>
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
            idDominio: '',
            description: '',
            editing: false,
            formData:{
                default_user_level: '',
                high_performance_factor: '',
                low_performance_factor: '',
                high_skill_factor: '',
                low_skill_factor: '',
                min_questions_number: '',
                question_factor: ''
            },
            rules: {
                required: [(v) => !!v || "Field is required"],
            },
            diff_level:['1','2','3','4','5'],
            min_number:['1','2','3','4','5','6'],
            quest_factor:['1','2','3']
        }
    },
    created() {
      if(this.$route.params.data!=null){
        let data = this.$route.params.data
            this.formData.default_user_level = data.default_user_level
            this.formData.high_performance_factor = data.high_performance_factor
            this.formData.low_performance_factor = data.low_performance_factor
            this.formData.high_skill_factor = data.high_skill_factor
            this.formData.low_skill_factor = data.low_skill_factor 
            this.formData.min_questions_number = data.min_questions_number 
            this.formData.question_factor = data.question_factor    
      }
    },
    mounted() {
      this.$root.$on('change', data => {
            this.idDominio = data.sendId
            this.description = data.sendDescription
      })
      this.$root.$on('import', data => {
            axios.get(`http://localhost:8001/domain/`+ data)
              .then((response)=>{
                this.formData.default_user_level = response.data.default_user_level
                this.formData.high_performance_factor = response.data.high_performance_factor
                this.formData.low_performance_factor = response.data.low_performance_factor
                this.formData.high_skill_factor = response.data.high_skill_factor
                this.formData.low_skill_factor = response.data.low_skill_factor 
                this.formData.min_questions_number = response.data.min_questions_number 
                this.formData.question_factor = response.data.question_factor 
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
              this.$emit('newdataComportamento', [this.formData.default_user_level,
              this.formData.high_performance_factor,this.formData.low_performance_factor,
              this.formData.high_skill_factor,this.formData.low_skill_factor,
              this.formData.min_questions_number,this.formData.question_factor]);            
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
