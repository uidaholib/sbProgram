

//Script for dynamically creating the table
function buildProjectTable (projectArray) {
  $(document).ready(function () {
    function build_table(projectArray) {

      let projectNumber = 0;
      let report_data = '';
      for (var i = 0; i < projectArray.length; i++) {
        projectNumber++;
        let project = projectArray[i];
        report_data += '<tr id=\"p'+projectNumber+'\">\n';
        report_data += '<td>' + projectNumber + '</td>\n';
        if (Array.isArray(project.fiscal_year)) {
          // First project.casc <td>
          report_data += '<td>';
          for (var i2=0; i2 < (project.casc.length - 1); i2++){
            report_data += project.casc[i2] + "</br>"
          }
          report_data += project.casc[i2] + '</td>\n';
          // Now project.fiscalyear <td>
          report_data += '<td>';
          for (var i2 = 0; i2 < (project.fiscal_year.length - 1); i2++) {
            report_data += project.fiscal_year[i2] + "</br>"
          }
          report_data += project.fiscal_year[i2] + '</td>\n';
        }
        else {
          report_data += '<td>' + project.casc + '</td>\n';
          report_data += '<td>' + project.fiscal_year + '</td>\n';
        }
        // report_data += '<td>' + itemData.ID + '</td>\n';
        report_data += '<td>' + project.obj_type + '</td>\n';
        report_data += '<td> <a href="' + project.url + '" target="_blank">' + project.name + '</a></td>\n';
        report_data += '<td><button class="btn waves-effect waves-light modalbtn" id="modal_' + project.sb_id + '" onclick="displayModal(modal_' + project.sb_id + ')">More Info</button></td>\n';
        report_data += '<td id="ElipseDataShort">' + project.data_in_project_GB + '</td>\n';
        report_data += '<td id="ElipseDataLong">' + project.num_of_files + '</td>\n';
        if (Array.isArray(project.total_data_in_fy_GB)) {
          // First project.total_data_in_fy_GB <td>
          report_data += '<td id="ElipseDataShort">';
          for (var i2=0; i2 < (project.total_data_in_fy_GB.length - 1); i2++) {
            report_data += project.total_data_in_fy_GB[i2] + "</br>"
          }
          report_data += project.total_data_in_fy_GB[i2] + '</td>\n';
        } else {
           report_data += '<td id="ElipseDataShort">' + project.total_data_in_fy_GB + '</td>\n';
        }
        report_data += '<td>' + "Retrieved " + moment(project.timestamp).fromNow() + '</td>\n';
        report_data += '</tr>\n';
      }
      $('#reportTable').append(report_data);
    };
    build_table(projectArray);
    findModalBtns(projectArray);
  });
}