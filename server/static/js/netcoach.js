/* Script: netcoach
 * ================
 * Contains main functionality for "netcoach" app
 * written in javascript, jQuery and plotly.js
 */

/*###################################################################*/
/*############## GLOBALS AND INITIALIZATION #########################*/
/*###################################################################*/

/* Var: GlobalState
 * ----------------
 * Contains all global information
 */
var globalState = {
    seriesList: [], //contains ids of all series available to plot
    plotData:[], //contains current plot data
    plotLayout: {
        autosize: false,
        width: 1000,
        height: 500,
        margin: {
            l: 50,
            r: 50,
            b: 100,
            t: 100,
            pad: 4
        },
    },
}

/* Function: initializer
 * ---------------------
 * Initializes everything when the DOM loads
 */
$(document).ready(function() {
    refreshSeriesList();
    refreshPlotData('char_rnn_32');
})


/*###################################################################*/
/*############## GLOBALS AND INITIALIZATION #########################*/
/*###################################################################*/

/* Function: refreshSeriesList
 * ---------------------------
 * refreshes globalState.seriesList via ajax request
 */
var refreshSeriesList = function() {
    return $.ajax({
        type:'POST',
        url:'/get_series_list',
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(data) {
            globalState.seriesList = data;
            $("#series-list").empty();
            globalState.seriesList.map(function(series_name) {
                var li = $("<li>", {
                                    id:series_name,
                                    text:series_name,
                                    click:function() {refreshPlotData(series_name);}
                                    });
                $("#series-list").append(li);
            });
        },
        error: function() {
            alert("Error: could not refresh available series");
        }
    })
}

/* Function: refreshPlotData
 * -------------------------
 * Given a plot id, returns all data to be plotted
 * Should be called every second or so once the plot is up
 */
var refreshPlotData = function(series_name) {
    return $.ajax({
        type:'GET',
        url:'/get_series',
        data:{'series_name':series_name},
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(data) {
            data.type = 'scatter';
            globalState.plotData = data;
            data.style = 'scatter'
            Plotly.newPlot('main-graph', [globalState.plotData], globalState.plotLayout);
        },
        error: function() {
            alert("Error: could not refresh plot data");
        }
    })
}
