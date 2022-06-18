(function() {
  $(document).ready(function() {
    initialize();
  });

  function initialize() {
    newLineChart();
  }

  function newLineChart() {
    InternalAPI.statistics.answers_degree().then(response => {
      var res = JSON.parse(response);
      keys = Object.keys(res);
      var points_degree_data = {};
      var max_dates=[];

      for(i in keys){
          points_degree_data[keys[i]]=[]
          max_dates.push({
                    data:new Date(res[keys[i]][res[keys[i]].length-1]._id),
                    key:keys[i]
                })
        for (j in res[keys[i]]) {
            new_date = new Date(res[keys[i]][j]._id);
            points_degree_data[keys[i]].push([new_date, res[keys[i]][j].points_degree]);
        }
        //alert(points_degree_data);
    }
    const min_max_DataObj = max_dates.reduce(function(prev, current) {
        return (prev.data < current.data) ? prev : current
    })

      var points_degree_settings = {
        grid: {
          show: true,
          aboveData: true,
          color: "#3f3f3f",
          labelMargin: 10,
          axisMargin: 0,
          borderWidth: 0,
          borderColor: null,
          minBorderMargin: 5,
          clickable: true,
          hoverable: true,
          autoHighlight: true,
          mouseActiveRadius: 100
        },
        series: {
          lines: {
            show: true,
            fill: true,
            lineWidth: 2,
            steps: false
          },
          points: {
            show: true,
            radius: 4.5,
            symbol: "circle",
            lineWidth: 3.0
          }
        },
        legend: {
          position: "ne",
          margin: [0, -25],
          noColumns: 0,
          labelBoxBorderColor: null,
          labelFormatter: function(label, series) {
            return label + "&nbsp;&nbsp;";
          },
          width: 40,
          height: 1
        },
        colors: [
          "#73879C",
          "#2A3F54",
          "#515356",
          "#23527c",
          "#f7cb38",
          "#5a8022",
          "#2c7282"
        ],
        shadowSize: 0,
        tooltip: true,
        tooltipOpts: {
          content: "%s: %y.0",
          xDateFormat: "%d/%m",
          shifts: {
            x: -30,
            y: -50
          },
          defaultTheme: false
        },
        yaxis: {
          min: 0
        },
        xaxis: {
          mode: "time",
          minTickSize: [1, "day"],
          timeformat: "%d/%m/%y",
          min: points_degree_data[min_max_DataObj.key][0][0],
          max: min_max_DataObj.data
        }
      };
      //alert(points_degree_data)
      if ($("#points_degree_chart").length) {
        console.log("Plot2");
        data_flot = [];
        for (i in keys) {
          json_label = {
            label: keys[i],
            data: points_degree_data[keys[i]],
            lines: {
              fillColor: "rgba(150, 202, 89, 0.12)"
            },
            points: {
              fillColor: "#fff"
            }
          };
          data_flot.push(json_label);
        }

        $.plot($("#points_degree_chart"), data_flot, points_degree_settings);
      }
    });

    InternalAPI.statistics.top_users().then(response => {
        var res = JSON.parse(response);
        for(i in res){
            $("#lista_top_alunos").append(
            '<li class="media event">'+
            '<div class="media-body">'+
            '<a class="title" href="#">'+ res[i]._id.name +'</a>'+
            '<p><strong>Pontuação:</strong>'+res[i].points_user+'</p>'+
            '<p><strong>Curso:</strong>'+res[i]._id.degree+'</p></div></li>'
            );
        }
    });
  }
})();
