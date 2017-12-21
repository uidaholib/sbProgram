

//Script for dynamically creating the table
function buildProjectTable (reportDict) {
  $(document).ready(function (report) {
    // console.log("reportDict:")   //DeBug
    
    // console.log(reportDict);   //DeBug
    var report = reportDict.report;
    var reportDate = reportDict.date;
    // console.log('reportDate:');   //DeBug
    // console.log(reportDate);   //DeBug
    var reportIdentity = reportDict.identity;
    // console.log("reportIdentity:");   //DeBug
    // console.log(reportIdentity);   //DeBug
    var missing = reportDict.missing;
    var exceptions = reportDict.exceptions;
    // report ? console.log('reportStr Exists!') : console.log('Doesn\'t exist!');    //DeBug
    
    function build_table(report, reportDate, reportIdentity) {
      // console.log("report2: ");
      // console.log(report);
      var projectNumber = 0;
      var report_data = '';
      var arrayLength = report.length;
      for (var i = 0; i < arrayLength; i++) {
        // alert(report[i]);
        var reportData = report[i];
        // console.log("reportData")   //DeBug
        // console.log(reportData)   //DeBug
        var reportDateCurr = reportDate[i];
        // console.log("reportDateCurr")   //DeBug
        // console.log(reportDateCurr)   //DeBug
        var reportIdentityCurr = reportIdentity[i];
        // console.log("reportIdentityCurr")   //DeBug
        // console.log(reportIdentityCurr)   //DeBug
        arrayLength2 = reportData.length;
        for (var z = 0; z < arrayLength2; z++) {
          projectNumber++;
          var itemData = reportData[z];
          var itemDate = reportDateCurr['dateTime'];
          var itemCSC = reportIdentityCurr['CSC'];
          // console.log('itemData: ');   //DeBug
          // console.log(itemData);   //DeBug
          // console.log('itemDate: ');   //DeBug
          // console.log(itemDate);   //DeBug
          // console.log('itemIdentity: ');   //DeBug
          // console.log(itemCSC);   //DeBug
          report_data += '<tr id=\"p'+projectNumber+'\">\n';
          report_data += '<td>' + projectNumber + '</td>\n';
          report_data += '<td>' + itemCSC + '</td>\n';
          report_data += '<td>' + itemData.FY + '</td>\n';
          // report_data += '<td>' + itemData.ID + '</td>\n';
          report_data += '<td>' + itemData.ObjectType + '</td>\n';
          report_data += '<td> <a href="' + itemData.URL + '" target="_blank">' + itemData.name + '</a></td>\n';
          report_data += '<td>' + itemData.project + '</td>\n';
          report_data += '<td id="ElipseDataShort">' + itemData.DataInProject + '</td>\n';
          report_data += '<td id="ElipseDataLong">' + itemData.DataPerFile + '</td>\n';
          report_data += '<td id="ElipseDataShort">' + itemData.totalFYData + '</td>\n';
          report_data += '<td>' + itemDate.slice(0, -7) + '</td>\n';
          // report_data += '<td id="ElipseDataShort">' + itemData.RunningDataTotal + '</td>\n';
          report_data += '</tr>\n';
        }
      }
      $('#reportTable').append(report_data);
    };
    build_table(report, reportDate, reportIdentity);
  });
}