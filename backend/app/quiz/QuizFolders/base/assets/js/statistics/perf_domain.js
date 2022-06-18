(function() {
  var self = {};
  var arr_data1 = [];
  var arr_data2 = [];
  var chart_plot_01_settings = {
    series: {
      lines: {
        show: false,
        fill: true
      },
      splines: {
        show: true,
        tension: 0.4,
        lineWidth: 1,
        fill: 0.6
      },
      points: {
        radius: 0,
        show: true
      },
      shadowSize: 2
    },
    grid: {
      verticalLines: true,
      hoverable: true,
      clickable: true,
      tickColor: "#d5d5d5",
      borderWidth: 1,
      color: "#fff"
    },
    colors: ["#73879C","#2A3F54"],
    xaxis: {
      tickColor: "rgba(51, 51, 51, 0.06)",
      mode: "time",
      tickSize: [1, "month"],
      //tickLength: 10,
      axisLabel: "Date",
      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 12,
      axisLabelFontFamily: "Verdana, Arial",
      axisLabelPadding: 10
    },
    yaxis: {
      ticks: 8,
      tickColor: "rgba(51, 51, 51, 0.06)"
    },
    tooltip: false
  };
  var optionSet1 = {
    startDate: moment().subtract(29, "days"),
    endDate: moment(),
    minDate: "01/01/2019",
    maxDate: moment().subtract(1, "days"),
    dateLimit: {
      days: 60
    },
    showDropdowns: true,
    showWeekNumbers: true,
    timePicker: false,
    timePickerIncrement: 1,
    timePicker12Hour: true,
    ranges: {
      Today: [moment(), moment()],
      Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
      "Last 7 Days": [moment().subtract(6, "days"), moment()],
      "Last 30 Days": [moment().subtract(29, "days"), moment()],
      "This Month": [moment().startOf("month"), moment().endOf("month")],
      "Last Month": [
        moment()
          .subtract(1, "month")
          .startOf("month"),
        moment()
          .subtract(1, "month")
          .endOf("month")
      ]
    },
    opens: "left",
    buttonClasses: ["btn btn-default"],
    applyClass: "btn-small btn-primary",
    cancelClass: "btn-small",
    format: "DD/MM/YYYY",
    separator: " to ",
    locale: {
      applyLabel: "Validar",
      cancelLabel: "Cancelar",
      fromLabel: "From",
      toLabel: "To",
      customRangeLabel: "Custom",
      daysOfWeek: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
      monthNames: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
      ],
      firstDay: 1
    }
  };

  $(document).ready(function() {
    init_flot_chart();
    init_daterangepicker();
    initialize();
    updateGraphRespostas();
  });

  function initialize() {
    self.$widgetGraphRespostas = $("#widget-update-graph");
    self.$widgetSubdomains = $("#widget-update-subdomains");
  }

  var cb = function(start, end, label) {
    //Atualizar plot
      startD = start.format("YYYY-MM-DD").split("-");
    endD = end.format("YYYY-MM-DD").split("-");
    s = gd(parseInt(startD[0]), parseInt(startD[1]), parseInt(startD[2]));
    e = gd(parseInt(endD[0]), parseInt(endD[1]), parseInt(endD[2]));
    newArray1 = new Array();
    newArray2 = new Array();
    for (i = 0; i < arr_data1.length && i < arr_data2.length; i++) {
      if (arr_data1[i][0] >= s && arr_data1[i][0] <= e) {
        newArray1.push(arr_data1[i]);
      }
      if (arr_data2[i][0] >= s && arr_data2[i][0] <= e) {
        newArray2.push(arr_data2[i]);
      }
    }
    arr_data1 = newArray1;
    arr_data2 = newArray2;
    var plot = $.plot(
      $("#chart_plot_01"),
      [arr_data1, arr_data2],
      chart_plot_01_settings
    );
    plot.draw();
    console.log(start.toISOString(), end.toISOString(), label);
    $("#reportrange span").html(
      start.format("D MMMM, YYYY") + " - " + end.format("D MMMM, YYYY")
    );
  };

  async function getSubdomains(params, sel) {
    return await InternalAPI.statistics.distinct_subdomain(params).then(resp => {
      var res = JSON.parse(resp)
      for (i in res) {
        sel.append(
          $("<option></option>")
            .attr("value", res[i])
            .attr("selected", true)
            .text(res[i])
        );
      }
      subdom = self.$widgetSubdomains.find(".select_subdomain").val();
     // init_bar_SN_chart(res);
     // init_bar_SAVG_chart(res);
     // init_bar_gender(res);
      return subdom;
    });
  }

  function updateSubdomains(subdom) {
    var params_Answers = {
      domain: dom,
      subdomain: subdom
    };
    InternalAPI.statistics.answers_domain(params_Answers).done(response => {
      var res = JSON.parse(response);
      var lista_right = new Array();
      var lista_wrong = new Array();

      for (i in res) {
        data = res[i]._id.split("-");
        d = gd(parseInt(data[0]), parseInt(data[1]), parseInt(data[2]));
        right = new Array(d, parseInt(res[i].right_answers_subdomain));
        wrong = new Array(d, parseInt(res[i].wrong_answers_subdomain));
        lista_right.push(right);
        lista_wrong.push(wrong);
      }
      arr_data1 = lista_right;
      arr_data2 = lista_wrong;
      var plot = $.plot(
        $("#chart_plot_01"),
        [lista_right, lista_wrong],
        chart_plot_01_settings
      );
      plot.draw();
      var percRight = right[1] / (right[1] + wrong[1]);
      var percWrong = wrong[1] / (right[1] + wrong[1]);
      $("#progBarC").attr("value", percRight * 100);
      $("#progBarW").attr("value", percWrong * 100);
      optionSet1.minDate = moment(arr_data1[0][0]);
      optionSet1.maxDate = moment(arr_data1[arr_data1.length - 1][0]);
      $("#reportrange").daterangepicker(optionSet1, cb);
    });
  }

  async function updateGraphRespostas() {
    //SET DEFAULT VALUE
    sel = self.$widgetSubdomains.find(".select_subdomain");
    dom = self.$widgetGraphRespostas.find(".select_domain").val();
    var params = {
      domain: dom
    };
    subdom = await getSubdomains(params, sel);
    updateSubdomains(subdom);
    //-------------------
    self.$widgetGraphRespostas.find("select").on("change", event => {
      sel.empty();
      dom = self.$widgetGraphRespostas.find(".select_domain").val();
      params = {
        domain: dom
      };
      getSubdomains(params, sel).then(sub => {
        updateSubdomains(sub);
      });
    });

    self.$widgetSubdomains.find("select").on("change", event => {
      subdom = self.$widgetSubdomains.find(".select_subdomain").val();
      updateSubdomains(subdom);
    });
  }

  function init_flot_chart() {
    $.plot($("#chart_plot_01"), [arr_data1, arr_data2], chart_plot_01_settings);
  }

  function init_bar_SN_chart(res){
      if ($("#barChartSN").length) {
        var data_morris_bar = [];
        for (i in res) {
          var json = {
            subdominio: res[i]['_id'],
            numero: res[i]['total_questions']
          };
          data_morris_bar.push(json);
        }

        Morris.Bar({
          element: "barChartSN",
          data: data_morris_bar,
          xkey: "subdominio",
          ykeys: ["numero"],
          labels: ["#questões"],
          axes : 'x ',
          barRatio: 0.4,
          barColors: ["#2A3F54"],
          xLabelAngle: 35,
          hideHover: "auto",
          resize: true
        });
      }
  }

  function init_bar_SAVG_chart(res){
    if ($("#barChartSAVG").length) {
      var data_morris_bar = [];
      for (i in res) {
        var json = {
          subdominio: res[i]['_id'],
          numero: res[i]['answertime_avg_sub']
        };
        data_morris_bar.push(json);
      }

      Morris.Bar({
        element: "barChartSAVG",
        data: data_morris_bar,
        xkey: "subdominio",
        ykeys: ["numero"],
        labels: ["avg"],
        axes : 'x ',
        barRatio: 0.4,
        barColors: ["#2A3F54"],
        xLabelAngle: 35,
        hideHover: "auto",
        resize: true
      });
    }
  }

  function init_bar_gender(res){
    var subs=[];
    var data_f = [];
    var data_m = [];
    for (i in res) {
      subs.push(res[i]['_id']);
      data_f.push(res[i]['points_f_sub'])
      data_m.push(res[i]['points_m_sub'])
    }
    if ($("#mybarGenderSub").length) {
      var ctx = document.getElementById("mybarGenderSub");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: subs,
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
                  beginAtZero: true,
                  display: false
                },
              },
            ],
            xAxes: [
              {
                ticks: {
                  display: false
                },
              },
            ]
          },
        }
      });
    }
  }

  function init_daterangepicker() {
    if (typeof $.fn.daterangepicker === "undefined") {
      return;
    }
    console.log("init_daterangepicker");

    $("#reportrange span").html(
      moment()
        .subtract(29, "days")
        .format("MMMM, D, YYYY") +
        " - " +
        moment().format("MMMM, D, YYYY")
    );
    $("#reportrange").daterangepicker(optionSet1, cb);
    $("#reportrange").on("show.daterangepicker", function() {
      console.log("show event fired");
    });
    $("#reportrange").on("hide.daterangepicker", function() {
      console.log("hide event fired");
    });
    $("#reportrange").on("apply.daterangepicker", function(ev, picker) {
      console.log(
        "apply event fired, start/end dates are " +
          picker.startDate.format("DD, MM, YYYY") +
          " to " +
          picker.endDate.format("DD, MM, YYYY")
      );
    });
    $("#reportrange").on("cancel.daterangepicker", function(ev, picker) {
      console.log("cancel event fired");
    });
    $("#options1").click(function() {
      $("#reportrange")
        .data("daterangepicker")
        .setOptions(optionSet1, cb);
    });
    $("#options2").click(function() {
      $("#reportrange")
        .data("daterangepicker")
        .setOptions(optionSet2, cb);
    });
    $("#destroy").click(function() {
      $("#reportrange")
        .data("daterangepicker")
        .remove();
    });
  }
})(jQuery);
