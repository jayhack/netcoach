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
    seriesList: [] //contains ids of all series available to plot
}

/* Function: initializer
 * ---------------------
 * Initializes everything when the DOM loads
 */
$(document).ready(function() {

    //=====[ Step 1: Initialize Graph ]=====
    refreshSeriesList();


   var trace1 = {
      x: [1, 2, 3, 4],
      y: [10, 15, 13, 17],
      type: 'scatter'
    };

    var trace2 = {
      x: [1, 2, 3, 4],
      y: [16, 5, 11, 9],
      type: 'scatter'
    };

    var data = [trace1, trace2];

    Plotly.newPlot('mainGraph', data);

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

/* Function: getPlotData
 * ---------------------
 * Given a plot id, returns all data to be plotted
 * Formatted as
 * [{'ts':timestamp, 'val':value}]
 */
var refreshPlotData = function(plot_id) {
    return $.ajax({
        type:'POST',
        url:'/get_plot_data',
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(data) {
            alert("");
        }
    })
}

/* Function: refreshPlot
 * ---------------------
 * NotImplementedError
 */

