<template>
  <v-container>
      <v-app-bar app height="50" color="#172d44" style="margin-left:4px; margin-right: 4px; margin-top: 6px" dark>
        <div class="d-flex align-center">
          <v-img
          alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            :src="require('../assets/raccoon.png')"
            transition="scale-transition"
            width="80"
            style="margin-left:30px;"
          />
          <h4>Leonardo - Sistema de Avaliação e de Ensino</h4>
        </div>

        <v-spacer></v-spacer>
        <div class="d-flex align-center" sm="3">
          <v-row align="center" justify="space-around" >
            <v-col class="text-center">
              <div>
                 <v-dialog v-model="dialog_util" persistent max-width="600px">
                   <template v-slot:activator="{ on: dialog }">
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on: tooltip, attrs }">
                                <v-btn text icon color="white"
                                    v-bind="attrs"
                                    v-on="{ ...tooltip, ...dialog }">
                                    <v-icon>fas fa-question-circle</v-icon>
                                </v-btn>
                            </template>
                            <span>Utilidade</span>
                        </v-tooltip>
                   </template>
                 <v-card>
                   <v-card-title class="utility" white>Utilidade do Inquérito</v-card-title>
                   <v-divider class="utility_divider"></v-divider>
                   <v-card-text class="utility_text">{{utility}}</v-card-text>
                   <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text @click="dialog_util = false"><v-icon>fas fa-sign-out-alt</v-icon></v-btn>
                   </v-card-actions>
                 </v-card>
                </v-dialog>
             </div>
          </v-col>
         </v-row>
        </div>
      </v-app-bar>
    <v-form
    ref="form"
    v-model="valid"
    lazy-validation>
    <v-container fluid>
      <h2>{{inquiry_type}} - Recolha de Opinião</h2>
      <h4 v-if="inquiry_type=='Questões'">{{domain}} - {{subdomain}}</h4>
      <v-list-item-group class="opinions">
        <v-list-item v-for="(next, i) in questions" :key="i">
          <v-container fluid>
            <p style="font-size: 0.875rem;">
                <b>{{i+1}}.</b> 
                {{next.text}}
            </p>
            <v-radio-group v-model="answers[next.property]" row>
              <v-radio color="#00cc99" :value="0" :label="'Não sei'"
              @change="update(0,next.property)"/>
              <v-radio color="#00cc99" v-for="n in 5" :key="n" :value="n" :label="`${n}`"
              @change="update(n,next.property)"/>
            </v-radio-group>
          </v-container>
        </v-list-item>
      </v-list-item-group>
      <v-textarea
          color="#00cc99" 
          v-if="comment"
          label="Comentário"
          auto-grow
          outlined
          rows="3"
          row-height="30"
          v-model="comments"
      ></v-textarea>
      <div class="buttons">
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn :disabled="!valid" 
                class="mr-4 white--text text-capitalize" 
                color="#00cc99" @click="validate" 
                v-bind="attrs"
                v-on="on">
                <v-icon>fas fa-check</v-icon>
              </v-btn>
            </template>
            <span>Submissão do formulário</span>
          </v-tooltip>
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn class="mr-4 white--text text-capitalize" 
                color="#172d44" @click="reset"
                v-bind="attrs"
                v-on="on">
                <v-icon>fas fa-sync-alt</v-icon>
              </v-btn>
            </template>
            <span>Limpeza do formulário</span>
          </v-tooltip>
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn class="mr-4 white--text text-capitalize" 
                color="red" @click="sendAnswer"
                v-bind="attrs"
                v-on="on">
                <v-icon>fas fa-sign-out-alt</v-icon>
              </v-btn>
            </template>
            <span>Saída da aplicação</span>
          </v-tooltip>   
    </div>
    <v-dialog v-model="dialog_valid" persistent max-width="600px">
      <v-card>
        <v-card-title class="utility" white><i class="fas fa-exclamation-triangle"></i></v-card-title>
        <v-divider class="utility_divider"></v-divider>
        <v-card-text class="utility_text">O preenchimento do inquérito não foi devidamente realizado.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog_valid = false"><v-icon style="font-size: 1.5em;">fas fa-sign-out-alt</v-icon></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </v-container>
    </v-form>
  </v-container>
</template>

<style>
html {
  overflow: auto !important;
  overflow-y: scroll !important;
  font-family: Arial, Helvetica, sans-serif;
}
.v-application {
  font-family: Arial, Helvetica, sans-serif !important;
}
.v-label {
  font-size: 0.875rem;
}
.opinions {
    margin-top: 25px;
}
.opinions .v-list-item {
    height: 95px;
}
.buttons {
    margin-top: 25px;
}
.v-icon.v-icon {
    font-size: 20px !important;
}
.v-dialog > .v-card > .v-card__title {
    font-size: 1.25rem !important;
}
.v-input--radio-group.v-input--radio-group--row .v-radio {
    margin-right: 10px;
}
.utility {
  color: white;
  background-color: #172d44;
}
.utility_divider {
    margin-top: 10px;
}
.utility_text {
    margin-top: 25px;
}
</style>

<script>

export default {
  name: 'Opinion',
  data() {
    return {
      valid: true,
      comment: false,
      finished: false,
      question: null,
      answers: {},
      questions: [],
      rb: '',
      comments: '',
      inquiry_id: '',
      dialog_util: false,
      utility: '',
      inquiry_type: '',
      dialog_valid: false,
      user: null,
      domain: '',
      subdomain: ''
    };
  },
  methods: {
    /*
      Este método atribui valores default às várias questões
      com radio buttons (default => "Não sei" => 0)
    */
    default_answers() {
      const answers = {};
      this.questions.forEach((item) => {
        answers[item.property] = 0;
      });
      return answers;
    },
    /*
      Este método faz reset do formulário para os valores default
      (os comentários vazios e os radio buttons para 'Não sei')
    */
    reset() {
      this.comments = '';
      this.answers = this.default_answers();
      console.log(this.answers);
    },
    /*
      Este método verifica se o formulário está valido para ser enviado
        (que todas as perguntas têm resposta).
      Se for válido este envia para a rota POST.
    */
    async validate() {
      if (this.validateAnswers()) {
        this.dialog_valid= true;
      } else if (this.$refs.form.validate()) {
        this.submit();
      }
    },
    validateAnswers() {
      const allFalseKeys = Object.keys(this.answers).every(k => this.answers[k] === 0) && this.comments === ''
      return allFalseKeys
    },
    submit() {
        this.finished = true;
        this.sendAnswer();
    },
    /*
      Este método vai buscar ao servidor o inquérito correspondente.
    */
    getQuestions() {
      this.$http.get('https://leonardo.di.uminho.pt/api/v0/inquiries/inquiry?inquiry=' + this.inquiry_id)
        .then((res) => {
          this.questions = res.data.questions;
          if (res.data.comments === 'true') {
            this.comment = true;
          }
          this.answers = this.default_answers();
          // eslint-disable-next-line
          // this.inquiry_id = res.data.inquiry_id;
          this.Answer_start_time = new Date();
          this.utility = res.data.utility
          const type = res.data.type
          if(type=='se') {
            this.inquiry_type = 'Sessões'
          } else if (type=='sy') {
            this.inquiry_type = 'Sistema'
          } else {
            this.inquiry_type = 'Questões'
            this.question = this.$store.getters.get_session_question.content['id']
            this.domain = this.$store.getters.get_quizz_parameters.domain
            var subdomains = eval(this.$store.getters.get_quizz_parameters.subdomains)
            if (subdomains.length > 1) {
                var last = subdomains.pop();
                this.subdomain = subdomains.join(', ') + " e " + last
            } else {
                this.subdomain = subdomains[0]
            }
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    /*
      Este método envia ao servidor as respostas ao questionário
    */
    sendAnswer() {
      var log;
      if (this.finished)
        log = this.createLog('Submited');
      else
        log = this.createLog('Canceled')
      this.$http.post('https://leonardo.di.uminho.pt/api/v0/inquiries/inquiry_answers', {
            'log': log,
            'answers': this.formatAnswer(),
            'date': new Date(),
            'finished': this.finished,
            'user': this.user,
            'question': this.question,
            'inquiry_id': this.inquiry_id
        })
        .then((res) => {
          // eslint-disable-next-line
          console.log(res);
          window.parent.close();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    /*
      Este método atualia as respostas das questões com radio
      buttons associados
    */
    update(value, property1) {
      this.answers[property1] = value;
      console.log(this.answers);
    },
    /*
      Este método cria um objeto no formato JSON com um log da operação executada.
    */
    createLog(logOperation) {
      const d = new Date();
      var body = {
        "inquiry_id": this.inquiry_id,
        "question": this.question,
        "operation": logOperation,
        "date": d,
      };
      return body;
    },
    /*
      Este método é responsável por obter o id que está no url
    */
    getUrlId() {
      this.inquiry_id = this.$router.history.current.query['inquiry']  
      this.user = this.$router.history.current.query['id']
      if (this.inquiry_id == null) {
        this.inquiry_id = this.$store.getters.get_inquiry_id
        this.user = this.$store.getters.get_session_user.id
      }
      console.log(this.inquiry_id)
      console.log(this.user)
    },
    /*
      Este método é responsável por tratar do JSON relativo à 'Answer'
    */
    formatAnswer() {
      var ans = {
        "InquiryAnswer": {
          "Properties": this.answers,
          "Comments": this.comments,
        },
      };
      return ans;
    }
  },
  created() {
    this.getUrlId();
    this.getQuestions();
  },
};
</script>
