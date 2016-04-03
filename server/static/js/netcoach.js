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
    plot:NaN
}

/* Function: initializer
 * ---------------------
 * Initializes everything when the DOM loads
 */
$(document).ready(function() {
    refreshSeriesList();
    refreshPlot();
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
var refreshPlotData = function(plot_id) {
    return $.ajax({
        type:'POST',
        url:'/get_plot_data',
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(data) {
            data.type = 'scatter';
            globalState.plotData = data;
        },
        error: function() {
            alert("Error: could not refresh plot data");
        }
    })
}

/* Function: refreshPlot
 * ---------------------
 * Updates the graph with new data
 */
var refreshPlot = function() {
    var graphData = globalState.plotData;
    graphData.type = 'scatter';
    debugger;
    Plotly.newPlot('mainGraph', graphData);
}
