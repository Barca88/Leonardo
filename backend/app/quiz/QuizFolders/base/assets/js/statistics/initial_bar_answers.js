(function() {
    $(document).ready(function() {
      initialize();
      addDiv();
    });
  
    function initialize() {
      self.$widgetInitialBar = $("#widget_initial_bar");
    }

    function addDiv(){
        InternalAPI.statistics.general_answers().then(response => {
            var res = JSON.parse(response);
            var divDom= '<div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">'+
            '<span class="count_top"><i class="fa fa-database"></i> Domínios</span>'+
            '<div class="count">'+res.total.domains+'</div>'+
            '<span class="count_bottom"><i class="green"><i class="fa fa-sort-asc"></i>'+res.semana.dom_sem+'</i> Na última semana</span>'+
            '</div>'
            var divRespC = '<div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">'+
            '<span class="count_top"><i class="fa fa-database"></i> Respostas Certas</span>'+
            '<div class="count">'+res.total.res_certas+'</div>'+
            '<span class="count_bottom"><i class="green"><i class="fa fa-sort-asc"></i>'+res.semana.rc_sem+'</i> Na última semana</span>'+
            '</div>'
            var divRespE = '<div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">'+
            '<span class="count_top"><i class="fa fa-database"></i> Respostas Erradas</span>'+
            '<div class="count">'+res.total.res_erradas+'</div>'+
            '<span class="count_bottom"><i class="green"><i class="fa fa-sort-asc"></i>'+res.semana.re_sem+'</i> Na última semana</span>'+
            '</div>'
            var divTmp_resp = '<div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">'+
            '<span class="count_top"><i class="fa fa-clock-o"></i> Tempo médio de Resposta</span>'+
            '<div class="count">'+res.total.total_time+'</div>'+
            '<span class="count_bottom"><i class="green"><i class="fa fa-sort-asc"></i>'+res.semana.ttime_sem+'</i> Na última semana</span>'+
            '</div>'
            var divEval = '<div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">'+
            '<span class="count_top"><i class="fa fa-star"></i> Avaliações</span>'+
            '<div class="count">'+res.total.total_docs+'</div>'+
            '<span class="count_bottom"><i class="green"><i class="fa fa-sort-asc"></i>'+res.semana.av_sem+'</i> Na última semana</span>'+
            '</div>'
            $widgetInitialBar.append(divDom)
            $widgetInitialBar.append(divRespC)
            $widgetInitialBar.append(divRespE)
            $widgetInitialBar.append(divTmp_resp)
            $widgetInitialBar.append(divEval)

        })
    }
})();