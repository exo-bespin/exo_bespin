/**
 * Various JS functions to support the ExoBespin web application.
 *
 * @author Matthew Bourque
 */

/**
 * Updates various compnents on the results page
 * @param {String} inst - The instrument of interest (e.g. "FGS")
 * @param {String} base_url - The base URL for gathering data from the AJAX view.
 */
function update_results() {
    $.ajax({
        url: 'http://127.0.0.1:8000/ajax/results/',
        success: function(data){

            $("#results")[0].innerHTML = 'Process Complete!!'
        }
    });
};