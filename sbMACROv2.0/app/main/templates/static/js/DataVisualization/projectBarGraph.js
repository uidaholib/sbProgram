function getShortParentIdentity(project) {
  let casc_short = shortenCascName(project.casc)
  let fy_short = project.fiscal_year.replace('FY ', '')
  return casc_short + ' ' + fy_short
}

function projectBarGraph(projectArray) {
  $(document).ready(function () {
    let cascs = {}
    for (var i = 0; i < projectArray.length; i++) {
      let currProj = projectArray[i]
      let currProjCascShort = shortenCascName(currProj.casc)
      if (!cascs.hasOwnProperty(currProjCascShort)) {
        // Casc project array has not been created.
        cascs[currProjCascShort] = []
      }
      let projObj = {}
      projObj.name = currProj.name
      projObj.size = currProj.data_in_project_GB
      projObj.number = (i + 1).toString()
      projObj.FY = currProj.fiscal_year.replace('FY ', '')
      projObj.casc = currProjCascShort
      cascs[currProjCascShort].push(projObj)
    }

    //Get to each casc in cascs
    //Check which size is the max size of all data.
    let maxSize = 0
    for (var casc in cascs) {
      if (cascs.hasOwnProperty(casc)) {
        let currCascMax = getMaxSize(cascs[casc])
        maxSize = currCascMax > maxSize ? currCascMax : maxSize
      }
    }

    if (maxSize > 0) {
      for (var casc in cascs) {
        if (cascs.hasOwnProperty(casc)) {
          let currCascMax = getMaxSize(cascs[casc])
          if (currCascMax > 0) {
            createGraph(cascs[casc], casc, maxSize)
          } else {
            createNoDataProjGraph(casc)
          }
        }
      }
      //else, if the maxSize of all CASCs is not greater than 0, create NoData graphs for all
    } else {
      for (var casc in cascs) {
        if (cascs.hasOwnProperty(casc)) {
          createNoDataProjGraph(casc)
        }
      }
    }
  })
}

var getMaxSize = function (objArray) {
  var maxSize = 0
  for (var i = 0; i < objArray.length; i++) {
    // console.log("current size: " + objArray[i].size);    //Debug
    // console.log("MaxSize: " + maxSize);    //Debug
    maxSize = objArray[i].size > maxSize ? objArray[i].size : maxSize
  }
  return maxSize
}

function createNoDataProjGraph(currCSC) {
  // set the dimensions and margins of the graph
  var margin = {
      top: 40,
      right: 20,
      bottom: 30,
      left: 60
    },
    width = 960 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom
  //Should set width and height dynamically
  updateFYDimensions(window.innerWidth, window.innerHeight)
  //Come back to this to change graph layout for small screen sizes
  var breakPoint = 768
  // set the ranges
  var y = d3.scaleLinear().range([0, height])

  var x = d3.scaleLinear().range([0, width])

  // append the svg object to the body of the page
  // append a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  var svg = d3
    .select('#fyGraphWrapper')
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .attr('id', 'FYGraph_svg')
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

  // Scale the range of the data in the domains
  x.domain([0, 100])
  // y.domain(d3.range(data.length));
  y.domain([0, 100])
  //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

  // append the rectangles for the bar chart

  //Adding x axis label
  svg
    .append('text')
    .attr('y', 0.1 * height)
    .attr('x', width / 2)
    .attr('dy', '1em')
    .attr('font-size', '1.2em')
    .attr('font-style', 'italic')
    .style('fill', 'grey')
    .style('text-anchor', 'middle')
    .text('Selected ' + currCSC + ' Projects')

  svg
    .append('text')
    .attr('y', 0.3 * height)
    .attr('x', width / 2)
    .attr('dy', '1em')
    .attr('font-size', '1.2em')
    .attr('font-style', 'italic')
    .style('fill', 'grey')
    .style('text-anchor', 'middle')
    .text('contain no data')

  //Adding a title
  svg
    .append('text')
    .attr('x', width / 2)
    .attr('y', 0 - margin.top / 2)
    .attr('text-anchor', 'middle')
    .style('font-size', '20px')
    .style('text-decoration', 'underline')
    .text('ScienceBase Project Size Comparison-- ' + currCSC)

  //Updating dimensions
  function updateFYDimensions(winWidth, winHeight) {
    margin.top = 40
    margin.right = winWidth < breakPoint ? 0 : 20
    margin.left = winWidth < breakPoint ? 0 : 50
    margin.bottom = 30

    width = winWidth * 0.5 - margin.left - margin.right
    height = winHeight * 0.25
  }
}

// tree map begin

// function createGraph(data, currCSC, DATA_max) {
//   // console.log("In createGraph");
//   // var data = projectObjArray;
//   // set the dimensions and margins of the graph

//   'use strict';

//   const margin = {
//       top: 40,
//       right: 10,
//       bottom: 10,
//       left: 10
//     },
//     width = 960 - margin.left - margin.right,
//     height = 500 - margin.top - margin.bottom,
//     color = d3.scaleOrdinal().range(d3.schemeCategory20c);

//   const treemap = d3.treemap().size([width, height]);

//   const div = d3.select("#wrapper").append("div")
//     .style("position", "relative")
//     .style("width", (width + margin.left + margin.right) + "px")
//     .style("height", (height + margin.top + margin.bottom) + "px")
//     .style("left", margin.left + "px")
//     .style("top", margin.top + "px");

//   data.forEach(function (d) {
//     d.size = +d.size;
//   });
//   const root = d3.hierarchy(data, (d) => d.name)
//     .sum((d) => d.size);

//   const tree = treemap(root);

//   const node = div.datum(data).selectAll(".node")
//     .data(tree.leaves())
//     .enter().append("div")
//     .attr("class", "node")
//     .style("left", (d) => d.x0 + "px")
//     .style("top", (d) => d.y0 + "px")
//     .style("width", (d) => Math.max(0, d.x1 - d.x0 - 1) + "px")
//     .style("height", (d) => Math.max(0, d.y1 - d.y0 - 1) + "px")
//     .style("background", (d) => color(d.size))
//     .text((d) => d.size);

//   d3.selectAll("input").on("change", function change() {
//     const value = this.value === "count" ?
//       (d) => {
//         return d.number ? 1 : 0;
//       } :
//       (d) => {
//         return d.size;
//       };

//     const newRoot = d3.hierarchy(data, (d) => d.number)
//       .sum(value);

//     node.data(treemap(newRoot).leaves())
//       .transition()
//       .duration(1500)
//       .style("left", (d) => d.x0 + "px")
//       .style("top", (d) => d.y0 + "px")
//       .style("width", (d) => Math.max(0, d.x1 - d.x0 - 1) + "px")
//       .style("height", (d) => Math.max(0, d.y1 - d.y0 - 1) + "px")
//   });

//Tree MAP end

//vertical graph begin

function createGraph(data, currCSC, DATA_max) {
  //console.log('In createGraph')
  //var data = projectObjArray
  // set the dimensions and margins of the graph
  var margin = {
      top: 40,
      right: 20,
      bottom: 30,
      left: 40
    },
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom
  // //Should set width and height dynamically
  updateDimensions(data, window.innerWidth, window.innerHeight)

  //Come back to this to change graph layout for small screen sizes
  var breakPoint = 768
  // set the ranges
  var x = d3
    .scaleBand()
    .range([0, width])
    .padding(0.1)
  var y = d3.scaleLinear().range([height, 0])

  // append the svg object to the body of the page
  // append a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  var svg = d3
    .select('#wrapper')
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .attr('id', 'projectGraph_svg')
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

  // get the data

  // format the data
  data.forEach(function (d) {
    d.size = +d.size
  })
  console.log(data)

  // Scale the range of the data in the domains
  x.domain(
    data.map(function (d) {
      return d.number
    })
  )
  y.domain([
    0,
    d3.max(data, function (d) {
      return d.size
    })
  ])

  //Adding labels for amount of each bar

  //d3-tip: http://bl.ocks.org/davegotz/bd54b56723c154d25eedde6504d30ad7
  // Setup the tool tip.
  // See original documentation for more details on styling: http://labratrevenge.com/d3-tip/
  var tool_tip = d3
    .tip()
    .attr('class', 'd3-tip')
    .offset([0, 0])
    .html(function (d) {
      var rStr = d.size.toString().substring(0, 4)
      var rFY = d.FY
      var rCSC = d.casc
      if (parseFloat(rStr) < 0.01) {
        rStr = 'Less than 0.01'
      } else {
        rStr = '~' + rStr
      }
      return (
        'Science Center: ' +
        rCSC +
        '<br>' +
        'Fiscal Year: ' +
        rFY +
        '<br>' +
        'Project Number: ' +
        d.number +
        '<br>' +
        rStr +
        'gb'
      )
    })
  svg.call(tool_tip)

  // append the rectangles for the bar chart
  svg
    .selectAll('.bar')
    .data(data)
    .enter()
    .append('rect')
    //.attr('class', 'bar')
    .attr('class', function (d) {
      return 'bar ' + d.casc + 'CASC'
    })
    .attr('id', function (d) {
      return 'FY' + d.FY
    })
    .attr('x', function (d) {
      return x(d.number)
    })
    .attr('width', x.bandwidth())
    .attr('y', function (d) {
      return y(d.size)
    })
    .attr('height', function (d) {
      return height - y(d.size)
    })
    .style('color', 'orange')
    .on('click', function (d) {
      let id
      if (d.number > 2) {
        let num = d.number - 2
        id = 'p' + num
      } else {
        id = 'table_head'
      }

      document.getElementById(id).scrollIntoView()
    })
    .on('mouseover', tool_tip.show)
    .on('mouseout', tool_tip.hide)

  // add the x Axis
  svg
    .append('g')
    .attr('transform', 'translate(0,' + height + ')')
    .call(d3.axisBottom(x))

  // add the y Axis
  svg.append('g').call(d3.axisLeft(y))

  // add the x-axis label

  svg
    .append('text')
    .attr('y', height + margin.bottom / 2)
    .attr('x', width)
    .attr('dy', '1em')
    .attr('font-size', '.8em')
    .style('text-anchor', 'end')
    //.text('Gigabytes (GB)')
    .text('Project Number')

  // add y-axis label
  // svg
  //   .append('text')
  //   .attr('y', -margin.top - 2)

  //   .attr('x', -margin.left)
  //   .attr('dy', '1em')
  //   .attr('font-size', '.8em')
  //   .style('text-anchor', 'end')
  //   .attr('transform', 'rotate(-90)')
  //   .text('Gigabytes (GB)')

  //.text('Project Number')

  //Adding a title
  svg
    .append('text')
    .attr('x', width / 2)
    .attr('y', 0 - margin.top / 2)
    .attr('text-anchor', 'middle')
    .style('font-size', '20px')
    .style('text-decoration', 'underline')
    .text('ScienceBase Project Size Comparison-- ' + currCSC + 'CASC')

  // vertical graph end

  //original begin

  // function createGraph(data, currCSC, DATA_max) {
  //   // console.log("In createGraph");
  //   // var data = projectObjArray;
  //   // set the dimensions and margins of the graph
  //   var margin = {
  //       top: 40,
  //       right: 20,
  //       bottom: 30,
  //       left: 40
  //     },
  //     width = 960 - margin.left - margin.right,
  //     height = 500 - margin.top - margin.bottom
  //   //Should set width and height dynamically
  //   updateDimensions(data, window.innerWidth, window.innerHeight)

  //   //Come back to this to change graph layout for small screen sizes
  //   var breakPoint = 768
  //   // set the ranges
  //   var y = d3
  //     .scaleBand()
  //     .range([0, height])
  //     .padding(0.1)

  //   var x = d3.scaleLinear().range([0, width])

  //   // append the svg object to the body of the page
  //   // append a 'group' element to 'svg'
  //   // moves the 'group' element to the top left margin
  //   var svg = d3
  //     .select('#wrapper')
  //     .append('svg')
  //     .attr('width', width + margin.left + margin.right)
  //     .attr('height', height + margin.top + margin.bottom)
  //     .attr('id', 'projectGraph_svg')
  //     .append('g')
  //     .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

  //   // format the data
  //   data.forEach(function (d) {
  //     d.size = +d.size
  //   })

  //   // Scale the range of the data in the domains
  //   // x.domain([0, d3.max(data, function(d){ return d.size; })])
  //   //Instead of normal ^, we must use max of both datasets for both graphs.
  //   x.domain([0, DATA_max])
  //   y.domain(
  //     data.map(function (d) {
  //       return d.number
  //     })
  //   )
  //   //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

  //   //Adding labels for amount of each bar

  //   //d3-tip: http://bl.ocks.org/davegotz/bd54b56723c154d25eedde6504d30ad7
  //   // Setup the tool tip.
  //   // See original documentation for more details on styling: http://labratrevenge.com/d3-tip/
  //   var tool_tip = d3
  //     .tip()
  //     .attr('class', 'd3-tip')
  //     .offset([0, 0])
  //     .html(function (d) {
  //       var rStr = d.size.toString().substring(0, 4)
  //       var rFY = d.FY
  //       var rCSC = d.casc
  //       if (parseFloat(rStr) < 0.01) {
  //         rStr = 'Less than 0.01'
  //       } else {
  //         rStr = '~' + rStr
  //       }
  //       return (
  //         'Science Center: ' +
  //         rCSC +
  //         '<br>' +
  //         'Fiscal Year: ' +
  //         rFY +
  //         '<br>' +
  //         'Project Number: ' +
  //         d.number +
  //         '<br>' +
  //         rStr +
  //         'gb'
  //       )
  //     })
  //   svg.call(tool_tip)

  //   // append the rectangles for the bar svg
  //   svg
  //     .selectAll('.bar')
  //     .data(data)
  //     .enter()
  //     // .append("svg:a")
  //     //   .attr("xlink:href", "#"+d.number)
  //     .append('rect')
  //     .attr('class', function (d) {
  //       return 'bar ' + d.casc + 'CASC'
  //     })
  //     // .attr("class", function (d) { console.log(d.casc); return d.casc; })
  //     .attr('id', function (d) {
  //       return 'FY' + d.FY
  //     })
  //     //.attr("x", function(d) { return x(d.sales); })
  //     .attr('width', function (d) {
  //       return x(d.size)
  //     })
  //     .attr('y', function (d) {
  //       return y(d.number)
  //     })
  //     .attr('height', y.bandwidth())
  //     .on('click', function (d) {
  //       let id
  //       if (d.number > 2) {
  //         let num = d.number - 2
  //         id = 'p' + num
  //       } else {
  //         id = 'table_head'
  //       }

  //       document.getElementById(id).scrollIntoView()
  //     })
  //     .on('mouseover', tool_tip.show)
  //     .on('mouseout', tool_tip.hide)

  //   // add the x Axis
  //   svg
  //     .append('g')
  //     .attr('transform', 'translate(0,' + height + ')')
  //     .call(d3.axisBottom(x))

  //   // add the y Axis
  //   svg.append('g').call(d3.axisLeft(y))

  //   //Adding x axis label
  // svg
  //   .append('text')
  //   .attr('y', height + margin.bottom / 2)
  //   .attr('x', width)
  //   .attr('dy', '1em')
  //   .attr('font-size', '.8em')
  //   .style('text-anchor', 'end')
  //   .text('Gigabytes (GB)')

  // //Adding a title
  // svg
  //   .append('text')
  //   .attr('x', width / 2)
  //   .attr('y', 0 - margin.top / 2)
  //   .attr('text-anchor', 'middle')
  //   .style('font-size', '20px')
  //   .style('text-decoration', 'underline')
  //   .text('ScienceBase Project Size Comparison-- ' + currCSC + 'CASC')

  //original end

  //Adding Legend
  var legendRectSize = 18
  var legendSpacing = 4

  var existing_FYs = []

  for (var i = 0; i < data.length; i++) {
    if ($.inArray(data[i].FY, existing_FYs) === -1) {
      // the value is not in the array
      existing_FYs.push(data[i].FY)
    }
  }

  var legend = svg
    .selectAll('.legend')
    .data(
      data.filter(function (d) {
        var index = $.inArray(d.FY, existing_FYs)
        if (index > -1) {
          // the value is in the array
          //remove element from array
          existing_FYs.splice(index, 1)
          //use this d:
          return d
        } else {
          //do nothing (skip this d)
        }
      })
    )
    .enter()
    .append('g')
    .attr('class', 'legend')
    .attr('id', function (d) {
      return 'FY' + d.FY
    })
    .attr('transform', function (d, i) {
      // var height = legendRectSize + legendSpacing;
      // var offset = height * data.length / 2;
      // var horz = -2 * legendRectSize;
      // var vert = i * height - offset;
      var horz = width * 0.85
      var vert = i * 18
      return 'translate(' + horz + ',' + vert + ')'
    })

  legend
    .append('rect')
    .attr('class', function (d) {
      return 'legend ' + currCSC + 'CASC'
    })
    .attr('id', function (d) {
      return 'FY' + d.FY
    })
    .attr('width', legendRectSize)
    .attr('height', legendRectSize)

  legend
    .append('text')
    .attr('x', legendRectSize + legendSpacing)
    .attr('y', legendRectSize - legendSpacing)
    .text(function (d) {
      return 'FY ' + d.FY
    })

  // var legendBackground = svg.selectAll(".legend-wrapper")
  // .append('g')
  // .append("class", "legend-wrapper")
  // .attr('transform', 'translate(100,100)')
  // .append("rect")
  //   .attr("class", "legend-wrapper")
  //   .attr("x", 10)
  //   .attr("y", 10)
  //   .attr("width", 100)
  //   .attr("height", 100);

  //Updating dimensions
  function updateDimensions(data, winWidth, winHeight) {
    // console.log("In UPdateDimensions");

    margin.top = 40
    margin.right = winWidth < breakPoint ? 0 : 20
    margin.left = winWidth < breakPoint ? 0 : 40
    margin.bottom = 30

    width = winWidth * 0.5 - margin.left - margin.right
    var barRelativeSize = 70 + 10 * data.length
    var widthRelativeSize = 0.5 * width
    height =
      widthRelativeSize > barRelativeSize ? widthRelativeSize : barRelativeSize
    // widthRelativeSize > barRelativeSize ? console.log("widthRelativeSize") : console.log("barRelativeSize");
    if (barRelativeSize > window.innerHeight) {
      height = winHeight * 0.5
      // console.log("Height = window.innerHeight");
    }
    // console.log("End updateDimensions");
  }
}

// d3.select(window).on('resize', createGraph(projectObjArray));
// function catchResize () {
//   console.log("Resized1!");
//   d3.select("#projectGraph_svg").remove();
//   d3.select("#projectGraph_svg").remove(); //once for each CSC
//   projectBarGraph(projectArray);
//   d3.select("#fyGraphWrapper").remove();
//   FY_BarGraph(projectArray);

// }
// // d3.select(window).on('resize', go);
// window.addEventListener('resize', catchResize);
// addEvent(window, "resize", function (event) {
//   console.log('resized');
// });