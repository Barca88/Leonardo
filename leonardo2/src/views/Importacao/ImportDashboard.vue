<template>
    <v-app>
        <div>
            <div class="greyBG">
                <h2>Importação de Questões</h2>
            </div>
            <div class="selectBoxs">
                <div class="list_domains">
                    <v-select
                        v-model="domain"
                        :items="domains"
                        label="Domínios"
                        ref="selectedDomain"
                        v-on:change="selectBy"
                    ></v-select>
                </div>
                <div class="list_editors">
                    <v-select
                        v-model="author"
                        :items="editors"
                        label="Editores"
                        ref="selectedAuthor"
                        v-on:change="selectBy"
                    ></v-select>
                </div>
                <v-btn v-on:click="refresh" class="im-btn" dark>
                    <v-icon>mdi-refresh</v-icon>
                </v-btn>
            </div>

            <div class="statistics">
                <div class="outerQuestions greyBG">
                    <div class="questionsHeader greyBG">
                        <h3> Questões </h3>
                    </div>
                    <div class="questions greyBG">
                        <div class="numericQuestions">
                            <div class="nQ_box">
                                <div class="nQ_text"> Importadas </div>
                                <div class="nQ_number"> {{ this.stats.imported }} </div>
                            </div>
                            <div class="nQ_box">
                                <div class="nQ_text"> Rejeitadas </div>
                                <div class="nQ_number"> {{ this.stats.rejected }} </div>
                            </div>
                            <div class="nQ_box">
                                <div class="nQ_text"> Validadas </div>
                                <div class="nQ_number"> {{ this.stats.validated }} </div>
                            </div>
                        </div>
                        <div id="doughnut" style="width: 300px; height: 300px"></div>
                    </div>
                </div>
                <div class="processing greyBG">
                    <h3 style="margin-left:10px"> Processamento de Questões </h3>
                    <div id="bars" style="width: 400px; height: 300px">
                    </div>
                </div>
                <div class="errors greyBG">
                    <h3 style="margin-left:10px"> Log de Erros </h3>
                    <div class="list_errors">
                        <li v-for="e in errors" :key="e.id">
                            {{ formatDate(e.createdAt) }} {{ e.header }} {{ e.type }}
                        </li>
                    </div>
                </div>
            </div>

            <div class="greyBG">
                <h3>Ficheiros importados</h3>
            </div>
            <div class="list_imported">
                <li v-for="log in importedData" :key="log.id">
                    {{ formatDate(log.date) }} {{ log.type }} {{ log.name }} {{ log.size }} {{ log.number }}
                </li>
            </div>
        </div>
        <GenericAlert :alertPopup="alertPopup"/>
    </v-app>
</template>

<script>
import GenericAlert from '../../components/Importacao/GenericAlert.vue'
import axios from 'axios'
import anychart from 'anychart'
import moment from 'moment'

export default {
      metaInfo:{
      title:'Leonardo-Dashboard'
    },
    data () {
        return {
            items: {},
            importedData: {},
            stats: {},
            domains: [],
            editors: [],
            alertPopup: {},
            errors: {},
            barChart: undefined,
            seriesBarChart: [],
            chart: undefined,
            chartInitialized: false,
            statsPromise: undefined,
            domain: undefined,
            author: undefined
        }
    },
    components:{
        GenericAlert
    },
    created() {
        this.loadQuestions();
    },
    async mounted() {
        await this.createCharts();
    },
    methods: {
        updateValue(json, question){
            json.imported += 1;
            if(question.flag === "aproved") json.validated += 1;
            else if(question.flag === "rejected") json.rejected += 1;
        },
        dayDifference (d1, d2){
            const moment = require('moment');
            var jsD1 = moment(d1, "YYYY-MM-DD").toDate();
            var jsD2 = moment(d2, "YYYY-MM-DD").toDate();

            const diffTime = Math.abs(jsD2 - jsD1);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            return diffDays;
        },
        generateStats: function (questions) {
            var rejected = questions.filter(q => q['flag'] === "rejected")
            var aproved = questions.filter(q => q['flag'] === "aproved")
            var json = {imported: questions.length, rejected: rejected.length, validated: aproved.length}

            // Sort the filtered data (should come sorted from the db)
            /*questions.sort(this.sortByDate);*/
            /*filtered.sort(this.sortByDate);*/

            // Construct the weekly stats
            var fixedDate = questions[0].inserted_at;
            var week = 1, i = 0;
            var weekQuestions = [];
            for (var q of questions){
                i++;
                // Compare with fixed date
                // If it blongs to the same week then add it to the list of the current week
                // Otherwise check which week it is and update the accumulatting variables
                var diffDays = this.dayDifference(fixedDate, q.inserted_at);
                if(diffDays <= 7 && !(i == questions.length)) weekQuestions.push(q);
                else {
                    if (i == questions.length) weekQuestions.push(q);
                    // Go through the old week questions and build the weekly stats
                    var tmp = {imported: 0, rejected: 0, validated: 0}
                    for(var question of weekQuestions) {
                        this.updateValue(tmp, question);
                    }

                    // Only update json if weekQuestions add any question
                    if(weekQuestions.length) json[week] = tmp;

                    // Reset the variables
                    fixedDate = q.inserted_at;
                    week = Math.ceil(diffDays / 7);
                    weekQuestions = [q]
                }
            }

            return json;
        },
        loadQuestions: function () {
            // Get the questions and obtain a list of domains and editors of those questions
          axios.get("http://localhost:1318/imported_questions", {}).then((resp) => {
            this.items = resp.data;
            this.domains = Array.from(this.items.map(obj => obj['domain']));
            this.editors = Array.from(this.items.map(obj => obj['author']));
            // Generate stats for the graphs
            this.stats = this.generateStats(this.items);
            console.log(this.stats)
            this.statsPromise(this.stats)
          });
          // Get the imported data for the imported scrollable section
          axios.get("http://localhost:1318/imported_info", {}).then((resp) => {
            this.importedData = resp.data;
          });
          // Load errors for the error scrollable section
          axios.get("http://localhost:1318/imported_errors", {}).then((resp) => {
            this.errors = resp.data;
          });
        },
        formatDate: function (d) {
            return moment(d).format("YYYY-MM-DD hh:mm");
        },
        printItems: function(){
            console.log(this.domains);
        },
        async refresh (){
            // Clean select boxes
            this.$refs["selectedDomain"].reset();
            this.$refs["selectedAuthor"].reset();

            // Do the startup promise
            this.loadQuestions();
            await this.createCharts();
        },
        async selectBy () {
            var query = "http://localhost:1318/imported_questions/stats"

            // Check if domain or author are unfulfilled and build the query
            if(this.author == undefined) query = query + "ByDomain/" + this.domain;
            else if(this.domain == undefined) query = query + "ByAuthor/" + this.author;
            else query = query + "ByBoth/" + this.author + "/" + this.domain;

            // Load data from endpoint
            axios.get(query, {}).then(resp => {
                this.stats = this.generateStats(resp.data);
                this.statsPromise(this.stats)
            });

            // Re-create every chart
            await this.createCharts();
        },
        async waitForStats () {
            return new Promise(v => {
                this.statsPromise = v
            })
        },
        createBarGraph () {
            // iterate through weekly stats and build the columns
            const weeklyKeys = Object.keys(this.stats).filter(key => !isNaN(key));
            const weeklyValues = new Array(3);

            for (var x = 0; x < 3; x++) weeklyValues[x] = new Array(weeklyKeys.length);

            var i = 0;
            for (const key in this.stats){
                // If the key is a number build a column
                if(!isNaN(key)){
                    weeklyValues[0][i] = [key, this.stats[key].imported];
                    weeklyValues[1][i] = [key, this.stats[key].rejected];
                    weeklyValues[2][i] = [key, this.stats[key].validated];
                }
                i++;
            }

            // If it has been initialized just update the data
            if(this.seriesBarChart.length){
                for (const col in weeklyValues){
                    this.seriesBarChart[col].data(weeklyValues[col]);
                }
            } else {
                // create a chart
                this.barChart = anychart.column();

                // create a column series and set the data
                for (const col in weeklyValues) {
                    this.seriesBarChart.push(this.barChart.column(weeklyValues[col]));
                }

                // Name the columns and color them
                this.seriesBarChart[0].name("Importadas");
                this.seriesBarChart[0].normal().fill("#2D35E7")
                this.seriesBarChart[0].normal().stroke("#242BCC")

                this.seriesBarChart[1].name("Rejeitadas");
                this.seriesBarChart[1].normal().fill("#CC3024")
                this.seriesBarChart[1].normal().stroke("#CC3024")

                this.seriesBarChart[2].name("Validadas");
                this.seriesBarChart[2].normal().fill("#55CC24")
                this.seriesBarChart[2].normal().stroke("#55CC24")

                // Set the interval on y axis
                this.barChart.yScale().ticks().interval(1);

                // Set the x axis as scrollable
                this.barChart.xScroller(true);
                var thumbs = this.barChart.xScroller().thumbs();
                thumbs.autoHide(true);
                thumbs.hovered().fill('#FFD700');
                this.barChart.xZoom().setToPointsCount(10,false);

                // Set the padding
                this.barChart.barsPadding(0);

                // set the titles of the axes
                this.barChart.xAxis().title("Semana");
                this.barChart.yAxis().title("Nr Questões");

                // set the container id
                this.barChart.container("bars");

                // set background color
                this.barChart.background().fill("#e6e6e6")

                // initiate drawing the chart
                this.barChart.draw();
            }
        },
        createDoughnutChart () {
            // Create doughnut chart
            var data = [
              {x: "Rejeitadas", value: this.stats.rejected},
              {x: "Validadas", value: this.stats.validated}
            ];

            // create a pie chart and set the data
            if(this.chartInitialized) this.chart.data(data);
            else {
                this.chart = anychart.pie(data);
                this.chartInitialized = true;

                /* set the inner radius
                (to turn the pie chart into a doughnut chart)*/
                this.chart.innerRadius("50%");

                // set the container id
                this.chart.container("doughnut");

                // set the palette
                var palette = ["#00b300", "#D3D3D3"]
                this.chart.palette(palette)

                // set background color
                this.chart.background().fill("#e6e6e6")

                // initiate drawing the chart
                this.chart.draw();
            }
        },
        async createCharts (){
            // Wait for created() to finish
            await this.waitForStats();

            this.createDoughnutChart();
            this.createBarGraph();
        }
    }
}
</script>

<style scoped>
.greyBG{
    background-color: #e6e6e6;
}

div.list_imported{
    background-color: #e6e6e6;
    overflow: auto;
    height: 100px;
}

div.list_domains{
    width: 400px;
    margin-right: 200px;
}

div.list_editors{
    width: 200px;
    margin-right: 300px;
}

div.selectBoxs{
    background-color: #e6e6e6;
    display: flex;
    margin-bottom: 20px;
}

div.questions{
    height: 300px;
    width: 500px;
    display: flex;
}

div.processing{
    margin-right: 20px;
    height: 400px;
}

div.statistics{
    display: flex;
    margin-bottom: 20px;
    height: 400px;
}

div.nQ_box{
    display: flex;
    margin-bottom: 20px;
}

div.nQ_text{
    margin-right: 20px;
    height: 50px;
    width: 80px;
    line-height: 50px;
    text-align: center;
    vertical-align: middle;
}

div.nQ_number{
    background-color: #80ff80;
    width: 120px;
    height: 50px;
    line-height: 50px;
    text-align: center;
    vertical-align: middle;
}

div.numericQuestions{
    width: 200px;
    height: 100px;
}

div.questionsHeader{
    margin-left: 100px;
    margin-bottom: 10px;
}

div.list_errors{
    background-color: #e6e6e6;
    overflow: auto;
    width: 415px;
    height: 360px;
}

div.outerQuestions{
    margin-right: 20px;
}
</style>
