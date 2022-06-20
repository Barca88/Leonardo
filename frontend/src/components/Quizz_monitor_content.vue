<template>
  <v-card>
    <HeaderModal/>
    <v-container>
      <div>
        <v-row cols="12">
          <v-col cols="12">
            <v-row>
              <v-card class="ml-4 mt-1" color="#172d44" flat height="65px" width="70px">
                <div>
                  <v-icon v-bind:style="'border: 0px #172d44; color: white; border-radius:0%; size: 30; height: 65px; width: 70px;'">mdi-text-account</v-icon>
                </div>
              </v-card>
              <v-card class="ml-0" flat>
                <v-card-title style="font-size: 20px;"><b>Monitorização do Quizz</b></v-card-title>
              </v-card>
              <v-card flat>
                <v-card-text style="font-size: 16px;">
                  <h3>Answers_time: {{ quizz_monitor_info.answers_time }}</h3>
                  <h3>Performance: {{ quizz_monitor_info.performance }}</h3>
                  <li v-for="item in quizz_monitor_info.profile" :key="item.id">
                    {{ item }}
                  </li>
                </v-card-text>
              </v-card>
            </v-row>
          </v-col>
        </v-row>
      </div>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
            <v-btn class="white--text text-capitalize; mr-3" color="#00cc99" @click="quit()" v-bind="attrs" v-on="on"><v-icon>mdi-door-open</v-icon></v-btn>
            </template>
            <span>Sair</span>
        </v-tooltip>
      </v-card-actions>
    </v-container>
  </v-card>
</template>

<script>
  import HeaderModal from './Header_modal';
  export default {
    name: 'Quizz_monitor_content',

    props: ['flag','username'],

    components: {
      HeaderModal
    },

    data: function () {
        return {
            isOpen: true,
            quizz_monitor_info: {
              answers_time: 0,
              performance: 0,
              profile: [],
            }
        }
    },

    async created() {
      await this.getQuizzParameters()
    },

    watch: {
        async flag_value(new_flag_value, old_flag_value){
          console.log("Valor antigo para a flag:", old_flag_value)
          if(new_flag_value == true) await this.getQuizzParameters()
        }
    },
    methods: {
      quit: function() {
            this.$emit("quit")
      },
      async getQuizzParameters(){
        await this.$http.get('http://localhost:5000/api/v0/evaluation/quizzParameters?username=' + this.username)
          .then(result => {
            var data = result.data

            this.quizz_monitor_info.answers_time = data.answers_time
            this.quizz_monitor_info.performance = data.performance
            this.quizz_monitor_info.profile = data.profile
          })
          .catch(error => { throw(error) })
      }
    },
    computed: {
        flag_value: function(){ return this.flag}
    }
  }
</script>
