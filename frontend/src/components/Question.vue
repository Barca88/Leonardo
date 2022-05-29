<template>
    <v-container v-if="1==1">
        <div v-if="final"> <Break :message="message"/> </div>
        <div v-else>
            <div> <h2>Sessão de Avaliação - {{ domain }} <template v-if="this.sub_domains.length > 0"> - {{ this.sub_domains[this.index_last_subdom_searched] }}</template></h2> </div>
            <v-spacer></v-spacer>
            <div v-if="this.out_of_range == 1"> <v-alert dismissible type="error"> Só existem {{ this.current_question.body.length }} opções de resposta </v-alert> </div>
            <div v-if="this.error_process_voice == 1"> <v-alert dismissible type="warning"> Não percebi o que disse, tente novamente </v-alert> </div>
            <div v-if="alert == true"> <v-alert dismissible type="error"> Não respondeu a esta questão </v-alert> </div>
            <v-container v-if="dialog_why" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Porquê'" :symbol="'mdi-help'" :buttonCode="'8.1'" v-on:quit="dialog_why = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_explain" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Explica'" :symbol="'mdi-newspaper'" :buttonCode="'9.1'" v-on:quit="dialog_explain = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_how" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Como'" :symbol="'mdi-loupe'" :buttonCode="'10.1'" v-on:quit="dialog_how = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_gam" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Gamificação'" :symbol="'mdi-trophy'" :text="frase" v-on:quit="dialog_gam = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_rules" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Regras'" :symbol="'mdi-ruler'" :buttonCode="'6.2'" v-on:quit="dialog_rules = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_help" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Ajuda'" :symbol="'mdi-lightbulb'" :buttonCode="'1.3'" v-on:quit="dialog_help = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_statistics" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Estatísticas'" :symbol="'mdi-chart-bar'" :buttonCode="'7.2'" v-on:quit="dialog_statistics = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_about" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Acerca'" :symbol="'fa fa-info-circle'" :buttonCode="'2.4'" v-on:quit="dialog_about = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_monitor" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <QuizzMonitorContent :flag='look_for_monitor_content' :username='this.$store.getters.get_session_user.username' v-on:quit="dialog_monitor = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-card>
                <v-list-item>
                    <v-list-item-content>
                        <v-card-text>
                            <v-card-title>Questão nº: {{ num_question }} | Level {{ current_question.difficulty_level }}</v-card-title>
                            <v-list class="list-group-item">
                                <p>{{ current_question.header }}</p>
                                <v-container>
                                    <v-row>
                                        <v-radio-group v-model="default_answer">
                                            <v-radio color="#00cc99" v-for="r in current_question.body" :value="`${r.answer}`" :key="r.answer" :label="`${r.answer}`" @change="set_given_answer(r.correction, r.points, r.answer)"></v-radio>
                                        </v-radio-group>
                                    </v-row>
                                </v-container>
                            </v-list>
                        </v-card-text>
                    </v-list-item-content>
                    <v-dialog v-model="dialog_image" width="500" v-if="this.num_question %2 == 0">
                        <template v-slot:activator="{ on, attrs }">
                            <v-img src="../assets/basededados.png" max-height="200px" max-width="400px" margin-right="0" float="right" v-bind="attrs" v-on="on"></v-img>
                        </template>
                        <ImageDialog :filename="'basededados.png'"></ImageDialog>
                    </v-dialog>
                    <v-dialog v-model="dialog_image" width="500" v-else>
                        <template v-slot:activator="{ on, attrs }">
                            <v-img src="../assets/faltaimagem.png" max-height="200px" max-width="250px" margin-right="0" float="right" v-bind="attrs" v-on="on"></v-img>
                        </template>
                        <ImageDialog :filename="'faltaimagem.png'"></ImageDialog>
                    </v-dialog>
                </v-list-item>
            </v-card>
            <v-divider></v-divider>
            <div> <v-progress-linear v-model="progress_bar_current_size" :buffer-progress_bar_current_size="progress_bar_initial_size" :background-opacity="opacity" :height="height" color="green"></v-progress-linear> </div>
            <v-row cols="12" style="display: flex; justify-content: space-between">
                <v-col cols="6">
                    <v-row style="height: 150px; float: left">
                        <v-card class="ml-3" flat>
                            <div>
                                <v-tooltip right>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="set_end_time_answer_question(), get_next_question()" class="white--text text-capitalize" color="#e6b800" v-bind="attrs" v-on="on" v-if="label_answer != ''"><v-icon>mdi-checkbox-marked-outline</v-icon></v-btn>
                                        <v-btn @click.stop="dialog = true" class="white--text text-capitalize" color="#e6b800" v-bind="attrs" v-on="on" v-else><v-icon>mdi-checkbox-marked-outline</v-icon></v-btn>
                                    </template>
                                    <span>Resposta</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2" v-if="this.session_mode == 'evaluation'"> <v-btn id="btnAnterior" :disabled="true" class="white--text text-capitalize" color="#00cc99"><v-icon>mdi-chevron-double-left</v-icon></v-btn> </div>
                            <div class="mt-2" v-else>
                                <v-tooltip left>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn class="white--text text-capitalize" color="#00cc99" @click="final = true, message = 'O utilizador terminou o quizz'" v-bind="attrs" v-on="on"><v-icon>mdi-flag-checkered</v-icon></v-btn> </template>
                                    <span>Terminar</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_why = !dialog_why" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-help</v-icon></v-btn> </template>
                                    <span>Porquê</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                        <v-card class="ml-2" flat>
                            <div> <v-btn text disabled></v-btn> </div>
                            <div class="mt-2" v-if="this.session_mode == 'evaluation'">
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="set_end_time_answer_question(), get_next_question()" class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on" v-if="label_answer != ''"><v-icon>mdi-chevron-double-right</v-icon></v-btn>
                                        <v-btn @click="set_end_time_answer_question(), question_was_answered = 0, get_next_question()" class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on" v-else><v-icon>mdi-chevron-double-right</v-icon></v-btn>
                                    </template>
                                    <span>Seguinte</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2" v-else>
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_quit = true" class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on"><v-icon>mdi-door-open</v-icon></v-btn> </template>
                                    <span>Sair</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_explain = !dialog_explain" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-newspaper</v-icon></v-btn> </template>
                                    <span>Explica</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                        <v-card class="ml-2" flat>
                            <div> <v-btn text disabled></v-btn> </div>
                            <div class="mt-2" v-if="this.session_mode == 'evaluation'">
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn class="white--text text-capitalize" color="#00cc99" @click="final = true, message = 'O utilizador terminou o quizz'" v-bind="attrs" v-on="on"><v-icon>mdi-flag-checkered</v-icon></v-btn> </template>
                                    <span>Terminar</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2" v-else>
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on"><v-icon>mdi-chevron-double-left</v-icon></v-btn> </template>
                                    <span>Anterior</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_how = !dialog_how" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-loupe</v-icon></v-btn> </template>
                                    <span>Como</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                        <v-card class="ml-2" flat>
                            <div> <v-btn text disabled></v-btn> </div>
                            <div class="mt-2" v-if="this.session_mode == 'evaluation'">
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_quit = true" class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on"><v-icon>mdi-door-open</v-icon></v-btn> </template>
                                    <span>Sair</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2" v-else>
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="set_end_time_answer_question(), get_next_question()" class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on" v-if="label_answer != ''"><v-icon>mdi-chevron-double-right</v-icon></v-btn>
                                        <v-btn @click="set_end_time_answer_question(), question_was_answered = 0, get_next_question()" class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on" v-else><v-icon>mdi-chevron-double-right</v-icon></v-btn>
                                    </template>
                                    <span>Seguinte</span>
                                </v-tooltip>
                            </div>
                            <div> <v-btn text disabled></v-btn> </div>
                        </v-card>
                    </v-row>
                </v-col>
                <v-col cols="6">
                    <v-row style="height: 150px; float: right">
                        <v-card class="mr-2" flat>
                            <div>
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_monitor = !dialog_monitor" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-text-account</v-icon></v-btn> </template>
                                    <span>Monitorização do Quizz</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_gam = !dialog_gam" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-trophy</v-icon></v-btn> </template>
                                    <span>Gamificação</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_rules = !dialog_rules" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-ruler</v-icon></v-btn> </template>
                                    <span>Regras</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                        <v-card class="mr-2" flat>
                            <div>
                                <v-tooltip left>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn class="white--text text-capitalize" color="#172d44" title="Opinião" @click="popupInquiry()" v-bind="attrs" v-on="on"><v-icon>mdi-comment-outline</v-icon></v-btn> </template>
                                    <span>Opinião</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip left>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="get_action(), reset_variables(), dialog_voice_loading = true, out_of_range = 0" class="white--text text-capitalize" color="#00cc99" title="Voz" v-bind="attrs" v-on="on"><v-icon>mdi-volume-high</v-icon></v-btn> </template>
                                    <span>Voz</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2"> 
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_help = !dialog_help" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-lightbulb</v-icon></v-btn> </template>
                                    <span>Ajuda</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                        <v-card class="mr-3" flat>
                            <div> 
                                <v-tooltip right>
                                    <template v-slot:activator="{ on, attrs }"> <v-btn @click="dialog_statistics = !dialog_statistics" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-chart-bar</v-icon></v-btn> </template>
                                    <span>Estatísticas</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2"> <v-btn class="white--text text-capitalize" color="#00cc99">
                                <v-tooltip right>
                                    <template v-slot:activator="{ on, attrs }"> <v-avatar size="32" v-bind="attrs" v-on="on"> <v-img :src="require('../assets/raccoon.png')"></v-img> </v-avatar> </template>
                                    <span>Leonardo</span>
                                </v-tooltip>
                            </v-btn></div>
                            <div class="mt-2"> 
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="dialog_about = !dialog_about" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on">
                                            <i class="fa fa-info-circle" style="font-size: 22px"></i>
                                        </v-btn>
                                    </template>
                                    <span>Acerca</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                    </v-row>
                </v-col>
            </v-row>
            <v-dialog v-model="dialog" persistent max-width="680">
                <ModalLayout :desc="'Sem resposta'" :symbol="'mdi-alert'" :text="'Não foi apresentada qualquer opção de resposta para a questão apresentada.'" v-on:answerQuestion="dialog = false, reset_variables()" v-on:nextQuestion="set_end_time_answer_question(), question_was_answered = 0, get_next_question()" v-on:quit="dialog = false, final = true, message = 'O utilizador terminou o quizz'"/>
            </v-dialog>
            <v-dialog v-model="dialog_quit" persistent max-width="590">
                <ModalLayout :desc="'Sair da sessão'" :symbol="'mdi-alert'" :text="'Pretende sair da sessão do Quizz?'" v-on:quit="windowClose()" v-on:cancel="dialog_quit = false"/>
            </v-dialog>
            <div class="text-center">
                <v-dialog v-model="dialog_voice_loading" persistent color="#00cc99" width="200">
                    <v-card color="primary" dark >
                        <v-card-text>
                            <h2 v-if="action_processing == 1">A processar</h2>
                            <h2 v-if="action_processing == 0 && action_listening == 1">A ouvir</h2>
                            <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                        </v-card-text>
                    </v-card>
                </v-dialog>
            </div>
        </div>
    </v-container>
    <Opinion v-else/>
</template>

<script>
  import ModalLayout from './Modal_layout';
  import ImageDialog from './Image_dialog';
  import Break from './Break';
  import QuizzMonitorContent from './Quizz_monitor_content';

  export default {
    name: 'Question',

    components: {
        ModalLayout, ImageDialog, Break, QuizzMonitorContent
    },

    data: function () {
        return {
            frase:"", action_listening: 0, action_processing: 0, error_process_voice: 0, default_answer_value: "", out_of_range: 0, session_mode: "",
            correction: -1, correction_given_answer: 0, points: -1, current_question: {}, num_question: 1, final: false, dialog: false,
            points_given_answer: 0, start_time_answer_question: 0, end_time_answer_question: 0, label_answer: "", questions_found: 0,
            index_last_subdom_searched: -1, domain: "", sub_domains: [], progress_bar_current_size: 100, progress_bar_initial_size: 100, interval: 0, opacity: 0.0, height: 15,
            dialog_why: false, dialog_explain: false, dialog_rules: false, dialog_how: false, dialog_voice_loading: false, dialog_quit: false, dialog_layout: false, dialog_help: false, dialog_statistics: false, dialog_about: false, dialog_gam: false, dialog_monitor: false, dialog_image: false,
            alert: false, question_was_answered: 1, message: "Terminou o quizz", recorder: "", isOpen: false, look_for_monitor_content: false,
            request: { "method": "post", "url": "http://localhost:5000/voice/", "data": '', "processData": false, "contentType": false }
        }
    },
    watch: {
        default_answer(new_default_answer, old_default_answer){
            console.log("Valor antigo para o default answer:", old_default_answer)
            this.default_answer_value = new_default_answer
        },
        action_question(new_action_question, old_action_question){
            var current_action_next = this.$store.getters.action_next
            
            console.log("Valor de action question passou de", old_action_question, "para", new_action_question)

            if( (current_action_next == 1) && (new_action_question == 0) && (this.label_answer == "")){ this.dialog = true }
            else if ( (current_action_next == 1) && (new_action_question == 0) && (this.label_answer != "") ){
                this.set_end_time_answer_question()
                this.get_next_question()
            }
            else if ( (current_action_next == 0) && (new_action_question > 0) ){
                if(new_action_question > this.current_question.body.length){ this.out_of_range = 1 }
                else{
                    var selected_answer = this.current_question.body[new_action_question-1]

                    this.default_answer_value = selected_answer.answer
                    this.set_given_answer(selected_answer.correction, selected_answer.points, selected_answer.answer)
                }
            }
            else if ( (current_action_next == 1) && (new_action_question > 0) ){
                if(new_action_question > this.current_question.body.length){ this.out_of_range = 1 }
                else{
                    var choosen_answer = this.current_question.body[new_action_question-1]

                    this.default_answer_value = choosen_answer.answer
                    this.set_given_answer(choosen_answer.correction, choosen_answer.points, choosen_answer.answer)
                    this.set_end_time_answer_question()
                    this.get_next_question()
                }
            }
        },
        listening(new_listening, old_listening){
            console.log("Listening antigo:", old_listening)
            this.action_listening = new_listening
        },
        processing(new_processing, old_processing){
            console.log("Processamento antigo:", old_processing)
            this.action_processing = new_processing

            if( (new_processing == 0) && (this.action_listening == 0) ){ this.dialog_voice_loading = false }
        },
        error_processing_voice(new_error_processing_voice, old_error_processing_voice){
            this.error_process_voice = new_error_processing_voice
            console.log("Novo valor do erro: passou de", old_error_processing_voice, "para", new_error_processing_voice)
        },
        voice_action(old_voice_action, new_voice_action){ console.log("Ação da voz mudou de", old_voice_action, "para", new_voice_action) },
        progress_bar_current_size(){
            var current_question = this.$store.getters.get_session_question
            if(this.progress_bar_current_size <= (-100/parseInt(current_question.content['answering_time']))){
                clearInterval(this.interval)
                this.alert = true
            }
        },
        alert(){ if(this.alert == false){ this.start_progress_bar() } }
    },
    computed: {
        default_answer: {
            get(){ return this.default_answer_value },
            set(new_default_answer){ this.default_answer_value = new_default_answer }
        },
        action_next:            function(){ return this.$store.getters.action_next },
        action_question:        function(){ return this.$store.getters.action_question },
        listening:              function(){ return this.$store.getters.listening },
        processing:             function(){ return this.$store.getters.processing },
        voice_action:           function(){ return this.$store.getters.voice_action },
        error_processing_voice: function(){ return this.$store.getters.error_processing_voice }
    },
    async created(){
        await this.reset_variables()

        var val = Math.floor(Math.random() * 5);

        if( val == 0 ){
            var val_1 = Math.floor(Math.random() * 100);
            this.frase = String(val_1) + "% acertaram esta pergunta.";
        }
        if( val == 1 ){
            this.frase = "Já tens uma sequencia certa bastante elevada, tenta continuar assim";
        }
        if( val == 2 ){
            this.frase = "Se responderes a esta pergunta em menos de metade do tempo ganhas a carta Sonic Racoon";
        }
        if( val == 3 ){
            this.frase = "Cuidado com o tempo, mais um bocado e vais receber a carta Racoon";
        }
        if( val == 4 ){
            this.frase = "Se acertares esta pergunta ficas em numero 1 do ranking"
        }

        var quizz_parameters = this.$store.getters.get_quizz_parameters

        this.session_mode = quizz_parameters.session_mode

        var user = {
            id: quizz_parameters.id,
            username: quizz_parameters.username,
            name: quizz_parameters.name,
            email: quizz_parameters.email,
            user_type: quizz_parameters.user_type,
            gender: quizz_parameters.gender,
            degree: quizz_parameters.degree
        }

        this.domain = quizz_parameters.domain
        this.sub_domains = eval(quizz_parameters.subdomains)
        this.look_for_monitor_content = false

        await this.save_user(user)       
        let url = await this.get_domain()

        var current_user = this.$store.getters.get_session_user
        var user_url = '&id=' + current_user.id + '&username=' + current_user.username + '&name=' + current_user.name + '&email=' + current_user.email + '&gender=' + current_user.gender + '&degree=' + current_user.degree + '&user_type=' + current_user.user_type

        for(let i = 0; i<this.sub_domains.length;){
            await this.$http.get('http://localhost:5000/api/v0/evaluation/new?' + url + '&subdomain=' + this.sub_domains[i] + user_url)
                .then(result => {
                    var dictionary = JSON.parse(result.data)

                    if(Object.keys(dictionary.content).length == 0){ i += 1 }
                    else{
                        var session_question = {
                            content: dictionary.content,
                            number: dictionary.number,
                            thrown_at: dictionary.thrown_at
                        }

                        this.$store.commit('set_session_question', session_question)

                        var current_question = this.$store.getters.get_session_question

                        this.current_question = {
                            difficulty_level: current_question.content['difficulty_level'],
                            header: current_question.content['header'],
                            precedence: current_question.content['precedence'],
                            body: current_question.content['body'],
                            domain: current_question.content['domain']
                        }

                        this.start_progress_bar()
                        this.start_time_answer_question = new Date()
                        this.num_question = current_question.number               
                        this.questions_found = 1
                        this.index_last_subdom_searched = i
                        i = this.sub_domains.length
                        this.look_for_monitor_content = true
                    }
                })
                .catch(error => { throw(error) })   
        }

        if(this.questions_found == 0){
            this.final = true
            this.message = "Não tenho mais questões para ti, neste momento."
        }
    },

    methods: {
        async reset_variables(){
            await this.$store.commit('set_action_next', -1)
            await this.$store.commit('set_action_question', -1)
            await this.$store.commit('set_error_processing_voice', 0)
        },
        async get_domain() {
            var study_cycle = ""
            var scholarity = ""
            var domains = this.$store.getters.get_user_domains
            
            for(let i = 0; i<domains.length; i++) {
                if(domains[i].domain == this.domain){
                    study_cycle = domains[i].study_cycle,
                    scholarity = domains[i].scholarity

                    await this.$store.commit('set_session_domain', {study_cycle: study_cycle, scholarity: scholarity, description: this.domain })

                    let url = "study_cycle=" + study_cycle + "&scholarity=" + scholarity + "&description=" + this.domain

                    return url
                }
            }
        },
        set_end_time_answer_question(){ this.end_time_answer_question = new Date() },
        start_progress_bar() {
            var current_question = this.$store.getters.get_session_question
    
            clearInterval(this.interval)

            this.interval = setInterval(() => { this.progress_bar_current_size -= (100/parseInt(current_question.content['answering_time'])) }, 1000)
        },
        set_given_answer(correction_given_answer, points_given_answer, label_given_answer) {
            this.correction_given_answer = parseInt(correction_given_answer)
            this.points_given_answer = parseInt(points_given_answer)
            this.label_answer = label_given_answer
        },
        build_answer_db(current_user){
            var current_question = this.$store.getters.get_session_question
            var answer_time = this.end_time_answer_question - this.start_time_answer_question
            var answer_time_in_minutes = Math.round(((answer_time % 86400000) % 3600000) / 60000);
            var hours_throw_question = this.start_time_answer_question.getHours()
            var period_throw_question = (hours_throw_question < 7) ? "A" : ((hours_throw_question >= 7 && hours_throw_question < 12) ? "M" : ((hours_throw_question >= 12 && hours_throw_question < 21) ? "T" : ((hours_throw_question > 21) ? "N" : "")))
            var answer = {
                "user":{
                    "id": String(current_user.id),
                    "name": String(current_user.name),
                    "gender": String(current_user.gender),
                    "degree": String(current_user.degree)
                },
                "timetag":{
                    "date": this.end_time_answer_question,
                    "time": this.start_time_answer_question,
                    "period": period_throw_question
                },
                "question":{
                    "questionid":current_question.content['id'],
                    "language":current_question.content['language'],
                    "study_cycle":current_question.content['study_cycle'],
                    "scholarity":current_question.content['scholarity'],
                    "domain": current_question.content['domain'],               
                    "subdomain":current_question.content['subdomain'],
                    "subsubdomain":current_question.content['subsubdomain'],
                    "difficulty_level":current_question.content['difficulty_level'],
                    "display_mode":current_question.content['display_mode'],
                    "answering_time":current_question.content['answering_time'],
                    "type":current_question.content['type']
                },
                "answer":{
                    "start_time": this.start_time_answer_question,
                    "end_time": this.end_time_answer_question,
                    "answer_time": String(answer_time_in_minutes),
                    "correction": this.question_was_answered == 1 ? String(this.correction_given_answer) : "0",
                    "points": String(this.points_given_answer)
                }
            }

            return answer
        },
        build_answer_dw(current_user){
            var current_question = this.$store.getters.get_session_question
            var answer_time = this.end_time_answer_question - this.start_time_answer_question
            var answer_time_in_minutes = Math.round(((answer_time % 86400000) % 3600000) / 60000);
            var hours_throw_question = this.start_time_answer_question.getHours()
            var period_throw_question = (hours_throw_question < 7) ? "A" : ((hours_throw_question >= 7 && hours_throw_question < 12) ? "M" : ((hours_throw_question >= 12 && hours_throw_question < 21) ? "T" : ((hours_throw_question > 21) ? "N" : "")))
            var answer = {
                "Answer": {
                    "Answer_Start_Time": this.start_time_answer_question,
                    "Answer_End_Time": this.end_time_answer_question,
                    "Answer_Time": String(answer_time_in_minutes),
                    "Correction": this.question_was_answered == 1 ? String(this.correction_given_answer) : "0",
                    "Answer_Points": String(this.points_given_answer)
                },
                "Dim_Calendar": {
                    "Date": this.end_time_answer_question,
                    "Month": String(this.end_time_answer_question.toLocaleString("en-us", { month: "long" })),
                    "Quarter": String(Math.floor((this.end_time_answer_question.getMonth() + 3) / 3)),
                    "Semester": (Math.floor((this.end_time_answer_question.getMonth() + 3) / 3) <= 2) ? "1" : "2",
                    "Year": String(this.end_time_answer_question.getFullYear()),
                    "Week": String(this.end_time_answer_question.getDay()),
                    "Weekday": this.end_time_answer_question.toLocaleDateString("en-us", { weekday: 'long' })
                },
                "Dim_Time": this.start_time_answer_question,
                "Dim_Period": period_throw_question,
                "Dim_Language": current_question.content['language'],
                "Dim_User": {
                    "UserId": String(current_user.id),
                    "Name": String(current_user.name),
                    "Gender": String(current_user.gender),
                    "Degree": String(current_user.degree)
                },
                "Dim_Question": {
                    "QuestionId": current_question.content['id'],
                    "Study_Cycle": current_question.content['study_cycle'],
                    "Scholarity": current_question.content['scholarity'],
                    "Domain": current_question.content['domain'],
                    "Subdomain": current_question.content['subdomain'],
                    "Subsubdomain": current_question.content['subsubdomain'],
                    "Difficulty_Level": current_question.content['difficulty_level'],
                    "Answering_Time": current_question.content['answering_time'],
                    "Type": current_question.content['type']
                }
            }

            this.correction_given_answer = 0

            return answer
        },
        async get_next_question() {
            this.look_for_monitor_content = false

            var user = this.$store.getters.get_session_user
            var response_db = this.build_answer_db(user)
            var response_dw = this.build_answer_dw(user)

            this.questions_found = 0

            var i = ((this.index_last_subdom_searched + 1) < this.sub_domains.length) ? (this.index_last_subdom_searched + 1) : 0

            while(i<this.sub_domains.length){
                await this.$http.post('http://localhost:5000/api/v0/evaluation/next', {
                    'current_user': user,
                    'answerObjectDB': response_db,
                    'answerObjectDW': response_dw,
                    'answer': (this.question_was_answered == 1 ? this.label_answer : "Sem resposta"),
                    'question': this.$store.getters.get_session_question,
                    'domain': this.$store.getters.get_session_domain,
                    'subdomain': this.sub_domains[i]
                })
                    .then(async result => {
                        var dictionary = JSON.parse(result.data)

                        if(Object.keys(dictionary.content).length == 0){
                            if(i == this.index_last_subdom_searched){
                                this.questions_found = -1
                                i = this.sub_domains.length
                            }
                            else if((i + 1) >= this.sub_domains.length){ i = 0 }
                            else i += 1
                        }
                        else{
                            var session_question = {
                                content: dictionary.content,
                                number: dictionary.number,
                                thrown_at: dictionary.thrown_at
                            }

                            this.$store.commit('set_session_question', session_question)
                            var current_question = this.$store.getters.get_session_question

                            this.current_question = {
                                difficulty_level: current_question.content['difficulty_level'],
                                header: current_question.content['header'],
                                precedence: current_question.content['precedence'],
                                body: current_question.content['body'],
                                domain: current_question.content['domain']
                            }
                            this.progress_bar_current_size = 100
                            this.start_time_answer_question = new Date()
                            this.num_question = current_question.number
                            this.alert = false
                            this.error_process_voice = 0
                            this.out_of_range = 0
                            this.question_was_answered = 1
                            this.points_given_answer = 0
                            this.label_answer = ""
                            this.default_answer_value = ""
                            this.dialog = false
                            this.questions_found = 1
                            this.index_last_subdom_searched = i

                            await this.$store.commit('set_action_next', -1)
                            await this.$store.commit('set_action_question', -1)

                            i = this.sub_domains.length
                            this.look_for_monitor_content = true
                        }
                    })
                    .catch((error) => { throw(error) })
            }
            if(this.questions_found != 1){
                this.final = true
                this.message = "Não tenho mais questões para ti, neste momento."
            }
        },
        async save_user(user){
            let domains = []

            await this.$store.commit('set_user', user)
            await this.$http.get('http://localhost:5000/api/v0/evaluation/getDomains?idUser=' + user.id)
                .then(async dados => {
                    let doms = eval(dados.data)

                    for(let i = 0; i<doms.length; i++)
                        for(let j = 0; j<doms[i].domains.length; j++)
                            domains.push({ domain: doms[i].domains[j].description, study_cycle: doms[i].domains[j].study_cycle, scholarity: doms[i].domains[j].scholarity })

                    await this.$store.commit('set_user_domains', domains)
                }) 
                .catch(error => { throw(error) })
        },
        windowClose(){ window.close(); },
        async popupInquiry() {
            await this.$store.commit('set_inquiry_id', 'INPTQU0001')
            window.open('http://localhost:5000/evaluation/inquiry', '_blank', 'width=615, height=500');
        },
        get_action(){ this.$listen(this.recorder, this.request) }
    }
  }
</script>

<style>
button.v-btn[disabled] {
  opacity: 0.75;
}
</style>
