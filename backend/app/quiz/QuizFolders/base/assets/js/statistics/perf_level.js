(function() {
  

  $(document).ready(function() {
    initialize();
  });

  function initialize() {
    newBarChart();
  }

  function newBarChart() {
    // Bar chart
    InternalAPI.statistics.answers_level().then(response => {
      var res = JSON.parse(response);
      var levels = [];
      var data_corretas = [];
      var data_incorretas = [];
      var data_avg = [];
      for (i in res) {
        levels.push(res[i]._id);
        data_corretas.push(res[i].right_answers_subdomain);
        data_incorretas.push(res[i].wrong_answers_subdomain);
        data_avg.push(res[i].answertime_avg_level);
      }
      //Respostas por nivel
      if ($("#mybarChart").length) {
        var ctx = document.getElementById("mybarChart");
        var mybarChart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: levels,
            datasets: [
              {
                label: "Corretas",
                backgroundColor: "#73879C",
                data: data_corretas
              },
              {
                label: "Incorretas",
                backgroundColor: "#2A3F54",
                data: data_incorretas
              }
            ]
          },

          options: {
            scales: {
              yAxes: [
                {
                  ticks: {
                    beginAtZero: true
                  }
                }
              ]
            }
          }
        });
      }

      //Tempo médio por nivel answertime_avg_level
      if ($("#graph_bar").length) {
        var data_morris_bar = [];
        for (i in levels) {
          var json = {
            level: "Nivel " + levels[i],
            avg: data_avg[i]
          };
          data_morris_bar.push(json);
        }

        Morris.Bar({
          element: "graph_bar",
          data: data_morris_bar,
          xkey: "level",
          ykeys: ["avg"],
          labels: ["Tempo médio"],
          barRatio: 0.4,
          barColors: ["#2A3F54"],
          xLabelAngle: 35,
          hideHover: "auto",
          resize: true
        });
      }
    });

  InternalAPI.statistics.score_level().then(response => {
    var res = JSON.parse(response);
    var levels=[];
    var data_f = [];
    var data_m = [];
    for (i in res) {
      levels.push(res[i]._id);
      data_f.push(res[i].points_f_level)
      data_m.push(res[i].points_m_level)
    }
    if ($("#mybarChartPoints").length) {
      var ctx = document.getElementById("mybarChartPoints");
      var mybarChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: levels,
          datasets: [
            {
              label: "Feminino",
              backgroundColor: "#73879C",
              data: data_f
            },
            {
              label: "Masculino",
              backgroundColor: "#2A3F54",
              data: data_m
            }
          ]
        },

        options: {
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true
                }
              }
            ]
          }
        }
      });
    }
  });

    var tallness = $("#left").height() - 10;
    $("#graph_bar").height(tallness);

    // $( window ).resize(function() {
    //   var tallness = $("#left").height()-10;
    //   alert("depois"+tallness)
    // $("#graph_bar").height(tallness);
    // });
  }
})();
