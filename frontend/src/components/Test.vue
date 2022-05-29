<template>
    <v-card max-width="444" class="mx-auto">
      <v-list two-line>
        <v-list-item> {{ test_question["header"] }} </v-list-item>
      </v-list>
      <v-carousel :continuous="false" :cycle="cycle" :show-arrows="false" hide-delimiter-background>
        <v-carousel-item v-for="(ans, i) in test_question['body']" :key="i">
          <v-sheet tile light>
            <v-row align="center" justify="center">
                <v-container>
                    <v-card-text> {{ ans["answer"] }} </v-card-text>
                    <v-container>
                        <v-radio-group v-model="value_answer" light>
                            <v-radio color="#00cc99" :value="`Verdadeiro`" :key="1" :label="`Verdadeiro`" @change="save_answer('verdadeiro', i)"></v-radio>
                            <v-radio color="#00cc99" :value="`Falso`" :key="2" :label="`Falso`" @change="save_answer('falso', i)"></v-radio>
                        </v-radio-group>
                    </v-container>
                </v-container>
            </v-row>
          </v-sheet>
        </v-carousel-item>
      </v-carousel>
      <v-btn @click="send_answers()">Enviar resposta</v-btn>
    </v-card>
</template>

<script>
  export default {
    name: 'Info',
    data: function () {
        return {
            cycle: false,
            test_question: {
                "id" : "PTEINSBDSQL021",
                "language" : "pt",
                "study_cycle" : "Ensino Superior",
                "scholarity" : "Engenharia Informática",
                "domain" : "Sistemas de Bases de Dados",
                "subdomain" : "SQL",
                "subsubdomain" : "",
                "difficulty_level" : "3",
                "display_mode" : "G",
                "answering_time" : "60",
                "type" : "",
                "precedence" : [ ],
                "repetitions" : "0",
                "header" : "A query 'INSERT INTO Alunos VALUES ('1','João Manuel Castro', 'MIEI'), ('2','Sílvia do Canto', 'LCC');' permite fazer:",
                "body" : [
                    {
                        "answer" : "Nada, uma vez que a query não está bem definida.",
                        "correction" : "0",
                        "mandatory" : "0",
                        "eliminative" : "0",
                        "points" : "0"
                    },
                    {
                        "answer" : "A inserção de um novo registo na tabela Alunos.",
                        "correction" : "0",
                        "mandatory" : "0",
                        "eliminative" : "0",
                        "points" : "0"
                    },
                    {
                        "answer" : "A inserção de um conjunto de registos na tabela Alunos, desde que a ordem dos valores apresentados siga o esquema da tabela.",
                        "correction" : "1",
                        "mandatory" : "1",
                        "eliminative" : "0",
                        "points" : "1"
                    },
                    {
                        "answer" : "A inserção não pode ser realizada, uma vez que a operação envolve mais do que um registo.",
                        "correction" : "0",
                        "mandatory" : "0",
                        "eliminative" : "0",
                        "points" : "0"
                    },
                    {
                        "answer" : "Dá erro, uma vez que a instrução apresentada tem erros de sintaxa.",
                        "correction" : "0",
                        "mandatory" : "0",
                        "eliminative" : "0",
                        "points" : "0"
                    },
                    {
                        "answer" : "Nenhuma das anteriores.",
                        "correction" : "0",
                        "mandatory" : "1",
                        "eliminative" : "0",
                        "points" : "0"
                    }
                ],
                "solution" : "",
                "images" : "",
                "videos" : "",
                "source" : "Belo, O., Cadernos de Problemas - Sistemas de Bases de Dados, Departamento de Informática, Escola de Engenharia, Universidade do Minho, 2021",
                "notes" : "Para utilização exclusiva da plataforma educacional Leonardo",
                "status" : "E",
                "inserted_by" : "Belo, O",
                "inserted_at" : "2021-01-31",
                "validated_by" : "",
                "validated_at" : ""
            },
            labels_per_question_answer: {}
        }
    },
    computed: {
        value_answer: {
            get(){ return "" },
            set(){ return "" }
        }   
    },
    methods: {
        save_answer(answer_label, question_answer){ this.labels_per_question_answer[question_answer] = answer_label },
        send_answers(){
            console.log("Pretendo enviar as respostas do utilizador")        
            console.log("Objeto que contém as respostas por question answer:", this.labels_per_question_answer)
        }
    }
  }
</script>

<style>
   .v-carousel__controls{
       background: white !important
   }
   .v-carousel__controls__item{
      color: grey !important
   }
</style>