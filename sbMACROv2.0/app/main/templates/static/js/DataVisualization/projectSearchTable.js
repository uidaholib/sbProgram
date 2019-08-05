

//Script for dynamically creating the table
function buildProjectTable(projectArray) {
  $(document).ready(function () {
    function build_table(projectArray) {

      let projectNumber = 0;
      let report_data = '';
      for (var i = 0; i < projectArray.length; i++) {
        projectNumber++;
        let project = projectArray[i];
        report_data += '<tr id=\"p' + projectNumber + '\">\n';
        report_data += '<td>' + projectNumber + '</td>\n';
        if (Array.isArray(project.Fy)) {
          // First project.casc <td>
          report_data += '<td>';
          for (var i2 = 0; i2 < (project.Fy.length - 1); i2++) {
            report_data += project.casc[i2] + "</br>"
          }
          report_data += project.casc[i2] + '</td>\n';
          // Now project.fiscalyear <td>
          report_data += '<td>';
          for (var i2 = 0; i2 < (project.Fy.length - 1); i2++) {
            report_data += project.Fy[i2] + "</br>"
          }
          report_data += project.Fy[i2] + '</td>\n';
        }
        else {
          report_data += '<td>' + project.casc + '</td>\n';
          report_data += '<td>' + project.Fy + '</td>\n';
        }
        report_data += '<td> <a href="' + project.url + '" target="_blank">' + project.name + '</a></td>\n';
        report_data += '<td><button class="btn waves-effect waves-light modalbtn" id="modal_' + project.sb_id + '" onclick="displayModal(modal_' + project.sb_id + ')">More Info</button></td>\n';
        report_data += '<td style="display: none">' + project.url + '</td>\n';
        if (project.xml.toString() == 'true') {
          report_data += '<td id="ElipseDataShort" style="color: green;">' + '&#10003' + '</td>\n';
        }
        else if (project.xml.toString() == 'false') {
          report_data += '<td id="ElipseDataShort" style="color: red";">' + '&#10007' + '</td>\n';
        }
        else {
          report_data += '<td id="ElipseDataShort">' + '&#10134' + '</td>\n';
        }
        report_data += '<td id="ElipseDataShort">' + project.size + '</td>\n';
        report_data += '<td id="ElipseDataShort">' + project.ctitle + '</td>\n';
        report_data += '</tr>\n';
      }
      $('#reportTable').append(report_data);
    };
    build_table(projectArray);
    findModalBtns(projectArray);
  });
}